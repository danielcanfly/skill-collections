#!/usr/bin/env python3
from pathlib import Path
import argparse,json,hashlib,sys
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def main():
 a=argparse.ArgumentParser();a.add_argument('root');a.add_argument('baseline');a.add_argument('--output',required=True);x=a.parse_args();r=Path(x.root);b=json.loads(Path(x.baseline).read_text());e=[]
 for q in b.get('files',[]):
  p=r/q['path']
  if not p.is_file() or sha(p)!=q['sha256'] or p.stat().st_size!=q['bytes']:e.append(q['path'])
 o={'status':'PASS' if not e else 'FAIL','changed_or_missing':e,'checked':len(b.get('files',[]))};Path(x.output).write_text(json.dumps(o,indent=2)+'\n');sys.exit(0 if not e else 1)
if __name__=='__main__':main()
