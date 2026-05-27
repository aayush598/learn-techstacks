# Section 08: Unified Intent and Topic Analytics Adapter

## Overview

The unified intent and topic analytics adapter integrates all intent and topic analysis capabilities into a single, consistent API. It provides access to intent classification results, topic clusters, intent frequency distributions, trend detection, heatmap data, drill-down analysis, and correlation analysis. The adapter handles routing queries to the appropriate data stores (ClickHouse for historical data, Redis for cached results), manages authentication and authorization, enforces tenant isolation, and transforms data into a unified format consumable by the dashboard and reporting frontend.

The adapter implements the Intent Analytics Protocol (IAP), a GraphQL API designed specifically for intent and topic analytics. Queries can request intent frequency distributions with trend detection, topic cluster hierarchies, heatmap configurations, drill-down paths, and correlation matrices in a single request. The adapter uses DataLoader for batching, Redis for caching with per-resolver TTLs, and ClickHouse's distributed query capabilities for multi-dimensional aggregation.

## Architecture

```
         Unified Intent & Topic Analytics Adapter

   Dashboard / API Clients
        |
   GraphQL (Intent Analytics Protocol)
        |
   ┌────┴────┐
   | Adapter  |
   └────┬────┘
        |
   ┌────┼─────────┬──────────┬──────────┬──────────┐
   |    |         |          |          |          |
   Intent Topic   Frequency  Trend     Heatmap    Drill
   Class  Cluster Distrib   Detect     Config     Down
   |    |         |          |          |          |
   ClickHouse (primary data store)
   Redis (cache, real-time counters)
   ML Service (intent/topic inference)
```

## Design Decisions

- **GraphQL schema designed for exploratory analytics over CRUD operations:** The IAP schema is optimized for read-heavy, exploratory analytics workloads. Queries support filtering by time range, dimensions, and aggregation level. The schema uses connection types (with pagination) for call lists and correlated data. Mutations are limited to refreshing caches and triggering re-classification. Trade-off: a read-optimized GraphQL schema is less suitable for administrative operations (creating intent definitions, managing topic labels), which use a separate REST API.

- **Unified result format with common metadata across all query types:** All query results include: a `metadata` object with `dataSource`, `cachedAt`, `processingTime`, and `totalResults` fields; a `request` object echoing the query parameters; and typed `data` arrays. This consistency allows the frontend to display a "last updated" timestamp, cache indicator, and query parameters regardless of the data type. Trade-off: the unified envelope adds ~200 bytes of overhead per response, but provides consistent user experience.

- **Permission hierarchy enforced at the adapter level over per-resolver checks:** The adapter extracts the user's role and permissions from the JWT context and passes them to a centralized permission checker. The checker evaluates whether the requested data type (intents, topics, drill-down, correlations) is accessible at the requested granularity (tenant-level, campaign-level, agent-level). This avoids repeating permission logic in every resolver and ensures consistent enforcement. Trade-off: centralized permission checking can become complex as the schema grows; permissions are defined in a configuration file loaded at startup.

## Implementation Approach

