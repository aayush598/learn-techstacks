# Section 08: Unified Agent Scorecard Adapter

## Overview

The unified agent scorecard adapter is the integration layer that abstracts all scorecard-related computations behind a single API. It provides a consistent interface for querying scorecard data (current scores, historical trends, benchmark comparisons, QA integration, adherence tracking, CSAT correlation) across any agent, team, or campaign. The adapter routes queries to the appropriate data stores (ClickHouse for scorecard data, PostgreSQL for template configs, Redis for real-time metrics) and transforms results into a unified format consumable by the dashboard and reporting systems.

The adapter implements the Scorecard Data Protocol (SDP), a GraphQL-based API that exposes scorecards, benchmarks, trends, and QA data as interconnected types. A single query can fetch an agent's current scorecard, their benchmark comparison, and their 12-week trend in one round trip. The adapter handles authorization — agents see only their own data, supervisors see team data, administrators see all data — and enforces data isolation between tenants.

## Architecture

```
              Unified Agent Scorecard Adapter

   Dashboard / Reporting Clients
        |
   GraphQL (Scorecard Data Protocol)
        |
   ┌────┴────┐
   | Adapter  |
   └────┬────┘
        |
   ┌────┼────────────┬──────────────┐
   |    |            |              |
   Score  Benchmark  Trend       QA/CSAT
   Resolver Resolver Resolver    Resolver
   |    |            |              |
   ClickHouse (primary scorecard store)
   PostgreSQL (template config)
   Redis (real-time scorecard cache)
   External APIs (WFM, HR, training)
```

## Design Decisions

- **Denormalized scorecard snapshot table for fast reads over normalized schema:** The adapter reads from a denormalized ClickHouse table that stores the complete scorecard snapshot for each agent-period in a single row (overall score + all dimension scores + benchmark percentiles). This avoids JOINs and sub-queries that would slow down dashboard loading. The normalized data (individual metric values) is stored in a separate table for drill-down queries. Trade-off: denormalization duplicates data and requires careful management of updates; the scorecard engine writes to both tables atomically.

- **DataLoader-based batching for GraphQL resolvers over individual queries:** When a supervisor loads a dashboard showing 20 agents' scorecards, the standard approach would make 20 individual database queries (one per agent). DataLoader batches these into a single query with `WHERE agentId IN (...)` and distributes the results back to the correct resolvers. This reduces database load by 95% for typical dashboard views. Trade-off: DataLoader adds complexity to the resolver layer and requires careful management of cache invalidation.

- **Stale-while-revalidate caching with tenant-aware cache keys over no caching:** Scorecard data changes daily (or weekly) and is read frequently (every dashboard load). The adapter caches scorecard snapshots in Redis with a TTL of 15 minutes. When returning cached data, the adapter includes a `cachedAt` timestamp so the UI can show "last updated: 10 minutes ago." Scorecards are recomputed on a schedule, and the cache is invalidated when the new snapshot is written. Trade-off: stale-while-revalidate may serve data that is up to 15 minutes old; supervisors who need real-time data can force a refresh.

## Implementation Approach

