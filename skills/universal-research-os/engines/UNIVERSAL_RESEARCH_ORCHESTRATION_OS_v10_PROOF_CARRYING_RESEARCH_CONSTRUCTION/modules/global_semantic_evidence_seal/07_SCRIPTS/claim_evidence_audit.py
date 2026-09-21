from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from pathlib import Path

from common import ensure_relative, load_json, read_csv, write_csv, write_json

ALLOWED_RELATIONS = {
    "direct_support", "partial_support", "contextual_support", "method_support",
    "challenge", "contradiction", "bounded_synthesis", "support", "partial", "contextual"
}
ALLOWED_BOUNDARIES = {
    "VERIFIED_EXACT_SPAN", "VERIFIED_SECTION_LOCATOR", "VERIFIED_DOCUMENT_LEVEL",
    "PACKAGE_LINEAGE_ONLY", "BOUNDED_SYNTHESIS", "UNSUPPORTED",
    "NOT-CAPTURED-IN-V1-INPUTS", "NOT_CAPTURED_IN_V1_INPUTS"
}


def value(row: dict[str, str], columns: dict[str, str], logical: str) -> str:
    return (row.get(columns.get(logical, logical), "") or "").strip()


def main() -> int:
    ap = argparse.ArgumentParser(description="Audit claim-evidence atomicity, coverage and evidence boundaries.")
    ap.add_argument("--config", required=True)
    args = ap.parse_args()
    cfg = load_json(Path(args.config))
    root = Path(cfg.get("repaired_root", cfg["baseline_root"]))
    out = Path(cfg["output_dir"])
    claims_path = ensure_relative(root, cfg["claims_csv"])
    bindings_path = ensure_relative(root, cfg["bindings_csv"])
    cc = cfg.get("claim_columns", {})
    bc = cfg.get("binding_columns", {})
    claims = read_csv(claims_path)
    bindings = read_csv(bindings_path)

    claim_ids = {value(r, cc, "claim_id") for r in claims if value(r, cc, "claim_id")}
    by_claim: dict[str, list[dict[str, str]]] = defaultdict(list)
    findings: list[dict] = []
    edge_keys: Counter[tuple[str, ...]] = Counter()

    for i, row in enumerate(bindings, 2):
        claim_id = value(row, bc, "claim_id")
        source_id = value(row, bc, "source_id")
        concept_id = value(row, bc, "concept_id")
        relation_raw = value(row, bc, "relation")
        relation = relation_raw.strip().lower().replace("-", "_").replace(" ", "_")
        boundary = value(row, bc, "evidence_boundary")
        boundary_norm = boundary.strip().upper().replace(" ", "_")
        locator_type = value(row, bc, "locator_type")
        source_locator = value(row, bc, "source_locator")
        package_locator = value(row, bc, "package_locator")
        verification = value(row, bc, "verification_status")
        by_claim[claim_id].append(row)
        key = (claim_id, source_id, concept_id, relation, source_locator, package_locator)
        edge_keys[key] += 1
        if claim_id not in claim_ids:
            findings.append({"severity": "P1", "code": "ORPHAN_CLAIM", "row": i, "claim_id": claim_id})
        if not source_id and relation != "bounded_synthesis":
            findings.append({"severity": "P1", "code": "MISSING_SOURCE_ID", "row": i, "claim_id": claim_id})
        if not concept_id:
            findings.append({"severity": "P1", "code": "MISSING_CONCEPT_ID", "row": i, "claim_id": claim_id})
        if relation not in ALLOWED_RELATIONS:
            findings.append({"severity": "P1", "code": "INVALID_RELATION", "row": i, "claim_id": claim_id, "value": relation_raw})
        if boundary and boundary_norm not in ALLOWED_BOUNDARIES:
            findings.append({"severity": "P1", "code": "INVALID_BOUNDARY", "row": i, "claim_id": claim_id, "value": boundary})
        if relation in {"direct_support", "support"}:
            if not boundary:
                findings.append({"severity": "P1", "code": "DIRECT_WITHOUT_BOUNDARY", "row": i, "claim_id": claim_id})
            if boundary_norm in {"PACKAGE_LINEAGE_ONLY", "BOUNDED_SYNTHESIS", "UNSUPPORTED", "NOT-CAPTURED-IN-V1-INPUTS", "NOT_CAPTURED_IN_V1_INPUTS"}:
                findings.append({"severity": "P2", "code": "DIRECT_WEAK_BOUNDARY", "row": i, "claim_id": claim_id, "boundary": boundary})
            if not source_locator and not package_locator:
                findings.append({"severity": "P1", "code": "DIRECT_WITHOUT_LOCATOR", "row": i, "claim_id": claim_id})
            if verification.upper() in {"", "UNVERIFIED", "NOT_AVAILABLE"}:
                findings.append({"severity": "P1", "code": "DIRECT_UNVERIFIED", "row": i, "claim_id": claim_id})
        if locator_type == "EXACT_QUOTE" and not source_locator:
            findings.append({"severity": "P1", "code": "QUOTE_WITHOUT_LOCATOR", "row": i, "claim_id": claim_id})

    for key, count in edge_keys.items():
        if count > 1:
            findings.append({"severity": "P2", "code": "DUPLICATE_BINDING", "count": count, "key": list(key)})

    direct_claims, bounded_claims, any_claims = set(), set(), set()
    for claim_id, rows in by_claim.items():
        if not claim_id:
            continue
        any_claims.add(claim_id)
        relations = {value(r, bc, "relation") for r in rows}
        if relations & {"direct_support", "support"}:
            direct_claims.add(claim_id)
        if "bounded_synthesis" in relations or not (relations & {"direct_support", "support"}):
            bounded_claims.add(claim_id)

    unsupported = sorted(claim_ids - any_claims)
    for claim_id in unsupported:
        findings.append({"severity": "P1", "code": "CLAIM_WITHOUT_BINDING", "claim_id": claim_id})

    summary = {
        "claims": len(claim_ids),
        "bindings": len(bindings),
        "claims_with_any_binding": len(any_claims),
        "claims_with_direct_support": len(direct_claims),
        "bounded_or_non_direct_claims": len(bounded_claims),
        "claims_without_binding": len(unsupported),
        "finding_counts": dict(Counter(x["severity"] for x in findings)),
        "status": "PASS" if not any(x["severity"] in {"P0", "P1"} for x in findings) else "FAIL",
    }
    write_json(out / "claim_evidence_audit.json", {"summary": summary, "findings": findings})
    write_csv(out / "claim_evidence_findings.csv", findings, fieldnames=sorted({k for x in findings for k in x}) if findings else ["severity", "code"])
    print(summary)
    return 0 if summary["status"] == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
