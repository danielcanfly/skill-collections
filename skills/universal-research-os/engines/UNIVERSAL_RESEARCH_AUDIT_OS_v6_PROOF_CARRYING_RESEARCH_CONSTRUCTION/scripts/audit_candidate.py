#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
import argparse,zipfile,tempfile,subprocess,json,sys,hashlib,datetime,csv,shutil,concurrent.futures
from common import load_json,tree_hash,sha256_file,parse_iso,rows
HERE=Path(__file__).resolve().parents[1]
def fail(out,status,msg,classification='NOT_EVALUATED'):
 s={'status':status,'audit_os_version':'6.0.0','orchestration_contract':'v10','dimension_scores':{'compatibility':0,'semantic':0,'retrieval':0,'seal':0,'independent_semantic':0,'production_assurance':0},'score':0,'admission_classification':classification,'findings':[{'finding_id':'GATE-001','severity':'P0','summary':msg,'blocking':True}]};(out/'AUDIT_SUMMARY.json').write_text(json.dumps(s,indent=2)+'\n');print(json.dumps(s,indent=2));raise SystemExit(1)
ap=argparse.ArgumentParser();ap.add_argument('candidate');ap.add_argument('--profile',default=str(HERE/'profiles/CHILD_PHASE_STRICT.json'));ap.add_argument('--output',required=True);ap.add_argument('--config');ap.add_argument('--admission-receipt',required=True);ap.add_argument('--independent-review-dir',required=True);a=ap.parse_args();cand=Path(a.candidate).resolve();out=Path(a.output).resolve();out.mkdir(parents=True,exist_ok=True)
adm=load_json(a.admission_receipt,{})
if adm.get('status')!='PASS' or adm.get('classification') not in {'V10_NATIVE_ACCEPTED','LEGACY_MIGRATABLE_ACCEPTED'}: fail(out,'ADMISSION_REJECTED','mandatory v10 admission receipt missing or rejected',adm.get('classification','MISSING'))
if adm.get('candidate_sha256')!=sha256_file(cand): fail(out,'ADMISSION_REJECTED','admission receipt candidate SHA does not match candidate',adm.get('classification','UNKNOWN'))
ind=Path(a.independent_review_dir).resolve();receipt=load_json(ind/'INDEPENDENT_SEMANTIC_REVIEW_RECEIPT.json',{})
if not receipt: fail(out,'INDEPENDENT_AUDIT_INCOMPLETE','independent semantic review receipt missing',adm.get('classification'))
errors=[];csha=sha256_file(cand)
for cond,msg in [
 (receipt.get('status')=='PASS','independent receipt not PASS'),(receipt.get('candidate_sha256')==csha,'independent receipt candidate SHA mismatch'),(receipt.get('auditor_role')=='INDEPENDENT','auditor role not INDEPENDENT'),(receipt.get('independence_attestation') is True,'independence attestation missing'),(receipt.get('audit_os_version')=='6.0.0','independent audit version mismatch'),(receipt.get('all_retained_direct_support_reviewed') is True,'not all retained direct-support edges reviewed'),(int(receipt.get('retained_direct_support_total',-1))==int(receipt.get('retained_direct_support_pass',-2)) and int(receipt.get('retained_direct_support_total',0))>=0,'retained support counts inconsistent'),(int(receipt.get('open_p0',999))==0 and int(receipt.get('open_p1',999))==0 and int(receipt.get('open_p2',999))==0,'independent review has open P0/P1/P2')]:
 if not cond: errors.append(msg)
for fn in ['INDEPENDENT_EDGE_REVIEW.csv','INDEPENDENT_SOURCE_REVIEW.csv','INDEPENDENT_LOCATOR_REVIEW.csv','INDEPENDENT_TOPIC_RISK_REVIEW.csv']:
 fp=ind/fn
 if not fp.is_file(): errors.append(fn+' missing')
 elif receipt.get('artifacts',{}).get(fn)!=sha256_file(fp): errors.append(fn+' hash missing or mismatched in receipt')
