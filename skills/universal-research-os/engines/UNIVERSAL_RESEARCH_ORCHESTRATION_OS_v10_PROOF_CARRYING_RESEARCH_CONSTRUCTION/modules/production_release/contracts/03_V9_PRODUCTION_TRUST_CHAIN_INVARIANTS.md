# V10 Production Trust-Chain Invariants

1. Promotion accepts only a strict manifest-governed Audit OS v6 output.
2. The audit package must contain the exact admission and external independent-review artifacts it evaluated.
3. Candidate, admission, review, audit summary, audit identity and production receipt SHA bindings must agree.
4. Six dimensions are required by exact key equality, not “all provided values”.
5. The production wrapper validator distrusts and recomputes every embedded claim.
6. Rebuilding a manifest after tampering does not restore trust because cross-artifact bindings are rechecked.
7. Production promotion never updates a live pointer.
