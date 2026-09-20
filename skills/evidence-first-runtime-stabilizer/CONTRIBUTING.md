# Contributing

Contributions should preserve evidence-first ordering, explicit uncertainty, and fail-closed semantics.

New adapters must:
- declare capabilities;
- emit JSONL telemetry;
- include synthetic tests;
- never convert unavailable signals into successful zeros.
