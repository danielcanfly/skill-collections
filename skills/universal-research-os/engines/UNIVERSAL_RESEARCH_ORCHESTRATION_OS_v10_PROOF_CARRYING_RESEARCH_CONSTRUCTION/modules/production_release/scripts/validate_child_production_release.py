#!/usr/bin/env python3
from pathlib import Path
import argparse,tempfile,zipfile,json,hashlib

DIMS={'compatibility','semantic','retrieval','seal','independent_semantic','production_assurance'}
REVIEW_FILES=['INDEPENDENT_EDGE_REVIEW.csv','INDEPENDENT_SOURCE_REVIEW.csv','INDEPENDENT_LOCATOR_REVIEW.csv','INDEPENDENT_TOPIC_RISK_REVIEW.csv']
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def load(p):
    try:return json.loads(Path(p).read_text(encoding='utf-8'))
    except:return {}
def actual_files(root):return {p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file() and p.relative_to(root).as_posix() not in {'manifest.json','SHA256SUMS.txt'}}
def strict_manifest(root,label,errors):
    ms=list(root.glob('manifest.json'))
    if len(ms)!=1: errors.append(f'{label}: exactly one root manifest.json required, found {len(ms)}');return
    m=load(ms[0]);entries=m.get('entries',[]) if isinstance(m,dict) else [];expected={e.get('path') for e in entries};actual=actual_files(root)
    if None in expected or expected!=actual:errors.append(f'{label}: strict manifest coverage mismatch missing={sorted(expected-actual)[:10]} extra={sorted(actual-expected)[:10]}')
    for e in entries:
        p=root/e.get('path','')
        if not p.is_file() or sha(p)!=e.get('sha256'):errors.append(f"{label}: manifest hash mismatch {e.get('path')}")
def exactly_one(root,name,label,errors):
    xs=list(root.rglob(name))
    if len(xs)!=1: errors.append(f'{label}: expected exactly one {name}, found {len(xs)}');return None
    return xs[0]
def extract_single(zpath,base,label,errors):
    try:
        with zipfile.ZipFile(zpath) as z:
            bad=z.testzip()
            if bad:errors.append(f'{label}: ZIP CRC failure {bad}')
            roots={Path(n).parts[0] for n in z.namelist() if n and not n.startswith('__MACOSX/')}
            if len(roots)!=1:errors.append(f'{label}: ZIP must have exactly one root')
            z.extractall(base)
        return base/next(iter(roots)) if len(roots)==1 else base
    except Exception as e:errors.append(f'{label}: {e}');return base

