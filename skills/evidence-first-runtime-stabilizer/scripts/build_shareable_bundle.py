#!/usr/bin/env python3
import argparse,shutil,subprocess,zipfile
from pathlib import Path

ap=argparse.ArgumentParser()
ap.add_argument('raw')
ap.add_argument('outzip')
a=ap.parse_args()

raw=Path(a.raw)
outzip=Path(a.outzip)
work=outzip.with_suffix('.redacted')

if work.exists():
    shutil.rmtree(work)

subprocess.run(['runtime-stabilizer','redact',str(raw),str(work)],check=True)
subprocess.run(['python3',str(Path(__file__).with_name('secret_scan.py')),str(work)],check=True)

with zipfile.ZipFile(outzip,'w',zipfile.ZIP_DEFLATED) as z:
    for p in work.rglob('*'):
        if p.is_file():
            z.write(p,p.relative_to(work))

print(outzip)
