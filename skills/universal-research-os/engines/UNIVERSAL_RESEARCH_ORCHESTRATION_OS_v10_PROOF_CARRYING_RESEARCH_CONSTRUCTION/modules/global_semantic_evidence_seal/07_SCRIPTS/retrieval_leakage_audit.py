from __future__ import annotations

import argparse
import ast
import re
import io
import tokenize
from pathlib import Path

from common import ensure_relative, glob_many, load_json, normalize_text, parse_markdown, sha256_file, write_json


def load_nodes(root: Path, cfg: dict) -> dict[str, list[str]]:
    nodes: dict[str, list[str]] = {}
    for p in glob_many(root, cfg.get("knowledge_globs", ["knowledge/**/*.md"])):
        fm, _ = parse_markdown(p)
        node_id = str(fm.get("id", ""))
        if not node_id:
            continue
        aliases = fm.get("aliases", []) or []
        if isinstance(aliases, str):
            aliases = [aliases]
        nodes[node_id] = [str(fm.get("title", ""))] + [str(x) for x in aliases]
    return nodes


def code_without_strings_and_comments(source: str) -> str:
    try:
        tokens = []
        for tok in tokenize.generate_tokens(io.StringIO(source).readline):
            if tok.type in {tokenize.STRING, tokenize.COMMENT}:
                tokens.append((tok.type, ""))
            else:
                tokens.append((tok.type, tok.string))
        return tokenize.untokenize(tokens)
    except Exception:
        return source


def runner_static_findings(source: str) -> list[dict]:
    findings: list[dict] = []
    code = code_without_strings_and_comments(source)
    lines = code.splitlines()

    # High-confidence static checks only. Evaluation-only references to expected_ids
    # and negative_ids are reported separately as P2 manual review.
    for i, line in enumerate(lines):
        low = line.lower()
        window = " ".join(x.lower() for x in lines[max(0, i-3):i+2])
        if re.search(r"scores?\s*\[.*\]\s*(?:\+=|-=|=)", low):
            if "expected" in window:
                findings.append({"severity": "P1", "code": "EXPECTED_ID_SCORE_USE", "line": i + 1})
            if "negative" in window:
                findings.append({"severity": "P1", "code": "NEGATIVE_ID_SCORE_USE", "line": i + 1})
            if "title" in window and ("bonus" in window or "+=" in low):
                findings.append({"severity": "P1", "code": "EXACT_TITLE_BONUS", "line": i + 1})
            if "alias" in window and ("bonus" in window or "+=" in low):
                findings.append({"severity": "P1", "code": "ALIAS_BONUS", "line": i + 1})
        if "expected" in window and re.search(r"(?:neighbor|neighbour|related|graph|expand)", window):
            if re.search(r"expected_ids?", window):
                findings.append({"severity": "P1", "code": "EXPECTED_GRAPH_EXPANSION", "line": i + 1})
        if re.search(r"(?:write_text|json\.dump|json\.dumps)", low) and re.search(r"benchmark|test_cases", window):
            findings.append({"severity": "P1", "code": "GENERATOR_IN_RUNNER", "line": i + 1})

    # De-duplicate repeated windows.
    unique = []
    seen = set()
    for finding in findings:
        key = (finding["code"], finding.get("line"))
        if key not in seen:
            unique.append(finding)
            seen.add(key)
    findings = unique
    try:
        tree = ast.parse(source)
        names = {n.id for n in ast.walk(tree) if isinstance(n, ast.Name)}
        if "expected_ids" in names or "negative_ids" in names:
            findings.append({"severity": "P2", "code": "RUNNER_REFERENCES_EVALUATION_FIELDS", "note": "Manual review required. Evaluation-only use can be legitimate."})
    except SyntaxError:
        findings.append({"severity": "P1", "code": "RUNNER_SYNTAX_ERROR"})
    return findings


