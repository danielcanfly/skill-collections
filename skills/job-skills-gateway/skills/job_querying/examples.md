# job_querying examples

## Example 1
User request:
- 列出最近 7 天 AI 類職缺，80 分以上，按分數排序

Skill choice:
- `job_querying`

Expected behavior:
- call `v2_tool_query_jobs`
- preserve:
  - days = 7
  - keyword_query = ai
  - min_score = 80
  - sort_by = score
  - sort_order = desc

## Example 2
User request:
- show me the top 10 product jobs

Skill choice:
- `job_querying`

Expected behavior:
- query existing stored jobs
- return a ranked shortlist from the current store

## Example 3
User request:
- find job 123456789

Skill choice:
- `job_querying`

Expected behavior:
- allow numeric ID matching through the backend query logic

## Negative example
User request:
- 幫我分析這份職缺值不值得投

Do not use:
- `job_querying`

Use instead:
- `job_decision_support`