```typescript
// === Scorecard Data Protocol Types ===

interface ScorecardQuery {
  agentIds: string[];
  period?: { date?: string; start?: string; end?: string };
  includeBenchmarks?: boolean;
  includeTrend?: boolean;
  includeQa?: boolean;
  tenantId: string;
}

interface ScorecardResponse {
  agentId: string;
  tenantId: string;
  period: { date: string; start: string; end: string };
  overallScore: number;
  overallPercentile?: number;
  overallRank?: number;
  dimensions: Array<{
    name: string;
    score: number;
    weight: number;
    contribution: number;
    benchmark?: {
      peerAverage: number;
      percentile: number;
      performance: string;
    };
  }>;
  trend?: TrendResult;
  lastUpdated: number;
  cached: boolean;
}

// === Unified Adapter Implementation ===

class ScorecardAdapter {
  private clickhouse: ClickHouseClient;
  private redis: Redis;
  private benchmarkEngine: BenchmarkEngine;
  private trendAnalyzer: TrendAnalyzer;
  private qaIntegration: QaScoreIntegration;

  constructor() {
    this.clickhouse = new ClickHouseClient({ host: process.env.CLICKHOUSE_HOST });
    this.redis = new Redis({ host: process.env.REDIS_HOST });
    this.benchmarkEngine = new BenchmarkEngine();
    this.trendAnalyzer = new TrendAnalyzer();
    this.qaIntegration = new QaScoreIntegration();
  }

  // DataLoader-compatible batch function
  async getScorecardsBatch(
    query: ScorecardQuery
  ): Promise<Map<string, ScorecardResponse>> {
    const { agentIds, period, tenantId } = query;
    const date = period?.date ?? new Date().toISOString().split('T')[0];

    // Check cache
    const cacheKeys = agentIds.map(id => `scorecard:${tenantId}:${id}:${date}`);
    const cachedResults = await this.redis.mget(cacheKeys);
    const results = new Map<string, ScorecardResponse>();
    const uncachedIds: string[] = [];

    for (let i = 0; i < agentIds.length; i++) {
      if (cachedResults[i]) {
        const parsed = JSON.parse(cachedResults[i]);
        results.set(agentIds[i], { ...parsed, cached: true });
      } else {
        uncachedIds.push(agentIds[i]);
      }
    }

    if (uncachedIds.length > 0) {
      // Batch query ClickHouse
      const idList = uncachedIds.map(id => `'${id}'`).join(',');
      const scoreData = await this.clickhouse.query(`
        SELECT
          agentId, overallScore, overallPercentile, overallRank,
          dimensionScores, lastUpdated
        FROM agent_scorecards
        WHERE agentId IN (${idList})
          AND tenantId = '${tenantId}'
          AND date = '${date}'
      `);

      // Get benchmarks if requested
      let benchmarks: Map<string, BenchmarkResult> | undefined;
      if (query.includeBenchmarks) {
        benchmarks = await this.benchmarkEngine.computeBenchmarks(
          'default',
          tenantId,
          new Date(date).getTime() - 30 * 24 * 3600 * 1000,
          new Date(date).getTime()
        );
      }

      for (const row of scoreData) {
        const response: ScorecardResponse = {
          agentId: row.agentId,
          tenantId,
          period: { date, start: date, end: date },
          overallScore: row.overallScore,
          overallPercentile: row.overallPercentile,
          overallRank: row.overallRank,
          dimensions: row.dimensionScores.map((d: any) => ({
            ...d,
            benchmark: benchmarks?.get(row.agentId)?.metrics
              .find(m => m.metricKey === d.name) ?? undefined,
          })),
          lastUpdated: row.lastUpdated,
          cached: false,
        };

        // Fetch trend if requested (separate query)
        if (query.includeTrend) {
          try {
            response.trend = await this.trendAnalyzer.computeTrends(
              row.agentId, tenantId, 'overall'
            );
          } catch {
            // Insufficient data
          }
        }

        // Cache in Redis
        await this.redis.setex(
          `scorecard:${tenantId}:${row.agentId}:${date}`,
          900,   // 15 min TTL
          JSON.stringify(response)
        );

        results.set(row.agentId, response);
      }
    }

    return results;
  }

  // GraphQL resolvers
  resolvers = {
    Query: {
      scorecard: async (
        _: unknown,
        args: { agentId: string; date?: string },
        context: Context
      ) => {
        this.requireAccess(context, args.agentId, 'scorecard:view');
        const results = await this.getScorecardsBatch({
          agentIds: [args.agentId],
          period: { date: args.date },
          includeBenchmarks: true,
          includeTrend: true,
          tenantId: context.tenantId,
        });
        return results.get(args.agentId) ?? null;
      },

      teamScorecards: async (
        _: unknown,
        args: { teamId: string; date?: string },
        context: Context
      ) => {
        this.requirePermission(context, 'scorecard:view-team');
        const teamAgents = await this.getTeamMembers(args.teamId, context.tenantId);
        const results = await this.getScorecardsBatch({
          agentIds: teamAgents,
          period: { date: args.date },
          includeBenchmarks: true,
          tenantId: context.tenantId,
        });
        return Array.from(results.values());
      },

      agentComparison: async (
        _: unknown,
        args: { agentIds: string[]; metric: string },
        context: Context
      ) => {
        this.requireAccess(context, args.agentIds, 'scorecard:view');
        const results = await this.getScorecardsBatch({
          agentIds: args.agentIds,
          includeBenchmarks: true,
          tenantId: context.tenantId,
        });

        // Return comparison data for the specified metric
        return Array.from(results.values()).map(r => ({
          agentId: r.agentId,
          overallScore: r.overallScore,
          metricScore: r.dimensions.find(d => d.name === args.metric)?.score ?? 0,
          percentile: r.dimensions.find(d => d.name === args.metric)?.benchmark?.percentile ?? 0,
        }));
      },
    },

    Mutation: {
      refreshScorecard: async (
        _: unknown,
        args: { agentId: string },
        context: Context
      ) => {
        this.requireAccess(context, args.agentId, 'scorecard:refresh');
        // Invalidate cache so next read triggers recomputation
        const date = new Date().toISOString().split('T')[0];
        await this.redis.del(`scorecard:${context.tenantId}:${args.agentId}:${date}`);
        return { success: true };
      },
    },
  };

  private requireAccess(context: Context, agentId: string | string[], permission: string): void {
    // Agent can access their own data; supervisors access team data
    if (context.userId === agentId || (Array.isArray(agentId) && agentId.includes(context.userId))) {
      return; // Agent viewing own data
    }
    this.requirePermission(context, permission);
  }

  private requirePermission(context: Context, permission: string): void {
    if (!context.permissions.includes(permission)) {
      throw new Error(`FORBIDDEN: ${permission} required`);
    }
  }

  private async getTeamMembers(teamId: string, tenantId: string): Promise<string[]> {
    const result = await this.clickhouse.query(`
      SELECT agentId FROM agents
      WHERE teamId = '${teamId}' AND tenantId = '${tenantId}'
    `);
    return result.map((r: any) => r.agentId);
  }
}

// React hook for scorecard data
function useScorecard(agentId: string, options?: { includeTrend?: boolean }) {
  const [data, setData] = useState<ScorecardResponse | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    setLoading(true);
    fetchScorecard(agentId, options)
      .then(setData)
      .finally(() => setLoading(false));
  }, [agentId]);

  return { data, loading };
}
```

