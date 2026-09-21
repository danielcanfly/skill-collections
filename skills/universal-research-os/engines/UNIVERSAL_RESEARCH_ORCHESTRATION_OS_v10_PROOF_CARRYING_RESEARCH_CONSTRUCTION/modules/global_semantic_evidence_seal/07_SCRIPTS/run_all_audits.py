from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

from common import load_json, write_json

SCRIPTS = [
    "inventory_baseline.py",
    "semantic_template_audit.py",
    "claim_evidence_audit.py",
    "source_note_audit.py",
    "retrieval_leakage_audit.py",
    "release_metadata_audit.py",
    "package_integrity_audit.py",
]


def main() -> int:
    ap = argparse.ArgumentParser(description="Run the Universal Semantic and Evidence Seal audit suite.")
    ap.add_argument("--config", required=True)
    args = ap.parse_args()
    cfg_path = Path(args.config).resolve()
    cfg = load_json(cfg_path)
    out = Path(cfg["output_dir"])
    out.mkdir(parents=True, exist_ok=True)
    base = Path(__file__).resolve().parent
    receipts = []
    for name in SCRIPTS:
        proc = subprocess.run([sys.executable, str(base / name), "--config", str(cfg_path)], text=True, capture_output=True)
        receipts.append({
            "script": name,
            "exit_code": proc.returncode,
            "stdout": proc.stdout[-10000:],
            "stderr": proc.stderr[-10000:],
        })
    status = "PASS" if all(x["exit_code"] == 0 for x in receipts) else "FAIL"
    write_json(out / "audit_suite_receipt.json", {"status": status, "receipts": receipts})
    print(json.dumps({"status": status, "scripts": len(receipts), "failed": [x["script"] for x in receipts if x["exit_code"] != 0]}, indent=2))
    return 0 if status == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
