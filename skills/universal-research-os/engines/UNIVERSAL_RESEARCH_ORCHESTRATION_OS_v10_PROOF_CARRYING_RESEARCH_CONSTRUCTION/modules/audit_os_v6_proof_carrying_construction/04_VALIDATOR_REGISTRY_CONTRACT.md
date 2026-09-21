# Validator Registry Contract

Audit OS executes only validators explicitly listed in `config/validator_registry.json`. Each validator declares read-only mode. The runner hashes the candidate tree before and after every validator. Any mutation is a P1 failure.
