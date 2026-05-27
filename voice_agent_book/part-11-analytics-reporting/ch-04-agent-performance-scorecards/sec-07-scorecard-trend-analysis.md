# Section 07: Scorecard Trend Analysis

## Overview

Scorecard trend analysis tracks how agent performance evolves over time, identifying improvement patterns, decline signals, and sustained performance levels. Trends are computed at multiple granularities (weekly, monthly, quarterly) for the overall scorecard score and each individual dimension. The system detects statistically significant trends — an agent whose CSAT score has increased for 4 consecutive weeks has a "significant improvement" flag, while an agent whose occupancy has decreased for 3 consecutive months has a "decline alert."

Trend analysis serves multiple purposes: recognizing sustained high performers (for rewards and recognition), identifying deteriorating performance early (for coaching intervention), evaluating the effectiveness of training programs (did metrics improve after training?), and validating scorecard calibration (are scores stable over time or fluctuating randomly?). The visualization includes trend lines with confidence intervals, moving averages, and annotated milestones (training completion, campaign changes, role changes).

## Architecture

```
           Scorecard Trend Analysis Pipeline

   ClickHouse (agent_scorecards table)
        |
   Trend Engine
        |
   ┌────┴────────────┐
   |                 |
   Statistical      Milestone
   Trend Detector   Annotations
   (linear          (from HR system,
    regression,      training system,
    Mann-Kendall     campaign changes)
    test)
   |                 |
   Dashboard         Alert Engine
   (trend charts,    (decline flag,
    improvement       improvement
    flags)            recognition)
```

## Design Decisions

- **Mann-Kendall trend test over simple linear regression for trend detection:** The Mann-Kendall test is non-parametric (no assumption of normal distribution), robust to outliers, and can detect monotonic trends that are not strictly linear. It returns a tau value (-1 to 1) indicating trend direction and strength, and a p-value for significance. Linear regression would detect only linear trends and is sensitive to outliers. Trade-off: Mann-Kendall requires O(n²) pairwise comparisons, making it slower for long time series (> 100 data points), but scorecard data is typically 12-52 points (monthly over 1-4 years).

- **Multi-window trend analysis (4-week, 12-week, 52-week) over single-window:** An agent's performance may be declining over 52 weeks (long-term concern) but improving over 4 weeks (recent coaching effect). The system computes trends over three windows: short-term (4 weeks), medium-term (12 weeks), and long-term (52 weeks), each with its own significance threshold. The overall trend label is determined by a weighted combination of the three windows. Trade-off: three windows means three times the computation, but each is a simple ClickHouse query with a different date range.

- **Milestone-based trend segmentation over continuous trend analysis:** Instead of computing a single trend line, the system divides the agent's timeline into segments separated by milestones (training events, role changes, campaign assignments). A separate trend is computed for each segment, allowing comparison of pre-training vs post-training performance. This provides actionable causality — "after completing the objection-handling training, the agent's CSAT increased by 15 points." Trade-off: milestone-based segmentation requires reliable milestone data from HR and training systems, which may not always be available.

## Implementation Approach