if errors: fail(out,'INDEPENDENT_AUDIT_INCOMPLETE','; '.join(errors),adm.get('classification'))
# extract
ctx={'candidate_sha256':csha,'candidate_zip_mtime':datetime.datetime.fromtimestamp(cand.stat().st_mtime,datetime.timezone.utc).isoformat()}
tmp=None
if cand.is_file():
 tmp=tempfile.TemporaryDirectory();base=Path(tmp.name)
 with zipfile.ZipFile(cand) as z:
  bad=z.testzip()
  if bad: fail(out,'ADMISSION_REJECTED','ZIP CRC failure')
  z.extractall(base); infos=z.infolist()
 roots=[p for p in base.iterdir() if p.is_dir()];root=roots[0] if len(roots)==1 else base
else:root=cand;infos=[]
# chronology and independence
selfcheck=load_json(root/'qa/candidate_self_check_receipt.json',{})
if receipt.get('auditor_id') and receipt.get('auditor_id')==selfcheck.get('researcher_id'): fail(out,'INDEPENDENT_AUDIT_INCOMPLETE','auditor and researcher identities are the same',adm.get('classification'))
seal=load_json(root/'qa/seal_state.json',{});sealed=parse_iso(seal.get('sealed_at'));reviewed=parse_iso(receipt.get('reviewed_at'));zipmtime=datetime.datetime.fromtimestamp(cand.stat().st_mtime,datetime.timezone.utc)
chron=[]
if not sealed: chron.append('sealed_at missing/invalid')
if not reviewed: chron.append('independent reviewed_at missing/invalid')
if sealed and reviewed and reviewed<sealed: chron.append('independent review predates candidate seal')
now=datetime.datetime.now(datetime.timezone.utc);observed=parse_iso(adm.get('observed_at'))
if sealed and sealed>now+datetime.timedelta(minutes=5): chron.append('candidate seal timestamp is in the future')
if reviewed and reviewed>now+datetime.timedelta(minutes=5): chron.append('independent review timestamp is in the future')
if sealed and sealed>zipmtime+datetime.timedelta(minutes=5): chron.append('candidate seal timestamp is after observed ZIP timestamp')
if observed and reviewed and reviewed<observed: chron.append('independent review predates return admission observation')
# Chronology is a pre-audit identity gate. Do not spend time on semantic validators
# when the artifact lifecycle is impossible or future-dated.
if chron:
 fail(out,'REPAIR_REQUIRED','artifact chronology failure: '+'; '.join(chron),adm.get('classification'))
# run independent read-only validators concurrently. The candidate tree is hashed once before and once after the complete read-only phase.
cfg=Path(a.config).resolve() if a.config else root/'audit_config.json';reg=load_json(HERE/'config/validator_registry.json',{});findings=[];results=[];dim={'compatibility':[],'semantic':[],'retrieval':[],'seal':[],'independent_semantic':[True],'production_assurance':[]}
profile_data=load_json(Path(a.profile).resolve(),{}); parallelism=max(1,min(int(profile_data.get('validator_parallelism',4)),8)); baseline_tree=tree_hash(root)
def run_validator(v):
 rp=out/f"{v['id']}.json";cmd=[sys.executable,str(HERE/'scripts'/v['script']),str(root),'--config',str(cfg),'--profile',str(Path(a.profile).resolve()),'--output',str(rp)];proc=subprocess.run(cmd,capture_output=True,text=True)
 try:r=json.loads(rp.read_text())
 except:r={'status':'FAIL','errors':[proc.stderr or proc.stdout or 'validator produced no result']}
 return v,proc,r,rp
validators=reg.get('validators',[])
with concurrent.futures.ThreadPoolExecutor(max_workers=parallelism) as ex:
 validator_runs=list(ex.map(run_validator,validators))
