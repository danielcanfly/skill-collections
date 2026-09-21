#!/usr/bin/env python3
import argparse,hashlib,json,mimetypes
from pathlib import Path
from lib.common import sha256_file
p=argparse.ArgumentParser(); p.add_argument('--root',required=True); p.add_argument('--manifest',default='manifest.json'); p.add_argument('--sha-file',default='SHA256SUMS.txt'); a=p.parse_args()
r=Path(a.root); exclude={a.manifest,a.sha_file}; rows=[]
for f in sorted(x for x in r.rglob('*') if x.is_file()):
    rel=f.relative_to(r).as_posix()
    if rel in exclude: continue
    rows.append({'path':rel,'size_bytes':f.stat().st_size,'sha256':sha256_file(f),'media_type':mimetypes.guess_type(f.name)[0] or 'application/octet-stream'})
(r/a.manifest).write_text(json.dumps({'entries':rows},ensure_ascii=False,indent=2)+'\n')
with (r/a.sha_file).open('w') as o:
    for x in rows: o.write(f"{x['sha256']}  {x['path']}\n")
print(len(rows))
