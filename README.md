# skill-collections

A public collection of reusable AI skills, agent workflows, and operational runbooks.

This repository is organized as a catalog. Each skill lives under `skills/<skill-name>/` with its own README, status, usage notes, and source package.

## Skills

| Skill | Status | Purpose |
|---|---|---|
| [`evidence-first-runtime-stabilizer`](skills/evidence-first-runtime-stabilizer/) | Beta | Evidence-first runtime incident stabilization for Linux services, with adapters, hooks, JSONL telemetry, redaction, state machine, and soak validation. |

## Repository conventions

Each skill directory should include:

- `README.md` for humans
- `SKILL.md` for AI agents
- `STATUS.md` or validation notes
- `docs/` for longer explanations
- `src/`, `scripts/`, `adapters/`, or `hooks/` when the skill includes executable tooling
- privacy and safety notes when the skill touches production systems, credentials, evidence, logs, or user data

## Current import status

The first catalog entry is **Evidence-First Runtime Stabilizer Public v3.0.0**. Its package checksum is recorded in `skills/evidence-first-runtime-stabilizer/PACKAGE.md`.
