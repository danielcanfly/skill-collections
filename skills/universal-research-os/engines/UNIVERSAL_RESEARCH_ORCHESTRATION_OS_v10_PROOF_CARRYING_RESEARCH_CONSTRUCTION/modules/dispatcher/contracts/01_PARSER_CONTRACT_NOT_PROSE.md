# Parser Contract, Not Prose

Any field consumed by a validator must be represented exactly as the parser reads it. Narrative equivalents do not count. Example: `split: holdout` does not replace `is_holdout: true`.
