#!/usr/bin/env python3
from pathlib import Path,PurePosixPath
import argparse,json,csv,re
from common import result,emit,load_json

ap=argparse.ArgumentParser(); ap.add_argument('root'); ap.add_argument('--config'); ap.add_argument('--profile'); ap.add_argument('--output'); a=ap.parse_args()
root=Path(a.root); profile=load_json(a.profile,{}) if a.profile else {}; errors=[]; warnings=[]
manifest=load_json(root/'release/production_surface_manifest.json',{}) or load_json(root/'qa/production_surface_manifest.json',{})
require_manifest=profile.get('require_production_surface_manifest',True)
if require_manifest and not manifest: errors.append('production surface manifest is required')
surfaces=manifest.get('surfaces',[]) if isinstance(manifest,dict) else []
if not surfaces and manifest.get('surface_roots'):
    surfaces=[{'surface_id':f'surface-{i+1}','kind':'knowledge','root':x} for i,x in enumerate(manifest.get('surface_roots',[]))]
forbidden_components={'__pycache__','.pytest_cache','__macosx','.git','.svn','node_modules','tmp','temp','fixtures','fixture'}
forbidden_suffixes={'.pyc','.pyo','.tmp','.swp','.bak'}
forbidden_tokens={'synthetic_bad_candidate','badslug','test_output','provisional','.ds_store'}
count=0
for s in surfaces:
    sid=s.get('surface_id','?'); kind=(s.get('kind') or '').lower(); rel=s.get('root','')
    p=root/rel
    if not p.exists(): errors.append(f'{sid}: production surface root missing: {rel}'); continue
    for f in p.rglob('*'):
        if not f.is_file(): continue
        count+=1; rp=f.relative_to(p).as_posix(); low=rp.lower(); parts={x.lower() for x in PurePosixPath(rp).parts}
        if parts & forbidden_components or f.suffix.lower() in forbidden_suffixes or any(t in low for t in forbidden_tokens): errors.append(f'{sid}: forbidden production artifact {rp}')
        if kind=='r2' and ('test' in parts or 'tests' in parts or 'audit' in parts or 'qa' in parts): errors.append(f'{sid}: audit/test/qa artifact cannot enter R2 payload: {rp}')

# Inspect object plans independently of the on-disk surface.
plan_paths=[]
for candidate in [manifest.get('r2_object_plan') if manifest else None,'r2/object_plan.json','r2/object_plan.csv','release/r2_object_plan.json','release/r2_object_plan.csv']:
    if candidate and candidate not in plan_paths and (root/candidate).is_file(): plan_paths.append(candidate)
keys=[]
for rel in plan_paths:
    p=root/rel
    if p.suffix=='.json':
        data=load_json(p,[]); rows0=data.get('objects',data.get('entries',[])) if isinstance(data,dict) else data
    else:
        with p.open(encoding='utf-8-sig',newline='') as f: rows0=list(csv.DictReader(f))
    for r in rows0 or []:
        if not isinstance(r,dict): continue
        key=str(r.get('object_key') or r.get('key') or r.get('path') or r.get('source_path') or '')
        if not key: errors.append(f'{rel}: object row missing key/path'); continue
        keys.append(key); pp=PurePosixPath(key); low=key.lower(); parts={x.lower() for x in pp.parts}
        if pp.is_absolute() or '..' in pp.parts: errors.append(f'{rel}: unsafe object key {key}')
        if parts & forbidden_components or any(t in low for t in forbidden_tokens) or pp.suffix.lower() in forbidden_suffixes: errors.append(f'{rel}: polluted object key {key}')
        if 'test' in parts or 'tests' in parts or 'audit' in parts or 'qa' in parts: errors.append(f'{rel}: non-production object key {key}')
if len(keys)!=len(set(keys)): errors.append('duplicate R2 object keys detected')
if profile.get('require_r2_object_plan',False) and not plan_paths: errors.append('R2 object plan required for final production release')
emit(result('PASS' if not errors else 'FAIL',errors,warnings,{'surfaces':len(surfaces),'surface_files':count,'r2_plan_files':len(plan_paths),'r2_objects':len(keys)}),a.output)
