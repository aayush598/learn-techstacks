# Section 05: Heatmap Visualization

## Overview

Heatmap visualization provides a dense, color-coded view of intent and topic data across two dimensions simultaneously — typically time (hour of day × day of week) and intent/topic (intent × campaign, intent × sentiment, topic × queue). Heatmaps reveal patterns that are invisible in line charts or bar charts: "Billing inquiries spike between 10 AM and 2 PM on weekdays," "Technical support intents have lower sentiment on Monday mornings," or "Account management intents are concentrated in the Enterprise queue."

The heatmap system supports multiple data series: call volume (intensity of color = number of calls), sentiment (color = average sentiment score from red to green), frequency (percentage of total calls), and trend change (color = change vs previous period). Users can configure the X and Y axes from available dimensions (time, intent, campaign, queue, agent team, customer segment) and toggle between absolute and relative color scales.

## Architecture

```
           Heatmap Visualization Pipeline

   ClickHouse (intent/topic daily aggregations)
        |
   Heatmap Data Builder
   (aggregates by (xDimension, yDimension))
        |
   Color Mapping Engine
   (absolute, relative, diverging scales)
        |
   Heatmap API
        |
   ECharts Heatmap Component
   (interactive, zoomable, tooltip)
```

## Design Decisions

- **Server-side aggregation over client-side computation:** Heatmaps aggregate data by two dimensions and a metric. Aggregating on the server (ClickHouse) for the requested dimensions and time range is more efficient than fetching raw data and aggregating on the client. The server returns a dense matrix of (x, y, value) tuples, typically 50-500 data points — trivial for the charting library to render. Trade-off: each unique (x, y) combination requires a separate server request; the system pre-computes the most common heatmap views (intent × time, intent × campaign).

- **Diverging color scale (red-green) for sentiment, sequential scale (blue) for volume:** Sentiment heatmaps use a diverging color scale with a neutral midpoint (white at sentiment = 0), red for negative, and green for positive. This makes it immediately obvious which cells are above/below neutral. Volume heatmaps use a sequential blue scale (light = low, dark = high) because volume is always non-negative. The system auto-detects the metric type and selects the appropriate scale. Trade-off: diverging scales can be misleading if the data range does not cross the midpoint; a "force neutral at median" option is available for skewed distributions.

- **Interactive filtering and cross-highlighting over static heatmap:** When the user hovers over a heatmap cell, the tooltip shows the exact values and allows clicking to drill down to the underlying data. Clicking an intent cell opens the intent detail view filtered to that time period. Clicking a time cell opens the call list for that time slot. Cross-highlighting: selecting a row highlights the corresponding columns and vice versa. Trade-off: interactivity requires additional JavaScript event handling and may reduce rendering performance for very large heatmaps (50+ cells).

## Implementation Approach

