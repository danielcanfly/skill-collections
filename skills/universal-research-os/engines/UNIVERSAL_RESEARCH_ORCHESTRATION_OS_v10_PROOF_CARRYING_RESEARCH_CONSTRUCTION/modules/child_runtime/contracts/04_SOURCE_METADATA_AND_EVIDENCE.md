# Universal Source Metadata and Evidence Contract v10

Every active source requires a production-eligible identity row with:

- verified title;
- named author or verified responsible organisation;
- explicit author basis;
- canonical identifier or URL;
- publication and/or effective-period date plus accessed timestamp;
- exact metadata locator and excerpt;
- access level and verification method;
- identity, temporal, reviewer and production-eligibility PASS.

Every active claim-source edge requires one immutable source-passage row with a real excerpt, typed resolvable locator, capture method, snapshot path and hashes. `source-note`, package summary, abstract-only metadata and synthetic locator language are not evidence passages. Direct support requires an original-source snapshot and full or section-level access.

No unresolved source-refresh row may remain open in a production release.
