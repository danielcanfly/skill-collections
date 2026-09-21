#!/usr/bin/env python3
from pathlib import Path
import argparse,re
from common import load_json,result,emit
ap=argparse.ArgumentParser();ap.add_argument('root');ap.add_argument('--config');ap.add_argument('--profile');ap.add_argument('--output');a=ap.parse_args();root=Path(a.root);cfg=load_json(a.config or root/'audit_config.json',{});errors=[]
truth={k:cfg.get(k) for k in ['candidate_id','candidate_version','final_output_name']}
for rel in ['PHASE_RETURN_MANIFEST.json','handoff/merge_manifest.json']:
    d=load_json(root/rel,{})
    for k,v in truth.items():
        if v and d.get(k)!=v: errors.append(f'{rel}: {k} mismatch')
    if str(d.get('status','')).upper()=='MERGE_READY': errors.append(f'{rel}: candidate self-awarded MERGE_READY')
for rel in ['00_COMPLETION_SUMMARY.md','QUALITY_REPORT.md','qa/final_acceptance_checklist.md']:
    p=root/rel
    if p.exists() and truth['final_output_name'] and truth['final_output_name'] not in p.read_text(encoding='utf-8',errors='replace'): errors.append(f'{rel}: final output identity missing')
emit(result('PASS' if not errors else 'FAIL',errors,stats=truth),a.output)
