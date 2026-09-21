---
name: universal-research-os
description: "Run rigorous proof-carrying research construction, orchestration, admission, independent audit, bounded repair, legacy migration, global reconciliation, production promotion, and release workflows using the preserved Universal Research Orchestration OS v10.0.0 and Audit OS v6.0.0. Use for new research programs, child research handoffs, candidate qualification, exact-SHA independent audit, repair, migration, global knowledge integration, and production release. Preserve role independence and never replace the canonical engines with a summarized prompt."
---

# Universal Research OS

Use this skill as a thin routing and activation layer over the complete canonical engines bundled under `engines/`. The skill does **not** replace, summarize away, merge, or weaken either OS.

## Canonical engines

- Orchestration: `engines/UNIVERSAL_RESEARCH_ORCHESTRATION_OS_v10_PROOF_CARRYING_RESEARCH_CONSTRUCTION/`
- Standalone Audit: `engines/UNIVERSAL_RESEARCH_AUDIT_OS_v6_PROOF_CARRYING_RESEARCH_CONSTRUCTION/`
- Immutable original ZIPs: `canonical_sources/`

The Orchestration OS v10 package is the primary engine. The standalone Audit OS v6 package is the independent read-only audit engine. Orchestration v10 also contains its canonical embedded copy of Audit OS v6. Keep all three surfaces intact.

## Start here

1. Read `router/ROUTING.md` and classify the requested situation.
2. Read only the minimum canonical engine entry files needed for that situation, then follow their references progressively.
3. Once a canonical engine or module is selected, its contracts, stage order, validators, schemas, receipts, manifests, and stop conditions are authoritative over this wrapper.
4. Never invent a replacement workflow when the canonical engine already defines one.
5. Never weaken an exact-SHA, external-review, admission, seal, validator, or production-release gate for convenience.

## Role independence is mandatory

Read `router/INDEPENDENCE_BOUNDARY.md` before any audit or semantic review.

The following roles must not be casually collapsed into one identity: Research Builder, Stage Pre-review Auditor, Candidate Auditor, Repair Builder, Global Builder, Global Auditor, Release Promoter.

A self-filled PASS is not independent proof. Candidate self-checks are not independent audit evidence.

For a formal candidate audit, prefer a fresh independent session/worker using only the standalone Audit OS v6 package plus the exact candidate and required external evidence. If the same runtime must orchestrate multiple roles, preserve explicit identity/session separation and every canonical external-review requirement; never describe same-context self-review as independent.

## Situation routing

Use the canonical Orchestration v10 Situation Router for definitive routing. The short map is:

- New multi-topic research: `modules/dispatcher/` + `modules/handoff_compiler/`
- Child-session research construction: `modules/proof_carrying_construction/`
- Returned candidate: `modules/control_plane/` admission first
- Candidate audit: standalone Audit OS v6 for strongest separation, or embedded v6 when shared orchestration context is legitimately required
- Bounded repair: `modules/repair/` + `modules/handoff_compiler/`
- Legacy migration: `modules/legacy_migration/`
- Global integration/reconciliation: `modules/global_builder/` plus the canonical reconciliation/global-seal modules as directed by the OS
- Production promotion/release: `modules/production_release/` + `modules/release/`

## Progressive disclosure

Do not load all 500+ engine files into context at once. Start from canonical entrypoints and expand only along referenced paths.

For Orchestration work, begin with:

- `01_AGENT_START_HERE.md`
- `03_SITUATION_ROUTER.md`
- then the selected module's own entry documentation and scripts

For standalone Audit work, begin with:

- `01_START_HERE.md`
- `02_AUDIT_DECISION_MODEL.md`
- `03_MANUAL_SEMANTIC_AUDIT_PROTOCOL.md`
- `04_VALIDATOR_REGISTRY_CONTRACT.md`
- `06_WHEN_TO_USE_STANDALONE_VS_EMBEDDED.md`
- `07_AUDIT_OUTPUT_CONTRACT.md`

For exact executable commands, follow the canonical engine's command cookbook or module instructions rather than improvising commands from this wrapper.

## Proof-carrying construction invariant

Direct-support research is constructed in proof order, not by writing claims first and backfilling citations. Preserve the canonical stage ordering and external proof requirements, including source snapshots, typed locators/passages, material clauses, external stage review, claim compilation, candidate sealing, admission, independent audit, and exact-SHA binding where required.

## Preservation invariant

The contents under both `engines/` canonical roots are byte-for-byte copies extracted from the original ZIPs included in `canonical_sources/`. Do not edit them in place when maintaining this wrapper. Add wrapper guidance outside the engine roots or rebuild from a newer canonical upstream release.

Run `python scripts/verify_skill_package.py` from the skill root to verify:

- both canonical ZIP SHA-256 values,
- byte-for-byte extracted-tree fidelity,
- embedded-vs-standalone Audit v6 parity,
- required wrapper files and version identities.

## Upgrade rule

When a newer canonical Orchestration or Audit OS is supplied, do not silently overwrite this version. Build a new skill release, preserve the new upstream ZIPs, regenerate extracted trees, update routing only as needed, and rerun full package verification.

## Boundaries

This skill helps execute the supplied research operating system. It does not make unsupported claims true, replace expert semantic judgment, or turn candidate-produced evidence into independent review. Follow tool, security, privacy, and external-source restrictions of the runtime in addition to the canonical OS.
