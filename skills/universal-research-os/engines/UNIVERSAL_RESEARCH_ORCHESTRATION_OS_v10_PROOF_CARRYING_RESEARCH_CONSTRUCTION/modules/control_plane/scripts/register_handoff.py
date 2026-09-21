#!/usr/bin/env python3
from pathlib import Path
import argparse,json,datetime
from common import *
ap=argparse.ArgumentParser();ap.add_argument('handoff_zip');ap.add_argument('--registry',required=True);ap.add_argument('--activate',action='store_true',default=True);a=ap.parse_args()
p=Path(a.handoff_zip).resolve();identity=read_handoff_identity_from_zip(p);reg=load_json(a.registry,{'registry_version':'1.0','entries':[]});hid=identity['handoff_id']
entry={'handoff_id':hid,'handoff_sha256':sha256_file(p),'status':'ACTIVE' if a.activate else 'REGISTERED','orchestration_os_version':identity.get('orchestration_os_version',''),'audit_os_version':identity.get('audit_os_version',''),'contract_generation':identity.get('contract_generation',''),'expected_output_name':identity.get('expected_output_name',''),'registered_at':datetime.datetime.utcnow().replace(microsecond=0).isoformat()+'Z','source_candidate_sha256':identity.get('source_candidate_sha256','')}
reg['entries']=[x for x in reg.get('entries',[]) if x.get('handoff_id')!=hid];reg['entries'].append(entry);write_json(a.registry,reg);print(json.dumps(entry,indent=2))
