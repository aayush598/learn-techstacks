# Section 08: Webhook Dashboard and Monitoring

## Overview

The Webhook Dashboard provides operational visibility into the webhook delivery system, enabling platform administrators and tenant customers to monitor delivery health, inspect delivery logs, manage endpoints, and diagnose delivery failures. The dashboard surfaces real-time and historical metrics: delivery volume, success rates, latency percentiles, retry distribution, DLQ contents, and endpoint health status.

The monitoring subsystem collects metrics from every stage of the webhook pipeline: event emission, queue enqueue, delivery attempt, and consumer response. These metrics feed into the platform's observability stack and are exposed through the dashboard API and Grafana dashboards. The system also provides alerting based on configurable thresholds — delivery success rate drops, DLQ growth, endpoint health degradation — with notifications routed through the platform's notification system (email, Slack, PagerDuty).

## Architecture

```
              Webhook Dashboard & Monitoring

   Webhook Engine → Metrics Collector → Dashboard API → UI
                        |
   +----------------------------------------------------------+
   |              Monitoring Architecture                     |
   |                                                          |
   |  +------------------+  +-------------------+            |
   |  | Metrics Pipeline |  | Dashboard API     |            |
   |  | • Delivery count |  | • Real-time stats |            |
   |  | • Success/fail   |  | • Endpoint list   |            |
   |  | • Latency        |  | • Delivery logs   |            |
   |  | • DLQ size       |  | • DLQ browser     |            |
   |  +------------------+  +-------------------+            |
   |  +------------------+  +-------------------+            |
   |  | Alerting Engine  |  | Health Checks     |             |
   |  | • Threshold-based|  | • Endpoint ping   |            |
   |  | • Anomaly detect |  | • Certificate     |            |
   |  | • Slack/Email    |  |   expiry          |            |
   |  | • PagerDuty      |  | • DNS resolution  |            |
   |  +------------------+  +-------------------+            |
   |  +------------------+  +-------------------+            |
   |  | Reporting        |  | Audit Log         |             |
   |  | • Daily summary  |  | • Config changes  |            |
   |  | • SLA compliance |  | • Endpoint ops    |            |
   |  | • Endpoint perf  |  | • Replay activity |            |
   |  +------------------+  +-------------------+            |
   +----------------------------------------------------------+
```

## Design Decisions

- **Count-min-sketch for high-cardinality metrics over exact counts:** For per-endpoint metrics at scale (thousands of endpoints emitting millions of events), exact counters are expensive to store and query. The monitoring system uses count-min-sketch data structures for high-cardinality metric dimensions (per-endpoint success counts, error code distributions) and exact counters only for aggregate metrics (total deliveries, DLQ total). Trade-off: count-min-sketch has probabilistic error (small overcounts) but uses constant memory regardless of cardinality.

- **Push-based metrics from webhook workers over pull-based scraping:** Webhook workers push metrics to a central metrics collector (Prometheus Pushgateway, StatsD) after each delivery attempt. This avoids the complexity of pull-based scraping in an ephemeral worker environment (workers may live only seconds). The metrics collector aggregates and exposes the data for Prometheus scraping. Trade-off: push-based requires managing a Pushgateway component but works reliably with short-lived worker processes.

- **SLA tracking by tenant and endpoint type over platform-wide aggregate:** The monitoring system tracks delivery SLAs at the tenant and endpoint level. Each endpoint has a configured SLA target (e.g., 99.9% delivery success within 60 seconds). The SLA engine evaluates compliance on a rolling 30-day window. Dashboard views show per-tenant SLA compliance, sorted by compliance level. Trade-off: per-endpoint SLA tracking requires more storage but enables customer-specific reporting and problem identification.

## Implementation Approach

