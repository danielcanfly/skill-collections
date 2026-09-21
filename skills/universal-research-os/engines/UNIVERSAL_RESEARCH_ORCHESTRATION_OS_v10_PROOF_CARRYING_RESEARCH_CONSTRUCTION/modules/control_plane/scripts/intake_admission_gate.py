#!/usr/bin/env python3
from pathlib import Path
import argparse,json,zipfile
from common import *
def main():
 ap=argparse.ArgumentParser();ap.add_argument('returned');ap.add_argument('--registry',required=True);ap.add_argument('--rejected-registry');ap.add_argument('--expected-name');ap.add_argument('--allow-legacy-migration',action='store_true');ap.add_argument('--output',required=True);a=ap.parse_args();p=Path(a.returned).resolve();import datetime
 receipt={'observed_at':datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0).isoformat().replace('+00:00','Z'),'candidate':p.name,'candidate_sha256':sha256_file(p),'filename_ok':not a.expected_name or p.name==a.expected_name,'zip_crc':'FAIL','lineage_status':'MISSING','handoff_status':'UNKNOWN','classification':'UNKNOWN_LINEAGE_REJECTED','status':'FAIL','errors':[]}
 if not receipt['filename_ok']:
  receipt['classification']='FILENAME_REJECTED';receipt['errors'].append('filename mismatch');write_json(a.output,receipt);print(json.dumps(receipt,indent=2));raise SystemExit(1)
 if not zipfile.is_zipfile(p):
  receipt['classification']='CRC_REJECTED';receipt['errors'].append('not a zip');write_json(a.output,receipt);print(json.dumps(receipt,indent=2));raise SystemExit(1)
 td,root=extract_single_root(p);receipt['zip_crc']='PASS';rej=load_json(a.rejected_registry,{'artifacts':[]}) if a.rejected_registry else {'artifacts':[]}
 if any(x.get('sha256')==receipt['candidate_sha256'] for x in rej.get('artifacts',[])):
  receipt['classification']='STALE_ARTIFACT_REJECTED';receipt['errors'].append('candidate hash is in rejected artifact registry');td.cleanup();write_json(a.output,receipt);print(json.dumps(receipt,indent=2));raise SystemExit(1)
 lin=load_json(root/'handoff/contract_lineage.json',{});receipt['lineage_status']=lin.get('status','MISSING');receipt['originating_handoff_id']=lin.get('originating_handoff_id','');receipt['originating_handoff_sha256']=lin.get('originating_handoff_sha256','');receipt['orchestration_os_version']=lin.get('orchestration_os_version','');receipt['audit_os_version']=lin.get('audit_os_version','');reg=load_json(a.registry,{'entries':[]});entry=next((x for x in reg.get('entries',[]) if x.get('handoff_id')==lin.get('originating_handoff_id')),None)
 if not lin or lin.get('status')!='BOUND':receipt['classification']='UNKNOWN_LINEAGE_REJECTED';receipt['errors'].append('contract lineage missing or not BOUND')
 elif not entry:receipt['classification']='UNKNOWN_LINEAGE_REJECTED';receipt['errors'].append('originating handoff not registered')
 else:
  receipt['handoff_status']=entry.get('status','UNKNOWN')
  if entry.get('status')=='SUPERSEDED_DO_NOT_EXECUTE':receipt['classification']='SUPERSEDED_HANDOFF_REJECTED';receipt['errors'].append('originating handoff is superseded')
  elif entry.get('status') not in {'ACTIVE','REGISTERED'}:receipt['classification']='STALE_ARTIFACT_REJECTED';receipt['errors'].append('originating handoff is not active')
  elif entry.get('handoff_sha256')!=lin.get('originating_handoff_sha256'):receipt['classification']='CONTRACT_HASH_REJECTED';receipt['errors'].append('originating handoff SHA mismatch')
  elif entry.get('expected_output_name') and p.name!=entry.get('expected_output_name'):receipt['classification']='FILENAME_REJECTED';receipt['errors'].append('returned filename differs from registry')
  elif (str(lin.get('orchestration_os_version','')).startswith('10.') and str(lin.get('audit_os_version','')).startswith('6.') and lin.get('contract_generation')=='v10' and str(entry.get('orchestration_os_version','')).startswith('10.') and str(entry.get('audit_os_version','')).startswith('6.') and entry.get('contract_generation')=='v10'):receipt['classification']='V10_NATIVE_ACCEPTED'
  elif a.allow_legacy_migration:receipt['classification']='LEGACY_MIGRATABLE_ACCEPTED'
  else:receipt['classification']='SUPERSEDED_HANDOFF_REJECTED';receipt['errors'].append('legacy or incompatible contract requires explicit migration approval')
 td.cleanup();receipt['status']='PASS' if receipt['classification'] in {'V10_NATIVE_ACCEPTED','LEGACY_MIGRATABLE_ACCEPTED'} and not receipt['errors'] else 'FAIL';write_json(a.output,receipt);print(json.dumps(receipt,ensure_ascii=False,indent=2));raise SystemExit(0 if receipt['status']=='PASS' else 1)
if __name__=='__main__':main()
