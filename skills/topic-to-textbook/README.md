# Topic to Textbook

A reusable AI Skill for turning a topic, curriculum, source pack, handoff, existing textbook, or teaching transcript into a research-grounded, beginner-readable, technically rigorous textbook.

**Version:** 2.1.1  
**Skill name:** `universal-topic-to-textbook`  
**License:** Apache-2.0  
**Release status:** Public Package Ready

---

## What this Skill does

Topic to Textbook is designed for cases where the user wants more than a long answer or a one-shot document.

It can take a broad topic such as:

- Agent Evaluation
- Kubernetes Autoscaling
- Working Capital
- Model Serving
- Enterprise SaaS Pricing
- Financial Statement Analysis
- Experiment Design
- Regulation and Policy
- Scientific or Engineering Concepts
- Historical Topics
- Quantitative Topics
- Language Learning
- Procedural or How-to Topics

and turn it into a structured learning system with:

- broad research
- source and evidence tracking
- curriculum design
- prerequisite ordering
- lesson-by-lesson manuscript construction
- misconception handling
- worked examples and practice
- assessment alignment
- textbook reconstruction
- fact and claim validation
- executable or numerical validation where possible
- publication QA
- refresh and revision support

The core idea is simple:

> **Research first. Build the knowledge structure second. Write complete lessons third. Reconstruct the textbook only after the lessons are complete.**

The Skill intentionally avoids the common failure mode of going directly from "research this topic" to "write me a textbook" in one pass.

---

## Why it exists

High-quality teaching material needs several things to be correct at the same time:

1. the research must be correct;
2. the scope must be complete;
3. prerequisite order must make sense;
4. explanations must work for the intended reader;
5. examples and calculations must be valid;
6. the final book must preserve source meaning;
7. assessments must test what the book actually teaches;
8. time-sensitive facts must remain traceable and refreshable.

Topic to Textbook treats these as separate quality problems instead of collapsing them into one writing step.

Its quality chain is:

`Research correctness -> Curriculum correctness -> Teaching quality -> Learning effectiveness -> Execution validity -> Publication quality`

---

## Quick start

You can give the Skill only a topic:

```text
Research Agent Evaluation broadly and turn it into a complete beginner-friendly textbook.
```

You can give it a topic plus an audience:

```text
Build a complete textbook on Kubernetes Networking for a product manager who is technical but does not operate clusters day to day.
```

You can give it an authoritative source pack:

```text
Use these files as the authoritative basis and expand them into a textbook. Preserve the source terminology and scope.
```

You can give it teaching transcripts:

```text
Rebuild these teaching sessions into a clean textbook. Preserve unique knowledge but remove chatty repetition.
```

You can also refresh an existing textbook:

```text
Update this textbook to current versions. Revalidate only chapters affected by changed sources or time-sensitive claims.
```

---

## Supported operating modes

The Skill routes each task into the appropriate workflow.

| Mode | Use when |
|---|---|
| `TOPIC_ONLY_AUTONOMOUS` | You provide only a topic, or ask for research before textbook construction. |
| `SOURCE_GROUNDED_EXPANSION` | You provide a curriculum, source pack, handoff, research package, or authoritative files. |
| `TRANSCRIPT_TO_TEXTBOOK` | Most of the teaching already exists as lesson transcripts or session logs. |
| `INTERACTIVE_LEARNING_FIRST` | You want to be taught first, then turn the completed learning process into a textbook. |
| `HYBRID` | Some material can be built directly while difficult sections need interactive teaching or deeper development. |
| `REFRESH_OR_REVISION` | An existing textbook needs updated facts, versions, sources, chapters, or targeted revalidation. |

The Skill is designed to continue long-running work through durable run state instead of requiring the user to repeatedly type "continue".

---

## How the workflow works

A typical topic-only run follows this sequence:

### 1. Scope the textbook

Define:

- topic
- intended audience
- in-scope and out-of-scope material
- language
- temporal cutoff
- expected artifact
- authoritative sources, if any

### 2. Research the landscape

