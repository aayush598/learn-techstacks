# Section 04: Customer Satisfaction Correlation

## Overview

Customer Satisfaction (CSAT) correlation analysis connects post-call survey responses to agent performance metrics, identifying which agent behaviors and operational factors most strongly influence customer satisfaction. The system collects CSAT scores (1-5 rating) and NPS scores (0-10) from post-call surveys, correlates them with agent-level metrics (AHT, sentiment during call, hold time, ACW time, QA scores), and presents the findings as actionable insights for coaching and process improvement.

The correlation analysis uses statistical methods (Pearson correlation, Spearman rank correlation) to identify significant relationships. For example, it might find that "agents with AHT between 180-300 seconds have 20% higher CSAT than agents with AHT < 120 seconds" or "calls with hold time exceeding 60 seconds see a 15-point drop in CSAT." Results are segmented by campaign, queue, and customer segment to provide context-specific insights.

## Architecture

```
           CSAT Correlation Pipeline

   Post-Call Survey → CSAT/NPS Data
        |
   Agent Metrics (from scorecard system)
        |
   Correlation Engine
        |
   ┌────┴────────────┐
   |                 |
   Statistical       Visualization
   Analysis          (scatter plot, heatmap,
   (Pearson,         correlation matrix,
    Spearman)        segment comparison)
   |                 |
   ClickHouse        Dashboard Widgets
   (correlation      (insight cards,
    results)          recommendation engine)
```

## Design Decisions

- **Segment-level correlation over global correlation:** A global correlation (e.g., "AHT vs CSAT across all calls") may hide important segment-specific patterns. The system computes correlations per campaign, per queue, per customer segment (new vs returning customer), and per time segment (business hours vs after-hours). This prevents Simpson's paradox — where a relationship appears in subgroups but disappears or reverses when combined. Trade-off: segment correlation increases computation time (N segments x M metric pairs = N*M correlation calculations instead of 1).

- **Non-linear correlation detection using Spearman rank over Pearson only:** The relationship between agent metrics and CSAT is often non-linear — very short AHT and very long AHT both correlate with lower CSAT, while moderate AHT correlates with higher CSAT (the "Goldilocks effect"). Spearman rank correlation captures monotonic relationships (including non-linear ones) without assuming linearity. The system computes both Pearson and Spearman and presents both, flagging cases where they differ significantly as "non-linear relationship detected." Trade-off: Spearman rank correlation requires sorting all data points, which is more computationally expensive than Pearson.

- **Actionable insights with confidence levels over raw correlation coefficients:** Presenting "r = -0.35" to a contact center manager is not helpful. The system translates statistical findings into natural-language insights: "Calls with hold time > 60 seconds average 0.4 points lower CSAT" with a confidence level and effect size. Insights are ranked by potential business impact (effect size × affected call volume). Trade-off: generating natural-language insights requires templated insight descriptions and thresholds for what constitutes a "significant" finding.

## Implementation Approach