```typescript
interface ScorecardSnapshot {
  agentId: string;
  tenantId: string;
  date: string;               // Weekly or monthly period end
  overallScore: number;
  dimensionScores: Array<{ name: string; score: number; weight: number }>;
}

interface TrendResult {
  metric: string;              // 'overall' or dimension name
  shortTerm: TrendWindow;
  mediumTerm: TrendWindow;
  longTerm: TrendWindow;
  overallDirection: 'improving' | 'declining' | 'stable' | 'volatile';
  rank?: number;               // Within team by trend strength
}

interface TrendWindow {
  windowWeeks: number;
  startDate: string;
  endDate: string;
  dataPoints: number;
  slope: number;              // Change per week
  tau: number;                // Mann-Kendall tau
  pValue: number;
  significant: boolean;
  direction: 'improving' | 'declining' | 'stable';
  averageScore: number;
  volatility: number;         // Standard deviation of residuals
}

interface Milestone {
  agentId: string;
  date: string;
  type: 'training_completed' | 'role_change' | 'campaign_change' | 'coaching_session' | 'promotion';
  title: string;
  description: string;
}

class TrendAnalyzer {
  private clickhouse: ClickHouseClient;

  async computeTrends(
    agentId: string,
    tenantId: string,
    metric: string = 'overall'
  ): Promise<TrendResult> {
    const scorecardData = await this.getScorecardHistory(agentId, tenantId, metric);
    if (scorecardData.length < 4) {
      throw new Error('Insufficient data for trend analysis (minimum 4 periods)');
    }

    const shortTerm = this.analyzeWindow(scorecardData, 4);
    const mediumTerm = this.analyzeWindow(scorecardData, 12);
    const longTerm = this.analyzeWindow(scorecardData, 52);

    // Compute overall direction from weighted combination
    const directions = [shortTerm, mediumTerm, longTerm].map(w => w.direction);
    const improvingCount = directions.filter(d => d === 'improving').length;
    const decliningCount = directions.filter(d => d === 'declining').length;

    let overallDirection: TrendResult['overallDirection'];
    if (improvingCount >= 2 && !decliningCount) {
      overallDirection = 'improving';
    } else if (decliningCount >= 2 && !improvingCount) {
      overallDirection = 'declining';
    } else if (this.isVolatile(shortTerm, mediumTerm, longTerm)) {
      overallDirection = 'volatile';
    } else {
      overallDirection = 'stable';
    }

    return {
      metric,
      shortTerm,
      mediumTerm,
      longTerm,
      overallDirection,
    };
  }

  private async getScorecardHistory(
    agentId: string,
    tenantId: string,
    metric: string
  ): Promise<Array<{ date: string; value: number }>> {
    const scoreData = await this.clickhouse.query(`
      SELECT date, overallScore, dimensionScores
      FROM agent_scorecards
      WHERE agentId = '${agentId}'
        AND tenantId = '${tenantId}'
      ORDER BY date ASC
    `);

    return scoreData.map((row: any) => ({
      date: row.date,
      value: metric === 'overall' ? row.overallScore
        : row.dimensionScores.find((d: any) => d.name === metric)?.score ?? 0,
    }));
  }

  private analyzeWindow(
    data: Array<{ date: string; value: number }>,
    windowWeeks: number
  ): TrendWindow {
    const endDate = new Date(data[data.length - 1].date);
    const startDate = new Date(endDate);
    startDate.setDate(startDate.getDate() - windowWeeks * 7);

    // Filter data within window
    const windowData = data.filter(d => {
      const dDate = new Date(d.date);
      return dDate >= startDate && dDate <= endDate;
    });

    if (windowData.length < 3) {
      return {
        windowWeeks,
        startDate: startDate.toISOString().split('T')[0],
        endDate: endDate.toISOString().split('T')[0],
        dataPoints: windowData.length,
        slope: 0, tau: 0, pValue: 1,
        significant: false, direction: 'stable',
        averageScore: windowData.reduce((s, d) => s + d.value, 0) / windowData.length,
        volatility: 0,
      };
    }

    // Mann-Kendall test
    const { tau, pValue } = this.mannKendall(windowData.map(d => d.value));
    const slope = this.sensSlope(windowData.map(d => d.value));
    const averageScore = windowData.reduce((s, d) => s + d.value, 0) / windowData.length;
    const volatility = this.computeVolatility(windowData.map(d => d.value));

    // Determine direction
    const significant = pValue < 0.1;
    const direction = significant
      ? slope > 0.5 ? 'improving'
        : slope < -0.5 ? 'declining'
        : 'stable'
      : 'stable';

    return {
      windowWeeks,
      startDate: startDate.toISOString().split('T')[0],
      endDate: endDate.toISOString().split('T')[0],
      dataPoints: windowData.length,
      slope,
      tau,
      pValue,
      significant,
      direction,
      averageScore,
      volatility,
    };
  }

  private mannKendall(values: number[]): { tau: number; pValue: number } {
    let s = 0;
    const n = values.length;

    for (let i = 0; i < n - 1; i++) {
      for (let j = i + 1; j < n; j++) {
        s += Math.sign(values[j] - values[i]);
      }
    }

    // Variance calculation
    const variance = (n * (n - 1) * (2 * n + 5)) / 18;
    const z = s > 0 ? (s - 1) / Math.sqrt(variance)
      : s < 0 ? (s + 1) / Math.sqrt(variance)
      : 0;

    // Two-tailed p-value approximation
    const pValue = 2 * (1 - this.normalCdf(Math.abs(z)));
    const tau = s / (n * (n - 1) / 2);

    return { tau, pValue };
  }

  private sensSlope(values: number[]): number {
    const slopes: number[] = [];
    for (let i = 0; i < values.length - 1; i++) {
      for (let j = i + 1; j < values.length; j++) {
        slopes.push((values[j] - values[i]) / (j - i));
      }
    }
    slopes.sort((a, b) => a - b);
    return slopes[Math.floor(slopes.length / 2)];
  }

  private computeVolatility(values: number[]): number {
    const mean = values.reduce((s, v) => s + v, 0) / values.length;
    const variance = values.reduce((s, v) => s + (v - mean) ** 2, 0) / values.length;
    return Math.sqrt(variance);
  }

  private normalCdf(x: number): number {
    // Approximation using Abramowitz and Stegun
    const a1 = 0.254829592;
    const a2 = -0.284496736;
    const a3 = 1.421413741;
    const a4 = -1.453152027;
    const a5 = 1.061405429;
    const p = 0.3275911;

    const sign = x < 0 ? -1 : 1;
    x = Math.abs(x) / Math.sqrt(2);
    const t = 1 / (1 + p * x);
    const y = 1 - (((((a5 * t + a4) * t) + a3) * t + a2) * t + a1) * t * Math.exp(-x * x);
    return 0.5 * (1 + sign * y);
  }

  private isVolatile(...trends: TrendWindow[]): boolean {
    // Volatility is high if standard deviation of short-term values > 15% of average
    return trends.some(t => t.volatility > 0.15 * t.averageScore);
  }

  async getMilestones(agentId: string, tenantId: string): Promise<Milestone[]> {
    // Query milestones from HR/training systems
    const trainingEvents = await this.clickhouse.query(`
      SELECT eventDate as date, 'training_completed' as type, title, description
      FROM agent_training_events
      WHERE agentId = '${agentId}' AND tenantId = '${tenantId}'
    `);

    const roleChanges = await this.clickhouse.query(`
      SELECT effectiveDate as date, 'role_change' as type, newRole as title, '' as description
      FROM agent_role_changes
      WHERE agentId = '${agentId}' AND tenantId = '${tenantId}'
    `);

    return [...trainingEvents, ...roleChanges].sort(
      (a: Milestone, b: Milestone) => new Date(a.date).getTime() - new Date(b.date).getTime()
    );
  }
}

// Trend chart component
const TrendChart: React.FC<{
  data: ScorecardSnapshot[];
  trends: TrendResult;
  milestones: Milestone[];
  metric: string;
}> = ({ data, trends, milestones, metric }) => {
  return (
    <div className="trend-chart-container">
      <TrendDirectionBadge direction={trends.overallDirection} />
      <LineChartWithConfidence
        data={data.map(d => ({ date: d.date, value: d.overallScore }))}
        xKey="date"
        yKey="value"
      />
      {trends.longTerm.significant && (
        <TrendAnnotation text={`${trends.longTerm.direction} ${Math.abs(trends.longTerm.slope).toFixed(1)} pts/week (p=${trends.longTerm.pValue.toFixed(3)})`} />
      )}
      <MilestoneOverlay milestones={milestones} />
    </div>
  );
};
```

