# Evidence-First Runtime Stabilizer

**Status:** Public v3.0.0 beta release candidate

Evidence-First Runtime Stabilizer is a production-runtime incident skill for AI agents and human operators. It is designed for Linux services that may suffer from OOM kills, swap thrashing, slow health/read paths, restart loops, expensive worker overlap, or ambiguous production instability.

The skill defaults to evidence-first, read-only investigation. Deployment, rollback, cleanup, and application-specific repair require explicit hooks and authorization.

## What it is for

Use this skill when a service shows symptoms such as:

- container or service OOM kills
- swap saturation or swap-thrashing behavior
- slow admin/operator endpoints
- production restart loops
- memory pressure from overlapping workers
- unclear runtime degradation where the final trigger and structural defect may differ

## Core workflow

The v3 workflow is organized as a state machine:

1. Preflight
2. Evidence capture
3. Incident timeline
4. Root-cause classification
5. Rollback readiness
6. Safe cleanup census
7. Repair planning
8. Regression and resource qualification
9. Deploy gate
10. Production validation
11. Soak monitoring
12. Authority comparison
13. Closure receipt

The key rule is simple: **do not clean, restart, deploy, or declare victory before preserving evidence and proving the actual production runtime recovered.**

## Public-package source

This entry corresponds to `EVIDENCE_FIRST_RUNTIME_STABILIZER_PUBLIC_v3.0.0.zip`.

Package checksum:

```text
74c87b6fa3a8d751904ef49e17835dd40e45d80e06ae0a190f5882859c97e8c4
```

## Import note

This catalog entry records the Public v3 package and its intended repository location. If the full generated package is not yet expanded here, import the ZIP contents into this directory while preserving the package checksum and validation report.
