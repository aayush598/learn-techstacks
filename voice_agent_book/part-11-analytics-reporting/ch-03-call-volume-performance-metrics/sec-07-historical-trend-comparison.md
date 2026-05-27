# Section 07: Historical Trend and Comparison

## Overview

Historical trend and comparison analysis enables contact center operators to understand how key performance metrics evolve over time and compare current performance against historical baselines. Trends are computed for all major metrics (call volume, AHT, ASA, service level, abandonment rate, occupancy) at multiple granularities (hourly, daily, weekly, monthly, quarterly, yearly). Comparisons include period-over-period (e.g., this week vs last week), year-over-year (this month vs same month last year), and day-over-day with same-day-of-week alignment.

The trend analysis engine uses ClickHouse time series functions to compute moving averages, detect seasonality, and identify inflection points (sudden changes in metric direction). Results are visualized as multi-series line charts with confidence bands, annotated with significant events (deployments, campaigns, holidays) that may explain metric changes. The system automatically detects and highlights anomalous periods where metrics deviate significantly from the expected range.

## Architecture

```
           Historical Trend and Comparison Pipeline

   ClickHouse (aggregated time series)
        |
   Trend Engine
        |
   ┌────┼────┬──────────┐
   |    |    |          |
   MoMA  YoY  Day/Day   Event Correlation
   (MoM  (YoY  (DoD      (annotations on
   Avg)  Comp) Comp)      chart)
        |
   API / WebSocket
        |
   Trend Chart Widget
   Comparison Table
   Anomaly Highlights
```

## Design Decisions

- **Moving Average (MA) with confidence bands over raw time series display:** Raw daily metrics are noisy (weekend dips, holiday spikes). A 7-day moving average smooths the noise while preserving trend direction. Confidence bands (±1 standard deviation of the moving average) show the expected range — points outside the bands are flagged as anomalies. Trade-off: the moving average introduces a 3-day lag in trend detection; for real-time anomaly detection, a separate EWMA (exponentially weighted moving average) stream processor is used.

- **Day-of-week alignment for period comparison over simple date alignment:** Comparing Tuesday, May 27 to Tuesday, May 20 (same day of week) is more meaningful than comparing to Monday, May 26 (adjacent day) because call volume follows strong weekly seasonality. The comparison engine automatically aligns by day of week when comparing two periods. Trade-off: day-of-week alignment requires at least 7 days of data to establish the baseline, and the comparison period must be a multiple of 7 days for fair comparison.

- **Event annotations from deployment/change logs over manual entry:** Significant metric changes often correlate with system changes (new IVR flow, agent reassignment, campaign launch). The system ingests deployment events from CI/CD pipelines and operational change logs, and overlays them on trend charts. Users can also add manual annotations for business events (holiday, promotion, outage). Trade-off: automated annotation ingestion depends on integration with the change management system; the initial setup requires configuration.

## Implementation Approach

