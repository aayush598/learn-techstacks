# Section 05: Funnel Comparison Analysis

## Overview

Funnel comparison analysis enables side-by-side comparison of conversion funnels across different time periods, segments, or experimental configurations. The goal is to identify which changes (intentional or unintentional) have statistically significant impacts on caller conversion. Common comparisons include: current week vs previous week (trend monitoring), before vs after an IVR change (impact analysis), campaign A vs campaign B (segmentation), and high-performing vs low-performing agents (peer comparison).

The comparison engine computes difference metrics for each stage: absolute difference in entry count, percentage point difference in conversion rate, and relative change (percentage change in conversion rate). Statistical significance is assessed using a two-proportion z-test for conversion rates and a chi-square test for overall funnel distribution. Results are visualized as side-by-side funnel charts with delta annotations, a difference waterfall, and a "statistically significant" highlight on stages where the change is meaningful.

## Architecture

```
            Funnel Comparison Pipeline

   ClickHouse (funnel event data)
        |
   Comparison Engine
        |
   ┌────┴────────────┐
   |                 |
   Period-over-     Segment         Experimental
   Period           Comparison      (A/B test)
   (week/week,      (campaign,      (before/after
    month/month)     queue, agent)    change)
   |                 |                 |
   Statistical Tests (z-test, chi-square)
        |
   Comparison Result
   (deltas, significance, effect size)
        |
   Dashboard (side-by-side funnels,
   delta annotations, significance flags)
```

## Design Decisions

- **Four comparison modes (period, segment, cohort, experiment) over a single comparison type:** Different analytical questions need different comparison modes: period comparison (this week vs last week) for trend monitoring, segment comparison (campaign A vs B) for allocation decisions, cohort comparison (new hires vs experienced agents) for training evaluation, and experimental comparison (before vs after change) for impact analysis. Each mode has slightly different statistical treatment — experimental comparisons use a longer pre-period baseline (4 weeks) to account for seasonality. Trade-off: four comparison modes increase development complexity but cover the full range of analytical needs.

- **Two-proportion z-test for conversion rate significance over Bayesian methods:** The z-test is computationally simple, widely understood, and appropriate for comparing two proportions (conversion rates) with large sample sizes typical in call centers (>100 calls per stage). Bayesian methods would provide more nuanced uncertainty estimates but require prior specification and MCMC computation. Trade-off: the z-test assumes independent observations (each call is independent), which is generally valid but may be violated by agent-level clustering effects.

- **Effect size reporting with confidence intervals over p-value-only reporting:** A statistically significant result (p < 0.05) doesn't mean the effect is practically significant. A 0.5% conversion improvement with p = 0.01 but 100,000 calls is statistically significant but may not be operationally meaningful. The system reports effect size (Cohen's h for proportions) alongside the p-value, with a "practical significance" label: "small" (h < 0.2), "medium" (h = 0.2-0.5), or "large" (h > 0.5). Trade-off: effect size interpretation requires user education — tooltips explain what the effect size means.

## Implementation Approach

