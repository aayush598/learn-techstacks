# Section 08: Unified Performance Metrics Adapter

## Overview

The unified performance metrics adapter is the integration layer that abstracts all call volume and performance metric computations behind a consistent API. It provides a single entry point for querying any metric (call volume, AHT, ASA, service level, abandonment rate, occupancy, duration distribution) across any dimension (time range, queue, campaign, agent group) and at any granularity (real-time, hourly, daily, weekly, monthly). The adapter handles routing queries to the appropriate data store (Redis for real-time, ClickHouse for historical), transforming results into a consistent format, and managing caching and error handling.

The adapter implements the Metric-Query Protocol (MQP), a GraphQL-based query language specifically designed for time-series metric data. Queries specify the metric name, dimensions, filters, granularity, and time range. The adapter translates MQP queries into the appropriate backend queries (Redis TimeSeries commands, ClickHouse SQL) and returns typed results. This abstraction enables the frontend to request any metric without knowing which data store backs it.

## Architecture

```
               Unified Performance Metrics Adapter

   Dashboard / API Clients
        |
   GraphQL (Metric-Query Protocol)
        |
   ┌────┴────┐
   | Adapter  |
   └────┬────┘
        |
   ┌────┼──────────────┐
   |    |              |
   Real-time       Historical
   Resolver        Resolver
   (Redis TS)      (ClickHouse)
   |    |              |
   |    |         Aggregation
   |    |         Engine
   |    |
   Cache Layer (Redis)
```

## Design Decisions

- **Metric-Query Protocol (MQP) over REST for metric queries:** MQP is a GraphQL schema where metrics are first-class types with fields for value, timestamp, dimensions, and metadata. A single GraphQL query can request multiple metrics across different dimensions and time ranges, reducing the number of API calls from 10+ to 1 for a typical dashboard load. Trade-off: MQP requires GraphQL schema design and resolver implementation; simpler REST endpoints would be faster to implement but would require more round trips.

- **Unified metric metadata registry over hardcoded metric names:** Each metric is defined in a registry with its name, description, unit, data source (Redis or ClickHouse), aggregation method, supported dimensions, and default visualization type. The adapter uses this registry to resolve queries, validate inputs, and provide auto-completion for the GraphQL schema. New metrics can be added by registering them in the database without code changes. Trade-off: the registry adds indirection and requires a schema migration for new metrics.

- **Adaptive caching with stale-while-revalidate over fixed TTL:** Different metrics change at different rates (call volume changes every second; abandonment rate changes slowly). The cache TTL is adaptive: metrics that change frequently have shorter TTLs (5 seconds for real-time metrics, 5 minutes for hourly metrics). When a cache entry is stale, the adapter returns the cached value immediately while fetching the fresh value in the background (stale-while-revalidate). Trade-off: stale-while-revalidate adds complexity to the caching layer but ensures dashboards never show loading spinners.

## Implementation Approach

