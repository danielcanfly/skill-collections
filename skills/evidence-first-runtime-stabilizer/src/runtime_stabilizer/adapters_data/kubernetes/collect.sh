#!/usr/bin/env bash
set -euo pipefail
OUT=${1:?}
mkdir -p "$OUT"
: "${RS_RUNTIME_TARGET:?}"
kubectl get "$RS_RUNTIME_TARGET" -o yaml > "$OUT/target.yaml"
kubectl describe "$RS_RUNTIME_TARGET" > "$OUT/describe.txt" 2>&1 || true
kubectl get events --sort-by=.lastTimestamp > "$OUT/events.txt" 2>&1 || true
kubectl top pods -A > "$OUT/top_pods.txt" 2>&1 || true