```typescript
interface CsatRecord {
  callSid: string;
  agentId: string;
  tenantId: string;
  campaignId: string;
  queueId: string;
  csatScore: number;       // 1-5
  npsScore?: number;       // 0-10
  surveyCompletedAt: number;
  // Metrics to correlate
  ahtSeconds: number;
  holdTimeSeconds: number;
  acwTimeSeconds: number;
  sentimentScore: number;
  talkTimeSeconds: number;
  transferCount: number;
  qaScore?: number;
}

interface CorrelationResult {
  metricA: string;
  metricB: string;
  segment?: string;
  pearsonR: number;
  spearmanRho: number;
  sampleSize: number;
  pValue: number;
  significant: boolean;
  nonLinear: boolean;       // true if Pearson and Spearman differ significantly
}

interface ActionableInsight {
  title: string;
  description: string;
  metric: string;
  threshold?: { operator: 'gt' | 'lt'; value: number };
  effectSize: number;        // e.g., "0.4 points CSAT difference"
  affectedCallVolume: number;
  confidence: 'high' | 'medium' | 'low';
  recommendedAction: string;
}

class CsatCorrelationEngine {
  private clickhouse: ClickHouseClient;

  async computeCorrelations(
    tenantId: string,
    start: number,
    end: number,
    segment?: { by: string; value: string }
  ): Promise<CorrelationResult[]> {
    const segments = segment
      ? [{ by: segment.by, value: segment.value }]
      : await this.getSegments(tenantId, start, end);

    const results: CorrelationResult[] = [];
    const metricPairs = [
      ['ahtSeconds', 'csatScore'],
      ['holdTimeSeconds', 'csatScore'],
      ['sentimentScore', 'csatScore'],
      ['transferCount', 'csatScore'],
      ['qaScore', 'csatScore'],
      ['talkTimeSeconds', 'npsScore'],
      ['holdTimeSeconds', 'npsScore'],
    ];

    for (const seg of segments) {
      const conditions = [
        `tenantId = '${tenantId}'`,
        `surveyCompletedAt >= ${start}`,
        `surveyCompletedAt <= ${end}`,
      ];

      if (seg.by && seg.value) {
        conditions.push(`${seg.by} = '${seg.value}'`);
      }

      const data = await this.clickhouse.query(`
        SELECT * FROM csat_calls
        WHERE ${conditions.join(' AND ')}
      `);

      if (data.length < 30) continue; // Minimum sample size

      for (const [metricA, metricB] of metricPairs) {
        const valuesA = data.map((r: any) => r[metricA]).filter((v: any) => v != null);
        const valuesB = data.map((r: any) => r[metricB]).filter((v: any) => v != null);

        if (valuesA.length < 30) continue;

        const pearsonR = this.pearsonCorrelation(valuesA, valuesB);
        const spearmanRho = this.spearmanCorrelation(valuesA, valuesB);
        const pValue = this.approximatePValue(pearsonR, valuesA.length);

        results.push({
          metricA,
          metricB,
          segment: seg.by ? `${seg.by}=${seg.value}` : undefined,
          pearsonR,
          spearmanRho,
          sampleSize: valuesA.length,
          pValue,
          significant: pValue < 0.05 && Math.abs(pearsonR) > 0.15,
          nonLinear: Math.abs(pearsonR - spearmanRho) > 0.15,
        });
      }
    }

    return results;
  }

  async generateInsights(
    tenantId: string,
    correlations: CorrelationResult[]
  ): Promise<ActionableInsight[]> {
    const insights: ActionableInsight[] = [];

    for (const corr of correlations) {
      if (!corr.significant) continue;

      // Compute effect size and affected volume
      const data = await this.getThresholdEffect(
        tenantId,
        corr.metricA,
        corr.metricB,
        corr.segment
      );

      if (corr.metricA === 'holdTimeSeconds' && corr.pearsonR < -0.15) {
        insights.push({
          title: 'Hold Time Reduces CSAT',
          description: `Calls with hold time > ${data.threshold}s average ${data.impactDelta.toFixed(1)} points lower CSAT`,
          metric: 'holdTimeSeconds',
          threshold: { operator: 'gt', value: data.threshold },
          effectSize: Math.abs(data.impactDelta),
          affectedCallVolume: data.affectedCalls,
          confidence: corr.pValue < 0.01 ? 'high' : corr.pValue < 0.05 ? 'medium' : 'low',
          recommendedAction: 'Review hold procedures and consider callback options for complex issues',
        });
      }

      if (corr.metricA === 'sentimentScore' && corr.pearsonR > 0.3) {
        insights.push({
          title: 'Call Sentiment Predicts CSAT',
          description: `Calls where agent sentiment drops below ${data.threshold} have ${data.impactDelta.toFixed(1)} points lower CSAT`,
          metric: 'sentimentScore',
          threshold: { operator: 'lt', value: data.threshold },
          effectSize: Math.abs(data.impactDelta),
          affectedCallVolume: data.affectedCalls,
          confidence: 'high',
          recommendedAction: 'Provide real-time sentiment alerts to agents when their sentiment drops below threshold',
        });
      }
    }

    return insights.sort((a, b) => b.effectSize * b.affectedCallVolume - a.effectSize * a.affectedCallVolume);
  }

  private async getThresholdEffect(
    tenantId: string,
    metricA: string,
    metricB: string,
    segment?: string
  ): Promise<{ threshold: number; impactDelta: number; affectedCalls: number }> {
    // Binary search for optimal threshold that maximizes CSAT difference
    const percentiles = [50, 60, 70, 80, 90, 95];
    let bestThreshold = 0;
    let bestDelta = 0;

    for (const p of percentiles) {
      const thresholdResult = await this.clickhouse.query(`
        SELECT
          quantile(${p / 100})(${metricA}) as threshold
        FROM csat_calls
        WHERE tenantId = '${tenantId}'
      `);

      const threshold = thresholdResult[0].threshold;
      const deltaResult = await this.clickhouse.query(`
        SELECT
          avgIf(${metricB}, ${metricA} > ${threshold}) as aboveAvg,
          avgIf(${metricB}, ${metricA} <= ${threshold}) as belowAvg,
          countIf(${metricA} > ${threshold}) as aboveCount
        FROM csat_calls
        WHERE tenantId = '${tenantId}'
      `);

      const delta = (deltaResult[0].belowAvg ?? 0) - (deltaResult[0].aboveAvg ?? 0);
      if (Math.abs(delta) > Math.abs(bestDelta)) {
        bestDelta = delta;
        bestThreshold = threshold;
      }
    }

    return {
      threshold: bestThreshold,
      impactDelta: bestDelta,
      affectedCalls: /* query count above threshold */ 0,
    };
  }

  private pearsonCorrelation(x: number[], y: number[]): number {
    const n = x.length;
    const sumX = x.reduce((a, b) => a + b, 0);
    const sumY = y.reduce((a, b) => a + b, 0);
    const sumXY = x.reduce((a, b, i) => a + b * y[i], 0);
    const sumX2 = x.reduce((a, b) => a + b * b, 0);
    const sumY2 = y.reduce((a, b) => a + b * b, 0);

    const numerator = n * sumXY - sumX * sumY;
    const denominator = Math.sqrt((n * sumX2 - sumX * sumX) * (n * sumY2 - sumY * sumY));

    return denominator === 0 ? 0 : numerator / denominator;
  }

  private spearmanCorrelation(x: number[], y: number[]): number {
    const rank = (arr: number[]): number[] => {
      const sorted = [...arr].sort((a, b) => a - b);
      return arr.map(v => sorted.indexOf(v) + 1);
    };
    return this.pearsonCorrelation(rank(x), rank(y));
  }

  private approximatePValue(r: number, n: number): number {
    const t = r * Math.sqrt((n - 2) / (1 - r * r));
    // Simplified p-value using t-distribution approximation
    return 2 * (1 - this.studentCdf(t, n - 2));
  }

  private studentCdf(t: number, df: number): number {
    // Simplified approximation
    const x = df / (df + t * t);
    return 1 - 0.5 * this.incompleteBeta(0.5 * df, 0.5, x);
  }

  private incompleteBeta(a: number, b: number, x: number): number {
    // Placeholder — in production use a statistics library
    return x; // Simplified
  }
}
```

