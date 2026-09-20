# job_querying eval notes

## Acceptance checks

- The skill uses only `v2_tool_query_jobs`.
- Empty results are returned as successful completion, not backend failure.
- The response preserves backend counts:
  - count
  - matched_count
  - relevant_count

## Failure modes to test

1. Missing request context
Expected:
- failed status surfaced clearly

2. Empty result set
Expected:
- completed status
- empty jobs array
- “No jobs found.” style summary

3. Query by keyword bucket such as `ai`
Expected:
- backend bucket expansion is respected

4. Query by numeric job ID or URL
Expected:
- exact or URL-based matching path remains possible

## Review notes

- This skill should never fetch new jobs.
- This skill should never call `v2_tool_generate_job_output`.
- Summaries should remain compact and shortlist-oriented.
