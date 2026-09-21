from __future__ import annotations

import argparse
from pathlib import Path

from common import sha256_file


def main() -> int:
    ap = argparse.ArgumentParser(description="Build SHA256SUMS.txt for a directory, excluding the manifest itself.")
    ap.add_argument("root")
    args = ap.parse_args()
    root = Path(args.root).resolve()
    manifest = root / "SHA256SUMS.txt"
    rows = []
    for p in sorted(x for x in root.rglob("*") if x.is_file() and x != manifest):
        rows.append(f"{sha256_file(p)}  {p.relative_to(root).as_posix()}")
    manifest.write_text("\n".join(rows) + "\n", encoding="utf-8")
    print(manifest)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
