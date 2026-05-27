# Section 02: Import Tenant Data

Data import allows tenants to migrate data from another platform or restore from a previous export. The import system accepts the same formats as export (JSON, CSV, ZIP archives) and validates data before committing. Import can be a full restore or selective merge of specific data types.

Import flow: upload archive (via dashboard or API, chunked upload for large files) → validation (schema checking, cross-reference consistency, duplicate detection) → preview (show what will be imported, allow conflict resolution) → import execution (async worker processes in order: configs first, then data) → verification (count records, test agent functionality) → notification (import complete or error).

Import supports conflict resolution strategies: skip (keep existing), overwrite (replace with imported), merge (combine fields), and create-new (import as copy). The system logs all import actions for audit. Rollback capability allows reverting an import if issues are detected.
