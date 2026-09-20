# Privacy and evidence sharing

Raw incident evidence is private by default.

Redaction is best-effort, not proof that arbitrary binary artifacts are safe.

The shareable pipeline is:

1. copy textual evidence through the redactor;
2. run secret scan;
3. exclude or manually review binary artifacts;
4. human review;
5. publish the redacted bundle only.
