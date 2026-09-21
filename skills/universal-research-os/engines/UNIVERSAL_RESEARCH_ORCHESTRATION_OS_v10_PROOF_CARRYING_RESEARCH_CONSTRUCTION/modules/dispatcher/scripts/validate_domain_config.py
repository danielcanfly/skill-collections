#!/usr/bin/env python3
from pathlib import Path
import argparse,json,re,sys,hashlib
REQ_CLASSES={'definition','comparison','how-to','decision/application','audit','source-provenance','multi-hop','adversarial'}
def fail(msgs):
 print(json.dumps({'status':'FAIL','errors':msgs},ensure_ascii=False,indent=2));raise SystemExit(1)
def main():
 ap=argparse.ArgumentParser();ap.add_argument('config');a=ap.parse_args();p=Path(a.config);d=json.loads(p.read_text(encoding='utf-8'));e=[]
 for k in ['domain_id','domain_title','domain_title_en','purpose','audience','languages','global_exclusions','children']:
  if not d.get(k):e.append('missing '+k)
 ids=set()
 for c in d.get('children',[]):
  sid=c.get('session_id','');
  if sid in ids:e.append('duplicate session_id '+sid)
  ids.add(sid)
  checks=[('ownership',len(c.get('canonical_ownership',[])),4),('exclusions',len(c.get('explicit_exclusions',[])),3),('modules',len(c.get('research_modules',[])),6),('questions',len(c.get('core_questions',[])),8),('nodes',len(c.get('expected_nodes',[])),16),('source routes',len(c.get('mandatory_source_routes',[])),8),('debates',len(c.get('debates',[])),5),('semantic risks',len(c.get('semantic_risks',[])),5),('auditor tests',len(c.get('auditor_holdout_tests',[])),10),('source authority tests',len(c.get('source_authority_tests',[])),2)]
  for n,v,m in checks:
   if v<m:e.append(f'{sid}: {n} {v} < {m}')
  if c.get('case_minimum',0)<6:e.append(f'{sid}: case_minimum <6')
  ver=c.get('candidate_version',''); out=c.get('final_output_name','')
  if ver and f'PRODUCTION_CANDIDATE_{ver}.zip' not in out:e.append(f'{sid}: final output version mismatch')
  nids=[n.get('candidate_id') for n in c.get('expected_nodes',[])]; ns=set(nids)
  if len(ns)!=len(nids):e.append(f'{sid}: duplicate node IDs')
  for n in c.get('expected_nodes',[]):
   if n.get('negative_candidate_id') not in ns:e.append(f"{sid}: negative node missing {n.get('negative_candidate_id')}")
   for qk in ['definition_query','decision_query','failure_query']:
    if len(n.get(qk,''))<20:e.append(f"{sid}: weak {qk} for {n.get('candidate_id')}")
  at=c.get('auditor_holdout_tests',[]); classes={x.get('class') for x in at}
  if len({x.get('query') for x in at})!=len(at):e.append(f'{sid}: duplicate auditor queries')
  if len(classes)<4:e.append(f'{sid}: auditor tests have fewer than 4 classes')
  for t in at:
   if not t.get('negative_ids'):e.append(f"{sid}: auditor test {t.get('test_id')} has no negative")
   for x in t.get('expected_ids',[])+t.get('negative_ids',[]):
    if x not in ns:e.append(f'{sid}: auditor test references unknown {x}')
  # placeholder and thin-topic detection
  blob=json.dumps(c,ensure_ascii=False).lower()
  for bad in ['replace with','請填入','todo','tbd','example-concept','topic unspecified']:
   if bad in blob:e.append(f'{sid}: placeholder token {bad}')
 if e:fail(e)
 print(json.dumps({'status':'PASS','children':len(d['children'])},ensure_ascii=False,indent=2))
if __name__=='__main__':main()
