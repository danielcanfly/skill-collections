# Evidence Binding Guide

## Atomicity

每一列 binding 只能表達：

`一個 claim × 一個 source × 一個 concept × 一種 relation × 一個 scope`

若 source 同時支持兩個不同 scope，拆成兩列。

## Direct support 判定

必須同時成立：

1. source identity 已確認；
2. claim proposition 可在 source 中被明確支持；
3. support scope 不超過 source 實際內容；
4. evidence boundary 已記錄；
5. 沒有把作者推論當成 source 原話。

## Bounded synthesis

適用於：

- 多個 sources 合併後才形成的工作性結論；
- Knowledge OS 的治理規範；
- 將方法移植到新 domain 的適用性判斷；
- 沒有單一來源直接說出完整 proposition。

Bounded synthesis 不是缺陷遮罩。它必須列出 contributing sources、推論步驟與限制。

## Locator hierarchy

1. `EXACT_QUOTE`
2. `PAGE_PARAGRAPH`
3. `SECTION_HEADING`
4. `DOCUMENT_LEVEL`
5. `PACKAGE_LINEAGE`
6. `NONE`

Locator 越弱，claim status與confidence 不得越強。
