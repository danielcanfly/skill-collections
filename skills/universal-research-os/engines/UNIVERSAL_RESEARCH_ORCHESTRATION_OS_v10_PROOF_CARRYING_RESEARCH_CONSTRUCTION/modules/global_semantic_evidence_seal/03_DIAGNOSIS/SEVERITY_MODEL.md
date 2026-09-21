# Severity Model

## P0 Critical

- 核心 ontology identity 破壞且無 migration path
- 發行包包含 fabricated evidence
- live pointer 被未授權修改
- production corpus 大量 unsupported 核心 claims
- benchmark 明確使用 expected/negative IDs 操控排名，且是唯一 acceptance evidence

## P1 High

- 高比例模板頁讓核心概念無法區分
- claim/source orphan 或 direct support inflation 影響核心域
- 多 bundle release identity 不一致
- holdout 已被調參污染但仍標為 independent
- manifest 或 ZIP integrity 失敗

## P2 Medium

- source passage locator 缺失，但 package lineage 透明且 claim 已降級
- 非核心頁模板化
- bounded synthesis 比例偏高但有治理
- source note limitations 不完整
- lifecycle 文案漂移但機器狀態一致

## P3 Low

- 命名、排序、格式或非阻斷 metadata 小問題

## Lifecycle disposition

- 任一 P0 open：`BLOCKED`
- 任一核心 P1 open：不得 `MERGE_READY`
- 僅有 bounded P2/P3：可 `MERGE_READY`
- `PROMOTION_READY` 另外要求 pointer plan、rollback、independent holdout 與 operator approval
