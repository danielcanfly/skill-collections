#!/usr/bin/env python3
from pathlib import Path
import argparse,json,shutil,tempfile,sys,csv,zipfile
from handoff_common import *
FORBIDDEN_NAMES=('KNOWN_GOOD','FINAL_ANSWER','MERGE_READY_CERTIFICATE','ANSWER_KEY')
def main():
 a=argparse.ArgumentParser();a.add_argument('candidate');a.add_argument('contract');a.add_argument('--audit-evidence',required=True);a.add_argument('--output',required=True);x=a.parse_args();c=json.loads(Path(x.contract).read_text());errors=[]
 if not c.get('failure_classes'):errors.append('failure_classes must be non-empty')
 baseline=c.get('protected_surface_baseline',{}).get('files',[])
 if not baseline:errors.append('protected_surface_baseline.files must be non-empty')
 for src in [Path(x.candidate),Path(x.audit_evidence)]:
  if any(k in src.name.upper() for k in FORBIDDEN_NAMES):errors.append('known-good/final-answer artifact forbidden: '+src.name)
 if errors:print(json.dumps({'status':'FAIL','errors':errors},indent=2));sys.exit(1)
 td=tempfile.mkdtemp();r=Path(td)/(c.get('handoff_name') or 'V10_REPAIR_HANDOFF');r.mkdir();shutil.copy2(x.candidate,r/'SOURCE_CANDIDATE.zip');shutil.copy2(x.contract,r/'repair_contract.json');shutil.copy2(x.audit_evidence,r/'AUDIT_EVIDENCE.zip');copy_tools(r/'tools')
 dump(r/'HANDOFF_IDENTITY.json',{'handoff_id':c['handoff_id'],'type':'BOUNDED_REPAIR','status':'ACTIVE','orchestration_os_version':'10.0.0','audit_os_version':'6.0.0','contract_generation':'v10','source_candidate_sha256':sha(x.candidate)});dump(r/'TARGET_IDENTITY.json',c);dump(r/'SOURCE_INPUT_REGISTRY.json',{'inputs':[{'filename':'SOURCE_CANDIDATE.zip','sha256':sha(x.candidate)},{'filename':'AUDIT_EVIDENCE.zip','sha256':sha(x.audit_evidence)}]});dump(r/'PROTECTED_SURFACE_BASELINE.json',c['protected_surface_baseline']);dump(r/'REQUIRED_OUTPUTS_AND_ACCEPTANCE.json',{'required_outputs':c['required_outputs'],'failure_class_population_required':True,'external_class_wide_reaudit_required':True});dump(r/'INDEPENDENCE_STATE_MACHINE.json',{'states':['GATE0','CONSTRUCT_REPAIR','RETURN','EXTERNAL_CLASS_WIDE_REAUDIT','PROMOTION'],'child_stop_state':'RETURN','child_forbidden_states':['MERGE_READY','PRODUCTION_RELEASE']});dump(r/'GATE0_RESPONSE.json',{'status':'NOT_COMPLETED','source_candidate_sha256':sha(x.candidate),'working_directory':'','planned_output_filename':c['required_outputs'][0]['filename'],'blocking_issues':[]})
 rows=c.get('allowed_change_matrix',[]);fields=['path_pattern','permission','allowed_fields','notes']
 with (r/'ALLOWED_CHANGE_MATRIX.csv').open('w',newline='') as f:w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)
 (r/'00_PASTE_THIS_PROMPT_FIRST.txt').write_text('Complete GATE0_RESPONSE.json. Verify exact source SHA. Freeze protected baseline. Repair the full declared failure-class population. Stop before external re-audit.\n');(r/'01_START_HERE.md').write_text('# v10 Bounded Repair Handoff\n\nRun `python tools/inspect_inputs.py .` and `python tools/validate_handoff_package.py .` first. Do not modify protected knowledge surfaces. Do not use known-good final artifacts. Before return run protected diff and exact return inventory.\n')
 dump(r/'PACKAGE_VALIDATION.json',{'status':'BUILDING'});entries=manifest(r);dump(r/'manifest.json',{'entries':entries});(r/'SHA256SUMS.txt').write_text(''.join(f"{q['sha256']}  {q['path']}\n" for q in entries));dump(r/'PACKAGE_VALIDATION.json',{'status':'PASS','source_sha256':sha(x.candidate),'failure_classes':len(c['failure_classes']),'tools_embedded':True,'protected_files':len(baseline)});entries=manifest(r);dump(r/'manifest.json',{'entries':entries});(r/'SHA256SUMS.txt').write_text(''.join(f"{q['sha256']}  {q['path']}\n" for q in entries));zipone(r,Path(x.output));print(json.dumps({'status':'PASS','output':x.output,'sha256':sha(x.output)},indent=2))
if __name__=='__main__':main()
