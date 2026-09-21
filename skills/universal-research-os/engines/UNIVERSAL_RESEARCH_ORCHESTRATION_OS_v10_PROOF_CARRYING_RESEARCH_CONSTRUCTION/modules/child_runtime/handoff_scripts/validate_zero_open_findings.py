#!/usr/bin/env python3
from pathlib import Path
import argparse,json,csv
from common import result,emit,load_json

ap=argparse.ArgumentParser(); ap.add_argument('root'); ap.add_argument('--config'); ap.add_argument('--profile'); ap.add_argument('--output'); a=ap.parse_args()
root=Path(a.root); profile=load_json(a.profile,{}) if a.profile else {}; errors=[]; warnings=[]; open_rows=[]
allow_p2=bool(profile.get('allow_open_p2',False))
for p in root.rglob('*'):
    if not p.is_file() or p.name.lower() not in {'findings_register.json','findings_register.csv','global_findings_register.csv','residual_claim_gaps.csv','source_refresh_queue.csv','residual_source_gaps.csv'}: continue
    if p.suffix.lower()=='.json':
        data=load_json(p,[]); rs=data.get('findings',data.get('rows',[])) if isinstance(data,dict) else data
    else:
        with p.open(encoding='utf-8-sig',newline='') as f: rs=list(csv.DictReader(f))
    for r in rs or []:
        if not isinstance(r,dict): continue
        status=str(r.get('status') or r.get('disposition') or r.get('state') or 'open').strip().lower(); sev=str(r.get('severity') or r.get('priority') or 'p2').strip().upper()
        if status not in {'closed','resolved','pass','accepted','waived','not-applicable'}: open_rows.append((p.relative_to(root).as_posix(),sev,r.get('finding_id') or r.get('source_id') or r.get('claim_id') or '?'))
for path,sev,fid in open_rows:
    if sev in {'P0','P1'} or not allow_p2: errors.append(f'{path}: open {sev} finding {fid}')
if not allow_p2 and open_rows: errors.append(f'production profile requires zero open P0/P1/P2; found {len(open_rows)} open rows')
emit(result('PASS' if not errors else 'FAIL',errors,warnings,{'open_findings':len(open_rows),'allow_open_p2':allow_p2}),a.output)
