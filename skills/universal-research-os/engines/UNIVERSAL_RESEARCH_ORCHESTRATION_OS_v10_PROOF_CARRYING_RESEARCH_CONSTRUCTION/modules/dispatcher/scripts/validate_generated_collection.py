#!/usr/bin/env python3
from pathlib import Path
import argparse,json,subprocess,sys
ROOT=Path(__file__).resolve().parent
def main():
 ap=argparse.ArgumentParser();ap.add_argument('dir');ap.add_argument('config');a=ap.parse_args();d=json.loads(Path(a.config).read_text());base=Path(a.dir);results=[]
 for c in d['children']:
  prefix=c['session_id'].replace('/','-')+'_PROOF_CARRYING_AUDIT_V6_RESEARCH_HANDOFF_v10'
  matches=list(base.glob(prefix+'.zip'))
  if len(matches)!=1:results.append({'session_id':c['session_id'],'status':'FAIL','error':'package missing or duplicate','expected':prefix+'.zip'});continue
  r=subprocess.run([sys.executable,str(ROOT/'validate_child_handoff.py'),str(matches[0])],text=True,capture_output=True);results.append({'session_id':c['session_id'],'status':'PASS' if r.returncode==0 else 'FAIL','detail':r.stdout[-4000:]})
 ok=all(x['status']=='PASS' for x in results);print(json.dumps({'status':'PASS' if ok else 'FAIL','results':results},ensure_ascii=False,indent=2));raise SystemExit(0 if ok else 1)
if __name__=='__main__':main()
