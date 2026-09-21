#!/usr/bin/env python3
from pathlib import Path
import argparse,re
from common import rows,result,emit,norm
ap=argparse.ArgumentParser();ap.add_argument('root');ap.add_argument('--config');ap.add_argument('--profile');ap.add_argument('--output');a=ap.parse_args();root=Path(a.root)
ident=rows(root/'research/source_identity_verification.csv');meta=rows(root/'research/source_metadata_reconciliation.csv');errors=[];warnings=[]
required=set(['source_id', 'declared_title', 'observed_title', 'title_match_status', 'declared_authors', 'observed_authors', 'author_match_status', 'identifier_type', 'declared_identifier', 'observed_identifier', 'identifier_match_status', 'canonical_url', 'publication_date', 'effective_or_period_date', 'accessed_at', 'date_basis', 'access_level', 'verification_method', 'exact_metadata_locator', 'metadata_excerpt', 'verified_proposition', 'abstract_support_allowed', 'identity_status', 'temporal_status', 'reviewer', 'notes', 'metadata_locator', 'identity_verdict', 'reviewer_status', 'responsible_entity', 'author_basis', 'production_eligibility'])
if not ident: errors.append('missing or empty research/source_identity_verification.csv')
elif not required.issubset(ident[0]): errors.append('source identity columns missing: '+','.join(sorted(required-set(ident[0]))))
by={r.get('source_id','').strip():r for r in ident}
active=[]
for r in meta:
    action=(r.get('action') or '').lower(); ver=(r.get('verification_status') or '').lower()
    if action not in {'remove','reject','exclude'} and ver in {'verified','corrected','replaced'}: active.append(r.get('source_id','').strip())
for sid in active:
    if sid not in by: errors.append(f'{sid}: active governed source missing identity row')
for i,r in enumerate(ident,2):
    sid=r.get('source_id') or f'row {i}'
    for c in required:
        if c in {'declared_identifier','observed_identifier','effective_or_period_date','publication_date','notes','declared_authors','observed_authors','responsible_entity'}: continue
        if not (r.get(c) or '').strip(): errors.append(f'{sid}: empty {c}')
    if (r.get('identity_status') or '').upper()!='PASS' or (r.get('identity_verdict') or '').upper()!='PASS' or (r.get('reviewer_status') or '').upper()!='PASS': errors.append(f'{sid}: individual identity/reviewer not PASS')
    if (r.get('temporal_status') or '').upper()!='PASS': errors.append(f'{sid}: temporal_status not PASS')
    if (r.get('production_eligibility') or '').upper()!='PASS': errors.append(f'{sid}: production_eligibility not PASS')
    if (r.get('author_basis') or '').strip().lower() not in {'named-author','responsible-organisation','official-issuer','dataset-owner','no-named-author-verified'}: errors.append(f'{sid}: invalid author_basis')
    if not (r.get('observed_authors') or '').strip() and not (r.get('responsible_entity') or '').strip(): errors.append(f'{sid}: author/responsible entity missing')

    if norm(r.get('declared_title'))!=norm(r.get('observed_title')): errors.append(f'{sid}: title mismatch')
    di=(r.get('declared_identifier') or '').strip(); oi=(r.get('observed_identifier') or '').strip()
    if di and di!=oi: errors.append(f'{sid}: identifier mismatch')
    loc=(r.get('exact_metadata_locator') or r.get('metadata_locator') or '').strip()
    if not loc or re.fullmatch(r'https?://\S+',loc): errors.append(f'{sid}: metadata locator missing or URL-only')
    pub=(r.get('publication_date') or '').strip(); eff=(r.get('effective_or_period_date') or '').strip(); acc=(r.get('accessed_at') or '').strip()
    if pub and eff and acc and pub==eff==acc and (r.get('date_basis') or '').lower() not in {'same-date-verified','single-date-source'}: errors.append(f'{sid}: publication/effective/access dates appear copied')
    if len((r.get('metadata_excerpt') or '').strip())<15: errors.append(f'{sid}: metadata excerpt too short')
    if len((r.get('verified_proposition') or '').strip())<15: errors.append(f'{sid}: verified proposition too short')
extra=set(by)-set(x for x in active if x)
if extra: warnings.append('identity rows not governed as active: '+','.join(sorted(extra)[:10]))
emit(result('PASS' if not errors else 'FAIL',errors,warnings,{'identity_rows':len(ident),'active_sources':len(active),'individual_pass':sum(1 for r in ident if (r.get('identity_status') or '').upper()=='PASS')}),a.output)
