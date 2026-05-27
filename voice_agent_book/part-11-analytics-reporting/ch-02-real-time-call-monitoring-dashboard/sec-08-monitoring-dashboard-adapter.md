# Section 08: Unified Monitoring Dashboard Adapter

## Overview

The unified monitoring dashboard adapter is the integration layer that connects the real-time call monitoring dashboard to the broader voice agent platform. It abstracts the data sources (Kafka events, Redis streams, ClickHouse aggregations), the WebSocket gateway, the alert engine, and the configuration persistence into a single, cohesive API that the dashboard client consumes. The adapter pattern ensures that the dashboard frontend is decoupled from the underlying infrastructure — enabling future migrations (e.g., Kafka to Redpanda, ClickHouse to DuckDB) without frontend changes.

The adapter exposes four main interfaces: the feed service (live call events), the metrics service (widget data and chart time series), the alerts service (rule management and alert instances), and the configuration service (dashboard CRUD, sharing, templates). Each service has a well-defined interface with TypeScript types, retry policies, caching strategies, and error handling. The adapter runs on the server side as an API gateway (BFF — Backend for Frontend) that aggregates and transforms data for the specific needs of the monitoring dashboard.

## Architecture

```
               Unified Monitoring Dashboard Adapter

   Dashboard Client (React)
        |
   BFF API Gateway (Node.js)
        |
   ┌────┴────┐
   | Adapter |
   └────┬────┘
        |
   ┌────┼────┬────┐
   |    |    |    |
   Feed  Met  Alert Config
   Srv   Srv  Srv   Srv
   |    |    |    |
   Kafka Redis Click Postgres
```

## Design Decisions

- **BFF pattern over direct client-to-service communication:** The dashboard client communicates exclusively with the BFF API gateway, which internally routes requests to the appropriate backend services. This encapsulation allows the backend to evolve independently — a change to the Kafka topic schema is handled in the feed adapter without the client needing updates. The BFF also handles authentication (JWT validation), data transformation (unit conversion, formatting), and aggregation (combining data from multiple services into a single response). Trade-off: the BFF adds a network hop and potential bottleneck; mitigated by horizontal scaling of the BFF service.

- **GraphQL for flexible data fetching over REST:** The monitoring dashboard displays many different views (feed, metrics, charts, alerts, config) with varying data requirements. GraphQL allows the client to request exactly the data it needs for a given view, reducing over-fetching and under-fetching. The adapter implements resolvers that map GraphQL queries to internal service calls. Trade-off: GraphQL requires schema management and resolver complexity; simple REST endpoints would be faster for fixed views like the live feed.

- **Unified error handling with structured errors over ad-hoc error codes:** All adapter services return errors in a consistent format: `{ code: string; message: string; details?: unknown; retryable: boolean }`. The client has a global error handler that maps error codes to user-facing messages and retry logic. Non-retryable errors (permission denied, not found) show an error state; retryable errors (timeout, service unavailable) trigger automatic retry with exponential backoff. Trade-off: the structured error format adds overhead to every response, but ensures predictable error handling across the entire dashboard.

## Implementation Approach

