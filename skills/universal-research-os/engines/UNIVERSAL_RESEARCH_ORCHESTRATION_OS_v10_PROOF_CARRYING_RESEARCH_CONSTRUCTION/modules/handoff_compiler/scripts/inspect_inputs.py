#!/usr/bin/env python3
from pathlib import Path
import argparse,json,zipfile,hashlib
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def main():
 a=argparse.ArgumentParser();a.add_argument('inputs',nargs='+');a.add_argument('--output',required=True);x=a.parse_args();rows=[]
 for q in x.inputs:
  p=Path(q).resolve();r={'path':str(p),'filename':p.name,'sha256':sha(p),'bytes':p.stat().st_size,'zip_crc':'N/A'}
  if zipfile.is_zipfile(p):
   with zipfile.ZipFile(p) as z:r['zip_crc']='PASS' if z.testzip() is None else 'FAIL'
  rows.append(r)
 Path(x.output).write_text(json.dumps({'status':'PASS' if all(r['zip_crc']!='FAIL' for r in rows) else 'FAIL','inputs':rows},indent=2)+'\n')
if __name__=='__main__':main()
