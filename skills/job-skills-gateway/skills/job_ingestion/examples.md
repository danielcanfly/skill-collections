# job_ingestion examples

## Example 1
User request:
- 幫我抓 JobStreet 最近 3 天的 PM 職缺，新的順便打分

Skill choice:
- `job_ingestion`

Expected backend sequence:
1. `v2_tool_fetch_recent_jobs`
2. if inserted_count > 0, `v2_tool_bulk_score_new_jobs`

Expected response shape:
- scope: JobStreet / PM / last 3 days / pages 1-3
- inserted_count reported
- scored_count reported if scoring ran

## Example 2
User request:
- refresh Singapore product manager jobs for the last 7 days

Skill choice:
- `job_ingestion`

Expected behavior:
- fetch recent rows
- no scoring if inserted_count is zero and no rescore was requested

## Example 3
User request:
- 幫我更新最近 5 天的 data engineer 職缺，抓到新的就補分

Skill choice:
- `job_ingestion`

Expected behavior:
- fetch first
- score only if newly inserted rows exist

## Negative example 1
User request:
- 把沒打分的都打分

Do not use:
- `job_ingestion`

Use instead:
- `job_scoring`

## Negative example 2
User request:
- 列出 80 分以上的 AI 職缺

Do not use:
- `job_ingestion`

Use instead:
- `job_querying`
