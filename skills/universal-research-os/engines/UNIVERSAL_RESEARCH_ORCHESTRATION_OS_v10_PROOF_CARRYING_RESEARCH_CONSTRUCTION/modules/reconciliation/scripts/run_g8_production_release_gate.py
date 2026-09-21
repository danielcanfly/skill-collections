#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path,PurePosixPath
import argparse,tempfile,zipfile,json,hashlib
DIMS={'compatibility','semantic','retrieval','seal','independent_semantic','production_assurance'}
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def load(p):
    try:return json.loads(Path(p).read_text(encoding='utf-8'))
    except:return {}
def extract(name,path,base):
    errors=[];path=Path(path).resolve();target=base/name;target.mkdir()
    try:
        with zipfile.ZipFile(path) as z:
            bad=z.testzip()
            if bad:errors.append(f'{name}: ZIP CRC failure {bad}')
            roots={Path(n).parts[0] for n in z.namelist() if n and not n.startswith('__MACOSX/')}
            if len(roots)!=1:errors.append(f'{name}: ZIP must have one root')
            z.extractall(target)
        root=target/next(iter(roots)) if len(roots)==1 else target
    except Exception as e:errors.append(f'{name}: {e}');root=target
    return root,errors
def strict_manifest(root):
    errors=[];ms=list(root.glob('manifest.json'))
    if len(ms)!=1:return [f'exactly one root manifest.json required, found {len(ms)}']
    m=load(ms[0]);entries=m.get('entries',[]) if isinstance(m,dict) else []
    expected={e.get('path') for e in entries};actual={p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file() and p.relative_to(root).as_posix() not in {'manifest.json','SHA256SUMS.txt'}}
    if None in expected or expected!=actual:errors.append(f'strict manifest coverage mismatch missing={sorted(expected-actual)[:10]} extra={sorted(actual-expected)[:10]}')
    for e in entries:
        p=root/e.get('path','')
        if not p.is_file() or sha(p)!=e.get('sha256'):errors.append('manifest mismatch '+str(e.get('path')))
    return errors
def canonical_identity(root,name):
    p=root/'RELEASE_IDENTITY.json'
    extras=[x for x in root.rglob('RELEASE_IDENTITY.json') if x!=p]
    if not p.is_file():return {},[f'{name}: root RELEASE_IDENTITY.json missing']
    if extras:return {},[f'{name}: multiple RELEASE_IDENTITY.json files forbidden: {[x.relative_to(root).as_posix() for x in extras]}']
    j=load(p);errs=[]
    if not j.get('release_id'):errs.append(f'{name}: release_id missing')
    if j.get('release_contract')!='v10':errs.append(f'{name}: release_contract must be v10')
    if j.get('orchestration_os_version')!='10.0.0':errs.append(f'{name}: orchestration_os_version must be 10.0.0')
    return j,errs
def exact_audit_summary(root):
    xs=list(root.rglob('AUDIT_SUMMARY.json'))
    if len(xs)!=1:return {},None,[f'audit: exactly one AUDIT_SUMMARY.json required, found {len(xs)}']
    j=load(xs[0]);errors=[];dims=j.get('dimension_scores',{})
    if j.get('status') not in {'MERGE_READY','GLOBAL_MERGE_READY'}:errors.append('audit status is not merge-ready')
    if j.get('audit_os_version')!='6.0.0':errors.append('audit_os_version must be 6.0.0')
    if j.get('orchestration_contract')!='v10':errors.append('orchestration_contract must be v10')
    if int(j.get('score',0))!=100:errors.append('audit score must be 100')
    if set(dims)!=DIMS or any(int(dims.get(k,0))!=100 for k in DIMS):errors.append('audit must contain exactly six 100-point dimensions including production_assurance')
    if j.get('findings') or any(int(j.get(k,0) or 0) for k in ['open_p0','open_p1','open_p2']):errors.append('audit contains findings or open P0/P1/P2')
    return j,xs[0],errors
