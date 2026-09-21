# Retrieval, Graph, Portable Reproduction and Packaging QA v10

## Retrieval design

At least 40 tests covering definition, comparison, how-to, decision/application, audit, source provenance, multi-hop, adversarial, Chinese and English. At least 25% must be holdout and 25% must include meaningful negative IDs. Expected and negative IDs may never influence ranking.

## Portable deterministic reproduction

`qa/reproduction_contract.json` is mandatory. Every command uses script-relative root resolution, contains no machine-specific path and runs successfully in an isolated copy. Declared outputs must regenerate byte-for-byte. The contract must include retrieval; final global releases also include release self-check.

## Graph and lineage

Validate duplicate IDs/titles, broken links, unresolved relations/sources, orphan production nodes and semantic bidirectionality.

## Production surfaces

`qa/production_surface_manifest.json` or `release/production_surface_manifest.json` identifies authoritative data surfaces and audit-only roots. R2 excludes tests, fixtures, QA, audit, synthetic candidates, provisional output, caches and temporary artifacts.

## Manifest and seal

Generate receipts first, manifest last, deterministic ZIP after manifest, fresh-extract, rerun read-only checks and prove zero mutation. Production requires zero open P0/P1/P2.
