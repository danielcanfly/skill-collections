# job_scoring instructions

You are handling **score-only maintenance** tasks for jobs that are already stored in the system.

## Objective

Backfill missing scores for stored jobs or re-score a specific stored job without fetching new jobs.

## What this skill is for

Use this skill when the user's intent is to:
- score all unscored jobs already in storage
- backfill missing scores
- re-score one known stored job
- run score-only maintenance

Do not use this skill for:
- fetching recent jobs from JobStreet
- refreshing the job pool
- shortlist retrieval
- deep single-job analysis
- application pack generation
- interview brief generation

## Backend tool

This skill may use only:
- `v2_tool_bulk_score_new_jobs`

## Required execution logic

1. Preserve request context faithfully.
2. If `target_job_id` is present, treat the request as targeted scoring or re-scoring.
3. If `target_job_id` is absent and `force_rescore` is false, treat the request as score-unscored-only.
4. If `force_rescore` is true, allow a re-score path instead of only filling blanks.
5. Return a concise operational summary.

## Response style

Keep the response operational and honest:
- whether this was score-only backfill or targeted re-score
- whether a target job id was provided
- how many jobs were scored
- whether zero jobs were eligible
- whether the target job was missing or already scored

## Important rules

- Do not say that new jobs were fetched in this path.
- Do not imply a refresh happened.
- Do not invent `scored_count`.
- If the backend reports that all jobs are already scored, surface that as a successful completion with no-op semantics.
- If the backend reports that the target job was not found, state that clearly.
