# Deployment runbook

This runbook assumes the skill server will be deployed on an Oracle VM and will call Make as a backend execution layer.

## End state

A public HTTPS endpoint is available at:

- `https://<your-domain>/mcp`

ChatGPT connects to that endpoint.
The FastMCP server loads the skill files in this repo.
The server then calls Make flows through an internal adapter.

## Deployment stages

### Stage 1. Repository preparation
Prepare this repository first.

Required contents:
- `skills/`
- deployment docs
- backend tool catalog
- future FastMCP app code

Acceptance check:
- the repo clearly defines only four skill entry points

### Stage 2. Oracle VM readiness
Confirm the Oracle VM is suitable for a public MCP endpoint.

Checklist:
- public IP assigned
- outbound internet access works
- SSH access works
- security list / NSG allows inbound 443
- DNS plan exists if you want a custom domain

Acceptance check:
- the VM can host a public HTTPS service

### Stage 3. FastMCP application
Create a thin Python + FastMCP app that does the following:

- loads all skill manifests and instructions from `skills/`
- exposes only:
  - `job_ingestion`
  - `job_scoring`
  - `job_querying`
  - `job_decision_support`
- routes each skill call to the appropriate Make adapter method
- does not expose raw Make flow names to ChatGPT

Acceptance check:
- tool discovery from the MCP endpoint shows only the four skill tools

### Stage 4. Make adapter
Implement a backend adapter that maps skill calls to Make flows.

Recommended mapping:
- `job_ingestion`
  - first: `v2_tool_fetch_recent_jobs`
  - then: `v2_tool_bulk_score_new_jobs` when inserted rows > 0
- `job_scoring`
  - `v2_tool_bulk_score_new_jobs`
- `job_querying`
  - `v2_tool_query_jobs`
- `job_decision_support`
  - `v2_tool_generate_job_output`

Acceptance check:
- each skill call can be traced to one or more Make flow calls

### Stage 5. Secret handling
Before going live, remove any hard-coded credentials from blueprints or server code.

Move all secrets into one of:
- Oracle VM environment variables
- a secrets manager
- Make-managed connections
- server-side secure configuration

Do not store secrets in:
- `manifest.yaml`
- `instructions.md`
- `examples.md`
- `eval-notes.md`

Acceptance check:
- no secret material exists in this repo
- no secret material is baked into a skill definition

### Stage 6. Process management
Run the FastMCP app as a long-lived service.

Operational requirements:
- auto restart on failure
- startup on reboot
- central log path
- health check endpoint if you add one
- clear separation between public HTTPS entry and internal app process

Acceptance check:
- the service survives VM restart and process crashes

### Stage 7. HTTPS entrypoint
Expose the FastMCP service behind HTTPS.

Recommended shape:
- reverse proxy or HTTPS frontend
- internal app listens on a private port
- public endpoint serves `/mcp`

Acceptance check:
- `https://<your-domain>/mcp` is reachable from outside your VM

### Stage 8. ChatGPT connector setup
In ChatGPT developer mode:

1. create a connector / app
2. enter the public MCP endpoint
3. verify tool discovery
4. run smoke tests for all four skills

Acceptance check:
- ChatGPT can connect successfully
- only the four skill tools are visible
- raw Make tools are not directly visible

## Smoke test plan

### Smoke test A. Ingestion
User request:
- “Fetch recent PM jobs from JobStreet for the last 3 days and score anything new.”

Expected:
- `job_ingestion` is used
- server calls fetch first, then score if needed
- response summarizes inserted and scored counts

### Smoke test B. Score-only backfill
User request:
- “把沒打分的都打分。”

Expected:
- `job_scoring` is used
- server calls only `v2_tool_bulk_score_new_jobs`
- no fetch flow is invoked

### Smoke test C. Querying
User request:
- “Show me AI jobs from the last 7 days with score >= 80.”

Expected:
- `job_querying` is used
- response includes shortlist-friendly job rows and counts

### Smoke test D. Decision support
User request:
- “Analyze whether job 123456789 is worth applying to.”

Expected:
- `job_decision_support` is used
- job reference is resolved
- output mode is `analyze_job`
