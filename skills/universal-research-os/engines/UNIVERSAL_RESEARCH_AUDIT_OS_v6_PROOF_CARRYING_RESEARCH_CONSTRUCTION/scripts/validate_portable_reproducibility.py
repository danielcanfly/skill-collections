#!/usr/bin/env python3
from pathlib import Path
import argparse, json, re, shutil, tempfile, subprocess, sys, os
from common import result, emit, load_json, sha256_file

ap=argparse.ArgumentParser()
ap.add_argument('root'); ap.add_argument('--config'); ap.add_argument('--profile'); ap.add_argument('--output')
a=ap.parse_args(); root=Path(a.root).resolve(); profile=load_json(a.profile,{}) if a.profile else {}; errors=[]; warnings=[]; stats={}
contract=load_json(root/'qa/reproduction_contract.json',{})
if not contract: errors.append('missing qa/reproduction_contract.json')
if contract and contract.get('root_resolution')!='script-relative': errors.append('reproduction root_resolution must be script-relative')
commands=contract.get('commands',[]) if isinstance(contract,dict) else []
required=set(profile.get('required_reproduction_commands',['retrieval']))
ids={str(c.get('id','')) for c in commands if isinstance(c,dict)}
for rid in sorted(required-ids): errors.append(f'missing required reproduction command {rid}')

abs_re=re.compile(r'(?<![A-Za-z0-9_])(?:/mnt/data/|/Users/[^/\s]+/|/home/[^/\s]+/|[A-Za-z]:\\\\|file:///)',re.I)
scan=[]
for base in [root/'qa',root/'scripts',root/'tools',root/'bin']:
    if not base.exists(): continue
    for p in base.rglob('*'):
        if not p.is_file() or p.suffix.lower() not in {'.py','.sh','.bash','.zsh','.js','.mjs','.ts'}: continue
        if p.name.startswith('validate_') or p.name in {'fresh_extraction_selfcheck.py','verify_manifest_readonly.py'}: continue
        if any(k in p.name.lower() for k in ['retrieval','build','package','release','ingest','compile','reproduce','finalize']): scan.append(p)
for p in scan:
    text=p.read_text(encoding='utf-8',errors='replace')
    if abs_re.search(text): errors.append(f'{p.relative_to(root)}: hard-coded machine/workspace path detected')

cleaned_outputs=0; regenerated_outputs=0
if commands and not errors:
    with tempfile.TemporaryDirectory() as td:
        clone=Path(td)/root.name; shutil.copytree(root,clone)
        env=os.environ.copy(); env['PYTHONDONTWRITEBYTECODE']='1'; env['SOURCE_DATE_EPOCH']=str(contract.get('source_date_epoch',0)); env['TZ']='UTC'; env['LC_ALL']='C.UTF-8'
        for c in commands:
            cid=str(c.get('id','')); argv=c.get('argv'); cwd=str(c.get('cwd','.')); outputs=c.get('outputs',[])
            if not isinstance(argv,list) or not argv: errors.append(f'{cid}: argv must be a non-empty list'); continue
            if not isinstance(outputs,list) or not outputs: errors.append(f'{cid}: outputs must be a non-empty list'); continue
            if Path(cwd).is_absolute() or '..' in Path(cwd).parts: errors.append(f'{cid}: cwd must be relative and contained'); continue
            rendered=[]
            for token in argv:
                token=str(token)
                if token=='{python}': rendered.append(sys.executable)
                else:
                    token=token.replace('{root}',str(clone))
                    if Path(token).is_absolute() and not token.startswith(str(clone)): errors.append(f'{cid}: literal absolute argv path forbidden: {token}')
                    rendered.append(token)
            originals={}
            safe_outputs=[]
            for rel in outputs:
                rel=str(rel); rp=Path(rel)
                if rp.is_absolute() or '..' in rp.parts or rel in {'','.','/'}:
                    errors.append(f'{cid}: invalid output path {rel}'); continue
                src=(root/rp).resolve(); dst=(clone/rp).resolve()
                if root not in src.parents or clone not in dst.parents:
                    errors.append(f'{cid}: output escapes candidate root: {rel}'); continue
                if not src.is_file():
                    errors.append(f'{cid}: declared canonical output missing before reproduction: {rel}'); continue
                originals[rel]=sha256_file(src); safe_outputs.append((rel,dst))
            if len(safe_outputs)!=len(outputs): continue
            # V9 clean-build invariant: declared outputs must not exist when the command starts.
            for rel,dst in safe_outputs:
                if dst.is_dir(): shutil.rmtree(dst)
                elif dst.exists(): dst.unlink()
                cleaned_outputs+=1
                if dst.exists(): errors.append(f'{cid}: failed to remove pre-existing output: {rel}')
            if errors: continue
            try:
                proc=subprocess.run(rendered,cwd=clone/cwd,env=env,capture_output=True,text=True,timeout=int(profile.get('reproduction_timeout_seconds',240)))
            except Exception as e:
                errors.append(f'{cid}: reproduction execution failed: {e}'); continue
            if proc.returncode!=0:
                errors.append(f'{cid}: reproduction command returned {proc.returncode}: {(proc.stderr or proc.stdout)[-500:]}'); continue
            for rel,dst in safe_outputs:
                if not dst.is_file(): errors.append(f'{cid}: output was not regenerated from clean state: {rel}')
                elif sha256_file(dst)!=originals[rel]: errors.append(f'{cid}: regenerated output hash differs from canonical output: {rel}')
                else: regenerated_outputs+=1
stats={'commands':len(commands),'required_commands':sorted(required),'scanned_executable_files':len(scan),'cleaned_outputs':cleaned_outputs,'regenerated_outputs':regenerated_outputs,'clean_rebuild_enforced':True}
emit(result('PASS' if not errors else 'FAIL',errors,warnings,stats),a.output)
