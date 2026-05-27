# Section 05: Performance Baselines

## Overview

Performance baselines establish expected performance characteristics at various load levels. Each baseline captures key metrics at specific concurrency levels: response times (p50, p95, p99), throughput, error rates, resource utilization, and platform-specific metrics (STT latency, TTS first byte, call completion rate). Baselines are versioned alongside releases.

## Design Decisions

- **Versioned Baselines**: Each version has associated baselines
- **Multi-Level**: Baselines at different concurrency levels
- **Statistical Significance**: Based on multiple test runs
- **Regression Gates**: CI compares against baselines to block regressions

## Implementation Approach

```typescript
interface PerformanceBaseline {
  version: string; capturedAt: Date; environment: string;
  metrics: {
    concurrency: number;
    responseTime: { p50: number; p95: number; p99: number };
    throughput: number; errorRate: number;
    sttLatency: { p50: number; p95: number };
    llmLatency: { p50: number; p95: number };
    ttsLatency: { p50: number; p95: number };
  }[];
}

class BaselineManager {
  async captureBaseline(version: string): Promise<PerformanceBaseline> {
    const scenarios = [50, 100, 200, 300];
    const results = [];
    for (const concurrency of scenarios) {
      const result = await this.runLoadTest({ targetConcurrency: concurrency, duration: '5m' });
      results.push({
        concurrency,
        responseTime: { p50: result.metrics.http_req_duration.values['p(50)'], p95: result.metrics.http_req_duration.values['p(95)'], p99: result.metrics.http_req_duration.values['p(99)'] },
        throughput: result.metrics.http_reqs.rate,
        errorRate: result.metrics.errors.rate,
        sttLatency: { p50: result.metrics.stt_latency_ms.values['p(50)'], p95: result.metrics.stt_latency_ms.values['p(95)'] },
        llmLatency: { p50: result.metrics.llm_latency_ms.values['p(50)'], p95: result.metrics.llm_latency_ms.values['p(95)'] },
        ttsLatency: { p50: result.metrics.tts_latency_ms.values['p(50)'], p95: result.metrics.tts_latency_ms.values['p(95)'] },
      });
    }
    const baseline: PerformanceBaseline = { version, capturedAt: new Date(), environment: process.env.NODE_ENV || 'staging', metrics: results };
    await this.store(baseline);
    return baseline;
  }

  async compareWithBaseline(current: PerformanceBaseline, baselineId: string): Promise<BaselineComparison> {
    const baseline = await this.load(baselineId);
    const regressions = [];
    for (const currMetric of current.metrics) {
      const baseMetric = baseline.metrics.find(m => m.concurrency === currMetric.concurrency);
      if (!baseMetric) continue;
      const change = ((currMetric.responseTime.p95 - baseMetric.responseTime.p95) / baseMetric.responseTime.p95) * 100;
      if (change > 10) regressions.push({ metric: 'p95_response_time', concurrency: currMetric.concurrency, baseline: baseMetric.responseTime.p95, current: currMetric.responseTime.p95, changePercent: change });
    }
    return { baseline: baselineId, current: current.version, hasRegressions: regressions.length > 0, regressions };
  }
}
```

## Integration Points

- **CI Pipeline**: Baselines compared on each deployment
- **Dashboard**: Baseline trends visualized
- **Release Process**: Baseline captured after each release

## Open-Source Tools

- **k6** (AGPL 3.0): Load test execution
- **k6 Cloud** (AGPL 3.0): Baseline comparison
- **InfluxDB** (MIT): Baseline metric storage

## Production Considerations

- **Environment Consistency**: Maintain per-environment baselines
- **Baseline Expiry**: Refresh baselines regularly
