#!/usr/bin/env python3
from pathlib import Path
import argparse,csv,json,re,datetime
def rows(p): return list(csv.DictReader(p.open(encoding='utf-8-sig',newline=''))) if p.exists() else []
def main():
 ap=argparse.ArgumentParser(); ap.add_argument('root'); ap.add_argument('--json-output'); a=ap.parse_args(); root=Path(a.root).resolve(); errors=[]; ident=rows(root/'research/source_identity_verification.csv')
 for r in ident:
  sid=r.get('source_id'); pub=r.get('publication_date','').strip(); eff=r.get('effective_or_period_date','').strip(); acc=r.get('accessed_at','').strip(); basis=r.get('date_basis','').strip().lower(); typ=(r.get('identifier_type','')+' '+r.get('notes','')).lower()
  if not pub: errors.append(f'{sid}: publication_date must be date/year or n.d.')
  if basis in {'access-date','accessed_at','current-year'}: errors.append(f'{sid}: access date cannot be publication date basis')
  if not acc: errors.append(f'{sid}: accessed_at missing')
  if any(x in typ for x in ['standard','regulation','filing','sec','annual report']) and not eff: errors.append(f'{sid}: effective/reporting date required')
  if pub.lower()!='n.d.' and not re.match(r'^\d{4}(?:-\d{2}(?:-\d{2})?)?$',pub): errors.append(f'{sid}: invalid publication_date {pub}')
  if eff and not re.match(r'^\d{4}(?:-\d{2}(?:-\d{2})?)?$',eff): errors.append(f'{sid}: invalid effective_or_period_date {eff}')
 out={'status':'PASS' if not errors else 'FAIL','rows':len(ident),'errors':errors}; txt=json.dumps(out,ensure_ascii=False,indent=2); print(txt); p=Path(a.json_output) if a.json_output else root/'qa/temporal_metadata_validation.json'; p.write_text(txt+'\n',encoding='utf-8'); raise SystemExit(0 if not errors else 1)
if __name__=='__main__': main()
