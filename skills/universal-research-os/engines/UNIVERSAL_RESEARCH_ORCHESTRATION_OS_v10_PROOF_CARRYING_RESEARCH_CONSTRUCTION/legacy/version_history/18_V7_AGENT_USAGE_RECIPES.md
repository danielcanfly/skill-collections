> **HISTORICAL MIGRATION REFERENCE ONLY. Do not execute these commands under v9. Use `21_V8_TO_V9_PRODUCTION_TRUST_CHAIN_HARDENING.md` and `22_V9_AGENT_USAGE_RECIPES.md`.**

# V7 Agent Usage Recipes

## Research child

Use `modules/child_runtime/`. Preserve original-source snapshots, typed locators, material claim clauses, and source-to-claim compatibility. Complete `qa/candidate_self_check_receipt.json`. Never create independent-review artifacts and never claim `MERGE_READY`.

## Return intake

Run `modules/control_plane/scripts/intake_admission_gate.py`. The Audit OS refuses to start without a PASS v7 admission receipt bound to the exact candidate SHA-256.

## Independent auditor

The auditor must be a different agent/session. Initialize the external workspace:

```bash
python modules/audit_os_v3_independent_semantic/scripts/initialize_independent_review.py CANDIDATE.zip \
  --output INDEPENDENT_REVIEW \
  --auditor-id AUDITOR_ID \
  --auditor-session-id AUDITOR_SESSION_ID
```

Review the original sources and every pre-populated retained direct-support material clause. Complete all source and locator rows. Hash the three CSV artifacts into the external receipt. Keep this directory outside the candidate tree.

Finalize the completed external review consistently:

```bash
python modules/audit_os_v3_independent_semantic/scripts/finalize_independent_review.py INDEPENDENT_REVIEW \
  --candidate CANDIDATE.zip \
  --attest-independent
```

## Audit

```bash
python modules/audit_os_v3_independent_semantic/scripts/audit_candidate.py CANDIDATE.zip \
  --admission-receipt ADMISSION_RECEIPT.json \
  --independent-review-dir INDEPENDENT_REVIEW \
  --output AUDIT_OUTPUT
```

Reject reports that omit admission, external review, Audit OS version 3.0.0, orchestration contract v7, or any of the five score dimensions.

## Repair

Every finding must define a class-wide population selector and executable closure command. Review all matching rows after repair, including retained direct-support rows not named in the original examples. Evidence-affecting repairs require a fresh admission receipt and a new external independent review bound to the repaired ZIP SHA.
