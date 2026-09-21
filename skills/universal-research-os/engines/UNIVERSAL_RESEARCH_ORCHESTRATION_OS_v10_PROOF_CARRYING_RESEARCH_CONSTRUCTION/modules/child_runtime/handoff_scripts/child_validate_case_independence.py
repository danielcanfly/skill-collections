#!/usr/bin/env python3
from pathlib import Path
import argparse,csv,json,re
def rows(p): return list(csv.DictReader(p.open(encoding='utf-8-sig',newline=''))) if p.exists() else []
def ids(s): return {x.strip() for x in re.split(r'[;,|]',s or '') if x.strip()}
def main():
 ap=argparse.ArgumentParser(); ap.add_argument('root'); ap.add_argument('--json-output'); a=ap.parse_args(); root=Path(a.root).resolve(); errors=[]; fam=rows(root/'research/evidence_family_registry.csv'); cases=rows(root/'research/case_registry.csv'); source_family={}
 for r in fam:
  for s in ids(r.get('source_ids')): source_family[s]=r.get('evidence_family_id')
 for r in cases:
  if r.get('case_type')!='evidence-backed': continue
  src=ids(r.get('source_ids')); actual={source_family.get(s,'') for s in src if source_family.get(s,'')}; declared=ids(r.get('evidence_family_ids'))
  if actual!=declared: errors.append(f"{r.get('case_id')}: declared evidence families {sorted(declared)} != mapped {sorted(actual)}")
  if len(actual)<2 and r.get('independence_status')!='approved-single-family-exception': errors.append(f"{r.get('case_id')}: fewer than two independent evidence families")
  if len(r.get('independence_rationale','').strip())<20: errors.append(f"{r.get('case_id')}: independence rationale too short")
 out={'status':'PASS' if not errors else 'FAIL','cases':len(cases),'errors':errors}; txt=json.dumps(out,ensure_ascii=False,indent=2); print(txt); p=Path(a.json_output) if a.json_output else root/'qa/case_independence_validation.json'; p.write_text(txt+'\n',encoding='utf-8'); raise SystemExit(0 if not errors else 1)
if __name__=='__main__': main()
