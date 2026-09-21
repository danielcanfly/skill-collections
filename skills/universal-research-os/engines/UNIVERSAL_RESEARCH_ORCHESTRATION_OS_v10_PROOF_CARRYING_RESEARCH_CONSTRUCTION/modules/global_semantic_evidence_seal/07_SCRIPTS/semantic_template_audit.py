from __future__ import annotations

import argparse
import re
import statistics
from collections import Counter
from pathlib import Path

from common import glob_many, load_json, normalize_text, parse_markdown, write_csv, write_json


def semantic_lines(body: str, excluded_headings: list[str], min_chars: int) -> list[str]:
    if excluded_headings:
        names = "|".join(re.escape(x) for x in excluded_headings)
        body = re.split(rf"^##\s+(?:{names})\s*$", body, flags=re.M)[0]
    lines: list[str] = []
    for raw in body.splitlines():
        s = raw.strip()
        if not s or s.startswith("#") or s.startswith("|"):
            continue
        if re.match(r"^-\s*`?[A-Z]{2,}[-_:]", s):
            continue
        s = normalize_text(s)
        if len(s) >= min_chars:
            lines.append(s)
    return lines


def collect(root: Path, cfg: dict) -> dict[str, dict]:
    active = set(cfg.get("active_statuses", ["production"]))
    semantic_types = set(cfg.get("semantic_types", ["Concept", "Pattern", "Checklist"]))
    excluded = cfg.get("semantic_excluded_headings", [])
    min_chars = int(cfg.get("semantic_min_line_chars", 30))
    items: dict[str, dict] = {}
    for p in glob_many(root, cfg.get("knowledge_globs", ["knowledge/**/*.md"])):
        if p.name.lower() == "index.md":
            continue
        fm, body = parse_markdown(p)
        if str(fm.get("status", "")) not in active or str(fm.get("type", "")) not in semantic_types:
            continue
        node_id = str(fm.get("id") or p.relative_to(root))
        items[node_id] = {
            "path": str(p.relative_to(root)),
            "title": str(fm.get("title", "")),
            "lines": semantic_lines(body, excluded, min_chars),
        }
    return items


def score(items: dict[str, dict], repeat_threshold: int) -> dict[str, float]:
    counts: Counter[str] = Counter()
    for item in items.values():
        counts.update(set(item["lines"]))
    return {
        node_id: (sum(counts[x] >= repeat_threshold for x in item["lines"]) / len(item["lines"]) if item["lines"] else 0.0)
        for node_id, item in items.items()
    }


def summarise(scores: dict[str, float]) -> dict:
    vals = list(scores.values())
    return {
        "pages": len(vals),
        "mean": round(sum(vals) / len(vals), 4) if vals else 0,
        "median": round(statistics.median(vals), 4) if vals else 0,
        "pages_ge_0_30": sum(x >= 0.30 for x in vals),
        "pages_ge_0_50": sum(x >= 0.50 for x in vals),
        "max": round(max(vals), 4) if vals else 0,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="Detect repeated semantic prose across knowledge nodes.")
    ap.add_argument("--config", required=True)
    args = ap.parse_args()
    cfg = load_json(Path(args.config))
    out = Path(cfg["output_dir"])
    repeat_threshold = int(cfg.get("semantic_repeat_doc_threshold", 4))

    baseline = collect(Path(cfg["baseline_root"]), cfg)
    repaired_root = Path(cfg.get("repaired_root", cfg["baseline_root"]))
    repaired = collect(repaired_root, cfg)
    before = score(baseline, repeat_threshold)
    after = score(repaired, repeat_threshold)

    rows = []
    for node_id in sorted(set(before) | set(after)):
        item = repaired.get(node_id) or baseline.get(node_id) or {}
        b, a = before.get(node_id, 0.0), after.get(node_id, 0.0)
        rows.append({
            "canonical_id": node_id,
            "path": item.get("path", ""),
            "title": item.get("title", ""),
            "duplicate_ratio_before": f"{b:.4f}",
            "duplicate_ratio_after": f"{a:.4f}",
            "delta": f"{a-b:.4f}",
            "after_gate": "PASS" if a < 0.30 else "FAIL",
        })

    bsum, asum = summarise(before), summarise(after)
    status = "PASS" if asum["pages_ge_0_30"] == 0 and asum["mean"] < 0.15 else "FAIL"
    metrics = {"status": status, "repeat_doc_threshold": repeat_threshold, "before": bsum, "after": asum}
    write_csv(out / "semantic_template_audit.csv", rows)
    write_json(out / "semantic_template_metrics.json", metrics)
    print(metrics)
    return 0 if status == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
