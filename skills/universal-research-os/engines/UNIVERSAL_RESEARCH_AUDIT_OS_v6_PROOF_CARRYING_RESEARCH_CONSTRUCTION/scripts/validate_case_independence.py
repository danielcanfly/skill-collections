#!/usr/bin/env python3
from pathlib import Path
import argparse
from common import rows,load_json,result,emit,split_ids
ap=argparse.ArgumentParser();ap.add_argument('root');ap.add_argument('--config');ap.add_argument('--profile');ap.add_argument('--output');a=ap.parse_args();root=Path(a.root);fams=rows(root/'research/evidence_family_registry.csv');cases=rows(root/'research/case_registry.csv');meta=rows(root/'research/source_metadata_reconciliation.csv');errors=[]
by_src={r.get('source_id',''):r.get('evidence_family_id','') for r in meta}; fb={r.get('evidence_family_id',''):r for r in fams}
for f in fams:
    if (f.get('status') or '').lower()=='active' and not split_ids(f.get('source_ids')): errors.append(f"{f.get('evidence_family_id')}: active family has no sources")
    if (f.get('status') or '').lower()=='active':
        for c in ['issuer_root','method_root','data_generation_root','publication_chain_root','independence_basis']:
            if not (f.get(c) or '').strip(): errors.append(f"{f.get('evidence_family_id')}: missing {c}")
checked=0
for c in cases:
    if (c.get('case_type') or '').lower()!='evidence-backed': continue
    checked+=1; sids=split_ids(c.get('source_ids')); fids={by_src.get(s) for s in sids if by_src.get(s)}
    roots=set()
    for fid in fids:
        f=fb.get(fid,{})
        roots.add((f.get('issuer_root'),f.get('method_root'),f.get('data_generation_root'),f.get('publication_chain_root')))
    if len(roots)<2: errors.append(f"{c.get('case_id')}: fewer than two independently generated evidence roots")
receipt=load_json(root/'qa/case_independence_receipt.json',{})
if receipt.get('status')!='PASS': errors.append('case independence receipt not PASS')
if receipt.get('status')=='PASS' and errors: errors.append('case independence receipt masks individual failures')
emit(result('PASS' if not errors else 'FAIL',errors,stats={'families':len(fams),'evidence_backed_cases_checked':checked}),a.output)
