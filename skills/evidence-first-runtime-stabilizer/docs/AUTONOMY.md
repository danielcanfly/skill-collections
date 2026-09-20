# Autonomy contract

`runtime-stabilizer run-until-blocked` performs safe mechanical phases continuously and stops at explicit blockers, failures, or completion. `run-next` executes one phase only.

Expected reasoning gates:
- P3 root-cause adjudication;
- P6 application repair/candidate creation.

Expected authorization gate:
- P9 deploy.

Expected environment hooks:
- rollback snapshot;
- regression;
- resource qualification;
- deploy;
- production probe;
- rollback;
- optional authority snapshot.

The state file is the resume contract. A later AI/session should inspect it and continue from the first non-PASS phase rather than replaying completed mutation or cleanup phases.

This is deliberate. A public tool that silently invents application authority, code repairs, or production mutation permissions is unsafe.

Transient blockers can be re-armed with `runtime-stabilizer retry-blocked --incident <dir>` after the missing authorization/capability is supplied. This resets only the current `BLOCKED` phase to `PENDING`; it never resets a `FAIL`.
