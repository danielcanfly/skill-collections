#!/usr/bin/env python3
from pathlib import Path
import argparse,difflib
from common import rows,result,emit,norm
ap=argparse.ArgumentParser();ap.add_argument('root');ap.add_argument('--config');ap.add_argument('--profile');ap.add_argument('--output');a=ap.parse_args();root=Path(a.root);rs=rows(root/'research/edge_entailment.csv');errors=[];items=[]
for r in rs:
    if r.get('support_label')!='contextual-support': continue
    key=f"{r.get('claim_id')}/{r.get('source_id')}"
    text=' | '.join((r.get(c) or '').strip() for c in ['shared_concept_or_method','source_passage_function','claim_context_function','why_context_not_entailment','transfer_boundary'])
    if len(text)<100: errors.append(f'{key}: contextual rationale lacks source-specific depth')
    items.append((key,text))
for i,(ka,ta) in enumerate(items):
    for kb,tb in items[i+1:]:
        q=difflib.SequenceMatcher(None,norm(ta),norm(tb)).ratio()
        if q>.82: errors.append(f'contextual rationales semantically templated {q:.3f}: {ka}/{kb}')
emit(result('PASS' if not errors else 'FAIL',errors,stats={'contextual_edges':len(items)}),a.output)
