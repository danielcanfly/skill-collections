#!/usr/bin/env python3
from pathlib import Path
import tempfile,csv,json,hashlib,sys,subprocess,shutil,datetime,runpy,contextlib,io
ROOT=Path(__file__).resolve().parents[2]
PC=ROOT/'modules/proof_carrying_construction/scripts'

def wcsv(p,rows,fields):
 p.parent.mkdir(parents=True,exist_ok=True)
 with p.open('w',newline='',encoding='utf-8') as f:w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)
def rows(p):
 with p.open(newline='',encoding='utf-8-sig') as f:return list(csv.DictReader(f))
def rsha(r,fields):return hashlib.sha256('\n'.join(str(r.get(k,'')).strip() for k in fields).encode()).hexdigest()
PF=['passage_id','source_id','excerpt_sha256','snapshot_sha256','locator_type','locator_value']
CF=['clause_id','proposed_claim_id','clause_text','passage_ids','support_status','unsupported_remainder']
def fixture(root,bad=None):
 (root/'research/source_snapshots').mkdir(parents=True);(root/'qa').mkdir();(root/'handoff').mkdir();(root/'external_stage_review').mkdir()
 sn=[];pa=[];cl=[];ed=[];pr=[];cr=[]
 now='2026-07-18T12:00:00Z'
 for i in range(40):
  sid=f'S{i:03d}';pid=f'P{i:03d}';cid=f'C{i:03d}';clid=f'CL{i:03d}';text=f'Primary source statement number {i} establishes bounded proposition {i}.';sp=root/f'research/source_snapshots/{sid}.txt';sp.write_text(text)
  ssha=hashlib.sha256(text.encode()).hexdigest();sn.append({'source_id':sid,'snapshot_path':sp.relative_to(root).as_posix(),'snapshot_sha256':ssha,'source_identity_status':'PASS','production_eligibility':'ELIGIBLE'})
  pa.append({'passage_id':pid,'source_id':sid,'passage_type':'verbatim','excerpt_text':text,'locator_type':'page','locator_value':f'page {i+1}','locator_resolved':'PASS','snapshot_path':sp.relative_to(root).as_posix(),'snapshot_sha256':ssha,'excerpt_sha256':ssha,'observed_at':now,'candidate_reviewer_status':'SELF_CHECK','capture_method':'snapshot','source_access_level':'public','production_eligibility':'ELIGIBLE'})
  cl.append({'clause_id':clid,'proposed_claim_id':cid,'clause_text':f'Bounded proposition {i}.','passage_ids':pid,'support_status':'SUPPORTED','unsupported_remainder':'none','external_pre_review_status':'PENDING'})
  ed.append({'edge_id':f'E{i:03d}','claim_id':cid,'source_id':sid,'passage_id':pid,'support_label':'support','final_disposition':'retain'})
 if bad=='overclaim':cl[0]['unsupported_remainder']='extra unsupported rule'
 if bad=='locator':pa[0]['locator_value']='original document section on topic'
 if bad=='zero':cl=[];ed=[]
 lineage={'researcher_id':'builder-A','researcher_session_id':'builder-session-A','contract_generation':'v10','audit_os_version':'6.0.0'};(root/'handoff/contract_lineage.json').write_text(json.dumps(lineage,indent=2)+'\n')
 wcsv(root/'research/source_snapshot_registry.csv',sn,list(sn[0]));wcsv(root/'research/source_passage_registry.csv',pa,list(pa[0]));wcsv(root/'research/material_clause_registry.csv',cl,list(cl[0]) if cl else ['clause_id','proposed_claim_id','clause_text','passage_ids','support_status','unsupported_remainder','external_pre_review_status']);wcsv(root/'research/edge_entailment.csv',ed,list(ed[0]) if ed else ['edge_id','claim_id','source_id','passage_id','support_label','final_disposition'])
 reviewer_id='builder-A' if bad=='self_review' else 'auditor-B';reviewer_session='builder-session-A' if bad=='self_review' else 'auditor-session-B'
 for q in pa:pr.append({'passage_id':q['passage_id'],'row_sha256':rsha(q,PF),'verdict':'PASS','reviewer_id':reviewer_id,'reviewer_session_id':reviewer_session,'reviewed_at':now,'notes':'verified against snapshot'})
 for q in cl:
  verdict='PASS' if q['support_status']=='SUPPORTED' and q['unsupported_remainder'].lower() in {'','none'} else 'NON_DIRECT';cr.append({'clause_id':q['clause_id'],'row_sha256':rsha(q,CF),'verdict':verdict,'reviewer_id':reviewer_id,'reviewer_session_id':reviewer_session,'reviewed_at':now,'notes':'full-population review'})
 if bad=='review_omission' and pr:pr.pop()
 wcsv(root/'external_stage_review/PASSAGE_REVIEW.csv',pr,list(pr[0]) if pr else ['passage_id','row_sha256','verdict','reviewer_id','reviewer_session_id','reviewed_at','notes']);wcsv(root/'external_stage_review/CLAUSE_REVIEW.csv',cr,list(cr[0]) if cr else ['clause_id','row_sha256','verdict','reviewer_id','reviewer_session_id','reviewed_at','notes'])
 ident={'status':'PASS','contract_generation':'v10','audit_os_version':'6.0.0','reviewer_id':reviewer_id,'reviewer_session_id':reviewer_session,'passage_registry_sha256':hashlib.sha256((root/'research/source_passage_registry.csv').read_bytes()).hexdigest(),'clause_registry_sha256':hashlib.sha256((root/'research/material_clause_registry.csv').read_bytes()).hexdigest()};(root/'external_stage_review/STAGE_REVIEW_IDENTITY.json').write_text(json.dumps(ident,indent=2)+'\n')
 return root
