#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
import tempfile,zipfile,json,hashlib,subprocess,sys,shutil,os
ROOT=Path(__file__).resolve().parents[1]
AUDIT=ROOT/'modules/audit_os_v6_proof_carrying_construction/scripts'
PROMOTE=ROOT/'modules/production_release/scripts/promote_audited_candidate.py'
VALIDATE=ROOT/'modules/production_release/scripts/validate_child_production_release.py'
G8=ROOT/'modules/reconciliation/scripts/run_g8_production_release_gate.py'
FIX=ROOT/'tests/fixtures'
DIMS={'compatibility','semantic','retrieval','seal','independent_semantic','production_assurance'}
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def run(args,expect):
 p=subprocess.run([str(x) for x in args],capture_output=True,text=True,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1','TZ':'UTC','LC_ALL':'C.UTF-8'});return p,p.returncode==expect
def rec(rows,name,ok,detail=''):
 rows.append({'test':name,'status':'PASS' if ok else 'FAIL','detail':detail[-500:]});print(name,rows[-1]['status'])
 if not ok:raise AssertionError(name+': '+detail)
def make_zip(root,out):
 with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
  for p in sorted(x for x in root.rglob('*') if x.is_file()):z.write(p,(Path(root.name)/p.relative_to(root)).as_posix())
def manifest(root):
 es=[]
 for p in sorted(x for x in root.rglob('*') if x.is_file() and x.relative_to(root).as_posix() not in {'manifest.json','SHA256SUMS.txt'}):es.append({'path':p.relative_to(root).as_posix(),'sha256':sha(p),'bytes':p.stat().st_size})
 (root/'manifest.json').write_text(json.dumps({'entries':es},indent=2)+'\n')
 (root/'SHA256SUMS.txt').write_text(''.join(f"{e['sha256']}  {e['path']}\n" for e in es))
def g8_surfaces(base,prefix='clean',extra=False,downgrade=False,conflict=False):
 zips={}
 for name in ['combined','kos','okf','r2','audit']:
  r=base/f'{prefix}-{name}-root';r.mkdir();(r/'RELEASE_IDENTITY.json').write_text(json.dumps({'release_id':'RID-V9','release_contract':'v9','orchestration_os_version':'10.0.0'}))
  if name=='combined':
   (r/'release').mkdir();(r/'release/production_surface_manifest.json').write_text(json.dumps({'version':'2.0','release_stage':'global_production_release','release_contract':'v9','surfaces':[{'surface_id':'release','kind':'release','root':'.'}]}))
  elif name=='r2':(r/'knowledge').mkdir();(r/'knowledge/node.md').write_text('# node\n')
  elif name=='audit':
   if downgrade:s={'status':'GLOBAL_MERGE_READY','audit_os_version':'3.0.0','orchestration_contract':'v7','score':100,'dimension_scores':{'compatibility':100,'semantic':100,'retrieval':100,'seal':100,'independent_semantic':100},'findings':[]}
   else:s={'status':'GLOBAL_MERGE_READY','audit_os_version':'6.0.0','orchestration_contract':'v10','score':100,'dimension_scores':{k:100 for k in DIMS},'findings':[],'open_p0':0,'open_p1':0,'open_p2':0}
   (r/'AUDIT_SUMMARY.json').write_text(json.dumps(s))
  else:(r/'payload.txt').write_text(name+'\n')
  if conflict and name=='kos':(r/'OTHER.json').write_text(json.dumps({'release_id':'DIFFERENT'}))
  manifest(r)
  if extra and name=='kos':(r/'rogue.txt').write_text('not manifested')
  zp=base/f'{prefix}-{name}.zip';make_zip(r,zp);zips[name]=zp
 return zips
def run_g8(zips,out):
 args=[sys.executable,G8]
 for n in ['combined','kos','okf','r2','audit']:args += [f'--{n}',zips[n]]
 args += ['--output',out];return run(args,0)
def main():
 rows=[]
 with tempfile.TemporaryDirectory() as td0:
  td=Path(td0)
  # No-op reproduction must fail after outputs are deleted.
  c=td/'noop';(c/'qa').mkdir(parents=True);(c/'qa/out.json').write_text('{}');(c/'qa/noop.py').write_text('# no output\n');(c/'qa/reproduction_contract.json').write_text(json.dumps({'root_resolution':'script-relative','commands':[{'id':'retrieval','cwd':'.','argv':['{python}','qa/noop.py'],'outputs':['qa/out.json']}]}));prof=td/'profile.json';prof.write_text(json.dumps({'required_reproduction_commands':['retrieval'],'reproduction_timeout_seconds':20}))
  p,ok=run([sys.executable,AUDIT/'validate_portable_reproducibility.py',c,'--profile',prof],1);rec(rows,'reject_noop_reproduction',ok,p.stdout+p.stderr)
  # Exact promotion and deterministic replay.
  release=td/'DEMO_PRODUCTION_RELEASE_v1.zip';args=[sys.executable,PROMOTE,FIX/'V9_GOOD_CANDIDATE.zip',FIX/'V9_GOOD_AUDIT_OUTPUT.zip','--admission-receipt',FIX/'V9_GOOD_ADMISSION.json','--output',release,'--promoted-at','2026-07-16T14:01:00Z']
  p,ok=run(args,0);rec(rows,'promote_strict_audit_package',ok,p.stdout+p.stderr);h=sha(release)
  release.unlink();p,ok=run(args,0);rec(rows,'deterministic_production_promotion',ok and sha(release)==h,p.stdout+p.stderr)
  p,ok=run([sys.executable,VALIDATE,release],0);rec(rows,'reverify_embedded_audit_chain',ok,p.stdout+p.stderr)
  # Loose audit summary without manifest cannot be promoted.
  loose=td/'loose';loose.mkdir();shutil.copy(FIX/'V9_GOOD_AUDIT_OUTPUT/AUDIT_SUMMARY.json',loose/'AUDIT_SUMMARY.json')
  p,ok=run([sys.executable,PROMOTE,FIX/'V9_GOOD_CANDIDATE.zip',loose,'--admission-receipt',FIX/'V9_GOOD_ADMISSION.json','--output',td/'bad.zip'],1);rec(rows,'reject_loose_audit_summary',ok,p.stdout+p.stderr)
  # Tamper the embedded audit, rebuild both manifests, and require rejection.
  x=td/'tamper';x.mkdir();
  with zipfile.ZipFile(release) as z:z.extractall(x)
  rr=next(x.iterdir());sp=next(rr.rglob('AUDIT_SUMMARY.json'));j=json.loads(sp.read_text());j.update({'status':'FAIL','audit_os_version':'0.0.0','score':0,'dimension_scores':{},'findings':[{'severity':'P0'}]});sp.write_text(json.dumps(j))
  manifest(rr/'independent_audit');manifest(rr);tam=td/'tampered.zip';make_zip(rr,tam)
  p,ok=run([sys.executable,VALIDATE,tam],1);rec(rows,'reject_tampered_embedded_audit',ok,p.stdout+p.stderr)
  # G8 positive and negative gates.
  z=g8_surfaces(td,'clean');args=[sys.executable,G8]
  for n in ['combined','kos','okf','r2','audit']:args += [f'--{n}',z[n]]
  args += ['--output',td/'g8-clean.json'];p,ok=run(args,0);rec(rows,'g8_accept_exact_v9_surfaces',ok,p.stdout+p.stderr)
  for label,kwargs in [('unmanifested_extra',{'extra':True}),('audit_downgrade',{'downgrade':True}),('conflicting_identity',{'conflict':True})]:
   z=g8_surfaces(td,label,**kwargs);args=[sys.executable,G8]
   for n in ['combined','kos','okf','r2','audit']:args += [f'--{n}',z[n]]
   args += ['--output',td/f'g8-{label}.json'];p,ok=run(args,1);rec(rows,'g8_reject_'+label,ok,p.stdout+p.stderr)
 report={'status':'PASS','tests':len(rows),'results':rows};(ROOT/'V9_FAULT_INJECTION_RESULT.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(json.dumps(report,indent=2))
if __name__=='__main__':main()
