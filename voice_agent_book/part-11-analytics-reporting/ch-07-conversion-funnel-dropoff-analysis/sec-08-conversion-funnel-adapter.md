# Section 08: Unified Conversion Funnel Adapter

## Overview

The unified conversion funnel adapter integrates all funnel analysis capabilities — stage definition, conversion tracking, drop-off identification, funnel visualization, comparison analysis, A/B testing, and optimization insights — into a single, consistent API. It provides a unified data model, query interface, and permission enforcement layer for the funnel analytics dashboard. The adapter abstracts the underlying data stores (ClickHouse for events, PostgreSQL for configurations, Redis for caching) behind a GraphQL schema designed for funnel analytics.

The adapter implements the Funnel Analytics Protocol (FAP), which defines funnel-specific query types: funnel overview (overall conversion, stage-by-stage breakdown, drop-off summary), funnel comparison (period, segment, experiment), funnel A/B test (results, variant details, Bayesian probabilities), and funnel insights (recommendations with impact estimates). The adapter handles caching with per-query TTLs, enforces tenant isolation, and provides DataLoader-based batching for efficient query resolution.

## Architecture

```
         Unified Conversion Funnel Adapter

   Dashboard / API Clients
        |
   GraphQL (Funnel Analytics Protocol)
        |
   ┌────┴────┐
   | Adapter  |
   └────┬────┘
        |
   ┌────┼──────┬─────────┬─────────────┬──────────┐
   |    |      |         |             |          |
   Stage Conversion Drop-off Comparison A/B Test  Insights
   Defin Resolver Resolver Resolver     Resolver  Resolver
   |    |      |         |             |          |
   PG   CH     CH       CH             CH        CH
   (def) (evts) (evts)   (evts)        (evts)    (metrics)
        |
   Redis Cache (all layers)
```

## Design Decisions

- **Funnel-specific GraphQL schema over generic analytics schema:** The FAP uses types specific to funnel analysis: `FunnelStage`, `ConversionRate`, `DropOffSummary`, `FunnelComparison`, `AbTest`, `OptimizationInsight`. This provides strongly typed queries with auto-completion for funnel-specific operations. Generic analytics queries (time series, trends) use the Intent Analytics Protocol or Metrics Adapter. Trade-off: a dedicated funnel schema requires maintaining a separate GraphQL type system, but provides a better developer experience for funnel-focused use cases.

- **Hybrid caching (Redis + CDN) for funnel data:** Funnel overview data (conversion rates, stage metrics) is relatively static — it changes only when new events arrive. Redis caches with 60-second TTL serve most dashboard requests. For highly cached queries (e.g., "overall funnel for last 7 days" viewed by 50 supervisors simultaneously), a CDN (Cloudflare, Fastly) with 5-minute TTL reduces origin load. Cache invalidation is event-based: when a new funnel event arrives, the relevant cache keys are invalidated via Redis Pub/Sub. Trade-off: CDN caching introduces 5-minute staleness for the most popular queries; the dashboard shows a "cached" indicator.

- **Unified permission model with stage-level granularity over query-level checks:** Funnel data access follows a hierarchy: funnel overview (anyone with `analytics:view`), stage-level drop-off details (`analytics:view`), comparison with agent filter (`agent-performance:view`), A/B test results (`analytics:view`), and optimization insights with agent names (`agent-performance:view`). The adapter evaluates permissions at the query level based on the filters and fields requested, rather than checking each resolver individually. Trade-off: unified permission checking requires parsing the GraphQL query to determine which fields are requested, adding complexity to the permission layer.

## Implementation Approach

