# QA & Publication Protocol

## A｜Coverage QA

- every scope item covered
- source requirements mapped
- unique knowledge preserved
- no missing lesson
- curriculum triangulation omissions resolved

## B｜Evidence / Claim Drift QA

- CRITICAL / MAJOR claims trace to evidence
- final wording has not become broader/stronger than evidence
- qualifiers, jurisdiction, version and date survived reconstruction
- volatile facts are current or dated
- contested claims are attributed
- citations support the final sentence, not only the old manuscript

## C｜Pedagogy QA

- prerequisites before dependents
- beginner bridges where needed
- terminology layering
- worked examples representative
- scaffolding fades
- retrieval / transfer appropriate
- Core Path independently readable

## D｜Consistency QA

Search across the full book for:

- term definitions
- abbreviations
- units
- formulas
- actor / component names
- architecture labels
- date / version references
- repeated examples with inconsistent numbers

## E｜Example / Calculation / Execution QA

Every important example should be:

- correct
- representative
- boundary-safe
- numerically valid
- clearly hypothetical if invented
- consistent with later chapters

Use executable validation classes from `references/13_EXECUTABLE_VALIDATION_AND_LABS.md`.

## F｜Assessment QA

- objectives aligned
- answers correct
- no unseen concept tested
- application / transfer differ materially from copied examples
- mastery remediation points to actual corrective material

## G｜Publication QA

If generating files:

- open / render / read back
- inspect first pages, dense pages, tables, figures, quiz/answer boundary, final pages
- no missing glyphs
- code/equations do not overflow
- heading hierarchy / TOC correct
- page breaks sensible
- citations readable
- accessibility alternatives where needed

File creation success alone is not PASS.

## H｜Run-state QA

Before release:

- RUN_STATE current gate/status matches artifacts
- no unresolved CRITICAL defects
- active freeze ID matches final qualification
- pending validations are zero or explicitly qualified
- revision impact set is closed

## Cold Review rubric

A fresh reviewer should answer:

1. What is the book trying to teach?
2. Can a beginner enter without hidden prerequisites?
3. What are the hardest sections?
4. Which claims look weakly sourced?
5. Did any claim become stronger than its source?
6. Where does terminology drift?
7. What is duplicated?
8. What important idea is missing?
9. Do assessments test objectives?
10. Is any example misleading or unvalidated?
11. Are volatile facts visibly scoped/date-stamped?
12. What would block PUBLIC_READY?

Critical defects must be repaired before `TEXTBOOK_COMPLETE`.
