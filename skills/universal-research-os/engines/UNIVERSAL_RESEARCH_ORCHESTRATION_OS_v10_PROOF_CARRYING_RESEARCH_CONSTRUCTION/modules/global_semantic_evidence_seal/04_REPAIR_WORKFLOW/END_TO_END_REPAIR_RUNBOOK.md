# End-to-end Repair Runbook

## R0 Intake and immutable baseline

### 目標

建立不可變原始輸入與可回溯 baseline。

### 動作

1. 將原始 ZIP 複製到 `inputs/immutable/`。
2. 產生 `input_sha256s.txt`。
3. ZIP CRC test。
4. 解壓到 `work/baseline/`，禁止原地修改。
5. 建立 inventory、canonical ID counts、bundle metadata matrix。
6. 宣告 authoritative input 與衍生 input。

### Gate

- 所有輸入 hash 已記錄
- 沒有 unsafe archive path
- baseline 可重新建立

## R1 Structural and identity diagnosis

### 動作

- 建立 concept/source/claim/case/edge inventory。
- 檢查 duplicate IDs、orphan IDs、namespace collision。
- 比對各 bundle release identity。
- 產生 `repair_scope_decision.json`。

### Gate

明確選擇：

- `BOUNDED_GLOBAL_REPAIR`
- `SOURCE_REFRESH_REPAIR`
- `RESEARCH_RESTART_REQUIRED`

不得在沒有 scope decision 的情況下改檔。

## R2 Semantic de-templating

### 選頁

只修 duplicate ratio 超過門檻或人工判定概念邊界不清的頁面。

### 保留

- ID
- title，除非錯誤
- aliases
- type
- namespace
- relationships
- status
- source/claim/case links

### 重寫內容骨架

每個頁面應有概念特定內容：

1. 定義與 decision role
2. 與最近鄰概念的邊界
3. 核心 mechanism 或 reasoning chain
4. 適用條件
5. 不適用條件
6. failure signals
7. operational procedure
8. evidence boundary

禁止只替換名詞。每一節都必須回答該 concept 特有的問題。

### 驗證

- 重跑 duplicate audit
- no active page ≥0.30 為推薦目標
- corpus mean <0.15
- 人工抽查最近鄰概念，確認可區分

## R3 Claim-evidence binding repair

### 建立 atomic binding registry

一列只表達一個 claim、source、concept 與 relation。

必要欄位見 `06_TEMPLATES/claim_evidence_binding_registry_template.csv`。

### Relation taxonomy

- `direct_support`
- `partial_support`
- `contextual_support`
- `method_support`
- `challenge`
- `contradiction`
- `bounded_synthesis`

### Evidence boundary rules

- Exact quote 必須保存 quote hash。
- Source locator 未驗證不得標 verified。
- 只有 package lineage 時，locator type 必須標 `PACKAGE_LINEAGE_ONLY`。
- 沒有 direct source 的 claim 必須保留 bounded synthesis 或 unsupported 狀態。
- 不得為達成 coverage 刪除 residual gap。

### 輸出

- binding registry
- residual claim gaps
- coverage metrics
- downgrade/upgrade log

## R4 Source-note depth repair

對每個 canonical source note 補齊：

- identity與access status
- method/evidence profile
- direct claim contributions
- non-direct contributions
- limitations
- linked concepts與claims
- package/source locators

若 source 無法讀取全文，明確標記，不可用摘要猜測 exact support。

## R5 Frozen retrieval acceptance rebuild

### 分離角色

- Auditor generator：建立測試與 hard negatives
- Freeze step：寫入 benchmark hash
- Runner：只讀 corpus 與 frozen benchmark
- Evaluator：讀 expected/negative IDs 計算結果

Runner 不得 import generator。

### Benchmark 最低要求

- 至少 30% holdout
- 每題至少一個 hard negative
- title/alias leakage = 0
- 至少 20 個 multi-hop，或為 corpus active concept 數的 5%，取較大者，上限可設 100
- 至少 20 個 source-provenance tests，若 source 數不足則覆蓋所有 direct sources
- development與holdout分開報告
- benchmark file與runner file各自 SHA256

### Holdout contamination rule

只要人或程式根據 holdout failure 改過 ranking、index、weights、query processing 或 corpus wording，該 holdout 立即標 `CONTAMINATED`。必須由獨立 generator 產生新 holdout，舊集合只能保留為 regression。

### Acceptance

- runner policy assertions全部 false/true符合規則
- title_alias_leak_count = 0
- negative ordering pass
- holdout達標
- 失敗案例保留，不得刪題直到 pass

注意：100% 不是必要條件。對真正 external holdout，可設定合理 threshold，例如 overall ≥0.90、核心類別 ≥0.85、P0 query 100%。門檻必須在跑分前凍結。

## R6 Multi-surface release reconstruction

以修復後 canonical KOS 為唯一 source of truth，重新編譯：

1. Extended KOS
2. Strict OKF
3. R2 ingestion pack
4. Combined production release
5. Independent audit surface

不得從舊衍生包反向拼接修復結果。

所有包統一：

- release ID
- content version
- lifecycle
- canonical lineage hash
- generated_at policy
- manifest schema

R2 pack 只能產生 immutable object plan與pointer proposal，不執行 live pointer update。

## R7 Independent audit

Audit 必須重新打開 ZIP，而不是直接看 build directory。

執行：

- ZIP CRC
- manifests
- identity consistency
- semantic metrics
- evidence coverage
- retrieval receipts
- OKF validation
- R2 dry-run
- prohibited-change checks

產出 findings register、severity counts、scorecard、final disposition。

## R8 Handoff packaging

Handoff ZIP 包含：

- 00 prompt
- start here
- 所有五個 release ZIP
- bundle index
- SHA256SUMS
- final audit summary
- remaining bounded gaps
- next allowed action

Next action 只可為：

- independent promotion readiness review
- source refresh with new verified passages
- bounded follow-up repair

不得暗示已自動 promotion。