def run(root):
 scripts=['validate_source_snapshots.py','validate_external_stage_review.py','validate_passage_stage.py','validate_clause_stage.py','compile_direct_support_claims.py','validate_proof_chain.py']
 old_argv=list(sys.argv);old_path=list(sys.path);buf=io.StringIO()
 try:
  sys.path.insert(0,str(PC))
  with contextlib.redirect_stdout(buf),contextlib.redirect_stderr(buf):
   for n in scripts:
    sys.argv=[n,str(root)]
    try:runpy.run_path(str(PC/n),run_name='__main__')
    except SystemExit as e:
     if int(e.code or 0)!=0:return False,buf.getvalue()
  return True,buf.getvalue()
 finally:
  sys.argv=old_argv;sys.path[:]=old_path
def main():
 results=[]
 with tempfile.TemporaryDirectory() as td:
  b=Path(td);ok,_=run(fixture(b/'good'));results.append({'test':'good_40_claim_proof_chain','pass':ok})
  for bad in ['overclaim','locator','zero','self_review','review_omission']:
   ok,_=run(fixture(b/bad,bad));results.append({'test':'reject_'+bad,'pass':not ok})
 static=[
  ('sealed_at_runtime','sealed_at' in (ROOT/'modules/child_runtime/candidate_qa_scripts/update_seal_state.py').read_text()),
  ('retrieval_ranked_ids','ranked_ids' in (ROOT/'modules/child_runtime/candidate_qa_scripts/run_retrieval_benchmark.py').read_text() and 'cm["corpus_hash"]' in (ROOT/'modules/child_runtime/candidate_qa_scripts/run_retrieval_benchmark.py').read_text()),
  ('source_note_depth_in_finalizer','validate_source_note_depth.py' in (ROOT/'modules/child_runtime/candidate_qa_scripts/finalize_candidate.py').read_text()),
  ('external_stage_review_in_finalizer','validate_external_stage_review.py' in (ROOT/'modules/child_runtime/candidate_qa_scripts/finalize_candidate.py').read_text()),
  ('audit_v6',json.loads((ROOT/'modules/audit_os_v6_proof_carrying_construction/VERSION.json').read_text())['version']=='6.0.0'),
  ('global_g8_pending','PENDING_EXTERNAL_AUDIT' in (ROOT/'modules/global_builder/scripts/build_global_candidate.py').read_text()),
  ('global_upstream_wrapper_revalidation','validate_child_production_release.py' in (ROOT/'modules/global_builder/scripts/build_global_candidate.py').read_text()),
  ('handoff_manifest_strict',(ROOT/'modules/handoff_compiler/scripts/validate_handoff_package.py').exists()),
  ('canonical_validator_parity',(ROOT/'scripts/verify_canonical_validator_parity.py').exists()),
  ('protected_baseline_tool',(ROOT/'modules/handoff_compiler/scripts/compare_protected_surfaces.py').exists()),
  ('legacy_migration_no_grandfather','grandfathering_allowed' in (ROOT/'modules/legacy_migration/scripts/classify_legacy.py').read_text()),
 ]
 results.extend({'test':n,'pass':bool(v)} for n,v in static)
 out={'status':'PASS' if all(x['pass'] for x in results) else 'FAIL','passed':sum(x['pass'] for x in results),'total':len(results),'fixture_claims':40,'results':results};(ROOT/'V10_LARGE_FIXTURE_SELFTEST.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2));sys.exit(0 if out['status']=='PASS' else 1)
if __name__=='__main__':main()
