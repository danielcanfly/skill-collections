# v5 → v6 Migration

1. 將所有未完成 v5及更早 handoff在 registry標為 `SUPERSEDED_DO_NOT_EXECUTE`。
2. 不允許子 Session繼續舊包；使用 v6重新生成或 compile repair handoff。
3. 舊 candidate只有在 admission gate被分類為 `LEGACY_MIGRATABLE_ACCEPTED`且主 Orchestrator明確批准時才能進 migration audit。
4. 為既有 active candidates補 `handoff/contract_lineage.json`，但不得偽造 originating ZIP SHA。
5. 使用四維 scorecard，不得再以單一30/100混合 compatibility與semantic品質。
