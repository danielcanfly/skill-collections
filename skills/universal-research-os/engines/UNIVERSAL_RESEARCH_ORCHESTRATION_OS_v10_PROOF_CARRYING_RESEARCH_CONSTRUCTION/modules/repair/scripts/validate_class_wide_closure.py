#!/usr/bin/env python3
from pathlib import Path
import argparse,json,subprocess,re
ap=argparse.ArgumentParser();ap.add_argument('matrix');ap.add_argument('--candidate-root');ap.add_argument('--output');a=ap.parse_args();obj=json.loads(Path(a.matrix).read_text());rows=obj.get('findings',obj.get('closures',obj if isinstance(obj,list) else []));errors=[];results=[]
def subst(cmd):
 return [str(x).replace('{candidate}',str(Path(a.candidate_root).resolve()) if a.candidate_root else '{candidate}') for x in cmd]
def population_count(stdout):
 text=(stdout or '').strip()
 try:
  o=json.loads(text.splitlines()[-1] if '\n' in text else text)
  if isinstance(o,dict) and 'population_count' in o:return int(o['population_count'])
  if isinstance(o,int):return o
 except:pass
 m=re.search(r'(-?\d+)\s*$',text)
 return int(m.group(1)) if m else None
for r in rows:
 fid=r.get('finding_id','?');rowerr=[]
 for k in ['finding_id','failure_class','population_selector','closure_scope','expected_population_count','population_command','closure_command']:
  if k not in r or r.get(k) is None or r.get(k)=='' or r.get(k)==[]: rowerr.append(f'missing {k}')
 if r.get('closure_scope')!='CLASS_WIDE': rowerr.append('closure_scope must be CLASS_WIDE')
 if r.get('review_all_retained_direct_support') is not True: rowerr.append('all retained direct support must be reviewed')
 try:expected=int(r.get('expected_population_count',-1))
 except:expected=-1
 if expected<0: rowerr.append('invalid expected population')
 observed=None;proc=None
 if a.candidate_root and r.get('population_command'):
  proc=subprocess.run(subst(r['population_command']),capture_output=True,text=True);observed=population_count(proc.stdout)
  if proc.returncode!=0: rowerr.append(f'population command exit {proc.returncode}')
  elif observed is None: rowerr.append('population command did not emit population_count')
  elif observed!=expected: rowerr.append(f'population count {observed} != expected {expected}')
 results.append({'finding_id':fid,'expected_population_count':expected,'observed_population_count':observed,'status':'PASS' if not rowerr else 'FAIL','errors':rowerr,'population_stdout':(proc.stdout[-1000:] if proc else ''),'population_stderr':(proc.stderr[-1000:] if proc else '')})
 errors.extend(f'{fid}: {e}' for e in rowerr)
out={'status':'PASS' if not errors else 'FAIL','errors':errors,'closure_rows':len(rows),'results':results}
if a.output: Path(a.output).write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2));raise SystemExit(0 if not errors else 1)
