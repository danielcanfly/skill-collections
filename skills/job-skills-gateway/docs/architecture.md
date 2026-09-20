# Architecture

## Target system

The recommended system has three layers:

### 1. ChatGPT
ChatGPT is the top-level host and user-facing orchestrator. It should **not** connect directly to the raw Make tool flows.

### 2. Thin skill server
A thin FastMCP server sits in front of Make and does four things:

1. loads skill files from `skills/`
2. exposes only skill-level tools
3. applies lightweight routing and tool-allow rules
4. translates each skill call into one or more Make flow invocations

### 3. Make execution layer
Make remains the execution layer for:
- scraping recent jobs
- scoring jobs
- querying jobs
- generating job-specific output

## Connection shape

```text
ChatGPT
  -> FastMCP skill server
  -> Make adapter
  -> Make flows
```

## Role boundaries

### ChatGPT
Responsible for:
- interacting with the user
- deciding when to call a skill
- passing structured intent and parameters into the skill server

Not responsible for:
- directly calling low-level Make tools
- reading skill files from GitHub by itself
- managing execution secrets

### FastMCP skill server
Responsible for:
- skill-first capability exposure
- loading manifests and instructions from disk
- enforcing which backend tools a given skill may use
- small-step orchestration across Make flows

Not responsible for:
- replacing Make as the execution runtime
- storing production secrets in plain files
- becoming a large workflow engine on day one

### Make
Responsible for:
- tool execution
- Sheets / datastore / HTTP integrations
- existing business logic embedded in the blueprints

Not responsible for:
- owning the skill registry
- deciding which skill ChatGPT should use first

## Skill-to-tool mapping

### `job_ingestion`
Primary job:
- refresh the candidate pool

Underlying execution plan:
1. call `v2_tool_fetch_recent_jobs`
2. if new rows were inserted, call `v2_tool_bulk_score_new_jobs`
3. summarize what was fetched, inserted, deduped, and scored

### `job_scoring`
Primary job:
- score jobs already stored in the system

Underlying execution plan:
1. call `v2_tool_bulk_score_new_jobs`
2. summarize whether the run backfilled unscored rows or re-scored a specific target job

### `job_querying`
Primary job:
- return filtered / ranked job lists from the existing store

Underlying execution plan:
1. call `v2_tool_query_jobs`
2. return shortlist-friendly output with count, matched_count, relevant_count, and job_ids

### `job_decision_support`
Primary job:
- produce a decision-useful output for a specific job

Underlying execution plan:
1. normalize the requested output mode
2. resolve the target job reference
3. assemble the downstream prompt context
4. generate one of:
   - analyze job
   - application pack
   - interview brief

## Why this design is recommended

This is the most conservative upgrade path because:

- it keeps your current Make investment intact
- it creates a clean place to version skill definitions
- it avoids asking ChatGPT to “please remember to read a skill file first”
- it makes it possible to hide raw Make tools from ChatGPT entirely
- it leaves room to migrate the orchestration layer later without rewriting the skills

## Security boundary

The skill layer should contain:
- manifests
- instructions
- examples
- evaluation notes

The skill layer should not contain:
- API secrets
- Basic Auth values
- service account credentials
- direct Make connection internals

Observed risk from the current blueprints:
- at least some Make flows contain hard-coded Authorization headers for Zyte extraction. This should be moved into a secure connection layer before production use.

## Internal helper policy

`v2_helper_resolve_job_reference` should remain an internal helper. It is not a public skill and should not be advertised directly to ChatGPT.

It is acceptable for `job_decision_support` to depend on this helper internally because the helper:
- resolves `target_job_id`, or
- resolves `target_company + target_title`, or
- returns blocked / ambiguous states when reference resolution fails
