#!/usr/bin/env python3
from pathlib import Path
import sys,json
root=Path(sys.argv[1] if len(sys.argv)>1 else '.').resolve()
bad=[]
forbidden_dirs={'__pycache__','build','dist','.pytest_cache','.mypy_cache','.ruff_cache'}
forbidden_files={'.DS_Store','.env'}
for p in root.rglob('*'):
    rel=str(p.relative_to(root))
    if p.is_dir() and (p.name in forbidden_dirs or p.name.endswith('.egg-info')):
        bad.append(rel)
    if p.is_file() and (p.suffix=='.pyc' or p.name in forbidden_files):
        bad.append(rel)
# optional caller-provided denylist, one case-insensitive literal per line
forbidden_file=root/'config/forbidden-identifiers.txt'
if forbidden_file.exists():
    patterns=[x.strip() for x in forbidden_file.read_text().splitlines() if x.strip() and not x.strip().startswith('#')]
    for p in root.rglob('*'):
        if not p.is_file() or p.suffix.lower() in {'.zip','.png','.jpg','.jpeg','.gif','.whl'}: continue
        try: text=p.read_text(errors='replace').lower()
        except Exception: continue
        for pat in patterns:
            if pat.lower() in text: bad.append(f'{p.relative_to(root)}:forbidden:{pat}')
# packaged adapters must match source adapters
src=root/'adapters'; pkg=root/'src/runtime_stabilizer/adapters_data'
if src.exists() and pkg.exists():
    a={str(p.relative_to(src)):p.read_bytes() for p in src.rglob('*') if p.is_file()}
    b={str(p.relative_to(pkg)):p.read_bytes() for p in pkg.rglob('*') if p.is_file()}
    if a!=b: bad.append('adapter trees are out of sync')
print('\n'.join(sorted(set(bad))) if bad else 'RELEASE_HYGIENE_PASS')
raise SystemExit(2 if bad else 0)
