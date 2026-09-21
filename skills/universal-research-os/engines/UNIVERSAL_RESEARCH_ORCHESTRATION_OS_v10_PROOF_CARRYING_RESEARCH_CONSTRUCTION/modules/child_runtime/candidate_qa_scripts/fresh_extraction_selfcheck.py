#!/usr/bin/env python3
from pathlib import Path
import argparse,zipfile,tempfile,json,hashlib

def strict_manifest(root):
    mp=root/'handoff/file_manifest.json'; errors=[]
    if not mp.exists(): return ['manifest missing'],0,0
    d=json.loads(mp.read_text(encoding='utf-8')); entries=d.get('files',[])
    exp={e['path']:e for e in entries if isinstance(e,dict) and e.get('path') and e.get('sha256')}
    actual={p.relative_to(root).as_posix():p for p in root.rglob('*') if p.is_file() and p!=mp and p.name!='SHA256SUMS.txt'}
    for rel,p in actual.items():
        if rel not in exp: errors.append('unexpected/unmanifested '+rel)
        elif hashlib.sha256(p.read_bytes()).hexdigest()!=exp[rel]['sha256']: errors.append('hash mismatch '+rel)
    for rel in exp:
        if rel not in actual: errors.append('manifested file missing '+rel)
    return errors,len(exp),len(actual)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('candidate_zip')
    ap.add_argument('--allow-pre-manifest',action='store_true')
    ap.add_argument('--expected-final-name')
    a=ap.parse_args()
    zpath=Path(a.candidate_zip).resolve(); errors=[]
    try:
        with zipfile.ZipFile(zpath) as z:
            bad=z.testzip()
            if bad: errors.append('ZIP CRC failure '+bad)
            roots={Path(n).parts[0] for n in z.namelist() if n and not n.startswith('__MACOSX/')}
            if len(roots)!=1: errors.append(f'ZIP must have one root, found {sorted(roots)}')
            with tempfile.TemporaryDirectory() as td:
                z.extractall(td); root=Path(td)/next(iter(roots)) if roots else Path(td)
                me,mc,ac=strict_manifest(root); errors.extend(me)
                sp=root/'qa/seal_state.json'
                if not sp.exists(): errors.append('qa/seal_state.json missing')
                else:
                    s=json.loads(sp.read_text(encoding='utf-8'))
                    allowed={'MANIFEST_FROZEN','SEALED'} if a.allow_pre_manifest else {'SEALED'}
                    if s.get('state') not in allowed: errors.append('invalid seal state '+str(s.get('state')))
                    if int(s.get('post_manifest_mutations',1))!=0: errors.append('post-manifest mutations nonzero')
                    if s.get('manifest_generated_after_all_receipts') is not True: errors.append('manifest-after-receipts flag false')
                    if not a.allow_pre_manifest and s.get('fresh_extraction_verified') is not True: errors.append('fresh extraction flag false')
                if (root/'qa/seal_state.json').exists(): errors.append('legacy uppercase seal state exists')
                cfg=json.loads((root/'audit_config.json').read_text(encoding='utf-8')) if (root/'audit_config.json').exists() else {}
                if not a.allow_pre_manifest and a.expected_final_name and zpath.name!=a.expected_final_name: errors.append('final ZIP filename mismatch')
                if a.expected_final_name and cfg.get('final_output_name')!=a.expected_final_name: errors.append('audit_config final_output_name mismatch')
    except Exception as e:
        errors.append('fresh extraction failed: '+str(e)); mc=ac=0
    out={'status':'PASS' if not errors else 'FAIL','zip':zpath.name,'sha256':hashlib.sha256(zpath.read_bytes()).hexdigest() if zpath.exists() else None,'manifested':mc,'actual':ac,'errors':errors}
    print(json.dumps(out,ensure_ascii=False,indent=2))
    raise SystemExit(0 if not errors else 1)
if __name__=='__main__': main()