The Skill first understands the field before designing the curriculum.

Research can include:

- landscape research
- primary-source deep dives
- standards and official documentation
- gap-driven research
- challenge or falsification search
- current-version verification
- curriculum triangulation against multiple mature frameworks or taxonomies

This is used for omission detection, not for copying someone else's syllabus.

### 3. Freeze the evidence base

Important claims are tracked in an evidence ledger.

Claims may be classified as:

- `CRITICAL`
- `MAJOR`
- `SUPPORTING`

Time-sensitive or version-sensitive facts are tied to dates, versions, releases, commits, or other locators where appropriate.

A research freeze can then record the evidence state used to construct the textbook.

### 4. Build the knowledge architecture

Before writing lessons, the Skill constructs:

- Knowledge Map
- Concept Dependency Graph
- Core Path vs Deep Path
- Terminology Layers
- Misconception Map
- domain-specific teaching grammar

This prevents later chapters from depending on concepts that have not been introduced yet.

### 5. Build the curriculum

Each lesson receives:

- a core question
- prerequisites
- learning objectives
- key concepts
- required examples, cases, or practice
- assessment targets

Lesson count is determined by the knowledge graph, not by an arbitrary fixed number.

### 6. Write complete lesson manuscripts

Each lesson is developed as a complete teaching unit before the textbook is assembled.

A typical lesson includes:

- purpose or problem
- prerequisite bridge
- beginner mental model
- formal terminology
- mechanism or causal process
- worked example or concrete case
- misconception or contrast
- real-world implication
- Core Path summary
- optional Deep Path
- retrieval, explanation, application, or transfer practice
- provenance hooks

Long lessons can be split into A/B/C sections rather than compressed until important knowledge disappears.

### 7. Audit cross-lesson consistency

The Skill checks for:

- missing concepts
- prerequisite inversions
- terminology drift
- contradictions
- accidental duplication
- orphan assessments
- missing source requirements
- scope loss

### 8. Reconstruct the textbook

Only after all lesson manuscripts are complete does the Skill perform editorial reconstruction.

Typical textbook surfaces include:

- first-read guide
- layered glossary
- global map, timeline, or system map
- core chapters
- Deep Path sections
- misconception boxes
- domain-appropriate labs, cases, exercises, or worked examples
- assessments
- separate answer keys
- rapid review
- sources and further reading

### 9. Audit the finished book

The final textbook is checked again against the evidence base.

This catches cases where editing accidentally:

- strengthens a claim
- broadens a claim
- removes a qualifier
- drops a version or date
- turns a contested claim into an absolute statement
- leaves a citation supporting an older sentence rather than the final edited sentence

### 10. Validate learning and execution

Where applicable, the Skill checks:

- cognitive load
- terminology density
- worked examples
- guidance fading
- retrieval practice
- explanation quality
- application
- transfer
- assessment alignment
- formulas
- units
- finance calculations
- SQL
- code
- commands
- labs
- API examples

Executable material is run, recalculated, or dry-run when the available environment and safety constraints allow it.

If execution is not possible, the Skill should say so instead of claiming runtime validation.

### 11. Publication QA

For document outputs such as DOCX, PDF, Slides, or web artifacts, the workflow can include read-back or render checks for:

- headings
- table of contents
- page breaks
- tables
- code
- equations
- fonts
- citations
- answer separation
- final-page integrity
- accessibility where relevant

### 12. Cold review and release readiness

A fresh reviewer is preferred when available.

The reviewer checks the scope, evidence, curriculum, textbook, validation outputs, and open defects without giving credit merely because a large amount of work was completed.

---

## Domain-aware textbook design

The Skill uses a universal quality core, but it does not force one teaching format onto every subject.

Supported domain families include:

- AI / ML / LLM
- AI Agents / MCP / Tooling
- Software / Cloud / Infrastructure / DevTools
- Product / Product Management / Enterprise SaaS
- Business / Strategy / Business Models
- Finance / Accounting / Financial Analysis
- Data / Analytics / Experimentation
- Science / Engineering
- Legal / Regulation / Policy
- General Conceptual / Academic
- Procedural / How-to
- Quantitative / Mathematical
- Historical / Narrative
- Language Learning

