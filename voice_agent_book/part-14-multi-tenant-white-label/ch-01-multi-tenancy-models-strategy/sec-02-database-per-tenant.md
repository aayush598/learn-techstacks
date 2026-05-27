# Section 02: Database-per-Tenant Strategy

## Overview

Database-per-tenant is the highest-isolation multi-tenancy model, where each customer receives a completely separate database instance or schema. This architecture provides the strongest data isolation guarantees, making it the preferred choice for healthcare (HIPAA), financial services (PCI DSS), and enterprise customers with strict compliance requirements. Each tenant's data resides in its own database, eliminating the risk of cross-tenant data leakage through application bugs, SQL injection, or RLS policy misconfiguration.

However, this isolation comes at a cost. Operational complexity increases significantly as the tenant base grows. Every tenant database must be provisioned, backed up, monitored, migrated, and optimized independently. Connection management becomes a challenge—thousands of tenants could mean millions of database connections if not managed properly. Schema changes must be rolled out across all tenant databases in a coordinated fashion, and aggregate reporting requires cross-database queries or a separate analytics data store.

For a voice agent platform, database-per-tenant provides benefits beyond security. Each tenant can have independent database configuration (e.g., different PostgreSQL versions, extensions, or parameter tuning). Tenants with high call volumes won't experience performance degradation from noisy neighbors. Backup and restore operations can be performed per-tenant, enabling precise recovery point objectives for individual customers.

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
class DatabasePerTenantManager {
  private pools: Map<string, Pool> = new Map();
  private connectionStringTemplate: string;

  async provisionTenantDatabase(tenant: Tenant): Promise<void> {
    const dbName = `voiceagent_${tenant.id}`;
    const host = this.selectHost(tenant.tier);
    
    const adminPool = new Pool({ connectionString: this.adminConnString });
    
    try {
      await adminPool.query(`CREATE DATABASE "${dbName}"`);
      await adminPool.query(`CREATE USER "${tenant.id}" WITH PASSWORD '${this.generatePassword()}'`);
      await adminPool.query(`GRANT ALL PRIVILEGES ON DATABASE "${dbName}" TO "${tenant.id}"`);
      
      const tenantPool = new Pool({ connectionString: `postgres://${tenant.id}:***@${host}/${dbName}` });
      await this.runBaselineMigrations(tenantPool);
      await this.seedDefaultConfiguration(tenantPool);
      
      this.pools.set(tenant.id, tenantPool);
    } finally {
      await adminPool.end();
    }
  }

  async getConnection(tenantId: string): Promise<Pool> {
    let pool = this.pools.get(tenantId);
    if (!pool) {
      pool = await this.connectToExisting(tenantId);
      this.pools.set(tenantId, pool);
    }
    return pool;
  }

  async runMigrationForAllTenants(migration: Migration): Promise<void> {
    const tenants = await this.listAllTenants();
    const results = [];
    
    for (const tenant of tenants) {
      try {
        const pool = await this.getConnection(tenant.id);
        await this.applyMigration(pool, migration);
        results.push({ tenant: tenant.id, status: 'success' });
      } catch (error) {
        results.push({ tenant: tenant.id, status: 'failed', error });
        // Send alert for failed migration
        await this.alertService.send({
          type: 'migration_failed',
          tenantId: tenant.id,
          migration: migration.name,
        });
      }
    }
    
    return results;
  }

  private async backupDatabase(tenantId: string): Promise<string> {
    const timestamp = Date.now();
    const bucketPath = `s3://voiceagent-backups/${tenantId}/${timestamp}/`;
    // Execute pg_dump via database service
    await exec(`pg_dump -Fc ${this.getConnString(tenantId)} | aws s3 cp - ${bucketPath}dump.pgdump`);
    return bucketPath;
  }
}
```

## Integration Points

- **Tenant Provisioning (Ch 03):** Database provisioning is the first step of the tenant creation pipeline
- **Data Migration (Ch 10):** Export/import operations work at the database level
- **Backup Service:** Per-tenant backup scheduling integrates with the infrastructure automation
- **Read Replicas:** Each tenant database needs its own read replicas for analytics queries
- **Monitoring:** Per-tenant database metrics (connections, CPU, IOPS) feed into the tenant dashboard

## Open-Source Tools

- **ws** (MIT): WebSocket
- **MediaRecorder API**: Recording
- **Opus** (BSD): Audio codec
## Production Considerations

- **Connection Scaling:** Each application instance should limit idle connections. Use PgBouncer in transaction mode to handle thousands of tenants with a small connection pool.
- **Warm vs Cold Databases:** Not all tenants are active simultaneously. Implement lazy connection establishment—first request triggers connection pool creation. Consider hibernating idle tenant databases.
- **Backup Window Staggering:** Avoid backing up all tenant databases simultaneously. Stagger backup schedules to prevent I/O spikes on shared storage.
- **Schema Version Tracking:** Maintain a `schema_migrations` table in each tenant database. Add a central `tenant_registry` table in the admin database to track which migration version each tenant is on.
- **Cost Attribution:** Tag each database resource with tenant ID for cost allocation. Use AWS resource tagging or GCP labels to map infrastructure costs to tenants.
- **Migration Phasing:** Never roll out migrations to all tenants simultaneously. Use a phased approach: internal tenants → beta tenants → all tenants, with monitoring gates between phases.
- **Disaster Recovery:** Per-tenant RTO/RPO documents must be maintained. Practice tenant-specific restore procedures regularly.
