#!/usr/bin/env python3
from pathlib import Path
import argparse,json
ap=argparse.ArgumentParser();ap.add_argument('candidate');ap.add_argument('--output');a=ap.parse_args()
msg={'status':'CANDIDATE_SELF_CHECK_ONLY','candidate':Path(a.candidate).name,'next_step':'Run mandatory v10 admission, then independent Audit OS v6 outside the candidate session.','merge_ready':False,'production_release':False}
print(json.dumps(msg,indent=2))
