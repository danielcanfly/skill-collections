# Problem Taxonomy and Detection

## SES-01 Semantic template saturation

### 症狀

- 同一 phase 的多個頁面共用完整段落。
- 不同 concept 的 failure modes、implementation checklist 或 boundaries 幾乎一樣。
- 節點標題不同，但拿掉標題後內容難以辨識。
- graph node count 很高，unique semantic propositions 卻很低。

### 偵測

以 active Concept、Pattern、Checklist 頁為母體：

1. 移除 front matter、導航、citation list、related list、registry dump。
2. 將 prose 切為句或長行。
3. 正規化大小寫、標點、ID、Markdown link。
4. 計算每句出現在多少頁。
5. 若句子出現在至少 4 頁，視為 repeated semantic prose。
6. 每頁 duplicate ratio = repeated semantic prose lines / semantic prose lines。

### 建議門檻

| 指標 | PASS | P2 | P1 | P0 |
|---|---:|---:|---:|---:|
| 單頁 duplicate ratio | <0.30 | 0.30–0.39 | 0.40–0.59 | ≥0.60 且核心頁 |
| corpus mean | <0.15 | 0.15–0.22 | >0.22 | >0.35 |
| pages ≥0.50 | 0 | 1–3 非核心 | >3 | 核心域廣泛存在 |

不要用簡單 cosine similarity 取代段落重複分析。兩個相關概念合理相似，但不應共享整段判斷語言。

## SES-02 Evidence relation inflation

### 症狀

- Claim registry 有 source ID，但沒有 locator、scope 或 relation type。
- 所有 edge 都叫 `support`。
- Source note 只複製 bibliographic metadata，沒有說明實際支持了什麼。
- Claims 100% direct support，但輸入並沒有 exact passages。

### 偵測

對每個 claim 檢查：

- 是否有唯一 claim ID
- 是否有 canonical proposition
- 是否有 concept binding
- 是否有 source binding
- support relation 是否在受控 taxonomy
- evidence boundary 是否存在
- locator type 與 locator 是否一致
- direct support 是否有 verification status
- source 與 concept 是否存在
- 是否存在完全重複 edge
- bounded synthesis 是否列出 contributing sources

核心 coverage 指標：

- claims total
- claims with any binding
- claims with direct support
- claims with only contextual/partial support
- bounded synthesis claims
- unsupported claims
- bindings with exact span
- bindings with package lineage only

## SES-03 Source-note shallowness

每個 canonical source note 至少應呈現：

- source identity
- source type與access status
- evidence/method profile
- direct contribution
- partial/contextual/challenge contribution
- limitations與不能證明的事項
- linked claims與concepts
- package locator或source locator

只有 title、publisher、URL 的 reference stub 不算 evidence note。

## SES-04 Retrieval acceptance leakage

### 高風險模式

- Query 中含 expected title 或 alias。
- Runner 對 exact title 或 alias 加分。
- Runner 讀 `negative_ids` 並將其設為負分或排除。
- Runner 使用 expected IDs 做 graph expansion。
- Generator 與 runner 在同一執行流程中。
- Benchmark hash 在 runner 執行前未凍結。
- Holdout 是固定抽每三題一題，但內容仍由同一 corpus template 生成，且被反覆用於調參。
- 測試全部是 title lookup，沒有 hard neighbour、boundary、multi-hop 或 provenance。

### 必測類別

- definition
- boundary
- comparison
- decision application
- how-to
- operational
- audit
- adversarial
- hard-negative neighbour
- multi-hop
- source-provenance

## SES-05 Release identity and lifecycle drift

跨 bundle 比對：

- release_id
- content_version
- schema_version
- lifecycle
- canonical root identity
- source lineage hash
- manifest hash
- pointer target
- generated_at
- bundle role

README、JSON、CSV、pointer plan、audit report 中若出現互相矛盾的狀態，視為 metadata drift。

## SES-06 Mechanical integrity

必檢查：

- ZIP CRC
- unsafe archive paths
- duplicate archive members
- SHA256 manifest correctness
- missing required files
- broken internal links
- duplicate canonical IDs
- orphan claim/source/concept/case IDs
- malformed CSV/JSON/YAML