```typescript
// === Adapter Service Interfaces ===

interface IFeedAdapter {
  getActiveCalls(tenantId: string, filters: FeedFilter): Promise<LiveCallFeedEvent[]>;
  subscribeToFeed(tenantId: string, filters: FeedFilter): AsyncIterable<LiveCallFeedEvent>;
  executeAction(callSid: string, action: SupervisorAction, params: Record<string, string>, userId: string): Promise<void>;
}

interface IMetricsAdapter {
  getWidgetData(tenantId: string, widgetConfig: MetricWidgetConfig): Promise<MetricValue>;
  getChartData(tenantId: string, chartConfig: ChartConfig, timeRange: TimeRange): Promise<ChartDataPoint[]>;
  getAvailableMetrics(tenantId: string): Promise<MetricDefinition[]>;
}

interface IAlertsAdapter {
  getAlertRules(tenantId: string): Promise<AlertRule[]>;
  createAlertRule(rule: Omit<AlertRule, 'id' | 'createdAt' | 'updatedAt'>): Promise<AlertRule>;
  getActiveAlerts(tenantId: string): Promise<AlertInstance[]>;
  acknowledgeAlert(alertId: string, userId: string): Promise<void>;
  getAlertHistory(tenantId: string, timeRange: TimeRange, filters?: AlertHistoryFilter): Promise<AlertInstance[]>;
}

interface IConfigAdapter {
  getDashboards(tenantId: string, userId: string): Promise<DashboardSummary[]>;
  getDashboard(dashboardId: string, userId: string): Promise<DashboardConfig>;
  saveDashboard(config: DashboardConfig, userId: string): Promise<void>;
  cloneDashboard(sourceId: string, name: string, userId: string): Promise<DashboardConfig>;
  shareDashboard(dashboardId: string, userId: string, targetUserId: string, role: 'viewer' | 'editor'): Promise<void>;
}

// === BFF Gateway Implementation ===

class DashboardBffGateway {
  private feedAdapter: IFeedAdapter;
  private metricsAdapter: IMetricsAdapter;
  private alertsAdapter: IAlertsAdapter;
  private configAdapter: IConfigAdapter;
  private cache: CacheManager;

  constructor() {
    this.feedAdapter = new FeedAdapter();
    this.metricsAdapter = new MetricsAdapter();
    this.alertsAdapter = new AlertsAdapter();
    this.configAdapter = new ConfigAdapter();
    this.cache = new CacheManager({ ttl: 5000 }); // 5-second cache
  }

  // GraphQL resolvers
  resolvers = {
    Query: {
      activeCalls: async (_: unknown, args: { filters: FeedFilter }, context: Context) => {
        this.requirePermission(context, 'monitoring:live-feed');
        return this.feedAdapter.getActiveCalls(context.tenantId, args.filters);
      },

      widgetData: async (_: unknown, args: { widgetConfig: MetricWidgetConfig }, context: Context) => {
        this.requirePermission(context, 'monitoring:metrics');
        const cacheKey = `widget:${context.tenantId}:${args.widgetConfig.id}`;
        return this.cache.wrap(cacheKey, () =>
          this.metricsAdapter.getWidgetData(context.tenantId, args.widgetConfig)
        );
      },

      dashboards: async (_: unknown, __: unknown, context: Context) => {
        return this.configAdapter.getDashboards(context.tenantId, context.userId);
      },

      activeAlerts: async (_: unknown, __: unknown, context: Context) => {
        this.requirePermission(context, 'monitoring:alerts');
        return this.alertsAdapter.getActiveAlerts(context.tenantId);
      },
    },

    Mutation: {
      executeAction: async (_: unknown, args: { callSid: string; action: string; params: Record<string, string> }, context: Context) => {
        this.requirePermission(context, 'calls:manage');
        return this.feedAdapter.executeAction(
          args.callSid,
          args.action as SupervisorAction,
          args.params,
          context.userId
        );
      },

      acknowledgeAlert: async (_: unknown, args: { alertId: string }, context: Context) => {
        this.requirePermission(context, 'monitoring:alerts');
        return this.alertsAdapter.acknowledgeAlert(args.alertId, context.userId);
      },

      saveDashboard: async (_: unknown, args: { config: DashboardConfig }, context: Context) => {
        return this.configAdapter.saveDashboard(args.config, context.userId);
      },
    },

    Subscription: {
      liveFeed: {
        subscribe: async function* (_: unknown, args: { filters: FeedFilter }, context: Context) {
          this.requirePermission(context, 'monitoring:live-feed');
          for await (const event of this.feedAdapter.subscribeToFeed(context.tenantId, args.filters)) {
            yield { liveFeed: event };
          }
        },
      },
    },
  };

  private requirePermission(context: Context, permission: string): void {
    if (!context.permissions.includes(permission)) {
      throw new BffError('FORBIDDEN', 'You do not have permission to perform this action', null, false);
    }
  }
}

// Structured error types
class BffError extends Error {
  constructor(
    public code: string,
    message: string,
    public details: unknown = null,
    public retryable: boolean = false
  ) {
    super(message);
    this.name = 'BffError';
  }
}

// Retry wrapper for retryable operations
async function withRetry<T>(
  fn: () => Promise<T>,
  maxRetries: number = 3,
  baseDelay: number = 200
): Promise<T> {
  let lastError: Error | null = null;
  for (let i = 0; i < maxRetries; i++) {
    try {
      return await fn();
    } catch (err) {
      lastError = err as Error;
      if (!(err instanceof BffError) || !err.retryable) throw err;
      await new Promise(resolve => setTimeout(resolve, baseDelay * Math.pow(2, i)));
    }
  }
  throw lastError;
}
```

## Open-Source Tools

| Tool | License | Purpose |
|------|---------|---------|
| Apollo Server (MIT) | Server | GraphQL BFF gateway |
| GraphQL Yoga (MIT) | Server | Alternative GraphQL server |
| DataLoader (MIT) | Server | Batching/caching GraphQL resolvers |
| Redis (RSAL) | Server | Response caching layer |

## Production Considerations

**Scaling:** The BFF gateway is stateless and scales horizontally behind a load balancer. Each instance maintains its own Redis cache client. Use DataLoader to batch and cache GraphQL resolver calls within a single request — this reduces the number of upstream service calls by 60% for dashboard page loads. For subscription-based resolvers (live feed, alert updates), use the WebSocket gateway integration described in Section 05 rather than long-polling.

**Security:** The BFF gateway is the authentication and authorization boundary. All GraphQL queries and mutations are rejected unless the JWT is valid and the required permission is present. Implement query depth limiting (max 5 levels) and query cost analysis to prevent malicious GraphQL queries from overloading upstream services. The BFF strips sensitive fields (PII, internal IDs) from responses if the user lacks the appropriate permission.

**Monitoring:** Track BFF request rate, p50/p95/p99 response time per resolver, cache hit rate, and error rate by error code. Alert if p95 response time exceeds 500 ms or if error rate exceeds 5%. Monitor upstream service health through the BFF — if an upstream service becomes unavailable, the BFF returns a degraded response (cached data with a "stale" marker) rather than failing the entire dashboard load.