```
interface DeliveryMetric {
  endpointId: string;
  tenantId: string;
  eventType: string;
  status: 'delivered' | 'failed' | 'retried' | 'dlq';
  statusCode?: number;
  latencyMs: number;
  attemptNumber: number;
  timestamp: Date;
}

interface WebhookDashboardStats {
  totalDelivered: number;
  totalFailed: number;
  successRate: number;
  avgLatencyMs: number;
  p95LatencyMs: number;
  p99LatencyMs: number;
  retryCount: number;
  dlqCount: number;
  activeEndpoints: number;
  periodStart: Date;
  periodEnd: Date;
}

class MetricsCollector {
  private counters = new Map<string, number>();
  private latencies = new Map<string, number[]>();
  private sketch: CountMinSketch;

  recordDelivery(metric: DeliveryMetric): void {
    const key = `${metric.endpointId}:${metric.status}`;

    // Exact counter (bounded cardinality)
    this.counters.set(key, (this.counters.get(key) || 0) + 1);

    // Latency tracking (sampled at 10% for long-tail accuracy)
    if (metric.status === 'delivered' && Math.random() < 0.1) {
      const latencies = this.latencies.get(metric.endpointId) || [];
      latencies.push(metric.latencyMs);
      if (latencies.length > 1000) latencies.shift(); // Keep last 1000
      this.latencies.set(metric.endpointId, latencies);
    }

    // Count-min-sketch for high-cardinality dimensions
    this.sketch.increment(`error:${metric.statusCode}`, 1);
    this.sketch.increment(`event_type:${metric.eventType}`, 1);

    // Push to Prometheus Pushgateway
    this.pushToPrometheus(metric);
  }

  getEndpointStats(endpointId: string, timeframeMs: number): WebhookDashboardStats {
    const delivered = this.counters.get(`${endpointId}:delivered`) || 0;
    const failed = this.counters.get(`${endpointId}:failed`) || 0;
    const total = delivered + failed;

    const latencies = this.latencies.get(endpointId) || [];
    const sortedLatencies = [...latencies].sort((a, b) => a - b);

    return {
      totalDelivered: delivered,
      totalFailed: failed,
      successRate: total > 0 ? (delivered / total) * 100 : 100,
      avgLatencyMs: latencies.length > 0 ? latencies.reduce((a, b) => a + b, 0) / latencies.length : 0,
      p95LatencyMs: sortedLatencies[Math.floor(sortedLatencies.length * 0.95)] || 0,
      p99LatencyMs: sortedLatencies[Math.floor(sortedLatencies.length * 0.99)] || 0,
      retryCount: this.counters.get(`${endpointId}:retried`) || 0,
      dlqCount: this.counters.get(`${endpointId}:dlq`) || 0,
      activeEndpoints: this.getActiveEndpointCount(),
      periodStart: new Date(Date.now() - timeframeMs),
      periodEnd: new Date(),
    };
  }
}

class AlertingEngine {
  private rules: AlertRule[];

  constructor(rules: AlertRule[]) {
    this.rules = rules;
  }

  async evaluate(metrics: MetricsCollector): Promise<Alert[]> {
    const alerts: Alert[] = [];

    for (const rule of this.rules) {
      const value = await rule.evaluate(metrics);
      if (value !== undefined) {
        alerts.push({
          ruleId: rule.id,
          severity: rule.severity,
          message: rule.formatMessage(value),
          value,
          threshold: rule.threshold,
          timestamp: new Date(),
        });
      }
    }

    return alerts;
  }
}

// Default alert rules
const DEFAULT_ALERT_RULES: AlertRule[] = [
  {
    id: 'delivery_success_rate',
    severity: 'critical',
    threshold: 90,
    evaluate: async (metrics) => {
      const stats = metrics.getEndpointStats('*', 300000); // 5 min window
      return stats.successRate < 90 ? stats.successRate : undefined;
    },
    formatMessage: (value: number) => `Webhook delivery success rate dropped to ${value.toFixed(1)}%`,
  },
  {
    id: 'dlq_growth',
    severity: 'warning',
    threshold: 100,
    evaluate: async (metrics) => {
      const dlqCount = metrics.getTotalDLQCount();
      return dlqCount > 100 ? dlqCount : undefined;
    },
    formatMessage: (value: number) => `DLQ contains ${value} undelivered events`,
  },
  {
    id: 'endpoint_health',
    severity: 'critical',
    threshold: 0,
    evaluate: async (metrics) => {
      // Check endpoints that have been failing for > 1 hour
      const unhealthyEndpoints = await getUnhealthyEndpoints(60);
      return unhealthyEndpoints.length > 0 ? unhealthyEndpoints.length : undefined;
    },
    formatMessage: (value: number) => `${value} webhook endpoints unhealthy for > 1 hour`,
  },
  {
    id: 'delivery_latency_p99',
    severity: 'warning',
    threshold: 30000,
    evaluate: async (metrics) => {
      const stats = metrics.getEndpointStats('*', 300000);
      return stats.p99LatencyMs > 30000 ? stats.p99LatencyMs : undefined;
    },
    formatMessage: (value: number) => `Webhook p99 delivery latency is ${(value / 1000).toFixed(1)}s`,
  },
];

// Dashboard API endpoint handler
async function dashboardHandler(req: Request, res: Response) {
  const { tenantId, endpointId, timeframe = '1h' } = req.query;
  const timeframeMs = parseTimeframe(timeframe as string);

  const metrics = await metricsCollector.getEndpointStats(
    endpointId as string || '*',
    timeframeMs
  );

  const dlqEvents = endpointId
    ? await dlq.getDLQEvents(endpointId as string, { limit: 20 })
    : { events: [], total: 0 };

  const endpoint = endpointId
    ? await db.webhookEndpoints.find(endpointId as string)
    : null;

  res.json({
    stats: metrics,
    dlq: dlqEvents,
    endpoint,
    timeframe,
  });
}
```

## Open-Source Tools

| Tool | License | Purpose |
|------|---------|---------|
| Prometheus (Apache 2.0) | Server | Metrics storage + alerting |
| Grafana (AGPL 3.0) | UI | Dashboard visualization |
| Pushgateway (Apache 2.0) | Metrics | Worker metric aggregation |
| Count-min-sketch (MIT) | Node.js | High-cardinality counting |

## Production Considerations

**Scaling:** The metrics pipeline must handle the peak webhook throughput without introducing latency. Metrics collection is non-blocking — worker threads push metrics asynchronously after responding to the delivery. Metrics data retention follows tiers: raw metrics for 7 days, 1-minute aggregates for 30 days, 1-hour aggregates for 1 year. Use Prometheus TSDB for short-term storage and Thanos/Cortex for long-term aggregation and multi-tenant isolation.

**Security:** Dashboard access must be authenticated and authorized by role (admin sees all endpoints, tenant sees only their own). Never expose endpoint secrets in the dashboard UI — mask secrets and show only the last 4 characters. Dashboard API responses should not include internal error details (stack traces, internal IPs). Audit log all dashboard operations (viewing DLQ, replaying events, modifying endpoints).

**Monitoring:** Monitor the monitoring system — track metrics pipeline lag (event time to metric availability), dashboard API response times, alert evaluation latency, and Prometheus TSDB health. Alert on monitoring pipeline lag exceeding 60 seconds (indicates metrics collection bottleneck) and dashboard API error rate exceeding 1%. Set up synthetic monitoring that periodically sends a test webhook and verifies end-to-end delivery and metric recording.