def main():
    ap=argparse.ArgumentParser();ap.add_argument('release_zip');ap.add_argument('--output');a=ap.parse_args();zpath=Path(a.release_zip).resolve();errors=[];stats={}
    with tempfile.TemporaryDirectory() as td0:
        td=Path(td0);root=extract_single(zpath,td/'release','release',errors)
        strict_manifest(root,'release',errors)
        rec=load(root/'PRODUCTION_RELEASE_RECEIPT.json');ident=load(root/'RELEASE_IDENTITY.json');payload=list((root/'payload').glob('*.zip')) if (root/'payload').is_dir() else []
        if rec.get('status')!='AUDITED_PRODUCTION_RELEASE' or rec.get('release_contract')!='v10':errors.append('invalid v10 production release receipt')
        if rec.get('orchestration_os_version')!='10.0.0' or rec.get('audit_os_version')!='6.0.0':errors.append('release version identity mismatch')
        dims=rec.get('dimension_scores',{})
        if set(dims)!=DIMS or any(int(dims.get(k,0))!=100 for k in DIMS):errors.append('production receipt must contain exactly six 100-point dimensions')
        if any(int(rec.get(k,999) or 0) for k in ['open_p0','open_p1','open_p2']):errors.append('open findings present')
        if len(payload)!=1:errors.append('exactly one candidate payload ZIP is required');csha=None
        else:
            csha=sha(payload[0])
            if csha!=rec.get('candidate_sha256'):errors.append('payload candidate SHA mismatch')
            croot=extract_single(payload[0],td/'candidate','candidate',errors);seal=load(croot/'qa/seal_state.json')
            if seal.get('state')!='SEALED' or int(seal.get('post_manifest_mutations',1))!=0:errors.append('payload candidate is not sealed')
        if ident.get('lifecycle_state')!='AUDITED_PRODUCTION_RELEASE' or ident.get('release_contract')!='v10':errors.append('release identity lifecycle/contract mismatch')
        if ident.get('orchestration_os_version')!='10.0.0' or ident.get('audit_os_version')!='6.0.0':errors.append('release identity version mismatch')
        if csha and ident.get('payload_candidate_sha256')!=csha:errors.append('release identity payload SHA mismatch')
        ext_adm=root/'admission_receipt.json';audit_root=root/'independent_audit'
        if not ext_adm.is_file():errors.append('wrapper admission receipt missing')
        if not audit_root.is_dir():errors.append('embedded independent_audit missing')
        else:
            strict_manifest(audit_root,'embedded audit',errors)
            sp=exactly_one(audit_root,'AUDIT_SUMMARY.json','embedded audit',errors);ip=exactly_one(audit_root,'AUDIT_PACKAGE_IDENTITY.json','embedded audit',errors);apath=exactly_one(audit_root,'admission_receipt.json','embedded audit',errors);rp=exactly_one(audit_root,'INDEPENDENT_SEMANTIC_REVIEW_RECEIPT.json','embedded audit',errors)
            summary=load(sp) if sp else {};aid=load(ip) if ip else {};adm=load(apath) if apath else {};irev=load(rp) if rp else {}
            sd=summary.get('dimension_scores',{})
            if summary.get('status')!='MERGE_READY' or summary.get('audit_os_version')!='6.0.0' or summary.get('orchestration_contract')!='v10':errors.append('embedded audit summary identity/status invalid')
            if csha and summary.get('candidate_sha256')!=csha:errors.append('embedded audit summary candidate binding mismatch')
            if int(summary.get('score',0))!=100 or set(sd)!=DIMS or any(int(sd.get(k,0))!=100 for k in DIMS):errors.append('embedded audit must be exact six-dimension 100/100')
            if summary.get('findings') or any(int(summary.get(k,0) or 0) for k in ['open_p0','open_p1','open_p2']):errors.append('embedded audit contains findings/open severities')
            if aid.get('package_type')!='INDEPENDENT_AUDIT_OUTPUT' or aid.get('audit_os_version')!='6.0.0' or aid.get('orchestration_contract')!='v10':errors.append('embedded audit package identity invalid')
            if csha and aid.get('candidate_sha256')!=csha:errors.append('embedded audit identity candidate binding mismatch')
            if sp and aid.get('audit_summary_sha256')!=sha(sp):errors.append('embedded audit identity summary SHA mismatch')
            if apath and aid.get('admission_receipt_sha256')!=sha(apath):errors.append('embedded audit identity admission SHA mismatch')
            if rp and aid.get('independent_review_receipt_sha256')!=sha(rp):errors.append('embedded audit identity review SHA mismatch')
            if ext_adm.is_file() and apath and sha(ext_adm)!=sha(apath):errors.append('wrapper and embedded admission receipts differ')
            if adm.get('status')!='PASS' or adm.get('classification')!='V10_NATIVE_ACCEPTED' or (csha and adm.get('candidate_sha256')!=csha):errors.append('embedded v10 admission invalid')
            if irev.get('status')!='PASS' or irev.get('audit_os_version')!='6.0.0' or (csha and irev.get('candidate_sha256')!=csha):errors.append('embedded independent review invalid')
            if irev.get('auditor_role')!='INDEPENDENT' or irev.get('independence_attestation') is not True:errors.append('embedded independent attestation missing')
            if any(int(irev.get(k,999) or 0) for k in ['open_p0','open_p1','open_p2']):errors.append('embedded independent review has open findings')
            if rp:
                review_dir=rp.parent
                for fn in REVIEW_FILES:
                    fp=review_dir/fn
                    if not fp.is_file() or irev.get('artifacts',{}).get(fn)!=sha(fp):errors.append('embedded independent review artifact mismatch '+fn)
            checks={'audit_package_manifest_sha256':audit_root/'manifest.json','audit_package_identity_sha256':ip,'audit_summary_sha256':sp,'admission_receipt_sha256':ext_adm,'independent_review_receipt_sha256':rp}
            for key,path in checks.items():
                if path is None or not Path(path).is_file() or rec.get(key)!=sha(Path(path)):errors.append('production receipt hash mismatch '+key)
        stats={'payloads':len(payload),'manifest_entries':len(load(root/'manifest.json').get('entries',[])),'release_id':ident.get('release_id'),'embedded_audit_reverified':audit_root.is_dir()}
    out={'status':'PASS' if not errors else 'FAIL','release_zip':zpath.name,'sha256':sha(zpath) if zpath.exists() else None,'errors':errors,'stats':stats}
    text=json.dumps(out,ensure_ascii=False,indent=2);print(text)
    if a.output:Path(a.output).write_text(text+'\n')
    raise SystemExit(0 if not errors else 1)
if __name__=='__main__':main()
