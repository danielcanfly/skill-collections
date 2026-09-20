# job_scoring examples

## Example 1
User request:
- 把沒打分的都打分

Skill choice:
- `job_scoring`

Expected backend sequence:
1. `v2_tool_bulk_score_new_jobs`

Expected behavior:
- no fetch happens
- only existing unscored rows are targeted

## Example 2
User request:
- backfill missing scores for stored jobs

Skill choice:
- `job_scoring`

Expected behavior:
- score-only path
- no refresh or crawl language in the summary

## Example 3
User request:
- rescore job 123456789

Skill choice:
- `job_scoring`

Expected behavior:
- targeted score or re-score path using `target_job_id`
- response explicitly states whether the target job was scored, missing, or already handled

## Negative example
User request:
- 幫我抓 JobStreet 最近 3 天的 PM 職缺，新的順便打分

Do not use:
- `job_scoring`

Use instead:
- `job_ingestion`
