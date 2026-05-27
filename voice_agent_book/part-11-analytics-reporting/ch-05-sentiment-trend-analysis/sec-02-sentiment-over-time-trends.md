# Section 02: Sentiment Over Time Trends

## Overview

Sentiment over time trends track how customer sentiment evolves across multiple time dimensions — hourly, daily, weekly, monthly, and quarterly. These trends reveal patterns in customer satisfaction that correlate with operational changes, campaign launches, staffing levels, and external factors (holidays, market events). The system aggregates per-call sentiment scores into time-series data, computes moving averages, identifies seasonality, and detects statistically significant shifts in sentiment.

Trend visualizations include multi-series line charts (overall sentiment, customer sentiment, agent sentiment), heatmaps (sentiment by hour × day of week), and anomaly-highlighted trend lines. Users can segment trend data by campaign, queue, agent team, IVR path, customer segment, or any other available dimension. The trend analysis engine supports comparison periods — displaying current period sentiment alongside the previous period and year-over-year comparison.

## Architecture

```
           Sentiment Trend Pipeline

   ClickHouse (per-call sentiment)
        |
   Trend Aggregator
   (hourly, daily, weekly rollups)
        |
   ┌────┴────────────┐
   |                 |
   ClickHouse        Redis Cache
   (trend tables)    (recent trends)
   |                 |
   Sentiment Trend API
        |
   Trend Dashboard
   (line chart, heatmap,
    anomaly highlight, comparison)
```

## Design Decisions

- **Multi-granularity pre-aggregation over query-time aggregation:** Pre-computing sentiment averages at hourly, daily, weekly, and monthly granularities (written during the nightly rollup) makes trend queries sub-second regardless of the time range. Query-time aggregation over raw per-call data for a 1-year trend would scan millions of rows. Trade-off: pre-aggregation adds storage overhead (4 additional tables) and a slight delay (new calls are only included in trends after the next rollup, max 1 hour).

- **EWMA (Exponentially Weighted Moving Average) for trend smoothing over simple moving average:** EWMA gives more weight to recent data points, making it more responsive to sentiment changes while still smoothing noise. A simple moving average assigns equal weight to all points in the window, causing a 7-day lag in detecting shifts. The smoothing factor (α=0.3 for daily, α=0.1 for weekly) is configurable. Trade-off: EWMA is less intuitive to explain to non-technical users than a simple moving average; the dashboard shows both smoothed and raw data.

- **Statistical significance detection for trend shifts over visual-only cues:** A sudden drop in sentiment from 0.3 to 0.1 over 3 days might be noise or a real shift. The system applies a CUSUM (Cumulative Sum) change detection algorithm that flags shifts exceeding 2 standard deviations from the baseline. Flagged shifts trigger an annotation on the trend chart and an optional alert. Trade-off: CUSUM requires a baseline period (minimum 14 days of data) and may produce false positives during high-variance periods.

## Implementation Approach

