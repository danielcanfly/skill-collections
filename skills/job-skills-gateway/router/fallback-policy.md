# Fallback policy

This file defines what the skill server should do when routing or backend execution cannot complete cleanly.

## Principles

1. Fail early on missing request context.
2. Prefer explicit clarification over silent guessing.
3. Treat zero results differently from true failures.
4. Keep skill-level summaries faithful to backend results.

## Routing fallbacks

### Unknown intent

Condition:
- no skill has a clear deterministic match

Behavior:
- do not call any Make flow
- return a clarification request asking whether the user wants:
  - fetch / refresh
  - shortlist / filter
  - single-job analysis / application / interview help

### Multi-skill intent in one turn

Condition:
- one request asks for both list retrieval and single-job analysis
- one request asks for both fetching and later ranking or analysis

Behavior:
- pick the earliest deterministic skill only if that step is safe and obvious
- otherwise ask the user to split the request into two steps

Recommended v1 default:
- do not auto-chain across public skills

## Backend fallbacks by skill

### `job_ingestion`

If fetch succeeds but inserts zero rows:
- complete successfully
- say that no new rows were inserted
- do not force scoring unless explicitly requested

If fetch returns rows but all are deduped or filtered:
- complete successfully
- mention dedupe/filtering outcome

If scoring returns zero scored rows:
- complete successfully
- mention that scoring ran but no new rows were scored

### `job_querying`

If zero jobs match:
- complete successfully
- return empty list semantics
- preserve counts from backend

If query context is invalid:
- fail clearly
- do not fabricate filters or results

### `job_decision_support`

If job reference resolution is ambiguous:
- do not call the final output generator yet
- ask for one of:
  - job id
  - exact company + title
  - pasted job URL

If job reference resolution fails entirely:
- return a blocked or failed outcome
- do not improvise a target job

If downstream output generation fails after a valid target is found:
- surface failure clearly
- preserve target reference details if safe to do so

## Security fallbacks

If the adapter is missing a required endpoint or secret:
- fail immediately at the server boundary
- do not attempt partial execution
- do not expose secret names in the user-facing summary beyond high-level labels

## Logging guidance

When a fallback is triggered, log:
- skill name
- request_id
- trace_id
- fallback reason category
- backend tool involved if any

Avoid logging:
- raw secrets
- full authorization headers
- unnecessary personal data