```typescript
// === Intent Analytics Protocol Types ===

interface IapContext {
  tenantId: string;
  userId: string;
  role: 'agent' | 'supervisor' | 'admin';
  permissions: string[];
}

interface IapQuery {
  intentAnalytics?: {
    timeRange: { start: number; end: number };
    granularity?: 'hour' | 'day' | 'week';
    level?: number;
    includeTrend?: boolean;
    includeCorrelation?: boolean;
    filters?: Record<string, string[]>;
  };
  topicAnalytics?: {
    timeRange: { start: number; end: number };
    includeHierarchy?: boolean;
    minTopicSize?: number;
  };
  drillDown?: {
    level: string;
    intentId?: string;
    callSid?: string;
    page?: number;
    pageSize?: number;
    filters?: Record<string, any>;
  };
}

// === Unified Adapter Implementation ===

class IntentTopicAdapter {
  private intentClassifier: IntentClassifier;
  private topicEngine: TopicClusteringEngine;
  private frequencyService: IntentFrequencyService;
  private trendDetector: IntentTrendDetector;
  private heatmapService: HeatmapService;
  private drillService: IntentDrillService;
  private correlationEngine: IntentCorrelationEngine;
  private cache: CacheManager;
  private permissionChecker: PermissionChecker;

  constructor() {
    this.permissionChecker = new PermissionChecker();
  }

  // Main query handler
  async query(iapQuery: IapQuery, context: IapContext): Promise<Record<string, any>> {
    const result: Record<string, any> = {};

    if (iapQuery.intentAnalytics) {
      this.permissionChecker.require(context, 'analytics:view');
      const q = iapQuery.intentAnalytics;

      result.intentFrequency = await this.frequencyService.getIntentFrequency({
        tenantId: context.tenantId,
        start: q.timeRange.start,
        end: q.timeRange.end,
        granularity: q.granularity ?? 'day',
        level: q.level ?? 2,
        filters: q.filters,
        includeChange: true,
      });

      if (q.includeTrend) {
        result.intentTrends = await this.trendDetector.detectTrends(
          context.tenantId, q.level ?? 2
        );
      }

      if (q.includeCorrelation) {
        result.coOccurrence = await this.correlationEngine.computeCoOccurrence(
          context.tenantId, q.timeRange.start, q.timeRange.end
        );
        result.transitions = await this.correlationEngine.computeSequenceTransitions(
          context.tenantId, q.timeRange.start, q.timeRange.end
        );
      }
    }

    if (iapQuery.topicAnalytics) {
      this.permissionChecker.require(context, 'analytics:view');
      const q = iapQuery.topicAnalytics;

      result.topicClusters = await this.clickhouse.query(`
        SELECT * FROM topic_clusters
        WHERE tenantId = '${context.tenantId}'
          AND createdAt >= ${q.timeRange.start}
          AND createdAt <= ${q.timeRange.end}
      `);
    }

    if (iapQuery.drillDown) {
      const q = iapQuery.drillDown;
      // Permission depends on drill level
      if (q.level === 'call_detail') {
        this.permissionChecker.require(context, 'calls:view-transcription');
      } else {
        this.permissionChecker.require(context, 'analytics:view');
      }

      result.drillData = await this.drillService.getDrillData({
        tenantId: context.tenantId,
        level: q.level as any,
        intentId: q.intentId,
        callSid: q.callSid,
        filters: q.filters as any,
        page: q.page ?? 1,
        pageSize: q.pageSize ?? 50,
      });
    }

    return result;
  }

  // GraphQL resolvers
  resolvers = {
    Query: {
      intentAnalytics: async (
        _: unknown,
        args: IapQuery['intentAnalytics'],
        context: { iap: IapContext }
      ) => {
        return this.query({ intentAnalytics: args! }, context.iap);
      },

      topicAnalytics: async (
        _: unknown,
        args: IapQuery['topicAnalytics'],
        context: { iap: IapContext }
      ) => {
        return this.query({ topicAnalytics: args! }, context.iap);
      },

      intentHeatmap: async (
        _: unknown,
        args: HeatmapConfig,
        context: { iap: IapContext }
      ) => {
        this.permissionChecker.require(context.iap, 'analytics:view');
        return this.heatmapService.getHeatmap({
          ...args,
          tenantId: context.iap.tenantId,
        });
      },

      intentDrillDown: async (
        _: unknown,
        args: IapQuery['drillDown'],
        context: { iap: IapContext }
      ) => {
        return this.query({ drillDown: args! }, context.iap);
      },
    },

    Mutation: {
      refreshIntentCache: async (
        _: unknown,
        __: unknown,
        context: { iap: IapContext }
      ) => {
        this.permissionChecker.require(context.iap, 'analytics:configure');
        await this.cache.flushPattern(`intent:*:${context.iap.tenantId}:*`);
        return { success: true };
      },

      triggerReclassification: async (
        _: unknown,
        args: { callSids: string[] },
        context: { iap: IapContext }
      ) => {
        this.permissionChecker.require(context.iap, 'analytics:configure');
        // Queue reclassification job
        const calls = await this.clickhouse.query(`
          SELECT callSid, transcription FROM call_records
          WHERE tenantId = '${context.iap.tenantId}'
            AND callSid IN (${args.callSids.map(s => `'${s}'`).join(',')})
        `);
        const results = await this.intentClassifier.classifyBatch(
          calls.map((c: any) => ({ text: c.transcription, callSid: c.callSid, tenantId: context.iap.tenantId }))
        );
        return { success: true, reclassifiedCount: results.length };
      },
    },
  };

  // GraphQL schema (simplified)
  typeDefs = `
    type IntentFrequency {
      intentId: String!
      intentName: String!
      callCount: Int!
      frequency: Float!
      change: Float
      significant: Boolean
      trend: String
      children: [IntentFrequency]
    }

    type IntentTrend {
      intentId: String!
      intentName: String!
      volumeTrend: TrendWindow
      sentimentTrend: SentimentTrendWindow
      impactScore: Float!
      dailyCallVolume: Float!
    }

    type TopicCluster {
      topicId: String!
      label: String
      autoLabel: String!
      callCount: Int!
      averageSentiment: Float!
      children: [TopicCluster]
    }

    type CoOccurrence {
      intentA: String!
      intentB: String!
      pmi: Float!
      lift: Float!
      correlation: Float!
      significant: Boolean!
    }

    type DrillResult {
      levels: [DrillLevel!]!
      items: [DrillCallItem!]!
      total: Int!
      page: Int!
      pageSize: Int!
    }

    type Query {
      intentAnalytics(
        timeRange: TimeRangeInput!,
        granularity: String,
        level: Int,
        includeTrend: Boolean,
        includeCorrelation: Boolean,
        filters: JSON
      ): IntentAnalyticsResult!

      topicAnalytics(
        timeRange: TimeRangeInput!,
        includeHierarchy: Boolean
      ): TopicAnalyticsResult!

      intentHeatmap(
        metric: String!,
        xDimension: String!,
        yDimension: String!,
        start: Float!,
        end: Float!
      ): HeatmapResult!

      intentDrillDown(
        level: String!,
        intentId: String,
        callSid: String,
        page: Int,
        pageSize: Int,
        filters: JSON
      ): DrillResult!
    }
  `;
}

// React hook for intent analytics
function useIntentAnalytics(config: {
  timeRange: { start: number; end: number };
  includeTrend?: boolean;
  includeCorrelation?: boolean;
}) {
  const { data, loading } = useQuery(GET_INTENT_ANALYTICS, {
    variables: config,
    fetchPolicy: 'cache-first',
  });

  return {
    frequencies: data?.intentAnalytics?.intentFrequency ?? [],
    trends: data?.intentAnalytics?.intentTrends ?? [],
    correlations: data?.intentAnalytics?.coOccurrence ?? [],
    loading,
  };
}
```

