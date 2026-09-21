#!/usr/bin/env python3
from pathlib import Path
import argparse,json
ap=argparse.ArgumentParser();ap.add_argument('root');ap.add_argument('--json-output');a=ap.parse_args();root=Path(a.root);p=root/'handoff/contract_lineage.json';errors=[]
try:o=json.loads(p.read_text(encoding='utf-8'))
except Exception as e:o={};errors.append('contract lineage missing or invalid: '+str(e))
for k in ['originating_handoff_id','originating_handoff_sha256','orchestration_os_version','audit_os_version','contract_generation','expected_output_name']:
 if not o.get(k) or str(o.get(k)).startswith('REQUIRED'): errors.append('missing '+k)
if o.get('status')!='BOUND': errors.append('contract lineage status must be BOUND')
if o.get('orchestration_os_version') and not str(o['orchestration_os_version']).startswith('7.'): errors.append('candidate is not v7-native')
r={'status':'PASS' if not errors else 'FAIL','errors':errors};out=json.dumps(r,indent=2)
if a.json_output:Path(a.json_output).write_text(out+'\n')
print(out);raise SystemExit(0 if not errors else 1)