A textbook may mix multiple adapters, but one primary teaching grammar should remain dominant.

For example:

- a technical infrastructure textbook may emphasize architecture, mechanics, failure modes, labs, and troubleshooting;
- a finance textbook may emphasize concepts, formulas, worked calculations, interpretation, and decision traps;
- a historical textbook may emphasize chronology, context, causality, competing interpretations, and source boundaries;
- a language textbook may emphasize vocabulary, patterns, input, examples, production, and spaced practice.

---

## Lesson-first two-pass construction

One of the most important design rules in this Skill is the two-pass construction model.

### Pass 1: Build the lessons

Every lesson is fully developed first.

This protects:

- explanation depth
- examples
- prerequisite bridges
- edge cases
- misconceptions
- source-derived details
- learner friction discovered during teaching

### Pass 2: Reconstruct the textbook

After all lessons are complete, the material is re-edited into a coherent book.

This removes:

- repetitive recap
- duplicated analogies
- conversational filler
- repeated definitions

without deleting unique knowledge.

The goal is not to make the textbook shorter at any cost. The goal is to make it cleaner without making it shallower.

---

## Source-grounded behavior

When user-provided material is designated as the authoritative basis, the Skill preserves its:

- terminology
- organization
- framing
- scope
- level of detail

External research may be used for validation or enrichment, but it should not silently replace the source.

This is especially important for:

- internal company material
- course handoffs
- regulated content
- research packages
- domain-specific frameworks
- existing curricula

---

## Research and evidence rules

When current web research is available, the Skill prefers:

- primary sources
- official documentation
- standards
- regulators
- original data
- peer-reviewed research where appropriate

Search snippets are treated as discovery aids, not as final evidence.

For PDFs, filings, papers, or standards, the relevant section or page should be inspected when possible.

Time-sensitive claims such as versions, prices, benchmarks, regulations, product behavior, and current specifications should be date- or version-qualified.

Contested claims should preserve attribution, scope, and disagreement.

High-stakes domains should use stricter source thresholds and preserve relevant jurisdiction, population, or constraint boundaries.

---

## Executable validation

The Skill distinguishes between material that has been written and material that has actually been validated.

Possible validation states include:

- `EXECUTED`
- `RECALCULATED`
- `DRY_RUN_VALIDATED`
- `SOURCE_VALIDATED`
- `UNEXECUTED`
- `NOT_RUNTIME_VALIDATED`

Examples:

- a finance example can be recalculated;
- a formula can be checked numerically;
- SQL can be executed when a safe database is available;
- code can be run when the environment permits;
- a shell command can be dry-run or tested in a safe environment;
- a lab can be marked unvalidated when the required runtime does not exist.

The Skill should never present unexecuted material as runtime-validated.

---

## Assessment and mastery

Assessment should map back to explicit learning objectives.

The Skill distinguishes among:

- recall
- explanation
- application
- transfer

A textbook is not considered evidence that a learner has mastered the material.

Likewise:

- seeing the answer is not the same as solving the problem;
- reading an explanation is not the same as passing an assessment;
- textbook completion and learner mastery remain separate states.

---

## Refreshing an existing textbook

The Skill supports targeted updates rather than blindly rebuilding an entire textbook.

A revision can track:

- changed sources
- changed versions
- volatile claims
- affected concepts
- downstream lessons
- examples
- assessments
- visuals
- citations

A revision impact map can then determine which parts need revalidation.

This makes the workflow suitable for textbooks about fast-moving topics such as AI tooling, cloud platforms, APIs, standards, regulation, and product ecosystems.

---

## Typical outputs

A high-quality run may produce some or all of the following:

- Scope Contract
- RUN_STATE
- Research Map
- Evidence Ledger
- Research Freeze Manifest
- Knowledge Map
- Concept Dependency Graph
- Misconception Map
- Curriculum Map
- Lesson Manuscripts
- Learner Friction Log
- Coverage Matrix
- Assessment Alignment Matrix
- Executable Validation Log
- Revision Impact Map
- Cold Review
- Final Qualification
- Final Textbook

