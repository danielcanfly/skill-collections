# Auth and secrets

This repository must not contain live secrets.

## Where secrets belong

Secrets should live in server-side configuration only, such as:
- Oracle VM environment variables
- a secrets manager
- Make-managed authenticated connections

## Sensitive values that must stay out of the repo

- Make webhook tokens
- Basic Auth credentials
- Zyte or extraction service credentials
- datastore or spreadsheet API keys
- any session cookies or bearer tokens

## Environment variable guidance

Recommended categories:
- Make endpoint URLs
- Make shared secret or token if needed
- request timeout settings
- optional logging or environment flags

## Rotation guidance

When a secret changes:
1. update server-side configuration
2. restart the service if required
3. do not modify skill manifests or examples to carry the new value

## Logging guidance

Allowed in logs:
- which endpoint category was called
- request_id
- trace_id
- timeout or response status category

Not allowed in logs:
- raw Authorization headers
- full signed URLs with secrets
- full request payloads if they contain sensitive data

## Existing blueprint risk to fix

At least some existing Make flows have used hard-coded authorization material in HTTP headers. Before production rollout, move that auth into:
- a Make connection
- a server-side secret
- or another secure runtime config layer
