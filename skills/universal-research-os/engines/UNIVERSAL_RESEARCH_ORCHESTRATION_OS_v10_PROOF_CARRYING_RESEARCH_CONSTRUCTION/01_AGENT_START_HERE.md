# Universal Research Orchestration OS v10

本包將研究施工改為 proof-carrying compilation。

## 開始前
1. 依 `03_SITUATION_ROUTER.md` 選模組。
2. 新研究先用 `modules/dispatcher/` 與 `modules/handoff_compiler/`。
3. 子研究必須依 `modules/proof_carrying_construction/` 的 stage order施工。
4. 回件先經 `modules/control_plane/` admission。
5. 正式 Audit 使用 `modules/audit_os_v6_proof_carrying_construction/`。
6. Repair 使用 `modules/repair/` 並要求 class-wide external pre-audit。
7. Global整合只能使用 `modules/global_builder/`。

任何舊 v9 或更早 handoff 若未完成，先 supersede 或進 approved legacy migration。

## v10 External Stage Proof
Direct-support construction requires an external `external_stage_review/STAGE_REVIEW_IDENTITY.json` plus full-population passage and clause review tables. The reviewer ID and Session ID must differ from the Research Builder. A self-filled PASS field is not proof.
