#!/usr/bin/env python3
"""Independent auditor holdout runner. Queries are locked by SHA; do not edit to force a pass."""
from pathlib import Path
import argparse, hashlib, json, math, re, unicodedata, sys
try: import yaml
except ImportError as e: raise SystemExit("PyYAML required: python -m pip install pyyaml") from e
CONFIG={"k1":1.2,"b":0.75,"weights":{"title":6.0,"aliases":4.5,"summary":2.5,"body":1.0,"identifier":3.0},"phrase_bonus":5.0,"top_k":10}
def locate(p):
 p=Path(p).resolve()
 if (p/'knowledge').is_dir(): return p
 ds=[x for x in p.iterdir() if x.is_dir() and (x/'knowledge').is_dir()]
 if len(ds)==1:return ds[0]
 raise SystemExit('Could not locate candidate root')
def fm(path):
 t=path.read_text(encoding='utf-8')
 if not t.startswith('---'): return {},t
 a=t.split('---',2); return (yaml.safe_load(a[1]) or {},a[2]) if len(a)==3 else ({},t)
def toks(x):
 s=unicodedata.normalize('NFKC',str(x)).lower(); out=re.findall(r"[a-z0-9]+(?:[-'][a-z0-9]+)*",s)
 for run in re.findall(r'[\u3400-\u9fff]+',s): out+=list(run)+[run[i:i+2] for i in range(len(run)-1)]
 return out
def summary(body):
 m=re.search(r"## (?:定義|Context|Problem|Source-specific Findings)\s*(.*?)(?:\n## |\Z)",body,re.S)
 return m.group(1).strip() if m else body[:1000]
def load(root):
 docs=[]
 for p in sorted((root/'knowledge').rglob('*.md')):
  meta,b=fm(p); did=meta.get('id') or meta.get('source_id')
  if not did: continue
  aliases=meta.get('aliases') or []; aliases=[aliases] if isinstance(aliases,str) else aliases
  dt='source' if meta.get('source_id') else meta.get('x-kos-kind','node')
  docs.append({'id':str(did),'title':meta.get('title',''),'aliases':aliases,'doc_type':dt,'path':p.relative_to(root).as_posix(),'fields':{'title':meta.get('title',''),'aliases':' '.join(map(str,aliases)),'summary':summary(b),'body':b,'identifier':str(did).replace('/',' ').replace('-',' ')}})
 return docs
def rank(q,docs,qclass):
 qt=toks(q); N=len(docs); dfs={}; fts=[]
 for d in docs:
  ft={k:toks(v) for k,v in d['fields'].items()}; fts.append(ft)
  for t in set(z for xs in ft.values() for z in xs): dfs[t]=dfs.get(t,0)+1
 av={k:sum(len(ft[k]) for ft in fts)/max(N,1) for k in CONFIG['weights']}; scored=[]; qn=unicodedata.normalize('NFKC',q).lower()
 for d,ft in zip(docs,fts):
  sc=0.0
  for field,w in CONFIG['weights'].items():
   c={}
   for t in ft[field]: c[t]=c.get(t,0)+1
   dl=len(ft[field]) or 1
   for t in qt:
    tf=c.get(t,0)
    if not tf: continue
    idf=math.log(1+(N-dfs.get(t,0)+.5)/(dfs.get(t,0)+.5)); den=tf+CONFIG['k1']*(1-CONFIG['b']+CONFIG['b']*dl/max(av[field],1))
    sc+=w*idf*(tf*(CONFIG['k1']+1)/den)
  title=unicodedata.normalize('NFKC',str(d['title'])).lower(); als=[unicodedata.normalize('NFKC',str(a)).lower() for a in d['aliases']]
  if title and title in qn: sc+=CONFIG['phrase_bonus']
  if any(a and a in qn for a in als): sc+=CONFIG['phrase_bonus']
  if qclass=='source-provenance': sc+=28 if d['doc_type']=='source' else -6
  else:
   sc+=20 if d['doc_type']!='source' else 0
   if qclass=='audit' and d['doc_type']=='checklist': sc+=12
   if qclass in {'how-to','decision/application'} and d['doc_type'] in {'checklist','pattern'}: sc+=5
  scored.append((sc,d))
 return sorted(scored,key=lambda x:(-x[0],x[1]['id']))
def verify_query(t):
 return hashlib.sha256(t['query'].encode()).hexdigest()==t.get('query_sha256') if t.get('query_sha256') else True
def main():
 ap=argparse.ArgumentParser(); ap.add_argument('candidate'); ap.add_argument('--tests'); ap.add_argument('--source-tests'); ap.add_argument('--output'); a=ap.parse_args()
 root=locate(a.candidate); tests_path=Path(a.tests) if a.tests else root/'qa'/'AUDITOR_HOLDOUT_TESTS.json'; source_path=Path(a.source_tests) if a.source_tests else root/'qa'/'AUDITOR_SOURCE_PROVENANCE_TESTS.json'
 tests=json.loads(tests_path.read_text()); stests=json.loads(source_path.read_text()) if source_path.exists() else []; docs=load(root); results=[]; passed=0
 for t in tests:
  if not verify_query(t): results.append({**t,'status':'FAIL','reason':'immutable query hash mismatch'}); continue
  top=rank(t['query'],docs,t['class'])[:10]; ids=[d['id'] for _,d in top]; ranks={e:(ids.index(e)+1 if e in ids else None) for e in t['expected_ids']}; primary=ranks.get(t['expected_ids'][0]); neg_ok=all((n not in ids) or (primary is not None and ids.index(n)+1>primary) for n in t.get('negative_ids',[])); ok=all(v is not None for v in ranks.values()) and primary is not None and primary<=5 and neg_ok
  passed+=int(ok); results.append({**t,'status':'PASS' if ok else 'FAIL','ranks':ranks,'negative_ok':neg_ok,'top10':ids})
 for t in stests:
  if not verify_query(t): results.append({**t,'status':'FAIL','reason':'immutable query hash mismatch'}); continue
  prim=t.get('primary_source_ids',[]); neg=t.get('secondary_or_practitioner_negative_ids',[])
  if len(prim)<int(t.get('minimum_primary_sources',2)) or not neg:
   results.append({**t,'status':'FAIL','reason':'source-provenance bindings incomplete'}); continue
  top=rank(t['query'],docs,'source-provenance')[:10]; ids=[d['id'] for _,d in top]; ranks={e:(ids.index(e)+1 if e in ids else None) for e in prim}; before=all(p in ids and all(n not in ids or ids.index(p)<ids.index(n) for n in neg) for p in prim); ok=all(v is not None and v<=5 for v in ranks.values()) and before
  passed+=int(ok); results.append({**t,'status':'PASS' if ok else 'FAIL','ranks':ranks,'rank_before_ok':before,'top10':ids})
 total=len(tests)+len(stests); out={'summary':{'total':total,'passed':passed,'failed':total-passed},'results':results}; op=Path(a.output) if a.output else root/'qa'/'auditor_holdout_results.json'; op.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8'); print(json.dumps(out['summary'],ensure_ascii=False)); raise SystemExit(0 if passed==total else 1)
if __name__=='__main__': main()
