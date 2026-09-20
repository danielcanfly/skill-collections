# Make adapter endpoints

This file defines the endpoint strategy for the thin skill server.

## Recommendation

The skill server should call Make through server-side HTTP endpoints or webhooks.
Do not expose these endpoints directly to ChatGPT.

## Recommended endpoint variables

The adapter layer should read the following environment variables:
- `MAKE_FETCH_RECENT_JOBS_URL`
- `MAKE_BULK_SCORE_NEW_JOBS_URL`
- `MAKE_QUERY_JOBS_URL`
- `MAKE_GENERATE_JOB_OUTPUT_URL`
- `MAKE_TIMEOUT_SECONDS`

Optional helper endpoint:
- `MAKE_RESOLVE_JOB_REFERENCE_URL`

## Endpoint policy

- one backend flow per endpoint variable
- all endpoint values live in server-side configuration
- no endpoint URLs inside skill manifests
- no endpoint URLs leaked to clients through tool descriptions

## Invocation shape

Recommended request shape:
- HTTP POST
- JSON body
- includes request context plus skill-specific arguments

Recommended response shape:
- pass through Make's `result` envelope with minimal transformation
- normalize transport errors into a consistent server-side exception class

## Why this adapter exists

The adapter gives you a stable seam between:
- the public MCP skill interface, and
- the private Make execution layer

That seam lets you:
- rotate Make webhooks without changing skill files
- swap Make for another execution engine later
- centralize auth, retries, timeout, and logging policy
