# Global Admission of Child Releases

G0 may admit only `AUDITED_PRODUCTION_RELEASE` wrappers validated by `validate_child_production_release.py`. The canonical child payload is the single ZIP under `payload/`; its SHA must equal `PRODUCTION_RELEASE_RECEIPT.json.candidate_sha256`. Global reconciliation must preserve the wrapper and payload hashes in the global lineage registry.
