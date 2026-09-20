# Intent signals

This file records the main routing signals used by the deterministic router.

## `job_ingestion`

Primary English signals:
- fetch recent jobs
- refresh jobs
- update jobs
- scrape jobs
- ingest jobs
- latest JobStreet jobs
- recent JobStreet jobs

Primary Chinese signals:
- 抓最近職缺
- 更新職缺
- 刷新職缺池
- 抓 JobStreet 職缺
- 幫我更新新職缺
- 拉最近幾天職缺

Parameter-like clues:
- source site
- role keyword
- days
- page_from
- page_to

## `job_scoring`

Primary English signals:
- score unscored jobs
- score all unscored
- backfill scores
- rescore stored jobs
- rescore existing jobs
- score only
- rescore job 123456789

Primary Chinese signals:
- 把沒打分的都打分
- 補打分
- 未打分
- 空白分數
- 重打分
- 幫我重打某筆 job 的分數

Parameter-like clues:
- target_job_id
- force_rescore

## `job_querying`

Primary English signals:
- list jobs
- show jobs
- filter jobs
- rank jobs
- shortlist jobs
- top jobs
- jobs above score
- find job
- search stored jobs

Primary Chinese signals:
- 列出職缺
- 篩選職缺
- 找高分職缺
- 80 分以上職缺
- shortlist
- 幫我排序職缺
- 找某個 job id

Parameter-like clues:
- days
- min_score
- job_status_filter
- keyword_query
- top_k
- sort_by
- sort_order

## `job_decision_support`

Primary English signals:
- worth applying
- should I apply
- analyze this job
- application pack
- interview brief
- interview prep
- tailor my CV
- generate application material

Primary Chinese signals:
- 值不值得投
- 幫我分析這份職缺
- 幫我做投遞包
- 幫我準備面試
- 面試 brief
- 客製履歷
- 分析這個 job

Parameter-like clues:
- target_job_id
- target_company
- target_title
- user_message_raw

## Ambiguous signals

These phrases are not enough on their own and need additional evidence:
- "幫我看一下工作"
- "幫我處理職缺"
- "find something good"
- "幫我整理一下"

Use context clues:
- if the request asks for a list -> `job_querying`
- if the request asks to fetch or update external jobs -> `job_ingestion`
- if the request asks to backfill or rescore existing stored jobs -> `job_scoring`
- if the request asks for a single-job judgment or output artifact -> `job_decision_support`

## Anti-signals

### Do not route to `job_ingestion` when:
- the user only wants an existing shortlist
- the request clearly references a known job id already in storage
- the request is score-only and does not ask to fetch new jobs

### Do not route to `job_scoring` when:
- the user clearly asks to fetch or refresh recent external jobs
- the user asks for a ranked list rather than score maintenance

### Do not route to `job_querying` when:
- the user asks for deep analysis or interview help
- the request starts with "fetch", "refresh", or "score all unscored"

### Do not route to `job_decision_support` when:
- the user is clearly asking for a list or ranking of multiple jobs
- no specific target job can be resolved and the request is not asking for deep analysis
