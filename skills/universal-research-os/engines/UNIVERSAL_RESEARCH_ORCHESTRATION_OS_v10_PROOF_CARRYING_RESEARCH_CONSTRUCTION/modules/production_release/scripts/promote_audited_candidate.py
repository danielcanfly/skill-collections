#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
import argparse, hashlib, json, shutil, tempfile, zipfile

EPOCH=(1980,1,1,0,0,0)
DIMS={'compatibility','semantic','retrieval','seal','independent_semantic','production_assurance'}
REVIEW_FILES=['INDEPENDENT_EDGE_REVIEW.csv','INDEPENDENT_SOURCE_REVIEW.csv','INDEPENDENT_LOCATOR_REVIEW.csv','INDEPENDENT_TOPIC_RISK_REVIEW.csv']

def sha(p:Path)->str: return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p:Path,default=None):
    try:return json.loads(p.read_text(encoding='utf-8'))
    except:return default

def extract_single(zpath:Path,base:Path)->Path:
    with zipfile.ZipFile(zpath) as z:
        bad=z.testzip()
        if bad: raise SystemExit(f'ZIP CRC failure: {bad}')
        names=[n for n in z.namelist() if n and not n.startswith('__MACOSX/')]
        roots={Path(n).parts[0] for n in names}
        if len(roots)!=1: raise SystemExit(f'ZIP must contain exactly one root: {sorted(roots)}')
        z.extractall(base)
    return base/next(iter(roots))

def materialize_package(src:Path,base:Path)->Path:
    if src.is_dir():
        dst=base/src.name; shutil.copytree(src,dst); return dst
    if zipfile.is_zipfile(src): return extract_single(src,base)
    raise SystemExit('audit input must be a strict manifest-governed directory or ZIP')

def strict_manifest(root:Path):
    ms=list(root.glob('manifest.json'))
    if len(ms)!=1: raise SystemExit(f'audit package requires exactly one root manifest.json, found {len(ms)}')
    m=load(ms[0],{}); entries=m.get('entries',[]) if isinstance(m,dict) else []
    expected={e.get('path') for e in entries}; actual={p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file() and p.relative_to(root).as_posix() not in {'manifest.json','SHA256SUMS.txt'}}
    if None in expected or actual!=expected:
        raise SystemExit(f'audit package strict manifest coverage mismatch: missing={sorted(expected-actual)[:10]} extra={sorted(actual-expected)[:10]}')
    for e in entries:
        p=root/e['path']
        if not p.is_file() or sha(p)!=e.get('sha256'): raise SystemExit('audit package manifest hash mismatch: '+str(e.get('path')))

def exactly_one(root:Path,name:str)->Path:
    xs=list(root.rglob(name))
    if len(xs)!=1: raise SystemExit(f'expected exactly one {name}, found {len(xs)}')
    return xs[0]

