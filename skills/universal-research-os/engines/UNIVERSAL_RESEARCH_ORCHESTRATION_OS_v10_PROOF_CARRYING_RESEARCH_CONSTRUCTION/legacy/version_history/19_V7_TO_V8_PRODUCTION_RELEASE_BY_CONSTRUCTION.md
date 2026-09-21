> **HISTORICAL MIGRATION REFERENCE ONLY. Do not execute these commands under v9. Use `21_V8_TO_V9_PRODUCTION_TRUST_CHAIN_HARDENING.md` and `22_V9_AGENT_USAGE_RECIPES.md`.**

# V7 → V8 Production Release by Construction

V8 closes the gap between a strong research candidate and an actual production release.

## Six new blocking controls

1. **Atomic evidence coverage:** every active claim-source pair is unique and bound to an immutable source passage, resolvable locator and snapshot.
2. **Source metadata completeness:** author or responsible organisation, identifier, temporal fields, exact metadata locator and access level must be production-eligible.
3. **Portable deterministic reproduction:** executable runners may not contain machine-specific paths; declared reproduction commands run in an isolated copy and must regenerate byte-identical outputs.
4. **Production-surface hygiene:** R2 and production objects reject tests, fixtures, synthetic candidates, cache files, provisional output and unsafe keys.
5. **Operational node depth:** minimum body depth, required decision/evidence/limitation sections, anti-boilerplate and stricter semantic similarity controls.
6. **Zero-open-finding production seal:** production profiles allow no open P0, P1 or P2.

## Lifecycle correction

A child builder emits `SEALED_CANDIDATE`, never production. Orchestration performs admission and an external Audit OS v4 review bound to the exact candidate SHA. Only then may `promote_audited_candidate.py` create an `AUDITED_PRODUCTION_RELEASE` wrapper. Global G0 admits only those wrappers.

## Exact-final global release

G8 compiles all five global release surfaces from one lineage and runs the production release assurance gate. Live R2 pointer promotion remains a separate authorised action.
