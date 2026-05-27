# Section 04: Shared Tenant + RLS Strategy

## Overview

The shared-tenant with Row-Level Security (RLS) model is the most operationally efficient multi-tenancy approach. All tenants share the same database tables, and tenant isolation is enforced at the database level through PostgreSQL RLS policies. Every row in every table contains a `tenant_id` column, and RLS policies transparently filter queries based on the current tenant context. This model minimizes infrastructure costs, simplifies operations (single database, single schema, single migration), and provides reasonable isolation for standard SaaS deployments.

PostgreSQL RLS works by attaching policy expressions to tables that are automatically appended to every query. A policy like `USING (tenant_id = current_setting('app.tenant_id')::UUID)` ensures that users can only see rows belonging to their tenant. These policies are enforced at the database engine level, meaning they apply regardless of how the data is accessed—through queries, views, ORMs, or raw SQL connections. This defense-in-depth approach means even if application-level tenant filtering fails, the database provides a safety net.

For a voice agent platform, the shared model is suitable for the default self-service tier where cost efficiency is paramount. Call records, agent configurations, transcripts, and analytics data all reside in shared tables with tenant_id discrimination. However, this model requires rigorous testing to ensure RLS policies are comprehensive and correct, and it lacks the compliance isolation that some regulations require.

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
// Database schema setup
async function setupRLS(): Promise<void> {
  const tables = ['calls', 'agents', 'transcripts', 'campaigns', 
                  'recordings', 'configurations', 'analytics_events'];

  for (const table of tables) {
    // Ensure tenant_id column exists
    await pool.query(`
      ALTER TABLE ${table} 
      ADD COLUMN IF NOT EXISTS tenant_id UUID 
      REFERENCES tenants(id) NOT NULL
    `);

    // Enable RLS
    await pool.query(`ALTER TABLE ${table} ENABLE ROW LEVEL SECURITY`);

    // Drop existing policy to avoid duplicates
    await pool.query(`DROP POLICY IF EXISTS tenant_isolation ON ${table}`);

    // Create tenant isolation policy
    await pool.query(`
      CREATE POLICY tenant_isolation ON ${table}
      FOR ALL
      USING (tenant_id = current_setting('app.tenant_id')::UUID)
      WITH CHECK (tenant_id = current_setting('app.tenant_id')::UUID)
    `);
  }

  // Create admin override policy
  await pool.query(`
    CREATE POLICY admin_override ON calls
    FOR SELECT
    USING (current_setting('app.user_role') = 'admin')
  `);
}

// Request middleware (Next.js / Express)
async function tenantContextMiddleware(req: Request, res: Response, next: NextFunction) {
  const tenantId = extractTenantFromRequest(req); // From JWT, API key, or domain
  
  // Set tenant context in AsyncLocalStorage for application-level use
  AlsContext.run({ tenantId, userId: req.user.id }, async () => {
    // Set in database session for RLS
    await pool.query('BEGIN');
    await pool.query(`SELECT set_config('app.tenant_id', $1, true)`, [tenantId]);
    await pool.query(`SELECT set_config('app.user_role', $1, true)`, [req.user.role]);
    
    try {
      await next();
    } finally {
      await pool.query('COMMIT');
    }
  });
}

// Example query (RLS transparently filters)
async function getCalls(filters: CallFilters): Promise<Call[]> {
  // No WHERE tenant_id = ? needed — RLS handles it
  const result = await pool.query(
    `SELECT * FROM calls 
     WHERE status = $1 
     AND created_at >= $2
     ORDER BY created_at DESC
     LIMIT 50`,
    [filters.status, filters.since]
  );
  return result.rows;
}
```

## Integration Points

- **Middleware Layer:** Tenant context must be established before any database query
- **Backup:** Single backup for all tenants; selective restore requires table-level filtering
- **Analytics:** Cross-tenant analytics queries need `SET ROLE` to admin or disable RLS
- **Data Migration:** Export operations filter by tenant_id; imports must set tenant_id correctly
- **Monitoring:** Track per-tenant row counts and query performance within shared tables

## Open-Source Tools

- **ws** (MIT): WebSocket
- **MediaRecorder API**: Recording
- **Opus** (BSD): Audio codec
## Production Considerations

- **RLS Performance Overhead:** RLS policies add query overhead. For simple equality checks on indexed columns, overhead is typically 3-8%. Policies with subqueries or function calls can add 20%+ overhead. Use `EXPLAIN ANALYZE` with and without RLS to measure impact.
- **Indexing Strategy:** Every RLS-filtered column (tenant_id) must be indexed. Composite indexes like `(tenant_id, created_at DESC)` optimize the common query pattern of "get my recent items".
- **Connection Pooling:** `SET LOCAL` is transaction-scoped, which works correctly with PgBouncer transaction mode. Never use `SET SESSION` as it can leak tenant context between requests using the same connection.
- **Admin Access:** Create a separate database role for admin/cross-tenant queries. Use `ALTER TABLE ... DISABLE ROW LEVEL SECURITY` only in maintenance windows, never in application code.
- **Testing:** Every deployment should include automated RLS penetration tests that verify:
  - Tenant A cannot see Tenant B's data via direct queries
  - Tenant A cannot see Tenant B's data via JOINs
  - Tenant A cannot see Tenant B's data via subqueries
  - SQL injection cannot bypass RLS
- **Monitoring RLS Violations:** Log any RLS policy violations using PostgreSQL audit logging. Create alerts for repeated violation attempts.
- **Partitioning:** For very large tables (billions of rows), consider partitioning by tenant_id to improve query performance and enable partition-level operations.
