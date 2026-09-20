# Evidence-First Runtime Stabilizer v3.0.0

Status: **Public Beta**.

The core workflow, CLI, schemas, fixtures, privacy gates and adapters are usable today. It defaults to read-only evidence capture. Deployment, rollback and application repair require explicit user-provided hooks and authorization.

Evidence-First Runtime Stabilizer is a CLI and agent skill for production runtime incidents: OOM, swap thrash, restart loops, slow operator reads, and heavy-worker overlap. It is designed for AI-assisted incident response, but it deliberately defaults to read-only evidence capture and explicit gates before cleanup, deployment or rollback.

## Install from source

```bash
git clone <your-fork-url> evidence-first-runtime-stabilizer
cd evidence-first-runtime-stabilizer
python3 -m pip install -e .
runtime-stabilizer --version
pytest
```

## Quick start

```bash
runtime-stabilizer init --config config/runtime-stabilizer.example.toml --root ./incidents --id demo
runtime-stabilizer run-until-blocked --incident ./incidents/demo
runtime-stabilizer status --incident ./incidents/demo
```

Most real incidents block at root-cause adjudication or repair candidate creation because application-specific reasoning is required. That is intentional. This tool is not a magical auto-fixer; it is an evidence-first controller, adapter layer, hook runner, soak evaluator, privacy pipeline and safety rail for AI/operator workflows.

## What v3 adds

- CLI-first package shape with `runtime-stabilizer` entry point.
- JSON schemas for incident state, phase receipts, telemetry and adapter capabilities.
- Docker Compose, systemd and Kubernetes fixture directories for examples and future integration tests.
- Capability-aware adapters with explicit gaps instead of pretending missing signals equal zero.
- JSONL telemetry and heavy-cycle-aware soak evaluation.
- Privacy/redaction pipeline and release hygiene checks.
- Beta status documentation and GitHub publishing checklist.

## Safety model

1. Evidence before cleanup.
2. Rollback snapshot before mutation.
3. Human/AI adjudication for root cause and app-specific repair.
4. Deploy requires explicit environment authorization.
5. Final closure requires soak, production validation and authority checks when configured.
6. Shareable bundles must be redacted and secret-scanned.

See `docs/QUICKSTART.md` and `docs/AUTONOMY.md`.

## License

Apache License 2.0. See `LICENSE`.
