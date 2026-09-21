#!/usr/bin/env python3
import argparse,json,sys
from pathlib import Path
p=argparse.ArgumentParser(); p.add_argument('--tests',required=True); p.add_argument('--results',required=True); p.add_argument('--receipt',required=True); p.add_argument('--cutoff',type=int,default=10); a=p.parse_args()
tests={x['test_id']:x for x in json.loads(Path(a.tests).read_text())}; results={x['test_id']:x for x in json.loads(Path(a.results).read_text())}
fail=[]
for tid,t in tests.items():
    ranked=results.get(tid,{}).get('ranked_ids',[])[:a.cutoff]
    missing=[x for x in t['expected_ids'] if x not in ranked]; neg=[x for x in t.get('negative_ids',[]) if x in ranked]
    if missing or neg: fail.append({'test_id':tid,'missing':missing,'negative_hits':neg})
count=len(tests); hold=sum(bool(t.get('holdout')) for t in tests.values()); negative=sum(bool(t.get('negative_ids')) for t in tests.values())
r={'tests':count,'passed':count-len(fail),'failures':fail,'holdout_ratio':hold/count if count else 0,'negative_ratio':negative/count if count else 0,'pass':not fail}
Path(a.receipt).write_text(json.dumps(r,indent=2)+'\n'); print(json.dumps(r,indent=2)); sys.exit(0 if r['pass'] else 1)
