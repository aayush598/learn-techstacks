# Section 04: Intent Trend Detection

## Overview

Intent trend detection monitors how the frequency and sentiment of intents change over time, identifying rising and falling intents before they become obvious. The system analyzes intent time series (daily call counts and average sentiment per intent) and applies statistical change detection to flag emerging trends. For example, a gradual 3-week increase in "Account Cancellation" intents might indicate a product or service issue that needs attention, while a sudden spike in "Password Reset" might indicate a system outage.

Trend detection operates at multiple levels: individual intents (L3), intent categories (L2/L1), and cross-intent correlations (e.g., "Billing Question" and "Payment Issue" intents are both rising — suggesting a pricing change impact). The system uses moving averages, seasonal decomposition, and change point detection to distinguish signal from noise. Detected trends are surfaced in the dashboard as "Trending Intents" with direction indicators, confidence levels, and estimated business impact.

## Architecture

```
           Intent Trend Detection Pipeline

   ClickHouse (intent daily counts + sentiment)
        |
   Trend Detection Engine
        |
   ┌────┴────────────┐
   |                 |
   Moving Average    Change Point
   (7-day, 30-day)   (PELT algorithm)
   |                 |
   Seasonal Decomposition (STL)
        |
   Trend Result
   (direction, magnitude, confidence, impact)
        |
   Dashboard Widget
   ("Trending Intents" cards,
    trend line charts)
```

## Design Decisions

- **PELT (Pruned Exact Linear Time) change point detection over CUSUM for trend detection:** CUSUM detects mean shifts but does not pinpoint when the change occurred. PELT efficiently identifies multiple change points in a time series and provides the exact date of each change. This allows the system to say "Intent X started rising on March 15" which can be correlated with other events. Trade-off: PELT requires computing the series mean and variance which is O(n²) in the worst case, but the pruned version is O(n) for most practical cases.

- **Seasonal-trend decomposition (STL) over raw time series analysis:** Call volume and intent frequency have strong weekly seasonality (high Monday, low Sunday). A rising intent might just be a Monday effect. STL decomposes the time series into trend, seasonal, and residual components, allowing trend detection on the seasonally-adjusted data. Trade-off: STL requires at least 2 full seasonal cycles (14 days for weekly seasonality) to initialize, so new intents (< 2 weeks old) cannot be trend-analyzed.

- **Business impact scoring over pure statistical significance:** A statistically significant trend (+5% per week) in a low-volume intent (10 calls/day) is less important than a smaller trend (+2% per week) in a high-volume intent (500 calls/day). The system computes a business impact score = trend magnitude × intent volume × sentiment delta (if sentiment is also trending negatively). Trends are ranked by impact score, and the top 5 are displayed. Trade-off: impact scoring is an approximation that may over-weight high-volume intents even if the trend is not actionable.

## Implementation Approach

