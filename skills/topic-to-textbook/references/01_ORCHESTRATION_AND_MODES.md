# Orchestration & Mode Selection

## Routing tree

Use the shortest workflow that preserves quality.

1. Only a topic / “research and make a textbook” → `TOPIC_ONLY_AUTONOMOUS`.
2. User provides authoritative source pack / curriculum / handoff → `SOURCE_GROUNDED_EXPANSION`.
3. Completed lessons / transcripts → `TRANSCRIPT_TO_TEXTBOOK`.
4. User explicitly wants paced learning first → `INTERACTIVE_LEARNING_FIRST`.
5. Mixed corpus or only some hard concepts need interaction → `HYBRID`.
6. Existing textbook needs current update / repair / new scope → `REFRESH_OR_REVISION`.

## Non-blocking defaults

Infer language, likely learner level, domain adapter, output format and coherent scope when safe. Ask only when materially different interpretations would create materially different books.

## Autonomous execution

The user should not need to type `continue` after each lesson. Long work uses `RUN_STATE` and intermediate artifacts.

Every formal lesson manuscript must exist before final reconstruction.

## Interactive execution

When paced instruction is requested:

- one lesson at a time
- A/B/C splits allowed
- preserve lesson completion state
- record learner friction
- do not use learner confusion as a reason to shrink the curriculum

## Repair outcomes

- `PASS`: proceed
- `PARTIAL`: bounded repair, recheck
- `BLOCKED`: record specific missing source/capability/access

Do not escalate a repair the builder can safely make autonomously.

## Resume / handoff

Resume from:

1. Scope Contract
2. RUN_STATE
3. active Research Freeze
4. completed gates
5. completed lesson manuscripts
6. open defects
7. pending validation

Do not re-run accepted research unless freshness or dependencies changed.

## Refresh routing

For an existing textbook:

- identify trigger
- calculate revision impact
- invalidate only affected gates/artifacts
- refresh sources / claims
- re-run downstream validation
- issue a new freeze and qualification when needed

See `references/10_RUN_STATE_AND_CHECKPOINTS.md` and `references/14_REFRESH_AND_REVISION_IMPACT.md`.
