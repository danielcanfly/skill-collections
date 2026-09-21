#!/usr/bin/env python3
from pathlib import Path
import argparse,sys,re
from common import *
def main():
 a=argparse.ArgumentParser();a.add_argument('root');x=a.parse_args();r=Path(x.root);rows=read_csv(r/'research/material_clause_registry.csv');e=[]
 if not rows:e.append('material clause registry empty')
 for q in rows:
  cid=q.get('clause_id','?')
  if q.get('support_status') not in {'SUPPORTED','PARTIAL','UNSUPPORTED'}:e.append(cid+': invalid support status')
  if q.get('support_status')=='SUPPORTED' and q.get('unsupported_remainder','').strip() not in {'','none','NONE'}:e.append(cid+': supported clause has remainder')
  if q.get('external_pre_review_status')!='PASS':e.append(cid+': external clause pre-review missing')
  if not q.get('passage_ids','').strip():e.append(cid+': no passage')
 o={'status':'PASS' if not e else 'FAIL','population_count':len(rows),'errors':e};dump(r/'qa/clause_stage_validation.json',o);print(__import__('json').dumps(o,indent=2));sys.exit(0 if not e else 1)
if __name__=='__main__':main()
