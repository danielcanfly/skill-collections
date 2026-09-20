# Security

Do not attach raw production evidence to public issues.

Treat credentials, cookies, tokens, private keys, database URLs, customer data, and internal topology as secrets. Redaction is a defense-in-depth helper, not a substitute for human review.

## Trust boundary

The local configuration file and configured hook commands are trusted operator-controlled code. Hooks are executed as local shell commands with the current user's privileges. Do not run an incident configuration supplied by an untrusted party without reviewing it first.

Runtime target names are also operator-controlled input and should come from known local infrastructure, not arbitrary external request data.

Binary and non-UTF8 evidence is omitted from automatic redacted bundles. Review it manually before any sharing.

Security-sensitive defects should be reported privately to the repository owner.
