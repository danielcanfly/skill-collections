#!/usr/bin/env python3
from pathlib import Path
import argparse, zipfile, json, hashlib, sys
from lib.common import sha256_file, zip_crc
p=argparse.ArgumentParser(); p.add_argument('zip'); p.add_argument('--expected-sha'); p.add_argument('--receipt'); a=p.parse_args()
z=Path(a.zip); receipt={'zip':str(z),'sha256':sha256_file(z),'crc':zip_crc(z),'checks':{}}
receipt['checks']['expected_sha']=not a.expected_sha or receipt['sha256']==a.expected_sha
with zipfile.ZipFile(z) as f:
    manifests=[n for n in f.namelist() if n.endswith('handoff/file_manifest.json')]
    receipt['embedded_manifests']=manifests
receipt['pass']=receipt['crc']['pass'] and receipt['checks']['expected_sha']
if a.receipt: Path(a.receipt).write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt,indent=2)); sys.exit(0 if receipt['pass'] else 1)
