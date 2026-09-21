#!/usr/bin/env python3
from pathlib import Path
import argparse,csv,json,re,difflib

def rows(p): return list(csv.DictReader(p.open(encoding='utf-8-sig',newline=''))) if p.exists() else []
def norm(s): return re.sub(r'\s+',' ',str(s).strip().lower())
def main():
 ap=argparse.ArgumentParser(); ap.add_argument('root'); ap.add_argument('--json-output'); a=ap.parse_args(); root=Path(a.root).resolve(); errors=[]; ledger=rows(root/'research/claim_ledger.csv'); reg=rows(root/'research/contextual_relevance_register.csv'); active={(r.get('claim_id'),r.get('source_id')) for r in ledger if r.get('support_challenge')=='contextual-support'}; by={(r.get('claim_id'),r.get('source_id')):r for r in reg}; texts=[]
 for key in active:
  r=by.get(key)
  if not r: errors.append(f'{key}: missing contextual relevance row'); continue
  if r.get('reviewer_status')!='PASS': errors.append(f'{key}: reviewer status not PASS')
  for c in ['shared_concept_or_method','source_passage_function','claim_context_function','why_context_not_entailment','transfer_boundary','exact_locator']:
   if len(r.get(c,'').strip())<15: errors.append(f'{key}: {c} too short')
  text=' | '.join(r.get(c,'') for c in ['shared_concept_or_method','source_passage_function','claim_context_function','why_context_not_entailment','transfer_boundary'])
  if re.search(r'denominator\s*[/,].*cohort\s*[/,].*causal\s*[/,].*valuation',text,re.I): errors.append(f'{key}: generic option-list rationale')
  texts.append((key,text))
 for i,(ka,ta) in enumerate(texts):
  for kb,tb in texts[i+1:]:
   sim=difflib.SequenceMatcher(None,norm(ta),norm(tb)).ratio()
   if sim>.82: errors.append(f'{ka}/{kb}: contextual prose similarity {sim:.3f}')
 extra=set(by)-active
 if extra: errors.append('contextual register contains inactive edges: '+str(sorted(extra)[:10]))
 out={'status':'PASS' if not errors else 'FAIL','active_contextual_edges':len(active),'errors':errors}; txt=json.dumps(out,ensure_ascii=False,indent=2); print(txt); p=Path(a.json_output) if a.json_output else root/'qa/contextual_relevance_validation.json'; p.write_text(txt+'\n',encoding='utf-8'); raise SystemExit(0 if not errors else 1)
if __name__=='__main__': main()
