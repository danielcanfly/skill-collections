# Contract: `v2_tool_query_jobs`

## Purpose

Retrieve jobs already stored in the system using deterministic filters and ranking preferences.

## Current role in the system

This is a backend execution tool used by the public `job_querying` skill.
It is not a public skill by itself.

## Inputs

Required request context:
- `request_id`
- `session_id`
- `trace_id`

Optional execution inputs:
- `source_channel` (default `chatgpt`)
- `actor_id`
- `parent_run_id`
- `days`
- `job_status_filter`
- `min_score`
- `keyword_query`
- `top_k`
- `sort_by`
- `sort_order`

## Expected behavior

The tool should:
1. validate request context
2. normalize query filters
3. query the stored job pool
4. rank or sort the returned jobs
5. return result counts and the final job list

## Output envelope

The tool returns a `result` envelope with top-level fields such as:
- `ok`
- `status`
- `tool_name`
- `request_id`
- `trace_id`
- `run_id`
- `summary`
- `data`
- `error`
- `meta`

## Data fields the skill layer should preserve

Expected summary-useful fields include:
- `count`
- `matched_count`
- `relevant_count`
- `primary_job_id`
- `job_ids`
- `jobs`
- `query_spec`
- `human_summary`

## Success semantics

Zero results are a successful completion, not a backend failure.

## Failure semantics

Hard failure examples:
- missing request context
- invalid filter values serious enough to make the query untrustworthy
- downstream storage/query layer unavailable

## Skill-layer notes

The public `job_querying` skill should:
- preserve the backend's counts and query summary
- not re-score or fetch jobs in this path
- clearly state when a top-K cap affects completeness
