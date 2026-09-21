#!/usr/bin/env python3
from pathlib import Path
import argparse,hashlib,json,sys
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def main():
 a=argparse.ArgumentParser();a.add_argument('surfaces_root');x=a.parse_args();r=Path(x.surfaces_root);names=['combined','kos','okf','r2','audit_consumption'];sets=[];e=[]
 for n in names:
  s=r/n
  if not s.is_dir():e.append('missing '+n);sets.append({});continue
  sets.append({p.relative_to(s).as_posix():sha(p) for p in s.rglob('*') if p.is_file()})
 if sets and any(q!=sets[0] for q in sets[1:]):e.append('path/sha/bytes mismatch across surfaces')
 o={'status':'PASS' if not e else 'FAIL','errors':e,'file_count':len(sets[0]) if sets else 0};print(json.dumps(o,indent=2));sys.exit(0 if not e else 1)
if __name__=='__main__':main()
