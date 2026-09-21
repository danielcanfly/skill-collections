# Universal Semantic Provenance Contract

## Claim ledger
Use one atomic row per claim-source-node relation.

```csv
claim_id,module_id,claim,claim_type,source_id,evidence_family_id,support_challenge,scope,confidence,candidate_node,notes
```

## Claim IDs
- `C001`, `C002A`, `C002B`
- Splits/renames require a migration record.
- Claim text/type/confidence must be consistent across rows sharing an ID.

## Support values
- `support`: directly supports the whole claim as written
- `partial-support`: directly supports a named subset
- `contextual-support`: provides relevant context, history, governance or method
- `challenge`: criticises definition, mechanism, evidence strength, scope or applicability

## Canonical synthesis
Use `claim_type: canonical synthesis` when a conclusion is composed across sources.

Requirements:
- each source row states its specific contribution
- no generic scope such as “supports node”
- gaps and unsupported clauses are visible
- confidence reflects independent evidence families and transfer limits

## Source-note sections
Every production source note contains:

```markdown
## Source-specific Findings
## Claims Supported
## Contextual or Partial Contributions
## What This Source Does Not Establish
## Caveats and Transfer Limits
## Concepts Updated
```

## Bidirectional semantic lineage
For each node-source relation:
1. node frontmatter contains source ID
2. source note lists full node ID
3. claim ledger has claim-source-node row
4. source note lists claim ID
5. source content genuinely supports the indicated support level
