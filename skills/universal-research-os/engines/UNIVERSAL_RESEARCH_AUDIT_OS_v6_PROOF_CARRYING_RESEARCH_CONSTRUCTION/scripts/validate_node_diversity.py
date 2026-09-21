#!/usr/bin/env python3
from pathlib import Path
import argparse,re,difflib
from common import load_json,result,emit
ap=argparse.ArgumentParser();ap.add_argument('root');ap.add_argument('--config');ap.add_argument('--profile');ap.add_argument('--output');a=ap.parse_args();root=Path(a.root);profile=load_json(a.profile,{}) if a.profile else {};thr=float(profile.get('node_similarity_threshold',0.88));errors=[]
files=[]
for sub in ['concepts','patterns','checklists']:
    d=root/'knowledge'/sub
    if d.exists(): files.extend(d.rglob('*.md'))
if not files and (root/'knowledge').exists(): files=[p for p in (root/'knowledge').glob('*.md')]
def norm(t):
    t=re.sub(r'^---.*?---','',t,flags=re.S);t=re.sub(r'^#+.*$','',t,flags=re.M);return re.sub(r'\s+',' ',t).strip().lower()
texts=[(p,norm(p.read_text(encoding='utf-8',errors='replace'))) for p in files]
for i in range(len(texts)):
    for k in range(i+1,len(texts)):
        if len(texts[i][1])>300 and len(texts[k][1])>300:
            q=difflib.SequenceMatcher(None,texts[i][1],texts[k][1]).ratio()
            if q>=thr: errors.append(f'node similarity {q:.3f}: {texts[i][0].name} / {texts[k][0].name}')
emit(result('PASS' if not errors else 'FAIL',errors,stats={'nodes':len(files),'threshold':thr}),a.output)
