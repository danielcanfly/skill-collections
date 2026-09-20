# Contract: `v2_tool_bulk_score_new_jobs`

## Purpose

Score newly inserted jobs, score all currently unscored jobs, or re-score a targeted stored job when explicitly requested.

## Current role in the system

This is a backend execution tool used by the public `job_scoring` skill.
It is also used internally by `job_ingestion` after fresh inserts.
It is not a raw public Make tool.

## Inputs

Required request context:
- `request_id`
- `session_id`
- `trace_id`

Optional execution inputs:
- `source_channel` (default `chatgpt`)
- `actor_id`
- `parent_run_id`
- `target_job_id`
- `force_rescore`

## Expected behavior

The tool should:
1. validate request context
2. determine the scoring scope
   - targeted single-job re-score, or
   - all currently unscored jobs, or
   - newly inserted not-yet-scored jobs after ingestion
3. execute the scoring path
4. return counts and identifiers that let the skill layer summarize what happened

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
- `scored_count`
- `primary_job_id`
- target resolution details if a specific job was requested
- a jobs array or other per-row scoring summary when returned

## Success semantics

These are all different valid outcomes:
- new jobs were scored after ingestion
- all currently unscored jobs were backfilled
- a targeted job was re-scored
- scoring ran but zero jobs met the scoring criteria

## Failure semantics

Hard failure examples:
- missing request context
- targeted job could not be located when the request required it
- downstream scoring service unavailable or invalid

## Skill-layer notes

The public `job_scoring` skill should:
- use this tool directly for score-only requests
- allow explicit user-triggered re-score even if no fresh ingestion occurred
- avoid implying that jobs were fetched in this path

The public `job_ingestion` skill should:
- only call this automatically after fetch when new rows were inserted
- avoid implying that every fetched job was scored
