# Global Semantic & Evidence Seal Module v1.1

## 目的

本交付包讓其他 session 能對不同研究主題或 Knowledge OS 發行包，識別並修復以下四類高風險問題：

1. **Semantic templating**：大量知識頁只是套用同一段模板，節點數增加但概念辨識度沒有增加。
2. **Evidence overclaiming**：claim 雖連到 source，卻沒有足夠 evidence boundary，或把 bounded synthesis 說成 direct support。
3. **Retrieval benchmark leakage**：測試題、runner 或 scoring logic 洩漏 expected ID、title、alias 或 negative ID，造成虛假的高通過率。
4. **Release metadata drift**：KOS、OKF、R2、production、audit 等包的 release ID、版本、lifecycle 與 pointer state 不一致。

本 OS 不綁定任何研究主題。歷史修復案例只保留匿名化的通用控制教訓，不包含可被誤複製的專題資料或 release artifacts。

## 使用方式

### 輸入

至少提供其中一項：

- combined production release ZIP
- extended KOS ZIP
- strict OKF ZIP
- R2 ingestion pack ZIP
- audit ZIP
- 各 phase 或 topic production candidate ZIP

若有多包，必須全部納入 identity 與 metadata consistency audit。

### 執行順序

1. 解壓至隔離工作目錄，保留原始 ZIP 不變。
2. 建立 baseline inventory 與 hash。
3. 執行四大診斷面與 mechanical validation。
4. 決定是 bounded repair、source refresh，還是 research restart。
5. 只對失敗面施工。
6. 重新編譯所有衍生發行面。
7. 以獨立 audit surface 驗證。
8. 打包新的 repair handoff，不修改 live pointer。

## 最小交付物

修復 session 最終至少要交付：

- `<DOMAIN>_GLOBAL_KOS_EXTENDED_BUNDLE_vN.zip`
- `<DOMAIN>_GLOBAL_OKF_BUNDLE_vN.zip`
- `<DOMAIN>_GLOBAL_R2_INGESTION_PACK_vN.zip`
- `<DOMAIN>_GLOBAL_KNOWLEDGE_OS_PRODUCTION_RELEASE_vN.zip`
- `<DOMAIN>_GLOBAL_RECONCILIATION_AUDIT_vN.zip`
- `<DOMAIN>_GLOBAL_SEMANTIC_EVIDENCE_SEAL_REPAIR_HANDOFF_vN.zip`

以及：

- baseline inventory
- semantic de-templating before/after report
- claim-evidence coverage report
- retrieval leakage report與 frozen benchmark receipts
- metadata consistency report
- manifest、SHA256SUMS、ZIP integrity receipt
- final findings register與 lifecycle status

## 成功定義

成功不是「腳本全部綠燈」，而是：

- canonical identity 沒有無理由漂移
- 高模板頁被實質改寫，而不是換同義詞
- evidence relation 與可驗證程度一致
- retrieval acceptance 不使用答案資訊幫助 ranking
- 每個 bundle 都從同一 canonical lineage 編譯
- remaining gaps 被列為 bounded findings，不被藏起來
