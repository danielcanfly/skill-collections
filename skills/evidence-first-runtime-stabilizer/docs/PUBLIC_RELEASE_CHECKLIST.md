# Public release checklist

- `python -m unittest discover -s tests -v` passes.
- shell scripts pass `bash -n`.
- `python -m compileall src scripts tests` passes.
- no `__pycache__`, `*.pyc`, `.DS_Store`, `.env`, raw evidence, credentials, or private identifiers.
- redaction test passes.
- secret leak fixture is detected.
- PASS soak fixture passes; restart/OOM fixture fails.
- package installs with `pip install -e .`.
- `runtime-stabilizer --version` matches release.
- README/support matrix/changelog updated.
