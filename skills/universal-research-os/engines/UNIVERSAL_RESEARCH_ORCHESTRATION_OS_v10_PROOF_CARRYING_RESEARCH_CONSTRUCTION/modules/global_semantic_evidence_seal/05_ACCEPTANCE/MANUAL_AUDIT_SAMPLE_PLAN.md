# Manual Audit Sample Plan

Mechanical tests之外，至少人工抽查：

- 每個 topic/phase 2 個 semantic repaired pages
- duplicate ratio最高的 10 頁
- 20 個 direct-support claims
- 20 個 bounded synthesis claims
- 10 個 source notes
- 10 個 multi-hop retrieval tests
- 10 個 source-provenance tests
- 所有 P0/P1 findings

抽樣時確認：

- 頁面不是只做同義改寫
- claim scope 沒有超過 source
- locator 真能指向 evidence
- negative node 確實是合理 hard negative
- README 狀態與機器 metadata 一致
