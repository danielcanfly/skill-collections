# Universal Exact Schemas

## Required research CSVs

```csv
accepted_sources.csv
source_id,trust_tier,authority,method,directness,recency,independence,applicability,decision,notes

source_family_map.csv
module_id,research_question,source_family,priority,target_examples,status

source_coverage_matrix.csv
module_id,question_id,source_id,coverage,directness,status,gap

claim_ledger.csv
claim_id,module_id,claim,claim_type,source_id,evidence_family_id,support_challenge,scope,confidence,candidate_node,notes

canonical_concept_registry.csv
id,title,kind,module_id,aliases,broader,contrasts,source_ids,maturity,confidence,status

alias_map.csv
alias,canonical_id,language,reason,source

confidence_assessment.csv
canonical_id,confidence,maturity,evidence_basis,conflicts,notes

evidence_family_registry.csv
evidence_family_id,canonical_name,description,source_ids,independence_basis,modules,claims,status,notes

source_metadata_reconciliation.csv
source_id,current_title,verified_title,verified_authors,verified_year,verified_source_type,verified_publisher,verified_doi_or_url,access_status,verification_status,action,evidence_family_id,notes

case_registry.csv
case_id,case_type,title,domain,jurisdiction_or_context,decision_or_problem,source_ids,mechanism,what_was_known_at_the_time,outcome,decision_quality_interpretation,transfer_limit,status

claim_migration_log.csv
old_claim_id,new_claim_id,action,reason,sources_changed,nodes_changed,confidence_change
```

## Required QA files
- `qa/run_retrieval_benchmark.py`
- `qa/validate_package.py`
- `qa/validate_semantic_provenance.py`
- `qa/make_file_manifest.py`
- `qa/finalize_candidate.py`
- `qa/REPRODUCE_RETRIEVAL.md`
- `qa/retrieval_test_cases.json`
- `qa/retrieval_results.json`
- `qa/retrieval_results.md`
- `qa/corpus_manifest.json`
- `qa/package_validation.json`
- `qa/semantic_provenance_validation.json`

## Required handoff files
- `handoff/completion_report.md`
- `handoff/production_build_summary.md`
- `handoff/merge_manifest.json`
- `handoff/file_manifest.json`
- `handoff/cross_topic_overlap.md`
- `handoff/open_gaps_and_update_triggers.md`
- `handoff/source_metadata_reconciliation.csv`
- `handoff/claim_migration_log.csv`

## KOS version
Concept, pattern and checklist frontmatter must use:

```yaml
x-kos-version: "0.1"
```
