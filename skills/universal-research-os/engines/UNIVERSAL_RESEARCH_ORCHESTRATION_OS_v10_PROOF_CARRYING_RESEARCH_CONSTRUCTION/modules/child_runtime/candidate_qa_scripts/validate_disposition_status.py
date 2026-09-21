#!/usr/bin/env python3
from pathlib import Path
import argparse,csv,json,re
ALLOWED={'create','merge','split','exclude','defer'}; FINAL={'accepted','production-candidate','active','canonical','complete','resolved'}
def rows(p): return list(csv.DictReader(p.open(encoding='utf-8-sig',newline=''))) if p.exists() else []
def ids(s): return {x.strip() for x in re.split(r'[;,|]',s or '') if x.strip()}
def main():
 ap=argparse.ArgumentParser(); ap.add_argument('root'); ap.add_argument('--json-output'); a=ap.parse_args(); root=Path(a.root).resolve(); errors=[]; can=rows(root/'research/canonical_concept_registry.csv'); exp=rows(root/'research/expected_node_disposition.csv')
 for r in can:
  if r.get('status','').lower() not in FINAL: errors.append(f"{r.get('id')}: non-final canonical status {r.get('status')}")
 for r in exp:
  if r.get('final_disposition') not in ALLOWED: errors.append(f"{r.get('candidate_id')}: invalid disposition {r.get('final_disposition')}")
  if r.get('status','').lower() not in FINAL: errors.append(f"{r.get('candidate_id')}: non-final disposition status {r.get('status')}")
  n=len(ids(r.get('source_ids')))
  try: declared=int(r.get('source_count',''))
  except: declared=-1; errors.append(f"{r.get('candidate_id')}: missing numeric source_count")
  if declared!=n: errors.append(f"{r.get('candidate_id')}: source_count {declared} != {n}")
 out={'status':'PASS' if not errors else 'FAIL','canonical_rows':len(can),'disposition_rows':len(exp),'errors':errors}; txt=json.dumps(out,ensure_ascii=False,indent=2); print(txt); p=Path(a.json_output) if a.json_output else root/'qa/disposition_status_validation.json'; p.write_text(txt+'\n',encoding='utf-8'); raise SystemExit(0 if not errors else 1)
if __name__=='__main__': main()
