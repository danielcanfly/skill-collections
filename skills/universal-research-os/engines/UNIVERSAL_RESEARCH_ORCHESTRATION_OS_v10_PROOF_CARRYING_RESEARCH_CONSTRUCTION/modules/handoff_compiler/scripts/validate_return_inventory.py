#!/usr/bin/env python3
from pathlib import Path
import argparse,json,hashlib,sys
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def main():
 a=argparse.ArgumentParser();a.add_argument('return_dir');a.add_argument('contract');x=a.parse_args();r=Path(x.return_dir);c=json.loads(Path(x.contract).read_text());e=[]
 for q in c.get('required_outputs',[]):
  p=r/q['filename']
  if not p.is_file():e.append('missing '+q['filename'])
 o={'status':'PASS' if not e else 'FAIL','errors':e};print(json.dumps(o,indent=2));sys.exit(0 if not e else 1)
if __name__=='__main__':main()
