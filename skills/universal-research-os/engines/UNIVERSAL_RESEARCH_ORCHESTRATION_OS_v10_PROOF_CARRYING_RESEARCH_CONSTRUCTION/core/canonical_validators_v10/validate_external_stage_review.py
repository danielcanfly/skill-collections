#!/usr/bin/env python3
from pathlib import Path
import argparse,sys,json
from common import *
PASSAGE_FIELDS=['passage_id','source_id','excerpt_sha256','snapshot_sha256','locator_type','locator_value']
CLAUSE_FIELDS=['clause_id','proposed_claim_id','clause_text','passage_ids','support_status','unsupported_remainder']
def main():
 a=argparse.ArgumentParser();a.add_argument('root');x=a.parse_args();r=Path(x.root);errors=[]
 lineage=load(r/'handoff/contract_lineage.json',{});builder_id=str(lineage.get('researcher_id','')).strip();builder_session=str(lineage.get('researcher_session_id','')).strip()
 ident=load(r/'external_stage_review/STAGE_REVIEW_IDENTITY.json',{})
 if ident.get('status')!='PASS':errors.append('external stage review identity not PASS')
 if ident.get('contract_generation')!='v10' or ident.get('audit_os_version')!='6.0.0':errors.append('external stage review identity/version mismatch')
 reviewer=str(ident.get('reviewer_id','')).strip();review_session=str(ident.get('reviewer_session_id','')).strip()
 if not builder_id or not builder_session:errors.append('researcher identity/session missing from contract_lineage')
 if not reviewer or not review_session:errors.append('stage reviewer identity/session missing')
 if reviewer==builder_id or review_session==builder_session:errors.append('stage reviewer is not independent from research builder')
 passages=read_csv(r/'research/source_passage_registry.csv') if (r/'research/source_passage_registry.csv').exists() else []
 clauses=read_csv(r/'research/material_clause_registry.csv') if (r/'research/material_clause_registry.csv').exists() else []
 prev=read_csv(r/'external_stage_review/PASSAGE_REVIEW.csv') if (r/'external_stage_review/PASSAGE_REVIEW.csv').exists() else []
 crev=read_csv(r/'external_stage_review/CLAUSE_REVIEW.csv') if (r/'external_stage_review/CLAUSE_REVIEW.csv').exists() else []
 if not passages:errors.append('source passage population empty')
 if not clauses:errors.append('material clause population empty')
 pm={q.get('passage_id'):q for q in passages};pr={q.get('passage_id'):q for q in prev}
 cm={q.get('clause_id'):q for q in clauses};cr={q.get('clause_id'):q for q in crev}
 if set(pm)!=set(pr):errors.append(f'passage review population mismatch expected={len(pm)} reviewed={len(pr)}')
 if set(cm)!=set(cr):errors.append(f'clause review population mismatch expected={len(cm)} reviewed={len(cr)}')
 for pid,row in pm.items():
  rv=pr.get(pid,{})
  if rv.get('verdict')!='PASS':errors.append(pid+': external passage verdict not PASS')
  if rv.get('row_sha256')!=row_sha(row,PASSAGE_FIELDS):errors.append(pid+': passage review row SHA mismatch')
  if rv.get('reviewer_id')!=reviewer or rv.get('reviewer_session_id')!=review_session:errors.append(pid+': passage reviewer identity mismatch')
  if not rv.get('reviewed_at'):errors.append(pid+': passage reviewed_at missing')
 for cid,row in cm.items():
  rv=cr.get(cid,{})
  expected='PASS' if row.get('support_status')=='SUPPORTED' and row.get('unsupported_remainder','').strip().lower() in {'','none','n/a','not applicable'} else 'NON_DIRECT'
  if rv.get('verdict')!=expected:errors.append(cid+f': clause verdict {rv.get("verdict")} != {expected}')
  if rv.get('row_sha256')!=row_sha(row,CLAUSE_FIELDS):errors.append(cid+': clause review row SHA mismatch')
  if rv.get('reviewer_id')!=reviewer or rv.get('reviewer_session_id')!=review_session:errors.append(cid+': clause reviewer identity mismatch')
  if not rv.get('reviewed_at'):errors.append(cid+': clause reviewed_at missing')
 psha=sha_file(r/'research/source_passage_registry.csv') if (r/'research/source_passage_registry.csv').exists() else ''
 csha=sha_file(r/'research/material_clause_registry.csv') if (r/'research/material_clause_registry.csv').exists() else ''
 if ident.get('passage_registry_sha256')!=psha:errors.append('stage identity passage registry SHA mismatch')
 if ident.get('clause_registry_sha256')!=csha:errors.append('stage identity clause registry SHA mismatch')
 out={'status':'PASS' if not errors else 'FAIL','reviewer_id':reviewer,'reviewer_session_id':review_session,'passage_population':len(passages),'clause_population':len(clauses),'errors':errors}
 dump(r/'qa/external_stage_review_validation.json',out);print(json.dumps(out,indent=2));sys.exit(0 if not errors else 1)
if __name__=='__main__':main()
