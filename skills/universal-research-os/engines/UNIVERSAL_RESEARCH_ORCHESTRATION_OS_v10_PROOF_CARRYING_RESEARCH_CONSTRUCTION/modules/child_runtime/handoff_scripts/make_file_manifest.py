#!/usr/bin/env python3
from pathlib import Path
import argparse, hashlib, json
from datetime import datetime, timezone

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("root"); args=ap.parse_args()
    root=Path(args.root).resolve()
    manifest_path=root/"handoff/file_manifest.json"
    files=[]
    for p in sorted(x for x in root.rglob("*") if x.is_file() and x!=manifest_path):
        files.append({"path":p.relative_to(root).as_posix(),"sha256":hashlib.sha256(p.read_bytes()).hexdigest(),"size_bytes":p.stat().st_size})
    out={"generated_at":datetime.now(timezone.utc).isoformat(),"hash_algorithm":"sha256","manifest_excludes":["handoff/file_manifest.json"],"file_count":len(files),"files":files}
    manifest_path.parent.mkdir(parents=True,exist_ok=True)
    manifest_path.write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding="utf-8")
    print(json.dumps({"file_count":len(files),"manifest":str(manifest_path)}))
if __name__=="__main__": main()
