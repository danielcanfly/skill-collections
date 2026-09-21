# Run State & Checkpoints

## Purpose

Long textbook jobs must not depend on conversational memory. `RUN_STATE` is the durable control plane for the run.

## Required lifecycle

Create after G0. Update after every gate transition, bounded repair, source freeze, lesson completion, revision, and final release decision.

## Minimum fields

- run_id
- skill_version
- mode
- topic
- audience
- language
- temporal_cutoff
- primary_domain_adapter
- secondary_domain_adapters
- current_gate
- gate_status
- completed_artifacts
- active_research_freeze_id
- completed_lessons
- open_defects
- blockers
- pending_validations
- revision_impact_set
- final_artifact_status
- learner_mastery_status

## Stable IDs

Use stable IDs across artifacts:

- `SRC-###` source
- `CLM-###` factual / evaluative claim
- `CON-###` concept
- `OBJ-###` learning objective
- `LES-##` lesson
- `ASM-###` assessment
- `EXE-###` executable validation
- `DEF-###` defect

Do not renumber IDs merely because chapters move.

## Gate transition rules

A gate transition record should contain:

- from_gate
- to_gate
- result: PASS / PARTIAL / BLOCKED
- evidence_artifacts
- unresolved_defects
- timestamp or execution date when available

`PARTIAL` cannot silently become PASS. Repair and recheck.

## Resume rules

When resuming a run:

1. Read `RUN_STATE` first.
2. Confirm the active research freeze is still valid for volatile content.
3. Reuse completed artifacts if their upstream dependencies have not changed.
4. Re-run only impacted gates.
5. If a source, scope, domain adapter, or temporal cutoff changes, create a revision impact set before editing downstream artifacts.

## State consistency

Before final release, verify:

- every artifact marked complete actually exists
- every PASS gate has evidence
- no CRITICAL defect remains open
- completed lesson list matches curriculum map
- final artifact status matches publication QA
- `TEXTBOOK_COMPLETE` is not used for learner mastery

## Failure recovery

If context is lost, reconstruct from artifacts in this order:

1. Scope Contract
2. RUN_STATE
3. Research Freeze + Evidence Ledger
4. Curriculum Map
5. completed Lesson Manuscripts
6. open defects / validation logs
7. final artifact state

Do not restart expensive research by default.
