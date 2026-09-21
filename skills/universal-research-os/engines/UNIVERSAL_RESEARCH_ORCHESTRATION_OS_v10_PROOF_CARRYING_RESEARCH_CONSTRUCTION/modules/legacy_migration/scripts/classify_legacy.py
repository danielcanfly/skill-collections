#!/usr/bin/env python3
from pathlib import Path
import argparse,json,hashlib,zipfile
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def main():
 a=argparse.ArgumentParser();a.add_argument('artifact');a.add_argument('--output',required=True);x=a.parse_args();p=Path(x.artifact);name=p.name.lower();generation='UNKNOWN'
 for v in range(4,11):
  if f'v{v}' in name:generation=f'v{v}'
 o={'status':'MIGRATION_REQUIRED' if generation!='v10' else 'V10_NATIVE','artifact':p.name,'sha256':sha(p),'detected_generation':generation,'grandfathering_allowed':False};Path(x.output).write_text(json.dumps(o,indent=2)+'\n')
if __name__=='__main__':main()
