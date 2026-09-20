#!/usr/bin/env bash
set -euo pipefail
OUT=${1:?}
N=${RS_SOAK_SAMPLES:-61}
I=${RS_SOAK_INTERVAL_SECONDS:-60}
T=${RS_RUNTIME_TARGET:?}

for n in $(seq 1 "$N"); do
  python3 - "$n" "$T" <<'PYCODE' >> "$OUT"
import subprocess,json,datetime,sys
def sh(x): return subprocess.run(x,shell=True,text=True,capture_output=True).stdout.strip()
n=int(sys.argv[1]); t=sys.argv[2]
raw=sh(f"kubectl get {t} -o json")
try:
    d=json.loads(raw)
    statuses=d.get('status',{}).get('containerStatuses',[])
    rest=sum(x.get('restartCount',0) for x in statuses)
    oom=any(x.get('lastState',{}).get('terminated',{}).get('reason')=='OOMKilled' for x in statuses)
    ready=all(x.get('ready',False) for x in statuses) if statuses else None
except Exception:
    rest=None; oom=None; ready=None
print(json.dumps({
  'ts':datetime.datetime.now(datetime.timezone.utc).isoformat(),
  'sample':n,'running':ready,'oom_killed':oom,'restart_count':rest,
  'heavy_processes':None,'public_health_http':None,'public_health_seconds':None,
  'kernel_oom_events':None,
}))
PYCODE
  [[ "$n" -lt "$N" ]] && sleep "$I"
done
