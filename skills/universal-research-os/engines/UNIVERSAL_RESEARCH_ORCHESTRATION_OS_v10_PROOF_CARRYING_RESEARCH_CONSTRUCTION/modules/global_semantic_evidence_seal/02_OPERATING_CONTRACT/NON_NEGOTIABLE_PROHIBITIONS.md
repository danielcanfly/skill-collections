# Non-negotiable Prohibitions

以下任一項發生，repair 不得標為 MERGE_READY：

1. 為了讓 coverage 變成 100%，捏造來源、quote、頁碼、段落或 evidence span。
2. 把 `contextual`、`partial`、`method-only`、`challenge` 或 `bounded synthesis` 靜默改成 `direct support`。
3. 只改標題或少量同義詞，卻宣稱完成 semantic de-templating。
4. Runner 讀取 expected IDs 後對其加分、擴展 graph、加入 title bonus 或 alias bonus。
5. Runner 使用 negative IDs 降分、排除候選或縮小 search space。
6. 在同一支程式執行時生成測試又跑分，卻稱為 frozen holdout。
7. 使用已看過失敗結果的 holdout 繼續調參，仍稱該集合為 holdout。
8. 重新編號 canonical IDs，但沒有 migration log 與 downstream map。
9. 只重建其中一個 bundle，讓其他 bundle 保留舊 lifecycle 或舊 release ID。
10. Repair 階段直接更新 live pointer。
11. 用 ZIP 可解壓、檔案數或 README 自評 PASS 取代內容與證據 audit。
12. 將來源缺失問題包裝成「格式限制」後消失於最終 findings。