def main() -> int:
    ap = argparse.ArgumentParser(description="Audit a frozen retrieval benchmark for answer leakage and runner policy violations.")
    ap.add_argument("--config", required=True)
    args = ap.parse_args()
    cfg = load_json(Path(args.config))
    root = Path(cfg.get("repaired_root", cfg["baseline_root"]))
    out = Path(cfg["output_dir"])
    benchmark_path = ensure_relative(root, cfg["benchmark_json"])
    manifest_path = ensure_relative(root, cfg["benchmark_manifest_json"])
    runner_path = ensure_relative(root, cfg["runner_source"])
    metrics_path = ensure_relative(root, cfg["retrieval_metrics_json"])

    bench = load_json(benchmark_path)
    manifest = load_json(manifest_path)
    metrics = load_json(metrics_path) if metrics_path.exists() else {}
    nodes = load_nodes(root, cfg)
    findings: list[dict] = []

    expected_hash = manifest.get("benchmark_sha256", "")
    actual_hash = sha256_file(benchmark_path)
    if expected_hash != actual_hash:
        findings.append({"severity": "P1", "code": "BENCHMARK_HASH_MISMATCH", "expected": expected_hash, "actual": actual_hash})
    if not manifest.get("frozen_before_runner_execution", False):
        findings.append({"severity": "P1", "code": "NOT_FROZEN_BEFORE_RUN"})
    if not manifest.get("runner_must_not_import_generator", False):
        findings.append({"severity": "P1", "code": "RUNNER_GENERATOR_SEPARATION_NOT_ASSERTED"})

    leaks = []
    for test in bench.get("tests", []):
        query = " " + normalize_text(str(test.get("query", ""))) + " "
        for node_id in test.get("expected_ids", []):
            for term in nodes.get(node_id, []):
                nt = normalize_text(term)
                if len(nt) >= 3 and f" {nt} " in query:
                    leaks.append({"test_id": test.get("test_id"), "expected_id": node_id, "term": term})
        if not test.get("negative_ids"):
            findings.append({"severity": "P2", "code": "TEST_WITHOUT_HARD_NEGATIVE", "test_id": test.get("test_id")})
    if leaks:
        findings.append({"severity": "P1", "code": "TITLE_ALIAS_LEAKAGE", "count": len(leaks)})

    source = runner_path.read_text(encoding="utf-8", errors="replace")
    findings.extend(runner_static_findings(source))
    policy = metrics.get("runner_policy", metrics.get("metrics", {}).get("runner_policy", {}))
    required_false = ["test_generation_inside_runner", "exact_title_bonus", "alias_bonus", "negative_id_score_exclusion", "graph_expected_id_expansion"]
    for key in required_false:
        if policy.get(key) is not False:
            findings.append({"severity": "P1", "code": "RUNNER_POLICY_NOT_FALSE", "field": key, "value": policy.get(key)})
    if policy.get("negative_ids_used_only_for_evaluation") is not True:
        findings.append({"severity": "P1", "code": "NEGATIVE_IDS_POLICY_NOT_EVALUATION_ONLY"})

    tests = bench.get("tests", [])
    holdout = [t for t in tests if t.get("split") == "holdout" or t.get("is_holdout") is True]
    holdout_ratio = len(holdout) / len(tests) if tests else 0
    if holdout_ratio < 0.30:
        findings.append({"severity": "P1", "code": "HOLDOUT_RATIO_TOO_LOW", "ratio": holdout_ratio})
    if any(str(t.get("contamination_status", "CLEAN")).upper() not in {"CLEAN", ""} for t in holdout):
        findings.append({"severity": "P1", "code": "CONTAMINATED_HOLDOUT"})

    p1 = [x for x in findings if x["severity"] in {"P0", "P1"}]
    summary = {
        "status": "PASS" if not p1 else "FAIL",
        "tests": len(tests),
        "holdout_tests": len(holdout),
        "holdout_ratio": round(holdout_ratio, 4),
        "title_alias_leak_count": len(leaks),
        "benchmark_sha256": actual_hash,
        "runner_sha256": sha256_file(runner_path),
        "findings": findings,
        "leaks": leaks,
    }
    write_json(out / "retrieval_leakage_audit.json", summary)
    print({k: v for k, v in summary.items() if k not in {"findings", "leaks"}})
    return 0 if summary["status"] == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
