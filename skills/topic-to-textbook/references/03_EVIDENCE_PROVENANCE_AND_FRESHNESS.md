# Evidence, Provenance & Freshness

## Evidence Ledger fields

For evidence-bearing claims / concepts track:

- Claim ID
- claim / concept
- criticality: CRITICAL / MAJOR / SUPPORTING
- lesson / concept IDs
- source ID(s)
- source type
- publication / effective date
- access date
- version / release / edition / commit when relevant
- locator
- provenance class
- freshness class
- confidence
- contradiction / boundary notes
- Final Textbook Locator after reconstruction

## Provenance

- `SOURCE_DERIVED`: user-provided authoritative material
- `WEB_RESEARCHED`: external research
- `LEARNER_DERIVED`: learner interaction revealed a gap / better teaching bridge
- `EDITORIAL_BRIDGE`: connective teaching text; must not smuggle unsupported facts
- `HYPOTHETICAL_EXAMPLE`: invented teaching scenario

## Freshness

- `STABLE`
- `VERSION_SENSITIVE`
- `TIME_SENSITIVE`
- `CONTESTED`

## Criticality

Use the requirements in `references/11_RESEARCH_FREEZE_AND_CLAIM_CRITICALITY.md`.

Do not require identical evidence effort for every sentence. Spend rigor where error consequences are highest.

## Two-layer citation model

Close-to-claim citations for numeric, legal/policy, version, benchmark, contested, surprising and CRITICAL claims when appropriate.

Chapter-end Sources / Further Reading can support stable background concepts where line-by-line citation would hurt readability.

Internal Evidence Ledger remains more detailed than the publication surface.

## Contradictions

When sources disagree, check:

1. date / version
2. jurisdiction / population / sample
3. definitions
4. methodology / benchmark setup
5. vendor / institutional incentives
6. whether claims answer different questions

If disagreement remains, teach it and its boundary.

## Source-grounded integrity

When user sources are authoritative:

- preserve material terminology / framing / structure
- do not silently “correct” them with general knowledge
- separate `source says` from `external research says`
- do not attribute unsupported claims to the source

## Post-reconstruction claim mapping

After textbook reconstruction, update the ledger with final-book locators for CRITICAL / MAJOR claims and run reverse support checks.

## Hypothetical examples

Invented numbers that could look like benchmarks must be labeled Example / Illustrative / Assumption or equivalent.
