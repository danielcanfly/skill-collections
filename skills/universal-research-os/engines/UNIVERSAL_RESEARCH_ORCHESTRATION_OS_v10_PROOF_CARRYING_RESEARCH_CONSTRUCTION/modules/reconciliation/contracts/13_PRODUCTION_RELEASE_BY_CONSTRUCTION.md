# Production Release by Construction Contract

The reconciliation pipeline must not relabel a candidate as production. It accepts only audited child production-release wrappers and emits five exact-final global surfaces from one canonical lineage:

1. Combined Knowledge OS production release.
2. Extended KOS bundle.
3. Strict OKF bundle.
4. Clean R2 ingestion pack.
5. Independent audit bundle.

Before `GLOBAL_MERGE_READY`, `run_g8_production_release_gate.py` must prove:

- one release identity across all five surfaces;
- deterministic ZIP, CRC, strict manifest and fresh extraction;
- R2 contains no audit, QA, tests, fixtures, synthetic candidates, caches or provisional outputs;
- production surface manifest exists;
- Audit OS v6 exact-final score is 100 in all six dimensions, including production assurance;
- open P0/P1/P2 are all zero;
- live pointer is unchanged.
