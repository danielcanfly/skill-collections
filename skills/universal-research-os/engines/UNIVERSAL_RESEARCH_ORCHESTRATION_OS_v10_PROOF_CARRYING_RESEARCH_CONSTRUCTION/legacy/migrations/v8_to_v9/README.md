# V8 to V9 migration

V9 preserves V8 production-release architecture and hardens the trust chain. V8 audit outputs, production wrappers and G8 receipts are not production-admissible without re-verification.

Required changes:

1. Regenerate admission as `V9_NATIVE_ACCEPTED`.
2. Run Audit OS v5 and package its strict manifest-governed output.
3. Re-run clean-output reproduction.
4. Re-promote the candidate with v9 promotion.
5. Re-run strict wrapper validation and the v9 G8 gate.
