# Universal Topic-to-Textbook v2.1.1 Public Release Qualification

Status: **PUBLIC_PACKAGE_READY**

Not claimed: host-independent `RUNTIME_SMOKE_QUALIFIED`.

## Scope

This qualification covers the public distribution package: current capability contracts, licensing, privacy/secret hygiene, generic public terminology, package integrity, research/pedagogy/assessment/publication controls, and preservation of the v2.1 textbook-construction behavior.

## Q1 | Package contract

PASS.

Evidence: `scripts/validate_package.py`.

## Q2 | Behavioral contract fixtures

PASS.

Evidence: `scripts/validate_behavioral_contracts.py` and the routing fixtures under `qualification/fixtures/`.

## Q3 | Public-release hygiene

PASS.

Evidence: `scripts/validate_public_release.py`. It requires Apache-2.0 licensing and scans public text for private course shorthand, local user paths, common secret patterns, version drift, and accidental `legacy/` bundling.

## Q4 | License

PASS.

The public package includes the Apache License 2.0 text in `LICENSE`, plus `NOTICE`.

## Q5 | Private development context

PASS.

Private lesson shorthand and non-runtime historical development snapshots are not bundled in the public distribution. The public documentation describes the underlying method generically as **lesson-first two-pass construction**.

## Q6 | Capability preservation

PASS BY CONTRACT.

The current public specification retains source census, autonomous research, curriculum mapping, lesson-manuscript-first construction, long-lesson splitting, terminology layering, misconception handling, knowledge/dependency maps, second-pass textbook reconstruction, Core/Deep paths, assessment alignment, executable validation, publication QA, cold review, refresh/revision impact, and separation of textbook completion from learner mastery.

Removing `legacy/` from the public archive does not remove runtime capability because the current `SKILL.md`, protocols, templates, schemas, and validators do not depend on it.

## Q7 | Security boundary

PASS BY DESIGN.

`SECURITY.md` and the untrusted-source protocol explicitly isolate source instructions from execution authority and prohibit embedding secrets/private paths in public artifacts.

## Q8 | Bounded execution evidence

PRESERVED.

The bounded v2.1 smoke evidence is retained as `qualification/BOUNDED_LIVE_SMOKE_REPORT_v2.1.1.md`. It demonstrates current/version-sensitive research behavior and numerical recalculation in the build environment. It is not a claim of identical behavior on every future host.

## Q9 | Installed-host runtime smoke

NOT CLAIMED.

Use `qualification/LIVE_SMOKE_TEST_PROMPTS.md` after installing the skill in the intended runtime when host-specific trigger, long-session recovery, or independent reviewer behavior matters.

## Release interpretation

- `DESIGN_QUALIFIED`: YES
- `BOUNDED_EXECUTION_QUALIFIED`: YES
- `PUBLIC_PACKAGE_READY`: YES
- `LICENSE_READY`: YES (Apache-2.0)
- `PRIVACY_SECRET_SCAN`: PASS
- `RUNTIME_SMOKE_QUALIFIED` across arbitrary hosts: NOT CLAIMED

## Final verdict

**PUBLIC_PACKAGE_READY**

The v2.1.1 archive is suitable for public distribution as a skill package. Runtime behavior still depends on the host model and available tools, so host-specific smoke qualification remains separate from package publication readiness.
