# Support matrix

| Runtime | Evidence | Soak telemetry | Restart/OOM | Host memory/swap | Notes |
|---|---|---|---|---|---|
| Docker Linux | Built in | Built in | Strong | Strong | Primary reference adapter |
| systemd Linux | Built in | Built in | Partial/strong by platform | Strong | OOMKilled is not always directly attributable |
| Kubernetes | Built in | Built in | Strong for pod/container restart/OOMKilled | Partial | Node/kernel visibility may require extra privileges |
| Custom | Contract | Contract | Unknown until declared | Unknown until declared | Must provide capability manifest |

Application repair/deploy/authority checks are provided through hooks.


Kubernetes note: built-in soak telemetry is trustworthy only for a Pod target. Higher-level workload objects require a custom adapter.
