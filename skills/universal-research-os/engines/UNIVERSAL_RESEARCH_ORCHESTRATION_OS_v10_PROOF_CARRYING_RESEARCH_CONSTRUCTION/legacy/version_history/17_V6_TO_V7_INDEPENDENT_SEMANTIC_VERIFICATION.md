> **HISTORICAL MIGRATION REFERENCE ONLY. Do not execute these commands under v9. Use `21_V8_TO_V9_PRODUCTION_TRUST_CHAIN_HARDENING.md` and `22_V9_AGENT_USAGE_RECIPES.md`.**

# V6 → V7 Independent Semantic Verification

V7 changes the trust model. Candidate-authored receipts are self-checks only. They cannot satisfy independent semantic acceptance.

## Mandatory gates

1. V7 return admission receipt.
2. Candidate self-check with no self-awarded `MERGE_READY`.
3. Material claim-clause matrix.
4. Source passage registry with typed locator, immutable snapshot and hashes.
5. Source-to-claim domain compatibility matrix.
6. External independent semantic review bound to candidate SHA-256.
7. Review of every retained direct-support material clause.
8. Artifact chronology validation.
9. Five-dimensional scorecard: compatibility, semantic evidence, retrieval, seal/reproducibility, independent semantic verification.
10. Class-wide repair closure for every failure family.

`MERGE_READY` is impossible when admission or independent review is absent.
