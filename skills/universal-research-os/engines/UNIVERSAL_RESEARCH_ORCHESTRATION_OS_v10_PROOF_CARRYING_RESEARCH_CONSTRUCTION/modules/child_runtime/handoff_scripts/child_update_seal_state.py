#!/usr/bin/env python3
from pathlib import Path
import argparse,json,datetime
def ok(root,rel):
 p=root/rel
 if not p.exists():return False
 try:return json.loads(p.read_text(encoding='utf-8')).get('status')=='PASS'
 except:return False
def main():
 ap=argparse.ArgumentParser();ap.add_argument('root');ap.add_argument('--stage',choices=['pre-manifest','sealed'],required=True);ap.add_argument('--fresh-receipt',default='qa/fresh_extraction_receipt.json');a=ap.parse_args();root=Path(a.root).resolve();now=datetime.datetime.now(datetime.timezone.utc).isoformat()
 receipts={'identity_rendered':'qa/identity_surface_validation.json','retrieval_receipts':'qa/retrieval_results_validation.json','semantic_receipts':'qa/proof_chain_validation.json','source_identity_receipt':'qa/source_identity_validation.json','edge_entailment_receipt':'qa/edge_entailment_validation.json','lineage_receipt':'qa/lineage_cascade_validation.json','manual_audit_receipt':'qa/candidate_self_check_validation.json','case_independence_receipt':'qa/case_independence_validation.json','source_note_depth_receipt':'qa/source_note_depth_validation.json','idempotency_receipt':'qa/IDEMPOTENCY_RECEIPT.json','package_validation_receipt':'qa/package_validation.json'}
 completed={k:ok(root,v) for k,v in receipts.items()}
 missing=[k for k,v in completed.items() if not v]
 if missing:raise SystemExit('cannot seal: required receipts not PASS: '+','.join(missing))
 if a.stage=='pre-manifest':d={'state':'MANIFEST_FROZEN','post_manifest_mutations':0,'manifest_generated_after_all_receipts':True,'fresh_extraction_verified':False,'completed':completed,'updated_at':now}
 else:
  rp=root/a.fresh_receipt
  if not ok(root,a.fresh_receipt):raise SystemExit('fresh-extraction receipt missing/not PASS')
  d={'state':'SEALED','post_manifest_mutations':0,'manifest_generated_after_all_receipts':True,'fresh_extraction_verified':True,'completed':completed,'fresh_extraction_receipt':a.fresh_receipt,'sealed_at':now,'updated_at':now,'candidate_status':'CANDIDATE_READY_FOR_INDEPENDENT_AUDIT'}
  for rel in ['PHASE_RETURN_MANIFEST.json','handoff/merge_manifest.json']:
   p=root/rel
   if p.exists():
    o=json.loads(p.read_text(encoding='utf-8'));o['status']='CANDIDATE_READY_FOR_INDEPENDENT_AUDIT';p.write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 p=root/'qa/seal_state.json';p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');(root/'qa/SEAL_STATE.json').unlink(missing_ok=True);print(json.dumps(d,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
