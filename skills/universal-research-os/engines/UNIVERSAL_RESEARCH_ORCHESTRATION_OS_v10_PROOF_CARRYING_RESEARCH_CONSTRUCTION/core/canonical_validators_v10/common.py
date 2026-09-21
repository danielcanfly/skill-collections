from pathlib import Path
import csv,json,hashlib,re

def sha_bytes(b): return hashlib.sha256(b).hexdigest()
def sha_file(p): return sha_bytes(Path(p).read_bytes())
def tree_sha(root):
 rows=[]
 for p in sorted(Path(root).rglob('*')):
  if p.is_file() and '__pycache__' not in p.parts and p.suffix not in {'.pyc','.pyo'} and p.relative_to(root).as_posix() not in {'qa/seal_state.json','handoff/file_manifest.json'}:
   rows.append(p.relative_to(root).as_posix()+':'+sha_file(p))
 return sha_bytes(('\n'.join(rows)).encode())
def read_csv(p):
 with Path(p).open(newline='',encoding='utf-8-sig') as f:return list(csv.DictReader(f))
def write_csv(p,rows,fields):
 Path(p).parent.mkdir(parents=True,exist_ok=True)
 with Path(p).open('w',newline='',encoding='utf-8') as f:
  wr=csv.DictWriter(f,fieldnames=fields);wr.writeheader();wr.writerows(rows)
def load(p,default=None):
 try:return json.loads(Path(p).read_text(encoding='utf-8'))
 except:return {} if default is None else default
def dump(p,o):Path(p).parent.mkdir(parents=True,exist_ok=True);Path(p).write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def row_sha(row,fields):
 return sha_bytes('\n'.join(str(row.get(k,'')).strip() for k in fields).encode())
