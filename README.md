# skill-collections

A collection of reusable AI skills, agent workflows, and operational runbooks.

## Skills

| Skill | Status | License | Description |
|---|---|---|---|
| [Evidence-First Runtime Stabilizer](skills/evidence-first-runtime-stabilizer/) | Public Beta | Apache-2.0 | Core workflow, CLI, schemas, fixtures, privacy gates and adapters are usable today. Defaults to read-only evidence capture; deployment, rollback and application repair require explicit hooks and authorization. |
| [Job Skills Gateway](skills/job-skills-gateway/) | Deprecated | Apache-2.0 | Legacy job-skills gateway preserved for reference; not recommended for new integrations. |
| [Blog Production Workflow](skills/blog-production-workflow/) | Public Beta | Apache-2.0 | Profile-driven 11+1 editorial workflow with setup contracts, research/drafting/repair/visual/release stages, hardened handoff validation, and independent qualification. |

## Related Projects

| Project | Location | Description |
|---|---|---|
| Jobs Scraper | [danielcanfly/jobs-scraper](https://github.com/danielcanfly/jobs-scraper) | LinkedIn job scraper and tracking toolkit for product-management roles, with CLI, local MCP server, Agent Skill, and an optional Google Sheet workflow. Maintained in its own repository and not bundled into this collection. |

## License policy

Current repository contents are licensed under the Apache License 2.0 unless a nested `LICENSE` states otherwise. Each skill keeps its own `LICENSE` so it remains self-contained when copied or redistributed.

Historical releases or commits may retain earlier license grants. See `LICENSE_POLICY.md` for details.

## Repository policy

- Keep each skill self-contained under `skills/<skill-name>/`.
- Do not commit private production evidence, credentials, tokens, `.env` files, or raw incident bundles.
- Public skills should include clear status, safety boundaries, validation instructions, and release notes.
