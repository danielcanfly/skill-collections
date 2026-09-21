#!/usr/bin/env python3
from pathlib import Path
import argparse,csv,json,hashlib,datetime,sys
def rows(p):
 with Path(p).open(newline='',encoding='utf-8-sig') as f:return list(csv.DictReader(f))
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def main():
 a=argparse.ArgumentParser();a.add_argument('candidate_root');a.add_argument('review_dir');a.add_argument('--attest-independent',action='store_true');x=a.parse_args();r=Path(x.candidate_root);d=Path(x.review_dir);ident=json.loads((d/'STAGE_REVIEW_IDENTITY.json').read_text());e=[]
 if not x.attest_independent:e.append('independence attestation missing')
 lineage=json.loads((r/'handoff/contract_lineage.json').read_text());
 if ident.get('reviewer_id')==lineage.get('researcher_id') or ident.get('reviewer_session_id')==lineage.get('researcher_session_id'):e.append('stage reviewer is not independent')
 for q in rows(d/'PASSAGE_REVIEW.csv'):
  if q.get('verdict')!='PASS':e.append('passage not PASS '+q.get('passage_id','?'))
  if not q.get('reviewed_at'):e.append('passage reviewed_at missing '+q.get('passage_id','?'))
 clauses={q.get('clause_id'):q for q in rows(r/'research/material_clause_registry.csv')}
 for q in rows(d/'CLAUSE_REVIEW.csv'):
  c=clauses.get(q.get('clause_id'),{});expected='PASS' if c.get('support_status')=='SUPPORTED' and c.get('unsupported_remainder','').strip().lower() in {'','none','n/a','not applicable'} else 'NON_DIRECT'
  if q.get('verdict')!=expected:e.append('clause verdict mismatch '+q.get('clause_id','?'))
  if not q.get('reviewed_at'):e.append('clause reviewed_at missing '+q.get('clause_id','?'))
 ident.update({'status':'PASS' if not e else 'FAIL','independence_attestation':bool(x.attest_independent),'completed_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'passage_review_sha256':sha(d/'PASSAGE_REVIEW.csv'),'clause_review_sha256':sha(d/'CLAUSE_REVIEW.csv'),'errors':e});(d/'STAGE_REVIEW_IDENTITY.json').write_text(json.dumps(ident,indent=2)+'\n');print(json.dumps({'status':ident['status'],'errors':e},indent=2));sys.exit(0 if not e else 1)
if __name__=='__main__':main()