```typescript
interface TrendDataPoint {
  timestamp: number;
  metric: string;
  value: number;
  movingAverage?: number;
  upperBand?: number;
  lowerBand?: number;
  isAnomaly?: boolean;
}

interface PeriodComparison {
  metric: string;
  currentPeriod: { label: string; value: number };
  previousPeriod: { label: string; value: number };
  absoluteDelta: number;
  percentageDelta: number;
  direction: 'up' | 'down' | 'flat';
  significant: boolean;
}

interface TrendAnnotation {
  timestamp: number;
  type: 'deployment' | 'campaign' | 'holiday' | 'outage' | 'manual';
  title: string;
  description: string;
  color: string;
}

class TrendEngine {
  private clickhouse: ClickHouseClient;

  async getTrend(
    tenantId: string,
    metric: string,
    start: number,
    end: number,
    granularity: 'hour' | 'day' | 'week' = 'day'
  ): Promise<TrendDataPoint[]> {
    const granularityFn = granularity === 'hour' ? 'toStartOfHour'
      : granularity === 'day' ? 'toDate'
      : 'toStartOfWeek';

    const result = await this.clickhouse.query(`
      SELECT
        ${granularityFn}(timestamp) as period,
        avg(value) as value,
        avg(avg(value)) OVER (
          ORDER BY ${granularityFn}(timestamp)
          ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
        ) as movingAverage,
        stddevSamp(value) OVER (
          ORDER BY ${granularityFn}(timestamp)
          ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
        ) as stdDev
      FROM daily_metric_rollups
      WHERE tenantId = '${tenantId}'
        AND metric = '${metric}'
        AND timestamp >= ${start}
        AND timestamp <= ${end}
      GROUP BY period
      ORDER BY period
    `);

    return result.map((row: any) => ({
      timestamp: new Date(row.period).getTime(),
      metric,
      value: row.value,
      movingAverage: row.movingAverage,
      upperBand: row.movingAverage + 1.96 * row.stdDev,
      lowerBand: row.movingAverage - 1.96 * row.stdDev,
      isAnomaly: row.value > row.movingAverage + 1.96 * row.stdDev
        || row.value < row.movingAverage - 1.96 * row.stdDev,
    }));
  }

  async comparePeriods(
    tenantId: string,
    metric: string,
    currentStart: number,
    currentEnd: number,
    granularity: 'day' | 'week' = 'day'
  ): Promise<PeriodComparison> {
    const periodDuration = currentEnd - currentStart;
    const previousStart = currentStart - periodDuration;

    const result = await this.clickhouse.query(`
      SELECT
        avgIf(value, timestamp >= ${currentStart} AND timestamp <= ${currentEnd}) as currentAvg,
        avgIf(value, timestamp >= ${previousStart} AND timestamp < ${currentStart}) as previousAvg,
        countIf(timestamp >= ${currentStart} AND timestamp <= ${currentEnd}) as currentCount,
        countIf(timestamp >= ${previousStart} AND timestamp < ${currentStart}) as previousCount
      FROM daily_metric_rollups
      WHERE tenantId = '${tenantId}'
        AND metric = '${metric}'
        AND timestamp >= ${previousStart}
        AND timestamp <= ${currentEnd}
    `);

    const row = result[0];
    const current = row.currentAvg ?? 0;
    const previous = row.previousAvg ?? 0;
    const delta = current - previous;
    const pct = previous !== 0 ? (delta / previous) * 100 : 0;

    // Simple significance check: at least 5% change and minimum 10 data points
    const significant = Math.abs(pct) > 5 && row.currentCount >= 10 && row.previousCount >= 10;

    return {
      metric,
      currentPeriod: { label: 'Current', value: current },
      previousPeriod: { label: 'Previous', value: previous },
      absoluteDelta: delta,
      percentageDelta: pct,
      direction: delta > 1 ? 'up' : delta < -1 ? 'down' : 'flat',
      significant,
    };
  }

  async getAnnotations(
    tenantId: string,
    start: number,
    end: number
  ): Promise<TrendAnnotation[]> {
    // Query deployment events from CI/CD webhook store
    const deployments = await this.clickhouse.query(`
      SELECT timestamp, title, description, 'deployment' as type
      FROM deployment_events
      WHERE tenantId = '${tenantId}'
        AND timestamp >= ${start}
        AND timestamp <= ${end}
    `);

    // Query campaign events from campaign management
    const campaigns = await this.clickhouse.query(`
      SELECT timestamp, name as title, description, 'campaign' as type
      FROM campaign_events
      WHERE tenantId = '${tenantId}'
        AND timestamp >= ${start}
        AND timestamp <= ${end}
    `);

    return [...deployments, ...campaigns].map((e: any) => ({
      timestamp: e.timestamp,
      type: e.type,
      title: e.title ?? e.name,
      description: e.description ?? '',
      color: e.type === 'deployment' ? '#3498DB' : '#2ECC71',
    }));
  }
}

// Trend chart component with annotations
const TrendChart: React.FC<{
  data: TrendDataPoint[];
  annotations?: TrendAnnotation[];
  metric: string;
  format: 'integer' | 'decimal' | 'duration' | 'percentage';
}> = ({ data, annotations, metric, format }) => {
  return (
    <div className="trend-chart">
      <LineChartWithConfidenceBands
        data={data}
        lineKey="movingAverage"
        bandUpperKey="upperBand"
        bandLowerKey="lowerBand"
        anomalyKey="isAnomaly"
        xKey="timestamp"
        yKey="value"
        yLabel={metric}
        format={format}
      />
      {annotations && annotations.length > 0 && (
        <AnnotationLayer
          annotations={annotations.map(a => ({
            x: a.timestamp,
            label: a.title,
            color: a.color,
            description: a.description,
          }))}
        />
      )}
      <ComparisonTable comparisons={/* fetched comparisons */} />
    </div>
  );
};

// Period comparison table
const ComparisonTable: React.FC<{
  comparisons: PeriodComparison[];
}> = ({ comparisons }) => (
  <table className="comparison-table">
    <thead>
      <tr>
        <th>Metric</th>
        <th>Current</th>
        <th>Previous</th>
        <th>Delta</th>
        <th>% Change</th>
      </tr>
    </thead>
    <tbody>
      {comparisons.map(c => (
        <tr key={c.metric} className={c.significant ? 'significant' : ''}>
          <td>{c.metric}</td>
          <td>{formatMetricValue(c.currentPeriod.value, 'decimal')}</td>
          <td>{formatMetricValue(c.previousPeriod.value, 'decimal')}</td>
          <td className={c.direction}>
            {c.direction === 'up' ? '↑' : c.direction === 'down' ? '↓' : '→'} {c.absoluteDelta.toFixed(1)}
          </td>
          <td className={c.direction}>{c.percentageDelta.toFixed(1)}%</td>
        </tr>
      ))}
    </tbody>
  </table>
);
```

## Open-Source Tools

| Tool | License | Purpose |
|------|---------|---------|
| ClickHouse (Apache 2.0) | Server | Time series trend computation |
| Apache ECharts (Apache 2.0) | Client | Multi-series line charts with bands |
| Apache Kafka (Apache 2.0) | Server | Deployment/campaign event ingestion |
| Recharts (MIT) | Client | Comparison table rendering |

## Production Considerations

**Scaling:** Historical trend queries aggregate across potentially millions of data points. Use ClickHouse materialized views pre-aggregated at hourly granularity for daily trend queries, and daily granularity for monthly/yearly queries. Set a maximum query range of 365 days to prevent runaway queries. Cache trend results for 5-15 minutes depending on granularity (hourly trends change more frequently than yearly).

**Security:** Trend data is tenant-scoped. Period comparisons compare the same tenant's data across time — no cross-tenant data is exposed. Annotations from deployment events may contain internal system information (version numbers, infrastructure changes) — ensure the deployment event webhook strips sensitive details before ingestion.

**Monitoring:** Track trend query performance — p95 should be under 500 ms for daily granularity over 90 days. Alert if the anomaly detection rate exceeds 10% of data points (indicates the confidence bands are too narrow or the metric is inherently unstable). Monitor the event annotation pipeline for freshness — if no deployment events are received within 48 hours, alert the operations team.
