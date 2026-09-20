# Contract: `v2_tool_fetch_recent_jobs`

## Purpose

Fetch recent jobs from the configured source site and normalize an ingestion summary.

## Current role in the system

This is a backend execution tool used by the public `job_ingestion` skill.
It is not a public skill by itself.

## Inputs

Required request context:
- `request_id`
- `session_id`
- `trace_id`

Optional execution inputs:
- `source_channel` (default `chatgpt`)
- `actor_id`
- `parent_run_id`
- `source_site` (expected default `jobstreet`)
- `role_keyword`
- `days`
- `page_from`
- `page_to`

## Expected behavior

The tool should:
1. validate request context
2. normalize the role keyword
3. compute the effective day and page range
4. assemble source URLs for the crawl
5. fetch / process the target pages
6. return a summary of extraction and insertion results

## Output envelope

The tool returns a `result` envelope with top-level fields such as:
- `ok`
- `status`
- `tool_name`
- `request_id`
- `trace_id`
- `run_id`
- `summary`
- `data`
- `error`
- `meta`

## Data fields the skill layer should preserve

Expected summary-useful fields include:
- `inserted_count`
- `total_extracted_count`
- `deduped_count`
- `zero_result_pages`
- `primary_job_id`
- crawl scope information such as source, role, days, and page range

## Success semantics

A successful completion does not require inserted rows.
These are all distinct outcomes:
- rows extracted and some inserted
- rows extracted but all deduped
- rows extracted but all filtered
- no rows found on some or all requested pages

## Failure semantics

Hard failure examples:
- missing or invalid request context
- invalid page range or unusable request input
- upstream crawl failure severe enough that no trustworthy result can be returned

## Skill-layer notes

The public `job_ingestion` skill should:
- treat zero inserts as a valid completion state
- avoid claiming scoring happened until the scoring tool actually runs
- mention dedupe/filter outcomes separately from insertion outcomes