mutated=tree_hash(root)!=baseline_tree
for v,proc,r,rp in validator_runs:
 if mutated:r={'status':'FAIL','errors':r.get('errors',[])+['one or more validators mutated candidate tree during read-only audit phase']}
 d=v.get('dimension','semantic');dim.setdefault(d,[]).append(r.get('status')=='PASS');results.append({'id':v['id'],'dimension':d,'status':r.get('status'),'returncode':proc.returncode,'result_file':rp.name})
 if r.get('status')!='PASS':findings.append({'finding_id':f'AUTO-{len(findings)+1:03d}','severity':'P0' if mutated else 'P1','rule_id':v['id'],'dimension':d,'status':'open','summary':'; '.join(r.get('errors',[])[:8]),'evidence':[rp.name],'blocking':True})
# independent rows must cover all direct support material clauses
edges=rows(root/'research/edge_entailment.csv');clauses=rows(root/'research/claim_clause_matrix.csv');irev=rows(ind/'INDEPENDENT_EDGE_REVIEW.csv');irevkey={(r.get('claim_id'),r.get('source_id'),r.get('clause_id')):r for r in irev};needed=[]
for e in edges:
 if e.get('support_label')=='support':
  for c in clauses:
   if c.get('claim_id')==e.get('claim_id') and c.get('source_id')==e.get('source_id') and c.get('materiality')=='material': needed.append((c.get('claim_id'),c.get('source_id'),c.get('clause_id')))
missing=[];bad=[];pmap={r.get('passage_id'):r for r in rows(root/'research/source_passage_registry.csv')};emap={(e.get('claim_id'),e.get('source_id')):e for e in edges}
for k in needed:
 r=irevkey.get(k);e=emap.get((k[0],k[1]),{});p0=pmap.get(e.get('passage_id'),{})
 if not r: missing.append(k)
 elif r.get('verdict')!='PASS' or r.get('locator_resolvable')!='PASS' or r.get('source_claim_compatibility')!='PASS' or (r.get('unsupported_material_clause') or '').strip().lower() not in {'','none','n/a'} or r.get('passage_sha256')!=p0.get('excerpt_sha256'): bad.append(k)
# source and locator independent review coverage
srev=rows(ind/'INDEPENDENT_SOURCE_REVIEW.csv');lrev=rows(ind/'INDEPENDENT_LOCATOR_REVIEW.csv');trev=rows(ind/'INDEPENDENT_TOPIC_RISK_REVIEW.csv');sby={r.get('source_id'):r for r in srev};lby={r.get('passage_id'):r for r in lrev};tby={r.get('risk_id'):r for r in trev};direct_sources={e.get('source_id') for e in edges if e.get('support_label')=='support'};direct_passages={e.get('passage_id') for e in edges if e.get('support_label')=='support'}
for sid in direct_sources:
 r=sby.get(sid)
 if not r or r.get('identity_verdict')!='PASS' or r.get('proposition_verified')!='PASS': bad.append(('source',sid,''))
for pid in direct_passages:
 r=lby.get(pid);p0=pmap.get(pid,{})
 if not r or r.get('resolved_verdict')!='PASS' or r.get('snapshot_sha256')!=p0.get('snapshot_sha256'): bad.append(('locator',pid,''))
# Every dispatcher-authored semantic risk must be externally reviewed with a counterexample or negative-fixture evidence reference.
risk_rows=rows(root/'research/topic_semantic_risk_resolution.csv');risk_ids={r.get('risk_id') for r in risk_rows if r.get('risk_id')}
for rid in risk_ids:
 r=tby.get(rid)
 if not r or r.get('verdict')!='PASS' or r.get('affected_population_reviewed')!='PASS' or r.get('counterexample_tested')!='PASS' or r.get('residual_gap_acceptable')!='PASS' or len((r.get('negative_fixture_or_counterexample_evidence') or '').strip())<10: bad.append(('topic-risk',rid,''))
# Receipt counts must describe the actual independently governed population.
try:
 if int(receipt.get('retained_direct_support_total',-1))!=len(needed) or int(receipt.get('retained_direct_support_pass',-1))!=len(needed): bad.append(('receipt','edge-counts',''))
 if int(receipt.get('source_review_total',-1))!=len(direct_sources) or int(receipt.get('source_review_pass',-1))!=len(direct_sources): bad.append(('receipt','source-counts',''))
 if int(receipt.get('locator_review_total',-1))!=len(direct_passages) or int(receipt.get('locator_review_pass',-1))!=len(direct_passages): bad.append(('receipt','locator-counts',''))
 if int(receipt.get('topic_risk_review_total',-1))!=len(risk_ids) or int(receipt.get('topic_risk_review_pass',-1))!=len(risk_ids): bad.append(('receipt','topic-risk-counts',''))
