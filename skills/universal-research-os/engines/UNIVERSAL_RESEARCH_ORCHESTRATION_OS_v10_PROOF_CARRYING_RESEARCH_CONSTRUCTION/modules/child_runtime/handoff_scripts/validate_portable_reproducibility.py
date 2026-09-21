#!/usr/bin/env python3
from pathlib import Path
import argparse,json,re,shutil,tempfile,subprocess,sys,os,hashlib
from common import result,emit,load_json,sha256_file

ap=argparse.ArgumentParser(); ap.add_argument('root'); ap.add_argument('--config'); ap.add_argument('--profile'); ap.add_argument('--output'); a=ap.parse_args()
root=Path(a.root).resolve(); profile=load_json(a.profile,{}) if a.profile else {}; errors=[]; warnings=[]
contract=load_json(root/'qa/reproduction_contract.json',{})
if not contract: errors.append('missing qa/reproduction_contract.json')
if contract and contract.get('root_resolution')!='script-relative': errors.append('reproduction root_resolution must be script-relative')
commands=contract.get('commands',[]) if isinstance(contract,dict) else []
required=set(profile.get('required_reproduction_commands',['retrieval']))
ids={str(c.get('id','')) for c in commands if isinstance(c,dict)}
for rid in sorted(required-ids): errors.append(f'missing required reproduction command {rid}')

# Scan executable production/retrieval/build scripts, not prose or this validator itself.
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

# Commands are executed only in an isolated copy. Generated outputs must be byte-identical.
if commands and not errors:
    with tempfile.TemporaryDirectory() as td:
        clone=Path(td)/root.name; shutil.copytree(root,clone)
        env=os.environ.copy(); env['PYTHONDONTWRITEBYTECODE']='1'; env['SOURCE_DATE_EPOCH']=str(contract.get('source_date_epoch',0)); env['TZ']='UTC'; env['LC_ALL']='C.UTF-8'
        for c in commands:
            cid=str(c.get('id','')); argv=c.get('argv'); cwd=str(c.get('cwd','.')); outputs=c.get('outputs',[])
            if not isinstance(argv,list) or not argv: errors.append(f'{cid}: argv must be a non-empty list'); continue
            if Path(cwd).is_absolute() or '..' in Path(cwd).parts: errors.append(f'{cid}: cwd must be relative and contained'); continue
            rendered=[]
            for token in argv:
                token=str(token)
                if token=='{python}': rendered.append(sys.executable)
                else:
                    token=token.replace('{root}',str(clone))
                    # Literal absolute paths are forbidden. The generated clone root is allowed only via {root}.
                    if Path(token).is_absolute() and not token.startswith(str(clone)): errors.append(f'{cid}: literal absolute argv path forbidden: {token}')
                    rendered.append(token)
            original_hash={rel:sha256_file(root/rel) for rel in outputs if (root/rel).is_file()}
            if len(original_hash)!=len(outputs): errors.append(f'{cid}: declared output missing before reproduction'); continue
            try:
                proc=subprocess.run(rendered,cwd=clone/cwd,env=env,capture_output=True,text=True,timeout=int(profile.get('reproduction_timeout_seconds',240)))
            except Exception as e:
                errors.append(f'{cid}: reproduction execution failed: {e}'); continue
            if proc.returncode!=0: errors.append(f'{cid}: reproduction command returned {proc.returncode}: {(proc.stderr or proc.stdout)[-500:]}'); continue
            for rel,expected in original_hash.items():
                fp=clone/rel
                if not fp.is_file(): errors.append(f'{cid}: output missing after reproduction: {rel}')
                elif sha256_file(fp)!=expected: errors.append(f'{cid}: non-deterministic output hash: {rel}')
emit(result('PASS' if not errors else 'FAIL',errors,warnings,{'commands':len(commands),'required_commands':sorted(required),'scanned_executable_files':len(scan)}),a.output)
