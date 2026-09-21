# V9 Agent Usage Recipes

## New research domain

Use Dispatcher to generate v9 handoffs. Register each exact ZIP SHA. Never adapt an old handoff by renaming it.

## Candidate returned

Run admission first. A rejected or legacy candidate must not enter semantic audit without an explicit migration decision.

## Independent audit

Create the review workspace outside the candidate. Review all governed populations, finalise the receipt, then run Audit OS v5. Treat `AUDIT_OUTPUT/manifest.json` as authoritative.

## Production promotion

Pass the complete audit output directory or deterministic audit ZIP to promotion. A copied `AUDIT_SUMMARY.json` alone is forbidden.

## Wrapper verification

Always run the production-wrapper validator after promotion. It deliberately distrusts the production receipt and recomputes the trust chain.

## Global release

Build all five surfaces with one v9 identity. Generate each manifest last. Run G8 and keep the live pointer unchanged until separately authorised.
