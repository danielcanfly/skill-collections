#!/usr/bin/env python3
from pathlib import Path
import argparse,subprocess,sys,json,tempfile
from repair_common import *
ap=argparse.ArgumentParser();ap.add_argument('--source',required=True);ap.add_argument('--returned',required=True);ap.add_argument('--contract',required=True);ap.add_argument('--closure-matrix',required=True);ap.add_argument('--audit-os',required=True);ap.add_argument('--repair-handoff',required=True);ap.add_argument('--admission-receipt',required=True);ap.add_argument('--independent-review-dir',required=True);ap.add_argument('--output-dir',default='FINAL_ACCEPTANCE');a=ap.parse_args();c=load(a.contract);out=Path(a.output_dir).resolve();out.mkdir(parents=True,exist_ok=True);errors=[];results=[]
def run(id,cmd):
 p=subprocess.run(cmd,capture_output=True,text=True);results.append({'id':id,'returncode':p.returncode,'stdout':p.stdout[-2000:],'stderr':p.stderr[-2000:]});
 if p.returncode!=0:errors.append(id)
if Path(a.returned).name!=c['expected_output_name']:errors.append('exact_filename')
# Returned candidate must be bound to this exact repair handoff.
td,rr=extract(a.returned);lin=load(rr/'handoff/contract_lineage.json') if (rr/'handoff/contract_lineage.json').exists() else {};td.cleanup();
if lin.get('originating_handoff_id')!=c['repair_id']:errors.append('repair_handoff_id_mismatch')
if lin.get('originating_handoff_sha256')!=sha(a.repair_handoff):errors.append('repair_handoff_sha_mismatch')
run('repair_delta',[sys.executable,str(Path(__file__).with_name('validate_repair_delta.py')),'--source',a.source,'--returned',a.returned,'--contract',a.contract])
run('class_wide_closure',[sys.executable,str(Path(__file__).with_name('validate_class_wide_closure.py')),a.closure_matrix,'--candidate-root',a.returned,'--output',str(out/'class_wide_closure.json')])
run('finding_closure',[sys.executable,str(Path(__file__).with_name('validate_finding_closure.py')),'--candidate',a.returned,'--matrix',a.closure_matrix,'--output',str(out/'finding_closure.json')])
run('cascade_closure',[sys.executable,str(Path(__file__).with_name('validate_cascade_closure.py')),'--candidate',a.returned,'--contract',a.contract,'--output',str(out/'cascade_closure.json')])
run('independent_audit',[sys.executable,str(Path(a.audit_os)/'scripts/audit_candidate.py'),a.returned,'--admission-receipt',a.admission_receipt,'--independent-review-dir',a.independent_review_dir,'--output',str(out/'AUDIT')])
r={'status':'PASS' if not errors else 'FAIL','errors':errors,'results':results,'returned_sha256':sha(a.returned)};write(out/'FINAL_ACCEPTANCE.json',r);print(json.dumps(r,indent=2));raise SystemExit(0 if not errors else 1)
