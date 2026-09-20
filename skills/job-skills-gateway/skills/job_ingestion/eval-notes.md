# job_ingestion eval notes

## Acceptance checks

- The skill never calls query-only tools.
- The skill does not call scoring when no insert happened unless the user explicitly asked to rescore the freshly fetched scope.
- The final summary distinguishes:
  - extracted rows
  - passed rows
  - deduped rows
  - inserted rows
  - scored rows
- The skill is not used for score-only backfill requests.

## Failure modes to test

1. Missing request context
Expected:
- hard failure

2. Valid fetch request, zero inserted rows
Expected:
- successful completion
- no fabricated scoring result

3. Inserted rows exist, scoring succeeds
Expected:
- both fetch and scoring reflected in the summary

4. User asks to score existing unscored rows without fetching
Expected:
- route away from this skill to `job_scoring`

## Review notes

- This skill should remain deterministic in v1.
- Do not collapse ingestion and score-only backfill into one skill.
- Keep the language operational rather than evaluative.
