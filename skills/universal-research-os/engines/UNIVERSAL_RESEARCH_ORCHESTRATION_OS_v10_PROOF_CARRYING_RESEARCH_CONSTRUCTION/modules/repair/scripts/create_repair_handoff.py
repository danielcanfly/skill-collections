#!/usr/bin/env python3
from pathlib import Path
import argparse,json,zipfile,hashlib,shutil,tempfile,subprocess,sys
from repair_common import *
ap=argparse.ArgumentParser();ap.add_argument('--candidate',required=True);ap.add_argument('--audit',required=True);ap.add_argument('--contract',required=True);ap.add_argument('--closure-matrix',required=True);ap.add_argument('--output',required=True);a=ap.parse_args();here=Path(__file__).resolve().parent
subprocess.run([sys.executable,str(here/'validate_repair_contract.py'),a.contract,'--candidate',a.candidate,'--closure-matrix',a.closure_matrix],check=True)
c=load(a.contract)
if sha(a.candidate)!=c['source_candidate_sha256']:raise SystemExit('source candidate SHA mismatch')
tmpbase=Path(tempfile.mkdtemp());root=tmpbase/c['repair_id'];root.mkdir();identity={'handoff_id':c['repair_id'],'handoff_type':'BOUNDED_REPAIR','status':'ACTIVE','orchestration_os_version':'7.0.0','audit_os_version':'3.0.0','contract_generation':'v7-repair-v4','expected_output_name':c['expected_output_name'],'source_candidate_sha256':c['source_candidate_sha256']};write(root/'HANDOFF_IDENTITY.json',identity);shutil.copy2(a.candidate,root/'SOURCE_CANDIDATE.zip');shutil.copytree(a.audit,root/'AUDIT_EVIDENCE');shutil.copy2(a.contract,root/'repair_contract.json');shutil.copy2(a.closure_matrix,root/'finding_closure_matrix.json');shutil.copytree(here,root/'scripts');shutil.copy2(Path(__file__).resolve().parents[2]/'child_runtime/handoff_scripts/initialize_contract_lineage.py',root/'scripts/initialize_contract_lineage.py')
# immutable baseline from source candidate and contract rules
td,sroot=extract(a.candidate);rows=[]
for pth,p in files(sroot).items():
 if rule_matches(pth,c.get('immutable_rules',[])):rows.append({'path':pth,'sha256':sha(p),'bytes':p.stat().st_size})
td.cleanup();write(root/'immutable_baseline.json',{'files':rows})
(root/'01_START_HERE.md').write_text('# v7 Repair Handoff\n\nRead repair_contract.json and finding_closure_matrix.json. Repair every row in each declared failure class, not only named examples. Run all class-wide closure validators. The parent auditor must run exact final acceptance with mandatory v7 admission and an external independent review directory.\n')
# Prove old candidate does not satisfy closure matrix; success here means the negative control is alive.
proc=subprocess.run([sys.executable,str(here/'validate_finding_closure.py'),'--candidate',a.candidate,'--matrix',a.closure_matrix,'--output',str(root/'OLD_CANDIDATE_NEGATIVE_CONTROL.json')],capture_output=True,text=True)
if proc.returncode==0:
 raise SystemExit('negative control invalid: source candidate already passes all declared closure commands')
# The declared failure population must also be executable on the source artifact.
pop=subprocess.run([sys.executable,str(here/'validate_class_wide_closure.py'),a.closure_matrix,'--candidate-root',a.candidate,'--output',str(root/'SOURCE_FAILURE_POPULATION.json')],capture_output=True,text=True)
if pop.returncode!=0:
 raise SystemExit('source failure population contract is not executable or does not match expected counts')
write(root/'PACKAGE_VALIDATION.json',{'status':'PASS','source_sha256':sha(a.candidate),'old_candidate_closure_exit_code':proc.returncode,'old_candidate_expected_to_fail':True,'source_population_validation_exit_code':pop.returncode,'immutable_files':len(rows)})
out=Path(a.output).resolve()
with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED) as z:
 for p in sorted(root.rglob('*')):
  if p.is_file():z.write(p,arcname=str(Path(root.name)/p.relative_to(root)))
with zipfile.ZipFile(out) as z:
 if z.testzip():raise SystemExit('ZIP CRC failure')
print(json.dumps({'status':'PASS','output':str(out),'sha256':sha(out),'immutable_files':len(rows)},indent=2))
