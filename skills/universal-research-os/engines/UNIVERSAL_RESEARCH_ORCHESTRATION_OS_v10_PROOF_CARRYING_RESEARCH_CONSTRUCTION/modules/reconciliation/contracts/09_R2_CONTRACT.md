# R2 Production Contract

R2 is a data-only immutable release surface.

## Hard requirements

- per-object SHA-256, MIME, release ID and immutable key;
- unique safe relative object keys;
- deterministic object plan generated from the same canonical lineage as KOS and OKF;
- two-phase pointer candidate and explicit rollback pointer;
- dry-run by default and no overwrite of immutable objects;
- exact exclusion of `tests`, `fixtures`, `qa`, `audit`, synthetic candidates, provisional output, cache files, bytecode, temporary files and platform metadata;
- `validate_production_surface_hygiene.py` and the G8 production release gate must PASS.

Live pointer update is never part of build or audit.
