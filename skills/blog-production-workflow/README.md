# Blog Production Workflow

> **Status: Public Beta**

A reusable, profile-driven 11+1 workflow for AI-assisted blog and publication production.

It covers roadmap planning, research, editorial planning, article architecture, drafting, evaluation, repair/humanization, visual planning, visual generation, visual acceptance, publish QA, and release handoff.

## Start here

1. Download and extract `BLOG_PRODUCTION_WORKFLOW_11_PLUS_1_PUBLIC_v1.0.0-beta3.zip`.
2. Read `00_START_HERE.md` and `GETTING_STARTED.md`.
3. Complete `SETUP_WORKBOOK.md`.
4. Fill the publication, editorial, visual, repository, deployment, and voice profiles for your own publication.
5. Run `scripts/validate_setup.py`. Continue only after `PUBLICATION_PROFILE_VALID`.
6. Start the workflow at Skill 00.

The public edition does not depend on the original author's private blog configuration. Publication name, locales, series taxonomy, writing voice, repository layout, visual policy, and deployment behavior are supplied through user profiles.

## Qualification

Public Beta2 completed the full independent qualification after the Beta1 repair round. Public Beta3 is a licensing-only rebuild and reran the behavioral suites after adding Apache-2.0 licensing to every nested Skill package:

- 12 / 12 skill packages carry Apache License 2.0
- 51 / 51 package tests passed
- 17 / 17 hostile public-regression tests passed
- 68 executable tests total
- nested manifests and SHA256 inventories were regenerated and verified
- final outer ZIP was re-extracted and matched the sealed source 61 / 61 files

See `QUALIFICATION_SUMMARY.md` and the qualification records inside the distribution ZIP.

## Integrity

Distribution SHA-256:

`679a9e05187b21e84182f62507992a5efd857f1c4763c46bafbf6a90b8a7e94a`

## License

Apache License 2.0. See `LICENSE`.
