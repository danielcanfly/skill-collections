#!/usr/bin/env bash
set -euo pipefail
OUT=${1:?output dir}
mkdir -p "$OUT"
: "${RS_RUNTIME_TARGET:?}"

date -u --iso-8601=seconds > "$OUT/time.txt"
uname -a > "$OUT/uname.txt"
uptime > "$OUT/uptime.txt"
free -h > "$OUT/free_h.txt"
cat /proc/meminfo > "$OUT/proc_meminfo.txt"
swapon --show > "$OUT/swap.txt" || true
vmstat 1 5 > "$OUT/vmstat.txt"
cat /proc/pressure/memory > "$OUT/psi_memory.txt" 2>/dev/null || true
df -h > "$OUT/df_h.txt"
ps auxww > "$OUT/ps.txt"
pstree -ap > "$OUT/pstree.txt" 2>/dev/null || true
docker ps -a --no-trunc > "$OUT/docker_ps.txt"
docker stats --no-stream > "$OUT/docker_stats.txt"
docker inspect "$RS_RUNTIME_TARGET" > "$OUT/target_inspect.json"
docker top "$RS_RUNTIME_TARGET" -eo pid,ppid,stat,etime,rss,cmd > "$OUT/target_top.txt" 2>/dev/null || true
docker logs --since 8h "$RS_RUNTIME_TARGET" > "$OUT/target_logs.txt" 2>&1 || true
journalctl -k --since '-8 hours' --no-pager > "$OUT/kernel.log" 2>/dev/null || true
