from pathlib import Path
import json,hashlib,zipfile,tempfile

def sha256_file(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def load_json(p,default=None):
 p=Path(p)
 return json.loads(p.read_text(encoding='utf-8')) if p.exists() else (default if default is not None else {})
def write_json(p,obj):
 p=Path(p);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def extract_single_root(zpath):
 td=tempfile.TemporaryDirectory();base=Path(td.name)
 with zipfile.ZipFile(zpath) as z:
  bad=z.testzip()
  if bad: raise ValueError('ZIP CRC failure: '+bad)
  z.extractall(base)
 roots=[p for p in base.iterdir() if p.is_dir()]
 return td,(roots[0] if len(roots)==1 else base)
def read_handoff_identity_from_zip(zpath):
 td,root=extract_single_root(zpath)
 p=root/'HANDOFF_IDENTITY.json'
 if not p.exists(): td.cleanup(); raise ValueError('HANDOFF_IDENTITY.json missing')
 obj=load_json(p);td.cleanup();return obj
