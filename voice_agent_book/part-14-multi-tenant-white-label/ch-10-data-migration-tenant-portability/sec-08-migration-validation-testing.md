# Section 08: Migration Validation & Testing

Migration validation ensures that data integrity is preserved throughout the migration process. Automated tests run before, during, and after migration to verify completeness, consistency, and correctness. Validation prevents data loss and reduces the risk of post-migration issues.

Validation phases: pre-migration (source data integrity checks: row counts, checksums, referential integrity), in-progress (replication status, lag metrics, error rate), post-migration (target data verification: compare row counts, checksum sample records, validate foreign keys, run application smoke tests). Any validation failure pauses the migration and triggers rollback.

Validation tooling: diff engines compare source and target databases (row-by-row for critical tables, sampling for large tables), integrity checkers verify foreign key relationships and required fields, application smoke tests execute tenant-specific test scenarios, and performance benchmarks compare query response times before and after migration. Reports are generated for audit compliance.
