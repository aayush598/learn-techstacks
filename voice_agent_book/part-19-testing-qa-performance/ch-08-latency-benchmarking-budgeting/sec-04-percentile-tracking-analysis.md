# Section 04: Percentile Tracking & Analysis

## Overview

Percentile tracking focuses on tail latency (p95, p99) rather than averages, as average latency masks poor experiences for a subset of users. The system tracks latency percentiles across multiple dimensions: pipeline stage, agent, region, time of day, and customer tier. Percentile data drives optimization priorities.

## Implementation Approach

```typescript
class PercentileTracker {
  private observations: Map<string, number[]> = new Map();

  record(key: string, value: number): void {
    if (!this.observations.has(key)) this.observations.set(key, []);
    this.observations.get(key)!.push(value);
  }

  getPercentile(key: string, percentile: number): number {
    const values = this.observations.get(key);
    if (!values || values.length === 0) return 0;
    const sorted = [...values].sort((a, b) => a - b);
    const index = Math.ceil((percentile / 100) * sorted.length) - 1;
    return sorted[index];
  }

  getSummary(key: string): PercentileSummary {
    return {
      p50: this.getPercentile(key, 50),
      p75: this.getPercentile(key, 75),
      p90: this.getPercentile(key, 90),
      p95: this.getPercentile(key, 95),
      p99: this.getPercentile(key, 99),
      count: this.observations.get(key)?.length || 0,
    };
  }

  getTailLatency(key: string): number {
    const p99 = this.getPercentile(key, 99);
    const p50 = this.getPercentile(key, 50);
    return p99 - p50; // Higher = worse tail behavior
  }
}

// Usage
const tracker = new PercentileTracker();
for (const call of completedCalls) {
  tracker.record('e2e_latency', call.latency);
  tracker.record(`stt_latency.${call.region}`, call.sttLatency);
}
const summary = tracker.getSummary('e2e_latency');
console.log(`P50: ${summary.p50}, P95: ${summary.p95}, P99: ${summary.p99}`);
```

## Integration Points

- **Prometheus**: Histogram metrics for percentile calculations
- **Grafana**: Heatmaps showing latency distribution over time
- **Alerting**: P95 exceeding budget triggers alerts
- **Capacity Planning**: Tail latency drives scaling decisions

## Open-Source Tools

- **Prometheus Histograms**: Native percentile calculation
- **HDR Histogram** (BSD-2): High Dynamic Range histogram
- **Grafana Heatmap**: Visual latency distribution

## Production Considerations

- **Statistical Significance**: Percentiles need sufficient data points
- **Aggregation Method**: Prometheus histograms use approximated percentiles
- **Windowing**: Use rolling windows for up-to-date percentile tracking
