#!/usr/bin/env python3
import argparse,zipfile
from pathlib import Path
p=argparse.ArgumentParser(); p.add_argument('--root',required=True); p.add_argument('--output',required=True); a=p.parse_args()
r=Path(a.root); out=Path(a.output); epoch=(2020,1,1,0,0,0)
with zipfile.ZipFile(out,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
    for f in sorted(x for x in r.rglob('*') if x.is_file()):
        rel=f.relative_to(r.parent).as_posix(); info=zipfile.ZipInfo(rel,epoch); info.compress_type=zipfile.ZIP_DEFLATED; info.external_attr=0o100644<<16
        z.writestr(info,f.read_bytes())
print(out)
