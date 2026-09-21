#!/usr/bin/env python3
from pathlib import Path
import argparse,csv,json,re
try: import yaml
except ImportError: raise SystemExit('PyYAML required')
def rows(p): return list(csv.DictReader(p.open(encoding='utf-8-sig',newline=''))) if p.exists() else []
def ids(s): return {x.strip() for x in re.split(r'[;,|]',s or '') if x.strip()}
def fm(p):
 t=p.read_text(encoding='utf-8');
 if not t.startswith('---'): return {},t
 q=t.split('---',2); return (yaml.safe_load(q[1]) or {},q[2]) if len(q)==3 else ({},t)
def main():
 ap=argparse.ArgumentParser(); ap.add_argument('root'); ap.add_argument('--json-output'); a=ap.parse_args(); root=Path(a.root).resolve(); errors=[]
 ledger=rows(root/'research/claim_ledger.csv'); can=rows(root/'research/canonical_concept_registry.csv'); exp=rows(root/'research/expected_node_disposition.csv'); exc=rows(root/'research/node_context_source_exceptions.csv')
 active={}
 for r in ledger: active.setdefault(r.get('candidate_node'),set()).add(r.get('source_id'))
 allowed={}
 for r in exc:
  if r.get('status')=='approved': allowed.setdefault(r.get('node_id'),set()).add(r.get('source_id'))
 canmap={r.get('id'):ids(r.get('source_ids')) for r in can}; expmap={r.get('candidate_id'):ids(r.get('source_ids')) for r in exp}
 nodefm={}
 for p in (root/'knowledge').rglob('*.md'):
  m,b=fm(p); nid=m.get('id')
  if nid: nodefm[str(nid)]={str(x) for x in (m.get('source_ids') or [])}
 nodes=set(active)|set(canmap)|set(expmap)|set(nodefm)
 for n in nodes:
  expected=active.get(n,set())|allowed.get(n,set())
  for label,actual in [('canonical_registry',canmap.get(n,set())),('expected_disposition',expmap.get(n,set())),('node_frontmatter',nodefm.get(n,set()))]:
   if actual!=expected: errors.append(f'{n}: {label} {sorted(actual)} != active+exceptions {sorted(expected)}')
 # source note claims must match ledger edges
 led_by_src={}
 for r in ledger: led_by_src.setdefault(r.get('source_id'),set()).add(r.get('claim_id'))
 for p in (root/'knowledge/sources').glob('*.md'):
  m,b=fm(p); sid=str(m.get('source_id',p.stem)); listed=set(re.findall(r'`(C\d+[A-Z]?)`',b)); missing=led_by_src.get(sid,set())-listed
  if missing: errors.append(f'{sid}: source note missing active claim IDs {sorted(missing)}')
 out={'status':'PASS' if not errors else 'FAIL','nodes_checked':len(nodes),'errors':errors}; txt=json.dumps(out,ensure_ascii=False,indent=2); print(txt); p=Path(a.json_output) if a.json_output else root/'qa/lineage_cascade_validation.json'; p.write_text(txt+'\n',encoding='utf-8'); raise SystemExit(0 if not errors else 1)
if __name__=='__main__': main()
