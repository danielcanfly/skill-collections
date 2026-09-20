import json,statistics,datetime
from pathlib import Path

def evaluate(path:Path,min_samples=61,min_seconds=3600,require_heavy_cycle=False):
    rows=[]
    errs=[]
    for l in path.read_text().splitlines():
        try:
            rows.append(json.loads(l))
        except Exception:
            errs.append('invalid JSONL telemetry line')

    if len(rows)<min_samples:
        errs.append(f'only {len(rows)} samples')

    if rows:
        try:
            elapsed=(datetime.datetime.fromisoformat(rows[-1]['ts'])-datetime.datetime.fromisoformat(rows[0]['ts'])).total_seconds()
            if elapsed<min_seconds:
                errs.append('duration below minimum')
        except Exception:
            errs.append('timestamp parse failed')

    restart_values=[r.get('restart_count') for r in rows if isinstance(r.get('restart_count'),int)]
    restart_baseline=restart_values[0] if restart_values else None
    for r in rows:
        if r.get('running') is False:
            errs.append(f"sample {r.get('sample')} not running")
        if r.get('oom_killed') is True:
            errs.append(f"sample {r.get('sample')} OOM killed")
        if restart_baseline is not None and isinstance(r.get('restart_count'),int) and r['restart_count']!=restart_baseline:
            errs.append(f"sample {r.get('sample')} restart count changed {restart_baseline}->{r['restart_count']}")
        if isinstance(r.get('kernel_oom_events'),int) and r['kernel_oom_events']>0:
            errs.append(f"sample {r.get('sample')} kernel OOM")
        if isinstance(r.get('public_health_http'),int) and r['public_health_http'] not in (0,200):
            errs.append(f"sample {r.get('sample')} public health {r['public_health_http']}")
        if r.get('runtime_health') not in (None,'','healthy'):
            errs.append(f"sample {r.get('sample')} runtime health {r.get('runtime_health')}")

    heavy=max([r.get('heavy_processes',r.get('python_processes',0)) or 0 for r in rows],default=0)>1
    if require_heavy_cycle and not heavy:
        errs.append('required heavy cycle not observed')

    lat=[r['public_health_seconds'] for r in rows if isinstance(r.get('public_health_seconds'),(int,float))]
    return {
        'status':'PASS' if not errs else 'FAIL',
        'samples':len(rows),
        'errors':errs,
        'heavy_cycle_observed':heavy,
        'restart_count_baseline':restart_baseline,
        'public_health_max_seconds':max(lat,default=None),
        'public_health_p95_seconds':statistics.quantiles(lat,n=20)[18] if len(lat)>=20 else max(lat,default=None),
    }
