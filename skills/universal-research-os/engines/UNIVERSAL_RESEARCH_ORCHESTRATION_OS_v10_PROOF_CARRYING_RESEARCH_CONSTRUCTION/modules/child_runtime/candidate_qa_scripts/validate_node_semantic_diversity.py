#!/usr/bin/env python3
from pathlib import Path
import argparse,json,re,difflib
try: import yaml
except ImportError: raise SystemExit('PyYAML required')
def body(p):
 t=p.read_text(encoding='utf-8');
 if t.startswith('---') and len(t.split('---',2))==3: t=t.split('---',2)[2]
 t=re.sub(r'^#{1,6} .*$', ' ', t, flags=re.M); t=re.sub(r'`[^`]+`',' ',t); t=re.sub(r'\s+',' ',t.lower()); return t.strip()
def main():
 ap=argparse.ArgumentParser(); ap.add_argument('root'); ap.add_argument('--json-output'); a=ap.parse_args(); root=Path(a.root).resolve(); cfg=json.loads((root/'audit_config.json').read_text()); threshold=float(cfg.get('max_node_similarity',.88)); errors=[]; warnings=[]; docs=[]
 for p in sorted((root/'knowledge').rglob('*.md')):
  if 'sources' in p.parts: continue
  t=body(p)
  if len(t)<250: errors.append(f'{p.relative_to(root)}: substantive text too short')
  docs.append((p,t))
 maxpair=None
 for i,(pa,ta) in enumerate(docs):
  for pb,tb in docs[i+1:]:
   sim=difflib.SequenceMatcher(None,ta,tb).ratio()
   if not maxpair or sim>maxpair[0]: maxpair=(sim,str(pa.relative_to(root)),str(pb.relative_to(root)))
   if sim>=threshold: errors.append(f'node similarity {sim:.3f} >= {threshold}: {pa.relative_to(root)} / {pb.relative_to(root)}')
 out={'status':'PASS' if not errors else 'FAIL','threshold':threshold,'documents':len(docs),'maximum_pair':maxpair,'errors':errors,'warnings':warnings}; txt=json.dumps(out,ensure_ascii=False,indent=2); print(txt); p=Path(a.json_output) if a.json_output else root/'qa/node_semantic_diversity_validation.json'; p.write_text(txt+'\n',encoding='utf-8'); raise SystemExit(0 if not errors else 1)
if __name__=='__main__': main()
