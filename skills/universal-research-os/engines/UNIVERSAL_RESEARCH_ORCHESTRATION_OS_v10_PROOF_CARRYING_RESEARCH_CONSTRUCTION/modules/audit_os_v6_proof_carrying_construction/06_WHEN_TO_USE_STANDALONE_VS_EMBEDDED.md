# Embedded vs Standalone Audit OS

Use the embedded module when the auditor also needs access to shared schemas, migration rules, repair generation, or global reconciliation.

Use the standalone export when an independent session should receive only audit capability and must not see or execute dispatcher or repair tooling.

Both artifacts are generated from the same canonical source. Never manually edit the standalone ZIP; rebuild it from `modules/audit_os_v6_proof_carrying_construction/`.
