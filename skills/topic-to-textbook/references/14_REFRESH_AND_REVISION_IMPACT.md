# Refresh & Revision Impact

## Goal

Update the smallest correct surface without silently leaving stale downstream content.

## Refresh modes

### VOLATILE_REFRESH
Recheck time/version-sensitive claims against the current date or requested cutoff.

### SOURCE_REFRESH
A source changed, moved, corrected, was superseded, or became unavailable.

### SCOPE_REVISION
Audience, depth, domain, jurisdiction, or in/out scope changed.

### CONTENT_REPAIR
A claim, example, lesson, assessment, or visual was found wrong or unclear.

## Revision impact graph

Map the changed item to downstream dependencies:

`Source / Claim → Concept → Lesson → Example/Lab → Assessment → Visual → Summary/Glossary → Final citations`

Only unaffected artifacts may retain PASS.

## Required impact record

For each revision record:

- revision ID
- trigger
- changed source / claim / concept IDs
- affected lesson IDs
- affected assessment IDs
- affected executable validations
- affected visuals
- gates to re-run
- new research freeze ID if needed

## No-blind-rebuild rule

Do not rebuild the whole textbook merely because one volatile claim changed. Conversely, do not patch a sentence if a changed concept invalidates examples and assessments downstream.

## Update publication labels

If the book includes volatile material, record:

- researched through date
- applicable software / standard / jurisdiction versions
- last refresh date
- known future refresh triggers when material