```typescript
interface FunnelComparisonRequest {
  tenantId: string;
  funnelId: string;
  mode: 'period' | 'segment' | 'cohort' | 'experiment';
  primaryFilter: ComparisonFilter;
  comparisonFilter: ComparisonFilter;
  stages?: string[];            // Limit comparison to specific stages
}

interface ComparisonFilter {
  start: number;
  end: number;
  segment?: { dimension: string; value: string };
  cohort?: { attribute: string; value: string };
  experiment?: { changeDate: number; preWindowDays: number; postWindowDays: number };
}

interface StageComparison {
  stageId: string;
  stageName: string;
  order: number;

  primary: StageMetrics;
  comparison: StageMetrics;

  entryDelta: number;
  entryDeltaPercent: number;
  conversionDelta: number;         // percentage point difference
  conversionRelativeChange: number; // percentage change

  test: {
    zStatistic: number;
    pValue: number;
    significant: boolean;           // p < 0.05
    effectSize: number;             // Cohen's h
    effectLabel: 'small' | 'medium' | 'large' | 'negligible';
  };
}

interface StageMetrics {
  entries: number;
  exits: number;
  dropOffs: number;
  conversionRate: number;
  averageDuration: number;
}

class FunnelComparisonEngine {
  private clickhouse: ClickHouseClient;

  async compare(request: FunnelComparisonRequest): Promise<{
    stageComparisons: StageComparison[];
    overallPrimary: { rate: number; entries: number; conversions: number };
    overallComparison: { rate: number; entries: number; conversions: number };
    overallDelta: number;
    overallSignificant: boolean;
  }> {
    const primaryData = await this.getStageMetrics(
      request.tenantId,
      request.funnelId,
      request.primaryFilter,
      request.stages
    );
    const comparisonData = await this.getStageMetrics(
      request.tenantId,
      request.funnelId,
      request.comparisonFilter,
      request.stages
    );

    const primaryMap = new Map(primaryData.map((r: any) => [r.stageId, r]));
    const comparisonMap = new Map(comparisonData.map((r: any) => [r.stageId, r]));
    const stageIds = Array.from(new Set([...primaryMap.keys(), ...comparisonMap.keys()]))
      .sort();

    const stageComparisons: StageComparison[] = [];

    for (const stageId of stageIds) {
      const primary = primaryMap.get(stageId) ?? { stageId, entries: 0, exits: 0, dropOffs: 0, avgDuration: 0 };
      const comparison = comparisonMap.get(stageId) ?? { stageId, entries: 0, exits: 0, dropOffs: 0, avgDuration: 0 };

      const primaryConv = primary.entries > 0 ? (primary.exits / primary.entries) * 100 : 0;
      const comparisonConv = comparison.entries > 0 ? (comparison.exits / comparison.entries) * 100 : 0;
      const entryDelta = primary.entries - comparison.entries;
      const conversionDelta = primaryConv - comparisonConv;
      const conversionRelativeChange = comparisonConv > 0 ? (conversionDelta / comparisonConv) * 100 : 0;

      // Two-proportion z-test
      const zTest = this.twoProportionZTest(
        primary.exits, primary.entries,
        comparison.exits, comparison.entries
      );

      // Cohen's h effect size
      const h = this.cohensH(primaryConv / 100, comparisonConv / 100);

      stageComparisons.push({
        stageId,
        stageName: stageId, // Will be replaced with actual name from definition
        order: 0,
        primary: {
          entries: primary.entries,
          exits: primary.exits,
          dropOffs: primary.dropOffs,
          conversionRate: primaryConv,
          averageDuration: primary.avgDuration,
        },
        comparison: {
          entries: comparison.entries,
          exits: comparison.exits,
          dropOffs: comparison.dropOffs,
          conversionRate: comparisonConv,
          averageDuration: comparison.avgDuration,
        },
        entryDelta,
        entryDeltaPercent: comparison.entries > 0 ? (entryDelta / comparison.entries) * 100 : 0,
        conversionDelta,
        conversionRelativeChange,
        test: {
          ...zTest,
          effectSize: h,
          effectLabel: Math.abs(h) < 0.2 ? 'negligible'
            : Math.abs(h) < 0.5 ? 'small'
            : Math.abs(h) < 0.8 ? 'medium'
            : 'large',
        },
      });
    }

    // Overall funnel comparison
    const firstStagePrimary = primaryData.find((r: any) => {
      // First stage in the funnel
      return true;
    });
    const lastStagePrimary = primaryData[primaryData.length - 1];
    const firstStageComparison = comparisonData[0];
    const lastStageComparison = comparisonData[comparisonData.length - 1];

    const overallPrimaryRate = firstStagePrimary?.entries > 0
      ? (lastStagePrimary?.exits / firstStagePrimary?.entries) * 100 : 0;
    const overallComparisonRate = firstStageComparison?.entries > 0
      ? (lastStageComparison?.exits / firstStageComparison?.entries) * 100 : 0;

    const overallTest = this.twoProportionZTest(
      lastStagePrimary?.exits ?? 0, firstStagePrimary?.entries ?? 1,
      lastStageComparison?.exits ?? 0, firstStageComparison?.entries ?? 1
    );

    return {
      stageComparisons,
      overallPrimary: {
        rate: overallPrimaryRate,
        entries: firstStagePrimary?.entries ?? 0,
        conversions: lastStagePrimary?.exits ?? 0,
      },
      overallComparison: {
        rate: overallComparisonRate,
        entries: firstStageComparison?.entries ?? 0,
        conversions: lastStageComparison?.exits ?? 0,
      },
      overallDelta: overallPrimaryRate - overallComparisonRate,
      overallSignificant: overallTest.significant,
    };
  }

  private async getStageMetrics(
    tenantId: string,
    funnelId: string,
    filter: ComparisonFilter,
    stageFilter?: string[]
  ): Promise<any[]> {
    const conditions = [
      `tenantId = '${tenantId}'`,
      `funnelId = '${funnelId}'`,
      `timestamp >= ${filter.start}`,
      `timestamp <= ${filter.end}`,
    ];

    if (filter.segment) {
      conditions.push(`${filter.segment.dimension} = '${filter.segment.value}'`);
    }

    if (stageFilter && stageFilter.length > 0) {
      conditions.push(`stageId IN (${stageFilter.map(s => `'${s}'`).join(',')})`);
    }

    return this.clickhouse.query(`
      SELECT
        stageId,
        countIf(eventType = 'stage_entry') as entries,
        countIf(eventType = 'stage_exit') as exits,
        countIf(eventType IN ('stage_dropoff', 'stage_abandon')) as dropOffs,
        avgIf(durationMs, eventType = 'stage_exit') as avgDuration
      FROM funnel_events
      WHERE ${conditions.join(' AND ')}
      GROUP BY stageId
      ORDER BY stageId
    `);
  }

  private twoProportionZTest(
    x1: number, n1: number,
    x2: number, n2: number
  ): { zStatistic: number; pValue: number; significant: boolean } {
    if (n1 < 5 || n2 < 5) {
      return { zStatistic: 0, pValue: 1, significant: false };
    }

    const p1 = x1 / n1;
    const p2 = x2 / n2;
    const p = (x1 + x2) / (n1 + n2);

    const se = Math.sqrt(p * (1 - p) * (1 / n1 + 1 / n2));
    if (se === 0) return { zStatistic: 0, pValue: 1, significant: false };

    const z = (p1 - p2) / se;
    // Two-tailed p-value
    const pValue = 2 * (1 - this.normalCdf(Math.abs(z)));

    return {
      zStatistic: z,
      pValue,
      significant: pValue < 0.05,
    };
  }

  private cohensH(p1: number, p2: number): number {
    const arcsin = (p: number) => 2 * Math.asin(Math.sqrt(Math.max(0, Math.min(1, p))));
    return arcsin(p1) - arcsin(p2);
  }

  private normalCdf(x: number): number {
    const a1 = 0.254829592; const a2 = -0.284496736;
    const a3 = 1.421413741; const a4 = -1.453152027;
    const a5 = 1.061405429; const p = 0.3275911;
    const sign = x < 0 ? -1 : 1;
    x = Math.abs(x) / Math.sqrt(2);
    const t = 1 / (1 + p * x);
    const y = 1 - (((((a5 * t + a4) * t) + a3) * t + a2) * t + a1) * t * Math.exp(-x * x);
    return 0.5 * (1 + sign * y);
  }
}

// Comparison result widget
const FunnelComparisonWidget: React.FC<{
  result: any;
  onStageClick: (stageId: string) => void;
}> = ({ result, onStageClick }) => (
  <div className="funnel-comparison">
    <div className="comparison-header">
      <div className="overall-delta">
        <span className={`delta ${result.overallDelta > 0 ? 'positive' : 'negative'}`}>
          {result.overallDelta > 0 ? '+' : ''}{result.overallDelta.toFixed(1)}%
        </span>
        <span className={`significance ${result.overallSignificant ? 'significant' : 'not-significant'}`}>
          {result.overallSignificant ? 'Significant' : 'Not significant'}
        </span>
      </div>
    </div>
    <div className="comparison-stages">
      {result.stageComparisons.map((sc: any) => (
        <StageComparisonRow
          key={sc.stageId}
          comparison={sc}
          onClick={() => onStageClick(sc.stageId)}
        />
      ))}
    </div>
  </div>
);
```

