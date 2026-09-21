# G1 — Global Inventory and Identity Registry


## Mission
為所有 active local objects 建立 phase-qualified、deterministic provisional global identities；只解撞號，不做語義合併。

## Allocation rules
- Concept：現有 canonical path，另記 phase/local identity。
- Source：`SRC-G-xxxxx`
- Claim：`CLM-G-xxxxx`
- Case：`CASE-G-xxxxx`
- Evidence family：`EF-G-xxxxx`

排序鍵必須凍結，例如 `(phase_order, local_id, normalized_title, local_path)`。

## Inventories
- node/source/claim/evidence-family/case identities
- atomic claim-edge inventory
- case-source edge inventory
- relationship inventory
- namespace registry
- local-ID collisions
- duplicate titles/locators
- semantic review queue

## Hard gate
每個 active local object 恰好一個 provisional identity；deprecated/alias lineage 明示；ID 唯一、連續或符合配置規則；allocation clean rebuild 一致。

## Forbidden
- 因相同 local ID 合併跨 phase objects
- 在 G1 決定 semantic merge
