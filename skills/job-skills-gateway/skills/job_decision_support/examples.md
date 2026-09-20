# job_decision_support examples

## Example 1
User request:
- 幫我分析 job 123456789 值不值得投

Skill choice:
- `job_decision_support`
- mode: `analyze_job`

Expected behavior:
- resolve job by `target_job_id`
- return fit / mismatch / blocker style output

## Example 2
User request:
- 幫我做這份職缺的 application pack，company 是 ABC，title 是 Senior Product Manager

Skill choice:
- `job_decision_support`
- mode: `generate_application_pack`

Expected behavior:
- resolve by `target_company + target_title`
- if multiple jobs match, block instead of guessing

## Example 3
User request:
- 幫我準備這個職缺的 interview brief，越嚴格越好

Skill choice:
- `job_decision_support`
- mode: `prepare_interview_brief`

Expected behavior:
- strict and realistic interview-prep output
- compact, decision-useful structure

## Negative example
User request:
- 列出最近 3 天 80 分以上的職缺

Do not use:
- `job_decision_support`

Use instead:
- `job_querying`
