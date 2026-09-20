# job_decision_support eval notes

## Acceptance checks

- Only the three canonical task types are accepted.
- Missing job reference becomes a blocked state.
- Ambiguous match becomes a blocked state.
- The skill does not expose the internal helper as a public skill.
- Output mode remains faithful to the selected task type.

## Failure modes to test

1. Missing request context
Expected:
- failed status

2. Unsupported task type
Expected:
- blocked status with unsupported task type handling

3. Missing job reference
Expected:
- blocked status with no fabricated resolution

4. Multiple matching jobs
Expected:
- blocked status with clarification need

5. Valid target job and analyze mode
Expected:
- completed path with analysis-oriented output

6. Valid target job and interview mode
Expected:
- completed path with interview-specific structure

## Review notes

- Keep this skill focused on one target job at a time.
- Do not merge shortlist retrieval into this skill.
- Preserve the backend’s strict style: realistic, compact, no invented facts.
