# G6 — Graph and Markdown-Link Compilation


## Mission
從 G2～G5 canonical registries 編譯 active graph、compiled Markdown、ordinary links、backlinks、indexes、aliases。

## Node classes
concept / claim / source / evidence-family / case / case-assertion。

## Edge rules
- provenance 和 ownership 使用已裁決的強類型；
- 未裁決的 `related` 預設保守 `contextualises`；
- merge-induced self-loop 移除且 audit；
- alias 不進 active graph。

## Markdown
- YAML 可解析；
- active path identity 正確；
- ordinary Markdown links；
- citations 可解析；
- alias redirect pages 分離。

## Hard gate
零 broken endpoints/links、unknown types、duplicate edge keys、active orphan；結構性 DAG 類關係零 cycle；deterministic rebuild。

## Forbidden
- graph 成為 source of truth；Markdown 才是 durable source
- 舊 ID 混入 active graph
- 將所有 related 猜成強關係
