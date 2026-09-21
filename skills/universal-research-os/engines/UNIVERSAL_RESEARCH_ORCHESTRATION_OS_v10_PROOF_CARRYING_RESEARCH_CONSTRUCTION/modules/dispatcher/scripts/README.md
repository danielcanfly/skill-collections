# Dispatcher Scripts

`validate_child_handoff.py` is the authoritative package validator. `validate_generated_collection.py` must call it for every ZIP and reject the whole collection if any child fails.
