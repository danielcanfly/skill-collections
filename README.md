# skill-collections

A collection of reusable AI skills, agent workflows, and operational runbooks.

## Skills

| Skill | Status | Description |
|---|---|---|
| [Evidence-First Runtime Stabilizer](skills/evidence-first-runtime-stabilizer/) | Beta | Evidence-first runtime incident stabilizer for Linux services. Defaults to read-only evidence capture; mutation, deployment, rollback and application repair require explicit hooks and authorization. |

## Repository policy

- Keep each skill self-contained under `skills/<skill-name>/`.
- Do not commit private production evidence, credentials, tokens, `.env` files, or raw incident bundles.
- Public skills should include clear status, safety boundaries, validation instructions, and release notes.
