# Evidence-First Runtime Stabilizer Skill

Use this skill for runtime incidents involving OOM kills, swap thrashing, restart loops, slow operator/admin reads, heavy worker overlap, or unclear production degradation.

## Operating principle

Preserve evidence before cleanup. Distinguish the final trigger from the structural defect. Do not declare closure from tests alone; verify the deployed production runtime.

## Default mode

Start in read-only mode. Mutation steps require explicit authorization and compatible hooks.

## State machine

1. `P0_PREFLIGHT`
2. `P1_EVIDENCE_CAPTURED`
3. `P2_TIMELINE_BUILT`
4. `P3_ROOT_CAUSE_CLASSIFIED`
5. `P4_ROLLBACK_READY`
6. `P5_CLEANUP_CENSUS`
7. `P6_REPAIR_PLAN`
8. `P7_REGRESSION_PASS`
9. `P8_RESOURCE_QUALIFICATION_PASS`
10. `P9_DEPLOY_READY`
11. `P10_PRODUCTION_VALIDATED`
12. `P11_SOAK_PASS`
13. `P12_AUTHORITY_UNCHANGED`
14. `P13_CLOSURE_PASS`

## Hard-stop conditions

Stop and require human review when any of these occur:

- evidence capture fails
- rollback anchor is missing
- production authority drifts unexpectedly
- candidate image digest does not match the deploy receipt
- authenticated production probe is unavailable when required
- secret scan fails
- soak observes OOM, restart, failed health, non-recovering swap, or stuck heavy workers
- cleanup would delete data without a prior census and explicit approval

## Required closure evidence

A valid closure must include:

- final commit or artifact identity
- runtime image or deploy identity
- pre/post authority comparison
- successful production health checks
- authenticated operator/API probe when applicable
- resource qualification receipt
- soak monitor receipt
- rollback receipt
- final closure receipt

## Public package

This catalog entry corresponds to the generated Public v3 package recorded in `PACKAGE.md`.
