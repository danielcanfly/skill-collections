#!/usr/bin/env python3
from pathlib import Path
import argparse,subprocess,sys,zipfile,json,hashlib

def run(cmd):
 print('+',' '.join(map(str,cmd)));subprocess.run(cmd,check=True)
def make_zip(root,out):
 if out.exists():out.unlink()
 epoch=(1980,1,1,0,0,0)
 with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
  for p in sorted(x for x in root.rglob('*') if x.is_file()):
   info=zipfile.ZipInfo((Path(root.name)/p.relative_to(root)).as_posix(),epoch);info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o100644<<16
   z.writestr(info,p.read_bytes())
 with zipfile.ZipFile(out) as z:
  bad=z.testzip()
  if bad:raise SystemExit('ZIP integrity failure '+bad)
def main():
 ap=argparse.ArgumentParser();ap.add_argument('root');ap.add_argument('--case-min',type=int);ap.add_argument('--output-zip',required=True);a=ap.parse_args();root=Path(a.root).resolve();out=Path(a.output_zip).resolve();cfg=json.loads((root/'audit_config.json').read_text());expected=cfg['final_output_name'];case_min=a.case_min or int(cfg.get('case_minimum',6));py=sys.executable
 if out.name!=expected:raise SystemExit(f'wrong output filename: expected {expected}')
 run([py,str(root/'qa/validate_contract_lineage.py'),str(root)])
 run([py,str(root/'qa/render_identity_surfaces.py'),str(root)])
 run([py,str(root/'qa/run_retrieval_benchmark.py'),'--root',str(root)])
 run([py,str(root/'qa/run_auditor_holdout.py'),str(root),'--tests',str(root/'qa/AUDITOR_HOLDOUT_TESTS.json'),'--source-tests',str(root/'qa/AUDITOR_SOURCE_PROVENANCE_TESTS.json')])
 validators=['validate_external_stage_review.py','validate_semantic_provenance.py','validate_audit_os_contract.py','validate_source_identity.py','validate_source_metadata_completeness.py','validate_source_passage_registry.py','validate_source_evidence_coverage.py','validate_claim_clause_matrix.py','validate_cross_domain_compatibility.py','validate_edge_entailment.py','validate_candidate_self_check.py','validate_contextual_relevance.py','validate_disposition_status.py','validate_lineage_cascade.py','validate_source_note_depth.py','validate_source_snapshots.py','validate_passage_stage.py','validate_clause_stage.py','validate_proof_chain.py','validate_node_semantic_diversity.py','validate_node_operational_depth.py','validate_temporal_metadata.py','validate_case_independence.py','validate_topic_red_team.py','validate_repair_contract_conflicts.py','validate_portable_reproducibility.py','validate_production_surface_hygiene.py','validate_zero_open_findings.py','validate_identity_surfaces.py']
 for name in validators:run([py,str(root/'qa'/name),str(root)])
 run([py,str(root/'qa/verify_idempotency.py'),str(root),'--case-min',str(case_min),'--output',str(root/'qa/IDEMPOTENCY_RECEIPT.json')])
 run([py,str(root/'qa/make_file_manifest.py'),str(root)]);run([py,str(root/'qa/validate_package.py'),str(root),'--case-min',str(case_min),'--json-output',str(root/'qa/package_validation.json')])
 run([py,str(root/'qa/update_seal_state.py'),str(root),'--stage','pre-manifest']);run([py,str(root/'qa/make_file_manifest.py'),str(root)]);run([py,str(root/'qa/verify_manifest_readonly.py'),str(root)])
 provisional=out.with_name(out.stem+'.PROVISIONAL.zip');make_zip(root,provisional)
 run([py,str(root/'qa/fresh_extraction_selfcheck.py'),str(provisional),'--allow-pre-manifest','--expected-final-name',expected])
 receipt={'status':'PASS','mode':'two-stage-fresh-extraction','provisional_zip':provisional.name,'provisional_sha256':hashlib.sha256(provisional.read_bytes()).hexdigest(),'final_exact_zip_readonly_check_required':True};(root/'qa/fresh_extraction_receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
 run([py,str(root/'qa/update_seal_state.py'),str(root),'--stage','sealed']);run([py,str(root/'qa/validate_seal_state.py'),str(root)]);run([py,str(root/'qa/make_file_manifest.py'),str(root)]);run([py,str(root/'qa/verify_manifest_readonly.py'),str(root)]);make_zip(root,out);run([py,str(root/'qa/fresh_extraction_selfcheck.py'),str(out),'--expected-final-name',expected]);provisional.unlink(missing_ok=True)
 print(json.dumps({'status':'PASS','output':str(out),'sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'next_required_step':'Run mandatory v10 admission, external independent Audit OS v6, then promote the exact audited ZIP to a child production release.'},indent=2))
if __name__=='__main__':main()
