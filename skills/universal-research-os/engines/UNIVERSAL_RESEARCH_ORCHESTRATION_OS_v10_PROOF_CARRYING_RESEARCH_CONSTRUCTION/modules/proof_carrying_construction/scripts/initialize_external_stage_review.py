#!/usr/bin/env python3
from pathlib import Path
import argparse,csv,json,hashlib,datetime
PASSAGE_FIELDS=['passage_id','source_id','excerpt_sha256','snapshot_sha256','locator_type','locator_value']
CLAUSE_FIELDS=['clause_id','proposed_claim_id','clause_text','passage_ids','support_status','unsupported_remainder']
def rows(p):
 with Path(p).open(newline='',encoding='utf-8-sig') as f:return list(csv.DictReader(f))
def rsha(r,fields):return hashlib.sha256('\n'.join(str(r.get(k,'')).strip() for k in fields).encode()).hexdigest()
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(p,fields,data):
 p.parent.mkdir(parents=True,exist_ok=True)
 with p.open('w',newline='',encoding='utf-8') as f:w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(data)
def main():
 a=argparse.ArgumentParser();a.add_argument('candidate_root');a.add_argument('--output',required=True);a.add_argument('--reviewer-id',required=True);a.add_argument('--reviewer-session-id',required=True);x=a.parse_args();r=Path(x.candidate_root);out=Path(x.output);out.mkdir(parents=True,exist_ok=True);now=datetime.datetime.now(datetime.timezone.utc).isoformat()
 ps=rows(r/'research/source_passage_registry.csv');cs=rows(r/'research/material_clause_registry.csv')
 pr=[{'passage_id':q['passage_id'],'row_sha256':rsha(q,PASSAGE_FIELDS),'verdict':'NOT_REVIEWED','reviewer_id':x.reviewer_id,'reviewer_session_id':x.reviewer_session_id,'reviewed_at':'','notes':''} for q in ps]
 cr=[{'clause_id':q['clause_id'],'row_sha256':rsha(q,CLAUSE_FIELDS),'verdict':'NOT_REVIEWED','reviewer_id':x.reviewer_id,'reviewer_session_id':x.reviewer_session_id,'reviewed_at':'','notes':''} for q in cs]
 write(out/'PASSAGE_REVIEW.csv',list(pr[0]) if pr else ['passage_id','row_sha256','verdict','reviewer_id','reviewer_session_id','reviewed_at','notes'],pr);write(out/'CLAUSE_REVIEW.csv',list(cr[0]) if cr else ['clause_id','row_sha256','verdict','reviewer_id','reviewer_session_id','reviewed_at','notes'],cr)
 ident={'status':'IN_PROGRESS','contract_generation':'v10','audit_os_version':'6.0.0','reviewer_id':x.reviewer_id,'reviewer_session_id':x.reviewer_session_id,'passage_registry_sha256':sha(r/'research/source_passage_registry.csv'),'clause_registry_sha256':sha(r/'research/material_clause_registry.csv'),'created_at':now};(out/'STAGE_REVIEW_IDENTITY.json').write_text(json.dumps(ident,indent=2)+'\n');print(json.dumps({'status':'PASS','passages':len(pr),'clauses':len(cr),'output':str(out)},indent=2))
if __name__=='__main__':main()
