> **HISTORICAL MIGRATION REFERENCE ONLY. Do not execute these commands under v9. Use `21_V8_TO_V9_PRODUCTION_TRUST_CHAIN_HARDENING.md` and `22_V9_AGENT_USAGE_RECIPES.md`.**

> **Historical migration reference only. Do not execute this workflow in v7.**

# v4 → v5 Upgrade and External Integration Decision

## Why v5 was necessary

Real Phase 7–10 returns exposed contract drift: the v4 package embedded Audit OS v2 but generated v1-style candidate paths and receipts. Additional failures included source-note circular proof, aggregate PASS masking individual incomplete sources, empty lineage with PASS receipts, direct-support saturation, temporal date filling, empty active evidence families, composite claims, and split uppercase/lowercase seal states.

## External packages reviewed

Two packages from an unrelated external domain were reviewed only for transferable mechanisms. Their domain content was not imported. The following mechanisms were integrated:

1. Global semantic template saturation diagnosis and de-templating.
2. Explicit evidence-boundary taxonomy: exact span, section locator, document level, package lineage, bounded synthesis, unsupported.
3. Retrieval benchmark leakage detection and frozen benchmark tiering.
4. Multi-surface release identity audit across KOS, OKF, R2, production and audit bundles.
5. Residual claim-gap registry and evidence-honest global repair.
6. R0–R8 bounded global semantic/evidence seal workflow.

Domain-specific nodes, claims, examples and release artifacts are excluded from universal core. An anonymised lesson profile is stored under `profiles/reference_cases/`.

## Breaking changes

- `modules/audit_os_v3_independent_semantic/` → `modules/audit_os_v3_independent_semantic/`
- Canonical child runtime is now single-source `modules/child_runtime/`.
- `research/provenance_edge_entailment.csv` is forbidden; use `research/edge_entailment.csv`.
- `qa/SEAL_STATE.json` is forbidden; use `qa/seal_state.json`.
- Predispatch validation checks exact Audit v2.1 schemas and runtime certification.
- Final sealing uses two-stage fresh extraction and read-only final audit.
