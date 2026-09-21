#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
import argparse,hashlib,json,subprocess,sys,tempfile,zipfile,shutil
ROOT=Path(__file__).resolve().parents[1]
ADMISSION=ROOT/'modules/control_plane/scripts/intake_admission_gate.py'
AUDIT=ROOT/'modules/audit_os_v6_proof_carrying_construction/scripts/audit_candidate.py'
PROFILE=ROOT/'modules/audit_os_v6_proof_carrying_construction/profiles/CHILD_PHASE_STRICT.json'
PROMOTE=ROOT/'modules/production_release/scripts/promote_audited_candidate.py'
VALIDATE=ROOT/'modules/production_release/scripts/validate_child_production_release.py'

def sha(p:Path):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p:Path,default=None):
    try:return json.loads(p.read_text(encoding='utf-8'))
    except Exception:return default

def candidate_config(candidate:Path):
    if candidate.is_dir():
        xs=list(candidate.rglob('audit_config.json'))
        return load(xs[0],{}) if len(xs)==1 else {}
    with tempfile.TemporaryDirectory() as td:
        with zipfile.ZipFile(candidate) as z:
            names=[n for n in z.namelist() if n.endswith('/audit_config.json') or n=='audit_config.json']
            if len(names)!=1:return {}
            return json.loads(z.read(names[0]).decode('utf-8'))

def call(cmd:list[str],log:Path):
    proc=subprocess.run(cmd,text=True,capture_output=True)
    log.write_text((proc.stdout or '')+(proc.stderr or ''),encoding='utf-8')
    if proc.returncode:raise SystemExit(f'pipeline stage failed ({Path(cmd[1]).name}); see {log}')

def main():
    ap=argparse.ArgumentParser(description='Run exact v10 admission, independent Audit OS v6, deterministic promotion, and release validation.')
    ap.add_argument('candidate_zip');ap.add_argument('--registry',required=True);ap.add_argument('--independent-review-dir',required=True);ap.add_argument('--output-dir',required=True);ap.add_argument('--expected-name');ap.add_argument('--profile',default=str(PROFILE));ap.add_argument('--promoted-at')
    a=ap.parse_args();candidate=Path(a.candidate_zip).resolve();outdir=Path(a.output_dir).resolve();outdir.mkdir(parents=True,exist_ok=True)
    cfg=candidate_config(candidate);production_name=cfg.get('production_release_output_name')
    if not production_name:raise SystemExit('candidate audit_config.json must declare production_release_output_name')
    admission=outdir/'ADMISSION_RECEIPT.json';audit_dir=outdir/'INDEPENDENT_AUDIT_OS_V5';release=outdir/production_name;validation=outdir/'PRODUCTION_RELEASE_VALIDATION.json'
    call([sys.executable,str(ADMISSION),str(candidate),'--registry',str(Path(a.registry).resolve()),'--expected-name',a.expected_name or candidate.name,'--output',str(admission)],outdir/'01_admission.log')
    call([sys.executable,str(AUDIT),str(candidate),'--profile',str(Path(a.profile).resolve()),'--output',str(audit_dir),'--admission-receipt',str(admission),'--independent-review-dir',str(Path(a.independent_review_dir).resolve())],outdir/'02_audit.log')
    cmd=[sys.executable,str(PROMOTE),str(candidate),str(audit_dir),'--admission-receipt',str(admission),'--output',str(release)]
    if a.promoted_at:cmd+=['--promoted-at',a.promoted_at]
    call(cmd,outdir/'03_promotion.log');call([sys.executable,str(VALIDATE),str(release),'--output',str(validation)],outdir/'04_release_validation.log')
    receipt={'status':'PASS','pipeline':'V10_CHILD_PRODUCTION_TRUST_CHAIN','candidate_filename':candidate.name,'candidate_sha256':sha(candidate),'production_release':release.name,'production_release_sha256':sha(release),'admission_receipt':admission.name,'audit_summary':'INDEPENDENT_AUDIT_OS_V5/AUDIT_SUMMARY.json','validation_receipt':validation.name,'live_pointer_updated':False}
    (outdir/'PIPELINE_RECEIPT.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps(receipt,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
