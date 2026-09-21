#!/usr/bin/env python3
import argparse,csv,itertools,difflib,re
from pathlib import Path
from lib.common import norm_text, read_csv
p=argparse.ArgumentParser(); p.add_argument('--input',required=True); p.add_argument('--id-col',required=True); p.add_argument('--title-col',required=True); p.add_argument('--output',required=True); p.add_argument('--threshold',type=float,default=.82); a=p.parse_args()
rows=read_csv(a.input); out=[]
for x,y in itertools.combinations(rows,2):
    tx,ty=norm_text(x[a.title_col]),norm_text(y[a.title_col]); score=difflib.SequenceMatcher(None,tx,ty).ratio()
    if tx==ty or score>=a.threshold:
        out.append([x[a.id_col],y[a.id_col],x[a.title_col],y[a.title_col],f'{score:.4f}','PENDING_MANUAL_REVIEW'])
out.sort(key=lambda r:(-float(r[4]),r[0],r[1]))
with open(a.output,'w',newline='',encoding='utf-8') as f:
    w=csv.writer(f); w.writerow(['id_a','id_b','title_a','title_b','similarity','status']); w.writerows(out)
print(len(out))
