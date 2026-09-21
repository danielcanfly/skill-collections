#!/usr/bin/env python3
from pathlib import Path
import argparse,hashlib
from common import load_json,result,emit
ap=argparse.ArgumentParser();ap.add_argument('root');ap.add_argument('--config');ap.add_argument('--profile');ap.add_argument('--output');a=ap.parse_args();root=Path(a.root);cfg=load_json(a.config or root/'audit_config.json',{});mp=root/(cfg.get('manifest_path') or 'handoff/file_manifest.json');m=load_json(mp,{});errors=[]
entries=m.get('files',[]) if isinstance(m,dict) else [];expected={x['path']:x for x in entries if isinstance(x,dict) and x.get('path') and x.get('sha256')}
actual={p.relative_to(root).as_posix():p for p in root.rglob('*') if p.is_file() and p!=mp and p.name not in {'SHA256SUMS.txt'}}
if not expected: errors.append('authoritative manifest missing or empty')
for rel,p in actual.items():
    if rel not in expected: errors.append(f'unexpected/unmanifested file {rel}')
    elif hashlib.sha256(p.read_bytes()).hexdigest()!=expected[rel]['sha256']: errors.append(f'hash mismatch {rel}')
for rel in expected:
    if rel not in actual: errors.append(f'manifested file missing {rel}')
emit(result('PASS' if not errors else 'FAIL',errors,stats={'manifested':len(expected),'actual':len(actual),'coverage':len(expected)/max(1,len(actual))}),a.output)
