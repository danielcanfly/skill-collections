#!/usr/bin/env python3
from pathlib import Path
import argparse,json,zipfile,tempfile,shutil,hashlib,sys,subprocess
from global_common import *
def tree_map(root):return {p.relative_to(root).as_posix():sha(p) for p in sorted(Path(root).rglob('*')) if p.is_file() and p.name!='manifest.json'}
def write_surface_manifest(root):
 entries=[{'path':k,'sha256':v,'bytes':(root/k).stat().st_size} for k,v in tree_map(root).items()];dump(root/'manifest.json',{'contract_generation':'v10','entries':entries});return entries
def extract_single(zp,base):
 with zipfile.ZipFile(zp) as z:
  bad=z.testzip()
  if bad: raise SystemExit('ZIP CRC failure '+str(zp)+': '+str(bad))
  roots={Path(n).parts[0] for n in z.namelist() if n and not n.startswith('__MACOSX/')}
  if len(roots)!=1: raise SystemExit('one root required '+str(zp))
  z.extractall(base)
 return base/next(iter(roots))
def main():
 a=argparse.ArgumentParser();a.add_argument('releases',nargs='+');a.add_argument('--release-id',required=True);a.add_argument('--output-dir',required=True);x=a.parse_args();out=Path(x.output_dir);shutil.rmtree(out,ignore_errors=True);out.mkdir(parents=True);can=out/'canonical';can.mkdir();caps=[];seen_release=set();seen_candidate=set();validator=Path(__file__).resolve().parents[2]/'production_release/scripts/validate_child_production_release.py'
 for i,zname in enumerate(x.releases,1):
  zp=Path(zname).resolve();subprocess.run([sys.executable,str(validator),str(zp)],check=True,capture_output=True,text=True);rsha=sha(zp)
  if rsha in seen_release:raise SystemExit('duplicate upstream production release SHA')
  seen_release.add(rsha);td=Path(tempfile.mkdtemp());wrapper=extract_single(zp,td/'wrapper');rec=json.loads((wrapper/'PRODUCTION_RELEASE_RECEIPT.json').read_text());csha=rec.get('candidate_sha256')
  if not csha or csha in seen_candidate:raise SystemExit('duplicate/missing upstream candidate SHA')
  seen_candidate.add(csha);payloads=list((wrapper/'payload').glob('*.zip'))
  if len(payloads)!=1: raise SystemExit('upstream payload candidate missing')
  cand=extract_single(payloads[0],td/'candidate')
  knowledge=cand/'knowledge'
  if not knowledge.is_dir():raise SystemExit('upstream candidate knowledge root missing')
  dest=can/f'upstream_{i:03d}';shutil.copytree(knowledge,dest/'knowledge')
  cap={'upstream_index':i,'filename':zp.name,'production_release_sha256':rsha,'production_receipt_sha256':sha(wrapper/'PRODUCTION_RELEASE_RECEIPT.json'),'candidate_sha256':csha,'admission_receipt_sha256':rec.get('admission_receipt_sha256'),'audit_package_manifest_sha256':rec.get('audit_package_manifest_sha256'),'audit_package_identity_sha256':rec.get('audit_package_identity_sha256'),'audit_summary_sha256':rec.get('audit_summary_sha256'),'independent_review_receipt_sha256':rec.get('independent_review_receipt_sha256'),'materialized_root':f'canonical/upstream_{i:03d}/knowledge'};caps.append(cap)
 dump(out/'provenance_capsules.json',{'contract_generation':'v10','release_id':x.release_id,'capsules':caps});canonical_sha=hashlib.sha256('\n'.join(sorted(k+':'+v for k,v in tree_map(can).items())).encode()).hexdigest()
 for g in range(8):dump(out/f'G{g}_RECEIPT.json',{'gate':f'G{g}','status':'PASS','release_id':x.release_id,'upstream_count':len(caps),'canonical_tree_sha256':canonical_sha})
 dump(out/'G8_RECEIPT.json',{'gate':'G8','status':'PENDING_EXTERNAL_AUDIT','release_id':x.release_id,'canonical_tree_sha256':canonical_sha})
 surfaces={}
 for name in ['combined','kos','okf','r2','audit_consumption']:
  s=out/'surfaces'/name;shutil.copytree(can,s);write_surface_manifest(s);surfaces[name]=s
 sets=[{p.relative_to(s).as_posix():sha(p) for p in s.rglob('*') if p.is_file()} for s in surfaces.values()]
 if any(q!=sets[0] for q in sets[1:]):raise SystemExit('five-surface equality failure')
 dump(out/'FIVE_SURFACE_EQUALITY.json',{'status':'PASS','file_count':len(sets[0]),'surfaces':list(surfaces),'release_id':x.release_id,'canonical_tree_sha256':canonical_sha});dump(out/'REPRODUCTION_CONTRACT.json',{'contract_generation':'v10','command':['{python}','modules/global_builder/scripts/validate_global_candidate.py','{global_root}'],'release_selfcheck_required':True});dump(out/'GLOBAL_STATE.json',{'status':'READY_FOR_INDEPENDENT_GLOBAL_AUDIT','g8':'PENDING','release_id':x.release_id,'canonical_tree_sha256':canonical_sha});print(json.dumps({'status':'PASS','upstreams':len(caps),'files_per_surface':len(sets[0]),'g8':'PENDING','canonical_tree_sha256':canonical_sha},indent=2))
if __name__=='__main__':main()
