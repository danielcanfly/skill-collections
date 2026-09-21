#!/usr/bin/env python3
from pathlib import Path
import argparse,re
from common import rows,result,emit,load_json,norm

ap=argparse.ArgumentParser(); ap.add_argument('root'); ap.add_argument('--config'); ap.add_argument('--profile'); ap.add_argument('--output'); a=ap.parse_args()
root=Path(a.root); profile=load_json(a.profile,{}) if a.profile else {}; errors=[]; warnings=[]
ledger=rows(root/'research/claim_ledger.csv'); edges=rows(root/'research/edge_entailment.csv'); passages=rows(root/'research/source_passage_registry.csv'); identities=rows(root/'research/source_identity_verification.csv')
if not ledger: errors.append('missing or empty research/claim_ledger.csv')
if not edges: errors.append('missing or empty research/edge_entailment.csv')
if not passages: errors.append('missing or empty research/source_passage_registry.csv')

placeholder=re.compile(r'(not[- ]captured|source[- ]?note|package lineage|summary[- ]only|abstract[- ]only|metadata[- ]only|relevant section|official page/pdf title|bounded source proposition|cited section documents)',re.I)

def key(r): return ((r.get('claim_id') or '').strip(),(r.get('source_id') or '').strip())

def duplicates(rs):
    seen=set(); dup=[]
    for r in rs:
        k=key(r)
        if not all(k): dup.append(k); continue
        if k in seen: dup.append(k)
        seen.add(k)
    return dup

for k in duplicates(ledger): errors.append(f'duplicate or missing atomic claim-source ledger pair {k}')
for k in duplicates(edges): errors.append(f'duplicate or missing edge entailment pair {k}')
ledger_by={key(r):r for r in ledger if all(key(r))}; edge_by={key(r):r for r in edges if all(key(r))}; passage_by={(r.get('passage_id') or '').strip():r for r in passages}; identity_by={(r.get('source_id') or '').strip():r for r in identities}
for k in sorted(set(ledger_by)-set(edge_by)): errors.append(f'{k}: active atomic edge has no entailment row')
for k in sorted(set(edge_by)-set(ledger_by)): errors.append(f'{k}: stale entailment row has no active ledger edge')

allowed_labels={'support','partial-support','contextual-support','challenge'}; direct=partial=contextual=challenge=0
for k,e in edge_by.items():
    lab=(e.get('support_label') or '').strip(); pid=(e.get('passage_id') or '').strip(); p=passage_by.get(pid); src=k[1]
    if lab not in allowed_labels: errors.append(f'{k}: invalid support label {lab!r}'); continue
    if not p: errors.append(f'{k}: passage_id {pid!r} missing from source passage registry'); continue
    if (p.get('source_id') or '').strip()!=src: errors.append(f'{k}: passage source_id does not match edge source_id')
    excerpt=(p.get('excerpt_text') or '').strip(); edge_excerpt=(e.get('exact_source_passage') or '').strip(); loc=(e.get('exact_locator') or p.get('locator_value') or '').strip()
    if len(excerpt)<20 or len(edge_excerpt)<20: errors.append(f'{k}: evidence passage too short')
    if norm(excerpt)!=norm(edge_excerpt): errors.append(f'{k}: edge passage differs from immutable passage registry')
    if not loc or re.fullmatch(r'https?://\S+',loc) or placeholder.search(loc): errors.append(f'{k}: locator is missing, URL-only, synthetic or non-resolvable')
    if placeholder.search(excerpt) or placeholder.search(edge_excerpt): errors.append(f'{k}: evidence is a placeholder, package summary or circular source-note text')
    snap=root/(p.get('snapshot_path') or '')
    if not snap.is_file(): errors.append(f'{k}: immutable source snapshot is missing')
    if (p.get('production_eligibility') or '').upper()!='PASS': errors.append(f'{k}: passage production_eligibility is not PASS')
    if (p.get('source_access_level') or '').strip().lower() in {'','unknown','metadata-only','abstract-only','preview-only'}: errors.append(f'{k}: passage access level insufficient')
    if str(p.get('locator_resolved','')).upper()!='PASS': errors.append(f'{k}: passage locator was not resolved')
    if str(p.get('candidate_reviewer_status','')).upper()!='PASS' or str(e.get('candidate_reviewer_status','')).upper()!='PASS': errors.append(f'{k}: candidate evidence review is not PASS')
    try: cov=float(e.get('coverage_ratio',''))
    except Exception: cov=-1
    boundary=(e.get('evidence_boundary') or '').strip()
    ident=identity_by.get(src,{})
    access=(ident.get('access_level') or '').strip().lower()
    if lab=='support':
        direct+=1
        if (e.get('evidence_origin') or '').strip()!='original-source-snapshot': errors.append(f'{k}: direct support must originate from original-source-snapshot')
        if cov!=1: errors.append(f'{k}: direct support coverage must equal 1')
        if boundary not in {'VERIFIED_EXACT_SPAN','VERIFIED_SECTION_LOCATOR'}: errors.append(f'{k}: direct support requires verified exact-span or section locator')
        if access in {'metadata','metadata-only','abstract','abstract-only','preview','snippet','unavailable','unknown'}: errors.append(f'{k}: direct support cannot rely on {access or "unknown"} access')
    elif lab=='partial-support':
        partial+=1
        if not 0<cov<1: errors.append(f'{k}: partial-support coverage must be between 0 and 1')
        if not (e.get('unsupported_remainder') or '').strip() or (e.get('unsupported_remainder') or '').strip().lower() in {'none','n/a'}: errors.append(f'{k}: partial support must disclose unsupported remainder')
    elif lab=='contextual-support':
        contextual+=1
        if cov!=0: errors.append(f'{k}: contextual support coverage must equal 0')
    else:
        challenge+=1
        if len((e.get('challenge_description') or '').strip())<20: errors.append(f'{k}: challenge requires a source-specific description')

if len(edge_by)!=len(ledger_by): errors.append(f'atomic edge population mismatch ledger={len(ledger_by)} entailment={len(edge_by)}')
if profile.get('require_all_edges_passage_bound',True) and len(edge_by)!=sum(1 for e in edge_by.values() if (e.get('passage_id') or '').strip() in passage_by): errors.append('not every active edge is bound to a governed source passage')
emit(result('PASS' if not errors else 'FAIL',errors,warnings,{'active_atomic_edges':len(ledger_by),'passage_bound_edges':len(edge_by),'direct':direct,'partial':partial,'contextual':contextual,'challenge':challenge}),a.output)
