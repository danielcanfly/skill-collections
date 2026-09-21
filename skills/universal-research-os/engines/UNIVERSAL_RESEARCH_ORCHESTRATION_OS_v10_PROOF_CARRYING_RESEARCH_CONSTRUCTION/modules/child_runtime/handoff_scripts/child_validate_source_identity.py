#!/usr/bin/env python3
from pathlib import Path
import argparse,csv,json,re,difflib

def rows(p): return list(csv.DictReader(p.open(encoding='utf-8-sig',newline=''))) if p.exists() else []
def norm(s): return re.sub(r'[^a-z0-9]+',' ',str(s).lower()).strip()
def main():
 ap=argparse.ArgumentParser(); ap.add_argument('root'); ap.add_argument('--json-output'); a=ap.parse_args(); root=Path(a.root).resolve(); errors=[]; warnings=[]
 meta=rows(root/'research/source_metadata_reconciliation.csv'); ident=rows(root/'research/source_identity_verification.csv'); ledger=rows(root/'research/claim_ledger.csv')
 by={r.get('source_id','').strip():r for r in ident}; active=[r for r in meta if (r.get('action','').lower() not in {'remove','reject','exclude'}) and r.get('verification_status','').lower() in {'verified','corrected','replaced'}]
 support_sources={r.get('source_id') for r in ledger if r.get('support_challenge')=='support'}
 need={'source_id','declared_title','observed_title','declared_authors','observed_authors','declared_identifier','observed_identifier','metadata_locator','metadata_excerpt','verified_proposition','identity_verdict','reviewer_status','exact_metadata_locator','identity_status','reviewer'}
 if ident and not need.issubset(ident[0]): errors.append('source_identity_verification missing canonical columns: '+','.join(sorted(need-set(ident[0]))))
 for m in active:
  sid=m.get('source_id','').strip(); r=by.get(sid)
  if not r: errors.append(f'{sid}: missing source identity verification row'); continue
  for c in ['declared_title','observed_title','canonical_url','metadata_locator','metadata_excerpt','verified_proposition','verification_method','reviewer','reviewer_status']:
   if not r.get(c,'').strip(): errors.append(f'{sid}: empty {c}')
  if r.get('identity_status')!='PASS' or r.get('identity_verdict')!='PASS': errors.append(f'{sid}: identity status/verdict must both be PASS')
  if r.get('reviewer_status')!='PASS': errors.append(f'{sid}: reviewer_status must be PASS')
  if r.get('temporal_status')!='PASS': errors.append(f'{sid}: temporal_status must be PASS')
  if r.get('metadata_locator')!=r.get('exact_metadata_locator'): errors.append(f'{sid}: metadata locator aliases diverge')
  sim=difflib.SequenceMatcher(None,norm(r.get('declared_title')),norm(r.get('observed_title'))).ratio()
  if sim<0.72: errors.append(f'{sid}: declared/observed title similarity too low ({sim:.2f})')
  loc=r.get('metadata_locator','').strip()
  if re.fullmatch(r'https?://\S+',loc): errors.append(f'{sid}: URL-only metadata locator')
  if len(r.get('metadata_excerpt','').strip())<20: errors.append(f'{sid}: metadata excerpt too short')
  access=r.get('access_level','').lower()
  if sid in support_sources and access in {'landing-page-only','snippet-only','inaccessible'}: errors.append(f'{sid}: direct support from insufficient access level {access}')
  if sid in support_sources and access=='abstract-only' and r.get('abstract_support_allowed','').lower()!='true': errors.append(f'{sid}: abstract-only direct support lacks explicit allowance')
 extra=sorted(set(by)-{r.get('source_id','').strip() for r in meta})
 if extra: warnings.append('identity rows without metadata rows: '+','.join(extra[:10]))
 out={'status':'PASS' if not errors and not warnings else ('PASS_WITH_WARNINGS' if not errors else 'FAIL'),'accepted_sources':len(active),'identity_rows':len(ident),'errors':errors,'warnings':warnings}; txt=json.dumps(out,ensure_ascii=False,indent=2); print(txt); p=Path(a.json_output) if a.json_output else root/'qa/source_identity_validation.json'; p.write_text(txt+'\n',encoding='utf-8'); raise SystemExit(0 if not errors and not warnings else 1)
if __name__=='__main__': main()