```typescript
interface SentimentTrendPoint {
  period: string;              // date or datetime
  averageSentiment: number;
  customerSentiment: number;
  agentSentiment: number;
  callCount: number;
  positivePercent: number;
  neutralPercent: number;
  negativePercent: number;
  smoothedValue: number;       // EWMA
  anomalyScore?: number;        // deviation from expected
  isAnomaly?: boolean;
}

interface SentimentTrendQuery {
  tenantId: string;
  granularity: 'hour' | 'day' | 'week' | 'month';
  start: string;
  end: string;
  dimensions?: { queue?: string; campaign?: string; agentTeam?: string };
  includeComparison?: boolean;
  comparisonPeriod?: 'previous' | 'year_over_year';
}

class SentimentTrendService {
  private clickhouse: ClickHouseClient;
  private cache: Redis;

  async getTrend(query: SentimentTrendQuery): Promise<{
    data: SentimentTrendPoint[];
    baseline?: SentimentTrendPoint[];
    shiftDetected?: { date: string; magnitude: number };
  }> {
    const cacheKey = `sentiment:trend:${JSON.stringify(query)}`;
    const cached = await this.cache.get(cacheKey);
    if (cached) return JSON.parse(cached);

    const table = this.getGranularityTable(query.granularity);
    const dimensions = query.dimensions ?? {};

    // Build WHERE clause
    const conditions = [
      `tenantId = '${query.tenantId}'`,
      `period >= '${query.start}'`,
      `period <= '${query.end}'`,
    ];
    if (dimensions.queue) conditions.push(`queueId = '${dimensions.queue}'`);
    if (dimensions.campaign) conditions.push(`campaignId = '${dimensions.campaign}'`);
    if (dimensions.agentTeam) conditions.push(`agentTeamId = '${dimensions.agentTeam}'`);

    const result = await this.clickhouse.query(`
      SELECT
        period,
        avgSentiment,
        customerSentiment,
        agentSentiment,
        callCount,
        positivePct,
        neutralPct,
        negativePct
      FROM ${table}
      WHERE ${conditions.join(' AND ')}
      ORDER BY period ASC
    `);

    // Apply EWMA smoothing
    const data = this.applyEwma(result, query.granularity);

    // Detect shifts
    const shiftDetected = this.detectShift(data, query.granularity);

    // Get comparison data if requested
    let baseline: SentimentTrendPoint[] | undefined;
    if (query.includeComparison) {
      const periodDuration = this.getDateRangeDuration(query.start, query.end);
      const comparisonStart = query.comparisonPeriod === 'year_over_year'
        ? this.subtractPeriod(query.start, '1 year')
        : this.subtractPeriod(query.start, periodDuration);
      const comparisonEnd = query.comparisonPeriod === 'year_over_year'
        ? this.subtractPeriod(query.end, '1 year')
        : this.subtractPeriod(query.end, periodDuration);

      const baselineQuery = { ...query, start: comparisonStart, end: comparisonEnd };
      const baselineResult = await this.clickhouse.query(`
        SELECT period, avgSentiment, callCount
        FROM ${table}
        WHERE ${conditions.join(' AND ')}
          AND period >= '${comparisonStart}'
          AND period <= '${comparisonEnd}'
        ORDER BY period ASC
      `);
      baseline = this.applyEwma(baselineResult, query.granularity);
    }

    const response = { data, baseline, shiftDetected };
    await this.cache.setex(cacheKey, 600, JSON.stringify(response)); // 10 min cache
    return response;
  }

  private applyEwma(
    rawData: Array<{ period: string; customerSentiment: number; avgSentiment: number; [key: string]: any }>,
    granularity: string
  ): SentimentTrendPoint[] {
    const alpha = granularity === 'hour' ? 0.5 : granularity === 'day' ? 0.3 : 0.1;
    let ewma = rawData.length > 0 ? rawData[0].customerSentiment : 0;

    return rawData.map((point, idx) => {
      if (idx > 0) {
        ewma = alpha * point.customerSentiment + (1 - alpha) * ewma;
      }

      return {
        period: point.period,
        customerSentiment: point.customerSentiment,
        agentSentiment: point.agentSentiment ?? 0,
        averageSentiment: point.avgSentiment,
        callCount: point.callCount,
        positivePercent: point.positivePct,
        neutralPercent: point.neutralPct,
        negativePercent: point.negativePct,
        smoothedValue: ewma,
      };
    });
  }

  private detectShift(
    data: SentimentTrendPoint[],
    granularity: string
  ): { date: string; magnitude: number } | undefined {
    if (data.length < 14) return undefined;

    // CUSUM algorithm
    const mean = data.slice(0, 14).reduce((s, d) => s + d.customerSentiment, 0) / 14;
    const std = Math.sqrt(
      data.slice(0, 14).reduce((s, d) => s + (d.customerSentiment - mean) ** 2, 0) / 14
    );

    const threshold = 2 * std;
    let cumSum = 0;

    for (let i = 14; i < data.length; i++) {
      cumSum += data[i].customerSentiment - mean;
      if (Math.abs(cumSum) > threshold) {
        return {
          date: data[i].period,
          magnitude: cumSum,
        };
      }
    }

    return undefined;
  }

  private getGranularityTable(granularity: string): string {
    const tables: Record<string, string> = {
      hour: 'sentiment_hourly_rollup',
      day: 'sentiment_daily_rollup',
      week: 'sentiment_weekly_rollup',
      month: 'sentiment_monthly_rollup',
    };
    return tables[granularity] ?? 'sentiment_daily_rollup';
  }

  private getDateRangeDuration(start: string, end: string): string {
    const d1 = new Date(start);
    const d2 = new Date(end);
    const diffMs = d2.getTime() - d1.getTime();
    const days = Math.round(diffMs / (24 * 3600 * 1000));
    return `${days} days`;
  }

  private subtractPeriod(date: string, duration: string): string {
    const d = new Date(date);
    if (duration.includes('year')) d.setFullYear(d.getFullYear() - 1);
    else if (duration.includes('day')) d.setDate(d.getDate() - parseInt(duration));
    return d.toISOString().split('T')[0];
  }
}

// Sentiment trend chart component
const SentimentTrendChart: React.FC<{
  data: SentimentTrendPoint[];
  baseline?: SentimentTrendPoint[];
  shiftDetected?: { date: string; magnitude: number };
  granularity: string;
}> = ({ data, baseline, shiftDetected, granularity }) => (
  <div className="sentiment-trend">
    <div className="sentiment-summary">
      <MetricRow label="Current" value={data[data.length - 1]?.customerSentiment.toFixed(3)} />
      <MetricRow label="Avg" value={data.reduce((s, d) => s + d.customerSentiment, 0) / data.length.toFixed(3)} />
      <MetricRow label="Positive" value={`${data[data.length - 1]?.positivePercent.toFixed(1)}%`} />
    </div>
    <LineChartWithComparison
      data={data}
      baseline={baseline}
      lineKey="smoothedValue"
      rawKey="customerSentiment"
      xKey="period"
      shiftAnnotation={shiftDetected}
    />
    <SentimentHeatmapBreakdown />
  </div>
);
```

## Open-Source Tools

| Tool | License | Purpose |
|------|---------|---------|
| ClickHouse (Apache 2.0) | Server | Time-series sentiment storage |
| Redis (RSAL) | Server | Trend result cache |
| Apache ECharts (Apache 2.0) | Client | Trend line charts |
| Recharts (MIT) | Client | Heatmap visualization |

## Production Considerations

**Scaling:** Pre-aggregated tables at each granularity store one row per period per dimension combination. For 50 queues × 365 days = 18,250 rows per year for daily granularity — negligible storage. The cache reduces query load for popular trend views (last 30 days, all campaigns). Set cache TTL to 10 minutes for hourly trends, 1 hour for weekly trends.

**Security:** Trend data is aggregated and does not expose individual call or agent sentiment. However, trends filtered to a single queue or campaign could reveal performance patterns — access requires the `analytics:view` permission. Year-over-year comparison data should not be accessible if the tenant has less than 1 year of history.

**Monitoring:** Track trend query performance (p95 < 200 ms). Alert if the sentiment hourly rollup job fails or completes later than 10 minutes past the hour. Monitor the CUSUM shift detection rate — if shifts are detected more than once per week on average, the sensitivity threshold may be too low.
