# skill-collections

A collection of reusable AI skills, agent workflows, and operational runbooks.

## Skills

| Skill | Status | Description |
|---|---|---|
| [Evidence-First Runtime Stabilizer](skills/evidence-first-runtime-stabilizer/) | Public Beta | Core workflow, CLI, schemas, fixtures, privacy gates and adapters are usable today. Defaults to read-only evidence capture; deployment, rollback and application repair require explicit hooks and authorization. |
| [Job Skills Gateway](skills/job-skills-gateway/) | Deprecated | Legacy job-skills gateway preserved for reference; not recommended for new integrations. |
| [Blog Production Workflow](skills/blog-production-workflow/) | Public Beta | Profile-driven 11+1 editorial workflow with setup contracts, research/drafting/repair/visual/release stages, hardened handoff validation, and independent qualification. |

## Repository policy

- Keep each skill self-contained under `skills/<skill-name>/`.
- Do not commit private production evidence, credentials, tokens, `.env` files, or raw incident bundles.
- Public skills should include clear status, safety boundaries, validation instructions, and release notes.
