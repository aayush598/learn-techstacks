# Section 06: Tenant-Aware Database Migrations

## Overview

Database migrations in a multi-tenant architecture present unique challenges that don't exist in single-tenant applications. A schema change must be applied to every tenant's data environment, whether that's in a shared table, a per-tenant schema, or per-tenant database. The migration must be safe to run across potentially thousands of tenants, each with different data volumes, custom configurations, and uptime requirements. A migration that works perfectly for a small tenant with 100 rows might cause a multi-hour lock on a large tenant with 100 million rows.

The migration strategy depends on the tenancy model. For shared+RLS, a single ALTER TABLE affects all tenants simultaneously—fast, but risky if the migration has issues. For schema-per-tenant, a loop applies the same migration to each schema independently—slower but with better blast radius control. For database-per-tenant, each database gets its own migration run—most flexible but most operationally complex.

Beyond the technical execution, tenant-aware migrations must handle tenant-specific migrations (some tenants get different schema versions), migration version tracking per tenant, phased rollouts (canary tenants first), and rollback procedures that work at the tenant level. Every migration should be reversible and tested against production-scale data before deployment.

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
interface Migration {
  id: string;
  name: string;
  description: string;
  up: (client: DatabaseClient, tenantId: string) => Promise<void>;
  down: (client: DatabaseClient, tenantId: string) => Promise<void>;
  check: (client: DatabaseClient, tenantId: string) => Promise<MigrationCheck>;
  parallelSafe: boolean;
  estimatedDuration: string; // e.g., "5s", "2min", "30min"
}

class TenantAwareMigrationRunner {
  private migrationRegistry: Map<string, number>;
  private currentBatch: string[];

  constructor(
    private pool: Pool,
    private tenantService: TenantService,
    private alertService: AlertService
  ) {}

  async runMigration(migration: Migration): Promise<MigrationResult> {
    const tenants = await this.tenantService.getActiveTenants();
    const results: TenantMigrationResult[] = [];

    // Phase 1: Canary (internal tenants)
    const internalTenants = tenants.filter(t => t.tier === 'internal');
    const canaryResults = await this.migrateBatch(internalTenants, migration, 'canary');
    results.push(...canaryResults);

    if (canaryResults.some(r => r.status === 'failed')) {
      const failedTenants = canaryResults.filter(r => r.status === 'failed');
      await this.alertService.sendMigrationAlert(migration.id, failedTenants);
      await this.rollbackBatch(failedTenants, migration);
      return { status: 'rolled_back', failedTenants };
    }

    // Phase 2: Gradual rollout (25% increments)
    const tiers = ['starter', 'growth', 'business', 'enterprise'];
    for (const tier of tiers) {
      const tierTenants = tenants.filter(t => t.tier === tier);
      const batchResults = await this.migrateBatch(tierTenants, migration, tier);
      results.push(...batchResults);

      if (batchResults.some(r => r.status === 'failed')) {
        const failedTenants = batchResults.filter(r => r.status === 'failed');
        await this.alertService.sendMigrationAlert(migration.id, failedTenants);
        
        if (batchResults.filter(r => r.status === 'failed').length > tierTenants.length * 0.01) {
          // >1% failure rate, rollback entire tier
          await this.rollbackBatch(tierTenants, migration);
          return { status: 'paused', failedTenants, tier };
        }
      }

      // Monitoring gate: wait and verify
      await this.verifyMigrationHealth(migration, tier, tierTenants);
    }

    return { status: 'completed', results };
  }

  private async migrateBatch(
    tenants: Tenant[],
    migration: Migration,
    batchName: string
  ): Promise<TenantMigrationResult[]> {
    const results: TenantMigrationResult[] = [];

    // Determine parallelism based on migration type
    const parallelism = migration.parallelSafe ? 10 : 1;
    const batches = chunkArray(tenants, parallelism);

    for (const batch of batches) {
      const batchPromises = batch.map(tenant => 
        this.migrateSingleTenant(tenant, migration)
      );
      const batchResults = await Promise.allSettled(batchPromises);
      
      for (const result of batchResults) {
        if (result.status === 'fulfilled') {
          results.push(result.value);
        } else {
          results.push({
            tenantId: 'unknown',
            status: 'failed',
            error: result.reason,
          });
        }
      }
    }

    return results;
  }

