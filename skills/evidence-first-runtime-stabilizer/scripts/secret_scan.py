#!/usr/bin/env python3
import re,sys,json
from pathlib import Path
PATTERNS=[
    r'gh[pousr]_[A-Za-z0-9_]{20,}',
    r'AKIA[0-9A-Z]{16}',
    r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----',
    r'(?i)authorization:\s*bearer\s+(?!<REDACTED>)\S+',
    r'eyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+',
]
hits=[]; skipped=[]
for f in Path(sys.argv[1]).rglob('*'):
    if not f.is_file(): continue
    b=f.read_bytes()
    if b'\x00' in b:
        skipped.append(str(f)); continue
    try:s=b.decode('utf-8')
    except UnicodeDecodeError:
        skipped.append(str(f)); continue
    for pat in PATTERNS:
        if re.search(pat,s): hits.append({'file':str(f),'pattern':pat})
print(json.dumps({'status':'PASS' if not hits else 'FAIL','hits':hits,'binary_or_non_utf8_skipped':skipped},indent=2))
raise SystemExit(0 if not hits else 2)
