#!/usr/bin/env python3
from pathlib import Path
import argparse,re,hashlib
from common import rows,result,emit,sha256_file,parse_iso
ap=argparse.ArgumentParser();ap.add_argument('root');ap.add_argument('--config');ap.add_argument('--profile');ap.add_argument('--output');a=ap.parse_args();root=Path(a.root);rs=rows(root/'research/source_passage_registry.csv');errors=[];required={'passage_id','source_id','passage_type','excerpt_text','locator_type','locator_value','locator_resolved','snapshot_path','snapshot_sha256','excerpt_sha256','observed_at','candidate_reviewer_status','capture_method','source_access_level','production_eligibility'}
allowed={'page','section','clause','paragraph','table','figure','filing-item','line-range','timestamp','article-heading','api-record','dataset-row'}
seen=set()
if not rs: errors.append('missing or empty research/source_passage_registry.csv')
elif not required.issubset(rs[0]): errors.append('source passage columns missing: '+','.join(sorted(required-set(rs[0]))))
for r in rs:
 pid=r.get('passage_id','').strip(); p=root/(r.get('snapshot_path') or '')
 if not pid or pid in seen: errors.append(f'duplicate/missing passage_id {pid}')
 seen.add(pid)
 if r.get('locator_type') not in allowed: errors.append(f'{pid}: unsupported locator_type')
 lv=(r.get('locator_value') or '').strip()
 if len(lv)<3 or re.search(r'original document section on|proposition section on|official page/pdf title|relevant section|source note',lv,re.I): errors.append(f'{pid}: locator is synthetic or non-resolvable')
 if str(r.get('locator_resolved','')).upper()!='PASS': errors.append(f'{pid}: locator not independently resolved')
 if not p.is_file(): errors.append(f'{pid}: snapshot missing')
 elif sha256_file(p)!=r.get('snapshot_sha256'): errors.append(f'{pid}: snapshot SHA mismatch')
 ex=(r.get('excerpt_text') or '').strip()
 if len(ex)<20: errors.append(f'{pid}: excerpt too short')
 if hashlib.sha256(ex.encode()).hexdigest()!=r.get('excerpt_sha256'): errors.append(f'{pid}: excerpt SHA mismatch')
 if not parse_iso(r.get('observed_at')): errors.append(f'{pid}: observed_at invalid')
 if str(r.get('candidate_reviewer_status','')).upper()!='PASS': errors.append(f'{pid}: candidate reviewer status not PASS')
 if (r.get('production_eligibility') or '').upper()!='PASS': errors.append(f'{pid}: production_eligibility not PASS')
 if (r.get('capture_method') or '').strip().lower() not in {'pdf-page-snapshot','html-section-snapshot','api-record-snapshot','dataset-row-snapshot','filing-section-snapshot','official-text-snapshot'}: errors.append(f'{pid}: invalid capture_method')
 if (r.get('source_access_level') or '').strip().lower() in {'','unknown','metadata-only','abstract-only','preview-only'}: errors.append(f'{pid}: source_access_level insufficient')
emit(result('PASS' if not errors else 'FAIL',errors,stats={'passages':len(rs)}),a.output)
