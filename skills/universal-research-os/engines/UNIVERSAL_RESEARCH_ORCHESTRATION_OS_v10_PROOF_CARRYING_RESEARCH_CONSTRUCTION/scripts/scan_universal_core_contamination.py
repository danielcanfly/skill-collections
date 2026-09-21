#!/usr/bin/env python3
from pathlib import Path
import json,re,argparse
ap=argparse.ArgumentParser();ap.add_argument('root',nargs='?',default=str(Path(__file__).resolve().parents[1]));a=ap.parse_args();root=Path(a.root);errors=[]
allowed={'scripts/scan_universal_core_contamination.py','modules/dispatcher/scripts/validate_child_handoff.py'}
pattern=re.compile(r'(?i)(?:\bSPSDA\b|\bBFA[_-])')
for p in root.rglob('*'):
    if not p.is_file() or p.suffix.lower() not in {'.py','.json','.md','.txt','.csv','.sh','.yaml','.yml'}: continue
    rel=p.relative_to(root).as_posix()
    if rel in allowed: continue
    try:t=p.read_text(encoding='utf-8')
    except UnicodeDecodeError:continue
    if pattern.search(t): errors.append(rel)
print(json.dumps({'status':'PASS' if not errors else 'FAIL','contaminated_files':errors},indent=2));raise SystemExit(0 if not errors else 1)
