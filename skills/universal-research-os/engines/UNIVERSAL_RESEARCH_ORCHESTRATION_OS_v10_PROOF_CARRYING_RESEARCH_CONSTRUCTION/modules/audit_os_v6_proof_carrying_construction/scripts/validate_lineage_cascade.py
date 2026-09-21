#!/usr/bin/env python3
from pathlib import Path
import argparse,re
from common import rows,load_json,result,emit,split_ids
ap=argparse.ArgumentParser();ap.add_argument('root');ap.add_argument('--config');ap.add_argument('--profile');ap.add_argument('--output');a=ap.parse_args();root=Path(a.root);reg=rows(root/'research/lineage_cascade_register.csv');claims=rows(root/'research/claim_ledger.csv');canon=rows(root/'research/canonical_concept_registry.csv');disp=rows(root/'research/expected_node_disposition.csv');errors=[]
if not reg: errors.append('lineage register missing or empty')
by={r.get('node_id',''):r for r in reg}; actual={}
for r in claims:
    n=r.get('candidate_node','').strip(); s=r.get('source_id','').strip(); c=r.get('claim_id','').strip()
    if n: actual.setdefault(n,{'sources':set(),'claims':set()}); actual[n]['sources'].add(s) if s else None; actual[n]['claims'].add(c) if c else None
for n,v in actual.items():
    r=by.get(n)
    if not r: errors.append(f'{n}: missing lineage row'); continue
    aset=v['sources']; rset=split_ids(r.get('active_source_ids')); cset=split_ids(r.get('active_claim_ids'))
    if aset!=rset: errors.append(f'{n}: active source mismatch actual={sorted(aset)} registry={sorted(rset)}')
    if v['claims']!=cset: errors.append(f'{n}: active claim mismatch')
    for col in ['registry_source_ids','expected_disposition_source_ids','node_frontmatter_source_ids','source_note_reverse_source_ids']:
        if split_ids(r.get(col))!=aset: errors.append(f'{n}: {col} mismatch')
    try: cnt=int(r.get('source_count') or -1)
    except: cnt=-1
    if cnt!=len(aset): errors.append(f'{n}: source_count {cnt}!={len(aset)}')
    if (r.get('status') or '').upper()!='PASS': errors.append(f'{n}: lineage row not PASS')
receipt=load_json(root/'qa/lineage_cascade_receipt.json',{})
if receipt.get('status')=='PASS' and errors: errors.append('lineage receipt claims PASS despite register mismatches')
if receipt.get('status')!='PASS': errors.append('lineage receipt not PASS')
emit(result('PASS' if not errors else 'FAIL',errors,stats={'lineage_rows':len(reg),'nodes_with_active_claims':len(actual)}),a.output)
