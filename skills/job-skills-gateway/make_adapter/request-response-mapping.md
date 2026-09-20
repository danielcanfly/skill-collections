# Request / response mapping

This document maps public skills to backend Make flows.

## Mapping overview

### Public skill: `job_ingestion`

Primary backend sequence:
1. `v2_tool_fetch_recent_jobs`
2. optionally `v2_tool_bulk_score_new_jobs`

Input mapping:
- `request_id` -> fetch request context
- `session_id` -> fetch request context
- `trace_id` -> fetch request context
- `source_site` -> fetch
- `role_keyword` -> fetch
- `days` -> fetch
- `page_from` -> fetch
- `page_to` -> fetch
- `force_rescore` -> scoring decision and optional scoring call

Response mapping:
- fetch summary fields bubble up into the public skill response
- if scoring runs, scoring summary fields are appended
- the final skill response should clearly separate ingestion outcome from scoring outcome

### Public skill: `job_querying`

Primary backend sequence:
1. `v2_tool_query_jobs`

Input mapping:
- `request_id` -> query request context
- `session_id` -> query request context
- `trace_id` -> query request context
- `days` -> query
- `job_status_filter` -> query
- `min_score` -> query
- `keyword_query` -> query
- `top_k` -> query
- `sort_by` -> query
- `sort_order` -> query

Response mapping:
- preserve `summary`
- preserve `count`, `matched_count`, `relevant_count`
- preserve `jobs`, `job_ids`, and `primary_job_id` when present
- zero-result outcomes remain successful at the skill level

### Public skill: `job_decision_support`

Primary backend sequence:
1. optional internal `v2_helper_resolve_job_reference`
2. `v2_tool_generate_job_output`

Input mapping:
- `request_id` -> request context
- `session_id` -> request context
- `trace_id` -> request context
- `user_message_raw` -> output tool and/or helper
- `task_type` -> output mode normalization
- `target_job_id` -> helper / output tool
- `target_company` -> helper / output tool
- `target_title` -> helper / output tool

Response mapping:
- preserve normalized mode
- preserve the resolved target job metadata
- preserve output content
- if job resolution is blocked or ambiguous, surface that before output generation runs

## Adapter normalization rules

The adapter should normalize transport-level failures into a small set of server-side categories:
- endpoint_missing
- auth_missing
- timeout
- bad_http_status
- invalid_json
- malformed_backend_result

The adapter should not silently coerce:
- a failed backend call into success
- a missing result envelope into a valid skill response