## Open-Source Tools

| Tool | License | Purpose |
|------|---------|---------|
| ClickHouse (Apache 2.0) | Server | Scorecard history queries |
| simple-statistics (ISC) | Server | Statistical trend detection |
| Apache ECharts (Apache 2.0) | Client | Trend line charts with confidence bands |
| D3.js (ISC) | Client | Milestone annotation rendering |

## Production Considerations

**Scaling:** Trend analysis requires scorecard history — compute trends on-demand (cache for 6 hours) rather than pre-computing for all agents. Each trend computation queries the last 52 scorecard records (52 rows in ClickHouse, < 10 ms). For supervisors viewing trend charts for 20 agents in a single page load, batch into a single query with `WHERE agentId IN (...)` and `GROUP BY agentId`.

**Security:** Trend data inherits the same access controls as scorecard data — agent views own trends, supervisor views team trends. Milestone data from HR systems (training completion, role changes) may be sensitive and should require the `agent-performance:view-milestones` permission. Training system integration should only expose training completion dates and course names, not performance scores.

**Monitoring:** Track the number of agents flagged as "declining" or "volatile" — a sudden increase may indicate a scorecard calibration issue or a broader morale problem. Monitor the trend computation success rate. Alert if the trend detection pipeline consumes more than 5 minutes of CPU time per hour — optimize by caching frequently accessed scorecard histories.
