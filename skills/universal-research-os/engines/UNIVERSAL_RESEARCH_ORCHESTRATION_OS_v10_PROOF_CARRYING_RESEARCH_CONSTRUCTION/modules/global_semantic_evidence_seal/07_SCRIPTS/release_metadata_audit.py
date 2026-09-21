from __future__ import annotations

import argparse
import json
import re
import zipfile
from pathlib import Path
from typing import Any

from common import load_json, write_csv, write_json

FIELDS = ["release_id", "content_version", "lifecycle", "global_lifecycle_status"]


def clean_value(value: str) -> str:
    value = value.strip().strip("*`_ ")
    value = re.sub(r"[\]})]+$", "", value).strip().strip("*`_ ")
    if value.lower() in {"null", "none", "n/a", "na", ""}:
        return ""
    return value


def scan_text(text: str) -> dict[str, set[str]]:
    found: dict[str, set[str]] = {k: set() for k in FIELDS}
    for field in FIELDS:
        rx = rf"[\"']?{re.escape(field)}[\"']?\s*[:=]\s*[\"'`]?([^\n,\"'`]+)"
        for m in re.finditer(rx, text, flags=re.I):
            cleaned = clean_value(m.group(1))
            if cleaned:
                found[field].add(cleaned)
    return found


def merge(target: dict[str, set[str]], src: dict[str, set[str]]) -> None:
    for k, vals in src.items():
        target.setdefault(k, set()).update(vals)


def scan_path(path: Path) -> dict[str, set[str]]:
    result: dict[str, set[str]] = {k: set() for k in FIELDS}
    if path.is_dir():
        files = [p for p in path.rglob("*") if p.is_file() and p.suffix.lower() in {".json", ".md", ".txt", ".csv"}]
        for p in files:
            try:
                merge(result, scan_text(p.read_text(encoding="utf-8", errors="replace")))
            except Exception:
                continue
    elif path.suffix.lower() == ".zip":
        with zipfile.ZipFile(path) as zf:
            for name in zf.namelist():
                if Path(name).suffix.lower() not in {".json", ".md", ".txt", ".csv"}:
                    continue
                try:
                    merge(result, scan_text(zf.read(name).decode("utf-8", errors="replace")))
                except Exception:
                    continue
    return result


def main() -> int:
    ap = argparse.ArgumentParser(description="Compare release identity and lifecycle across bundle directories or ZIP files.")
    ap.add_argument("--config", required=True)
    args = ap.parse_args()
    cfg = load_json(Path(args.config))
    out = Path(cfg["output_dir"])
    authoritative: dict[str, Any] = cfg.get("authoritative_metadata", {})
    rows = []
    findings = []
    for raw in cfg.get("bundle_paths", []):
        p = Path(raw)
        vals = scan_path(p)
        row = {"bundle": str(p)}
        for field in FIELDS:
            cleaned = sorted(x for x in vals.get(field, set()) if x)
            row[field] = ";".join(cleaned)
            expected = authoritative.get(field)
            if expected and cleaned and expected not in cleaned:
                findings.append({"severity": "P1", "code": "AUTHORITATIVE_VALUE_MISSING", "bundle": str(p), "field": field, "expected": expected, "found": cleaned})
            if len(cleaned) > 1:
                findings.append({"severity": "P1", "code": "INTRA_BUNDLE_METADATA_DRIFT", "bundle": str(p), "field": field, "found": cleaned})
        rows.append(row)
    status = "PASS" if not findings else "FAIL"
    write_csv(out / "release_metadata_matrix.csv", rows, fieldnames=["bundle"] + FIELDS)
    write_json(out / "release_metadata_audit.json", {"status": status, "authoritative": authoritative, "findings": findings})
    print({"status": status, "bundles": len(rows), "findings": len(findings)})
    return 0 if status == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
