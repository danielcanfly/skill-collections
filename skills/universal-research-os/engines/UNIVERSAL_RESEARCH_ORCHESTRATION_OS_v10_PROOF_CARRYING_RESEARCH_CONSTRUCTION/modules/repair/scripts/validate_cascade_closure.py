#!/usr/bin/env python3
from pathlib import Path
import argparse,json,subprocess
from repair_common import *
ap=argparse.ArgumentParser();ap.add_argument('--candidate',required=True);ap.add_argument('--contract',required=True);ap.add_argument('--output',required=True);a=ap.parse_args();c=load(a.contract);results=[];errors=[]
for i,ch in enumerate(c.get('required_cascade_checks',[]),1):
 if isinstance(ch,str):results.append({'id':f'cascade-{i}','status':'DOCUMENTED','description':ch});continue
 cmd=[x.replace('{candidate}',str(Path(a.candidate).resolve())) for x in ch.get('command',[])];proc=subprocess.run(cmd,capture_output=True,text=True);ok=proc.returncode==int(ch.get('expected_exit_code',0));results.append({'id':ch.get('id',f'cascade-{i}'),'status':'PASS' if ok else 'FAIL','stdout':proc.stdout[-1000:],'stderr':proc.stderr[-1000:]})
 if not ok:errors.append(results[-1]['id'])
r={'status':'PASS' if not errors else 'FAIL','results':results,'failed':errors};write(a.output,r);print(json.dumps(r,indent=2));raise SystemExit(0 if not errors else 1)
