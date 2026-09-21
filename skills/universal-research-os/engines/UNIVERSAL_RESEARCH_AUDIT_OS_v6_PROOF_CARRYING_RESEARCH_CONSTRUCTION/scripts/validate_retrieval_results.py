#!/usr/bin/env python3
from pathlib import Path
import argparse,hashlib
from common import load_json,result,emit
ap=argparse.ArgumentParser();ap.add_argument('root');ap.add_argument('--config');ap.add_argument('--profile');ap.add_argument('--output');a=ap.parse_args();root=Path(a.root);tests=load_json(root/'qa/retrieval_test_cases.json',[]) or [];res=load_json(root/'qa/retrieval_results.json',{}) or {};errors=[]
items=res.get('results',res if isinstance(res,list) else []);by={x.get('test_id'):x for x in items if isinstance(x,dict)};corpus=res.get('corpus_sha256') or res.get('corpus_hash')
if not corpus: errors.append('retrieval results missing corpus hash')
for t in tests:
    tid=t.get('test_id');r=by.get(tid)
    if not r or r.get('status')!='PASS': errors.append(f'{tid}: retrieval not PASS');continue
    qh=hashlib.sha256((t.get('query') or '').encode()).hexdigest()
    if t.get('immutable_query') and t.get('query_sha256')!=qh: errors.append(f'{tid}: test query hash invalid')
    if t.get('immutable_query') and r.get('query_sha256')!=qh: errors.append(f'{tid}: result query hash mismatch')
    ranks=r.get('ranked_ids',[]);exp=t.get('expected_ids',[]);neg=t.get('negative_ids',[])
    if any(x not in ranks for x in exp): errors.append(f'{tid}: expected ID absent')
    if exp and neg:
        ep=[ranks.index(x) for x in exp if x in ranks];np=[ranks.index(x) for x in neg if x in ranks]
        if np and ep and min(np)<min(ep): errors.append(f'{tid}: negative outranks expected')
    pri=t.get('primary_source_ids',[]);sec=t.get('secondary_or_practitioner_negative_ids',[])
    if pri:
        pp=[ranks.index(x) for x in pri if x in ranks];sp=[ranks.index(x) for x in sec if x in ranks]
        if len(pp)<len(pri) or (sp and max(pp)>=min(sp)): errors.append(f'{tid}: authority ranking failed')
emit(result('PASS' if not errors else 'FAIL',errors,stats={'tests':len(tests),'results':len(items),'corpus_hash':corpus}),a.output)
