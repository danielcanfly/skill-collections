# G0 — Immutable Intake and Preflight

G0 accepts only child ZIPs whose outer wrapper validates as `AUDITED_PRODUCTION_RELEASE`.

For every child:

1. Verify outer ZIP CRC, single root, manifest and checksum.
2. Verify `PRODUCTION_RELEASE_RECEIPT.json`, five-dimensional 100/100 and zero P0/P1/P2.
3. Verify the single nested candidate ZIP SHA equals the receipt.
4. Preserve both wrapper SHA and candidate SHA in the global identity registry.
5. Extract the nested candidate into an isolated immutable intake area.
6. Reject candidate-only, filename-only, stale, superseded or unregistered artifacts.

No semantic merge begins until all children pass G0.
