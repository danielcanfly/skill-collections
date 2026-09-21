#!/usr/bin/env python3
from pathlib import Path
import argparse,re,difflib
from common import rows,result,emit,norm,token_containment
ap=argparse.ArgumentParser();ap.add_argument('root');ap.add_argument('--config');ap.add_argument('--profile');ap.add_argument('--output');a=ap.parse_args();root=Path(a.root)
ents=rows(root/'research/edge_entailment.csv');ledger=rows(root/'research/claim_ledger.csv');passages=rows(root/'research/source_passage_registry.csv');errors=[];warnings=[]
required={'edge_id','claim_id','source_id','candidate_node','support_label','claim_atomicity_status','passage_id','passage_type','evidence_boundary','exact_source_passage','exact_locator','coverage_ratio','supported_subset','unsupported_remainder','shared_contextual_concept','shared_concept_or_method','source_passage_function','claim_context_function','why_context_not_entailment','transfer_boundary','challenge_description','disposition','candidate_reviewer_status','notes','evidence_origin'}
if not ents: errors.append('missing or empty research/edge_entailment.csv')
elif not required.issubset(ents[0]): errors.append('edge entailment columns missing: '+','.join(sorted(required-set(ents[0]))))
pby={r.get('passage_id',''):r for r in passages}; by={};ctx=[];direct=0
for r in ents:
 k=(r.get('claim_id','').strip(),r.get('source_id','').strip());by[k]=r
for l in ledger:
 k=(l.get('claim_id','').strip(),l.get('source_id','').strip());r=by.get(k)
 if not r: errors.append(f'{k}: active edge missing entailment');continue
 lab=r.get('support_label','').strip();claim=(l.get('claim') or '').strip();passage=(r.get('exact_source_passage') or '').strip();loc=(r.get('exact_locator') or '').strip();pid=r.get('passage_id','').strip()
 if pid not in pby: errors.append(f'{k}: passage_id not in source passage registry')
 elif norm(pby[pid].get('excerpt_text'))!=norm(passage): errors.append(f'{k}: edge passage differs from immutable passage registry')
 if lab!=l.get('support_challenge','').strip(): errors.append(f'{k}: support label mismatch')
 if str(r.get('candidate_reviewer_status','')).upper()!='PASS': errors.append(f'{k}: candidate reviewer status not PASS')
 if str(r.get('claim_atomicity_status','')).upper()!='PASS': errors.append(f'{k}: atomicity not PASS')
 if len(passage)<20: errors.append(f'{k}: passage too short')
 if not loc or re.fullmatch(r'https?://\S+',loc): errors.append(f'{k}: locator invalid')
 ratio=difflib.SequenceMatcher(None,norm(claim),norm(passage)).ratio();contain=token_containment(claim,passage)
 wrappers=re.search(r'(bounded source proposition|cited section documents|source establishes the proposition|documents the bounded proposition|supports the claim that)',passage,re.I)
 if norm(claim)==norm(passage) or ratio>.88 or (wrappers and contain>.55): errors.append(f'{k}: claim-derived/circular passage detected ratio={ratio:.3f} containment={contain:.3f}')
 if re.search(r'source[- ]?note|as recorded|本來源筆記',passage,re.I): errors.append(f'{k}: source-note circular evidence')
 try: cov=float(r.get('coverage_ratio',''))
 except: cov=-1;errors.append(f'{k}: invalid coverage_ratio')
 rem=(r.get('unsupported_remainder') or '').strip().lower()
 if lab=='support':
  direct+=1
  if (r.get('evidence_origin') or '').strip()!='original-source-snapshot': errors.append(f'{k}: direct support evidence_origin must be original-source-snapshot')
  if cov!=1 or rem not in {'','none','n/a','not applicable'}: errors.append(f'{k}: direct support not full')
  if r.get('evidence_boundary') not in {'VERIFIED_EXACT_SPAN','VERIFIED_SECTION_LOCATOR'}: errors.append(f'{k}: direct support requires exact/section verified boundary')
 elif lab=='partial-support':
  if not 0<cov<1 or rem in {'','none','n/a'}: errors.append(f'{k}: partial support invalid')
 elif lab=='contextual-support':
  if cov!=0: errors.append(f'{k}: contextual coverage must be zero')
  text=' | '.join(r.get(c,'') for c in ['shared_concept_or_method','source_passage_function','claim_context_function','why_context_not_entailment','transfer_boundary']);ctx.append((k,text))
 elif lab=='challenge':
  if len((r.get('challenge_description') or '').strip())<20: errors.append(f'{k}: challenge description too short')
 else: errors.append(f'{k}: invalid support label')
for i,(ka,ta) in enumerate(ctx):
 for kb,tb in ctx[i+1:]:
  q=difflib.SequenceMatcher(None,norm(ta),norm(tb)).ratio()
  if q>.82: errors.append(f'contextual rationale template similarity {q:.3f}: {ka}/{kb}')
if len(ledger)>=30 and direct/len(ledger)>.85: errors.append(f'direct-support saturation {direct}/{len(ledger)} requires independent recalibration')
emit(result('PASS' if not errors else 'FAIL',errors,warnings,{'active_edges':len(ledger),'direct_support':direct}),a.output)
