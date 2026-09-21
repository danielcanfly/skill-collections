# Qualification Test Matrix v2.1.1

| ID | Surface | Test | Evidence | Expected |
|---|---|---|---|---|
| Q01 | Package | Required files nonempty | `validate_package.py` | PASS |
| Q02 | Legacy | v1 checksum preserved | SHA-256 | PASS |
| Q03 | Legacy | v2.0 core checksum preserved | SHA-256 | PASS |
| Q04 | Core size | orchestration core <= 450 lines | validator | PASS |
| Q05 | Routing | Topic-only fixture | fixture validator | PASS |
| Q06 | Routing | Source-grounded fixture | fixture validator | PASS |
| Q07 | Routing | Refresh fixture | fixture validator | PASS |
| Q08 | Domain | Finance adapter | fixture validator | PASS |
| Q09 | Domain | Infra adapter | fixture validator | PASS |
| Q10 | Domain | Agent adapter | fixture validator | PASS |
| Q11 | Research | curriculum triangulation contract | protocol invariant | PASS |
| Q12 | Evidence | claim criticality | protocol invariant | PASS |
| Q13 | Evidence | research freeze | schema/template/protocol | PASS |
| Q14 | Safety | untrusted-source/prompt-injection boundary | protocol invariant | PASS |
| Q15 | Rights | copyright/licensing guard | protocol invariant | PASS |
| Q16 | Execution | validation status classes | protocol invariant | PASS |
| Q17 | Editing | post-reconstruction claim drift | core + QA | PASS |
| Q18 | Revision | impact graph/no blind rebuild | protocol + fixture | PASS |
| Q19 | Schema | RUN_STATE JSON contract parses | validator | PASS |
| Q20 | Schema | freeze JSON contract parses | validator | PASS |
| Q21 | Live smoke | Kubernetes current/version-sensitive case | bounded live report | PASS |
| Q22 | Live smoke | Working Capital recalculation | bounded live report | PASS |
| Q23 | Live smoke | Agent Evaluation volatile/deprecation case | bounded live report | PASS |
| Q24 | Host runtime | installed skill trigger / long run / cold reviewer | intended-host live execution | NOT TESTED |

A `NOT TESTED` host-specific row cannot be converted to PASS by static inspection.
