# Section 04: Schema Versioning per Tenant

Schema versioning tracks which database schema version each tenant is running, enabling gradual migrations across a fleet of tenants. Different tenants can be at different schema versions simultaneously, allowing canary deployments and rollback without affecting all tenants. This is critical for schema-per-tenant and database-per-tenant models.

Schema version management: each schema change is versioned (migration files numbered sequentially), tenant records track current schema version, migrations are applied per-tenant when they are active, rollbacks revert to previous version for specific tenants. The migration runner applies pending versions automatically.

Version metadata stored: tenant_id, current_version, applied_versions (JSON array of version+timestamp), migration_status (pending, applying, applied, failed), last_migration_at. The dashboard shows schema version distribution across all tenants and allows targeting specific tenants for upgrade.