  private async migrateSingleTenant(
    tenant: Tenant,
    migration: Migration
  ): Promise<TenantMigrationResult> {
    const startTime = Date.now();
    
    try {
      // Acquire tenant migration lock
      const lock = await this.acquireMigrationLock(tenant.id);
      if (!lock) {
        return { tenantId: tenant.id, status: 'skipped', reason: 'locked' };
      }

      // Run pre-migration check
      const check = await this.runPreMigrationCheck(tenant, migration);
      if (!check.passed) {
        return { tenantId: tenant.id, status: 'skipped', reason: check.reason };
      }

      // Execute migration
      const client = await this.getTenantClient(tenant);
      await migration.up(client, tenant.id);

      // Update migration version
      await this.updateMigrationVersion(tenant.id, migration.id);

      // Run post-migration verification
      await this.verifyMigration(tenant, migration);

      const duration = Date.now() - startTime;
      return { tenantId: tenant.id, status: 'completed', duration };
    } catch (error) {
      return { tenantId: tenant.id, status: 'failed', error: error.message };
    }
  }

  private async rollbackBatch(
    tenants: Tenant[],
    migration: Migration
  ): Promise<void> {
    for (const tenant of tenants) {
      try {
        const client = await this.getTenantClient(tenant);
        await migration.down(client, tenant.id);
        await this.alertService.send({
          type: 'migration_rolled_back',
          tenantId: tenant.id,
          migrationId: migration.id,
        });
      } catch (error) {
        // Manual intervention required for rollback failures
        await this.alertService.send({
          type: 'rollback_failed',
          tenantId: tenant.id,
          error: error.message,
          severity: 'critical',
          requiresManualIntervention: true,
        });
      }
    }
  }

  async runOnlineSchemaChange(
    tenant: Tenant,
    tableName: string,
    alterStatement: string
  ): Promise<void> {
    // Use pgroll for zero-downtime schema changes
    const client = await this.getTenantClient(tenant);
    
    // Create new table with desired schema
    await client.query(`
      CREATE TABLE ${tableName}_new (LIKE ${tableName} INCLUDING ALL)
    `);
    await client.query(alterStatement.replace(tableName, `${tableName}_new`));

    // Create trigger to sync writes to both tables
    await client.query(`
      CREATE FUNCTION sync_${tableName}_fn() RETURNS TRIGGER AS $$
      BEGIN
        INSERT INTO ${tableName}_new SELECT * FROM ${tableName} WHERE id = NEW.id;
        RETURN NEW;
      END;
      $$ LANGUAGE plpgsql;
    `);

    // Backfill data in batches
    await client.query(`
      INSERT INTO ${tableName}_new 
      SELECT * FROM ${tableName} 
      WHERE id > $1 
      ORDER BY id 
      LIMIT 1000
    `);

    // Swap tables
    await client.query(`ALTER TABLE ${tableName} RENAME TO ${tableName}_old`);
    await client.query(`ALTER TABLE ${tableName}_new RENAME TO ${tableName}`);

    // Drop old table after verification
    await client.query(`DROP TABLE ${tableName}_old`);
  }
}
```

## Integration Points

- **CI/CD Pipeline:** Migrations are deployed through the same pipeline as application code
- **Tenant Registry:** Central registry tracks migration version per tenant
- **Monitoring:** Migration metrics (duration, success rate, locks) feed into dashboards
- **Incident Response:** Migration failures trigger automatic rollback and alerting
- **Data Migration (Ch 10):** Schema migrations are the foundation for data migration between tiers

## Open-Source Tools

- **ws** (MIT): WebSocket
- **MediaRecorder API**: Recording
- **Opus** (BSD): Audio codec
## Production Considerations

- **Lock Timeouts:** Set `lock_timeout` in migration sessions to prevent long-running locks. An ALTER TABLE that takes more than 5 seconds should be automatically cancelled and retried using online schema change tools.
- **Tenant Migration Locking:** Use a distributed lock (Redis Redlock or PostgreSQL advisory lock) to prevent concurrent migrations on the same tenant.
- **Aborted Migration Cleanup:** If a migration fails mid-way, have a cleanup script that reverts partial changes. Track "dirty" tenants that need manual review.
- **Migration Dry-Run:** Every migration should support a `--dry-run` mode that reports what would change without actually applying. Run dry-runs against production data before deployment.
- **Dependency Ordering:** Migrations may have dependencies on each other. Track dependency graphs and enforce linear migration ordering per tenant.
- **Emergency Pause:** Implement a kill switch that pauses all tenant migrations when a critical issue is detected. This prevents a bad migration from spreading.
- **Tenant Blacklist:** Maintain a list of tenants that should be skipped during automatic migration (e.g., tenants with custom schema modifications, legal holds).
- **Backward Compatibility:** Database schema changes must be backward-compatible with the current version of the application code. Never remove columns that the current code still references.
