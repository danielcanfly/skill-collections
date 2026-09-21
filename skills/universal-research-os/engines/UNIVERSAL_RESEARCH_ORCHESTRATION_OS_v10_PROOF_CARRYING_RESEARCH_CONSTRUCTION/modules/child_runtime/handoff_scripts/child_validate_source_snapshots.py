#!/usr/bin/env python3
from pathlib import Path
import argparse,sys
from common import *
def main():
 a=argparse.ArgumentParser();a.add_argument('root');x=a.parse_args();r=Path(x.root);rows=read_csv(r/'research/source_snapshot_registry.csv');e=[]
 if not rows:e.append('source snapshot registry empty')
 for q in rows:
  p=r/q.get('snapshot_path','')
  if not p.is_file():e.append(q.get('source_id','?')+': snapshot missing');continue
  if sha_file(p)!=q.get('snapshot_sha256'):e.append(q.get('source_id','?')+': snapshot sha mismatch')
  if q.get('source_identity_status')!='PASS' or q.get('production_eligibility')!='ELIGIBLE':e.append(q.get('source_id','?')+': identity/eligibility incomplete')
 o={'status':'PASS' if not e else 'FAIL','population_count':len(rows),'errors':e};dump(r/'qa/source_snapshot_validation.json',o);print(__import__('json').dumps(o,indent=2));sys.exit(0 if not e else 1)
if __name__=='__main__':main()
