#!/usr/bin/env python3
from pathlib import Path
import argparse
from common import rows,result,emit
ap=argparse.ArgumentParser();ap.add_argument('root');ap.add_argument('--config');ap.add_argument('--profile');ap.add_argument('--output');a=ap.parse_args();root=Path(a.root);clauses=rows(root/'research/claim_clause_matrix.csv');edges=rows(root/'research/edge_entailment.csv');errors=[];required={'claim_id','clause_id','clause_text','materiality','source_id','passage_id','support_status','unsupported_reason','candidate_reviewer_status'}
if not clauses: errors.append('missing or empty research/claim_clause_matrix.csv')
elif not required.issubset(clauses[0]): errors.append('claim clause columns missing: '+','.join(sorted(required-set(clauses[0]))))
by={}
for r in clauses:
 k=(r.get('claim_id','').strip(),r.get('source_id','').strip());by.setdefault(k,[]).append(r)
 if not r.get('clause_id') or len((r.get('clause_text') or '').strip())<8: errors.append(f'{k}: invalid clause')
 if r.get('materiality') not in {'material','non-material'}: errors.append(f'{k}: invalid materiality')
 if str(r.get('candidate_reviewer_status','')).upper()!='PASS': errors.append(f'{k}: candidate clause review not PASS')
for e in edges:
 k=(e.get('claim_id','').strip(),e.get('source_id','').strip());rs=by.get(k,[]);lab=e.get('support_label','')
 if not rs: errors.append(f'{k}: no clause matrix rows');continue
 material=[x for x in rs if x.get('materiality')=='material']
 if lab=='support' and any(x.get('support_status')!='SUPPORTED' for x in material): errors.append(f'{k}: direct support has unsupported material clause')
 if lab=='partial-support' and not(any(x.get('support_status')=='SUPPORTED' for x in material) and any(x.get('support_status')!='SUPPORTED' for x in material)): errors.append(f'{k}: partial support must contain supported and unsupported material clauses')
 if lab=='contextual-support' and any(x.get('support_status')=='SUPPORTED' for x in material): errors.append(f'{k}: contextual edge may not claim material-clause support')
emit(result('PASS' if not errors else 'FAIL',errors,stats={'clause_rows':len(clauses),'edge_pairs':len(by)}),a.output)
