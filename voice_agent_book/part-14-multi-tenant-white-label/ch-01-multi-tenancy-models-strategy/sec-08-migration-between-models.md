# Section 08: Migration Between Tenancy Models

## Overview

As a voice agent platform matures, the need to migrate tenants between isolation models becomes inevitable. A tenant that started on shared infrastructure may outgrow it, require compliance certifications, or negotiate an enterprise contract that demands dedicated resources. Conversely, a tenant that overprovisioned may need to downgrade to a lower isolation level to reduce costs. Migrating between tenancy models with zero downtime and zero data loss is one of the most technically challenging operations in a multi-tenant SaaS.

The migration challenge varies depending on the source and target models. Shared-to-dedicated requires extracting tenant data from shared tables and importing into a new database. Schema-to-schema is the simplest (just copying a schema). Dedicated-to-shared (downgrade) is the most complex, requiring merging isolated data into shared tables while ensuring RLS policies are applied correctly. Each migration path has specific risks: data consistency, foreign key integrity, sequence synchronization, and application availability during cutover.

For a voice agent platform, call records and transcripts are append-only, which simplifies the migration somewhat—there's no need to worry about concurrent updates during migration if we establish a cutover point. However, mutable data like agent configurations and knowledge base articles require more careful synchronization.

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
abstract class TenantMigration {
  abstract sourceType: IsolationTier;
  abstract targetType: IsolationTier;

  async migrate(tenantId: string): Promise<MigrationResult> {
    const tenant = await this.getTenant(tenantId);
    
    // Phase 1: Pre-migration validation
    await this.validateSource(tenant);
    await this.validateTarget(tenant);
    await this.checkDependencies(tenant);
    
    // Phase 2: Provision target
    const targetId = await this.provisionTarget(tenant);
    
    // Phase 3: Data migration
    const migrationId = await this.startDataMigration(tenant, targetId);
    const progress = await this.monitorProgress(migrationId);
    
    // Phase 4: Verification
    await this.verifyDataIntegrity(tenant, targetId, migrationId);
    
    // Phase 5: Cutover
    await this.setSourceReadOnly(tenantId);
    await this.catchUpReplication(tenantId, targetId);
    await this.switchTraffic(tenantId, targetId);
    
    // Phase 6: Cleanup
    await this.decommissionSource(tenantId);
    await this.updateTenantConfig(tenantId, { isolationTier: this.targetType });
    
    return { success: true, targetId, migrationId };
  }

  protected abstract provisionTarget(tenant: Tenant): Promise<string>;
  protected abstract startDataMigration(tenant: Tenant, targetId: string): Promise<string>;
  protected abstract verifyDataIntegrity(tenant: Tenant, targetId: string, migrationId: string): Promise<boolean>;
  protected abstract setSourceReadOnly(tenantId: string): Promise<void>;
  protected abstract switchTraffic(tenantId: string, targetId: string): Promise<void>;
  protected abstract decommissionSource(tenantId: string): Promise<void>;
}

class SharedToDedicatedMigration extends TenantMigration {
  sourceType = 'shared' as IsolationTier;
  targetType = 'dedicated' as IsolationTier;

  async provisionTarget(tenant: Tenant): Promise<string> {
    // Create new dedicated database
    const dbManager = new DatabasePerTenantManager(config);
    await dbManager.provisionTenantDatabase(tenant);
    return tenant.id;
  }

  async startDataMigration(tenant: Tenant, targetId: string): Promise<string> {
    const migrationId = generateId('mig_');
    
    // Export all tenant data from shared tables
    const tables = ['calls', 'transcripts', 'agents', 'campaigns', 'recordings', 'configurations'];
    
    for (const table of tables) {
      const stream = await this.sourcePool.query(
        `SELECT * FROM ${table} WHERE tenant_id = $1`,
        [tenant.id]
      );
      
      // Stream directly to target database
      for (const row of stream.rows) {
        await this.targetPool.query(
          `INSERT INTO ${table} (${Object.keys(row).join(',')}) 
           VALUES (${Object.keys(row).map((_, i) => `$${i + 1}`).join(',')})`,
          Object.values(row)
        );
      }
    }
    
    // Copy sequence values to maintain ID generation
    await this.copySequences(tenant);
    
    return migrationId;
  }

  async setSourceReadOnly(tenantId: string): Promise<void> {
    // Temporarily set tenant to read-only mode
    await this.sourcePool.query(
      `UPDATE tenants SET migration_status = 'readonly' WHERE id = $1`,
      [tenantId]
    );
    
    // Wait for in-flight transactions to complete
    await this.sourcePool.query(`
      SELECT pg_wal_lsn_diff(pg_current_wal_lsn(), 
        replay_lag) < 1024 * 1024 FROM pg_stat_replication
    `);
  }