```typescript
// === Funnel Analytics Protocol Types ===

interface FunnelQuery {
  funnelId: string;
  timeRange: { start: number; end: number };
  segment?: { dimension: string; value: string };
  includeStages?: string[];       // Filter to specific stages
  includeDropOffs?: boolean;
  includeComparison?: {
    enabled: boolean;
    mode?: 'period' | 'segment';
    comparisonTimeRange?: { start: number; end: number };
  };
}

interface FunnelAnalyticsResult {
  funnelId: string;
  funnelName: string;
  overallConversionRate: number;
  totalEntries: number;
  totalConversions: number;
  stages: FunnelStageResult[];
  dropOffSummary?: DropOffSummary[];
  comparison?: FunnelComparisonResult;
  insights?: OptimizationRecommendation[];
  metadata: {
    cached: boolean;
    cachedAt?: number;
    processingTime: number;
  };
}

// === Unified Adapter Implementation ===

class FunnelAdapter {
  private stageService: FunnelStageService;
  private conversionTracker: ConversionTracker;
  private dropOffAnalyzer: DropOffAnalyzer;
  private visualizationService: FunnelVisualizationService;
  private comparisonEngine: FunnelComparisonEngine;
  private abTestEngine: AbTestEngine;
  private insightEngine: OptimizationInsightEngine;
  private cache: CacheManager;
  private permissionChecker: PermissionChecker;

  constructor() {
    this.cache = new CacheManager({ adapter: 'redis' });
    this.permissionChecker = new PermissionChecker();
  }

  async getFunnelAnalytics(
    query: FunnelQuery,
    context: IapContext
  ): Promise<FunnelAnalyticsResult> {
    this.permissionChecker.require(context, 'analytics:view');
    const startTime = Date.now();
    const cacheKey = `funnel:analytics:${context.tenantId}:${JSON.stringify(query)}`;

    const cached = await this.cache.get(cacheKey);
    if (cached) {
      return { ...cached, metadata: { ...cached.metadata, cached: true, cachedAt: Date.now() } };
    }

    // Get funnel definition
    const funnelDef = await this.stageService.getFunnel(query.funnelId, context.tenantId);
    if (!funnelDef) throw new Error(`Funnel ${query.funnelId} not found`);

    // Get conversion rates
    const conversionRates = await this.conversionTracker.getConversionRates(
      context.tenantId,
      query.funnelId,
      query.timeRange.start,
      query.timeRange.end,
      query.includeStages
    );

    // Get overall conversion
    const overall = await this.conversionTracker.getOverallConversion(
      context.tenantId,
      query.funnelId,
      query.timeRange.start,
      query.timeRange.end
    );

    // Get drop-off summary if requested
    let dropOffSummary: DropOffSummary[] | undefined;
    if (query.includeDropOffs) {
      dropOffSummary = await this.dropOffAnalyzer.identifyDropOffs(
        context.tenantId,
        query.funnelId,
        query.timeRange.start,
        query.timeRange.end
      );
    }

    // Get comparison if requested
    let comparisonResult: FunnelComparisonResult | undefined;
    if (query.includeComparison?.enabled) {
      this.permissionChecker.require(context, 'analytics:view');
      const comparisonQuery = query.includeComparison;
      const comparisonTimeRange = comparisonQuery.comparisonTimeRange ?? {
        start: query.timeRange.start - (query.timeRange.end - query.timeRange.start),
        end: query.timeRange.start,
      };

      const comparison = await this.comparisonEngine.compare({
        tenantId: context.tenantId,
        funnelId: query.funnelId,
        mode: comparisonQuery.mode ?? 'period',
        primaryFilter: {
          start: query.timeRange.start,
          end: query.timeRange.end,
          segment: query.segment,
        },
        comparisonFilter: {
          start: comparisonTimeRange.start,
          end: comparisonTimeRange.end,
          segment: query.segment,
        },
        stages: query.includeStages,
      });
      comparisonResult = comparison;
    }

    // Get insights
    const insights = await this.insightEngine.generateRecommendations(
      context.tenantId,
      query.funnelId
    );

    const result: FunnelAnalyticsResult = {
      funnelId: query.funnelId,
      funnelName: funnelDef.name,
      overallConversionRate: overall.overallRate,
      totalEntries: overall.startEntries,
      totalConversions: overall.finalExits,
      stages: conversionRates.map(cr => ({
        ...cr,
        name: funnelDef.stages.find(s => s.id === cr.stageId)?.name ?? cr.stageId,
        order: funnelDef.stages.find(s => s.id === cr.stageId)?.order ?? 0,
      })).sort((a, b) => a.order - b.order),
      dropOffSummary,
      comparison: comparisonResult,
      insights,
      metadata: {
        cached: false,
        processingTime: Date.now() - startTime,
      },
    };

    // Cache for 1 minute
    await this.cache.setex(cacheKey, 60, result);

    return result;
  }

  async getAbTestResults(
    testId: string,
    context: IapContext
  ): Promise<{ test: AbTestConfig; results: AbTestResult[] }> {
    this.permissionChecker.require(context, 'analytics:view');
    const test = await this.clickhouse.query(
      `SELECT * FROM ab_tests WHERE id = '${testId}' AND tenantId = '${context.tenantId}'`
    );
    if (test.length === 0) throw new Error(`Test ${testId} not found`);

    const results = await this.abTestEngine.getResults(testId);
    return { test: test[0], results };
  }

  // GraphQL schema
  typeDefs = `
    type FunnelOverview {
      funnelId: String!
      funnelName: String!
      overallConversionRate: Float!
      totalEntries: Int!
      totalConversions: Int!
      stages: [FunnelStageMetrics!]!
      dropOffSummary: [DropOffSummary!]
      comparison: FunnelComparisonResult
      insights: [OptimizationInsight!]
    }

    type FunnelStageMetrics {
      stageId: String!
      stageName: String!
      order: Int!
      entries: Int!
      exits: Int!
      dropOffs: Int!
      conversionRate: Float!
      cumulativeConversion: Float!
      averageDuration: Float!
      previousConversionRate: Float
      conversionDelta: Float
      significant: Boolean
    }

    type DropOffSummary {
      stageId: String!
      stageName: String!
      dropOffRate: Float!
      totalDropOffs: Int!
      byType: JSON!
      estimatedCost: Float!
    }

    type Query {
      funnelAnalytics(
        funnelId: String!,
        timeRange: TimeRangeInput!,
        segment: SegmentInput,
        includeDropOffs: Boolean,
        includeComparison: ComparisonInput
      ): FunnelOverview!

      abTestResults(testId: String!): AbTestResultPayload!

      funnelDefinitions: [FunnelDefinition!]!
    }

    type Mutation {
      createFunnel(funnel: FunnelInput!): FunnelDefinition!
      startAbTest(config: AbTestInput!): AbTestConfig!
      dismissInsight(insightId: String!): Boolean!
    }
  `;
}

// React hook for funnel analytics
function useFunnelAnalytics(config: {
  funnelId: string;
  timeRange: { start: number; end: number };
  includeDropOffs?: boolean;
}) {
  const { data, loading, refetch } = useQuery(GET_FUNNEL_ANALYTICS, {
    variables: config,
    fetchPolicy: 'cache-and-network',
  });

  return {
    overview: data?.funnelAnalytics,
    stages: data?.funnelAnalytics?.stages ?? [],
    dropOffs: data?.funnelAnalytics?.dropOffSummary ?? [],
    loading,
    refetch,
  };
}
```

