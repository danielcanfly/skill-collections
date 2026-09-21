#!/usr/bin/env python3
from pathlib import Path
import argparse,json,re
def main():
 ap=argparse.ArgumentParser();ap.add_argument('root');a=ap.parse_args();root=Path(a.root).resolve();cfg=json.loads((root/'audit_config.json').read_text());cid=cfg['candidate_id'];ver=cfg['candidate_version'];out=cfg['final_output_name']
 for rel in ['PHASE_RETURN_MANIFEST.json','handoff/merge_manifest.json']:
  p=root/rel;d=json.loads(p.read_text());d['candidate_id']=cid;d['candidate_version']=ver;d['final_output_name']=out;p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 pattern=r'[A-Za-z0-9_.-]+_PRODUCTION_CANDIDATE_v[0-9A-Za-z_.-]+\.zip'
 for rel in ['00_COMPLETION_SUMMARY.md','QUALITY_REPORT.md','qa/final_acceptance_checklist.md']:
  p=root/rel;t=p.read_text(encoding='utf-8');t=re.sub(pattern,out,t);p.write_text(t,encoding='utf-8')
 print(json.dumps({'status':'PASS','candidate_id':cid,'candidate_version':ver,'final_output_name':out},indent=2))
if __name__=='__main__':main()
