# Section 04: Real-Time Chart Visualizations

## Overview

Real-time chart visualizations transform streaming metric data into live-updating line charts, area charts, bar charts, and heatmaps on the monitoring dashboard. These charts display trends over rolling time windows (last 5 minutes, last hour, last 24 hours) and auto-scroll as new data points arrive. Key visualizations include: call volume over time (line chart), average handle time trend (area chart), queue depth vs. agent availability (dual-axis chart), and sentiment distribution (stacked area chart).

Charts use a sliding window approach — as new data points arrive via WebSocket, old points beyond the window boundary are dropped. The render loop is throttled to 30 FPS even if data arrives at higher frequency. Users can pause the real-time feed to inspect historical data within the current window, and can export the visible chart as PNG or CSV. Each chart shows confidence intervals or prediction bands for metrics computed from sample data.

## Architecture

```
               Real-Time Chart Pipeline

   Stream Processor → Redis TS → Metrics API → WebSocket
                                                   |
                                        Chart Engine
                                        (ECharts/Recharts)
                                                   |
                                        Window Buffer (Client)
                                                   |
                                        Auto-scroll / Pause
                                        Tooltip / Zoom / Export
```

## Design Decisions

- **Client-side window buffer over server-side pre-aggregation for chart data:** The server sends raw time-series data points at 1-second granularity. The client maintains a ring buffer of the last N data points (configurable by time window). The charting library renders from this buffer. This allows users to freely scroll within the window and adjust the time range without additional server queries. Trade-off: large windows (24 hours at 1-second resolution = 86,400 points) exceed browser rendering capacity, so progressive downsampling is needed — average to 1-minute resolution for views beyond 1 hour.

- **Dual-axis charts for correlated metrics over separate chart panels:** When displaying queue depth (bars) alongside agent availability (line), using a single chart with dual Y-axes helps operators visually correlate the two metrics. However, dual-axis charts can be misleading if the axis scales are not clearly labeled. We implement dual-axis charts only for well-understood metric pairs (queue depth/agents available, calls offered/answered) and always draw a visual separator on the axis labels. Trade-off: dual-axis charts require careful handling of the secondary axis scale to avoid visual distortion.

- **ECharts over Recharts for real-time performance:** ECharts uses a Canvas-based renderer that handles 10,000+ data points without DOM node overhead, while Recharts (SVG-based) degrades beyond 2,000 points. For real-time monitoring dashboards that frequently display 24-hour windows, ECharts provides smoother animation and faster initial render. Trade-off: ECharts has a steeper learning curve and larger bundle size (500 KB vs 150 KB for Recharts), but we use dynamic import to load it only on dashboard pages.

## Implementation Approach

