# Repair Decision Tree

## A. 是否需要重做研究

只有以下情況才進 research restart：

- 核心 ontology 無法表示主題中的主要決策、機制或工作流程。
- 大量 canonical claims 經查證為錯誤、過時或互相衝突，且既有 sources 無法修復。
- source coverage 缺失到無法形成 bounded synthesis。
- canonical identity collision 廣泛到無法以 migration repair 解決。

以下情況不構成 research restart：

- 頁面模板化
- claim locator 不精確
- source note 太薄
- retrieval benchmark 洩漏
- release metadata 不一致
- OKF/KOS/R2 編譯面不同步

## B. Evidence repair 類型

1. 有 exact quote/span：建立 `VERIFIED_EXACT_SPAN`。
2. 有可信 section locator：建立 `VERIFIED_SECTION_LOCATOR`。
3. 有完整 source text，但無段落位置：最多 `VERIFIED_DOCUMENT_LEVEL`。
4. 只有既有 package lineage：標記 `PACKAGE_LINEAGE_ONLY`，不得新增虛構 span。
5. Claim 為多來源推導：標記 `BOUNDED_SYNTHESIS`，列出 contributing sources。
6. 找不到支持：標記 `UNSUPPORTED`，若為核心 claim 則 P1 或 P0。

## C. Retrieval acceptance 強度

- Tier 0: corpus-derived regression，僅供 CI，不可單獨作為 production acceptance。
- Tier 1: auditor-authored frozen benchmark，generator/runner 分離，無答案洩漏。
- Tier 2: independent external holdout，題目作者不接觸 title/alias，最適合作為 production acceptance。

至少達 Tier 1 才能 MERGE_READY；PROMOTION_READY 建議 Tier 2。
