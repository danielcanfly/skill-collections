#!/usr/bin/env bash
set -euo pipefail
: "${RS_RUNTIME_TARGET:?RS_RUNTIME_TARGET missing}"
docker inspect "$RS_RUNTIME_TARGET" --format 'running={{.State.Running}} oom={{.State.OOMKilled}} restart={{.RestartCount}} health={{if .State.Health}}{{.State.Health.Status}}{{end}} image={{.Image}}'