## Open-Source Tools

| Tool | License | Purpose |
|------|---------|---------|
| Apollo Server (MIT) | Server | GraphQL BFF |
| DataLoader (MIT) | Server | Batch query optimization |
| Redis (RSAL) | Server | Cache layer |
| ClickHouse (Apache 2.0) | Server | Primary event store |

## Production Considerations

**Scaling:** The adapter is stateless and scales horizontally. DataLoader batches within-query requests — e.g., if the funnel query also requests drop-off data for each stage, DataLoader batches all stage drop-off queries into one ClickHouse query with `GROUP BY stageId`. Redis cache with 60-second TTL handles most requests without hitting ClickHouse. For high-traffic tenants (>50 concurrent dashboard users), enable CDN caching for the most common funnel queries (last 7 days, last 30 days).

**Security:** The permission checker evaluates access at query time based on requested fields and filters. Funnel overview requires `analytics:view`. Drop-off details with agent-level breakdown require `agent-performance:view`. A/B test configuration requires `analytics:configure`. Optimization insights referencing specific agents require `agent-performance:view`.

**Monitoring:** Track adapter query rate, response time per funnel (p95 < 500 ms), cache hit rate, and DataLoader batch efficiency. Alert if any funnel query fails or exceeds 2 seconds. Monitor the number of active A/B tests and their status distribution. Track insight click-through rate and dismissal rate to evaluate recommendation relevance.
