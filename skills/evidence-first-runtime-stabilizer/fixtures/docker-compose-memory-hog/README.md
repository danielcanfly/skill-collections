# Docker Compose Memory Hog Fixture

This fixture documents the shape of an integration test service that allocates memory and exposes `/health`. It is intentionally not auto-run by CI because many CI runners do not allow swap/cgroup manipulation.

Use it for local adapter rehearsals before trusting deployment automation.