def main():
    ap=argparse.ArgumentParser()
    for x in ['combined','kos','okf','r2','audit']:ap.add_argument(f'--{x}',required=True)
    ap.add_argument('--output',required=True);a=ap.parse_args();errors=[];records={}
    with tempfile.TemporaryDirectory() as td0:
        td=Path(td0);roots={};identities={}
        for name in ['combined','kos','okf','r2','audit']:
            path=Path(getattr(a,name)).resolve();root,es=extract(name,path,td);errors+=es;roots[name]=root
            errors += [f'{name}: {e}' for e in strict_manifest(root)]
            ident,ies=canonical_identity(root,name);errors+=ies;identities[name]=ident
            records[name]={'filename':path.name,'sha256':sha(path),'release_id':ident.get('release_id'),'release_contract':ident.get('release_contract')}
        ids={j.get('release_id') for j in identities.values() if j.get('release_id')}
        if len(ids)!=1 or any(not j.get('release_id') for j in identities.values()):errors.append(f'exact release identity mismatch across five surfaces: {records}')
        # Reject any extra identity-like metadata that conflicts with canonical identity.
        for name,root in roots.items():
            rid=identities[name].get('release_id')
            for p in root.rglob('*.json'):
                if p==root/'RELEASE_IDENTITY.json':continue
                j=load(p)
                if not isinstance(j,dict):continue
                other=j.get('release_id') or j.get('global_release_id')
                if other and other!=rid:errors.append(f'{name}: conflicting release identity in {p.relative_to(root)}: {other}')
                if j.get('orchestration_contract') and j.get('orchestration_contract')!='v10':errors.append(f'{name}: contract downgrade in {p.relative_to(root)}')
        bad=[]
        for p in roots['r2'].rglob('*'):
            if not p.is_file():continue
            rel=p.relative_to(roots['r2']).as_posix();low=rel.lower();parts={x.lower() for x in PurePosixPath(rel).parts}
            if parts & {'tests','test','fixtures','fixture','__pycache__','qa','audit','.pytest_cache'} or p.suffix.lower() in {'.pyc','.pyo','.tmp'} or any(x in low for x in ['synthetic_bad_candidate','badslug','test_output','provisional','__macosx','.ds_store']):bad.append(rel)
        if bad:errors.append(f'r2 production pollution: {bad[:20]}')
        manifests=list(roots['combined'].rglob('production_surface_manifest.json'))
        if len(manifests)!=1:errors.append(f'combined release requires exactly one production_surface_manifest.json, found {len(manifests)}')
        else:
            ps=load(manifests[0])
            if ps.get('release_contract')!='v10' or ps.get('release_stage')!='global_production_release':errors.append('combined production surface manifest is not v10 global production release')
        summary,sp,aerrors=exact_audit_summary(roots['audit']);errors+=aerrors
        # Pointer is a candidate only. Promotion remains separately authorised.
        for p in roots['combined'].rglob('*.json'):
            j=load(p)
            if isinstance(j,dict) and (j.get('live_pointer_updated') is True or j.get('pointer_state') in {'PROMOTED','LIVE'}):errors.append(f'live pointer changed during release build: {p.relative_to(roots["combined"])}')
    receipt={'status':'PASS' if not errors else 'FAIL','gate':'G8_PROOF_CARRYING_RELEASE_V10','release_id':next(iter(ids)) if len(ids)==1 else None,'orchestration_os_version':'10.0.0','required_audit_os_version':'6.0.0','required_dimensions':sorted(DIMS),'surfaces':records,'audit_summary_file':sp.name if sp else None,'errors':errors,'open_p0':0 if not errors else 1,'open_p1':0 if not errors else 1,'open_p2':0 if not errors else 1,'live_pointer_updated':False}
    Path(a.output).write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n');print(json.dumps(receipt,ensure_ascii=False,indent=2));raise SystemExit(0 if not errors else 1)
if __name__=='__main__':main()
