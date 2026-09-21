# Universal Child Session Phase 1–10

This process applies to any research topic. The topic-specific content must be supplied by the master dispatcher.

## Phase 1｜Scope, boundaries and questions
- Restate mission, canonical ownership and exclusions.
- Build inclusion/exclusion criteria.
- Decompose core questions into searchable subquestions.
- Create provisional taxonomy, concept registry and aliases.
- Record cross-topic overlaps.
- Define completion by evidence coverage, not word count.

Required:
- `research/phase01_scope.md`
- `research/inclusion_exclusion.md`
- `research/research_questions.md`
- `research/provisional_concept_registry.csv`
- `handoff/cross_topic_overlap.md`

Gate:
- Topic exactly matches assigned brief.
- No unrelated topic invention.
- Ownership and exclusions are explicit.
- Every seed concept has a provisional owner.

## Phase 2｜Source landscape
- Map original authors, official standards, academic reviews, empirical evidence, practitioner guidance and criticism.
- Build exact, alias, origin, critique, empirical and case queries.
- Identify paywalls, inaccessible full text and alternative access paths.
- Require at least two independent source families for every core question.

Required:
- `research/phase02_source_landscape.md`
- `research/search_query_bank.md`
- `research/source_family_map.csv`
- `research/paywall_and_access_gaps.md`

Gate:
- Every core question has a credible source route.
- No dependence on a single consultant, institution or framework.
- Criticism and failure sources are included.

## Phase 3｜Deep acquisition
- Run multi-round search.
- Backward, forward, version, maintainer and critique chaining.
- Record metadata and access level.
- Inspect PDFs, tables, methods and relevant pages directly.
- Create raw registry and initial source notes.

Required:
- `research/raw_source_registry.csv`
- `research/acquisition_log.md`
- `research/source_coverage_matrix.csv`
- `knowledge/sources/*.md`

Gate:
- Topic-specific source floor is reached or gaps are documented.
- Core concepts have primary/authoritative candidates.
- No claim of reading inaccessible full text.

## Phase 4｜Source reconciliation, quality and deduplication
- Verify title, author, year, venue, DOI/official URL, version and access level.
- Group reprints, mirrors, summaries and derivative versions.
- Assess authority, method, directness, recency, independence, applicability and bias.
- Separate accepted, background-only and rejected.
- Build evidence-family registry.

Required:
- `research/source_metadata_reconciliation.csv`
- `research/accepted_sources.csv`
- `research/rejected_sources.csv`
- `research/deduplication_report.md`
- `research/source_quality_rubric.md`
- `research/evidence_family_registry.csv`

Gate:
- Accepted sources are verified/corrected.
- Search pages and metadata mismatches are removed.
- Same underlying evidence is not counted repeatedly.

## Phase 5｜Atomic claims and framework extraction
- Extract definitions, mechanisms, conditions, benefits, limitations, failures, examples and evidence.
- Separate source claim, subagent inference and canonical synthesis.
- Use one row per claim-source-node relation.
- Mark support, partial-support, contextual-support or challenge.
- Build framework comparison.

Required:
- `research/claim_ledger.csv`
- `research/framework_comparison_matrix.csv`
- `research/unresolved_claims.md`
- complete source notes

Gate:
- Important claims are traceable and atomic.
- No broad claim is directly attributed to a source that supports only one clause.
- Synthesis boundaries are explicit.

## Phase 6｜Canonicalisation and ontology
- Merge aliases, abbreviations, translations and near-duplicates.
- Decide concept, pattern, checklist or source note.
- Record merge/split/broader/narrower/contrast decisions.
- Assign one canonical ID/path.
- Cross-topic content becomes links or overlap records, not duplicate nodes.

Required:
- `research/canonical_concept_registry.csv`
- `research/alias_map.csv`
- `research/merge_split_decisions.md`
- `research/ontology_map.md`

Gate:
- Unique IDs and boundaries.
- No synonym duplicates.
- Ownership conflicts are recorded.

## Phase 7｜Conflicts, gaps and confidence
- Analyse definition, scope, empirical, normative, method, version and jurisdiction conflicts.
- Record missing perspectives, counterexamples and applications.
- Assess maturity, confidence and transfer limits.
- Preserve unresolved disagreements.

Required:
- `research/conflict_matrix.md`
- `research/gap_register.md`
- `research/confidence_assessment.csv`
- `research/open_questions.md`
- `research/topic_semantic_risk_resolution.csv`

Gate:
- Major conflicts and limits are visible.
- Confidence is evidence-based.
- Topic-specific semantic risks are resolved, bounded, deferred or marked open.

## Phase 8｜KOS-OKF synthesis
- Use the original templates.
- One principal concept/pattern/checklist per file.
- Add definitions, boundaries, mechanism, use/not-use, failures, implementation and links.
- Source notes distinguish direct, partial, contextual and unsupported interpretations.
- Current facts stay in source notes/appendices with as-of dates.

Required:
- `knowledge/concepts/*.md`
- `knowledge/patterns/*.md`
- `knowledge/checklists/*.md`
- `knowledge/sources/*.md`
- `knowledge/index.md`
- `knowledge/log.md`

Gate:
- Template compliance.
- No giant framework dump.
- All source IDs exist.
- No query leakage in aliases.

## Phase 9｜Graph, lineage, retrieval and reasoning QA
- Check duplicate IDs/titles, broken links, unresolved relations and orphans.
- Verify bidirectional node-source-claim lineage.
- Run definition, comparison, how-to, decision, audit, provenance, multi-hop and adversarial retrieval tests.
- Include Chinese and English queries.
- Freeze corpus hash and full rankings.

Required:
- `qa/link_validation.md`
- `qa/orphan_and_duplicate_report.md`
- `qa/retrieval_test_cases.json`
- `qa/retrieval_results.json`
- `qa/retrieval_results.md`
- `qa/corpus_manifest.json`
- `qa/source_traceability_report.md`
- machine-readable validator outputs

Gate:
- Zero errors and unresolved warnings.
- At least 40 retrieval tests, 25% holdout.
- Claim-source support is semantically correct.

## Phase 10｜Refinement, acceptance and handoff
- Remove repetition and repair terminology.
- Update maturity, confidence and review dates.
- Complete case registry, manifests, overlap and update triggers.
- Run finaliser and test ZIP integrity.

Required:
- `handoff/completion_report.md`
- `handoff/production_build_summary.md`
- `handoff/merge_manifest.json`
- `handoff/file_manifest.json`
- `handoff/cross_topic_overlap.md`
- `handoff/open_gaps_and_update_triggers.md`
- `qa/final_acceptance_checklist.md`
- final production-candidate ZIP

Gate:
- All contracts pass.
- The reconciliation session can merge without guessing.
