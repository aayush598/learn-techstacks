# Section 04: RLS Performance Optimization

## Overview

Row-Level Security policies add query overhead—every row touched by a query must be evaluated against active policies. While simple equality policies (tenant_id = current_setting(...)) typically add only 3-8% overhead, complex policies with subqueries, joins, or function calls can degrade query performance by 50% or more. In a high-throughput voice agent platform processing thousands of calls per second, RLS performance optimization is critical to maintaining sub-100ms API response times.

The key to RLS performance is ensuring that policy expressions reference indexed columns and avoid row-by-row computation. A well-designed RLS policy with a matching index can be nearly as fast as an un-filtered query. Poorly designed policies, especially those with correlated subqueries or unindexed columns, can force sequential scans on every query.

Performance optimization spans multiple layers: index design for tenant_id columns, policy expression simplification, use of immutable functions for context lookups, query planner hints, and monitoring with EXPLAIN ANALYZE. Additionally, certain query patterns (batch operations, analytic queries) may need special handling to work efficiently with RLS.

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

```sql
-- 1. Create efficient composite indexes for RLS
-- Common query: "Get my recent calls"
CREATE INDEX idx_calls_tenant_created 
  ON calls (tenant_id, created_at DESC);

-- Common query: "Get my active calls"
CREATE INDEX idx_calls_tenant_status_created
  ON calls (tenant_id, status, created_at DESC);

-- Common query: "Search my calls by phone number"
CREATE INDEX idx_calls_tenant_caller 
  ON calls (tenant_id, caller_phone);

-- 2. Use IMMUTABLE functions for context lookup
-- IMMUTABLE tells PostgreSQL the function always returns same value for same input
-- This allows the planner to evaluate it once per query, not per row
CREATE OR REPLACE FUNCTION app.current_tenant_id()
RETURNS UUID
LANGUAGE SQL
IMMUTABLE  -- Actually STABLE, but IMMUTABLE is safe here as it's session-level
PARALLEL SAFE
AS $$
  SELECT current_setting('app.tenant_id', true)::UUID;
$$;

-- 3. Create partial indexes for specific RLS scenarios
-- Only index active calls (common query pattern)
CREATE INDEX idx_calls_active_for_tenant 
  ON calls (tenant_id, created_at DESC)
  WHERE status IN ('pending', 'in_progress', 'queued');

-- 4. Optimized RLS policy using indexed columns
CREATE POLICY optimized_tenant_isolation ON calls
  FOR SELECT
  USING (tenant_id = app.current_tenant_id());
-- This will use the composite index idx_calls_tenant_created

-- 5. For admin override, use role-based approach
CREATE POLICY admin_override ON calls
  FOR ALL
  USING (current_setting('app.user_role', true) = 'admin');
-- Avoid subquery, just check a session parameter

-- 6. Use row-level security with partitioning for large tenants
-- Create partitions by tenant (requires PostgreSQL 12+)
CREATE TABLE calls_partitioned (
  tenant_id UUID NOT NULL,
  id UUID NOT NULL DEFAULT gen_random_uuid(),
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  -- ... other columns
) PARTITION BY LIST (tenant_id);

-- Automatic partition creation (using pg_partman or custom trigger)
CREATE TABLE calls_tenant_abc PARTITION OF calls_partitioned
  FOR VALUES IN ('abc12345-...');
CREATE TABLE calls_tenant_xyz PARTITION OF calls_partitioned
  FOR VALUES IN ('xyz67890-...');

-- 7. Benchmark RLS vs no-RLS
-- Use EXPLAIN ANALYZE to compare performance
EXPLAIN (ANALYZE, BUFFERS)
SELECT * FROM calls 
WHERE created_at >= NOW() - INTERVAL '7 days'
LIMIT 100;

-- Compare with explicit tenant filter
EXPLAIN (ANALYZE, BUFFERS)
SELECT * FROM calls 
WHERE tenant_id = 'abc12345-...'
  AND created_at >= NOW() - INTERVAL '7 days'
LIMIT 100;
```

## Performance Testing Strategy

```typescript
// Automated RLS performance testing
class RLSPerformanceTest {
  async runBenchmark(): Promise<BenchmarkResult> {
    const queries = [
      { name: 'list_recent_calls', sql: 'SELECT * FROM calls WHERE created_at >= NOW() - $1 INTERVAL \'1 day\' LIMIT 50' },
      { name: 'get_call_by_id', sql: 'SELECT * FROM calls WHERE id = $1' },
      { name: 'search_by_phone', sql: 'SELECT * FROM calls WHERE caller_phone LIKE $1' },
      { name: 'active_calls_count', sql: 'SELECT COUNT(*) FROM calls WHERE status IN (\'in_progress\')' },
    ];

    const results: QueryTiming[] = [];

    for (const query of queries) {
      // With RLS
      const withRLS = await this.measureWithRLS(query);
      
      // Without RLS (explicit tenant_id filter)
      const withoutRLS = await this.measureWithoutRLS(query);
      
      results.push({
        queryName: query.name,
        withRLS: withRLS,
        withoutRLS: withoutRLS,
        overhead: ((withRLS - withoutRLS) / withoutRLS * 100).toFixed(2) + '%',
      });
    }

    return { queries: results, timestamp: new Date().toISOString() };
  }

  private async measureWithRLS(query: QueryDef, iterations = 100): Promise<number> {
    const times: number[] = [];
    for (let i = 0; i < iterations; i++) {
      const start = process.hrtime.bigint();
      await this.pool.query(`SELECT set_config('app.tenant_id', $1, true)`, [this.testTenantId]);
      await this.pool.query(query.sql, query.params);
      times.push(Number(process.hrtime.bigint() - start));
    }
    return median(times);
  }
}
```

## Integration Points

- **Index Management:** Automated index analysis tools (pg_stat_all_indexes) inform RLS optimization
- **Query Monitoring:** pg_stat_statements tracks query performance per normalized query pattern
- **Capacity Planning:** RLS overhead factor is included in capacity calculations
- **Tenant Tier:** Enterprise tenants on dedicated databases don't need RLS, eliminating overhead entirely
- **CI/CD Pipeline:** RLS performance benchmarks run as part of deployment pipeline

## Open-Source Tools

- **ws** (MIT): WebSocket
- **MediaRecorder API**: Recording
- **Opus** (BSD): Audio codec
## Production Considerations

- **Monitor RLS Overhead:** Track the "RLS check" time in query profiling. Use `auto_explain` module to log slow queries with RLS overhead.
- **Index Maintenance:** As data grows, monitor index bloat. Reindex tenant_id composite indexes during maintenance windows.
- **Query Planner Statistics:** Ensure `ANALYZE` runs regularly. Outdated statistics cause the planner to misestimate row counts, leading to suboptimal plans.
- **Connection Pool Impact:** `SET LOCAL` statements add overhead to each connection acquisition. In high-throughput scenarios, consider setting tenant context once per connection and recycling connections by tenant.
- **Vacuum Strategy:** RLS-filtered tables may have different dead tuple patterns. Monitor autovacuum settings for tables with RLS.
- **Read Replicas:** RLS policies apply on read replicas as well. Ensure session parameters are set on replica connections before querying.
- **WAL Generation:** RLS evaluation doesn't affect WAL generation since it only filters existing data, but partition pruning disabled by RLS can lead to more data being scanned.
- **Benchmark Before/After:** Always benchmark RLS impact before deploying new policies. Use `EXPLAIN (ANALYZE, BUFFERS)` with representative data volumes.
