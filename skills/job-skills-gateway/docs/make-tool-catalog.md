# Make tool catalog

This catalog documents the current Make blueprints as execution tools.

## Public tools

### 1. `v2_tool_fetch_recent_jobs`
Role:
- scrape recent jobs from JobStreet Singapore
- dedupe against existing `jobs_raw`
- insert new rows
- return ingestion statistics

Key inputs:
- `request_id`
- `session_id`
- `source_channel`
- `actor_id`
- `source_site` (default: `jobstreet`)
- `role_keyword`
- `days`
- `page_from`
- `page_to`

Pre-processing behavior:
- normalizes role aliases such as `pm`, `product manager`, `apm`, `project manager`, and Chinese role names
- derives a `role_path` and `url_array`
- swaps page bounds if needed
- validates request context

Observed backend behavior:
- reads current `job_id` values from `jobs_raw`
- scrapes JobStreet list pages through Zyte extraction
- parses job cards from HTML
- dedupes against existing jobs
- writes new rows into storage
- returns a completed response even when no new rows were inserted

Important response fields:
- `requested_urls`
- `total_extracted_count`
- `total_passed_count`
- `deduped_count`
- `inserted_count`
- `zero_result_pages`
- `jobs`
- `primary_job_id`
- `diagnostic`

Skill fit:
- primary backend tool for `job_ingestion`

### 2. `v2_tool_bulk_score_new_jobs`
Role:
- score one job or a set of unscored jobs from `jobs_raw`

Key inputs:
- `request_id`
- `session_id`
- `source_channel`
- `actor_id`
- `job_id`
- `force_rescore`

Pre-processing behavior:
- normalizes `job_id` into `target_job_id`
- builds a Google Sheets query
- if `force_rescore` is false, filters to rows where `score` is null
- validates request context

Observed backend behavior:
- queries `jobs_raw`
- fetches detail pages through Zyte when a `detail_url` exists
- produces scored job rows with:
  - `job_id`
  - `score`
  - `is_relevant`
  - `relevant_reason`
  - `scored_at`
  - `detail_url`
  - `status`
  - `role`
  - `company`

Important response fields:
- `target_job_id`
- `scored_count`
- `primary_job_id`
- `jobs`

Summary behavior:
- `Scored X jobs.`
- `Scored target job <id>.`
- `Target job <id> was not scored.`
- `All jobs are already scored.`

Skill fit:
- primary backend tool for `job_scoring`
- secondary internal backend tool for `job_ingestion` after fresh inserts

### 3. `v2_tool_query_jobs`
Role:
- query, filter, and rank jobs already present in the store

Key inputs:
- `request_id`
- `session_id`
- `source_channel`
- `actor_id`
- `days`
- `job_status_filter`
- `min_score`
- `keyword_query`
- `top_k`
- `sort_by`
- `sort_order`

Pre-processing behavior:
- converts numeric / blank fields safely
- computes date filtering using Asia/Taipei date logic
- expands some keyword buckets such as:
  - `ai`
  - `fintech`
  - `web3`
  - `internal_tools`
  - `strategy`
  - `product`
  - `chief_of_staff`
- supports numeric job IDs and URLs inside keyword search
- defaults sort preference toward `score` when ranking signals exist, otherwise `posted_at`

Observed response behavior:
- empty result path:
  - status `completed`
  - summary `No jobs found.`
- non-empty result path:
  - summary `Found <n> jobs.`
  - sorts relevant jobs before irrelevant ones
  - returns shortlist-friendly job objects

Important response fields:
- `query_spec`
- `google_query`
- `jobs`
- `count`
- `matched_count`
- `relevant_count`
- `primary_job_id`
- `job_ids`
- `meta.human_summary`

Skill fit:
- primary backend tool for `job_querying`

### 4. `v2_tool_generate_job_output`
Role:
- generate a decision-useful output for a single target job

Required conceptual inputs:
- `user_message_raw`
- `task_type`
- optional job reference:
  - `target_job_id`
  - `target_company`
  - `target_title`

Accepted output modes:
- `analyze_job`
- `generate_application_pack`
- `prepare_interview_brief`

Skill fit:
- primary backend tool for `job_decision_support`
