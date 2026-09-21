#!/usr/bin/env python3
from pathlib import Path
import argparse,sys,re,hashlib
from common import *
T={'page','section','clause','paragraph','table','figure','filing-item','line-range','timestamp','article-heading','api-record','dataset-row'}
def main():
 a=argparse.ArgumentParser();a.add_argument('root');x=a.parse_args();r=Path(x.root);rows=read_csv(r/'research/source_passage_registry.csv');e=[]
 if not rows:e.append('passage registry empty')
 for q in rows:
  ex=q.get('excerpt_text','').strip(); loc=q.get('locator_value','').strip(); typ=q.get('locator_type','')
  if typ not in T:e.append(q.get('passage_id','?')+': locator type invalid')
  if len(loc)<3 or re.search(r'original document section|relevant section|proposition section|official page/pdf title',loc,re.I):e.append(q.get('passage_id','?')+': synthetic locator')
  if q.get('locator_resolved')!='PASS':e.append(q.get('passage_id','?')+': locator not resolved')
  if hashlib.sha256(ex.encode()).hexdigest()!=q.get('excerpt_sha256'):e.append(q.get('passage_id','?')+': excerpt sha mismatch')
  if q.get('stage_pre_review_status')!='PASS':e.append(q.get('passage_id','?')+': external passage pre-review missing')
 o={'status':'PASS' if not e else 'FAIL','population_count':len(rows),'errors':e};dump(r/'qa/passage_stage_validation.json',o);print(__import__('json').dumps(o,indent=2));sys.exit(0 if not e else 1)
if __name__=='__main__':main()