def validate_audit_package(root:Path,csha:str,external_admission:Path):
    strict_manifest(root)
    summary_path=exactly_one(root,'AUDIT_SUMMARY.json'); identity_path=exactly_one(root,'AUDIT_PACKAGE_IDENTITY.json')
    summary=load(summary_path,{}); identity=load(identity_path,{})
    dims=summary.get('dimension_scores',{})
    if summary.get('status')!='MERGE_READY' or summary.get('audit_os_version')!='6.0.0' or summary.get('orchestration_contract')!='v10': raise SystemExit('Audit OS v6 exact identity required')
    if summary.get('candidate_sha256')!=csha or int(summary.get('score',0))!=100: raise SystemExit('audit summary does not bind exact 100/100 candidate')
    if set(dims)!=DIMS or any(int(dims[k])!=100 for k in DIMS): raise SystemExit('exact six 100-point audit dimensions required')
    if summary.get('findings') or any(int(summary.get(k,0) or 0) for k in ['open_p0','open_p1','open_p2']): raise SystemExit('audit has findings or open P0/P1/P2')
    adm=exactly_one(root,'admission_receipt.json'); ind=exactly_one(root,'INDEPENDENT_SEMANTIC_REVIEW_RECEIPT.json')
    embedded_adm=load(adm,{}); independent=load(ind,{})
    if sha(adm)!=sha(external_admission): raise SystemExit('external admission differs from audit-embedded admission')
    if embedded_adm.get('status')!='PASS' or embedded_adm.get('classification')!='V10_NATIVE_ACCEPTED' or embedded_adm.get('candidate_sha256')!=csha: raise SystemExit('embedded admission is not exact v10-native candidate admission')
    if independent.get('status')!='PASS' or independent.get('audit_os_version')!='6.0.0' or independent.get('candidate_sha256')!=csha: raise SystemExit('independent review receipt is invalid or unbound')
    if independent.get('auditor_role')!='INDEPENDENT' or independent.get('independence_attestation') is not True: raise SystemExit('independent review attestation missing')
    if any(int(independent.get(k,999) or 0) for k in ['open_p0','open_p1','open_p2']): raise SystemExit('independent review has open findings')
    review_dir=ind.parent
    for fn in REVIEW_FILES:
        fp=review_dir/fn
        if not fp.is_file() or independent.get('artifacts',{}).get(fn)!=sha(fp): raise SystemExit('independent review artifact hash mismatch: '+fn)
    if identity.get('package_type')!='INDEPENDENT_AUDIT_OUTPUT' or identity.get('audit_os_version')!='6.0.0' or identity.get('orchestration_contract')!='v10': raise SystemExit('audit package identity invalid')
    checks={
      'candidate_sha256':csha,
      'audit_summary_sha256':sha(summary_path),
      'admission_receipt_sha256':sha(adm),
      'independent_review_receipt_sha256':sha(ind),
    }
    for k,v in checks.items():
        if identity.get(k)!=v: raise SystemExit(f'audit package identity {k} mismatch')
    return summary_path,summary,adm,ind,identity_path