```typescript
interface HeatmapConfig {
  tenantId: string;
  metric: 'call_volume' | 'sentiment' | 'frequency' | 'trend_change';
  xDimension: 'hour' | 'day_of_week' | 'date' | 'campaign' | 'queue' | 'agent_team';
  yDimension: 'intent' | 'topic' | 'category' | 'campaign';
  xOrder?: string[];
  yOrder?: string[];
  start: number;
  end: number;
  aggregation: 'sum' | 'avg' | 'p95';
  colorScale: 'sequential' | 'diverging' | 'sequential_reverse';
  filters?: Record<string, string[]>;
}

interface HeatmapDataPoint {
  x: string | number;           // X axis label
  y: string | number;           // Y axis label
  value: number;
  count?: number;               // Number of data points aggregated (for significance)
}

interface HeatmapResult {
  xLabels: (string | number)[];
  yLabels: (string | number)[];
  data: HeatmapDataPoint[];
  minValue: number;
  maxValue: number;
  config: HeatmapConfig;
}

class HeatmapService {
  private clickhouse: ClickHouseClient;
  private cache: Redis;

  async getHeatmap(config: HeatmapConfig): Promise<HeatmapResult> {
    const cacheKey = `heatmap:${JSON.stringify(config)}`;
    const cached = await this.cache.get(cacheKey);
    if (cached) return JSON.parse(cached);

    const result = await this.queryHeatmap(config);

    // Cache based on metric volatility
    const ttl = config.metric === 'sentiment' ? 600 : config.metric === 'trend_change' ? 300 : 1800;
    await this.cache.setex(cacheKey, ttl, JSON.stringify(result));

    return result;
  }

  private async queryHeatmap(config: HeatmapConfig): Promise<HeatmapResult> {
    const conditions = [
      `ci.tenantId = '${config.tenantId}'`,
      `ci.timestamp >= ${config.start}`,
      `ci.timestamp <= ${config.end}`,
    ];

    if (config.filters) {
      for (const [dim, values] of Object.entries(config.filters)) {
        if (values.length > 0) {
          conditions.push(`ci.${dim} IN (${values.map(v => `'${v}'`).join(',')})`);
        }
      }
    }

    // Build X and Y expressions based on dimensions
    const xExpr = this.getDimensionExpression(config.xDimension, 'ci');
    const yExpr = this.getDimensionExpression(config.yDimension, 'ci');
    const metricExpr = this.getMetricExpression(config.metric, config.aggregation);

    const query = `
      SELECT
        ${xExpr} as x,
        ${yExpr} as y,
        ${metricExpr} as value,
        count() as count
      FROM call_intents ci
      JOIN intent_definitions id ON ci.intentId = id.id
      WHERE ${conditions.join(' AND ')}
      GROUP BY x, y
      ORDER BY x, y
    `;

    const rows = await this.clickhouse.query(query);

    // Extract unique labels
    const xSet = new Set<string | number>();
    const ySet = new Set<string | number>();
    const data: HeatmapDataPoint[] = [];

    for (const row of rows) {
      xSet.add(row.x);
      ySet.add(row.y);
      data.push({
        x: row.x,
        y: row.y,
        value: row.value,
        count: row.count,
      });
    }

    const xLabels = config.xOrder ?? Array.from(xSet);
    const yLabels = config.yOrder ?? Array.from(ySet);

    // Sort labels if not custom ordered
    if (!config.xOrder) {
      xLabels.sort((a, b) => {
        if (typeof a === 'number' && typeof b === 'number') return a - b;
        return String(a).localeCompare(String(b));
      });
    }
    if (!config.yOrder) {
      yLabels.sort((a, b) => {
        if (typeof a === 'number' && typeof b === 'number') return a - b;
        return String(a).localeCompare(String(b));
      });
    }

    const values = data.map(d => d.value);

    return {
      xLabels,
      yLabels,
      data,
      minValue: Math.min(...values),
      maxValue: Math.max(...values),
      config,
    };
  }

  private getDimensionExpression(dimension: string, alias: string): string {
    switch (dimension) {
      case 'hour': return `toHour(${alias}.timestamp)`;
      case 'day_of_week': return `toDayOfWeek(${alias}.timestamp)`;
      case 'date': return `toDate(${alias}.timestamp)`;
      case 'intent': return `${alias}.intentId`;
      case 'topic': return `${alias}.topicId`;
      case 'category': return `id.parentId`;
      case 'campaign': return `${alias}.campaignId`;
      case 'queue': return `${alias}.queueId`;
      case 'agent_team': return `${alias}.agentTeamId`;
      default: return `'${dimension}'`;
    }
  }

  private getMetricExpression(metric: string, aggregation: string): string {
    switch (metric) {
      case 'call_volume':
        return `count(DISTINCT ${aggregation === 'sum' ? 'ci.callSid' : 'ci.callSid'})`;
      case 'sentiment':
        return `${aggregation}(ci.score)`;
      case 'frequency':
        // Frequency relative to all intents in the period (handled separately)
        return `count()`;
      case 'trend_change':
        // Computed by comparing current to previous period
        return `count()`; // Placeholder — actual trend change is computed separately
      default:
        return `count()`;
    }
  }
}

// Heatmap React component
const IntentHeatmap: React.FC<{
  data: HeatmapResult;
  metric: string;
  onCellClick: (x: string | number, y: string | number) => void;
}> = ({ data, metric, onCellClick }) => {
  const colorScale = metric === 'sentiment'
    ? ['#E74C3C', '#FADBD8', '#FFFFFF', '#D5F5E3', '#2ECC71']
    : ['#EBF5FB', '#3498DB'];

  return (
    <div className="intent-heatmap">
      <EChartsHeatmap
        xLabels={data.xLabels}
        yLabels={data.yLabels}
        data={data.data.map(d => [d.x, d.y, d.value])}
        minValue={data.minValue}
        maxValue={data.maxValue}
        colorScale={colorScale}
        onCellClick={(x, y) => onCellClick(x, y)}
        tooltipFormatter={(params: any) => {
          const d = data.data.find(p => p.x === params[0] && p.y === params[1]);
          return `X: ${params[0]}<br/>Y: ${params[1]}<br/>Value: ${params[2].toFixed(2)}<br/>Count: ${d?.count ?? 0}`;
        }}
      />
      <div className="heatmap-controls">
        <MetricToggle
          options={['call_volume', 'sentiment', 'frequency']}
          selected={metric}
        />
        <DimensionSelector
          label="X Axis"
          value={data.config.xDimension}
          options={['hour', 'day_of_week', 'campaign', 'queue']}
        />
        <DimensionSelector
          label="Y Axis"
          value={data.config.yDimension}
          options={['intent', 'category', 'campaign', 'queue']}
        />
      </div>
    </div>
  );
};
```

## Open-Source Tools

| Tool | License | Purpose |
|------|---------|---------|
| Apache ECharts (Apache 2.0) | Client | Heatmap chart rendering |
| ClickHouse (Apache 2.0) | Server | Two-dimensional aggregation |
| Redis (RSAL) | Server | Heatmap cache |
| React (MIT) | Client | Interactive heatmap controls |

## Production Considerations

**Scaling:** Heatmap queries group by two dimensions, which can be computationally expensive for high-cardinality dimensions. Limit the number of unique values in each dimension to 50 (if exceeded, bucket the larger dimension). Pre-compute the most common heatmap configurations (hour × intent, campaign × intent) every hour and cache. For ad-hoc configurations, set a 30-second query timeout.

**Security:** Heatmap data is aggregated and tenant-scoped. Access requires `analytics:view` permission. Heatmaps showing per-agent data (agent × intent) require `agent-performance:view`. The color scale does not expose PII — only aggregate counts and averages are displayed.

**Monitoring:** Track heatmap query performance (p95 < 500 ms). Alert if a heatmap query exceeds 5 seconds (indicates too many unique values). Monitor the most popular heatmap configurations to guide pre-computation prioritization.