## Open-Source Tools

| Tool | License | Purpose |
|------|---------|---------|
| ClickHouse (Apache 2.0) | Server | Correlation data queries |
| simple-statistics (ISC) | Server/Client | Statistical functions |
| Apache ECharts (Apache 2.0) | Client | Scatter plot and heatmap visualization |
| Nivo (MIT) | Client | Correlation matrix visualization |

## Production Considerations

**Scaling:** Correlation computation is CPU-intensive for large datasets. For tenants with 100K+ CSAT records, run correlations as a nightly batch job and cache the results. Segment-level correlations multiply the computation; limit to the top 10 segments by call volume. Use ClickHouse's `corr()` function for Pearson correlation in SQL, which is highly optimized for columnar data.

**Security:** CSAT records are linked to agent IDs. Aggregated correlation results (e.g., "agents with AHT > 5 minutes have lower CSAT") do not identify individual agents and are viewable by supervisors. Raw CSAT-surveyed call data requires the `calls:view-details` permission. Per-agent CSAT correlation results are agent performance data and require `agent-performance:view`.

**Monitoring:** Track the number of significant correlations found per week — a sudden drop may indicate a data quality issue. Monitor the correlation computation job duration and alert if it exceeds 30 minutes. Track the insight adoption rate — how many recommended actions are acknowledged or implemented by supervisors.
