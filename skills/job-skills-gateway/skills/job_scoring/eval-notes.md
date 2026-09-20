# job_scoring eval notes

## Acceptance checks

- The skill uses only `v2_tool_bulk_score_new_jobs`.
- The skill never calls a fetch or refresh backend.
- Score-only requests do not get routed to `job_ingestion`.
- The final summary distinguishes:
  - score-only backfill
  - targeted re-score
  - zero eligible jobs

## Failure modes to test

1. Missing request context
Expected:
- hard failure

2. Score-only request where all jobs are already scored
Expected:
- successful completion
- explicit no-op style summary

3. Targeted re-score request for an unknown job id
Expected:
- successful completion with clear not-found note, or a faithful backend failure if the backend treats it as hard failure

4. Valid targeted re-score request
Expected:
- scored_count and primary_job_id are preserved faithfully

## Review notes

- This skill exists to stop score-only requests from accidentally routing into fetch-first ingestion.
- Keep the language operational rather than evaluative.
- Do not blur the boundary between score maintenance and refresh.