The exact artifact set depends on the selected mode and domain.

---

## Package structure

```text
topic-to-textbook/
├── SKILL.md
├── README.md
├── LICENSE
├── NOTICE
├── SECURITY.md
├── CHANGELOG.md
├── MIGRATION_AND_CAPABILITY_MAP.md
├── references/
├── templates/
├── schemas/
├── examples/
├── qualification/
└── scripts/
```

### Important directories

- `SKILL.md` - routing, invariants, gate sequence, and Definition of Done
- `references/` - research, evidence, pedagogy, domain, safety, execution, QA, and refresh protocols
- `templates/` - reusable run artifacts and audit surfaces
- `schemas/` - machine-readable run state and research freeze contracts
- `examples/` - domain routing examples
- `qualification/` - behavioral fixtures, reports, smoke prompts, and test matrix
- `scripts/` - package, behavioral-contract, and public-release validators

Keep the folder intact so the Skill can access its supporting protocols, templates, schemas, and validation assets.

---

## Installation and use

Place or install the complete `skills/topic-to-textbook/` directory in a Skill-capable AI environment.

The exact installation mechanism depends on the host.

After installation, invoke the Skill explicitly or use a request that clearly matches its purpose.

Example:

```text
Use Topic to Textbook to research model serving and build a complete textbook for a technical product manager.
```

For environments where host-specific runtime behavior matters, use:

`qualification/LIVE_SMOKE_TEST_PROMPTS.md`

to test triggering, long-run continuation, routing, and reviewer behavior.

---

## Qualification status

The public v2.1.1 package is qualified as:

- `DESIGN_QUALIFIED: YES`
- `BOUNDED_EXECUTION_QUALIFIED: YES`
- `PUBLIC_PACKAGE_READY: YES`
- `LICENSE_READY: YES`
- `PRIVACY_SECRET_SCAN: PASS`

The package does **not** claim identical runtime behavior across every AI host.

`RUNTIME_SMOKE_QUALIFIED` remains host-specific and should be tested after installation when that guarantee matters.

See:

- `qualification/QUALIFICATION_REPORT_v2.1.1.md`
- `qualification/BOUNDED_LIVE_SMOKE_REPORT_v2.1.1.md`
- `qualification/TEST_MATRIX.md`

---

## Safety and trust boundaries

External content is treated as source material, not as authority to change the Skill's instructions or tool permissions.

Web pages, PDFs, repositories, pasted prompts, READMEs, comments, datasets, and attached documents may contain instruction-like text. The Skill treats such text as untrusted source content unless the user explicitly asks for those instructions to be executed.

The Skill also separates:

- source claims from execution authority
- documentation from runtime proof
- hypothetical examples from benchmarks
- textbook completion from learner mastery

See `SECURITY.md` and `references/12_UNTRUSTED_SOURCES_AND_EXECUTION_SAFETY.md`.

---

## Public release principles

This public package is designed to be:

- self-contained
- portable
- inspectable
- evidence-aware
- refreshable
- domain-agnostic
- safe to redistribute under Apache-2.0

Private development shorthand, personal local paths, secrets, and non-runtime historical development artifacts are intentionally excluded from the public release.

---

## License

Licensed under the Apache License 2.0.

See:

- `LICENSE`
- `NOTICE`

---

## Summary

Topic to Textbook is for users who want an AI system to do more than produce a long document.

It is built to turn research into a teachable knowledge structure, turn that structure into complete lessons, turn those lessons into a coherent textbook, and then validate the finished artifact against its sources, calculations, learning objectives, and publication requirements.

If the starting point is only a topic, the Skill can begin with research.

If the starting point is an authoritative source pack, it can preserve and expand it.

If the starting point is a set of teaching sessions, it can reconstruct them into a cleaner book.

If the starting point is an older textbook, it can refresh only what changed.

That is the full purpose of Topic to Textbook.
