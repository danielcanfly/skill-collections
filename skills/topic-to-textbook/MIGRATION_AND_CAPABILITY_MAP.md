# Migration & Capability Map

## Public-release principle

The public package ships only the current executable specification and its supporting protocols. Historical private development snapshots are intentionally not bundled because they are not runtime dependencies.

## Earlier curriculum-to-textbook capability → v2.1.1

| Earlier capability | v2.1.1 location |
|---|---|
| Source census | G0 + SOURCE_GROUNDED mode |
| Curriculum map | G5 |
| Complete lesson before reconstruction | G6 |
| Long lesson A/B/C split | G6 hard rule |
| Plain language before jargon | Pedagogy protocol |
| Layered glossary | G4/G8 |
| Confusing-concept contrasts | Misconception Map |
| Global map | Knowledge Architecture |
| Reconstruction after lesson construction | G8 |
| Preserve unique knowledge | G7 / DoD |
| Lab / case / quiz / teach-back | Domain + assessment adapters |
| Example vs benchmark distinction | Evidence / QA |
| Read-back QA | G12 |
| Textbook complete != learner mastery | R6 / DoD |

## v2.0-class architecture → v2.1.1 hardening

| Earlier gap | Current repair |
|---|---|
| conversational state dependence | RUN_STATE + checkpoints |
| no reproducible research snapshot | Research Freeze Manifest |
| vague high-impact claim handling | claim criticality |
| source prompt-injection not explicit | untrusted-source protocol |
| examples/labs mostly checklist-validated | executable validation classes |
| autonomous curriculum can omit canonical modules | curriculum triangulation |
| manuscript evidence may drift during editing | post-reconstruction claim audit |
| updates may cause blind rebuild or incomplete patch | revision impact graph |
| static qualification could overclaim | evidence-based qualification tiers |

## Public-release patch

v2.1.1 adds Apache-2.0 licensing, public-release hygiene checks, generic public terminology, and removes non-runtime historical development snapshots from the distribution archive. No textbook-construction capability is intentionally removed.
