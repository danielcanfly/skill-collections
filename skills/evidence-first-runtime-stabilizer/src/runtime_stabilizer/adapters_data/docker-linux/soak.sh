#!/usr/bin/env bash
set -euo pipefail
OUT=${1:?output jsonl}
: "${RS_RUNTIME_TARGET:?}"
N=${RS_SOAK_SAMPLES:-61}
I=${RS_SOAK_INTERVAL_SECONDS:-60}
URL=${RS_RUNTIME_HEALTH_URL:-}
START=$(date -u +%FT%TZ)

for n in $(seq 1 "$N"); do
  python3 - "$n" "$START" "$RS_RUNTIME_TARGET" "$URL" <<'PYCODE' >> "$OUT"
import json,subprocess,sys,datetime
n=int(sys.argv[1]); start=sys.argv[2]; c=sys.argv[3]; url=sys.argv[4]
def sh(x): return subprocess.run(x,shell=True,text=True,capture_output=True).stdout.strip()

s=sh(f"docker inspect {c} --format '{{{{.State.Running}}}}|{{{{.State.OOMKilled}}}}|{{{{.RestartCount}}}}|{{{{if .State.Health}}}}{{{{.State.Health.Status}}}}{{{{end}}}}'").split('|')
top=sh(f"docker top {c} -eo rss,cmd")
heavy=sum(1 for x in top.splitlines()[1:] if any(k in x.lower() for k in ('python','node','java','worker')))
mem=sh("free -m | awk '/^Mem:/{print $7} /^Swap:/{print $3 \"|\" $2}'").splitlines()
sw=mem[1].split('|') if len(mem)>1 else ['-1','-1']
h=sh(f"curl -sS -o /dev/null -w '%{{http_code}}|%{{time_total}}' --max-time 5 {url}").split('|') if url else ['0','0']
oom=sh(f"journalctl -k --since '{start}' --no-pager 2>/dev/null | grep -Eic 'oom-kill|Out of memory|Killed process' || true")

print(json.dumps({
  'ts':datetime.datetime.now(datetime.timezone.utc).isoformat(),
  'sample':n,
  'running':s[0]=='true' if s else None,
  'oom_killed':s[1]=='true' if len(s)>1 else None,
  'restart_count':int(s[2]) if len(s)>2 and s[2].isdigit() else None,
  'runtime_health':s[3] if len(s)>3 else None,
  'host_mem_available_mib':int(mem[0]) if mem else None,
  'swap_used_mib':int(sw[0]),
  'swap_total_mib':int(sw[1]),
  'heavy_processes':heavy,
  'public_health_http':int(h[0]) if h[0].isdigit() else None,
  'public_health_seconds':float(h[1]) if len(h)>1 else None,
  'kernel_oom_events':int(oom or 0),
}))
PYCODE
  [[ "$n" -lt "$N" ]] && sleep "$I"
done
