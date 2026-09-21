#!/usr/bin/env python3
import argparse,csv,json,sys
from pathlib import Path
p=argparse.ArgumentParser(); p.add_argument('--templates',required=True); p.add_argument('--actual',required=True); p.add_argument('--receipt',required=True); a=p.parse_args()
T=Path(a.templates); A=Path(a.actual); errors=[]; checked=0
for tp in sorted(T.glob('*.csv')):
    ap=A/tp.name
    if not ap.exists(): errors.append({'file':tp.name,'error':'missing'}); continue
    with tp.open(newline='',encoding='utf-8-sig') as f: th=next(csv.reader(f),[])
    with ap.open(newline='',encoding='utf-8-sig') as f: ah=next(csv.reader(f),[])
    checked+=1
    if th!=ah: errors.append({'file':tp.name,'expected':th,'actual':ah})
r={'checked':checked,'errors':errors,'pass':not errors}; Path(a.receipt).write_text(json.dumps(r,indent=2)+'\n'); print(json.dumps(r,indent=2)); sys.exit(0 if r['pass'] else 1)
