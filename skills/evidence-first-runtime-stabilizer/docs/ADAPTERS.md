# Adapters

Each adapter provides `capabilities.json`, `preflight.sh`, `collect.sh`, and `soak.sh`.

Capability values may be `true`, `false`, `partial`, `hook`, or `unknown`.

`unknown` means the evaluator cannot make a positive claim from that signal. Never replace unknown with zero.

Built-ins:
- docker-linux
- systemd-linux
- kubernetes
- custom

## External custom adapters

Set `runtime.adapter = "custom"` and `runtime.adapter_path` to a directory containing:

- `capabilities.json`
- `preflight.sh`
- `collect.sh`
- `soak.sh`

Relative paths resolve from the incident TOML file. Missing actions block the phase with `MISSING_ADAPTER_ACTION` instead of being treated as success.

## Capability values

- `true`: supported and suitable for a required signal.
- `false` / `unknown`: unavailable.
- `partial`: informative but not accepted for a required signal unless `allow_partial_required_signals=true`.
- `hook`: reserved for project-specific integration and should not be considered satisfied until implemented by the project.

## Kubernetes safety boundary

The built-in Kubernetes adapter intentionally requires a **Pod** target during preflight. Deployment/StatefulSet targets do not expose the container-level restart/OOM/ready fields this soak evaluator needs directly, so the adapter blocks instead of silently treating missing telemetry as healthy. Use a Pod target or provide a project-owned custom adapter that resolves workload pods explicitly.