## Open-Source Tools

| Tool | License | Purpose |
|------|---------|---------|
| Apollo Server (MIT) | Server | GraphQL BFF for scorecard data |
| DataLoader (MIT) | Server | Batch query optimization |
| Redis (RSAL) | Server | Scorecard cache |
| ClickHouse (Apache 2.0) | Server | Primary scorecard store |

## Production Considerations

**Scaling:** The adapter is stateless and scales horizontally. Each instance connects to the same Redis cache cluster. DataLoader ensures that even with 100 agents in a single page load, only one ClickHouse query per data type is made. The Redis cache uses per-tenant key prefixes (`scorecard:{tenantId}:{agentId}:{date}`) to prevent cache key collisions. Cache TTL is 15 minutes — the daily scorecard recomputation job invalidates these cache keys after writing new data.

**Security:** The adapter is the authorization boundary for all scorecard data. Every resolver checks that the requesting user has the appropriate permission (`scorecard:view` for own data, `scorecard:view-team` for team data, `scorecard:view-all` for any agent). The tenant ID is extracted from the JWT and injected into every query as a filter, preventing cross-tenant data access. Benchmark data includes only peer averages and percentiles (not raw values of other agents).

**Monitoring:** Track adapter query rate, p50/p95/p99 resolver response time, cache hit rate per data type, and DataLoader batch efficiency (average batch size). Alert if p95 response time exceeds 500 ms or cache hit rate drops below 80%. Monitor the scorecard cache size per tenant — if it exceeds 1 GB, reduce the TTL or implement LRU eviction.
