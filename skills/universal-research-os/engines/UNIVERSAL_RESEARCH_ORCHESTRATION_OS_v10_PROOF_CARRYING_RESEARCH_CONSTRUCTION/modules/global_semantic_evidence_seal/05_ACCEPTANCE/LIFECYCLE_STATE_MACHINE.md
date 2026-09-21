# Lifecycle State Machine

合法狀態：

1. `BASELINE_FROZEN`
2. `DIAGNOSIS_COMPLETE`
3. `REPAIR_IN_PROGRESS`
4. `REPAIR_VALIDATED`
5. `MERGE_READY`
6. `GLOBAL_MERGE_READY`
7. `PROMOTION_REVIEW_REQUIRED`
8. `PROMOTION_READY`
9. `PROMOTED`
10. `BLOCKED`

Repair handoff 的最高狀態通常是 `GLOBAL_MERGE_READY`。沒有 operator approval、live environment validation 與 rollback review，不得直接宣稱 `PROMOTED`。