## Open-Source Tools

| Tool | License | Purpose |
|------|---------|---------|
| Apollo Server (MIT) | Server | GraphQL BFF |
| DataLoader (MIT) | Server | Batch query optimization |
| Redis (RSAL) | Server | Cache layer |
| ClickHouse (Apache 2.0) | Server | Primary data store |

## Production Considerations

**Scaling:** The adapter is stateless and scales horizontally behind a load balancer. DataLoader batches requests within a single GraphQL query — 20 intent frequency requests become 1 ClickHouse query. Redis caches are partitioned by tenant ID to prevent cross-tenant cache contamination. Cache TTLs vary by data type: 5 minutes for intent frequency, 10 minutes for trends, 30 minutes for topic clusters, 2 minutes for heatmaps.

**Security:** The permission checker evaluates access at the adapter level. Intent analytics at the tenant level requires `analytics:view`. Drill-down to call level requires `calls:view`. Transcription viewing requires `calls:view-transcription`. Per-agent intent breakdowns require `agent-performance:view`. The permission configuration is loaded from PostgreSQL on startup and cached for 5 minutes.

**Monitoring:** Track adapter query rate, resolver response times per type, cache hit rates, and DataLoader batch sizes. Alert if any resolver's p95 exceeds 500 ms. Monitor the number of active GraphQL subscriptions for intent analytics. Track the cache miss rate — if it exceeds 30%, review TTL configurations or increase cache capacity.
