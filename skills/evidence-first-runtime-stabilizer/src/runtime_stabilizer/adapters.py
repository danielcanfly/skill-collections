from pathlib import Path
import json,subprocess

ADAPTERS=Path(__file__).resolve().parent/'adapters_data'

def adapter_dir(cfg):
    runtime=cfg.get('runtime',{})
    explicit=str(runtime.get('adapter_path','')).strip()
    if explicit:
        p=Path(explicit)
        if not p.is_absolute():
            base=Path(cfg.get('_meta',{}).get('config_dir','.'))
            p=(base/p).resolve()
        return p
    return ADAPTERS/runtime['adapter']

def capabilities(cfg):
    p=adapter_dir(cfg)/'capabilities.json'
    if not p.exists():
        return {}
    caps=json.loads(p.read_text())
    # A built-in adapter may technically support public health while the
    # incident configuration intentionally omits a URL. Treat that signal as
    # unavailable instead of silently reporting success with HTTP=0.
    if caps.get('public_health') is True and not str(cfg.get('runtime',{}).get('health_url','')).strip():
        caps['public_health']=False
    return caps

def run_adapter(cfg,action,*args):
    p=adapter_dir(cfg)/(action+'.sh')
    if not p.exists():
        raise RuntimeError(f'MISSING_ADAPTER_ACTION:{action}:{p}')
    if not p.is_file():
        raise RuntimeError(f'INVALID_ADAPTER_ACTION:{action}:{p}')
    from .config import env_from
    try:
        return subprocess.run([str(p),*map(str,args)],env=env_from(cfg),text=True,capture_output=True)
    except PermissionError as e:
        raise RuntimeError(f'ADAPTER_ACTION_NOT_EXECUTABLE:{p}') from e

def required_signal_gaps(caps, required, *, allow_partial=False, require_heavy_cycle=False):
    accepted={True}
    if allow_partial:
        accepted.add('partial')
    gaps=[name for name in required if caps.get(name) not in accepted]
    if require_heavy_cycle and caps.get('heavy_processes') not in accepted:
        gaps.append('heavy_processes(required_by_soak)')
    return gaps