```typescript
// === Metric-Query Protocol Types ===

interface MetricQuery {
  metrics: string[];            // e.g., ['callVolume', 'aht', 'asa']
  dimensions?: {                // grouping dimensions
    by?: string[];              // e.g., ['queue', 'campaign', 'agent']
    filters?: Record<string, string[]>;
  };
  timeRange: {
    start: number;
    end: number;
    granularity: 'raw' | '5min' | 'hour' | 'day' | 'week';
  };
  includeComparison?: boolean;
  comparisonPeriod?: 'previous_period' | 'same_period_last_week' | 'same_period_last_month' | 'year_over_year';
}

interface MetricResult {
  name: string;
  unit: string;
  data: Array<{
    timestamp: number;
    value: number;
    dimensions?: Record<string, string>;
  }>;
  comparison?: {
    values: Array<{ timestamp: number; value: number }>;
    delta: number;
    percentageDelta: number;
  };
  metadata: {
    dataSource: 'redis' | 'clickhouse';
    granularity: string;
    totalPoints: number;
    cached: boolean;
    cachedAt?: number;
  };
}

// === Metric Registry ===

interface MetricDefinition {
  name: string;
  displayName: string;
  description: string;
  unit: 'count' | 'seconds' | 'percentage' | 'ratio';
  dataSource: 'redis' | 'clickhouse';
  redisKey?: string;
  clickhouseQuery?: string;
  supportedDimensions: string[];
  granularities: string[];
  aggregation: 'avg' | 'sum' | 'count' | 'p95';
  defaultVisualization: 'line' | 'gauge' | 'bar' | 'histogram';
  ttlSeconds: number;           // cache TTL
}

class MetricRegistry {
  private definitions: Map<string, MetricDefinition> = new Map();

  register(definition: MetricDefinition): void {
    this.definitions.set(definition.name, definition);
  }

  get(name: string): MetricDefinition | undefined {
    return this.definitions.get(name);
  }

  getAll(): MetricDefinition[] {
    return Array.from(this.definitions.values());
  }
}

// === Adapter Implementation ===

class MetricsAdapter {
  private registry: MetricRegistry;
  private redisTs: RedisTimeSeries;
  private clickhouse: ClickHouseClient;
  private cache: CacheManager;

  constructor() {
    this.registry = new MetricRegistry();
    this.redisTs = new RedisTimeSeries({ host: process.env.REDIS_HOST });
    this.clickhouse = new ClickHouseClient({ host: process.env.CLICKHOUSE_HOST });
    this.cache = new CacheManager({ adapter: 'redis' });
    this.registerDefaultMetrics();
  }

  private registerDefaultMetrics(): void {
    this.registry.register({
      name: 'callVolume',
      displayName: 'Call Volume',
      description: 'Number of calls offered',
      unit: 'count',
      dataSource: 'clickhouse',
      supportedDimensions: ['queue', 'campaign', 'direction'],
      granularities: ['5min', 'hour', 'day', 'week'],
      aggregation: 'sum',
      defaultVisualization: 'line',
      ttlSeconds: 60,
    });
    this.registry.register({
      name: 'aht',
      displayName: 'Average Handle Time',
      description: 'Average talk + hold + ACW time',
      unit: 'seconds',
      dataSource: 'clickhouse',
      supportedDimensions: ['queue', 'campaign', 'agent'],
      granularities: ['hour', 'day', 'week'],
      aggregation: 'avg',
      defaultVisualization: 'line',
      ttlSeconds: 300,
    });
    this.registry.register({
      name: 'asa',
      displayName: 'Average Speed of Answer',
      description: 'Average queue wait time for answered calls',
      unit: 'seconds',
      dataSource: 'clickhouse',
      supportedDimensions: ['queue', 'campaign'],
      granularities: ['5min', 'hour', 'day'],
      aggregation: 'avg',
      defaultVisualization: 'line',
      ttlSeconds: 300,
    });
    this.registry.register({
      name: 'serviceLevel',
      displayName: 'Service Level',
      description: 'Percentage answered within target seconds',
      unit: 'percentage',
      dataSource: 'clickhouse',
      supportedDimensions: ['queue'],
      granularities: ['5min', 'hour', 'day'],
      aggregation: 'avg',
      defaultVisualization: 'gauge',
      ttlSeconds: 60,
    });
    this.registry.register({
      name: 'abandonmentRate',
      displayName: 'Abandonment Rate',
      description: 'Percentage of callers who hung up before answer',
      unit: 'percentage',
      dataSource: 'clickhouse',
      supportedDimensions: ['queue', 'campaign'],
      granularities: ['hour', 'day', 'week'],
      aggregation: 'avg',
      defaultVisualization: 'line',
      ttlSeconds: 300,
    });
  }

  async query(tenantId: string, query: MetricQuery): Promise<Record<string, MetricResult>> {
    const results: Record<string, MetricResult> = {};

    for (const metricName of query.metrics) {
      const definition = this.registry.get(metricName);
      if (!definition) {
        throw new Error(`Unknown metric: ${metricName}`);
      }

      // Check cache
      const cacheKey = `metrics:${tenantId}:${metricName}:${JSON.stringify(query)}`;
      const cached = await this.cache.get(cacheKey);
      if (cached) {
        results[metricName] = { ...cached, metadata: { ...cached.metadata, cached: true, cachedAt: Date.now() } };
        continue;
      }

      // Query appropriate data source
      let data: Array<{ timestamp: number; value: number; dimensions?: Record<string, string> }>;

      if (definition.dataSource === 'redis') {
        data = await this.queryRedis(tenantId, metricName, definition, query);
      } else {
        data = await this.queryClickhouse(tenantId, metricName, definition, query);
      }

      const result: MetricResult = {
        name: metricName,
        unit: definition.unit,
        data,
        metadata: {
          dataSource: definition.dataSource,
          granularity: query.timeRange.granularity,
          totalPoints: data.length,
          cached: false,
        },
      };

      // Compute comparison if requested
      if (query.includeComparison && query.comparisonPeriod) {
        result.comparison = await this.computeComparison(tenantId, metricName, definition, query);
      }

      // Cache result
      await this.cache.set(cacheKey, result, definition.ttlSeconds);

      results[metricName] = result;
    }

    return results;
  }

  private async queryRedis(
    tenantId: string,
    metricName: string,
    definition: MetricDefinition,
    query: MetricQuery
  ): Promise<Array<{ timestamp: number; value: number }>> {
    const key = `ts:${tenantId}:${metricName}`;
    const range = await this.redisTs.range(key, query.timeRange.start, query.timeRange.end);
    return range.map(([timestamp, value]: [number, number]) => ({
      timestamp,
      value,
    }));
  }

  private async queryClickhouse(
    tenantId: string,
    metricName: string,
    definition: MetricDefinition,
    query: MetricQuery
  ): Promise<Array<{ timestamp: number; value: number; dimensions?: Record<string, string> }>> {
    // Build ClickHouse query from metric definition and query parameters
    const granularityFn = this.getGranularityFunction(query.timeRange.granularity);
    const aggregationFn = definition.aggregation === 'p95' ? 'quantile(0.95)' : definition.aggregation;

    let sql = `
      SELECT
        ${granularityFn}(timestamp) as period,
        ${aggregationFn}(value) as value
    `;

    // Add dimension columns
    if (query.dimensions?.by && query.dimensions.by.length > 0) {
      sql += `, ${query.dimensions.by.map(d => `${d}Id as ${d}`).join(', ')}`;
    }

    sql += `
      FROM daily_metric_rollups
      WHERE tenantId = '${tenantId}'
        AND metric = '${metricName}'
        AND timestamp >= ${query.timeRange.start}
        AND timestamp <= ${query.timeRange.end}
    `;

    // Add filters
    if (query.dimensions?.filters) {
      for (const [dim, values] of Object.entries(query.dimensions.filters)) {
        if (values.length > 0) {
          sql += ` AND ${dim}Id IN (${values.map(v => `'${v}'`).join(',')})`;
        }
      }
    }

    sql += ` GROUP BY period`;
    if (query.dimensions?.by) {
      sql += `, ${query.dimensions.by.map(d => `${d}Id`).join(', ')}`;
    }
    sql += ` ORDER BY period`;

    const result = await this.clickhouse.query(sql);

    return result.map((row: any) => ({
      timestamp: new Date(row.period).getTime(),
      value: row.value,
      dimensions: query.dimensions?.by
        ? Object.fromEntries(query.dimensions.by.map((d: string) => [d, row[d]]))
        : undefined,
    }));
  }

  private async computeComparison(
    tenantId: string,
    metricName: string,
    definition: MetricDefinition,
    query: MetricQuery
  ): Promise<MetricResult['comparison']> {
    const duration = query.timeRange.end - query.timeRange.start;
    let comparisonStart: number;

    switch (query.comparisonPeriod) {
      case 'previous_period':
        comparisonStart = query.timeRange.start - duration;
        break;
      case 'same_period_last_week':
        comparisonStart = query.timeRange.start - 7 * 24 * 3600 * 1000;
        break;
      case 'same_period_last_month':
        comparisonStart = query.timeRange.start - 30 * 24 * 3600 * 1000;
        break;
      case 'year_over_year':
        comparisonStart = query.timeRange.start - 365 * 24 * 3600 * 1000;
        break;
      default:
        return undefined;
    }

    const comparisonQuery: MetricQuery = {
      ...query,
      timeRange: { ...query.timeRange, start: comparisonStart, end: comparisonStart + duration },
      includeComparison: false,
    };

    const current = await this.queryClickhouse(tenantId, metricName, definition, query);
    const previous = await this.queryClickhouse(tenantId, metricName, definition, comparisonQuery);

    const currentAvg = current.reduce((s, p) => s + p.value, 0) / (current.length || 1);
    const previousAvg = previous.reduce((s, p) => s + p.value, 0) / (previous.length || 1);
    const delta = currentAvg - previousAvg;

    return {
      values: previous,
      delta,
      percentageDelta: previousAvg !== 0 ? (delta / previousAvg) * 100 : 0,
    };
  }

  private getGranularityFunction(granularity: string): string {
    switch (granularity) {
      case '5min': return 'toStartOfFiveMinutes';
      case 'hour': return 'toStartOfHour';
      case 'day': return 'toDate';
      case 'week': return 'toStartOfWeek';
      default: return 'toStartOfHour';
    }
  }
}

// GraphQL resolver using the adapter
const metricsResolver = {
  Query: {
    metrics: async (_: unknown, args: { query: MetricQuery }, context: Context) => {
      const adapter = new MetricsAdapter();
      return adapter.query(context.tenantId, args.query);
    },
    metricDefinitions: async (_: unknown, __: unknown, context: Context) => {
      const adapter = new MetricsAdapter();
      return adapter['registry'].getAll();
    },
  },
};
```

