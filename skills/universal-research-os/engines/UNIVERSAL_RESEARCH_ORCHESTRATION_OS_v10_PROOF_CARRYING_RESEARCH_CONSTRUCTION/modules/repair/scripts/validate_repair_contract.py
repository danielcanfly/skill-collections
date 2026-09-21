#!/usr/bin/env python3
from pathlib import Path
import argparse,json
from repair_common import *
ap=argparse.ArgumentParser();ap.add_argument('contract');ap.add_argument('--candidate');ap.add_argument('--closure-matrix');a=ap.parse_args();c=load(a.contract);errors=[]
for k in ['repair_id','source_candidate_sha256','originating_handoff_id','originating_handoff_sha256','expected_output_name','finding_ids','allowed_change_rules','immutable_rules','required_cascade_checks','negative_control','positive_control']:
 if not c.get(k):errors.append('missing '+k)
if a.candidate:
 td,root=extract(a.candidate);fs=files(root)
 for path in fs:
  ar=rule_matches(path,c.get('allowed_change_rules',[]));ir=rule_matches(path,c.get('immutable_rules',[]))
  if ar and ir:errors.append('allowed/immutable overlap on actual file '+path)
 td.cleanup()
if a.closure_matrix:
 m=load(a.closure_matrix);ids={x.get('finding_id') for x in m.get('findings',[])}
 for fid in c.get('finding_ids',[]):
  if fid not in ids:errors.append('finding lacks closure rule: '+fid)

if c.get('class_wide_closure_required') is not True: errors.append('class_wide_closure_required must be true')
if c.get('retained_direct_support_full_review_required') is not True: errors.append('retained_direct_support_full_review_required must be true')
if c.get('independent_reaudit_required') is not True: errors.append('independent_reaudit_required must be true')
if a.closure_matrix:
 m=load(a.closure_matrix)
 for row in m.get('findings',[]):
  if row.get('closure_scope')!='CLASS_WIDE': errors.append('finding closure_scope must be CLASS_WIDE: '+str(row.get('finding_id')))
  if not row.get('population_selector'): errors.append('finding population_selector missing: '+str(row.get('finding_id')))
  if int(row.get('expected_population_count',-1))<0: errors.append('finding expected_population_count invalid: '+str(row.get('finding_id')))
  if row.get('review_all_retained_direct_support') is not True: errors.append('finding must review all retained direct support: '+str(row.get('finding_id')))
  if not isinstance(row.get('population_command'),list) or not row.get('population_command'): errors.append('finding population_command missing: '+str(row.get('finding_id')))
  if not isinstance(row.get('closure_command'),list) or not row.get('closure_command'): errors.append('finding closure_command missing: '+str(row.get('finding_id')))
print(json.dumps({'status':'PASS' if not errors else 'FAIL','errors':errors},indent=2));raise SystemExit(0 if not errors else 1)
