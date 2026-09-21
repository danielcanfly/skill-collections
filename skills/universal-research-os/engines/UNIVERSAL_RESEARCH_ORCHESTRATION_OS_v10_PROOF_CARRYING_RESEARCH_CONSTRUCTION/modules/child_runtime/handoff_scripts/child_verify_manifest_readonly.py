#!/usr/bin/env python3
from pathlib import Path
import argparse,hashlib,json

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('root')
    ap.add_argument('--json-output')
    a=ap.parse_args()
    root=Path(a.root).resolve()
    mp=root/'handoff/file_manifest.json'
    errors=[]
    if not mp.exists():
        errors.append('authoritative manifest missing: handoff/file_manifest.json')
        data={}
    else:
        try: data=json.loads(mp.read_text(encoding='utf-8'))
        except Exception as e:
            errors.append(f'manifest unreadable: {e}')
            data={}
    entries=data.get('files',[]) if isinstance(data,dict) else []
    expected={}
    for e in entries:
        if not isinstance(e,dict) or not e.get('path') or not e.get('sha256'):
            errors.append('manifest contains invalid/non-hashed entry')
            continue
        if e['path'] in expected: errors.append('duplicate manifest path '+e['path'])
        expected[e['path']]=e
    actual={p.relative_to(root).as_posix():p for p in root.rglob('*') if p.is_file() and p!=mp and p.name!='SHA256SUMS.txt'}
    for rel,p in actual.items():
        if rel not in expected: errors.append('unexpected/unmanifested file '+rel)
        elif hashlib.sha256(p.read_bytes()).hexdigest()!=expected[rel]['sha256']: errors.append('hash mismatch '+rel)
    for rel in expected:
        if rel not in actual: errors.append('manifested file missing '+rel)
    if not entries: errors.append('manifest missing or empty')
    if data.get('file_count') not in {None,len(expected)}: errors.append('manifest file_count mismatch')
    out={'status':'PASS' if not errors else 'FAIL','manifested':len(expected),'actual':len(actual),'errors':errors}
    txt=json.dumps(out,ensure_ascii=False,indent=2)
    print(txt)
    if a.json_output: Path(a.json_output).write_text(txt+'\n',encoding='utf-8')
    raise SystemExit(0 if not errors else 1)
if __name__=='__main__': main()
