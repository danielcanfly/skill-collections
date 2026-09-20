# Custom adapter contract

Provide executable `preflight.sh`, `collect.sh`, `soak.sh`, and a `capabilities.json`.

`soak.sh OUTPUT.jsonl` should emit one JSON object per sample.

Unknown fields must be JSON `null`, not invented zeros. See `schemas/telemetry.schema.json` and the built-in adapters.
