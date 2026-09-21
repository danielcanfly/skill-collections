#!/usr/bin/env python3
from pathlib import Path
import argparse
from common import load_json,result,emit
ap=argparse.ArgumentParser();ap.add_argument('root');ap.add_argument('--config');ap.add_argument('--profile');ap.add_argument('--output');a=ap.parse_args();root=Path(a.root);r=load_json(root/'qa/candidate_self_check_receipt.json',{});errors=[]
if not r: errors.append('missing qa/candidate_self_check_receipt.json')
if r.get('status')!='PASS': errors.append('candidate self-check is not PASS')
if r.get('decision') in {'MERGE_READY','ACCEPTED','FINAL_ACCEPTED'}: errors.append('candidate self-check illegally self-awards acceptance')
if r.get('decision')!='CANDIDATE_READY_FOR_INDEPENDENT_AUDIT': errors.append('candidate decision must be CANDIDATE_READY_FOR_INDEPENDENT_AUDIT')
if not r.get('researcher_id') or not r.get('completed_at'): errors.append('researcher_id/completed_at missing')
if int(r.get('open_p0',999)) or int(r.get('open_p1',999)): errors.append('candidate self-check has open P0/P1')
emit(result('PASS' if not errors else 'FAIL',errors,stats={'decision':r.get('decision')}),a.output)
