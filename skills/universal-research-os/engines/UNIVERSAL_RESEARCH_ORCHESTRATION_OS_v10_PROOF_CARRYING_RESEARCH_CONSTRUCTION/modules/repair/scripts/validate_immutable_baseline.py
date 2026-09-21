#!/usr/bin/env python3
import argparse,json
from repair_common import *
ap=argparse.ArgumentParser();ap.add_argument('--candidate',required=True);ap.add_argument('--baseline',required=True);a=ap.parse_args();base=load(a.baseline);td,root=extract(a.candidate);fs=files(root);errors=[]
for row in base.get('files',[]):
 p=row['path']
 if p not in fs:errors.append('missing immutable '+p)
 elif sha(fs[p])!=row['sha256']:errors.append('immutable mismatch '+p)
td.cleanup();print(json.dumps({'status':'PASS' if not errors else 'FAIL','errors':errors},indent=2));raise SystemExit(0 if not errors else 1)
