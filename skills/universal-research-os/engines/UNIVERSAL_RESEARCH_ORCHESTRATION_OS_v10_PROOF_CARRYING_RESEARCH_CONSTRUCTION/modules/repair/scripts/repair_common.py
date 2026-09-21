from pathlib import Path
import hashlib,json,zipfile,tempfile,fnmatch,csv

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def load(p):return json.loads(Path(p).read_text(encoding='utf-8'))
def write(p,o):Path(p).write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def extract(z):
 td=tempfile.TemporaryDirectory();base=Path(td.name)
 with zipfile.ZipFile(z) as zz:
  bad=zz.testzip()
  if bad:raise ValueError('CRC '+bad)
  zz.extractall(base)
 roots=[p for p in base.iterdir() if p.is_dir()];return td,(roots[0] if len(roots)==1 else base)
def files(root):return {p.relative_to(root).as_posix():p for p in root.rglob('*') if p.is_file()}
def matches(path,pattern):return fnmatch.fnmatch(path,pattern) or path==pattern or path.startswith(pattern.rstrip('/')+'/')
def rule_matches(path,rules):return [r for r in rules if matches(path,r['path_pattern'])]
def tree_hashes(root):return {k:sha(v) for k,v in files(root).items()}
