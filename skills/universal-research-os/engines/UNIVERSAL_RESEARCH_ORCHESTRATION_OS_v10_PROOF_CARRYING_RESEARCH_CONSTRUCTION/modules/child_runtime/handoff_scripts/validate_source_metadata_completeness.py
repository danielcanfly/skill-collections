#!/usr/bin/env python3
from pathlib import Path
import argparse,re,csv
from common import rows,result,emit,load_json,parse_iso

ap=argparse.ArgumentParser(); ap.add_argument('root'); ap.add_argument('--config'); ap.add_argument('--profile'); ap.add_argument('--output'); a=ap.parse_args()
root=Path(a.root); profile=load_json(a.profile,{}) if a.profile else {}; errors=[]; warnings=[]
meta=rows(root/'research/source_metadata_reconciliation.csv'); ident=rows(root/'research/source_identity_verification.csv'); ledger=rows(root/'research/claim_ledger.csv'); edges=rows(root/'research/edge_entailment.csv')
active=set()
for r in meta:
    action=(r.get('action') or '').strip().lower(); status=(r.get('verification_status') or '').strip().lower()
    if action not in {'remove','reject','exclude'} and status in {'verified','corrected','replaced'}: active.add((r.get('source_id') or '').strip())
active|={(r.get('source_id') or '').strip() for r in ledger if (r.get('source_id') or '').strip()}
by={(r.get('source_id') or '').strip():r for r in ident}
mb={(r.get('source_id') or '').strip():r for r in meta}
placeholder={'','unknown','n/a','na','not available','not captured','tbd','pending','unverified','none'}
for sid in sorted(active):
    r=by.get(sid); m=mb.get(sid,{})
    if not r: errors.append(f'{sid}: active source has no identity verification row'); continue
    title=(r.get('observed_title') or '').strip(); authors=(r.get('observed_authors') or r.get('responsible_entity') or '').strip(); publisher=(m.get('verified_publisher') or '').strip()
    if title.lower() in placeholder: errors.append(f'{sid}: observed title missing or placeholder')
    if authors.lower() in placeholder: errors.append(f'{sid}: verified author or responsible organisation missing')
    if publisher.lower() in placeholder: warnings.append(f'{sid}: verified publisher/responsible institution is weak or absent')
    ident_value=(r.get('observed_identifier') or r.get('canonical_url') or m.get('verified_doi_or_url') or '').strip()
    if ident_value.lower() in placeholder: errors.append(f'{sid}: canonical identifier/URL missing')
    if ident_value.startswith('http') and not re.match(r'^https?://[^\s]+$',ident_value): errors.append(f'{sid}: malformed canonical URL')
    locator=(r.get('exact_metadata_locator') or r.get('metadata_locator') or '').strip()
    if locator.lower() in placeholder or re.fullmatch(r'https?://\S+',locator): errors.append(f'{sid}: exact metadata locator missing or URL-only')
    if len((r.get('metadata_excerpt') or '').strip())<15: errors.append(f'{sid}: metadata excerpt too short')
    if not parse_iso(r.get('accessed_at')): errors.append(f'{sid}: accessed_at must be a full ISO date/time')
    if not (r.get('publication_date') or '').strip() and not (r.get('effective_or_period_date') or '').strip(): errors.append(f'{sid}: publication or effective/period date required')
    if (r.get('date_basis') or '').strip().lower() in placeholder: errors.append(f'{sid}: date_basis missing')
    if (r.get('production_eligibility') or '').upper()!='PASS': errors.append(f'{sid}: production_eligibility not PASS')
    if (r.get('identity_status') or '').upper()!='PASS' or (r.get('identity_verdict') or '').upper()!='PASS' or (r.get('temporal_status') or '').upper()!='PASS' or (r.get('reviewer_status') or '').upper()!='PASS': errors.append(f'{sid}: identity/temporal/reviewer status is not fully PASS')

direct_sources={(r.get('source_id') or '').strip() for r in edges if (r.get('support_label') or '').strip()=='support'}
for sid in sorted(direct_sources):
    r=by.get(sid,{})
    if (r.get('access_level') or '').strip().lower() in {'metadata','metadata-only','abstract','abstract-only','preview','snippet','unavailable','unknown',''}: errors.append(f'{sid}: direct-support source lacks full or section-level access')
    if str(r.get('abstract_support_allowed','')).strip().lower()=='true': errors.append(f'{sid}: abstract-support permission cannot coexist with direct support')

# Production strict forbids carrying unresolved source-refresh debt into a sealed production release.
open_refresh=[]
for name in ['source_refresh_queue.csv','residual_source_gaps.csv','source_enrichment_queue.csv']:
    p=root/'research'/name
    if p.exists():
        for row in rows(p):
            status=(row.get('status') or row.get('disposition') or '').strip().lower(); sev=(row.get('severity') or row.get('priority') or 'p2').strip().lower()
            if status not in {'closed','resolved','pass','accepted','waived'}: open_refresh.append((name,row.get('source_id') or row.get('finding_id') or '?',sev))
if not profile.get('allow_open_p2',False) and open_refresh: errors.append(f'open source-refresh/enrichment queue is forbidden in production: {len(open_refresh)} rows')
emit(result('PASS' if not errors else 'FAIL',errors,warnings,{'active_sources':len(active),'identity_rows':len(ident),'direct_support_sources':len(direct_sources),'open_source_refresh_rows':len(open_refresh)}),a.output)
