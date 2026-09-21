from __future__ import annotations

import argparse
from collections import Counter
from pathlib import Path

from common import glob_many, load_json, parse_markdown, sha256_file, write_csv, write_json


def main() -> int:
    ap = argparse.ArgumentParser(description="Build a baseline inventory for a Knowledge OS tree.")
    ap.add_argument("--config", required=True)
    args = ap.parse_args()
    cfg = load_json(Path(args.config))
    root = Path(cfg["baseline_root"])
    out = Path(cfg["output_dir"])
    md_paths = glob_many(root, cfg.get("knowledge_globs", ["knowledge/**/*.md"]))

    rows = []
    ids = []
    for p in md_paths:
        fm, body = parse_markdown(p)
        node_id = str(fm.get("id", ""))
        if node_id:
            ids.append(node_id)
        rows.append({
            "path": str(p.relative_to(root)),
            "sha256": sha256_file(p),
            "id": node_id,
            "title": fm.get("title", ""),
            "type": fm.get("type", ""),
            "status": fm.get("status", ""),
            "body_chars": len(body),
        })

    dup = {k: v for k, v in Counter(ids).items() if v > 1}
    summary = {
        "root": str(root),
        "markdown_files": len(rows),
        "nodes_with_id": len(ids),
        "unique_ids": len(set(ids)),
        "duplicate_ids": dup,
        "status": "PASS" if not dup else "FAIL",
    }
    write_csv(out / "inventory_baseline.csv", rows)
    write_json(out / "inventory_baseline.json", summary)
    print(summary)
    return 0 if summary["status"] == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
