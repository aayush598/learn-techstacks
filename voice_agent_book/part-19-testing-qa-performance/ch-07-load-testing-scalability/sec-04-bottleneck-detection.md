# Section 04: Bottleneck Detection

## Overview

Bottleneck detection identifies components that limit platform throughput or latency under load. Common bottlenecks include STT service capacity, LLM inference throughput, database connection pool exhaustion, WebSocket handler limits, and network bandwidth constraints. The detection approach combines load testing with infrastructure monitoring.

## Design Decisions

- **Top-Down Analysis**: Start with system-level metrics, drill into components
- **Latency Breakdown**: Instrument each pipeline stage for timing
- **Resource Saturation Curves**: Plot resource utilization vs. throughput
- **Queue Depth Monitoring**: Track request queue depths at each service
- **Automated Detection**: Scripts flag potential bottlenecks during test runs

## Implementation Approach

```typescript
class BottleneckDetector {
  async analyze(testRun: LoadTestResult): Promise<BottleneckReport> {
    const bottlenecks: Bottleneck[] = [];
    const cpuData = testRun.metrics.filter(m => m.name === 'cpu_utilization');
    const cpuSaturated = cpuData.filter(d => d.value > 80).length / cpuData.length > 0.5;
    if (cpuSaturated) bottlenecks.push({
      type: 'cpu', severity: 'high',
      description: 'CPU saturation detected',
      recommendations: ['Scale horizontally', 'Optimize hot paths'],
    });
    const dbConnections = testRun.metrics.filter(m => m.name === 'db_connections_used');
    if (dbConnections.some(d => d.value >= d.max)) bottlenecks.push({
      type: 'database', severity: 'critical',
      description: 'Database connection pool exhausted',
      recommendations: ['Increase pool size', 'Add read replicas'],
    });
    const llmLatency = testRun.metrics.filter(m => m.name === 'llm_latency_p95');
    if (llmLatency.some(d => d.value > 1000)) bottlenecks.push({
      type: 'llm', severity: 'high',
      description: 'LLM inference latency exceeds threshold',
      recommendations: ['Implement caching', 'Use faster model'],
    });
    return { testRunId: testRun.id, summary: { totalBottlenecks: bottlenecks.length }, bottlenecks };
  }
}
```

## Integration Points

- **Profiling Tools**: Continuous profiling during load tests
- **APM**: Distributed tracing to identify slow services
- **Monitoring Stack**: Prometheus metrics for resource utilization

## Open-Source Tools

- **Pyroscope** (Apache 2.0): Continuous profiling
- **Prometheus** (Apache 2.0): Metrics collection
- **FlameGraph** (CDDL): CPU flame graphs

## Production Considerations

- **False Positives**: Validate with trend data before acting
- **Profiling Overhead**: Use sampling to minimize performance impact
