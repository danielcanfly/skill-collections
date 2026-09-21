#!/usr/bin/env python3
from pathlib import Path
import argparse,hashlib,json,subprocess,tempfile,shutil,sys
def locate(p):
 p=Path(p).resolve()
 if (p/'qa').is_dir(): return p
 ds=[x for x in p.iterdir() if x.is_dir() and (x/'qa').is_dir()]
 if len(ds)==1:return ds[0]
 raise SystemExit('candidate root not found')
def snap(root): return {str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(root.rglob('*')) if p.is_file() and p.name!='IDEMPOTENCY_RECEIPT.json'}
def call(cmd,cwd):
 r=subprocess.run(cmd,cwd=cwd,text=True,capture_output=True); return {'command':cmd,'returncode':r.returncode,'stdout':r.stdout[-1600:],'stderr':r.stderr[-1600:]}
def main():
 ap=argparse.ArgumentParser(); ap.add_argument('candidate'); ap.add_argument('--case-min',type=int,required=True); ap.add_argument('--output'); a=ap.parse_args()
 with tempfile.TemporaryDirectory() as td:
  shutil.copytree(Path(a.candidate).resolve(),Path(td)/'x'); root=locate(Path(td)/'x'); py=sys.executable
  cmds=[[py,str(root/'qa/render_identity_surfaces.py'),str(root)],[py,str(root/'qa/run_retrieval_benchmark.py'),'--root',str(root)],[py,str(root/'qa/run_auditor_holdout.py'),str(root),'--tests',str(root/'qa/AUDITOR_HOLDOUT_TESTS.json'),'--source-tests',str(root/'qa/AUDITOR_SOURCE_PROVENANCE_TESTS.json')]]
  for name in ['validate_semantic_provenance.py','validate_audit_os_contract.py','validate_source_identity.py','validate_edge_entailment.py','validate_contextual_relevance.py','validate_disposition_status.py','validate_lineage_cascade.py','validate_node_semantic_diversity.py','validate_temporal_metadata.py','validate_case_independence.py','validate_topic_red_team.py','validate_repair_contract_conflicts.py','validate_identity_surfaces.py']:
   cmds.append([py,str(root/'qa'/name),str(root)])
  cmds += [[py,str(root/'qa/update_seal_state.py'),str(root)],[py,str(root/'qa/validate_seal_state.py'),str(root)],[py,str(root/'qa/make_file_manifest.py'),str(root)],[py,str(root/'qa/validate_package.py'),str(root),'--case-min',str(a.case_min)]]
  one=[call(c,root) for c in cmds]; s1=snap(root); two=[call(c,root) for c in cmds]; s2=snap(root); changed=sorted(k for k in set(s1)|set(s2) if s1.get(k)!=s2.get(k)); out={'status':'PASS' if all(x['returncode']==0 for x in one+two) and not changed else 'FAIL','first_run':one,'second_run':two,'changed_after_second_run':changed}; txt=json.dumps(out,ensure_ascii=False,indent=2); print(txt)
  if a.output: Path(a.output).write_text(txt+'\n',encoding='utf-8')
  raise SystemExit(0 if out['status']=='PASS' else 1)
if __name__=='__main__': main()
