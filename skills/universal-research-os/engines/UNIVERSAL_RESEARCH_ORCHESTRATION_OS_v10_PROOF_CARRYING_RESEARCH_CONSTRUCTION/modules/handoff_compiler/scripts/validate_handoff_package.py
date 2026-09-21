#!/usr/bin/env python3
from pathlib import Path
import argparse,json,hashlib,sys
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def main():
 a=argparse.ArgumentParser();a.add_argument('root');x=a.parse_args();r=Path(x.root);req=['00_PASTE_THIS_PROMPT_FIRST.txt','HANDOFF_IDENTITY.json','manifest.json','SHA256SUMS.txt','PACKAGE_VALIDATION.json','TARGET_IDENTITY.json','ALLOWED_CHANGE_MATRIX.csv','REQUIRED_OUTPUTS_AND_ACCEPTANCE.json','INDEPENDENCE_STATE_MACHINE.json','SOURCE_INPUT_REGISTRY.json','PROTECTED_SURFACE_BASELINE.json','PACKAGE_VALIDATION.json','GATE0_RESPONSE.json','tools/inspect_inputs.py','tools/compare_protected_surfaces.py','tools/validate_handoff_package.py','tools/validate_return_inventory.py'];e=[]
 for q in req:
  if not (r/q).is_file():e.append('missing '+q)
 m=json.loads((r/'manifest.json').read_text()) if (r/'manifest.json').exists() else {'entries':[]};expected={q['path'] for q in m.get('entries',[])};actual={p.relative_to(r).as_posix() for p in r.rglob('*') if p.is_file() and p.relative_to(r).as_posix() not in {'manifest.json','SHA256SUMS.txt'}}
 if expected!=actual:e.append('manifest exact coverage mismatch')
 for q in m.get('entries',[]):
  p=r/q['path']
  if not p.is_file() or sha(p)!=q['sha256']:e.append('manifest mismatch '+q['path'])
 o={'status':'PASS' if not e else 'FAIL','errors':e,'files':len(actual)};print(json.dumps(o,indent=2));sys.exit(0 if not e else 1)
if __name__=='__main__':main()
