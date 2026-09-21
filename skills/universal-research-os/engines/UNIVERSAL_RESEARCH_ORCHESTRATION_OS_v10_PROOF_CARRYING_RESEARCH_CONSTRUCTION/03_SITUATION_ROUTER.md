# Situation Router

| 情境 | 模組 | 首要動作 |
|---|---|---|
| 新多主題研究 | `dispatcher` + `handoff_compiler` | 生成v10 handoff並完成Gate 0 |
| 子Session研究 | `proof_carrying_construction` | source snapshot → clause pre-review → compile |
| 候選回件 | `control_plane` | admission，不可直接Audit |
| 候選審查 | `audit_os_v6_proof_carrying_construction` | 綁定exact SHA與external review |
| 定點修補 | `repair` + `handoff_compiler` | protected baseline與class-wide closure |
| 舊版遷移 | `legacy_migration` | 凍結legacy SHA並重新admission |
| Global整合 | `global_builder` | 綁定audited production releases，建G0-G7 |
| 正式發行 | `production_release` + `release` | promotion、wrapper、G8、five surfaces |
