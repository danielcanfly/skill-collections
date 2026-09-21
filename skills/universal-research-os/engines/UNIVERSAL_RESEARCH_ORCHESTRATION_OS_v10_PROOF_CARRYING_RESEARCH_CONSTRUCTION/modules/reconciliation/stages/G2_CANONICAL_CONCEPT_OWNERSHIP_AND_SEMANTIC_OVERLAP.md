# G2 — Canonical Concept Ownership and Semantic Overlap


## Mission
對所有 concept/title/alias overlap 進行語義裁決，建立唯一 ownership 與可逆 migration。

## Candidate generation
- exact normalized title
- alias collision
- token/character similarity
- shared definitions/sections
- same pattern/checklist name
- cross-phase links

## Decisions
KEEP / MERGE / DISTINGUISH / MOVE / ALIAS / DEPRECATE / LINK_AS_APPLICATION。

## Required reasoning
- canonical owner
- semantic equivalence
- application relation
- preserved clauses
- old/new path
- title/alias hygiene

## Hard gate
所有 G1 nodes 都有 resolution；owner 唯一；MERGE/MOVE 可逆；active title+alias namespace 零碰撞；無 unresolved mandatory groups。

## Forbidden
- 只憑名稱自動 merge
- 合併後遺失 phase-specific clauses
- 修改 source/claim/case identities
