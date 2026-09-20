#!/usr/bin/env bash
set -euo pipefail
OUT=${1:?}
mkdir -p "$OUT"
: "${RS_RUNTIME_TARGET:?}"
date -u --iso-8601=seconds > "$OUT/time.txt"
free -h > "$OUT/free_h.txt"
swapon --show > "$OUT/swap.txt" || true
vmstat 1 5 > "$OUT/vmstat.txt"
ps auxww > "$OUT/ps.txt"
systemctl status "$RS_RUNTIME_TARGET" --no-pager > "$OUT/systemd_status.txt" 2>&1 || true
systemctl show "$RS_RUNTIME_TARGET" > "$OUT/systemd_show.txt"
journalctl -u "$RS_RUNTIME_TARGET" --since '-8 hours' --no-pager > "$OUT/service.log"
journalctl -k --since '-8 hours' --no-pager > "$OUT/kernel.log" 2>/dev/null || true
