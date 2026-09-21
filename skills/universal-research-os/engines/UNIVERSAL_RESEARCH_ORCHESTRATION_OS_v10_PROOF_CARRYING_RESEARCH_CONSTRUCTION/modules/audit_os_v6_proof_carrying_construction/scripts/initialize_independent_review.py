#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
import argparse,csv,hashlib,json,tempfile,zipfile,shutil,datetime

def sha256_file(p: Path) -> str:
 h=hashlib.sha256()
 with p.open('rb') as f:
  for chunk in iter(lambda:f.read(1024*1024),b''): h.update(chunk)
 return h.hexdigest()

def read_rows(p: Path):
 if not p.is_file(): return []
 with p.open(newline='',encoding='utf-8-sig') as f: return list(csv.DictReader(f))

def write_rows(p: Path, fields, rows):
 p.parent.mkdir(parents=True,exist_ok=True)
 with p.open('w',newline='',encoding='utf-8') as f:
  w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)

def main():
 ap=argparse.ArgumentParser(description='Initialize an external, candidate-SHA-bound v7 independent semantic review workspace.')
 ap.add_argument('candidate')
 ap.add_argument('--output',required=True)
 ap.add_argument('--auditor-id',required=True)
 ap.add_argument('--auditor-session-id',required=True)
 a=ap.parse_args()
 cand=Path(a.candidate).resolve(); out=Path(a.output).resolve()
 if out.exists(): shutil.rmtree(out)
 out.mkdir(parents=True)
 tmp=None
 if cand.is_file():
  csha=sha256_file(cand);tmp=tempfile.TemporaryDirectory();base=Path(tmp.name)
  with zipfile.ZipFile(cand) as z:
   bad=z.testzip()
   if bad: raise SystemExit(f'ZIP CRC failure: {bad}')
   z.extractall(base)
  roots=[p for p in base.iterdir() if p.is_dir()];root=roots[0] if len(roots)==1 else base
 else:
  root=cand;csha='DIRECTORY_REVIEW_REQUIRES_FINAL_ZIP_SHA_BEFORE_PASS'
 edges=read_rows(root/'research/edge_entailment.csv')
 clauses=read_rows(root/'research/claim_clause_matrix.csv')
 passages=read_rows(root/'research/source_passage_registry.csv')
 pmap={r.get('passage_id',''):r for r in passages}
 direct=[e for e in edges if e.get('support_label')=='support' and (e.get('final_disposition') or 'retain') not in {'exclude','defer','remove'}]
 edge_rows=[]
 for e in direct:
  matching=[c for c in clauses if c.get('claim_id')==e.get('claim_id') and c.get('source_id')==e.get('source_id') and c.get('materiality')=='material']
  for c in matching:
   p=pmap.get(e.get('passage_id',''),{})
   edge_rows.append({'edge_id':e.get('edge_id',''),'claim_id':e.get('claim_id',''),'source_id':e.get('source_id',''),'clause_id':c.get('clause_id',''),'verdict':'NOT_REVIEWED','passage_sha256':p.get('excerpt_sha256',''),'locator_resolvable':'NOT_REVIEWED','source_claim_compatibility':'NOT_REVIEWED','unsupported_material_clause':'UNKNOWN','reviewer_notes':''})
 source_ids=sorted({e.get('source_id','') for e in direct if e.get('source_id')})
 source_rows=[{'source_id':s,'identity_verdict':'NOT_REVIEWED','snapshot_sha256':'','authority_tier':'','proposition_verified':'NOT_REVIEWED','reviewer_notes':''} for s in source_ids]
 passage_ids=sorted({e.get('passage_id','') for e in direct if e.get('passage_id')})
 risk_rows=read_rows(root/'research/topic_semantic_risk_resolution.csv')
 topic_rows=[{'risk_id':r.get('risk_id',''),'verdict':'NOT_REVIEWED','affected_population_reviewed':'NOT_REVIEWED','counterexample_tested':'NOT_REVIEWED','residual_gap_acceptable':'NOT_REVIEWED','negative_fixture_or_counterexample_evidence':'','reviewer_notes':''} for r in risk_rows if r.get('risk_id')]
 locator_rows=[]
 for pid in passage_ids:
  p=pmap.get(pid,{})
  locator_rows.append({'passage_id':pid,'locator_type':p.get('locator_type',''),'locator_value':p.get('locator_value',''),'resolved_verdict':'NOT_REVIEWED','snapshot_sha256':p.get('snapshot_sha256',''),'reviewer_notes':''})
 write_rows(out/'INDEPENDENT_EDGE_REVIEW.csv',['edge_id','claim_id','source_id','clause_id','verdict','passage_sha256','locator_resolvable','source_claim_compatibility','unsupported_material_clause','reviewer_notes'],edge_rows)
 write_rows(out/'INDEPENDENT_SOURCE_REVIEW.csv',['source_id','identity_verdict','snapshot_sha256','authority_tier','proposition_verified','reviewer_notes'],source_rows)
 write_rows(out/'INDEPENDENT_LOCATOR_REVIEW.csv',['passage_id','locator_type','locator_value','resolved_verdict','snapshot_sha256','reviewer_notes'],locator_rows)
 write_rows(out/'INDEPENDENT_TOPIC_RISK_REVIEW.csv',['risk_id','verdict','affected_population_reviewed','counterexample_tested','residual_gap_acceptable','negative_fixture_or_counterexample_evidence','reviewer_notes'],topic_rows)
 receipt={'status':'IN_PROGRESS','candidate_sha256':csha,'auditor_id':a.auditor_id,'auditor_session_id':a.auditor_session_id,'auditor_role':'INDEPENDENT','independence_attestation':False,'audit_os_version':'6.0.0','reviewed_at':'','all_retained_direct_support_reviewed':False,'retained_direct_support_total':len(edge_rows),'retained_direct_support_pass':0,'source_review_total':len(source_rows),'source_review_pass':0,'locator_review_total':len(locator_rows),'locator_review_pass':0,'topic_risk_review_total':len(topic_rows),'topic_risk_review_pass':0,'open_p0':999,'open_p1':999,'artifacts':{}}
 (out/'INDEPENDENT_SEMANTIC_REVIEW_RECEIPT.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n')
 (out/'README.md').write_text('# Independent semantic review workspace\n\nThis workspace is external to the candidate. Review every pre-populated row against original-source snapshots. Do not copy candidate self-review verdicts. After review, update the three CSV files, hash them into the receipt, set the independence attestation, counts, timestamp, and final status. The audit runner independently recomputes coverage and rejects missing retained-support clauses.\n')
 print(json.dumps({'status':'PASS','candidate_sha256':csha,'edge_clause_rows':len(edge_rows),'source_rows':len(source_rows),'locator_rows':len(locator_rows),'topic_risk_rows':len(topic_rows),'output':str(out)},indent=2))
if __name__=='__main__': main()
