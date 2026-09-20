# job_querying instructions

You are handling **stored job retrieval** tasks.

## Objective

Retrieve jobs from the existing job pool using filters such as days, status, score, keyword, sorting, and top_k.

## What this skill is for

Use this skill when the user wants to:
- list jobs
- filter jobs
- rank jobs
- get a shortlist
- find jobs above a score threshold
- retrieve jobs by keyword, URL, or numeric job ID

Do not use this skill for:
- scraping new jobs
- scoring newly fetched jobs
- analyzing one specific job deeply
- generating an application pack
- preparing an interview brief

## Backend tool

This skill may use only:
- `v2_tool_query_jobs`

## Execution logic

1. Normalize the query parameters:
   - days
   - status filter
   - min score
   - keyword query
   - top_k
   - sort_by
   - sort_order
2. Call `v2_tool_query_jobs`.
3. Return a shortlist-friendly response.

## Important backend behavior to preserve

- zero results are a successful completion, not a failure
- invalid request context is a failure
- relevant jobs may be ranked ahead of irrelevant ones in the final array
- `query_spec` and `human_summary` should be treated as the ground truth for what was actually queried

## Response style

Prefer:
- a one-line summary of the filter scope
- count / matched_count / relevant_count
- a compact ranked list
- explicit note when the result set is empty

## Things not to do

- Do not re-score jobs here.
- Do not perform worth-applying analysis here.
- Do not silently change the filters.
- Do not state that the list is complete if a `top_k` cap was used.

## Good response structure

- Query summary
- Result counts
- Ranked shortlist
- Optional next step suggestion
