# Project Status

Status: **Public Beta**.

The core workflow, CLI, schemas, fixtures, privacy gates and adapters are usable today. It defaults to read-only evidence capture. Deployment, rollback and application repair require explicit user-provided hooks and authorization.

Mature:

- Evidence-first workflow.
- Resumable incident state.
- Adapter capability checks.
- Hook-based authority/probe/regression/resource/deploy/rollback model.
- JSONL soak evaluation.
- Privacy/redaction and secret scanning.

Still adapter/application dependent:

- Application code repair.
- Production deployment.
- Rollback implementation.
- Authenticated operator probes.
- Authority snapshot semantics.

Default posture: read-only. Mutation/deploy must be explicitly configured and authorized.
