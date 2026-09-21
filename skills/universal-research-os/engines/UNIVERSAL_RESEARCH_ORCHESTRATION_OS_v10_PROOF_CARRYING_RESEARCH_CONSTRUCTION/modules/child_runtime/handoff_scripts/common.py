from __future__ import annotations
from pathlib import Path
import csv,json,hashlib,re

def load_json(p,default=None):
    p=Path(p)
    if not p.exists(): return default
    try: return json.loads(p.read_text(encoding='utf-8'))
    except Exception: return default

def rows(p):
    p=Path(p)
    if not p.exists(): return []
    with p.open(encoding='utf-8-sig',newline='') as f: return list(csv.DictReader(f))

def tree_hash(root):
    root=Path(root); h=hashlib.sha256()
    for p in sorted(root.rglob('*')):
        if p.is_file():
            h.update(p.relative_to(root).as_posix().encode());h.update(b'\0');h.update(hashlib.sha256(p.read_bytes()).digest())
    return h.hexdigest()

def result(status,errors=None,warnings=None,stats=None): return {'status':status,'errors':errors or [],'warnings':warnings or [],'stats':stats or {}}

def emit(obj,path=None):
    text=json.dumps(obj,ensure_ascii=False,indent=2)
    if path: Path(path).write_text(text+'\n',encoding='utf-8')
    print(text); raise SystemExit(0 if obj.get('status')=='PASS' else 1)

def norm(s): return re.sub(r'[^a-z0-9\u3400-\u9fff]+',' ',str(s).lower()).strip()

def split_ids(s): return {x.strip() for x in re.split(r'[;|,]',str(s or '')) if x.strip()}


def sha256_file(path):
    path=Path(path); return hashlib.sha256(path.read_bytes()).hexdigest()

def token_set(s): return {x for x in norm(s).split() if len(x)>1}

def token_containment(a,b):
    aa=token_set(a); bb=token_set(b)
    return (len(aa & bb)/len(aa)) if aa else 0.0

def parse_iso(s):
    import datetime
    if not s: return None
    try: return datetime.datetime.fromisoformat(str(s).replace('Z','+00:00'))
    except Exception: return None
