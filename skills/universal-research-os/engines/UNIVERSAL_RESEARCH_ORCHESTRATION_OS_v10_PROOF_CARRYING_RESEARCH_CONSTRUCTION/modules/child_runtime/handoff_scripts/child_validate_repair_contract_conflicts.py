#!/usr/bin/env python3
from pathlib import Path
import argparse,json,fnmatch
def main():
 ap=argparse.ArgumentParser(); ap.add_argument('root'); ap.add_argument('--json-output'); a=ap.parse_args(); root=Path(a.root).resolve(); p=root/'qa/repair_scope.json'; errors=[]
 d=json.loads(p.read_text()) if p.exists() else {'mode':'initial-build','mutable_paths':['**'],'immutable_paths':[]}
 mut=d.get('mutable_paths',[]); imm=d.get('immutable_paths',[])
 if d.get('mode')=='repair':
  for m in mut:
   for i in imm:
    if m==i or m.startswith(i.rstrip('*')) or i.startswith(m.rstrip('*')): errors.append(f'overlapping mutable/immutable scope: {m} / {i}')
 out={'status':'PASS' if not errors else 'FAIL','mode':d.get('mode'),'errors':errors}; txt=json.dumps(out,indent=2); print(txt); q=Path(a.json_output) if a.json_output else root/'qa/repair_contract_conflict_validation.json'; q.write_text(txt+'\n'); raise SystemExit(0 if not errors else 1)
if __name__=='__main__': main()
