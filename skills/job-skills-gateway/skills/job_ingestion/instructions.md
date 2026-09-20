# job_ingestion instructions

You are handling **job pool refresh** tasks.

## Objective

Fetch recent jobs from the supported source, record what changed, and score newly inserted items when appropriate.

## What this skill is for

Use this skill when the user's intent is to:
- fetch recent jobs
- refresh a role-specific job pool
- bring in recent jobs from JobStreet
- score newly ingested jobs as part of the refresh flow

Do not use this skill for:
- shortlist retrieval from already stored jobs
- worth-applying analysis for a single job
- interview prep
- application pack generation
- score-only requests against jobs that are already stored
- requests like 「把沒打分的都打分」 or "rescore existing jobs"

## Backend tools

This skill may use only:
- `v2_tool_fetch_recent_jobs`
- `v2_tool_bulk_score_new_jobs`

## Required execution logic

1. Normalize the user request into fetch parameters:
   - source site
   - role keyword
   - day range
   - page range
2. Call `v2_tool_fetch_recent_jobs`.
3. Read the fetch result carefully.
4. If there are newly inserted rows, call `v2_tool_bulk_score_new_jobs`.
5. If there are no inserted rows, do not force a scoring call unless the user explicitly asked to rescore the freshly fetched scope.
6. Return a concise operational summary.

## Response style

Keep the response decision-useful and operational:
- what source and role were used
- what date window and page range were used
- how many rows were extracted
- how many new rows were inserted
- how many were deduped
- whether scoring ran
- how many rows were scored

## Important rules

- Do not pretend that deduped rows are new rows.
- Do not say “no jobs found” if rows were extracted but filtered or deduped.
- Do not infer scoring results from fetch results alone.
- If the backend returns an invalid request context, surface that as a failure instead of improvising.
- If the user wants to backfill or rescore existing stored rows without fetching, route to `job_scoring` instead.

## Preferred summary structure

- Fetch scope
- Ingestion outcome
- Scoring outcome
- Any operational caveat

## Caveats to mention when relevant

- zero result pages were encountered
- all passed rows already existed
- extracted rows were filtered out before insertion
- target job was not found for scoring
