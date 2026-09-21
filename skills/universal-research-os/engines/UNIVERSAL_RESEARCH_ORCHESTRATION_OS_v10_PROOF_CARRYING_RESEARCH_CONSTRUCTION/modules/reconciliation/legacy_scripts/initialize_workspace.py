#!/usr/bin/env python3
from pathlib import Path
import argparse, json
p=argparse.ArgumentParser(); p.add_argument('--root',required=True); p.add_argument('--project',required=True); a=p.parse_args()
r=Path(a.root)
for d in ['inputs/immutable','workspace/extracted','registries','artifacts','compiled_markdown','benchmark','results','audit','logs','dependencies','contracts','scripts','release']:
    (r/d).mkdir(parents=True,exist_ok=True)
(r/'project.json').write_text(json.dumps({'project':a.project,'status':'INITIALIZED'},indent=2)+'\n')
print(r)
