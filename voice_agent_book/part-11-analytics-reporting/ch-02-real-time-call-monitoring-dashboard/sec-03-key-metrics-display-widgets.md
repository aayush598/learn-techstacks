# Section 03: Key Metrics Display Widgets

## Overview

The key metrics display widgets provide at-a-glance operational statistics for the contact center. These widgets — rendered as configurable cards, gauges, and sparklines — show real-time and rolling-window values for metrics such as calls in queue, longest wait time, active agents, call completion rate, and average sentiment. Each widget subscribes to a dedicated Redis channel or WebSocket topic, updating automatically as new data arrives from the stream processing layer.

The widgets are designed for flexibility: supervisors can rearrange them on the dashboard (drag-and-drop), resize them, and configure the time window (last 5 minutes, last hour, or a custom range). The backend serves metric definitions from a configuration store, enabling operators to add custom metrics without deploying new code. Widgets degrade gracefully if their data source is unavailable — showing the last known value with a stale indicator instead of an error state.

## Architecture

```
              Key Metrics Widget System

   Stream Processor → Aggregator (Redis Time Series)
                            |
              Metrics API → WebSocket Gateway
                            |
            Dashboard Widget Grid (React Grid Layout)
                            |
    +-------+-------+-------+
    | Queue | Wait  | Agents|
    | Count | Time  | Online|
    +-------+-------+-------+
    | Call  | Sent  | Longest|
    | Rate  | Avg   | Call  |
    +-------+-------+-------+
```

## Design Decisions

- **Server-side aggregation in Redis Time Series over client-side computation:** The stream processor writes pre-computed metric snapshots to Redis Time Series every 5 seconds. Widgets fetch these pre-computed values rather than raw events. This reduces client computation to zero and ensures all users see consistent values. Trade-off: the 5-second aggregation window introduces a slight delay, and some metrics (like "calls in the last 1 minute") require server-side tumbling windows rather than exact counts.

- **Metric definitions as configuration over hardcoded widgets:** Each widget is defined by a JSON configuration (metric name, aggregation function, time window, comparison period, visualization type) stored in PostgreSQL. The dashboard fetches the layout and metric configs on load, rendering widgets dynamically. Operators can create new widgets through an admin UI without redeployment. Trade-off: dynamic widgets have a steeper performance optimization path; some complex visualizations require custom React components.

- **Stale-while-revalidate caching over real-time-only updates:** Widgets cache the last received metric value in the browser's state management store (Zustand). When reconnecting after a disconnect, widgets immediately display the cached value (marked as "cached") while the WebSocket reconnects and fetches fresh data. This prevents blank widgets during brief network interruptions. Trade-off: the cached value may be up to 30 seconds old, which could mislead operators who don't notice the stale indicator.

## Implementation Approach

```typescript
interface MetricWidgetConfig {
  id: string;
  title: string;
  metricKey: string;           // e.g., 'calls.in_queue'
  aggregation: 'latest' | 'avg' | 'sum' | 'min' | 'max';
  timeWindow: number;          // seconds (300 = 5 min, 3600 = 1 hour)
  comparisonWindow?: number;   // previous period for delta display
  visualization: 'number' | 'gauge' | 'sparkline' | 'progress';
  threshold: { warning: number; critical: number; direction: 'above' | 'below' };
  format: 'integer' | 'decimal' | 'duration' | 'percentage';
}

interface MetricValue {
  metricKey: string;
  value: number;
  timestamp: number;
  windowStart: number;
  windowEnd: number;
  comparedTo?: number;  // previous period value for delta
  status: 'fresh' | 'stale' | 'error';
}

class MetricsAggregator {
  private redisTs: RedisTimeSeries;

  async aggregate(tenantId: string, windowSeconds: number): Promise<void> {
    const now = Date.now();
    const windowStart = now - windowSeconds * 1000;

    // Query stream processor output
    const rawMetrics = await this.queryStreamAggregates(tenantId, windowStart);

    // Write to Redis Time Series
    for (const [key, value] of Object.entries(rawMetrics)) {
      await this.redisTs.add(
        `ts:${tenantId}:${key}`,
        value as number,
        now,
        { labels: { tenantId, metric: key } }
      );
    }
  }

  async getWidgetData(
    tenantId: string,
    config: MetricWidgetConfig
  ): Promise<MetricValue> {
    const key = `ts:${tenantId}:${config.metricKey}`;

    // Get current value
    const current = await this.redisTs.get(key, {
      aggregation: config.aggregation as 'avg' | 'sum',
      timeBucket: config.timeWindow * 1000,
    });

    // Get comparison value if configured
    let comparedTo: number | undefined;
    if (config.comparisonWindow) {
      const past = await this.redisTs.get(key, {
        aggregation: config.aggregation as 'avg' | 'sum',
        timeBucket: config.comparisonWindow * 1000,
      });
      comparedTo = past?.value;
    }

    return {
      metricKey: config.metricKey,
      value: current?.value ?? 0,
      timestamp: current?.timestamp ?? Date.now(),
      windowStart: Date.now() - config.timeWindow * 1000,
      windowEnd: Date.now(),
      comparedTo,
      status: current ? 'fresh' : 'error',
    };
  }
}

// Metric widget React component
const MetricWidget: React.FC<{
  config: MetricWidgetConfig;
  data: MetricValue | null;
}> = ({ config, data }) => {
  const displayValue = formatMetricValue(data?.value ?? 0, config.format);
  const delta = data?.comparedTo != null
    ? ((data.value - data.comparedTo) / data.comparedTo) * 100
    : null;

  return (
    <div className={`metric-widget ${data?.status ?? 'loading'}`}>
      <WidgetHeader title={config.title} status={data?.status} />
      <div className="metric-value-container">
        <span className="metric-value">{displayValue}</span>
        {delta != null && (
          <DeltaBadge value={delta} direction={config.threshold.direction} />
        )}
      </div>
      <Sparkline data={sparklineData} />
      <ThresholdBar value={data?.value ?? 0} config={config.threshold} />
    </div>
  );
};

// Comparison delta calculation
function computeDelta(current: number, previous: number): number {
  if (previous === 0) return 0;
  return ((current - previous) / previous) * 100;
}
```

## Open-Source Tools

| Tool | License | Purpose |
|------|---------|---------|
| RedisTimeSeries (RSAL) | Server | Time-series metric storage |
| React Grid Layout (MIT) | Client | Drag-and-drop widget grid |
| Zustand (MIT) | Client | State management with caching |
| Recharts / Nivo (MIT) | Client | Sparkline charts |

## Production Considerations

**Scaling:** RedisTimeSeries data points should have a retention policy — keep raw 5-second data for 7 days, roll up to 1-minute averages for 30 days, and 1-hour averages for 1 year. Use RedisTimeSeries compaction rules to auto-rollup. Widget polling should use WebSocket push rather than HTTP polling to minimize latency and server load. For dashboards with 50+ widgets per user, batch metric fetches into a single multi-get Redis command.

**Security:** Metric access is scoped to tenant ID — the aggregation key includes `ts:{tenantId}:{metric}` and the API validates that the requesting user belongs to that tenant. Threshold values (warning/critical) are stored per-tenant and can be customized by supervisors. Prevent metric injection attacks by validating metric keys against a whitelist defined in the configuration store.

**Monitoring:** Track widget render time (should be < 50 ms), WebSocket message size per widget, and stale widget count. Alert if more than 10% of widgets on any dashboard are in "stale" state — this indicates a stream processing or Redis connectivity issue. Monitor RedisTimeSeries memory usage per tenant and set max memory policies.
