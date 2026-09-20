import tomllib
from pathlib import Path

def load(path):
    path=Path(path).resolve()
    with open(path,'rb') as f:
        cfg=tomllib.load(f)
    cfg['_meta']={'config_dir':str(path.parent),'config_path':str(path)}
    return cfg

def env_from(cfg):
    import os
    e=os.environ.copy()
    for section,vals in cfg.items():
        if section.startswith('_') or not isinstance(vals,dict):
            continue
        for k,v in vals.items():
            if isinstance(v,(str,int,float,bool)):
                e[f'RS_{section}_{k}'.upper()]=str(v).lower() if isinstance(v,bool) else str(v)
    return e
