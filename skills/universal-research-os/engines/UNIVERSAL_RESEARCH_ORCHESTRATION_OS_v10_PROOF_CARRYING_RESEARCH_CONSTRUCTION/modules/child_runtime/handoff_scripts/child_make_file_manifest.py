#!/usr/bin/env python3
from pathlib import Path
import argparse,hashlib,json
EXCLUDES={'handoff/file_manifest.json','qa/package_validation.json'}
def main():
 ap=argparse.ArgumentParser(); ap.add_argument('root'); a=ap.parse_args(); root=Path(a.root).resolve(); files=[]
 for p in sorted(x for x in root.rglob('*') if x.is_file()):
  rel=p.relative_to(root).as_posix()
  if rel in EXCLUDES: continue
  files.append({'path':rel,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'size_bytes':p.stat().st_size})
 out={'manifest_version':'1.0','hash_algorithm':'sha256','generation_mode':'deterministic-final-step','manifest_excludes':sorted(EXCLUDES),'file_count':len(files),'files':files}; q=root/'handoff/file_manifest.json'; q.parent.mkdir(parents=True,exist_ok=True); q.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8'); print(json.dumps({'file_count':len(files),'manifest':str(q)}))
if __name__=='__main__': main()
