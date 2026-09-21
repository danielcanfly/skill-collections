#!/usr/bin/env python3
from pathlib import Path
import argparse
from common import rows,result,emit
ap=argparse.ArgumentParser();ap.add_argument('root');ap.add_argument('--config');ap.add_argument('--profile');ap.add_argument('--output');a=ap.parse_args();root=Path(a.root);rs=rows(root/'research/source_claim_domain_compatibility.csv');edges=rows(root/'research/edge_entailment.csv');errors=[];required={'claim_id','source_id','source_domain','claim_domain','source_kind','transfer_type','compatibility_status','transfer_limit','independent_review_required','candidate_reviewer_status'}
if not rs: errors.append('missing or empty research/source_claim_domain_compatibility.csv')
elif not required.issubset(rs[0]): errors.append('domain compatibility columns missing: '+','.join(sorted(required-set(rs[0]))))
by={(r.get('claim_id','').strip(),r.get('source_id','').strip()):r for r in rs}
for e in edges:
 k=(e.get('claim_id','').strip(),e.get('source_id','').strip());r=by.get(k)
 if not r: errors.append(f'{k}: missing domain compatibility row');continue
 if r.get('compatibility_status')!='PASS': errors.append(f'{k}: domain compatibility not PASS')
 if r.get('source_domain')!=r.get('claim_domain'):
  if r.get('transfer_type') not in {'bounded-analogy','method-transfer','definition-transfer','jurisdiction-specific','entity-specific'}: errors.append(f'{k}: cross-domain transfer type invalid')
  if len((r.get('transfer_limit') or '').strip())<20: errors.append(f'{k}: cross-domain transfer limit missing')
  if str(r.get('independent_review_required','')).upper()!='TRUE': errors.append(f'{k}: cross-domain edge must require independent review')
 if str(r.get('candidate_reviewer_status','')).upper()!='PASS': errors.append(f'{k}: candidate domain review not PASS')
emit(result('PASS' if not errors else 'FAIL',errors,stats={'rows':len(rs)}),a.output)
