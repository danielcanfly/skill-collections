# Migration v4 → v5

1. Rename `research/provenance_edge_entailment.csv` to `research/edge_entailment.csv` and add v2.1 columns.
2. Replace `qa/SEAL_STATE.json` with `qa/seal_state.json`.
3. Expand manual audit receipt and enforce per-row completion.
4. Add temporal status, exact metadata locator and reviewer status to every source identity row.
5. Add evidence boundary and passage type to every edge.
6. Rebuild lineage register and evidence-family independence dimensions.
7. Re-run finalizer using two-stage fresh extraction.
