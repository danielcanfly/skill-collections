#!/usr/bin/env python3
import argparse,json,csv
from repair_common import *
ap=argparse.ArgumentParser();ap.add_argument('--source',required=True);ap.add_argument('--returned',required=True);ap.add_argument('--contract',required=True);a=ap.parse_args();c=load(a.contract);td1,r1=extract(a.source);td2,r2=extract(a.returned);f1=files(r1);f2=files(r2);allp=sorted(set(f1)|set(f2));errors=[];changed=[]
for p in allp:
 h1=sha(f1[p]) if p in f1 else None;h2=sha(f2[p]) if p in f2 else None
 if h1==h2:continue
 changed.append(p);ar=rule_matches(p,c.get('allowed_change_rules',[]));ir=rule_matches(p,c.get('immutable_rules',[]))
 if not ar:errors.append('unauthorized changed path '+p)
 if ir:errors.append('immutable path changed '+p)
 # CSV field-level restriction
 for rule in ar:
  if rule.get('file_type')=='csv' and p in f1 and p in f2 and rule.get('allowed_columns'):
   with f1[p].open(newline='',encoding='utf-8-sig') as A,f2[p].open(newline='',encoding='utf-8-sig') as B:
    ra=list(csv.DictReader(A));rb=list(csv.DictReader(B));keys=rule.get('key_columns',[]);idxa={tuple(x.get(k,'') for k in keys):x for x in ra};idxb={tuple(x.get(k,'') for k in keys):x for x in rb}
    for key in set(idxa)&set(idxb):
     for col in set(idxa[key])|set(idxb[key]):
      if idxa[key].get(col,'')!=idxb[key].get(col,'') and col not in rule['allowed_columns']:errors.append(f'forbidden CSV field change {p} {key} {col}')
td1.cleanup();td2.cleanup();print(json.dumps({'status':'PASS' if not errors else 'FAIL','changed_paths':changed,'errors':errors},indent=2));raise SystemExit(0 if not errors else 1)
