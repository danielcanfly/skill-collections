#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
import argparse,csv,json,hashlib,datetime

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def rows(p):
 with Path(p).open(newline='',encoding='utf-8-sig') as f:return list(csv.DictReader(f))
def main():
 ap=argparse.ArgumentParser(description='Finalize an already-completed external independent review. This script checks consistency; it does not perform source review.')
 ap.add_argument('review_dir');ap.add_argument('--candidate',required=True);ap.add_argument('--attest-independent',action='store_true');ap.add_argument('--reviewed-at');a=ap.parse_args()
 d=Path(a.review_dir).resolve();rp=d/'INDEPENDENT_SEMANTIC_REVIEW_RECEIPT.json';r=json.loads(rp.read_text());errors=[]
 if not a.attest_independent:errors.append('independence attestation flag not provided')
 edge=rows(d/'INDEPENDENT_EDGE_REVIEW.csv');source=rows(d/'INDEPENDENT_SOURCE_REVIEW.csv');loc=rows(d/'INDEPENDENT_LOCATOR_REVIEW.csv');topic=rows(d/'INDEPENDENT_TOPIC_RISK_REVIEW.csv')
 for x in edge:
  if x.get('verdict')!='PASS' or x.get('locator_resolvable')!='PASS' or x.get('source_claim_compatibility')!='PASS' or (x.get('unsupported_material_clause') or '').strip().lower() not in {'','none','n/a','not applicable'}:errors.append('edge review incomplete: '+str((x.get('claim_id'),x.get('source_id'),x.get('clause_id'))))
 for x in source:
  if x.get('identity_verdict')!='PASS' or x.get('proposition_verified')!='PASS':errors.append('source review incomplete: '+str(x.get('source_id')))
 for x in loc:
  if x.get('resolved_verdict')!='PASS':errors.append('locator review incomplete: '+str(x.get('passage_id')))
 for x in topic:
  if x.get('verdict')!='PASS' or x.get('affected_population_reviewed')!='PASS' or x.get('counterexample_tested')!='PASS' or x.get('residual_gap_acceptable')!='PASS' or len((x.get('negative_fixture_or_counterexample_evidence') or '').strip())<10: errors.append('topic risk review incomplete: '+str(x.get('risk_id')))
 c=Path(a.candidate).resolve();csha=sha(c) if c.is_file() else ''
 if not csha:errors.append('candidate must be the exact final ZIP')
 r.update({'status':'PASS' if not errors else 'FAIL','candidate_sha256':csha,'independence_attestation':bool(a.attest_independent),'reviewed_at':a.reviewed_at or datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0).isoformat().replace('+00:00','Z'),'all_retained_direct_support_reviewed':not errors,'retained_direct_support_total':len(edge),'retained_direct_support_pass':sum(x.get('verdict')=='PASS' and x.get('locator_resolvable')=='PASS' and x.get('source_claim_compatibility')=='PASS' and (x.get('unsupported_material_clause') or '').strip().lower() in {'','none','n/a','not applicable'} for x in edge),'source_review_total':len(source),'source_review_pass':sum(x.get('identity_verdict')=='PASS' and x.get('proposition_verified')=='PASS' for x in source),'locator_review_total':len(loc),'locator_review_pass':sum(x.get('resolved_verdict')=='PASS' for x in loc),'topic_risk_review_total':len(topic),'topic_risk_review_pass':sum(x.get('verdict')=='PASS' and x.get('affected_population_reviewed')=='PASS' and x.get('counterexample_tested')=='PASS' and x.get('residual_gap_acceptable')=='PASS' and len((x.get('negative_fixture_or_counterexample_evidence') or '').strip())>=10 for x in topic),'open_p0':0 if not errors else max(1,int(r.get('open_p0',0) or 0)),'open_p1':0 if not errors else max(1,int(r.get('open_p1',0) or 0)),'artifacts':{n:sha(d/n) for n in ['INDEPENDENT_EDGE_REVIEW.csv','INDEPENDENT_SOURCE_REVIEW.csv','INDEPENDENT_LOCATOR_REVIEW.csv','INDEPENDENT_TOPIC_RISK_REVIEW.csv']},'finalization_errors':errors})
 rp.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n');print(json.dumps({'status':r['status'],'errors':errors,'receipt':str(rp)},indent=2));raise SystemExit(0 if not errors else 1)
if __name__=='__main__':main()
