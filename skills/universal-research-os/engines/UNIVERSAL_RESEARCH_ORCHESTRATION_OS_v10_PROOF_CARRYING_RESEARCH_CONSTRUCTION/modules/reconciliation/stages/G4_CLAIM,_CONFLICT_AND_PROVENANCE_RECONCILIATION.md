# G4 — Claim, Conflict and Provenance Reconciliation


## Mission
將 phase-local claims 收斂為 bounded canonical propositions，完整保留 atomic lineage、challenge boundaries、confidence 與 gaps。

## Proposition fingerprint
比較 subject、predicate、object、scope、condition、modality、polarity、claim type、application domain。

## Decisions
- same proposition → MERGE + reversible alias
- broader/narrower/application/contextual → separate IDs + relation
- direct contradiction → conflict matrix
- source challenge → boundary，不虛構 opposite claim

## Atomic edge
每條 G1 lineage 映射至 G4 claim、G3 source/family、G2 concept。

## Confidence
需說明 component：directness、edge confidence、source access、family breadth、challenge penalty。不是 truth probability。

## Hard gate
所有 claims resolved；atomic lineage count 100% preserved；canonical tuple 唯一；conflicts/gaps 完整；cases untouched。

## Forbidden
- 以文字相似度直接 merge proposition
- mirror 增加 family breadth
- challenge 自動生成相反 claim
