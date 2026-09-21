#!/usr/bin/env python3
from pathlib import Path
import subprocess,sys,tempfile,shutil,json
ROOT=Path(__file__).resolve().parents[1]
def run(cmd):
 r=subprocess.run(cmd,text=True,capture_output=True);print(r.stdout);print(r.stderr,file=sys.stderr)
 if r.returncode:raise SystemExit(r.returncode)
def main():
 tmp=Path(tempfile.mkdtemp())
 try:
  cfg=ROOT/'examples/domain_dispatch_config.example.json';run([sys.executable,str(ROOT/'scripts/validate_domain_config.py'),str(cfg)]);out=tmp/'children';run([sys.executable,str(ROOT/'scripts/generate_child_packages.py'),str(cfg),'--output-dir',str(out)]);run([sys.executable,str(ROOT/'scripts/validate_generated_collection.py'),str(out),str(cfg)]);print(json.dumps({'status':'PASS','generated':len(list(out.glob('*.zip')))},indent=2))
 finally:shutil.rmtree(tmp,ignore_errors=True)
if __name__=='__main__':main()
