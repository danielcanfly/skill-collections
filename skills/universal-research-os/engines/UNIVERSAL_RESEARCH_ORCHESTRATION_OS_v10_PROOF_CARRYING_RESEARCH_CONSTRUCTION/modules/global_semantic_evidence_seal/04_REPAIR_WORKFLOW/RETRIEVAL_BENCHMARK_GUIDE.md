# Retrieval Benchmark Guide

## 四個不可混合的角色

1. **Corpus builder**：產生索引文件。
2. **Benchmark author**：建立 query、expected IDs、hard negatives。
3. **Runner**：根據 query 排名，不知道 expected/negative IDs。
4. **Evaluator**：比較排名與答案。

實作上 evaluator 可以讀 expected IDs，但 scoring function 不可接收它們。

## Leakage scan

對每個 query 檢查：

- canonical title exact match
- alias exact match
- ID pattern
- source title
- 唯一 slug
- 題目中直接寫「retrieve X」

對 runner source code 檢查：

- `expected_ids` 是否進入 score function
- `negative_ids` 是否進入 score function
- title/alias bonus
- expected graph expansion
- query-specific hard-coded routing

## Hard negatives

Hard negative 應是：

- 同 phase 的最近鄰概念
- title相似但 decision role 不同的 node
- 同 source family 但支持不同 claim 的 reference
- parent/child 或 input/output 容易混淆的 node

## Multi-hop

測試應要求同時找回兩個或更多不同 node，且 query 不含其 title/alias。評估 expected set recall 與 negative ordering。
