#!/usr/bin/env python3
import argparse,tempfile,zipfile,json,hashlib,sys
from pathlib import Path
from lib.common import sha256_file,zip_crc
p=argparse.ArgumentParser(); p.add_argument('zip'); p.add_argument('--receipt',required=True); a=p.parse_args(); z=Path(a.zip)
r={'zip':str(z),'zip_sha256':sha256_file(z),'crc':zip_crc(z),'checksum_errors':[]}
with tempfile.TemporaryDirectory() as td:
    with zipfile.ZipFile(z) as f: f.extractall(td)
    roots=[p for p in Path(td).iterdir() if p.is_dir()]; root=roots[0] if len(roots)==1 else Path(td)
    sf=root/'SHA256SUMS.txt'
    if sf.exists():
        for line in sf.read_text().splitlines():
            if not line.strip(): continue
            h,rel=line.split(None,1); rel=rel.strip(); fp=root/rel
            if not fp.exists() or sha256_file(fp)!=h: r['checksum_errors'].append(rel)
    else: r['checksum_errors'].append('SHA256SUMS.txt missing')
r['pass']=r['crc']['pass'] and not r['checksum_errors']; Path(a.receipt).write_text(json.dumps(r,indent=2)+'\n'); print(json.dumps(r,indent=2)); sys.exit(0 if r['pass'] else 1)
