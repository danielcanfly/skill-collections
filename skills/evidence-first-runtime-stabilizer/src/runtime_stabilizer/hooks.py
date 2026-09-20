from __future__ import annotations
import subprocess,shlex,os
from pathlib import Path

def get(cfg,name):
    return cfg.get('hooks',{}).get(name,'').strip()

def _resolve_command(cfg,cmd):
    parts=shlex.split(cmd)
    if not parts:
        return cmd
    first=Path(parts[0])
    if not first.is_absolute() and ('/' in parts[0] or parts[0].startswith('.')):
        base=Path(cfg.get('_meta',{}).get('config_dir','.'))
        parts[0]=str((base/first).resolve())
        return shlex.join(parts)
    return cmd

def run(cfg,name,*args,required=True):
    cmd=get(cfg,name)
    if not cmd:
        if required:
            raise RuntimeError(f'MISSING_HOOK:{name}')
        return None
    cmd=_resolve_command(cfg,cmd)
    env=os.environ.copy()
    env.update({f'RS_HOOK_ARG_{i}':str(v) for i,v in enumerate(args)})
    return subprocess.run(cmd,shell=True,text=True,capture_output=True,env=env)
