# Section 08: Pacing Metrics & Monitoring

## Overview

Pacing metrics and monitoring provide the observability layer required to understand how well the dialing system is balancing call volume against agent capacity. Without proper pacing metrics, contact centers operate blind — unable to detect when dialing is too aggressive (causing abandoned calls and compliance violations) or too conservative (leaving agents idle and wasting capacity). Key pacing metrics include answered call rate, abandonment rate, agent utilization percentage, service level percentage, average speed of answer, calls per agent per hour, and concurrency utilization across all limit tiers.

These metrics feed both real-time dashboards for operations teams and historical analytics for capacity planning. Real-time monitoring enables immediate corrective actions like adjusting dialing ratios, pausing campaigns, or reassigning agents between campaigns. Historical trend analysis reveals systematic issues like carrier degradation during peak hours, agent pool imbalances across shifts, or campaign-level pacing inefficiencies that require configuration changes. The monitoring system also generates alerts when metrics breach pre-configured thresholds, enabling proactive intervention before compliance or service level violations occur.

## Architecture

```
                    Pacing Metrics Pipeline

   Dialer Events (Dial, Answer, Abandon, Complete, Wait)
              |
              v
   +-----------------------+
   |  Event Ingestion      |  Kafka / Redis Streams
   |  (Real-time)          |  Sub-second latency
   +-----------------------+
        |            |
        v            v
   +----------+  +----------+
   | Real-time |  | Time-    |  ClickHouse / TimescaleDB
   | Counters  |  | Series   |
   | (Redis)   |  | (DB)     |
   +----------+  +----------+
        |            |
        v            v
   +-----------------------+
   |  Metrics Aggregator   |  Rolling windows: 1min, 5min, 15min, 1hr
   |                       |  Calculations: rates, ratios, percentiles
   +-----------------------+
        |            |
        v            v
   +----------+  +----------+
   | Alerting  |  | API/     |  Prometheus + Grafana / Custom Dashboard
   | Engine    |  | Dashboard|
   +----------+  +----------+
```

## Design Decisions

- **Sliding window aggregation over fixed windows for real-time metrics:** Sliding windows (e.g., rolling 5-minute abandonment rate) provide more accurate real-time views than fixed calendar windows. A fixed window can mask a recent spike if it straddles the boundary. Trade-off: sliding windows are computationally more expensive — each metric update requires re-scanning events within the window rather than incrementing a counter.

- **Separate real-time (Redis) and historical (ClickHouse) stores:** Redis counters handle sub-second metric reads for dashboard auto-refresh and alert threshold checks. ClickHouse stores raw events for ad-hoc querying and historical analysis. The dual-store approach prevents expensive analytical queries from impacting real-time dashboard performance. Trade-off: maintaining two stores adds operational complexity and requires careful data consistency verification.

- **Composite metric calculation with configurable weights:** The system computes a composite "pacing health score" from individual metrics (abandonment rate 30%, agent utilization 30%, service level 25%, concurrency utilization 15%). This single score simplifies operational decision-making while allowing drill-down into component metrics. Trade-off: composite scores can mask individual metric problems — a healthy score might conceal a high abandonment rate offset by excellent utilization.

## Implementation Approach

```
interface PacingMetricPoint {
  timestamp: number;
  campaignId: string;
  tenantId: string;
  metrics: {
    answeredRate: number;       // 0.0 - 1.0
    abandonmentRate: number;    // 0.0 - 1.0
    agentUtilization: number;   // 0.0 - 1.0
    serviceLevel: number;       // % answered within threshold
    averageSpeedOfAnswer: number; // seconds
    concurrencyUtilization: number; // % of max
    callsPerAgentPerHour: number;
    avgCallDuration: number;    // seconds
    avgWaitTime: number;        // seconds
  };
}

class PacingMetricsService {
  constructor(redis, clickhouse) {
    this.realtime = redis;
    this.historical = clickhouse;
    this.windowSizes = [60, 300, 900, 3600]; // 1m, 5m, 15m, 1hr
  }

  async recordEvent(event) {
    // Increment real-time counters
    await this.realtime.hIncrBy(
      `pacing:${event.campaignId}:${this.getWindowKey(60)}`,
      event.type, 1
    );
    // Insert into historical store
    await this.historical.insert('pacing_events', event);
    // Check alert thresholds
    await this.evaluateAlerts(event.campaignId);
  }

  async getMetrics(campaignId, windowSize) {
    const raw = await this.realtime.hGetAll(
      `pacing:${campaignId}:${this.getWindowKey(windowSize)}`
    );
    return this.calculateDerivedMetrics(raw);
  }

  calculateDerivedMetrics(raw) {
    const total = raw.dialed || 0;
    const answered = raw.answered || 0;
    const abandoned = raw.abandoned || 0;

    return {
      answeredRate: total > 0 ? answered / total : 0,
      abandonmentRate: answered > 0 ? abandoned / answered : 0,
      // ... additional calculations
    };
  }
}
```

## Open-Source Tools

| Tool | License | Purpose |
|------|---------|---------|
| **Prometheus** (Apache 2.0) | Monitoring | Metrics collection and alerting |
| **Grafana** (AGPLv3) | Dashboards | Real-time pacing dashboards |
| **Redis** (BSD) | Cache | Real-time metric counters |
| **ClickHouse** (Apache 2.0) | Analytics | Historical metric storage |
| **Alertmanager** (Apache 2.0) | Alerting | Threshold-based alert routing |

## Production Considerations

**Scaling:** Real-time metric aggregation must be horizontally scalable. Use Redis Cluster with hash tags to co-locate all metrics for a single campaign on the same node, ensuring atomic increment operations. For ClickHouse, use `AggregatingMergeTree` tables with materialized views for pre-computed window aggregates. Partition pacing events by day and use TTL to automatically expire old data.

**Security:** Pacing metrics should be accessible only to authorized users — multi-tenant isolation requires that tenant A cannot view pacing data for tenant B. Implement row-level security in ClickHouse using tenant_id filtering. Dashboard API endpoints must validate tenant access tokens.

**Monitoring:** The monitoring system itself must be monitored — tracking Redis latency for real-time counters, ClickHouse query performance for metrics aggregation, and alert delivery latency. Define SLOs for metric freshness (p99 metrics delay under 2 seconds for real-time views) and dashboard load time (p95 under 500ms).
