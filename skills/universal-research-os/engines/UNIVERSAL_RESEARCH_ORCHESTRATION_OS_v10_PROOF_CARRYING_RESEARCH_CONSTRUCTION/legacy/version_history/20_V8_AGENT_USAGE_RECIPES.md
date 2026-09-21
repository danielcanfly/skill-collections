> **HISTORICAL MIGRATION REFERENCE ONLY. Do not execute these commands under v9. Use `21_V8_TO_V9_PRODUCTION_TRUST_CHAIN_HARDENING.md` and `22_V9_AGENT_USAGE_RECIPES.md`.**

# V8 Agent Usage Recipes

## Build a child candidate

```bash
python qa/finalize_candidate.py . --case-min <N> --output-zip ../<DOMAIN>_PRODUCTION_CANDIDATE_vN.zip
```

## Admit and independently audit

```bash
python modules/control_plane/scripts/intake_admission_gate.py <candidate.zip> --registry <handoff_registry.json> --expected-name <candidate.zip> --output admission.json
python modules/audit_os_v4_production_release_assurance/scripts/audit_candidate.py <candidate.zip> --admission-receipt admission.json --independent-review-dir <external_review_dir> --output <audit_output_dir>
```

## Promote exact audited candidate

```bash
python modules/production_release/scripts/promote_audited_candidate.py <candidate.zip> <audit_output_dir> --admission-receipt admission.json --output <DOMAIN>_PRODUCTION_RELEASE_vN.zip
python modules/production_release/scripts/validate_child_production_release.py <DOMAIN>_PRODUCTION_RELEASE_vN.zip
```

## Final global G8 gate

```bash
python modules/reconciliation/scripts/run_g8_production_release_gate.py \
  --combined <combined.zip> --kos <kos.zip> --okf <okf.zip> \
  --r2 <r2.zip> --audit <audit.zip> --output GLOBAL_G8_ACCEPTANCE.json
```

## One-command governed child production pipeline

After the independent reviewer has completed and sealed the review directory:

```bash
python scripts/run_child_production_pipeline.py <candidate.zip> \
  --registry <handoff_registry.json> \
  --independent-review-dir <external_review_dir> \
  --output-dir <production_output_dir>
```

The command stops on the first failed gate. It never converts a failed candidate into a production release and never updates a live pointer.
