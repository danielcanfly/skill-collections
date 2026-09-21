# Universal Research OS Skill v1.0.1

A lossless, public-ready Skill wrapper around two preserved production research operating systems:

- **Universal Research Orchestration OS v10.0.0 — Proof-Carrying Research Construction**
- **Universal Research Audit OS v6.0.0 — Proof-Carrying Research Construction**

The Skill adds a discoverable entry point, routing, progressive disclosure, public usage guidance, and an explicit audit-independence boundary. It does **not** rewrite, simplify, merge, or remove the canonical engines.

## Quick Start

1. Install or place this directory where your Skill-capable ChatGPT/Codex environment can discover `SKILL.md`.
2. Invoke **Universal Research OS** explicitly, or describe a matching research/orchestration/audit task when implicit invocation is enabled.
3. Give the agent the research brief, candidate package, repair target, legacy package, or accepted upstream releases relevant to the task.
4. The Skill reads `router/ROUTING.md`, selects the correct canonical engine/module, and then follows only the required canonical files progressively.
5. For a **formal independent audit**, use a fresh independent session/worker with the standalone Audit OS v6 surface whenever possible. Do not treat same-context self-review as independent proof.

No private credentials, fixed local paths, or owner-specific environment configuration are required by the Skill wrapper. External tools, source access, credentials, or runtime permissions needed by a particular research job remain the responsibility of that job/runtime and must not be invented.

## Example Prompts

### Start a new research program

> Use Universal Research OS to build a proof-carrying research program for [topic]. Create the correct research handoff, follow the canonical v10 construction stages, and stop at every required external-review or admission gate.

### Run an independent candidate audit

> Use Universal Research OS to independently audit this candidate package. Bind the audit to the exact candidate SHA, use the standalone Audit OS v6 path, remain read-only, and report the canonical audit result and findings.

### Repair a failed candidate

> Use Universal Research OS to take this admitted candidate plus its independent audit findings and perform the smallest bounded repair allowed by the canonical v10 repair contract. Preserve the protected baseline and prove class-wide closure where required.

### Migrate a legacy research package

> Use Universal Research OS to migrate this older research package into the current v10 proof-carrying contract. Freeze the legacy identity, use the approved migration path, and do not grandfather missing evidence.

### Integrate multiple completed phases

> Use Universal Research OS to reconcile these accepted, audited production releases into a global knowledge release. Follow the canonical Global Builder stages, preserve exact upstream identities, and complete all required global audit/seal gates.

### Promote and release

> Use Universal Research OS to revalidate this exact upstream production release and run the canonical production-promotion and final-release workflow, including manifests, checksums, and required acceptance gates.

## What changed in v1.0.1

Public-release polish only:

- added `agents/openai.yaml` with user-facing metadata, a default prompt, and implicit-invocation policy;
- expanded this README with Quick Start and reusable example prompts for first-time users;
- added the standard **Apache License 2.0** at `LICENSE`;
- strengthened package verification so these public wrapper surfaces are checked as part of qualification.

No canonical engine file changed.

## What is preserved

- Full Orchestration v10 extracted tree
- Full standalone Audit v6 extracted tree
- Orchestration v10's embedded Audit v6 copy
- Both original upstream ZIP files
- Every original script, schema, validator, template, fixture, manifest, checksum file, and document

## Why one Skill but two engines?

Users get one discoverable entry point, while construction/orchestration and independent audit retain different authority boundaries. The standalone Audit surface remains available specifically so a fresh independent worker can audit without seeing repair or dispatcher tooling.

## Skill layout

```text
UNIVERSAL_RESEARCH_OS_SKILL_v1.0.1_PUBLIC_RELEASE/
├── SKILL.md                         # Skill entry point and invariant layer
├── agents/openai.yaml              # OpenAI UI/invocation metadata
├── README.md                        # Public quick start and examples
├── LICENSE                          # Apache License 2.0
├── QUALIFICATION.md                 # Qualification receipt
├── VERSION.json
├── SOURCE_PROVENANCE.json
├── PACKAGE_MANIFEST.json
├── SHA256SUMS.txt
├── router/
│   ├── ROUTING.md
│   └── INDEPENDENCE_BOUNDARY.md
├── scripts/
│   └── verify_skill_package.py
├── canonical_sources/              # Immutable original upstream ZIPs
└── engines/                        # Byte-for-byte extracted canonical engines
```

## Verify

From this directory:

```bash
python scripts/verify_skill_package.py
```

A successful run prints:

```text
PASS: UNIVERSAL_RESEARCH_OS_SKILL package verified
```

The verifier checks canonical ZIP identities, byte-for-byte extracted-tree fidelity, standalone/embedded Audit parity, package checksum membership, version identity, and the required public Skill wrapper files.

## License

This release includes the standard **Apache License 2.0**. See `LICENSE`.
