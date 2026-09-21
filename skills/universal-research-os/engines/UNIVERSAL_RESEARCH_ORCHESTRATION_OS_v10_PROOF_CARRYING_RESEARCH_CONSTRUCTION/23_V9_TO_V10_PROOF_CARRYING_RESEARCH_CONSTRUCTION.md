# v9 → v10: Proof-Carrying Research Construction

v9 was strong at detecting and containing bad packages after completion, but real KPIOC and BFA audits showed 95%–98% first-pass direct-support failure, repeated repair loops, runtime contract drift and global/handoff gaps.

v10 changes the dependency graph: source evidence and external stage proof precede claim and node compilation. It also introduces a production-grade Handoff Compiler, approved legacy migration and an executable Global Builder.

## Systemic defects closed
- claim-first evidence backfill
- candidate self-review treated as proof
- child/audit validator divergence
- retrieval producer/consumer mismatch
- missing source-note depth and case-independence parity
- false receipt completion flags
- missing `sealed_at`
- 0/0 direct-support false perfect score
- finding-local repair
- inventory-only global reconciliation
- handoff prose without machine control plane

## v10 External Stage Proof
Direct-support construction requires an external `external_stage_review/STAGE_REVIEW_IDENTITY.json` plus full-population passage and clause review tables. The reviewer ID and Session ID must differ from the Research Builder. A self-filled PASS field is not proof.
