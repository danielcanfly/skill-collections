#!/usr/bin/env python3
from pathlib import Path
import os,subprocess,sys,json,tempfile
root=Path(__file__).resolve().parents[1];env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1','TZ':'UTC','LC_ALL':'C.UTF-8'};results=[]
def run(name,args):
 p=subprocess.run([str(x) for x in args],capture_output=True,text=True,env=env);ok=p.returncode==0;results.append({'test':name,'status':'PASS' if ok else 'FAIL','detail':((p.stdout or '')+(p.stderr or ''))[-1000:]});print(name,results[-1]['status']);return ok
ok=True
ok &= run('full_pipeline',[sys.executable,root/'tests/run_v9_full_pipeline_selftest.py'])
ok &= run('fault_injection',[sys.executable,root/'tests/run_v9_trust_chain_fault_injection.py'])
with tempfile.TemporaryDirectory() as td:
 out=Path(td)/'generated';out.mkdir()
 ok &= run('dispatcher_generate',[sys.executable,root/'modules/dispatcher/scripts/generate_child_packages.py',root/'modules/dispatcher/examples/domain_dispatch_config.example.json','--output-dir',out])
 ok &= run('dispatcher_validate',[sys.executable,root/'modules/dispatcher/scripts/validate_generated_collection.py',out,root/'modules/dispatcher/examples/domain_dispatch_config.example.json'])
compile_errors=[]
for p in root.rglob('*.py'):
 if '__pycache__' in p.parts:continue
 try:compile(p.read_text(encoding='utf-8'),str(p),'exec')
 except Exception as e:compile_errors.append(f'{p.relative_to(root)}: {e}')
results.append({'test':'python_compile','status':'PASS' if not compile_errors else 'FAIL','detail':'\n'.join(compile_errors[:20])});ok &= not compile_errors
report={'status':'PASS' if ok else 'FAIL','tests':len(results),'results':results};(root/'V9_SELFTEST_RESULT.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(json.dumps(report,ensure_ascii=False,indent=2));raise SystemExit(0 if ok else 1)
