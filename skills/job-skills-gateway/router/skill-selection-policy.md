# Skill selection policy

This document defines the first-pass routing policy for the thin skill server.

## Goal

Select exactly one public skill before any backend Make flow is invoked.

Public skills:
- `job_ingestion`
- `job_scoring`
- `job_querying`
- `job_decision_support`

## Why this policy exists

The current Make blueprints are execution tools, not public skills. If ChatGPT sees the raw Make tools directly, it may bypass the intended skill-first behavior. The skill server therefore chooses a skill first, then exposes or invokes only the backend flows allowed by that skill.

## Routing order

### 1. Explicit skill call wins

If the caller invokes a named skill tool directly, respect that choice unless the input is invalid.

Examples:
- `job_ingestion(...)`
- `job_scoring(...)`
- `job_querying(...)`
- `job_decision_support(...)`

### 2. Deterministic routing for freeform requests

If the future server adds a freeform router entrypoint, choose the skill using deterministic keyword and intent matching before considering any model-based routing.

Priority order:
1. `job_decision_support`
2. `job_scoring`
3. `job_ingestion`
4. `job_querying`

This priority is intentional:
- worth-applying analysis is the most semantically specific path
- score-only backfill is more specific than ingestion and should not accidentally fetch
- ingestion changes system state and should not be confused with retrieval
- querying is the broadest and safest read-oriented path

## Skill boundaries

### `job_ingestion`
Use when the user wants to:
- fetch recent jobs
- refresh the candidate pool
- ingest recent JobStreet roles
- score newly fetched jobs as part of refresh

Allowed backend tools:
- `v2_tool_fetch_recent_jobs`
- `v2_tool_bulk_score_new_jobs`

### `job_scoring`
Use when the user wants to:
- score all unscored jobs already in storage
- backfill missing scores
- re-score a known stored job
- score existing jobs without fetching new jobs

Allowed backend tools:
- `v2_tool_bulk_score_new_jobs`

### `job_querying`
Use when the user wants to:
- list jobs already in storage
- filter by days, score, status, keyword, company, title, or job id
- rank or sort a shortlist
- retrieve top-K jobs without generating a deep report

Allowed backend tools:
- `v2_tool_query_jobs`

### `job_decision_support`
Use when the user wants to:
- assess whether a job is worth applying to
- generate an application pack
- prepare an interview brief
- produce a deep single-job output rather than a list

Allowed backend tools:
- `v2_helper_resolve_job_reference` (internal)
- `v2_tool_generate_job_output`

## Conflict resolution

If a request contains signals from multiple skills, resolve them in this order:

1. If the request asks for a single-job report, choose `job_decision_support`.
2. If the request asks to score existing stored jobs without fetching, choose `job_scoring`.
3. If the request asks to fetch or refresh data, choose `job_ingestion`.
4. If the request asks to list, rank, or filter existing jobs, choose `job_querying`.

Examples:
- "幫我把沒打分的都打分" -> route to `job_scoring`
- "抓最近三天 PM 職缺，新的順便打分" -> route to `job_ingestion`
- "列出 80 分以上職缺，並幫我分析第 1 個" -> first route to `job_querying`; the follow-up deep analysis belongs to `job_decision_support`

## Chaining policy

Version 1 of the thin skill server should avoid automatic multi-skill chaining unless the behavior is fully deterministic and reversible.

Recommended v1 rule:
- allow `job_ingestion` to chain internally from fetch -> bulk score
- allow `job_scoring` to call only the bulk scoring backend
- do not chain from `job_querying` into `job_decision_support` automatically
- do not chain from `job_ingestion` into `job_querying` automatically

## Rejection rules

Do not invoke any backend flow when:
- required request context is missing
- the request is too ambiguous to determine the target job for decision support
- the user asks for a capability not covered by the current four skills
