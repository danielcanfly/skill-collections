> **HISTORICAL MIGRATION REFERENCE ONLY. Do not execute these commands under v9. Use `21_V8_TO_V9_PRODUCTION_TRUST_CHAIN_HARDENING.md` and `22_V9_AGENT_USAGE_RECIPES.md`.**

> **Historical migration reference only. Do not execute this workflow in v7.**

> Historical migration reference. Do not use as the active v7 operating recipe.

# v5 → v6 Control-Plane Hardening

## 為什麼需要 v6

v5 的 Audit OS v2.1 能正確抓出來源身份、edge entailment、lineage、retrieval和seal問題，但其 orchestration control plane仍允許：

- 已被新 contract取代的舊 handoff繼續施工；
- 不明 contract lineage的 candidate進入完整 audit；
- 舊 artifact重傳後才在深度 audit中被發現；
- compatibility問題與semantic問題混成單一分數；
- repair handoff只靠 prose與大範圍 allowed paths；
- repair generator未提供可執行 finding closure、delta、cascade和exact-final驗收；
- 通用 child runtime被單一主題 hard-code污染。

## v6 新增

1. Handoff supersession registry與kill switch。
2. Candidate contract lineage manifest。
3. Mandatory return admission gate與五類分類。
4. Stale/rejected artifact registry。
5. 四維 audit scorecard。
6. Repair Contract v3，支援 path glob、row/field級規則、closure commands與cascade checks。
7. Repair compiler生成專用 validators與exact-final acceptance runner。
8. Universal runtime topic-contamination scan。
9. Generic finalizer，由 `audit_config.json` 驅動，零主題硬編碼。
10. v5→v6 migration與所有真實 regression fixtures。
