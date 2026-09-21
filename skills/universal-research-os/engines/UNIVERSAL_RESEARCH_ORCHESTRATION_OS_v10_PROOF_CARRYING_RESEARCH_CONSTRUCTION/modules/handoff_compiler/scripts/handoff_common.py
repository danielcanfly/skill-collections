from pathlib import Path
import hashlib,json,zipfile,shutil,tempfile,csv
EPOCH=(1980,1,1,0,0,0)
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def dump(p,o):Path(p).parent.mkdir(parents=True,exist_ok=True);Path(p).write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n')
def tree(root):return {p.relative_to(root).as_posix():{'sha256':sha(p),'bytes':p.stat().st_size} for p in sorted(Path(root).rglob('*')) if p.is_file() and '__pycache__' not in p.parts and p.suffix not in {'.pyc','.pyo'}}
def manifest(root):return [{'path':k,**v} for k,v in tree(root).items() if k not in {'manifest.json','SHA256SUMS.txt'}]
def zipone(root,out):
 out=Path(out);out.parent.mkdir(parents=True,exist_ok=True);out.unlink(missing_ok=True)
 with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
  for p in sorted(Path(root).rglob('*')):
   if p.is_file() and '__pycache__' not in p.parts and p.suffix not in {'.pyc','.pyo'}:
    info=zipfile.ZipInfo((Path(root).name/p.relative_to(root)).as_posix(),EPOCH);info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o100644<<16;z.writestr(info,p.read_bytes())
 with zipfile.ZipFile(out) as z:
  if z.testzip():raise SystemExit('ZIP CRC failure')
  roots={Path(n).parts[0] for n in z.namelist() if n and not n.startswith('__MACOSX/')}
  if len(roots)!=1:raise SystemExit('handoff ZIP must have one root')
def copy_tools(dst):
 src=Path(__file__).resolve().parent
 dst.mkdir(parents=True,exist_ok=True)
 for name in ['inspect_inputs.py','compare_protected_surfaces.py','validate_handoff_package.py','validate_return_inventory.py']:
  shutil.copy2(src/name,dst/name)
