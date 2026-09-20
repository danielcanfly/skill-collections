# Instructions for AI agents

Read `SKILL.md` first.

Use:

```bash
runtime-stabilizer status --incident <dir>
runtime-stabilizer run-next --incident <dir>
```

Never skip a blocked phase by manually editing `incident_state.json`.

Record root cause only after reviewing evidence. Never deploy without the incident-bound authorization gate. If a required hook or capability is unavailable, report BLOCKED rather than inventing evidence.
