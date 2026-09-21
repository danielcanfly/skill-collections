#!/usr/bin/env python3
from pathlib import Path
import argparse,csv,json,re,difflib

def rr(p): return list(csv.DictReader(p.open(encoding='utf-8-sig',newline=''))) if p.exists() else []
def norm(s): return re.sub(r'\s+',' ',str(s).strip().lower())
def main():
 ap=argparse.ArgumentParser(); ap.add_argument('root'); ap.add_argument('--json-output'); a=ap.parse_args(); root=Path(a.root).resolve(); errors=[]; warnings=[]
 ledger=rr(root/'research/claim_ledger.csv'); ent=rr(root/'research/edge_entailment.csv'); by={(r.get('claim_id'),r.get('source_id')):r for r in ent}; seen=set(); ctx=[]
 need={'edge_id','claim_id','source_id','candidate_node','support_label','claim_atomicity_status','passage_type','exact_source_passage','exact_locator','coverage_ratio','supported_subset','unsupported_remainder','shared_contextual_concept','source_passage_function','claim_context_function','why_context_not_entailment','transfer_boundary','challenge_description','disposition','reviewer_status','notes'}
 if ent and not need.issubset(ent[0]): errors.append('entailment registry missing columns: '+','.join(sorted(need-set(ent[0]))))
 for l in ledger:
  key=(l.get('claim_id'),l.get('source_id')); r=by.get(key)
  if not r: errors.append(f'{key}: missing entailment row'); continue
  if key in seen: errors.append(f'{key}: duplicate entailment row')
  seen.add(key)
  if r.get('support_label')!=l.get('support_challenge'): errors.append(f'{key}: support label mismatch')
  if r.get('candidate_node')!=l.get('candidate_node'): errors.append(f'{key}: candidate node mismatch')
  if r.get('claim_atomicity_status')!='PASS': errors.append(f'{key}: atomicity not PASS')
  if r.get('reviewer_status')!='PASS': errors.append(f'{key}: reviewer status not PASS')
  if r.get('disposition') not in {'keep','relabel','split'}: errors.append(f'{key}: invalid final disposition')
  passage=r.get('exact_source_passage','').strip(); loc=r.get('exact_locator','').strip(); label=r.get('support_label')
  if len(passage)<20: errors.append(f'{key}: source passage too short')
  if re.fullmatch(r'https?://\S+',loc): errors.append(f'{key}: URL-only locator')
  if not loc: errors.append(f'{key}: missing locator')
  if norm(passage)==norm(l.get('claim')) and r.get('passage_type')!='verbatim-quote': errors.append(f'{key}: claim copied as source passage')
  try: cov=float(r.get('coverage_ratio',''))
  except: cov=-1; errors.append(f'{key}: invalid coverage_ratio')
  unsupported=r.get('unsupported_remainder','').strip().lower()
  if label=='support':
   if cov!=1.0: errors.append(f'{key}: support coverage must equal 1.0')
   if unsupported not in {'','none','n/a','not applicable'}: errors.append(f'{key}: support has unsupported remainder')
  elif label=='partial-support':
   if not (0<cov<1): errors.append(f'{key}: partial coverage must be between 0 and 1')
   if unsupported in {'','none','n/a'}: errors.append(f'{key}: partial support missing unsupported remainder')
   if not r.get('supported_subset','').strip(): errors.append(f'{key}: partial support missing supported subset')
  elif label=='contextual-support':
   if cov!=0: errors.append(f'{key}: contextual coverage must equal 0')
   for c in ['shared_contextual_concept','source_passage_function','claim_context_function','why_context_not_entailment','transfer_boundary']:
    if len(r.get(c,'').strip())<15: errors.append(f'{key}: contextual {c} too vague')
   ctx.append((key,' | '.join(r.get(c,'') for c in ['shared_contextual_concept','source_passage_function','claim_context_function','why_context_not_entailment','transfer_boundary'])))
  elif label=='challenge':
   if len(r.get('challenge_description','').strip())<20: errors.append(f'{key}: challenge description too short')
 for i,(ka,ta) in enumerate(ctx):
  for kb,tb in ctx[i+1:]:
   sim=difflib.SequenceMatcher(None,norm(ta),norm(tb)).ratio()
   if sim>.82: errors.append(f'contextual rationale too similar {ka} / {kb}: {sim:.3f}')
 extra=set(by)-{(r.get('claim_id'),r.get('source_id')) for r in ledger}
 if extra: warnings.append('entailment rows without active ledger edge: '+str(sorted(extra)[:10]))
 out={'status':'PASS' if not errors and not warnings else ('PASS_WITH_WARNINGS' if not errors else 'FAIL'),'active_edges':len(ledger),'entailment_rows':len(ent),'errors':errors,'warnings':warnings}; txt=json.dumps(out,ensure_ascii=False,indent=2); print(txt); p=Path(a.json_output) if a.json_output else root/'qa/edge_entailment_validation.json'; p.write_text(txt+'\n',encoding='utf-8'); raise SystemExit(0 if not errors and not warnings else 1)
if __name__=='__main__': main()