```typescript
interface ChartConfig {
  id: string;
  type: 'line' | 'area' | 'bar' | 'dual-axis' | 'heatmap' | 'stacked-area';
  title: string;
  metrics: ChartMetric[];
  timeWindow: number;        // ms
  refreshInterval: number;   // ms
  yAxisLabel?: string;
  yAxisSecondaryLabel?: string;
  groupBy?: string;           // e.g., 'campaign', 'agent'
  threshold?: { warning: number; critical: number };
}

interface ChartMetric {
  key: string;
  label: string;
  color: string;
  yAxisIndex?: 0 | 1;       // for dual-axis
  aggregation: 'avg' | 'sum' | 'count' | 'p95' | 'p99';
  format: 'integer' | 'decimal' | 'duration' | 'percentage';
}

class RealtimeChartBuffer {
  private buffer: Map<string, Array<{ timestamp: number; value: number }>> = new Map();
  private maxPoints: number;
  private downsampledResolution: number;

  constructor(maxPoints: number = 1440) {
    this.maxPoints = maxPoints;
    this.downsampledResolution = 60000; // 1 minute
  }

  push(metricKey: string, timestamp: number, value: number): void {
    if (!this.buffer.has(metricKey)) {
      this.buffer.set(metricKey, []);
    }

    const series = this.buffer.get(metricKey)!;
    series.push({ timestamp, value });

    // Trim excess with downsampling
    if (series.length > this.maxPoints) {
      this.downsample(series);
    }
  }

  private downsample(series: Array<{ timestamp: number; value: number }>): void {
    // Group by resolution bucket, average values in each bucket
    const buckets = new Map<number, number[]>();

    for (const point of series) {
      const bucket = Math.floor(point.timestamp / this.downsampledResolution) * this.downsampledResolution;
      if (!buckets.has(bucket)) buckets.set(bucket, []);
      buckets.get(bucket)!.push(point.value);
    }

    const downsampled = Array.from(buckets.entries())
      .map(([timestamp, values]) => ({
        timestamp,
        value: values.reduce((a, b) => a + b, 0) / values.length,
      }))
      .sort((a, b) => a.timestamp - b.timestamp);

    // Keep only the last maxPoints after downsampling
    this.buffer.set('downsampled', downsampled.slice(-this.maxPoints));
  }

  getWindow(metricKey: string, startTime: number, endTime: number) {
    const series = this.buffer.get(metricKey) ?? [];
    return series.filter(p => p.timestamp >= startTime && p.timestamp <= endTime);
  }
}

// ECharts option builder
function buildChartOption(config: ChartConfig, data: Map<string, Array<[number, number]>>) {
  const series = config.metrics.map((metric, idx) => ({
    name: metric.label,
    type: config.type === 'dual-axis' && idx === 1 ? 'line' : config.type,
    data: data.get(metric.key) ?? [],
    smooth: true,
    showSymbol: false,
    yAxisIndex: metric.yAxisIndex ?? 0,
    areaStyle: config.type === 'area' || config.type === 'stacked-area'
      ? { opacity: 0.3 }
      : undefined,
    stack: config.type === 'stacked-area' ? 'stack' : undefined,
    itemStyle: { color: metric.color },
  }));

  return {
    grid: { left: 60, right: 60, top: 40, bottom: 40 },
    xAxis: {
      type: 'time',
      min: Date.now() - config.timeWindow,
      max: Date.now(),
    },
    yAxis: [
      {
        type: 'value',
        name: config.yAxisLabel,
      },
      ...(config.yAxisSecondaryLabel
        ? [{ type: 'value', name: config.yAxisSecondaryLabel }]
        : []),
    ],
    series,
    tooltip: {
      trigger: 'axis',
      valueFormatter: (value: number, metricIndex: number) =>
        formatMetricValue(value, config.metrics[metricIndex].format),
    },
    dataZoom: [
      { type: 'inside', xAxisIndex: 0 },
      { type: 'slider', xAxisIndex: 0 },
    ],
  };
}

// Worker-based data processing
const chartWorker = new Worker(
  URL.createObjectURL(new Blob([`
    self.onmessage = function(e) {
      const { data, config } = e.data;
      // Run downsampling in worker
      const processed = downsample(data, config.timeWindow);
      self.postMessage(processed);
    };
  `], { type: 'application/javascript' }))
);
```

## Open-Source Tools

| Tool | License | Purpose |
|------|---------|---------|
| Apache ECharts (Apache 2.0) | Client | Canvas-based real-time charting |
| Recharts (MIT) | Client | SVG charting for static charts |
| D3.js (ISC) | Client | Custom visualizations |
| Web Workers API (Browser) | Client | Background data processing |

## Production Considerations

**Scaling:** Client-side rendering performance is the primary concern. For dashboards with 10+ charts, lazy-load charts that are not in the visible viewport. Use `requestAnimationFrame` throttling for chart updates (not `setInterval`) to align with browser paint cycles. Implement progressive loading: render a coarse chart immediately (1-minute resolution), then refine with 1-second resolution data as it arrives. Disable animations on chart initial render when there are 500+ data points.

**Security:** Chart data inherits the same tenant-scoped access as all dashboard data. Export functionality (PNG/CSV) must respect data access permissions — a supervisor exporting a chart should only receive data they have permission to view. CSV exports should strip PII fields automatically.

**Monitoring:** Track chart render time per chart type (p50/p95), WebSocket data point throughput per chart, and memory usage of chart buffers. Alert if any chart's render time exceeds 100 ms — this may indicate excessive data points that need more aggressive downsampling. Monitor client-side memory for the window buffer — if it exceeds 50 MB, force a buffer flush and reload.
