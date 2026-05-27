# Section 07: Integration Health Monitoring

## Overview

Integration health monitoring provides real-time visibility into the operational status of every external system connection, enabling proactive detection and response to integration failures. The monitoring system tracks connection status (connected, degraded, disconnected), error rates, latency trends, rate limit utilization, authentication status, and data synchronization freshness. It provides both real-time dashboards for operations teams and automated alerting for critical issues.

Health monitoring operates at multiple levels: individual integration check (is the Salesforce adapter working?), integration category (are all CRM integrations healthy?), tenant-level (are all of tenant A's integrations working?), and platform-level (what is the overall health of the integration ecosystem?). Each level provides different stakeholders with the appropriate granularity. The system performs active health checks (periodic API calls to test endpoints) and passive health monitoring (analysis of real traffic patterns to detect degradation).

## Architecture

```
                  Integration Health Monitoring Architecture

   +------------------------------------------------------+
   |              Health Monitoring Service                |
   |                                                      |
   |  Active Checks:         Passive Monitoring:          |
   |  +------------------+  +-------------------------+   |
   |  | Health Check     |  | Error Rate Analysis     |   |
   |  | Scheduler        |  | • Per-integration       |   |
   |  | • Periodic       |  | • Per-endpoint          |   |
   |  | • On-demand      |  | • Per-tenant            |   |
   |  | • Custom         |  |                         |   |
   |  +------------------+  +-------------------------+   |
   |  +------------------+  +-------------------------+   |
   |  | Latency Monitor  |  | Sync Freshness          |   |
   |  | • p50/p95/p99    |  | • Last successful sync  |   |
   |  | • Trend analysis |  | • Sync lag              |   |
   |  | • Anomaly detect |  | • Queue depth           |   |
   |  +------------------+  +-------------------------+   |
   |                                                      |
   |  Output:                                              |
   |  - Health scores (0-100) per integration/tenant       |
   |  - Status: Healthy / Degraded / Unhealthy / Unknown   |
   |  - Alerts via webhook, email, Slack                   |
   |  - Dashboards via Grafana                             |
   +------------------------------------------------------+
```

## Design Decisions

- **Composite health score with weighted sub-scores over binary status:** Each integration gets a composite health score (0-100) calculated from availability (40% weight), latency (25%), error rate (20%), and data freshness (15%). This provides a nuanced view — an integration might have perfect availability but degrading latency, resulting in a score of 85/100 ("degraded"). Binary status (up/down) misses these leading indicators. Trade-off: composite scores require careful calibration of weights and thresholds.

- **Active + passive monitoring hybrid over either alone:** Active health checks (periodic API pings) provide proactive detection of outages but add load to external APIs and may be blocked. Passive monitoring (analysis of real traffic) has zero additional API cost but requires traffic to detect issues. The hybrid approach uses active checks for low-traffic integrations (ensuring baseline coverage) and passive monitoring for high-traffic integrations (where traffic provides sufficient signal). Trade-off: hybrid monitoring requires maintaining two monitoring pipelines.

- **Anomaly detection with dynamic baselines over static thresholds:** Latency and error rate baselines are learned automatically from historical data (rolling 7-day window) rather than configured as static thresholds. Deviations beyond 3 standard deviations from the baseline trigger alerts. This adapts to normal variations (higher latency during business hours, lower on weekends) without manual threshold tuning. Trade-off: dynamic baselines require 2-3 weeks of data before they become accurate and can be fooled by gradual degradation.

## Implementation Approach

```
interface IntegrationHealth {
  integrationId: string;
  tenantId: string;
  status: 'healthy' | 'degraded' | 'unhealthy' | 'unknown';
  score: number;
  components: {
    availability: { score: number; status: string; lastChecked: number; uptimePercent: number };
    latency: { score: number; status: string; p50: number; p95: number; p99: number };
    errors: { score: number; status: string; errorRate: number; topErrors: { type: string; count: number }[] };
    freshness: { score: number; status: string; lastSync: number; syncLag: number };
  };
  alerts: HealthAlert[];
  lastUpdated: number;
}

class HealthMonitor {
  constructor(
    private activeChecker: ActiveHealthChecker,
    private passiveMonitor: PassiveHealthMonitor,
    private anomalyDetector: AnomalyDetector
  ) {}

  async getHealth(integrationId: string, tenantId: string): Promise<IntegrationHealth> {
    const [activeResult, passiveMetrics] = await Promise.all([
      this.activeChecker.check(integrationId, tenantId),
      this.passiveMonitor.getMetrics(integrationId, tenantId)
    ]);

    const availability = this.computeAvailability(activeResult, passiveMetrics);
    const latency = this.computeLatencyScore(passiveMetrics);
    const errors = this.computeErrorScore(passiveMetrics);
    const freshness = this.computeFreshness(passiveMetrics);

    const score = availability.score * 0.4 + latency.score * 0.25 +
                  errors.score * 0.2 + freshness.score * 0.15;

    const status = score >= 90 ? 'healthy' : score >= 70 ? 'degraded' : 'unhealthy';

    return {
      integrationId, tenantId, status, score,
      components: { availability, latency, errors, freshness },
      alerts: await this.getActiveAlerts(integrationId, tenantId),
      lastUpdated: Date.now()
    };
  }

  private async checkAnomalies(integrationId: string, metrics: PassiveMetrics) {
    const latencyAnomaly = await this.anomalyDetector
      .detect(integrationId, 'latency_p95', metrics.latency.p95);
    if (latencyAnomaly) {
      await this.alertService.send({
        severity: 'warning',
        integrationId,
        metric: 'latency_p95',
        currentValue: metrics.latency.p95,
        baselineValue: latencyAnomaly.baseline,
        deviation: latencyAnomaly.deviation
      });
    }
  }
}
```

## Open-Source Tools

| Tool | License | Purpose |
|------|---------|---------|
| **Prometheus** (Apache 2.0) | Monitoring | Metrics collection |
| **Grafana** (AGPLv3) | Dashboards | Health dashboards |
| **Alertmanager** (Apache 2.0) | Alerting | Alert routing |
| **Elasticsearch** (Elastic) | Logging | Error log aggregation |
| **StatsD** (MIT) | Metrics | Metrics aggregation |

## Production Considerations

**Scaling:** Health check execution must be distributed across worker instances to avoid overloading a single node. Use a work queue (BullMQ) with configurable concurrency. Store health metrics in a time-series database (Prometheus, ClickHouse) with appropriate retention policies (raw data 7 days, aggregated 30 days, summaries 1 year). Health checks to the same integration should be deduplicated when multiple tenants share the same integration instance.

**Security:** Health check endpoints should not expose sensitive integration details (credentials, internal configuration). Health data access should be restricted — tenants should see only their own integration health. Shared integration health (e.g., a shared Salesforce org) should be visible only to platform administrators.

**Monitoring:** The health monitoring system itself requires monitoring — track check execution time, check success rate, alert delivery latency, and monitoring coverage (% of integrations with active checks). Alert when the monitoring system fails to execute checks for more than 5 minutes, as this creates blind spots.
