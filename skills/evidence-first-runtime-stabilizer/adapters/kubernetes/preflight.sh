#!/usr/bin/env bash
set -euo pipefail
: "${RS_RUNTIME_TARGET:?}"
kind=$(kubectl get "$RS_RUNTIME_TARGET" -o jsonpath='{.kind}')
[[ "$kind" == "Pod" ]] || {
  echo "BLOCKED: built-in Kubernetes adapter requires a Pod target for trustworthy restart/OOM/ready soak telemetry; got kind=$kind" >&2
  exit 40
}
kubectl get "$RS_RUNTIME_TARGET" -o wide
