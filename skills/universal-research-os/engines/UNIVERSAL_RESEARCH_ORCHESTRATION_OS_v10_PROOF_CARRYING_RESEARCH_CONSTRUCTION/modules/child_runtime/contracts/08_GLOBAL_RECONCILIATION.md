# Global Reconciliation Contract for the Master Dispatcher

Child production candidates are not merged by concatenation.

## Reconciliation phases

### R1｜Inventory
- Extract every child package.
- Record nodes, sources, claims, cases, IDs, paths and manifests.
- Verify each child validator output and ZIP integrity.

### R2｜Ownership
- Compare each child package with the canonical ownership registry.
- Identify duplicate or stolen concepts.
- Select one canonical owner.
- Convert non-owner duplicates into links, contextual notes or removal decisions.

### R3｜IDs and aliases
- Detect duplicate IDs/titles.
- Reconcile aliases, translations and historic names.
- Create migration records for renamed IDs.

### R4｜Sources and evidence families
- Merge identical source records by canonical DOI/URL/title-author-year.
- Reconcile version relationships.
- Merge evidence families without destroying child provenance.
- Detect the same underlying study counted in multiple packages.

### R5｜Claims and conflicts
- Detect duplicate, complementary and contradictory claims.
- Keep separate scopes when claims only appear contradictory.
- Preserve challenge sources and dissent.
- Record global confidence decisions.

### R6｜Cross-links
- Replace placeholders with canonical Markdown links and related IDs.
- Validate bidirectional relations.
- Avoid importing domain-specific current facts into universal concepts.

### R7｜Global retrieval
- Build cross-topic queries and multi-hop tests.
- Test near-neighbour confusion between child domains.
- Include source-provenance and ownership queries.

### R8｜Global acceptance
- Run global graph, source, claim, retrieval and manifest validation.
- Produce reconciliation report and final global package.

## Required reconciliation outputs
- `reconciliation/child_inventory.csv`
- `reconciliation/global_ownership_registry.csv`
- `reconciliation/duplicate_node_decisions.csv`
- `reconciliation/source_merge_registry.csv`
- `reconciliation/evidence_family_merge_registry.csv`
- `reconciliation/claim_conflict_matrix.csv`
- `reconciliation/id_migration_log.csv`
- `reconciliation/cross_link_report.md`
- `reconciliation/global_retrieval_results.json`
- `reconciliation/global_acceptance.md`
- final merged ZIP
