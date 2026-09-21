# Hard Gates and Scorecard

## Hard gates

以下全部通過才可 `MERGE_READY`：

### Identity

- duplicate canonical IDs = 0
- unresolved namespace collisions = 0
- canonical ID renumbering without migration = 0
- orphan core edges = 0

### Semantic

- active pages duplicate ratio ≥0.50 = 0
- active pages duplicate ratio ≥0.30 = 0，或每一項有人工 justified exception
- corpus mean duplicate ratio <0.15
- repaired page ID與relationships保留

### Evidence

- every claim 有 status與evidence boundary
- fabricated locator count = 0
- unsupported core claims = 0
- direct-support bindings missing source identity = 0
- relation taxonomy violations = 0
- residual gaps register 存在

### Retrieval

- benchmark frozen before runner execution
- generator與runner分離
- title/alias leakage = 0
- expected ID scoring bonus = false
- alias bonus = false
- negative ID score exclusion = false
- expected graph expansion = false
- holdout contamination = false
- hard-negative coverage達標

### Release

- KOS/OKF/R2/production/audit release ID一致
- content version一致
- lifecycle一致
- ZIP CRC PASS
- SHA256 manifests PASS
- R2 dry run PASS
- live pointer unchanged

## 建議 100 分 scorecard

| Area | Weight |
|---|---:|
| Canonical identity and lineage | 15 |
| Semantic distinctiveness | 20 |
| Claim-evidence integrity | 25 |
| Source-note depth | 10 |
| Retrieval acceptance validity | 15 |
| Release consistency and packaging | 10 |
| Governance and bounded gaps | 5 |

### Disposition

- 95–100：MERGE_READY，僅 bounded P2/P3
- 90–94：MERGE_READY_WITH_CONDITIONS 或 repair required，依 findings
- 80–89：REPAIR_REQUIRED
- <80：BLOCKED

分數不能覆蓋 hard-gate failure。即使 99 分，只要有 open P0/P1 hard gate，也不能 MERGE_READY。


## v5 inherited gates
- All global active claim edges must satisfy Audit OS v6 Production Trust Chain Hardened entailment.
- Global evidence-family independence is recomputed after merge.
- All release surfaces must share one release identity and content lineage.
- Frozen retrieval runner must pass leakage audit.
- Independent final Audit OS v6 Production Trust Chain Hardened remains authoritative.
