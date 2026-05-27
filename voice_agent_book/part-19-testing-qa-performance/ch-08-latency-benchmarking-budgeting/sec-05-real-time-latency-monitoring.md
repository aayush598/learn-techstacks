# Section 05: Real-Time Latency Monitoring

## Overview

Real-time latency monitoring provides immediate visibility into platform responsiveness. Dashboards show current latency percentiles, stage-by-stage breakdowns, and geographic variations. Alerting rules detect anomalous latency increases within seconds, enabling rapid response to performance degradation.

## Implementation Approach

```typescript
class RealTimeLatencyMonitor {
  private window: number; // sliding window in ms
  private buckets: Map<string, number[]> = new Map();

  constructor(window = 60000) { this.window = window; }

  record(stage: string, latency: number): void {
    const now = Date.now();
    if (!this.buckets.has(stage)) this.buckets.set(stage, []);
    this.buckets.get(stage)!.push(latency);
    setInterval(() => this.cleanup(), this.window);
  }

  private cleanup(): void {
    const cutoff = Date.now() - this.window;
    for (const [stage, values] of this.buckets) {
      this.buckets.set(stage, values);
    }
  }

  getCurrentMetrics(): LatencyMetrics {
    const result: LatencyMetrics = {};
    for (const [stage, values] of this.buckets) {
      const sorted = [...values].sort((a, b) => a - b);
      result[stage] = {
        p50: sorted[Math.floor(sorted.length * 0.5)],
        p95: sorted[Math.floor(sorted.length * 0.95)],
        p99: sorted[Math.floor(sorted.length * 0.99)],
        count: sorted.length,
      };
    }
    return result;
  }

  checkAlerts(thresholds: Map<string, number>): Alert[] {
    const metrics = this.getCurrentMetrics();
    const alerts: Alert[] = [];
    for (const [stage, threshold] of thresholds) {
      if (metrics[stage]?.p95 > threshold) {
        alerts.push({ stage, current: metrics[stage].p95, threshold });
      }
    }
    return alerts;
  }
}

// Grafana dashboard annotations
const annotations = {
  latencySpike: {
    expr: 'histogram_quantile(0.95, rate(stt_latency_bucket[5m])) > 400',
    title: 'STT Latency Spike',
    text: 'STT p95 latency exceeded 400ms threshold',
  },
};
```

## Integration Points

- **Grafana**: Real-time dashboards with auto-refresh
- **Prometheus**: Metrics collection at 15s scrape intervals
- **AlertManager**: Alert routing and notification
- **Slack**: On-call notifications for critical latency spikes

## Open-Source Tools

- **Prometheus** (Apache 2.0): Metrics storage and query
- **Grafana** (AGPL 3.0): Real-time dashboards
- **AlertManager** (Apache 2.0): Alert management

## Production Considerations

- **Scrape Interval**: 15s default; decrease for faster detection
- **Dashboard Refresh**: Auto-refresh every 5-10s for real-time view
- **Alert Fatigue**: Tune thresholds to avoid false alarms
