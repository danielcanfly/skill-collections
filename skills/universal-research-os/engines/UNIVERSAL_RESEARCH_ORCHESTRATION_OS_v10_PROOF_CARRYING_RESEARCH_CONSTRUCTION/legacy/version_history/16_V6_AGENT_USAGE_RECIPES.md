> **HISTORICAL MIGRATION REFERENCE ONLY. Do not execute these commands under v9. Use `21_V8_TO_V9_PRODUCTION_TRUST_CHAIN_HARDENING.md` and `22_V9_AGENT_USAGE_RECIPES.md`.**

> **Historical migration reference only. Do not execute this workflow in v7.**

> Historical migration reference. Do not use as the active v7 operating recipe.

# v6 Agent Usage Recipes

## A. 主 Orchestrator生成並派發新研究包

```bash
python modules/dispatcher/scripts/validate_domain_config.py DOMAIN_CONFIG.json
python modules/dispatcher/scripts/generate_child_packages.py DOMAIN_CONFIG.json --output-dir GENERATED
python modules/dispatcher/scripts/validate_generated_collection.py GENERATED DOMAIN_CONFIG.json
python modules/control_plane/scripts/register_handoff.py GENERATED/<HANDOFF>.zip --registry control_plane/handoff_registry.json
```

## B. Contract升版後停止舊任務

```bash
python modules/control_plane/scripts/supersede_handoffs.py \
  --registry control_plane/handoff_registry.json \
  --older-than-os 7.0.0 \
  --reason "OS v6 contract migration"
```

舊包不得繼續施工。必須重發 v6-native handoff。

## C. 子 Session綁定 contract lineage

```bash
python scripts/initialize_contract_lineage.py \
  --candidate-root OUTPUT_SKELETON \
  --handoff-zip /absolute/path/to/HANDOFF.zip \
  --handoff-identity HANDOFF_IDENTITY.json
```

Finalizer會拒絕未綁定 candidate。

## D. 回件 admission

```bash
python modules/control_plane/scripts/intake_admission_gate.py RETURN.zip \
  --registry control_plane/handoff_registry.json \
  --rejected-registry control_plane/rejected_artifact_registry.json \
  --expected-name EXPECTED.zip \
  --output INTAKE_ADMISSION_RECEIPT.json
```

只有 `V7_NATIVE_ACCEPTED` 或被明確核准的 `LEGACY_MIGRATABLE_ACCEPTED` 可以進 Audit。

## E. 四維 Audit

```bash
python modules/audit_os_v3_independent_semantic/scripts/audit_candidate.py RETURN.zip \
  --output AUDIT_OUT \
  --admission-receipt INTAKE_ADMISSION_RECEIPT.json
```

## F. 生成 bounded repair handoff

```bash
python modules/repair/scripts/create_repair_handoff.py \
  --candidate RETURN.zip \
  --audit AUDIT_OUT \
  --contract repair_contract_v3.json \
  --closure-matrix finding_closure_matrix.json \
  --output REPAIR_HANDOFF.zip
```

## G. Repair回件 exact-final驗收

```bash
python scripts/run_exact_final_acceptance.py \
  --source SOURCE_CANDIDATE.zip \
  --returned REPAIRED.zip \
  --contract repair_contract.json \
  --closure-matrix finding_closure_matrix.json \
  --audit-os AUDIT_OS/UNIVERSAL_RESEARCH_AUDIT_OS_v3_INDEPENDENT_SEMANTIC_VERIFICATION
```
