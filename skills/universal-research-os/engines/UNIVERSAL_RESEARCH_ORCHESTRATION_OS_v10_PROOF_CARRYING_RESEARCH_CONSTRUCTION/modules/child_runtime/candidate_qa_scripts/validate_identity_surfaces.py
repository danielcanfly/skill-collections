#!/usr/bin/env python3
from pathlib import Path
import argparse,json,re,sys
FORBIDDEN_DIRS=['concepts','patterns','source-notes','registries','checklists','evaluation','compatibility']
def main():
 ap=argparse.ArgumentParser(); ap.add_argument('root'); ap.add_argument('--config',default=None); ap.add_argument('--json-output'); a=ap.parse_args(); root=Path(a.root).resolve(); cfg=json.loads(Path(a.config).read_text()) if a.config else json.loads((root/'audit_config.json').read_text()); errors=[]
 expected=cfg['final_output_name']; cid=cfg['candidate_id']; version=cfg['candidate_version']
 prm=root/'PHASE_RETURN_MANIFEST.json'; mm=root/'handoff/merge_manifest.json'
 if not prm.exists(): errors.append('missing PHASE_RETURN_MANIFEST.json')
 else:
  d=json.loads(prm.read_text());
  if d.get('candidate_version')!=version: errors.append(f'PHASE_RETURN_MANIFEST candidate_version {d.get("candidate_version")} != {version}')
  if d.get('final_output_name')!=expected: errors.append('PHASE_RETURN_MANIFEST final_output_name mismatch')
 if not mm.exists(): errors.append('missing handoff/merge_manifest.json')
 else:
  d=json.loads(mm.read_text());
  if d.get('candidate_id')!=cid: errors.append(f'merge_manifest candidate_id {d.get("candidate_id")} != {cid}')
  if d.get('candidate_version')!=version: errors.append('merge_manifest candidate_version mismatch')
  if d.get('final_output_name')!=expected: errors.append('merge_manifest final_output_name mismatch')
  if str(d.get('status','')).upper()=='MERGE_READY': errors.append('child candidate may not self-award MERGE_READY')
 for d in FORBIDDEN_DIRS:
  if (root/d).exists(): errors.append(f'forbidden root merge surface: {d}/')
 for rel in ['qa/final_acceptance_checklist.md','QUALITY_REPORT.md','00_COMPLETION_SUMMARY.md']:
  p=root/rel
  if not p.exists(): errors.append(f'missing {rel}'); continue
  text=p.read_text(encoding='utf-8')
  if expected not in text: errors.append(f'{rel} does not name exact final output {expected}')
 # Reject stale production-candidate identities.
 stale=[]
 for p in root.rglob('*'):
  if p.is_file() and p.suffix.lower() in {'.md','.json','.txt','.csv'}:
   try: t=p.read_text(encoding='utf-8-sig')
   except: continue
   for m in re.findall(r'PRODUCTION_CANDIDATE_v(\d+)',t):
    if 'v'+m!=version: stale.append(f'{p.relative_to(root)}: v{m}')
 if stale: errors.append('stale version identities: '+ '; '.join(stale[:20]))
 out={'status':'PASS' if not errors else 'FAIL','expected_output':expected,'candidate_id':cid,'errors':errors}; txt=json.dumps(out,ensure_ascii=False,indent=2); print(txt); op=Path(a.json_output) if a.json_output else root/'qa/identity_surface_validation.json'; op.write_text(txt+'\n',encoding='utf-8'); raise SystemExit(0 if not errors else 1)
if __name__=='__main__': main()
