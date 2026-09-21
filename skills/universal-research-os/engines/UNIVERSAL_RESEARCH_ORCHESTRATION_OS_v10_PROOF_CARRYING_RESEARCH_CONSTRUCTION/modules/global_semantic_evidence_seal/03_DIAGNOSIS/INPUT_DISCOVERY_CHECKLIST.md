# Input Discovery Checklist

在 repair 前建立以下 inventory：

- 所有 ZIP 與 SHA256
- 每包 member count、compressed/uncompressed size
- 可能的 canonical KOS root
- knowledge node 目錄與 front matter schema
- concept/source/claim/case/evidence-family registries
- graph nodes/edges
- retrieval benchmark、runner、results、metrics
- OKF validator與export map
- R2 object plan與pointer plan
- release plan與lifecycle status
- audit findings、scorecard、validator receipts

若同一檔案在多包出現，計算 content hash 判斷是同 lineage、copy drift 或不同版本。不可只看 filename。
