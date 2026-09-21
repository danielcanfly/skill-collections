from __future__ import annotations

import argparse
import hashlib
import re
import zipfile
from pathlib import Path, PurePosixPath

from common import load_json, write_json


def audit_zip(path: Path) -> dict:
    findings = []
    names = []
    try:
        with zipfile.ZipFile(path) as zf:
            names = zf.namelist()
            bad = zf.testzip()
            if bad:
                findings.append({"severity": "P1", "code": "ZIP_CRC_FAILURE", "member": bad})
            if len(names) != len(set(names)):
                findings.append({"severity": "P1", "code": "DUPLICATE_ARCHIVE_MEMBER"})
            for name in names:
                pp = PurePosixPath(name)
                if pp.is_absolute() or ".." in pp.parts:
                    findings.append({"severity": "P0", "code": "UNSAFE_ARCHIVE_PATH", "member": name})
            manifest_names = [n for n in names if Path(n).name in {"SHA256SUMS.txt", "MANIFEST.sha256"}]
            for mn in manifest_names:
                base = str(PurePosixPath(mn).parent)
                text = zf.read(mn).decode("utf-8", errors="replace")
                for line in text.splitlines():
                    m = re.match(r"^([0-9a-fA-F]{64})\s+\*?(.+)$", line.strip())
                    if not m:
                        continue
                    expected, rel = m.group(1).lower(), m.group(2).strip()
                    candidate = str(PurePosixPath(base) / rel) if base not in {"", "."} else rel
                    if candidate not in names:
                        # Some manifests intentionally cover only sibling files. Record as P2, not P1.
                        findings.append({"severity": "P2", "code": "MANIFEST_MEMBER_MISSING", "manifest": mn, "member": candidate})
                        continue
                    actual = hashlib.sha256(zf.read(candidate)).hexdigest()
                    if actual != expected:
                        findings.append({"severity": "P1", "code": "MANIFEST_HASH_MISMATCH", "manifest": mn, "member": candidate})
    except zipfile.BadZipFile:
        findings.append({"severity": "P0", "code": "BAD_ZIP"})
    status = "PASS" if not any(x["severity"] in {"P0", "P1"} for x in findings) else "FAIL"
    return {"path": str(path), "status": status, "member_count": len(names), "findings": findings}


def main() -> int:
    ap = argparse.ArgumentParser(description="Run ZIP CRC, archive safety and manifest checks.")
    ap.add_argument("--config", required=True)
    args = ap.parse_args()
    cfg = load_json(Path(args.config))
    out = Path(cfg["output_dir"])
    results = [audit_zip(Path(x)) for x in cfg.get("bundle_paths", []) if str(x).lower().endswith(".zip")]
    status = "PASS" if all(x["status"] == "PASS" for x in results) else "FAIL"
    write_json(out / "package_integrity_audit.json", {"status": status, "results": results})
    print({"status": status, "zips": len(results)})
    return 0 if status == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