def write_integrity(root:Path):
    entries=[]
    for p in sorted(x for x in root.rglob('*') if x.is_file() and x.relative_to(root).as_posix() not in {'manifest.json','SHA256SUMS.txt'}):
        entries.append({'path':p.relative_to(root).as_posix(),'sha256':sha(p),'bytes':p.stat().st_size})
    (root/'manifest.json').write_text(json.dumps({'manifest_version':'1.0','package_type':'AUDITED_PRODUCTION_RELEASE','entries':entries},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    (root/'SHA256SUMS.txt').write_text(''.join(f"{x['sha256']}  {x['path']}\n" for x in entries),encoding='utf-8')

def make_zip(root:Path,out:Path):
    out.parent.mkdir(parents=True,exist_ok=True)
    if out.exists():out.unlink()
    with zipfile.ZipFile(out,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for p in sorted(x for x in root.rglob('*') if x.is_file()):
            info=zipfile.ZipInfo((Path(root.name)/p.relative_to(root)).as_posix(),EPOCH);info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o100644<<16
            z.writestr(info,p.read_bytes())
    with zipfile.ZipFile(out) as z:
        if z.testzip():raise SystemExit('output ZIP CRC failure')

def verify_integrity(root:Path):
    m=load(root/'manifest.json',{});entries=m.get('entries',[]);expected={e.get('path') for e in entries};actual={p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file() and p.relative_to(root).as_posix() not in {'manifest.json','SHA256SUMS.txt'}}
    if expected!=actual:raise SystemExit('fresh-extraction strict manifest coverage mismatch')
    for e in entries:
        p=root/e['path']
        if not p.is_file() or sha(p)!=e.get('sha256'):raise SystemExit('fresh-extraction integrity mismatch: '+e.get('path','?'))

def main():
    ap=argparse.ArgumentParser();ap.add_argument('candidate_zip');ap.add_argument('audit');ap.add_argument('--admission-receipt',required=True);ap.add_argument('--output',required=True);ap.add_argument('--promoted-at');a=ap.parse_args()
    cand=Path(a.candidate_zip).resolve(); audit=Path(a.audit).resolve(); adm_path=Path(a.admission_receipt).resolve(); out=Path(a.output).resolve(); csha=sha(cand)
    adm=load(adm_path,{})
    if adm.get('status')!='PASS' or adm.get('classification')!='V10_NATIVE_ACCEPTED' or adm.get('candidate_sha256')!=csha:raise SystemExit('v10 admission receipt does not bind the exact candidate')
    with tempfile.TemporaryDirectory() as td0:
        td=Path(td0); candidate_root=extract_single(cand,td/'candidate_extract'); audit_root=materialize_package(audit,td/'audit_extract')
        summary_path,summary,embedded_adm,ind,identity_path=validate_audit_package(audit_root,csha,adm_path)
        seal=load(candidate_root/'qa/seal_state.json',{})
        if seal.get('state')!='SEALED' or int(seal.get('post_manifest_mutations',1))!=0:raise SystemExit('candidate is not sealed')
        cfg=load(candidate_root/'audit_config.json',{}); expected=cfg.get('production_release_output_name') or cand.name.replace('PRODUCTION_CANDIDATE','PRODUCTION_RELEASE')
        if out.name!=expected:raise SystemExit(f'production release filename mismatch: expected {expected}')
        release_root=td/out.stem; (release_root/'payload').mkdir(parents=True); shutil.copy2(cand,release_root/'payload'/cand.name); shutil.copytree(audit_root,release_root/'independent_audit'); shutil.copy2(adm_path,release_root/'admission_receipt.json')
        now=a.promoted_at or summary.get('completed_at') or adm.get('admitted_at') or adm.get('observed_at') or cfg.get('reproducible_generated_at')
        if not now: raise SystemExit('deterministic promoted_at is required')
        dims=summary['dimension_scores']
        receipt={'status':'AUDITED_PRODUCTION_RELEASE','release_contract':'v10','orchestration_os_version':'10.0.0','audit_os_version':'6.0.0','candidate_filename':cand.name,'candidate_sha256':csha,'audit_package_manifest_sha256':sha(audit_root/'manifest.json'),'audit_package_identity_sha256':sha(identity_path),'audit_summary_sha256':sha(summary_path),'admission_receipt_sha256':sha(adm_path),'independent_review_receipt_sha256':sha(ind),'dimension_scores':dims,'open_p0':0,'open_p1':0,'open_p2':0,'promoted_at':now,'live_pointer_updated':False}
        (release_root/'PRODUCTION_RELEASE_RECEIPT.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n')
        (release_root/'RELEASE_IDENTITY.json').write_text(json.dumps({'release_id':out.stem,'lifecycle_state':'AUDITED_PRODUCTION_RELEASE','release_contract':'v10','orchestration_os_version':'10.0.0','audit_os_version':'6.0.0','payload_candidate_sha256':csha,'canonical_payload_path':f'payload/{cand.name}','audit_path':'independent_audit','live_pointer_state':'UNCHANGED'},ensure_ascii=False,indent=2)+'\n')
        (release_root/'release').mkdir(); (release_root/'release/production_surface_manifest.json').write_text(json.dumps({'version':'2.0','release_stage':'child_production_release','release_contract':'v10','surfaces':[{'surface_id':'payload','kind':'nested-audited-candidate','root':'payload'}],'r2_object_plan':None,'audit_only_roots':['independent_audit']},indent=2)+'\n')
        write_integrity(release_root); make_zip(release_root,out); fresh=extract_single(out,td/'fresh'); verify_integrity(fresh)
    print(json.dumps({'status':'PASS','production_release':str(out),'sha256':sha(out),'candidate_sha256':csha,'lifecycle_state':'AUDITED_PRODUCTION_RELEASE','release_contract':'v10'},indent=2))
if __name__=='__main__':main()
