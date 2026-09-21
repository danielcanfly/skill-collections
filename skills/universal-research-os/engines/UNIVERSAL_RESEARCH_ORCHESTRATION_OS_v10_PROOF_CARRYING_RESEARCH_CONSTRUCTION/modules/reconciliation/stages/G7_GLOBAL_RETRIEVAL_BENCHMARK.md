# G7 — Global Retrieval Benchmark


## Mission
針對 reconciled canonical corpus 建立全新的 global benchmark，不串接 phase-local tests。

## Reference Strict composition
240 tests，12 類各 20：definition、comparison、how-to、decision/application、source-provenance、case-provenance、audit、multi-hop、cross-phase、adversarial、negative-neighbour、bilingual-paraphrase。

## Split
- holdout ≥30%，建立後 freeze；
- negative-ID tests ≥40%；
- mandatory overlap groups 全覆蓋；
- Top 10 cutoff。

## Pass rule
每題所有 expected IDs 進 Top 10，所有 declared negative IDs 不進 Top 10。

## Integrity
- retriever 不得讀 expected IDs 做 ranking；
- 失敗不能靠刪 expected/negative 來修；
- 保留 title-only baseline；
- 失敗修復要有 failure-driven log。

## Hard gate
240/240，holdout 100%，negative tests 100%，unresolved failures=0，deterministic results。
