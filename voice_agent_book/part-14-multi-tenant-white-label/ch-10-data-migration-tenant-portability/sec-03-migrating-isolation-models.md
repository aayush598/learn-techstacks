# Section 03: Migrating Between Isolation Models

Tenants may need to migrate between isolation models as they grow: from shared+RLS to schema-per-tenant or from schema-per-tenant to database-per-tenant. The migration process must move data without downtime and ensure all references are preserved. A tenant typically starts in shared+RLS and migrates to higher isolation when they need dedicated resources or have compliance requirements.

Migration paths: shared→schema (copy tenant's rows to dedicated schema, update connection routing), schema→database (move schema to new database, update connection string), shared→database (direct migration from shared tables to dedicated database). Each path has a specific data movement strategy.

The migration orchestrator: create target (schema or database), lock tenant (read-only mode), verify source data integrity, transfer data with transformations, verify target data integrity, update routing configuration, run integration tests, unlock tenant. Rollback plan: keep source available for 30 days, revert routing if issues detected.
