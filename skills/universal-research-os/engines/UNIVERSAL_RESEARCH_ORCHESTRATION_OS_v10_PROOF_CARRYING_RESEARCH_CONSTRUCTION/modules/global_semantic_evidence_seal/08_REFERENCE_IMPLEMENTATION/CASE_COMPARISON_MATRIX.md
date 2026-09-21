# Case Comparison Matrix

| Problem | Weak implementation | anonymized repaired implementation | Universal rule |
|---|---|---|---|
| Semantic duplication | 只換標題或同義詞 | 112 頁重構概念角色、邊界與操作化 | 目標 active pages duplicate ratio <0.30，mean <0.15 |
| Evidence precision | source ID 即視為 direct evidence | 994 atomic bindings，缺 span 時保留 package-lineage boundary | 不得捏造 span；relation、boundary、locator、verification 分欄 |
| Unsupported synthesis | 靜默標 support | 226 claims 保留 bounded synthesis/contextual | 沒有 direct evidence 不得升級 |
| Source note | bibliography stub | 337 source notes 加 contribution、limitations、locator | 每個 source note 必須說能證明與不能證明什麼 |
| Retrieval leakage | expected title bonus、negative exclusion | generator/runner 分離，無 title/alias bonus | expected/negative IDs 只可由 evaluator 使用 |
| Holdout | 反覆調參仍稱 holdout | frozen split與hash | 一旦看過結果並調參，holdout 作廢 |
| Release drift | 每包自行寫 status | 五包同 canonical lineage 重編 | 所有衍生面由 repaired KOS 單一來源生成 |
| Promotion | repair 完就改 live pointer | 只出 pointer proposal | repair 不等於 promotion |
