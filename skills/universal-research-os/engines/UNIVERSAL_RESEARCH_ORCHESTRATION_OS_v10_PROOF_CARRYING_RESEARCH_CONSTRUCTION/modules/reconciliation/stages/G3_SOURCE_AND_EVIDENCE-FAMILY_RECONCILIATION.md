# G3 — Source and Evidence-Family Reconciliation


## Mission
建立 canonical meaningful source versions，修復 metadata，治理 evidence-family independence。

## Source matching evidence
- normalized DOI/ISBN/report ID
- canonical URL and mirrors
- title/authors/publisher/year
- edition/version
- content hash（若合法取得）
- source note statements

## Source decisions
KEEP / MERGE / PRESERVE_VERSION / REPAIR_METADATA / DEPRECATE。

## Evidence-family decisions
KEEP / MERGE / SPLIT。每個 canonical source 恰好一個 family。

## Access boundary
保留 best verified 與 floor；不得因查到 metadata 就宣稱已讀全文。

## Hard gate
所有 active sources/families resolved；版本邊界正確；source-family membership 1:1；mirrors 不虛增 independence；concept mappings 使用 G2 IDs。

## Forbidden
- 同 URL 一律合併
- 同 publisher 一律同 family
- 外部查證擴張 claim support
