# Quickstart

```bash
python3 -m pip install -e .
runtime-stabilizer --version
runtime-stabilizer init --config config/runtime-stabilizer.example.toml --root ./incidents --id demo
runtime-stabilizer run-until-blocked --incident ./incidents/demo
```

The example config uses the custom adapter and safe example hooks. For real incidents, start with read-only collection and capability discovery. Do not enable deployment gates until rollback and probe hooks are proven.
