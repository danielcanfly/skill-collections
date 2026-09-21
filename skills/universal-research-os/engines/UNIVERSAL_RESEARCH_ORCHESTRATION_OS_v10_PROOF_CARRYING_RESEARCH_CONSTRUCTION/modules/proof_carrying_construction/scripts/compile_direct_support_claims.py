#!/usr/bin/env python3
from pathlib import Path
import argparse,sys,json,datetime
from common import *
def main():
 a=argparse.ArgumentParser();a.add_argument('root');x=a.parse_args();r=Path(x.root);rows=read_csv(r/'research/material_clause_registry.csv');reviews=read_csv(r/'external_stage_review/CLAUSE_REVIEW.csv');rm={q.get('clause_id'):q for q in reviews};groups={};e=[]
 if load(r/'qa/external_stage_review_validation.json',{}).get('status')!='PASS':e.append('external stage review not PASS')
 for q in rows:
  rv=rm.get(q.get('clause_id'),{})
  if q.get('support_status')!='SUPPORTED' or rv.get('verdict')!='PASS':continue
  groups.setdefault(q['proposed_claim_id'],[]).append(q)
 out=[]
 for cid,qs in sorted(groups.items()):
  if any(q.get('unsupported_remainder','').strip().lower() not in {'','none','n/a','not applicable'} for q in qs):e.append(cid+': unsupported remainder')
  out.append({'claim_id':cid,'claim_text':' '.join(q['clause_text'].strip() for q in qs),'material_clause_ids':'|'.join(q['clause_id'] for q in qs),'passage_ids':'|'.join(sorted({z for q in qs for z in q['passage_ids'].split('|') if z})),'construction_method':'COMPILED_FROM_EXTERNALLY_PRE_REVIEWED_CLAUSES','candidate_reviewer_status':'COMPILED'})
 if not out:e.append('no direct-support claims compiled; zero denominator is not PASS')
 if e:print(json.dumps({'status':'FAIL','errors':e},indent=2));sys.exit(1)
 write_csv(r/'research/compiled_direct_support_claims.csv',out,list(out[0]))
 receipt={'stage':'claims','status':'PASS','candidate_tree_sha256':tree_sha(r),'population_count':len(out),'passed_count':len(out),'failed_count':0,'compiler':'v10','stage_review_identity_sha256':sha_file(r/'external_stage_review/STAGE_REVIEW_IDENTITY.json'),'completed_at':datetime.datetime.now(datetime.timezone.utc).isoformat()};dump(r/'qa/claim_compilation_receipt.json',receipt);print(json.dumps(receipt,indent=2))
if __name__=='__main__':main()
