# Research Freeze & Claim Criticality

## Why freeze research

A textbook needs a reproducible evidence state. Without a freeze, later edits may quietly mix different versions, dates, regulations, releases, or benchmark definitions.

## Claim criticality

Classify evidence-bearing claims:

### CRITICAL
If wrong, the reader may learn the core model incorrectly, make an unsafe/high-stakes decision, misunderstand a governing rule, or invalidate a central conclusion.

Expected treatment:

- strongest practical source tier
- explicit scope / date / version
- cross-check with a second independent strong source when materially possible
- contradiction search
- close-to-claim citation in final textbook when appropriate

### MAJOR
Important to a lesson or decision but a local error does not invalidate the whole textbook.

Expected treatment:

- strong source
- date/version qualification if volatile
- second source when uncertainty, vendor bias, or contested interpretation is material

### SUPPORTING
Background, illustrative context, low-impact factual detail, optional enrichment.

Expected treatment:

- credible support
- do not over-invest research effort relative to learning value

Criticality is about consequence of error, not how interesting a claim sounds.

## Research Freeze Manifest

Create after the Research Sufficiency Gate and before final lesson construction is considered stable.

For material sources record:

- source ID
- canonical URL / document identifier
- title
- publisher / authority
- source type
- publication / effective date
- access date
- version / release / standard edition / commit when applicable
- exact locator(s)
- freshness class
- supported claim IDs / concept IDs
- snapshot / archive / checksum when the environment and rights permit
- notes on known limitations

## Freeze ID

Use a stable freeze identifier such as:

`RF-2026-09-21-01`

All downstream manuscripts and final qualification should name the active freeze.

## Re-freeze conditions

Create a new freeze if any of the following materially changes:

- temporal cutoff
- software / API / standard version
- regulation / policy
- benchmark methodology
- source correction or retraction
- core scope
- CRITICAL claim evidence

Do not mutate an accepted freeze invisibly. Supersede it.

## Freshness expiry

The skill should define refresh triggers by content type, not a universal number of days.

Examples:

- stable mathematical identity: no routine expiry
- software feature / API behavior: refresh when version/current-status matters
- price / market / leadership / schedules: refresh near publication/use time
- law / regulation: refresh against current jurisdiction/effective date

## Post-freeze additions

If a new source is added after freeze:

- mark it `POST_FREEZE_ADDITION`
- explain why it was necessary
- update impacted claim IDs
- run revision impact analysis
- either amend under a new freeze ID or explicitly record the exception before release
