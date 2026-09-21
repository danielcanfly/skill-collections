#!/usr/bin/env python3
from pathlib import Path
import argparse,json,hashlib,sys,datetime
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def main():
 a=argparse.ArgumentParser();a.add_argument('global_root');a.add_argument('external_audit');a.add_argument('--canonical-tree-sha',required=True);x=a.parse_args();r=Path(x.global_root);aobj=json.loads(Path(x.external_audit).read_text());e=[]
 if aobj.get('status')!='PASS':e.append('external global audit not PASS')
 if aobj.get('canonical_tree_sha256')!=x.canonical_tree_sha:e.append('canonical tree SHA mismatch')
 if aobj.get('auditor_session_id')==aobj.get('builder_session_id'):e.append('global auditor not independent')
 if e:print(json.dumps({'status':'FAIL','errors':e},indent=2));sys.exit(1)
 (r/'G8_RECEIPT.json').write_text(json.dumps({'gate':'G8','status':'PASS','canonical_tree_sha256':x.canonical_tree_sha,'external_audit_sha256':sha(x.external_audit),'closed_at':datetime.datetime.now(datetime.timezone.utc).isoformat()},indent=2)+'\n');(r/'GLOBAL_STATE.json').write_text(json.dumps({'status':'GLOBAL_MERGE_READY','g8':'PASS'},indent=2)+'\n');print(json.dumps({'status':'PASS','global_status':'GLOBAL_MERGE_READY'},indent=2))
if __name__=='__main__':main()