  async switchTraffic(tenantId: string, targetId: string): Promise<void> {
    // Update the tenant registry to point to new database
    await this.registryPool.query(`
      UPDATE tenant_registry 
      SET connection_string = $1, isolation_tier = 'dedicated', migration_status = 'active'
      WHERE tenant_id = $2
    `, [this.targetConnString, tenantId]);
    
    // Invalidate any cached connections
    await this.cacheService.del(`tenant_config:${tenantId}`);
    
    // Now all new requests will route to the dedicated database
  }

  async decommissionSource(tenantId: string): Promise<void> {
    // Remove tenant data from shared tables after confirming target is healthy
    const tables = ['calls', 'transcripts', 'agents', 'campaigns', 'recordings', 'configurations'];
    
    for (const table of tables) {
      await this.sourcePool.query(
        `DELETE FROM ${table} WHERE tenant_id = $1`,
        [tenantId]
      );
    }
    
    // Update tenant status
    await this.sourcePool.query(
      `UPDATE tenants SET migration_status = 'migrated' WHERE id = $1`,
      [tenantId]
    );
  }
}

// Migration orchestration
class MigrationOrchestrator {
  private migrations: Map<string, TenantMigration>;

  constructor() {
    this.migrations = new Map();
    this.migrations.set('shared->dedicated', new SharedToDedicatedMigration());
    this.migrations.set('shared->schema', new SharedToSchemaMigration());
    this.migrations.set('schema->dedicated', new SchemaToDedicatedMigration());
  }

  async executeMigration(tenantId: string, targetTier: IsolationTier): Promise<MigrationResult> {
    const tenant = await this.getTenant(tenantId);
    const key = `${tenant.isolationTier}->${targetTier}`;
    const migration = this.migrations.get(key);
    
    if (!migration) {
      throw new Error(`No migration path from ${tenant.isolationTier} to ${targetTier}`);
    }
    
    // Execute with rollback capability
    try {
      const result = await migration.migrate(tenantId);
      await this.auditService.log('migration.completed', {
        tenantId,
        source: tenant.isolationTier,
        target: targetTier,
        result,
      });
      return result;
    } catch (error) {
      await this.rollbackMigration(tenantId, tenant.isolationTier);
      throw error;
    }
  }

  private async rollbackMigration(tenantId: string, originalTier: IsolationTier): Promise<void> {
    // Rollback logic: restore from pre-migration snapshot
    await this.auditService.log('migration.rolled_back', {
      tenantId,
      originalTier,
      timestamp: new Date().toISOString(),
    });
  }
}
```

## Integration Points

- **Tenant Management UI:** Migration status display, trigger button, progress tracking
- **Provisioning Pipeline (Ch 03):** Target infrastructure provisioned during migration
- **Data Portability API (Ch 10):** Reuses export/import functionality for data transfer
- **Monitoring:** Track migration progress, rate, and error metrics
- **Audit Logging:** Every migration step is logged for compliance and debugging

## Open-Source Tools

- **ws** (MIT): WebSocket
- **MediaRecorder API**: Recording
- **Opus** (BSD): Audio codec
## Production Considerations

- **Rollback Always:** Every migration must have a tested rollback plan. Pre-migration: take a full snapshot or backup. Store it until the migration has been verified in production for at least 72 hours.
- **Cutover Window:** Schedule migrations during low-traffic periods. Even with read-only mode lasting only seconds, some requests will be rejected. Communicate the maintenance window to the tenant.
- **Data Size Estimation:** A tenant with 500GB of call recordings will take hours to migrate. Use parallel streaming and compression. Estimate migration time based on data volume and network throughput.
- **Testing Migration:** Test every migration path in a staging environment before production. Rehearse the migration with a copy of the tenant's data.
- **Progress Tracking:** Provide real-time migration progress to operations teams. Key metrics: rows migrated, bytes transferred, remaining time estimate, error count.
- **Foreign Key Considerations:** When migrating schema-per-tenant to dedicated, ensure all cross-schema foreign keys within the tenant's schema are preserved.
- **Sequence Synchronization:** Auto-incrementing primary keys must maintain their current values after migration. Export and import sequence values (`pg_get_serial_sequence`).
- **Compliance Holds:** If a tenant has a legal hold or eDiscovery request, ensure the migration preserves all retained data and metadata.
