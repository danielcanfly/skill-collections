#!/usr/bin/env python3
from pathlib import Path
import argparse,sys,json
from common import *
def main():
 a=argparse.ArgumentParser();a.add_argument('root');x=a.parse_args();r=Path(x.root);rows=read_csv(r/'research/material_clause_registry.csv');e=[]
 ext=load(r/'qa/external_stage_review_validation.json',{})
 if ext.get('status')!='PASS':e.append('external stage review validation not PASS')
 if not rows:e.append('material clause registry empty')
 for q in rows:
  cid=q.get('clause_id','?');st=q.get('support_status')
  if st not in {'SUPPORTED','PARTIAL','UNSUPPORTED'}:e.append(cid+': invalid support status')
  if st=='SUPPORTED' and q.get('unsupported_remainder','').strip().lower() not in {'','none','n/a','not applicable'}:e.append(cid+': supported clause has remainder')
  if not q.get('passage_ids','').strip():e.append(cid+': no passage')
 o={'status':'PASS' if not e else 'FAIL','population_count':len(rows),'errors':e};dump(r/'qa/clause_stage_validation.json',o);print(json.dumps(o,indent=2));sys.exit(0 if not e else 1)
if __name__=='__main__':main()
