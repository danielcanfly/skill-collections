#!/usr/bin/env python3
from pathlib import Path
import argparse,csv,json

def main():
 ap=argparse.ArgumentParser();ap.add_argument('root');ap.add_argument('--json-output');a=ap.parse_args();root=Path(a.root).resolve();errors=[]
 tp=root/'qa/TOPIC_SEMANTIC_RED_TEAM_TESTS.json';rp=root/'research/topic_semantic_risk_resolution.csv'
 try:tests=json.loads(tp.read_text())
 except Exception as e:tests=[];errors.append('missing/invalid topic semantic risk tests: '+str(e))
 try:
  with rp.open(newline='',encoding='utf-8-sig') as f:rows=list(csv.DictReader(f))
 except Exception as e:rows=[];errors.append('missing/invalid topic risk resolution registry: '+str(e))
 by={r.get('risk_id'):r for r in rows};expected={t.get('risk_id') for t in tests if t.get('risk_id')}
 if len(expected)<5:errors.append('fewer than five dispatcher-authored semantic risks')
 for t in tests:
  rid=t.get('risk_id');r=by.get(rid)
  if not r:errors.append(f'{rid}: missing candidate risk resolution');continue
  for field in ['claims','sources','resolution','residual_gap']:
   if not (r.get(field) or '').strip():errors.append(f'{rid}: empty {field}')
  if r.get('status') not in {'CANDIDATE_SELF_CHECK_PASS','RESOLVED'}:errors.append(f'{rid}: status must be candidate self-check PASS/RESOLVED')
  if t.get('independent_review_required') is not True:errors.append(f'{rid}: independent review requirement missing')
  if t.get('counterexample_required') is not True:errors.append(f'{rid}: counterexample requirement missing')
 extra=set(by)-expected
 if extra:errors.append('unexpected semantic risk IDs: '+','.join(sorted(x for x in extra if x)))
 out={'status':'PASS' if not errors else 'FAIL','mode':'CANDIDATE_SELF_CHECK_ONLY','tests':len(tests),'errors':errors,'independent_review_still_required':True};txt=json.dumps(out,ensure_ascii=False,indent=2);print(txt);p=Path(a.json_output) if a.json_output else root/'qa/topic_red_team_validation.json';p.write_text(txt+'\n');raise SystemExit(0 if not errors else 1)
if __name__=='__main__':main()