## Open-Source Tools

| Tool | License | Purpose |
|------|---------|---------|
| GraphQL (MIT) | Server | Metric-Query Protocol |
| Apollo Server (MIT) | Server | GraphQL server |
| RedisTimeSeries (RSAL) | Server | Real-time metric cache |
| ClickHouse (Apache 2.0) | Server | Historical metric warehouse |

## Production Considerations

**Scaling:** The adapter is stateless and scales horizontally. Each instance maintains its own connection pool to Redis and ClickHouse. Use DataLoader to batch same-metric queries within a single request. For high-traffic tenants (100+ dashboard users), enable query result caching with per-tenant cache key prefixes. The metric registry is loaded at startup from the database and refreshed every 5 minutes.

**Security:** The adapter validates that the requesting user has the necessary permission for each requested metric. Some metrics (AHT by agent, occupancy) require `agent-performance:view` while others (call volume, service level) require `analytics:view`. The registry includes a `requiredPermission` field. Cache keys include the tenant ID to prevent cross-tenant cache hits.

**Monitoring:** Track adapter query rate, p50/p95/p99 response time per metric, cache hit rate, and error rate. Alert if any metric query's p95 exceeds 1 second for Redis-sourced metrics or 3 seconds for ClickHouse-sourced metrics. Monitor the metric registry freshness — if the registry hasn't been updated in 10 minutes, log a warning. Track the number of active metric definitions and warn if it exceeds 200 (indicates metric proliferation).
