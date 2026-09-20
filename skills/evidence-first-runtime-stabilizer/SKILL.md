# Evidence-First Production Runtime Stabilization Skill v2

## Goal

Guide an AI agent through a production runtime incident with machine-enforced phase order and explicit safety blockers.

## Core phases

P0_PREFLIGHT → P1_EVIDENCE_CAPTURED → P2_TIMELINE_BUILT → P3_ROOT_CAUSE_QUALIFIED → P4_ROLLBACK_READY → P5_CLEANUP_QUALIFIED → P6_REPAIR_CANDIDATE_READY → P7_REGRESSION_PASS → P8_RESOURCE_QUALIFICATION_PASS → P9_DEPLOY_READY → P10_PRODUCTION_VALIDATED → P11_FINAL_SOAK_PASS → P12_AUTHORITY_CHECK_PASS → P13_CLOSURE_PASS.

Use `runtime-stabilizer run-next --incident <dir>` repeatedly. A phase is never skipped because it is inconvenient.

## Evidence and uncertainty

Preserve evidence before restart/cleanup. Reconstruct when pressure/latency began. Record `FINAL_TRIGGER` separately from `STRUCTURAL_DEFECT`. Trigger confidence must be PROVEN/HIGH/MEDIUM/LOW/UNKNOWN. A generic diagnosis is only a draft until adjudicated.

## Capabilities

Every adapter publishes capabilities such as kernel OOM visibility, restart count, cgroup memory, swap, process tree, and health. Missing capability is `unknown`; evaluators must not convert it to a successful zero.

## Repair

Prefer workload-shape repair over symptom masking. Examples include bounded concurrency, short-lived worker isolation, single-flight, materialized snapshots, stale-while-revalidate, backpressure, timeouts, queue limits, and correct cache/authority boundaries.

Application repair remains AI/application-specific and must produce a candidate receipt with exact revision/artifact/digest.

## Validation

The exact candidate must pass regression and realistic resource qualification. Production deploy requires an immutable rollback target, a pre-deploy authority snapshot when configured, and explicit incident-bound authorization.

Immediate validation failure should invoke a configured rollback hook.

## Soak

Final soak telemetry is JSONL. Require real elapsed time, runtime health/restart/OOM checks, pressure metrics available from the adapter, real workload/heavy-cycle evidence when relevant, and recovery from peaks. A quiet idle hour is not enough for a repair aimed at expensive background work.

## Privacy

Create two evidence classes:
- private raw forensic bundle;
- redacted, secret-scanned shareable bundle.

Binary evidence is not considered safely redacted merely because text files passed regex replacement.

## Closure

Closure requires final artifact identity, validation, soak, authority comparison when configured, rollback availability, and a closure receipt.

If a required capability or hook is unavailable, close as BLOCKED, not PASS.
