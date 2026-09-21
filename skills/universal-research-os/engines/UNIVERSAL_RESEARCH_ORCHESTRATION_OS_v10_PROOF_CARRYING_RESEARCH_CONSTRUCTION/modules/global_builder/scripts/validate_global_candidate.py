#!/usr/bin/env python3
from pathlib import Path
import argparse,json,hashlib,sys
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def main():
 a=argparse.ArgumentParser();a.add_argument('global_root');x=a.parse_args();r=Path(x.global_root);e=[]
 caps=json.loads((r/'provenance_capsules.json').read_text()).get('capsules',[]) if (r/'provenance_capsules.json').exists() else []
 if not caps:e.append('provenance capsules missing/empty')
 for i in range(8):
  p=r/f'G{i}_RECEIPT.json';j=json.loads(p.read_text()) if p.exists() else {}; 
  if j.get('status')!='PASS':e.append(f'G{i} not PASS')
 g8=json.loads((r/'G8_RECEIPT.json').read_text()) if (r/'G8_RECEIPT.json').exists() else {}
 if g8.get('status') not in {'PENDING_EXTERNAL_AUDIT','PASS'}:e.append('G8 state invalid')
 names=['combined','kos','okf','r2','audit_consumption'];sets=[]
 for n in names:
  s=r/'surfaces'/n
  if not s.is_dir():e.append('surface missing '+n);sets.append({});continue
  m=json.loads((s/'manifest.json').read_text()) if (s/'manifest.json').exists() else {'entries':[]};exp={q['path']:q['sha256'] for q in m.get('entries',[])};act={p.relative_to(s).as_posix():sha(p) for p in s.rglob('*') if p.is_file() and p.name!='manifest.json'}
  if exp!=act:e.append('surface manifest mismatch '+n)
  if any('/independent_audit/' in ('/'+k+'/') or k.startswith('qa/') or k.startswith('research/') or k.startswith('handoff/') for k in act):e.append('audit-only root leaked into '+n)
  sets.append({p.relative_to(s).as_posix():sha(p) for p in s.rglob('*') if p.is_file()})
 if sets and any(q!=sets[0] for q in sets[1:]):e.append('five-surface path/SHA mismatch')
 rc=json.loads((r/'REPRODUCTION_CONTRACT.json').read_text()) if (r/'REPRODUCTION_CONTRACT.json').exists() else {}
 if rc.get('release_selfcheck_required') is not True or not rc.get('command'):e.append('release-selfcheck reproduction contract missing')
 o={'status':'PASS' if not e else 'FAIL','errors':e,'upstreams':len(caps),'surface_files':len(sets[0]) if sets else 0};print(json.dumps(o,indent=2));sys.exit(0 if not e else 1)
if __name__=='__main__':main()
