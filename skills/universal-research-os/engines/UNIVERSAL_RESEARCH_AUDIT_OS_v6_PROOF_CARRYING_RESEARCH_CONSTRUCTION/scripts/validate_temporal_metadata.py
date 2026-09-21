#!/usr/bin/env python3
from pathlib import Path
import argparse
from common import rows,result,emit
ap=argparse.ArgumentParser();ap.add_argument('root');ap.add_argument('--config');ap.add_argument('--profile');ap.add_argument('--output');a=ap.parse_args();root=Path(a.root);rs=rows(root/'research/source_identity_verification.csv');errors=[]
for r in rs:
    sid=r.get('source_id');pub=(r.get('publication_date') or '').strip();eff=(r.get('effective_or_period_date') or '').strip();acc=(r.get('accessed_at') or '').strip();basis=(r.get('date_basis') or '').lower()
    if not acc: errors.append(f'{sid}: accessed_at missing')
    if pub and eff and acc and pub==eff==acc and basis not in {'same-date-verified','single-date-source'}: errors.append(f'{sid}: publication/effective/access copied')
    if pub.lower() in {'unknown','n/a','na'}: errors.append(f'{sid}: unknown publication date must use n.d.')
    if (r.get('temporal_status') or '').upper()!='PASS': errors.append(f'{sid}: temporal status not PASS')
emit(result('PASS' if not errors else 'FAIL',errors,stats={'sources':len(rs)}),a.output)
