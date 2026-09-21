# Shared Semantic Truth Model

The following records remain stable across dispatch, production, audit, repair, reconciliation, and release:

- SourceIdentity
- EvidenceFamily
- AtomicClaim
- ClaimSourceEdge
- EdgeEntailment
- ContextualRelevance
- CanonicalNode
- NodeLineage
- EvidenceBackedCase
- OwnershipDecision
- MigrationDecision
- ManualSemanticAuditReceipt
- AuditFinding
- FindingDisposition / Waiver
- SealState

Modules may add fields but may not reinterpret universal fields.


# V7 Independent Semantic Objects

- `MaterialClaimClause`: smallest decision-relevant clause whose support must be assessed independently.
- `SourcePassageSnapshot`: immutable excerpt/snapshot, exact locator grammar, and cryptographic hashes.
- `SourceClaimCompatibility`: source domain, claim domain, source kind, transfer rule, and compatibility verdict.
- `CandidateSelfCheck`: child-authored QA that can never grant merge readiness.
- `IndependentSemanticReview`: external auditor artifact bound to candidate SHA-256.
- `ClassWideRepairClosure`: closure of every row matching a failure class, not only listed examples.
- `ArtifactChronology`: monotonic ordering of research, review, seal, manifest, ZIP and independent audit events.

# V8 Production Assurance Objects

- `ReproductionContract`: script-relative commands and byte-deterministic declared outputs.
- `ProductionSurfaceManifest`: authoritative data surfaces, audit-only roots and R2 object plan.
- `SourceProductionEligibility`: explicit identity, temporal, access and enrichment closure verdict.
- `AuditedProductionReleaseReceipt`: exact candidate SHA, Audit OS v6 six dimensions and zero-open-finding seal.
- `GlobalFiveSurfaceAcceptance`: one-lineage acceptance for combined, KOS, OKF, R2 and audit bundles.

A filename cannot create a lifecycle state. Only governed receipts may grant `AUDITED_PRODUCTION_RELEASE` or `GLOBAL_MERGE_READY`.
