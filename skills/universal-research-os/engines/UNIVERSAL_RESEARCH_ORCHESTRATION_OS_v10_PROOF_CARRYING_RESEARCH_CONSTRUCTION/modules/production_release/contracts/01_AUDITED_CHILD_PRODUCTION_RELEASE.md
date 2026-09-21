# Audited Child Production Release Contract

A child builder may emit only a sealed candidate. Production status is granted only by orchestration after all of the following bind to the exact candidate SHA-256:

1. V10 native admission PASS.
2. External Audit OS v6 independent review.
3. All five dimensions equal 100.
4. Open P0, P1 and P2 equal zero.
5. Candidate fresh-extraction and deterministic reproduction PASS.
6. Promotion creates a wrapper containing the exact immutable candidate ZIP, independent audit surface, admission receipt, production release receipt, identity surface, strict manifest and detached checksums.

The wrapper lifecycle is `AUDITED_PRODUCTION_RELEASE`. A filename containing `PRODUCTION_RELEASE` without this receipt is invalid.