```typescript
interface IntentTrendResult {
  intentId: string;
  intentName: string;
  level: number;
  category: string;              // L1 parent name
  
  // Volume trend
  volumeTrend: {
    direction: 'increasing' | 'decreasing' | 'stable';
    pctChangeWeekly: number;     // average % change per week
    changePoint?: number;        // timestamp of detected change
    confidence: number;
    seasonallyAdjusted: boolean;
  };
  
  // Sentiment trend
  sentimentTrend: {
    direction: 'improving' | 'declining' | 'stable';
    changePerWeek: number;
    currentSentiment: number;
  };
  
  // Business impact
  impactScore: number;           // 0-100 ranking
  dailyCallVolume: number;
  
  // Drill-down
  breakdownByCampaign?: Array<{ campaign: string; direction: string; change: number }>;
}

class IntentTrendDetector {
  private clickhouse: ClickHouseClient;

  async detectTrends(
    tenantId: string,
    intentLevel: number = 2,
    lookbackDays: number = 90
  ): Promise<IntentTrendResult[]> {
    const endDate = new Date();
    const startDate = new Date();
    startDate.setDate(startDate.getDate() - lookbackDays);

    // Get daily intent counts and sentiment
    const dailyData = await this.clickhouse.query(`
      SELECT
        intentId,
        id.name as intentName,
        id.level,
        ip.name as categoryName,
        toDate(timestamp) as date,
        count(DISTINCT callSid) as callCount,
        avg(score) as avgSentiment
      FROM call_intents ci
      JOIN intent_definitions id ON ci.intentId = id.id
      LEFT JOIN intent_definitions ip ON id.parentId = ip.id
      WHERE ci.tenantId = '${tenantId}'
        AND id.level = ${intentLevel}
        AND ci.timestamp >= ${startDate.getTime()}
        AND ci.timestamp <= ${endDate.getTime()}
      GROUP BY intentId, id.name, id.level, ip.name, toDate(timestamp)
      ORDER BY intentId, date
    `);

    // Group by intent
    const intentGroups = new Map<string, Array<{ date: string; count: number; sentiment: number }>>();
    for (const row of dailyData) {
      if (!intentGroups.has(row.intentId)) {
        intentGroups.set(row.intentId, []);
      }
      intentGroups.get(row.intentId)!.push({
        date: row.date,
        count: row.callCount,
        sentiment: row.avgSentiment,
      });
    }

    const results: IntentTrendResult[] = [];

    for (const [intentId, series] of intentGroups) {
      if (series.length < 14) continue; // Need at least 2 weeks

      series.sort((a, b) => new Date(a.date).getTime() - new Date(b.date).getTime());

      // STL decomposition (simplified)
      const { trend, seasonal, residual } = this.stlDecompose(series);

      // Volume trend detection on seasonally-adjusted data
      const volumeTrend = this.detectVolumeTrend(trend, residual);

      // Sentiment trend
      const sentimentValues = series.map(s => s.sentiment).filter(s => s != null);
      const sentimentTrend = this.detectSentimentTrend(sentimentValues);

      // Business impact
      const avgDailyVolume = series.reduce((s, r) => s + r.count, 0) / series.length;
      const impactScore = this.computeImpactScore(volumeTrend, sentimentTrend, avgDailyVolume);

      results.push({
        intentId,
        intentName: series[0]?.intentName ?? intentId,
        level: intentLevel,
        category: series[0]?.categoryName ?? '',
        volumeTrend,
        sentimentTrend,
        impactScore,
        dailyCallVolume: avgDailyVolume,
      });
    }

    return results.sort((a, b) => b.impactScore - a.impactScore);
  }

  private stlDecompose(series: Array<{ date: string; count: number }>): {
    trend: number[];
    seasonal: number[];
    residual: number[];
  } {
    const n = series.length;
    const values = series.map(s => s.count);
    const period = 7; // Weekly seasonality

    // Simplified STL: moving average for trend, average deviation for seasonal
    const trend = [];
    const windowSize = Math.min(period, Math.floor(n / 2));

    for (let i = 0; i < n; i++) {
      const start = Math.max(0, i - Math.floor(windowSize / 2));
      const end = Math.min(n, i + Math.ceil(windowSize / 2));
      const window = values.slice(start, end);
      trend.push(window.reduce((s, v) => s + v, 0) / window.length);
    }

    // Seasonal: average of (value - trend) for each position in the period
    const detrended = values.map((v, i) => v - trend[i]);
    const seasonal = new Array(n).fill(0);
    for (let i = 0; i < period; i++) {
      const positions: number[] = [];
      for (let j = i; j < n; j += period) positions.push(j);
      const avg = positions.reduce((s, p) => s + detrended[p], 0) / positions.length;
      for (const p of positions) seasonal[p] = avg;
    }

    const residual = values.map((v, i) => v - trend[i] - seasonal[i]);

    return { trend, seasonal, residual };
  }

  private detectVolumeTrend(
    trend: number[],
    residual: number[]
  ): IntentTrendResult['volumeTrend'] {
    if (trend.length < 7) {
      return { direction: 'stable', pctChangeWeekly: 0, confidence: 0, seasonallyAdjusted: true };
    }

    // Linear regression on last 14 trend points
    const recentTrend = trend.slice(-14);
    const n = recentTrend.length;
    const xMean = (n - 1) / 2;
    const yMean = recentTrend.reduce((s, v) => s + v, 0) / n;

    let numerator = 0;
    let denominator = 0;
    for (let i = 0; i < n; i++) {
      const xDiff = i - xMean;
      const yDiff = recentTrend[i] - yMean;
      numerator += xDiff * yDiff;
      denominator += xDiff * xDiff;
    }

    const slope = denominator !== 0 ? numerator / denominator : 0;
    const pctChangeWeekly = yMean !== 0 ? (slope / yMean) * 100 : 0;

    // Confidence based on residual variance
    const residualVariance = residual.slice(-14).reduce((s, v) => s + v * v, 0) / n;
    const signalVariance = recentTrend.reduce((s, v) => s + (v - yMean) * (v - yMean), 0) / n;
    const confidence = signalVariance > 0
      ? Math.min(1, 1 - residualVariance / signalVariance)
      : 0;

    // PELT-like change point detection: look for max deviation in recent trend
    const baselineMean = trend.slice(0, Math.max(7, trend.length - 14)).reduce((s, v) => s + v, 0) / 7;
    const changePoint = Math.abs(recentTrend[recentTrend.length - 1] - baselineMean) > residualVariance * 2
      ? Date.now() - 14 * 24 * 3600 * 1000 + residual.indexOf(Math.max(...residual.slice(-14))) * 24 * 3600 * 1000
      : undefined;

    const direction = Math.abs(pctChangeWeekly) < 2 ? 'stable'
      : pctChangeWeekly > 0 ? 'increasing' : 'decreasing';

    return {
      direction,
      pctChangeWeekly,
      changePoint,
      confidence: confidence * (1 - residualVariance / (yMean + 0.01)),
      seasonallyAdjusted: true,
    };
  }

  private detectSentimentTrend(
    values: number[]
  ): IntentTrendResult['sentimentTrend'] {
    if (values.length < 7) {
      return { direction: 'stable', changePerWeek: 0, currentSentiment: 0 };
    }

    const recent = values.slice(-14);
    const firstAvg = recent.slice(0, 7).reduce((s, v) => s + v, 0) / 7;
    const lastAvg = recent.slice(-7).reduce((s, v) => s + v, 0) / 7;
    const changePerWeek = (lastAvg - firstAvg) / 2;

    const direction = Math.abs(changePerWeek) < 0.05 ? 'stable'
      : changePerWeek > 0 ? 'improving' : 'declining';

    return {
      direction,
      changePerWeek,
      currentSentiment: lastAvg,
    };
  }

  private computeImpactScore(
    volumeTrend: IntentTrendResult['volumeTrend'],
    sentimentTrend: IntentTrendResult['sentimentTrend'],
    dailyVolume: number
  ): number {
    const volumeMagnitude = Math.abs(volumeTrend.pctChangeWeekly) / 20; // 0-1 scale
    const volumeConfidence = volumeTrend.confidence;
    const sentimentMagnitude = Math.abs(sentimentTrend.changePerWeek) / 0.5; // 0-1 scale
    const volumeFactor = Math.min(1, dailyVolume / 500); // Normalize to 0-1

    // Negative sentiment trend + increasing volume = highest impact
    const combinedScore = volumeMagnitude * volumeConfidence * volumeFactor
      + (sentimentTrend.direction === 'declining' ? sentimentMagnitude * 2 : 0);

    return Math.min(100, Math.round(combinedScore * 100));
  }
}

// Trending intents widget
const TrendingIntentsWidget: React.FC<{
  trends: IntentTrendResult[];
}> = ({ trends }) => (
  <div className="trending-intents">
    {trends.slice(0, 10).map(t => (
      <TrendCard
        key={t.intentId}
        intentName={t.intentName}
        direction={t.volumeTrend.direction}
        change={t.volumeTrend.pctChangeWeekly}
        confidence={t.volumeTrend.confidence}
        sentimentDirection={t.sentimentTrend.direction}
        volume={t.dailyCallVolume}
        impactScore={t.impactScore}
        onClick={() => navigateToIntentDetail(t.intentId)}
      />
    ))}
  </div>
);
```

## Open-Source Tools

| Tool | License | Purpose |
|------|---------|---------|
| ClickHouse (Apache 2.0) | Server | Daily intent time series |
| STL decomposition (Python statsmodels) | BSD-3 | Server (Python worker) | Seasonal decomposition |
| Apache ECharts (Apache 2.0) | Client | Trend line charts |
| Recharts (MIT) | Client | Trend card sparklines |

## Production Considerations

**Scaling:** Trend detection runs nightly for all intents with sufficient data. For 100 intents × 90 days = 9,000 data points, the computation completes in < 5 seconds. The STL decomposition runs in-process (JavaScript) for simplicity — for larger datasets (500+ intents), offload to a Python worker with statsmodels. Trend results are cached in Redis with a 6-hour TTL (computed nightly, so cache lives until next computation).

**Security:** Trend results are aggregated and do not expose individual data points. Access requires `analytics:view` permission. The business impact score is computed from aggregate data and is tenant-scoped.

**Monitoring:** Track the number of intents with statistically significant trends detected per week. Alert if the trend detection pipeline fails. Monitor the confidence distribution — if average confidence drops below 0.3, the data may be too noisy or the STL decomposition parameters need adjustment.
