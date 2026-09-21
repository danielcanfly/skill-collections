#!/usr/bin/env python3
from pathlib import Path
import argparse,json,subprocess
from repair_common import *
ap=argparse.ArgumentParser();ap.add_argument('--candidate',required=True);ap.add_argument('--matrix',required=True);ap.add_argument('--output',required=True);a=ap.parse_args();m=load(a.matrix);results=[];errors=[]
for f in m.get('findings',[]):
 cmd=[x.replace('{candidate}',str(Path(a.candidate).resolve())) for x in f['closure_command']];proc=subprocess.run(cmd,capture_output=True,text=True);ok=proc.returncode==int(f.get('expected_exit_code',0));missing=[p for p in f.get('required_evidence_paths',[]) if not Path(p.replace('{candidate}',str(Path(a.candidate).resolve()))).exists()];ok=ok and not missing;results.append({'finding_id':f['finding_id'],'status':'PASS' if ok else 'FAIL','returncode':proc.returncode,'missing_evidence':missing,'stdout':proc.stdout[-1000:],'stderr':proc.stderr[-1000:]})
 if not ok:errors.append(f['finding_id'])
r={'status':'PASS' if not errors else 'FAIL','results':results,'failed':errors};write(a.output,r);print(json.dumps(r,indent=2));raise SystemExit(0 if not errors else 1)
