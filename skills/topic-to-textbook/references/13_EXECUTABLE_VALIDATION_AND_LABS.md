# Executable Validation & Labs

## Principle

If an educational artifact makes an executable or calculable claim, validate it when practical and safe. “Looks plausible” is not enough.

## Validation classes

### EXECUTED
Actually run in a controlled environment and observed expected behavior.

### RECALCULATED
Formula / numerical example independently recomputed.

### DRY_RUN_VALIDATED
Syntax / plan / request structure validated without consequential execution.

### SOURCE_VALIDATED
Cannot be executed here, but verified against authoritative documentation / specification.

### UNEXECUTED
Execution was possible in principle but not performed. Do not imply otherwise.

### NOT_RUNTIME_VALIDATED
Environment cannot reproduce the target runtime or external dependency.

## Code / SQL / shell

When safe and useful:

- run minimal examples
- capture environment / version
- verify expected output
- test error path if the lesson teaches troubleshooting
- avoid destructive commands
- use sample/synthetic data

## APIs / cloud / external systems

Prefer:

- schema validation
- mock / dry run
- official examples
- non-mutating endpoints

Do not invent credentials. Do not perform consequential actions merely to validate a textbook example.

## Quantitative examples

Recompute:

- arithmetic
- formulas
- percentages
- unit conversions
- accounting reconciliations
- statistics
- denominators
- rounding

Record assumptions explicitly.

## Labs

Every hands-on lab should define:

- objective
- prerequisites
- environment / version
- input
- steps
- expected observable output
- success criteria
- common failure modes
- safe cleanup / rollback when relevant
- validation status

A lab is not validated merely because commands are syntactically plausible.

## Release rule

Any CRITICAL executable claim that is `UNEXECUTED` or `NOT_RUNTIME_VALIDATED` must be explicitly qualified in the textbook / handoff and in final qualification.
