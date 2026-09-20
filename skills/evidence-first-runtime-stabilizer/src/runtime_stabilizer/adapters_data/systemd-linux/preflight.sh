#!/usr/bin/env bash
set -euo pipefail
: "${RS_RUNTIME_TARGET:?}"
systemctl show "$RS_RUNTIME_TARGET" -p ActiveState -p SubState -p NRestarts -p MainPID
