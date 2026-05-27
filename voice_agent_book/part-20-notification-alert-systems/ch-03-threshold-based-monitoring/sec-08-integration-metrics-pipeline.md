# Section 08: Integration with Metrics Pipeline

## Overview

Threshold evaluation integrates with the metrics pipeline through Prometheus, OpenTelemetry, and custom metric sources. The integration layer normalizes metric queries across providers, handles authentication, and provides a unified query interface. Alert events are enriched with metric context.

## Implementation Approach

```typescript
interface MetricsBackend {
  type: 'prometheus' | 'otel' | 'cloudwatch' | 'datadog' | 'custom';
  config: Record<string, unknown>;
  query(query: string, range?: TimeRange): Promise<MetricDataPoint[]>;
  health(): Promise<boolean>;
}

class MetricsPipelineIntegrator {
  private backends: Map<string, MetricsBackend> = new Map();

  registerBackend(name: string, backend: MetricsBackend): void {
    this.backends.set(name, backend);
  }

  async query(threshold: Threshold): Promise<number> {
    const backend = this.backends.get(threshold.metricSource.type);
    if (!backend) throw new Error(`Unknown backend: ${threshold.metricSource.type}`);

    const data = await backend.query(threshold.metricSource.query);
    return this.aggregate(data, threshold.metricSource.aggregation);
  }

  private aggregate(data: MetricDataPoint[], method: string): number {
    const values = data.map(d => d.value);
    switch (method) {
      case 'avg': return values.reduce((a, b) => a + b, 0) / values.length;
      case 'sum': return values.reduce((a, b) => a + b, 0);
      case 'max': return Math.max(...values);
      case 'min': return Math.min(...values);
      case 'count': return values.length;
      default: return values[values.length - 1];
    }
  }

  async createPromQLThreshold(metric: string, conditions: ThresholdCondition[]): Promise<Threshold> {
    // Map high-level metric to PromQL
    const promQL = this.metricMapper.toPromQL(metric);
    return this.thresholdManager.createThreshold({
      metricSource: { type: 'prometheus', query: promQL, aggregation: 'avg', interval: 60 },
      conditions,
      severity: 'major',
      evaluationWindow: 300,
    });
  }
}

// Prometheus backend implementation
class PrometheusBackend implements MetricsBackend {
  type = 'prometheus' as const;
  config: Record<string, unknown>;

  async query(query: string, range?: TimeRange): Promise<MetricDataPoint[]> {
    const url = `${this.config.url}/api/v1/query_range`;
    const params = {
      query,
      start: range?.start,
      end: range?.end,
      step: '60',
    };
    const response = await fetch(url, { headers: { Authorization: `Bearer ${this.config.token}` } });
    const data = await response.json();
    return data.data.result[0]?.values.map(([t, v]: [number, string]) => ({
      timestamp: new Date(t * 1000).toISOString(),
      value: parseFloat(v),
    })) || [];
  }

  async health(): Promise<boolean> {
    try {
      const response = await fetch(`${this.config.url}/-/healthy`);
      return response.ok;
    } catch { return false; }
  }
}
```

## Integration Points

- **Prometheus**: Primary metrics backend for infrastructure monitoring
- **OpenTelemetry**: Application-level metrics and traces
- **Custom Backends**: Cloud provider metrics (CloudWatch, Azure Monitor)

## Production Considerations

- **Authentication**: Securely store and rotate API tokens
- **Query Timeouts**: Set timeouts for metric queries
- **Caching**: Cache frequently queried metrics to reduce backend load
