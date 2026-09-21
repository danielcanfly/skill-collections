#!/usr/bin/env python3
from pathlib import Path
import argparse,json
ap=argparse.ArgumentParser();ap.add_argument('root');ap.add_argument('--config');ap.add_argument('--profile');ap.add_argument('--output',required=True);a=ap.parse_args();p=Path(a.root)/'handoff/contract_lineage.json';errors=[]
try:o=json.loads(p.read_text(encoding='utf-8'))
except Exception as e:o={};errors.append('contract lineage missing or invalid')
for k in ['originating_handoff_id','originating_handoff_sha256','orchestration_os_version','audit_os_version','contract_generation','expected_output_name']:
 if not o.get(k):errors.append('missing '+k)
if o.get('status')!='BOUND':errors.append('lineage status not BOUND')
r={'status':'PASS' if not errors else 'FAIL','errors':errors};Path(a.output).write_text(json.dumps(r,indent=2)+'\n');raise SystemExit(0 if not errors else 1)
