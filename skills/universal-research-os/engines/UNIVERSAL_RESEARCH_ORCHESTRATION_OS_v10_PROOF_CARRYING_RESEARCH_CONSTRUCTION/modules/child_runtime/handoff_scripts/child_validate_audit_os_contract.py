#!/usr/bin/env python3
from pathlib import Path
import argparse,csv,json,re,hashlib,sys
try: import yaml
except ImportError: raise SystemExit('PyYAML required')
REQ_CLASSES={'definition','comparison','how-to','decision/application','audit','source-provenance','multi-hop','adversarial'}
ALLOWED_SUPPORT={'support','partial-support','contextual-support','challenge'}
META_PHRASES=('this source supports','source directly supports','the source establishes','本來源支持','該來源支持')
NEG_SCOPE=re.compile(r'\b(does not|not establish|cannot establish|not prove|不支持|不能建立|無法證明)\b',re.I)
def jaccard(a,b):
 a=set(re.findall(r'[a-z0-9\u3400-\u9fff]+',a.lower())); b=set(re.findall(r'[a-z0-9\u3400-\u9fff]+',b.lower())); return len(a&b)/max(1,len(a|b))
def fm(p):
 t=p.read_text(encoding='utf-8');
 if not t.startswith('---'): return {},t
 x=t.split('---',2); return (yaml.safe_load(x[1]) or {},x[2]) if len(x)==3 else ({},t)
def sec(body,h):
 m=re.search(rf'## {re.escape(h)}\s*(.*?)(?:\n## |\Z)',body,re.S); return re.sub(r'\s+',' ',m.group(1).strip()) if m else ''
def main():
 ap=argparse.ArgumentParser(); ap.add_argument('root'); ap.add_argument('--json-output'); a=ap.parse_args(); root=Path(a.root).resolve(); errors=[]; warnings=[]
 # Retrieval metadata exact parser compatibility.
 p=root/'qa/retrieval_test_cases.json'; tests=json.loads(p.read_text()) if p.exists() else []
 if isinstance(tests,dict): tests=tests.get('tests',[])
 total=len(tests); hold=sum(bool(t.get('is_holdout') or t.get('holdout')) for t in tests); neg=sum(bool(t.get('negative_ids')) for t in tests); classes={str(t.get('class') or t.get('test_class') or '') for t in tests}
 if total<40: errors.append(f'retrieval total {total}<40')
 if total and hold/total<.25: errors.append(f'holdout {hold}/{total}<25%')
 if total and neg/total<.25: errors.append(f'negative coverage {neg}/{total}<25%')
 missing=sorted(REQ_CLASSES-classes)
 if missing: errors.append('missing retrieval classes: '+', '.join(missing))
 for t in tests:
  if not isinstance(t.get('is_holdout'),bool): errors.append(f"{t.get('test_id')}: is_holdout must be boolean")
  if not isinstance(t.get('holdout'),bool): errors.append(f"{t.get('test_id')}: holdout must be boolean")
 # Auditor queries locked and source bindings complete.
 for name in ['AUDITOR_HOLDOUT_TESTS.json','AUDITOR_SOURCE_PROVENANCE_TESTS.json']:
  q=root/'qa'/name
  if not q.exists(): errors.append(f'missing {q.relative_to(root)}'); continue
  for t in json.loads(q.read_text()):
   if hashlib.sha256(t['query'].encode()).hexdigest()!=t.get('query_sha256'): errors.append(f"{name}:{t.get('test_id')} immutable query hash mismatch")
   if name.startswith('AUDITOR_SOURCE'):
    if len(t.get('primary_source_ids',[]))<int(t.get('minimum_primary_sources',2)): errors.append(f"{t.get('test_id')}: fewer than required primary source bindings")
    if not t.get('secondary_or_practitioner_negative_ids'): errors.append(f"{t.get('test_id')}: missing secondary/practitioner negative binding")
 # Claims and support calibration.
 ledger=root/'research/claim_ledger.csv'; rows=list(csv.DictReader(ledger.open(encoding='utf-8-sig',newline=''))) if ledger.exists() else []
 dist={x:0 for x in ALLOWED_SUPPORT}
 for r in rows:
  cid=r.get('claim_id',''); typ=r.get('support_challenge',''); dist[typ]=dist.get(typ,0)+1
  if typ not in ALLOWED_SUPPORT: errors.append(f'{cid}: invalid support type {typ}')
  if typ=='support' and NEG_SCOPE.search(r.get('scope','')): errors.append(f'{cid}: direct-support scope contains self-contradicting limitation language')
  if any(x in r.get('claim','').lower() for x in META_PHRASES): errors.append(f'{cid}: meta source-support wording is not a durable domain claim')
  if not r.get('subtype','').strip(): errors.append(f'{cid}: missing subtype')
 if len(rows)>=20 and dist.get('support',0)==len(rows): errors.append('all claim-source rows are support')
 if len(rows)>=30 and dist.get('support',0)/len(rows)>.90: errors.append(f'direct-support share too high: {dist.get("support")}/{len(rows)}')
 # Semantic risk lineage exact columns.
 rp=root/'research/topic_semantic_risk_resolution.csv'; risks=list(csv.DictReader(rp.open(encoding='utf-8-sig',newline=''))) if rp.exists() else []
 need={'risk_id','risk','status','claims','sources','resolution','residual_gap'}
 if risks and not need.issubset(risks[0].keys()): errors.append('semantic risk registry missing: '+','.join(sorted(need-set(risks[0].keys()))))
 for r in risks:
  for c in ['claims','sources','resolution','residual_gap','status']:
   if not r.get(c,'').strip(): errors.append(f"{r.get('risk_id')}: empty {c}")
 # Source-note anti-boilerplate.
 blocks=[]; finds=[]
 for q in sorted((root/'knowledge/sources').glob('*.md')):
  meta,b=fm(q); sid=str(meta.get('source_id',q.stem)); lim=sec(b,'What This Source Does Not Establish'); finding=sec(b,'Source-specific Findings')
  if len(lim)<80: errors.append(f'{sid}: limitation section too short/source-generic')
  if len(finding)<100: errors.append(f'{sid}: source-specific findings too short')
  blocks.append((sid,lim)); finds.append((sid,finding))
 for items,label in [(blocks,'limitation'),(finds,'findings')]:
  for i in range(len(items)):
   for j in range(i+1,len(items)):
    if items[i][1] and items[i][1]==items[j][1]: errors.append(f'identical {label} block: {items[i][0]} / {items[j][0]}')
    elif len(items[i][1])>80 and len(items[j][1])>80 and jaccard(items[i][1],items[j][1])>.88: warnings.append(f'highly similar {label}: {items[i][0]} / {items[j][0]}')
 # Unique authoritative merge surface.
 for d in ['concepts','patterns','source-notes','registries','checklists','evaluation','compatibility']:
  if (root/d).exists(): errors.append(f'forbidden duplicate/legacy root surface: {d}/')
 out={'status':'PASS' if not errors and not warnings else ('PASS_WITH_WARNINGS' if not errors else 'FAIL'),'stats':{'retrieval_total':total,'holdout':hold,'negative':neg,'support_distribution':dist,'risks':len(risks),'source_notes':len(blocks)},'errors':errors,'warnings':warnings}; txt=json.dumps(out,ensure_ascii=False,indent=2); print(txt); op=Path(a.json_output) if a.json_output else root/'qa/audit_os_contract_validation.json'; op.write_text(txt+'\n',encoding='utf-8'); raise SystemExit(0 if not errors and not warnings else 1)
if __name__=='__main__': main()
