#!/usr/bin/env python3
from pathlib import Path
import argparse,hashlib,json
def main():
 ap=argparse.ArgumentParser();ap.add_argument('root');a=ap.parse_args();root=Path(a.root).resolve();mp=root/'handoff/file_manifest.json';files=[]
 for p in sorted(x for x in root.rglob('*') if x.is_file() and x!=mp and x.name!='SHA256SUMS.txt'):
  files.append({'path':p.relative_to(root).as_posix(),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'size_bytes':p.stat().st_size})
 mp.parent.mkdir(parents=True,exist_ok=True);mp.write_text(json.dumps({'manifest_version':'2.0','hash_algorithm':'sha256','file_count':len(files),'files':files},ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps({'status':'PASS','file_count':len(files)}))
if __name__=='__main__':main()
