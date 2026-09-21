#!/usr/bin/env python3
from pathlib import Path
import argparse,zipfile
ap=argparse.ArgumentParser();ap.add_argument('root');ap.add_argument('output');a=ap.parse_args();root=Path(a.root).resolve();out=Path(a.output).resolve()
with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED) as z:
 for p in sorted(root.rglob('*')):
  if p.is_file():
   info=zipfile.ZipInfo(str(Path(root.name)/p.relative_to(root)),(1980,1,1,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o644<<16;z.writestr(info,p.read_bytes())
print(out)
