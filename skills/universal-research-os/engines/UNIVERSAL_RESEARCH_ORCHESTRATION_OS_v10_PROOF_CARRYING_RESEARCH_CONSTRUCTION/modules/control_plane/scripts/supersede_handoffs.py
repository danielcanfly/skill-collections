#!/usr/bin/env python3
import argparse,json,datetime
from common import *
def vt(s):
 try:return tuple(int(x) for x in str(s).split('.')[:3])
 except:return (0,)
ap=argparse.ArgumentParser();ap.add_argument('--registry',required=True);ap.add_argument('--older-than-os');ap.add_argument('--handoff-id',action='append',default=[]);ap.add_argument('--reason',required=True);ap.add_argument('--superseded-by',default='');a=ap.parse_args();reg=load_json(a.registry,{'entries':[]});changed=[]
for e in reg.get('entries',[]):
 hit=e.get('handoff_id') in a.handoff_id or (a.older_than_os and vt(e.get('orchestration_os_version','0'))<vt(a.older_than_os))
 if hit and e.get('status') in {'ACTIVE','REGISTERED'}:
  e['status']='SUPERSEDED_DO_NOT_EXECUTE';e['reason']=a.reason;e['superseded_by']=a.superseded_by;e['superseded_at']=datetime.datetime.utcnow().replace(microsecond=0).isoformat()+'Z';changed.append(e['handoff_id'])
write_json(a.registry,reg);print(json.dumps({'status':'PASS','superseded':changed},indent=2))
