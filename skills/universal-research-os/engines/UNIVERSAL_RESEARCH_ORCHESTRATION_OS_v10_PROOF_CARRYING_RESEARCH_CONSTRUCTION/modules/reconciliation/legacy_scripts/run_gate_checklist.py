#!/usr/bin/env python3
import argparse,json,sys
from pathlib import Path
p=argparse.ArgumentParser(); p.add_argument('--stage-root',required=True); p.add_argument('--stage',required=True); p.add_argument('--receipt',required=True); a=p.parse_args(); r=Path(a.stage_root)
required=['README.md',f'{a.stage}_COMPLETION_REPORT.md','manifest.json','SHA256SUMS.txt','audit','scripts']
missing=[x for x in required if not (r/x).exists()]
acc=list((r/'audit').glob('*acceptance*.json')) if (r/'audit').exists() else []
status=[]
for f in acc:
    try: status.append(json.loads(f.read_text()))
    except Exception as e: missing.append(f'bad json:{f.name}:{e}')
out={'stage':a.stage,'missing':missing,'acceptance_receipts':[x.name for x in acc],'pass':not missing and bool(acc)}
Path(a.receipt).write_text(json.dumps(out,indent=2)+'\n'); print(json.dumps(out,indent=2)); sys.exit(0 if out['pass'] else 1)
