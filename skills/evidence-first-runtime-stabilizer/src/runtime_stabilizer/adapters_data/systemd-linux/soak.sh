#!/usr/bin/env bash
set -euo pipefail
OUT=${1:?}
N=${RS_SOAK_SAMPLES:-61}
I=${RS_SOAK_INTERVAL_SECONDS:-60}
S=${RS_RUNTIME_TARGET:?}
URL=${RS_RUNTIME_HEALTH_URL:-}
START=$(date -u +%FT%TZ)

for n in $(seq 1 "$N"); do
  python3 - "$n" "$S" "$URL" "$START" <<'PYCODE' >> "$OUT"
import subprocess,json,datetime,sys
def sh(x): return subprocess.run(x,shell=True,text=True,capture_output=True).stdout.strip()
n=int(sys.argv[1]); svc=sys.argv[2]; url=sys.argv[3]; start=sys.argv[4]
vals={}
for l in sh(f"systemctl show {svc} -p ActiveState -p NRestarts -p MainPID").splitlines():
    if '=' in l:
        k,v=l.split('=',1); vals[k]=v
h=sh(f"curl -sS -o /dev/null -w '%{{http_code}}|%{{time_total}}' --max-time 5 {url}").split('|') if url else ['0','0']
oom=sh(f"journalctl -k --since '{start}' --no-pager 2>/dev/null | grep -Eic 'oom-kill|Out of memory|Killed process' || true")
print(json.dumps({
  'ts':datetime.datetime.now(datetime.timezone.utc).isoformat(),
  'sample':n,
  'running':vals.get('ActiveState')=='active',
  'oom_killed':None,
  'restart_count':int(vals['NRestarts']) if vals.get('NRestarts','').isdigit() else None,
  'heavy_processes':None,
  'public_health_http':int(h[0]) if h[0].isdigit() else None,
  'public_health_seconds':float(h[1]) if len(h)>1 else None,
  'kernel_oom_events':int(oom or 0),
}))
PYCODE
  [[ "$n" -lt "$N" ]] && sleep "$I"
done
