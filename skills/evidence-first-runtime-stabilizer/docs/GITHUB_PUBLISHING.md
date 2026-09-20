# GitHub publishing

Suggested repository name:

`evidence-first-runtime-stabilizer`

Suggested description:

`Evidence-first, resumable production runtime incident harness for OOM, swap thrash, restart loops and runaway worker memory.`

Suggested topics:

`incident-response`, `sre`, `devops`, `oom`, `docker`, `kubernetes`, `observability`, `ai-agents`, `production-engineering`

Before publishing:

```bash
python scripts/release_hygiene.py .
python -m unittest discover -s tests -v
```

Do not publish real production evidence as fixtures.
