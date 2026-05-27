# Section 05: Hybrid Multi-Tenancy Approaches

## Overview

A hybrid multi-tenancy architecture combines multiple isolation models to serve different customer segments optimally. Rather than forcing all tenants into a single model, the platform offers a tiered approach: small tenants share infrastructure with RLS, mid-market tenants get schema-level isolation, and enterprise tenants receive dedicated databases. This tiered strategy allows the platform to optimize for both cost efficiency (serving hundreds of small tenants inexpensively) and compliance requirements (meeting enterprise audit demands).

The hybrid model is particularly powerful for a voice agent SaaS that serves diverse customer segments. A startup using the platform for outbound sales calls has very different isolation needs than a healthcare provider using the platform for patient communications. By making isolation level a feature that customers can select (or that is determined by their plan tier), the platform can capture value at both ends of the market while maintaining operational efficiency.

The core challenge of a hybrid architecture is managing the complexity of multiple isolation mechanisms within a single codebase. The data access layer must abstract away whether a tenant is on shared, schema, or dedicated infrastructure. Connection routing, migration management, backup strategies, and monitoring all become conditional on the tenant's isolation tier.

## Architecture

```
+----------+    +----------+    +----------+    +----------+    +----------+
| AI       |--->| Monitor  |--->| Escalatio|--->| Human    |--->| Seamless |
| Handles  |    | (watch)  |    | n Detect |    | Takes    |    | Context  |
| Call     |    | (confid  |    | (score > |    | Over     |    | Transfer |
|          |    |  low)    |    |  0.8)    |    | (active) |    | (state)  |
+----------+    +----------+    +----------+    +----------+    +----------+
```


## Design Decisions

- **AI-First with Human Oversight**: AI handles all calls. Human monitors threshold-based escalations.
- **State Machine**: Five states: AI_ACTIVE, MONITORING, ESCALATING, HUMAN_ACTIVE, RETURNING_TO_AI.
- **Context Preservation**: Full transcript + state transferred on handoff. No repetition for customer.
## Implementation Approach

```typescript
interface DataAccessLayer {
  query<T>(query: string, params: any[]): Promise<T>;
}

class TenantModelRouter {
  private sharedPool: Pool;
  private schemaPool: Pool;
  private tenantConnections: Map<string, Pool>;

  constructor(config: DALConfig) {
    this.sharedPool = new Pool(config.sharedConnection);
    this.schemaPool = new Pool(config.schemaConnection);
    this.tenantConnections = new Map();
  }

  getDAL(tenant: Tenant): DataAccessLayer {
    switch (tenant.isolationTier) {
      case 'shared':
        return new SharedDAL(this.sharedPool, tenant.id);
      case 'schema':
        return new SchemaDAL(this.schemaPool, tenant.id);
      case 'dedicated':
        return new DedicatedDAL(this.getTenantPool(tenant.id));
    }
  }

  async queryTenant<T>(
    tenantId: string, 
    query: string, 
    params: any[]
  ): Promise<T> {
    const tenant = await this.getTenant(tenantId);
    const dal = this.getDAL(tenant);
    return dal.query(query, params);
  }
}

class SharedDAL implements DataAccessLayer {
  constructor(private pool: Pool, private tenantId: string) {}

  async query<T>(query: string, params: any[]): Promise<T> {
    return this.pool.transaction(async (client) => {
      await client.query(
        `SELECT set_config('app.tenant_id', $1, true)`,
        [this.tenantId]
      );
      return client.query(query, params);
    });
  }
}

class SchemaDAL implements DataAccessLayer {
  private schemaName: string;

  constructor(private pool: Pool, tenantId: string) {
    this.schemaName = `tenant_${tenantId.slice(0, 12)}`;
  }

  async query<T>(query: string, params: any[]): Promise<T> {
    return this.pool.transaction(async (client) => {
      await client.query(
        `SET LOCAL search_path TO "${this.schemaName}", public`
      );
      return client.query(query, params);
    });
  }
}

class DedicatedDAL implements DataAccessLayer {
  constructor(private pool: Pool) {}

  async query<T>(query: string, params: any[]): Promise<T> {
    return this.pool.query(query, params);
  }
}

// Migration orchestration across tiers
async function runMigrationForAllTenants(migration: Migration): Promise<void> {
  const tenants = await getAllTenants();
  const results: MigrationResult[] = [];

  for (const tenant of tenants) {
    try {
      const dal = router.getDAL(tenant);
      await migration.up(tenant, dal);
      results.push({ tenantId: tenant.id, status: 'success' });
    } catch (error) {
      results.push({ tenantId: tenant.id, status: 'failed', error });
      await alertService.sendTenantAlert(tenant.id, 'migration_failed', { error });
    }
  }

  await analyticsService.recordMigrationBatch(results);
}

// Tier upgrade migration
async function upgradeTenantTier(
  tenantId: string, 
  targetTier: 'shared' | 'schema' | 'dedicated'
): Promise<void> {
  const tenant = await getTenant(tenantId);
  const currentTier = tenant.isolationTier;

  if (currentTier === targetTier) return;

  // 1. Mark tenant as "migrating"
  await updateTenantStatus(tenantId, 'migrating');

  // 2. Provision target infrastructure
  await provisionForTier(tenant, targetTier);

  // 3. Export data from current tier
  const exportData = await exportTenantData(tenant, currentTier);

  // 4. Import data to target tier
  await importTenantData(tenant, targetTier, exportData);

  // 5. Verify data consistency
  await verifyMigration(tenant, exportData);

  // 6. Switch tenant to new tier
  await updateTenantTier(tenantId, targetTier);

  // 7. Decommission old infrastructure
  await decommissionTier(tenant, currentTier);

  // 8. Mark tenant as "active"
  await updateTenantStatus(tenantId, 'active');
}
```

## Integration Points

- **Plan Management (Part 17):** Tenant isolation tier is determined by subscription plan
- **Provisioning Pipeline (Ch 03):** Tier selection happens during provisioning and determines infrastructure to create
- **Data Export/Import (Ch 10):** Migration between tiers reuses the data portability system
- **Cost Tracking (Part 17):** Infrastructure cost per tier feeds into COGS calculations
- **Monitoring:** Aggregated monitoring must work across all tiers with tier-specific metrics

## Open-Source Tools

- **Redis** (BSD): State machine
- **Mediasoup** (MIT): Audio bridge
- **BullMQ** (MIT): Handoff queue
## Production Considerations

- **Tier Migration Tooling:** Invest heavily in migration automation early. Manual migrations between isolation tiers are error-prone and time-consuming. Test migration paths thoroughly before offering self-service upgrades.
- **Pricing Isolation:** Isolation tier should correlate with plan tier. Free/Starter plans use shared, Growth plans get schema, Enterprise gets dedicated. This creates a natural upgrade incentive.
- **Resource Planning:** Each tier has different resource profiles. Shared tier needs IOPS headroom for peak loads. Dedicated tier needs per-instance monitoring. Plan capacity accordingly.
- **Support Escalation:** Enterprise customers on dedicated infrastructure require different support procedures. Ensure support tooling is tier-aware.
- **Feature Parity:** Maintain feature parity across tiers where possible. The only difference should be data isolation and performance guarantees, not missing functionality.
- **Monitoring Consolidation:** Even with different tiers, monitoring should provide a unified view. Use labels/tags to identify tenant tier and aggregate metrics across tiers for platform-level visibility.
- **Cost Allocation:** Implement chargeback/showback for infrastructure costs. The dedicated tier's per-database costs must be accurately attributed.
