# Section 03: Schema-per-Tenant Strategy

## Overview

Schema-per-tenant offers a middle ground between database-per-tenant isolation and shared-tenant operational efficiency. In this model, a single PostgreSQL database hosts multiple tenants, but each tenant's data resides in a separate database schema. PostgreSQL schemas provide namespace isolation—tables, views, functions, and sequences are scoped to a schema—preventing direct cross-tenant access while sharing the same database server, connection pool, and backup infrastructure.

The schema-per-tenant model is particularly well-suited for mid-market voice agent customers who need stronger isolation than a shared model provides but don't require the full compliance guarantees of a dedicated database. It offers better resource utilization than database-per-tenant (database connections are shared, buffer cache is shared) while providing logical data separation that can be audited and enforced.

Operationally, schema-per-tenant simplifies several management tasks compared to database-per-tenant. A single database backup covers all tenants (though selective restore is more complex). Schema migrations can be applied with a single `ALTER` statement that iterates over tenant schemas. Connection pooling is simpler since all connections go to the same database. However, tenants are still subject to the noisy neighbor problem—a resource-intensive query from one tenant can impact others in the same database.

## Architecture

```
+----------+    +----------+    +----------+    +----------+    +----------+
| Audio    |--->| WebSocket|--->| Jitter   |--->| PLC      |--->| Player   |
| Producer |    | (WSS)    |    | Buffer   |    | (Packet  |    | (smooth  |
| (100ms   |    | (binary) |    | (adaptive|    |  Loss    |    |  output) |
|  chunks) |    |          |    |  60-200) |    |  Conceal)|    +----------+
+----------+    +----------+    +----------+    +----------+
```


## Design Decisions

- **Provider Abstraction**: All STT providers implement a common interface. Enables seamless failover (Deepgram -> Whisper -> Web Speech API) without code changes.
- **VAD Gating**: Reduces STT costs by 40-60% by not billing silence. VAD miss rate must be <1%.
- **Audio Normalization**: 16kHz mono PCM via Kaiser-window resampling ensures consistent quality across diverse input codecs.
## Implementation Approach

```typescript
class SchemaPerTenantManager {
  private pool: Pool;

  async createTenantSchema(tenant: Tenant): Promise<void> {
    const schemaName = this.schemaName(tenant.id);
    
    await this.pool.query(`CREATE SCHEMA IF NOT EXISTS "${schemaName}"`);
    await this.pool.query(`GRANT USAGE ON SCHEMA "${schemaName}" TO "${this.appRole}"`);
    await this.pool.query(`GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA "${schemaName}" TO "${this.appRole}"`);
    
    // Set search_path to the tenant schema and run migrations
    await this.pool.query(`SET search_path TO "${schemaName}", public`);
    await this.runMigrations(schemaName);
    
    // Register in tenant registry
    await this.pool.query(
      `INSERT INTO admin.tenant_registry (id, schema_name, created_at) VALUES ($1, $2, NOW())`,
      [tenant.id, schemaName]
    );
  }

  async withTenantContext<T>(
    tenantId: string,
    fn: (searchPath: string) => Promise<T>
  ): Promise<T> {
    const schemaName = this.schemaName(tenantId);
    // Using connection from pool; set search_path for this transaction
    return this.pool.transaction(async (client) => {
      await client.query(`SET LOCAL search_path TO "${schemaName}", public`);
      return fn(`"${schemaName}"`);
    });
  }

  private schemaName(tenantId: string): string {
    // Deterministic, reversible mapping from tenant ID to schema name
    const shortHash = tenantId.replace(/-/g, '').slice(0, 12);
    return `tenant_${shortHash}`;
  }

  async runMigrationAcrossAllTenants(migration: Migration): Promise<void> {
    const tenantSchemas = await this.pool.query(
      'SELECT schema_name FROM admin.tenant_registry WHERE status = \'active\''
    );
    
    for (const { schema_name } of tenantSchemas.rows) {
      await this.pool.transaction(async (client) => {
        await client.query(`SET LOCAL search_path TO "${schema_name}", public`);
        await migration.up(client);
        await client.query(
          `INSERT INTO "${schema_name}".schema_migrations (name, applied_at) VALUES ($1, NOW())`,
          [migration.name]
        );
      });
    }
  }

  async listTenantTables(tenantId: string): Promise<string[]> {
    const schemaName = this.schemaName(tenantId);
    const result = await this.pool.query(
      `SELECT table_name FROM information_schema.tables 
       WHERE table_schema = $1 AND table_type = 'BASE TABLE'`,
      [schemaName]
    );
    return result.rows.map(r => r.table_name);
  }
}
```

## Integration Points

- **Connection Pooling:** All tenants share the same pool, reducing connection overhead
- **Search Path Middleware:** Each request middleware sets `SET LOCAL search_path` before query execution
- **Backup Strategy:** Single database backup covers all tenants; selective restore requires extracting specific schemas
- **Migration Pipeline:** Single migration script iterates over all tenant schemas
- **Analytics:** Cross-tenant analytics queries use UNION ALL across schemas or feed into a separate analytics database

## Open-Source Tools

- **ws** (MIT): WebSocket
- **MediaRecorder API**: Recording
- **Opus** (BSD): Audio codec
## Production Considerations

- **Schema Count Limits:** PostgreSQL doesn't have a hard limit on schemas, but very high counts (10,000+) can degrade system catalog performance in `information_schema` queries. Monitor query planning times as tenant count scales.
- **search_path Gotchas:** When using PgBouncer in transaction mode, `SET search_path` persists within the transaction. Always use `SET LOCAL` (transaction-scoped) rather than `SET` (session-scoped) to avoid cross-tenant leakage.
- **Connection Pooling:** With hundreds of tenants on the same database, ensure `max_connections` is set appropriately. PgBouncer in transaction mode is recommended.
- **Tenant Schema Enumeration:** Avoid sequential scans of `information_schema` or `pg_namespace` for tenant management. Maintain a tenant registry table in a separate admin schema.
- **Resource Contention:** A single tenant's expensive query can impact shared buffer cache and CPU. Use `pg_stat_statements` to identify noisy neighbors. Consider PostgreSQL resource groups or cgroups for isolation.
- **Migration Safety:** Always run migrations with `SET LOCAL search_path` within a transaction. Test migrations against a copy of the largest tenant schema before production rollout.
- **Schema Size Monitoring:** Track per-schema size with `SELECT pg_size_pretty(pg_total_relation_size(schemaname || '.' || tablename))`. Set alerts when any tenant's data approaches storage limits.
