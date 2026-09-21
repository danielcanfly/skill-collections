# Integrated Postmortem: Nine Audit Packages → v10

The KPIOC F/K/G reports, BFA global parity report and KPIOC handoff parity report show a single systemic pattern: v9 detected errors after package completion but did not constrain their creation. First-pass direct-support failure reached 95%–98%; repairs frequently closed examples rather than classes; runtime producers and audit consumers disagreed; global packages lacked exact upstream materialisation; and repair handoffs lacked machine control planes.

## v10 mapping
- overclaim → source/passage/clause pre-review before claim compilation
- synthetic evidence → immutable snapshots, hashes and typed locators
- self-review masking → external stage receipts and candidate Audit remain separate
- runtime drift → canonical validator lock and parity tests
- retrieval mismatch → ranked_ids/query/corpus hash in producer and consumer
- missing sealed_at → one finalizer and receipt-derived completion flags
- zero denominator → no compiled direct claim means failure, not100
- finding-local repair → failure-class population selectors and protected baselines
- global inventory-only → exact production releases materialised into one canonical tree
- handoff prose-only → Handoff Compiler with identity, manifest, Gate0, diff and return inventory
