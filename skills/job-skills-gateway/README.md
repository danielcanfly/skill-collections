> [!WARNING]
> **Status: DEPRECATED**
> This project is preserved for historical/reference purposes and is not recommended for new integrations.
> Snapshot source: `huaihsuanbusiness/job-skills-gateway@b73d16948ff8fe207ae46a92354e392379435c7d`.

# job-skills-gateway

This repository defines a thin **skill layer** that sits between ChatGPT and the existing Make-based execution flows.

## Purpose

The repository does **not** replace Make. It packages the current Make blueprints into four higher-level skills so that ChatGPT can work in a **skill-first** way instead of calling low-level tools directly.

The intended runtime shape is:

1. ChatGPT connects to a thin FastMCP server.
2. The FastMCP server exposes only four skill-level tools.
3. The skill server routes each skill call to one or more Make flows.
4. Make remains the execution layer for scraping, querying, scoring, and output generation.

## Scope

This first version is based on the following Make blueprints:

- `v2_tool_fetch_recent_jobs`
- `v2_tool_bulk_score_new_jobs`
- `v2_tool_query_jobs`
- `v2_tool_generate_job_output`
- internal helper: `v2_helper_resolve_job_reference`

## Skill map

### 1. `job_ingestion`
User intent:
- fetch recent jobs
- refresh a job pool
- score newly ingested jobs after refresh

Uses:
- `v2_tool_fetch_recent_jobs`
- `v2_tool_bulk_score_new_jobs` only after fresh inserts or explicit refresh-scope rescore

### 2. `job_scoring`
User intent:
- score all currently unscored jobs already in storage
- backfill missing scores
- re-score a known stored job

Uses:
- `v2_tool_bulk_score_new_jobs`

### 3. `job_querying`
User intent:
- retrieve shortlist candidates
- filter by score, days, keyword, status, top_k
- rank or sort a job list

Uses:
- `v2_tool_query_jobs`

### 4. `job_decision_support`
User intent:
- analyze whether a job is worth applying to
- generate an application pack
- prepare an interview brief

Uses:
- `v2_tool_generate_job_output`
- internal helper: `v2_helper_resolve_job_reference`

## Why skills live here instead of inside Make

The Make blueprints already behave like stable execution contracts. This repo keeps the **strategy layer** separate from the **execution layer**:

- Make stays responsible for execution and external integrations.
- Skill manifests and instructions stay versioned as plain files.
- The MCP server can load these files before exposing any capability to ChatGPT.
- ChatGPT sees only skill-level entry points, not every raw Make flow.

## Directory guide

- `docs/architecture.md`: target architecture and role boundaries
- `docs/deployment-runbook.md`: deployment plan for Oracle VM + FastMCP
- `docs/make-tool-catalog.md`: tool-by-tool review of the current Make blueprints
- `skills/*/manifest.yaml`: machine-readable skill contract
- `skills/*/instructions.md`: human/model-facing operating instructions
- `skills/*/examples.md`: example user requests and expected use
- `skills/*/eval-notes.md`: failure modes, review notes, and acceptance checks

## Implementation notes

- This repo assumes a future FastMCP server will load these skill files from disk at startup.
- The current Make blueprints should be treated as backend execution tools, not as skills.
- Secrets should not be copied into skill files. Some existing blueprints contain hard-coded authorization headers and should be cleaned before production rollout.
- The MCP tool descriptions in `server.py` must stay aligned with the skill files, because runtime tool selection depends more on exposed tool descriptions than on passive markdown files sitting on disk.

## License

This archived snapshot in `skill-collections` is distributed under the Apache License 2.0. See `LICENSE`.
