# Roles and State Machine

角色不可混用：Research Builder、Stage Pre-review Auditor、Candidate Auditor、Repair Builder、Global Builder、Global Auditor、Release Promoter。

`HANDOFF_ACTIVE → SOURCE_REGISTERED → PASSAGES_VERIFIED → CLAUSES_PRE_REVIEWED → CLAIMS_COMPILED → NODES_COMPILED → CANDIDATE_SEALED → ADMISSION_PASS → INDEPENDENT_AUDIT_PASS → PRODUCTION_RELEASE → GLOBAL_G0_G7_READY → GLOBAL_G8_PASS → RELEASED`

任何狀態缺少receipt或exact SHA binding，下一狀態不可建立。

## v10 External Stage Proof
Direct-support construction requires an external `external_stage_review/STAGE_REVIEW_IDENTITY.json` plus full-population passage and clause review tables. The reviewer ID and Session ID must differ from the Research Builder. A self-filled PASS field is not proof.
