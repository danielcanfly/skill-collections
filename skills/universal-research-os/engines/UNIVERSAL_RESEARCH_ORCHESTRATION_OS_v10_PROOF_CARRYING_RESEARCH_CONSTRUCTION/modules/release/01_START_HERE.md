# Release Module

Use after global reconciliation and all independent audits pass. Generate every mutable receipt first. Then set seal state to MANIFEST_FROZEN, generate the manifest last, verify it read-only, build deterministic ZIP, fresh-extract, and rerun the independent audit. Any post-manifest mutation invalidates the release.
