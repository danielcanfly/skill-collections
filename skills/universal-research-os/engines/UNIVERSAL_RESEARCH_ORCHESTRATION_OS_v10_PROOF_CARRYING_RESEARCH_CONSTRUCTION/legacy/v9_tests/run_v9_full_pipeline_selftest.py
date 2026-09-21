#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
import tempfile,subprocess,sys,json,hashlib,os
ROOT=Path(__file__).resolve().parents[1]
FIX=ROOT/'tests/fixtures'
AUDIT=ROOT/'modules/audit_os_v6_proof_carrying_construction/scripts/audit_candidate.py'
PROFILE=ROOT/'modules/audit_os_v6_proof_carrying_construction/profiles/CHILD_PHASE_STRICT.json'
PROMOTE=ROOT/'modules/production_release/scripts/promote_audited_candidate.py'
VALIDATE=ROOT/'modules/production_release/scripts/validate_child_production_release.py'
ENV={**os.environ,'PYTHONDONTWRITEBYTECODE':'1','TZ':'UTC','LC_ALL':'C.UTF-8'}
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def call(args):
 p=subprocess.run([str(x) for x in args],capture_output=True,text=True,env=ENV,timeout=300)
 if p.returncode:raise SystemExit((p.stdout or '')+(p.stderr or ''))
 return p
with tempfile.TemporaryDirectory() as td0:
 td=Path(td0);audit=td/'audit';release=td/'DEMO_PRODUCTION_RELEASE_v1.zip';validation=td/'validation.json'
 call([sys.executable,AUDIT,FIX/'V9_GOOD_CANDIDATE.zip','--profile',PROFILE,'--output',audit,'--admission-receipt',FIX/'V9_GOOD_ADMISSION.json','--independent-review-dir',FIX/'V9_GOOD_INDEPENDENT_REVIEW'])
 summary=json.loads((audit/'AUDIT_SUMMARY.json').read_text())
 if summary.get('status')!='MERGE_READY' or summary.get('score')!=100 or any(v!=100 for v in summary.get('dimension_scores',{}).values()):raise SystemExit('Audit OS v5 did not produce exact six-dimensional MERGE_READY')
 call([sys.executable,PROMOTE,FIX/'V9_GOOD_CANDIDATE.zip',audit,'--admission-receipt',FIX/'V9_GOOD_ADMISSION.json','--output',release,'--promoted-at','2026-07-16T14:01:00Z'])
 call([sys.executable,VALIDATE,release,'--output',validation])
 val=json.loads(validation.read_text())
 if val.get('status')!='PASS':raise SystemExit('production wrapper revalidation failed')
 result={'status':'PASS','pipeline':'V9_CANDIDATE_TO_AUDITED_PRODUCTION_RELEASE','candidate_sha256':sha(FIX/'V9_GOOD_CANDIDATE.zip'),'audit_os_version':'6.0.0','audit_status':summary['status'],'dimension_scores':summary['dimension_scores'],'production_release_sha256':sha(release),'wrapper_validation':val,'stages':['candidate','v9-admission','external-independent-review','audit-os-v5','deterministic-promotion','embedded-chain-revalidation']}
 (ROOT/'V9_FULL_PIPELINE_RESULT.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps(result,ensure_ascii=False,indent=2))
