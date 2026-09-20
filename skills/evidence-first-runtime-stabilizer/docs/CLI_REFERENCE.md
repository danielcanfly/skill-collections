# CLI Reference

Core commands:

- `init --config CONFIG --root DIR [--id ID]`
- `status --incident DIR`
- `run-next --incident DIR [--config CONFIG]`
- `run-until-blocked --incident DIR [--max-steps N]`
- `retry-blocked --incident DIR`
- `diagnose-evidence EVIDENCE_DIR`
- `record-root-cause --incident DIR --trigger TEXT --confidence LEVEL --structural-defect TEXT`
- `record-candidate --incident DIR --revision REV --artifact ARTIFACT --digest DIGEST`
- `evaluate-soak LOG [--require-heavy-cycle]`
- `redact SRC DST`
- `print-capabilities --config CONFIG`
- `validate-state INCIDENT_DIR`