## Open-Source Tools

| Tool | License | Purpose |
|------|---------|---------|
| ClickHouse (Apache 2.0) | Server | Funnel metrics queries |
| simple-statistics (ISC) | Server | Statistical test functions |
| Apache ECharts (Apache 2.0) | Client | Side-by-side funnel charts |
| Recharts (MIT) | Client | Difference waterfall chart |

## Production Considerations

**Scaling:** Comparison queries run two funnel queries (primary and comparison) and apply statistical tests in application code. Each funnel query scans the funnel_events table filtered by (tenantId, funnelId, timestamp) — index on those three columns ensures fast queries even for large tables. Cache comparison results for 5 minutes (results change only when new events arrive). The z-test and Cohen's h computations are trivially fast in JavaScript.

**Security:** Comparison access is tenant-scoped. Segment comparisons (e.g., agent A vs agent B) respect the same permission hierarchy as the underlying data — per-agent comparison requires `agent-performance:view`. Experimental comparisons (before/after a system change) are accessible with `analytics:view`.

**Monitoring:** Track comparison query performance (p95 < 1 second for 30-day ranges). Alert if the z-test produces NaN or Infinity values (indicates division by zero — insufficient data). Monitor the distribution of effect sizes — if most comparisons show "negligible" effect, the data may be too noisy or the metrics may not be sensitive enough.