except Exception: bad.append(('receipt','invalid-counts',''))
if missing or bad:
 dim['independent_semantic']=[False];findings.append({'finding_id':'INDEP-001','severity':'P0','rule_id':'independent_clause_coverage','dimension':'independent_semantic','status':'open','summary':f'missing={len(missing)} bad={len(bad)} independent review records','blocking':True})
else: dim['independent_semantic']=[True]
scores={k:(round(100*sum(v)/len(v)) if v else 0) for k,v in dim.items()};status='MERGE_READY' if not findings and all(x==100 for x in scores.values()) else 'REPAIR_REQUIRED'
summary={'status':status,'audit_os_version':'6.0.0','orchestration_contract':'v10','score':min(scores.values()),'dimension_scores':scores,'candidate':cand.name,'candidate_sha256':csha,'validators':results,'findings':findings,'admission_classification':adm.get('classification'),'independent_review_status':receipt.get('status'),'independent_auditor_id':receipt.get('auditor_id'),'open_p0':0 if not findings else sum(1 for x in findings if x.get('severity')=='P0'),'open_p1':0 if not findings else sum(1 for x in findings if x.get('severity')=='P1'),'open_p2':0,'completed_at':receipt.get('reviewed_at') or adm.get('observed_at')}
(out/'AUDIT_SUMMARY.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
(out/'FINDINGS_REGISTER.json').write_text(json.dumps(findings,ensure_ascii=False,indent=2)+'\n')
# V9 audit outputs are self-contained, strictly manifest-governed evidence packages.
inputs=out/'inputs'; review_out=inputs/'independent_review'; review_out.mkdir(parents=True,exist_ok=True)
shutil.copy2(Path(a.admission_receipt).resolve(),inputs/'admission_receipt.json')
for fn in ['INDEPENDENT_SEMANTIC_REVIEW_RECEIPT.json','INDEPENDENT_EDGE_REVIEW.csv','INDEPENDENT_SOURCE_REVIEW.csv','INDEPENDENT_LOCATOR_REVIEW.csv','INDEPENDENT_TOPIC_RISK_REVIEW.csv']:
 shutil.copy2(ind/fn,review_out/fn)
identity={'package_type':'INDEPENDENT_AUDIT_OUTPUT','audit_os_version':'6.0.0','orchestration_contract':'v10','candidate_filename':cand.name,'candidate_sha256':csha,'admission_receipt_sha256':sha256_file(inputs/'admission_receipt.json'),'independent_review_receipt_sha256':sha256_file(review_out/'INDEPENDENT_SEMANTIC_REVIEW_RECEIPT.json'),'audit_summary_sha256':sha256_file(out/'AUDIT_SUMMARY.json'),'status':status}
(out/'AUDIT_PACKAGE_IDENTITY.json').write_text(json.dumps(identity,ensure_ascii=False,indent=2)+'\n')
entries=[]
for fp in sorted(x for x in out.rglob('*') if x.is_file() and x.relative_to(out).as_posix() not in {'manifest.json','SHA256SUMS.txt'}):
 entries.append({'path':fp.relative_to(out).as_posix(),'sha256':sha256_file(fp),'bytes':fp.stat().st_size})
(out/'manifest.json').write_text(json.dumps({'manifest_version':'1.0','package_type':'INDEPENDENT_AUDIT_OUTPUT','entries':entries},ensure_ascii=False,indent=2)+'\n')
(out/'SHA256SUMS.txt').write_text(''.join(f"{e['sha256']}  {e['path']}\n" for e in entries),encoding='utf-8')
print(json.dumps(summary,ensure_ascii=False,indent=2));raise SystemExit(0 if status=='MERGE_READY' else 1)
