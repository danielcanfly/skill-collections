# Contract: `v2_tool_generate_job_output`

## Purpose

Generate a single-job output for one of three high-level modes:
- job analysis
- application pack generation
- interview brief generation

## Current role in the system

This is the main backend execution tool used by the public `job_decision_support` skill.
It may rely on internal helper flows such as job reference resolution.
It is not a public skill by itself.

## Inputs

Required request context:
- `request_id`
- `session_id`
- `trace_id`

Common optional inputs:
- `source_channel` (default `chatgpt`)
- `actor_id`
- `parent_run_id`
- `user_message_raw`
- `task_type`
- `target_job_id`
- `target_company`
- `target_title`

## Expected behavior

The tool should:
1. validate request context
2. normalize task type aliases into one of:
   - `analyze_job`
   - `generate_application_pack`
   - `prepare_interview_brief`
3. resolve the target job reference directly or via helper
4. assemble downstream prompt/context inputs
5. generate the requested single-job output

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
- normalized mode / task type
- resolved target job reference
- output text or structured payload
- blocked or ambiguous resolution state when present

## Success semantics

A successful completion requires:
- a valid target job reference
- a valid output mode
- downstream output generation to finish successfully

## Failure semantics

Hard failure examples:
- missing request context
- ambiguous or missing target job reference
- invalid task type after normalization
- downstream extraction or generation failure

## Skill-layer notes

The public `job_decision_support` skill should:
- ask for clarification when a target job cannot be resolved
- never invent a target job
- preserve the selected mode faithfully
- keep job resolution helper behavior internal to the skill server
