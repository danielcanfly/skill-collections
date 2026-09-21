#!/usr/bin/env python3
from pathlib import Path
import argparse,json,hashlib,datetime
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def main():
 a=argparse.ArgumentParser();a.add_argument('legacy_wrapper');a.add_argument('--legacy-payload');a.add_argument('--output',required=True);x=a.parse_args();o={'migration_contract':'v10','legacy_wrapper':{'filename':Path(x.legacy_wrapper).name,'sha256':sha(x.legacy_wrapper)},'legacy_payload':{'filename':Path(x.legacy_payload).name,'sha256':sha(x.legacy_payload)} if x.legacy_payload else None,'required_steps':['rebuild_source_snapshots','typed_locator_resolution','clause_pre_review','v10_admission','Audit_OS_v6','promotion','wrapper_validation'],'created_at':datetime.datetime.now(datetime.timezone.utc).isoformat()};Path(x.output).write_text(json.dumps(o,indent=2)+'\n')
if __name__=='__main__':main()
