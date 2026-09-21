#!/usr/bin/env python3
from pathlib import Path
import argparse,json,hashlib

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def main():
    ap=argparse.ArgumentParser();ap.add_argument('root',nargs='?',default=str(Path(__file__).resolve().parents[2]));ap.add_argument('--output',default='qa/release_selfcheck_result.json');a=ap.parse_args();root=Path(a.root).resolve();errors=[]
    manifest=root/'manifest.json'
    if not manifest.is_file():errors.append('manifest.json missing')
    else:
        try:data=json.loads(manifest.read_text());entries=data.get('entries',data.get('files',[]))
        except Exception:data={};entries=[];errors.append('manifest unreadable')
        for e in entries:
            rel=e.get('path');p=root/rel
            if not p.is_file() or sha(p)!=e.get('sha256'):errors.append('manifest mismatch '+str(rel))
    surf=root/'release/production_surface_manifest.json'
    if not surf.is_file() and not (root/'qa/production_surface_manifest.json').is_file():errors.append('production surface manifest missing')
    out={'status':'PASS' if not errors else 'FAIL','errors':errors,'manifest_entries':len(entries) if 'entries' in locals() else 0}
    op=root/a.output;op.parent.mkdir(parents=True,exist_ok=True);op.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2));raise SystemExit(0 if not errors else 1)
if __name__=='__main__':main()
