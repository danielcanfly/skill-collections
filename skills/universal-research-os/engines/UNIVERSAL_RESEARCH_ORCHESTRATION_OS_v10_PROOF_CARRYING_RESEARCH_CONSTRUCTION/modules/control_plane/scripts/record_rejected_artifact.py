#!/usr/bin/env python3
from pathlib import Path
import argparse,json,datetime
from common import *
ap=argparse.ArgumentParser();ap.add_argument('artifact');ap.add_argument('--registry',required=True);ap.add_argument('--reason',required=True);ap.add_argument('--finding-ids',default='');a=ap.parse_args();reg=load_json(a.registry,{'registry_version':'1.0','artifacts':[]});h=sha256_file(a.artifact);reg['artifacts']=[x for x in reg.get('artifacts',[]) if x.get('sha256')!=h];reg['artifacts'].append({'sha256':h,'filename':Path(a.artifact).name,'reason':a.reason,'finding_ids':[x for x in a.finding_ids.split(',') if x],'recorded_at':datetime.datetime.now(datetime.timezone.utc).isoformat()});write_json(a.registry,reg);print(json.dumps(reg['artifacts'][-1],indent=2))
