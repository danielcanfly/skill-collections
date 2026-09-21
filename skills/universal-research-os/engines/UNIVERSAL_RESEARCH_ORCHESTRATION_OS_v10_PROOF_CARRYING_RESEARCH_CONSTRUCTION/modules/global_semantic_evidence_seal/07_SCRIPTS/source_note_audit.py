from __future__ import annotations

import argparse
import re
from pathlib import Path

from common import glob_many, load_json, parse_markdown, write_csv, write_json

REQUIRED_GROUPS = {
    "identity": ["Source identity", "Bibliographic Identity", "來源識別", "來源身份"],
    "profile": ["Evidence and method profile", "Evidence / Method Profile", "Evidence / method profile", "證據與方法", "證據／方法"],
    "direct": ["Direct claim contributions", "Direct Contribution", "直接支持", "直接貢獻"],
    "non_direct": ["Partial, contextual, method or challenge contributions", "Partial, Contextual and Challenge Contributions", "Non-direct contributions", "部分支持", "情境支持"],
    "limitations": ["Limitations and non-claims", "What This Source Does Not Establish", "Limitations", "限制", "不能證明"],
    "links": ["Linked concepts and claims", "Concepts and Claims", "Concepts Updated", "關聯概念", "關聯主張"],
    "locators": ["Evidence locators", "Package Evidence Locators", "證據定位", "套件定位"],
}


def headings(body: str) -> set[str]:
    return {m.group(1).strip().casefold() for m in re.finditer(r"^##\s+(.+?)\s*$", body, flags=re.M)}


def main() -> int:
    ap = argparse.ArgumentParser(description="Audit canonical source-note depth.")
    ap.add_argument("--config", required=True)
    args = ap.parse_args()
    cfg = load_json(Path(args.config))
    root = Path(cfg.get("repaired_root", cfg["baseline_root"]))
    out = Path(cfg["output_dir"])
    rows = []
    for p in glob_many(root, cfg.get("reference_globs", ["knowledge/references/*.md"])):
        fm, body = parse_markdown(p)
        if p.name.lower() == "index.md":
            continue
        if str(fm.get("status", "")) not in set(cfg.get("active_statuses", ["production"])):
            continue
        if str(fm.get("type", "")) not in {"Reference", "Source", "reference", "source"}:
            continue
        hs = headings(body)
        missing = [key for key, variants in REQUIRED_GROUPS.items() if not any(v.casefold() in hs for v in variants)]
        rows.append({
            "id": fm.get("id", ""),
            "path": str(p.relative_to(root)),
            "title": fm.get("title", ""),
            "missing_groups": ";".join(missing),
            "status": "PASS" if not missing else "FAIL",
        })
    failed = sum(r["status"] == "FAIL" for r in rows)
    summary = {"source_notes": len(rows), "failed": failed, "pass_rate": round((len(rows)-failed)/len(rows), 4) if rows else 0, "status": "PASS" if failed == 0 else "FAIL"}
    write_csv(out / "source_note_audit.csv", rows)
    write_json(out / "source_note_audit.json", summary)
    print(summary)
    return 0 if failed == 0 else 2


if __name__ == "__main__":
    raise SystemExit(main())
