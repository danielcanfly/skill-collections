# v7 to v8 Migration

v8 preserves v7 candidates as immutable inputs but does not grandfather them into production. A v7 candidate must be migrated to the v8 schemas, re-sealed, admitted by exact SHA, externally reviewed with Audit OS v4, and promoted through the production-release module.

New blocking requirements include complete source-passage coverage, source identity/temporal completeness, zero open P0/P1/P2, portable byte-identical reproduction, clean production/R2 surfaces, operational node depth, and an audited production wrapper.
