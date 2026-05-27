# Section 01: Tenancy Model Comparison Framework

## Overview

Multi-tenancy is the architectural foundation that enables a single SaaS instance to serve multiple customers (tenants) while maintaining data isolation, security, and performance. Choosing the right tenancy model is one of the most consequential architectural decisions for a voice agent platform, affecting everything from operational cost and development velocity to compliance certification and customer trust. The four primary models are database-per-tenant, schema-per-tenant, shared-tenant with row-level security, and hybrid approaches that combine elements of each.

Each model exists on a spectrum of isolation versus operational efficiency. Database-per-tenant provides the strongest isolation but the highest operational overhead and cost. Schema-per-tenant offers a middle ground with shared infrastructure but logical separation. Shared-tenant with RLS minimizes cost and operational complexity but requires careful security implementation. The hybrid approach allows different customers to receive different isolation levels based on their requirements, making it suitable for platforms serving both SMB and enterprise customers.

The decision framework must consider data sensitivity (healthcare, financial), compliance requirements (HIPAA, SOC 2, PCI), tenant size and growth patterns, operational complexity tolerance, and cost structure. For a voice agent platform, the choice also affects how call recordings, transcripts, and AI model configurations are isolated between customers.

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

```
interface TenancyModel {
  createTenant(config: TenantConfig): Promise<Tenant>;
  getContext(): TenantContext;
  executeQuery<T>(query: string, params: any[]): Promise<T>;
  migrateTenant(tenantId: string, targetModel: TenancyModel): Promise<void>;
}

class DatabasePerTenantModel implements TenancyModel {
  private connections: Map<string, Pool>;

  async createTenant(config: TenantConfig): Promise<Tenant> {
    const dbName = `tenant_${config.tenantId}_${config.region}`;
    await this.provisionDatabase(dbName);
    await this.runMigrations(dbName);
    return { id: config.tenantId, database: dbName };
  }

  getContext(): TenantContext {
    // Extract from request-scoped storage (AsyncLocalStorage)
    return AlsContext.getStore().tenant;
  }

  async executeQuery<T>(query: string, params: any[]): Promise<T> {
    const { tenantId } = this.getContext();
    const pool = this.connections.get(tenantId);
    return pool.query(query, params);
  }
}

class SharedTenantModel implements TenancyModel {
  private pool: Pool;

  async createTenant(config: TenantConfig): Promise<Tenant> {
    await this.pool.query(
      'INSERT INTO tenants (id, name, tier) VALUES ($1, $2, $3)',
      [config.tenantId, config.name, config.tier]
    );
    await this.pool.query(
      `GRANT USAGE ON SCHEMA public TO "${config.tenantId}"`
    );
    return { id: config.tenantId };
  }

  getContext(): TenantContext {
    return AlsContext.getStore().tenant;
  }

  async executeQuery<T>(query: string, params: any[]): Promise<T> {
    const { tenantId } = this.getContext();
    // Set tenant context for RLS policies
    await this.pool.query(
      `SELECT set_config('app.tenant_id', $1, true)`,
      [tenantId]
    );
    return this.pool.query(query, params);
  }
}
```

## Integration Points

- **Tenant Provisioning:** Models integrate with the provisioning pipeline (Ch 03) for automated tenant creation
- **API Gateway:** Tenant context extraction happens in middleware shared across all API routes
- **Knowledge Base:** Per-tenant knowledge base isolation depends on the tenancy model
- **Analytics:** Aggregated analytics require cross-tenant queries with proper isolation
- **Data Migration:** Migration between models (Ch 10) handles data transfer and re-provisioning

## Open-Source Tools

- **ws** (MIT): WebSocket
- **MediaRecorder API**: Recording
- **Opus** (BSD): Audio codec
## Production Considerations

- **Connection Pool Limits:** Each database connection consumes memory. Database-per-tenant with many tenants may hit PostgreSQL connection limits. Use PgBouncer for connection pooling and consider connection limits per tenant.
- **Backup Complexity:** Database-per-tenant requires orchestrating backups across potentially hundreds of databases. Implement a centralized backup scheduler with per-tenant retention policies.
- **Monitoring:** Track per-tenant query performance. A noisy neighbor in shared-tenant can impact other tenants. Implement statement timeout and resource quotas.
- **Connection Warm-up:** For database-per-tenant, consider lazy connection establishment on first request to avoid provisioning costs for idle tenants.
- **RLS Performance:** RLS policies add query overhead (typically 3-8%). Benchmark complex policies and ensure proper indexing for the tenant_id column.
- **Testing:** Maintain test suites that validate tenant isolation across all models. Automated penetration testing should verify no cross-tenant data leakage.
- **Migration Tooling:** Build tooling early for moving tenants between models. Expect migrations to be rare but critical when needed.
