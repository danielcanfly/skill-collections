from pathlib import Path
import hashlib,json,zipfile,tempfile,shutil
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def dump(p,o):Path(p).parent.mkdir(parents=True,exist_ok=True);Path(p).write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n')
def zipdir(root,out):
 with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED) as z:
  for p in sorted(Path(root).rglob('*')):
   if p.is_file():z.write(p,arcname=(Path(root).name/p.relative_to(root)).as_posix())
