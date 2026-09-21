# Audit Scripts

## 快速執行

1. 複製 `10_SCHEMAS/repair_config.example.json`。
2. 填入 baseline、repaired root、registry、retrieval 與 bundle paths。
3. 安裝 requirements。
4. 執行：

```bash
./RUN_AUDIT.sh /absolute/path/to/repair_config.json
```

這些腳本是跨主題的 diagnostics，不會自動改寫知識內容，也不會碰 live pointer。內容修復仍需依 runbook 進行，完成後再重跑 scripts。

Static retrieval leakage audit 會保守地標示可疑程式碼。`RUNNER_REFERENCES_EVALUATION_FIELDS` 是需要人工確認的 P2，因 evaluator 在同一檔案時可能合理讀取答案，但 ranking function 不得使用答案。
