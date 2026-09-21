# Universal Topic-to-Textbook Skill v2.1.1

> A domain-agnostic autonomous research-to-textbook skill. Give it a topic, curriculum, source pack, or teaching transcript; it can research, structure, teach, reconstruct, validate, and publish a textbook-quality artifact.

**License:** Apache License 2.0. See `LICENSE`.

從「只有一個主題」一路自主研究、設計課程、逐課完整施工、第二次重編成書，再做 evidence / executable / pedagogy / assessment / publication QA 的通用教材 Skill。

## 最簡單用法

你可以只說：

- `幫我做一份 Working Capital 教材。`
- `研究 Agent Evaluation，做成零基礎到 PM 可用的教材。`
- `幫我把 Kubernetes Networking 做成完整教材。`
- `把這個 handoff 做成教材。`
- `把這幾個上課 session 重編成正式教材。`
- `把這本舊教材更新到目前版本，只重驗受影響的章節。`

Topic-only 模式會走：

`scope → landscape/triangulation → primary/gap/challenge research → evidence/freeze → knowledge architecture → curriculum → lesson manuscripts → reconstruction → claim-drift/executable/pedagogy/assessment/publication QA → cold review`

不需要使用者先準備 curriculum，也不需要一路手動按「接下一課」。

## v2.1 hardening

v2.1 在 v2.0 之上新增：

- durable `RUN_STATE` 與跨 session checkpoint
- stable IDs for source / claim / concept / objective / lesson / assessment / defect
- curriculum triangulation，避免自主課綱漏掉公認核心模組
- CRITICAL / MAJOR / SUPPORTING claim criticality
- Research Freeze Manifest，記錄版本／日期／commit／locator
- untrusted-source / prompt-injection 防護
- executable validation：code / SQL / formula / lab / dry-run
- post-reconstruction claim drift audit
- refresh / revision impact analysis
- Science / Engineering 與 Legal / Regulation / Policy adapters
- qualification 改為 evidence-based，不再把「規格存在」當作 live quality PASS

## Lesson-first two-pass construction

保留最重要的兩段式製程：

**每課先充分展開 → 全部 lesson 完成後再第二次重編成正式教材。**

詳細不等於重複；簡潔不等於刪知識。


## Public use

This package is designed to be portable across compatible agent runtimes. Keep the folder intact so `SKILL.md`, `references/`, `templates/`, `schemas/`, and validators remain available together.

Typical entry prompts:

- `Research <topic> broadly and turn it into a beginner-friendly textbook.`
- `Use this source pack as the authoritative basis and expand it into a textbook.`
- `Rebuild these teaching transcripts into a clean textbook without losing unique knowledge.`
- `Refresh this existing textbook against current sources and revalidate affected chapters only.`

The package does not claim identical behavior across every host. Run the included host smoke prompts after installation when runtime-level qualification matters.

## Package structure

- `SKILL.md`：核心 routing、硬規則、gate sequence、Definition of Done
- `references/`：研究、證據、教學法、domain adapters、state、安全、執行驗證、refresh、QA
- `templates/`：可稽核工作產物
- `schemas/`：run state / freeze machine-readable contracts
- `examples/`：routing 與 domain examples
- `qualification/`：contract fixtures、qualification report、live test matrix
- `scripts/`：package / behavioral-contract / public-release validators

## Qualification language

- `DESIGN_QUALIFIED`：規格、模板、validator、fixtures 完整。
- `RUNTIME_SMOKE_QUALIFIED`：已在特定 host/runtime 實際跑 smoke tests。
- `PUBLIC_READY`：除 runtime smoke 外，必要的 artifact/read-back、claim/execution validation 與 unresolved critical defect gate 均通過。

Package 自己不得把尚未執行的 host-specific smoke test寫成 PASS。
