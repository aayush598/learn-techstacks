# Section 05: Funnel Analytics & Optimization

## Overview

Campaign funnel analytics break down the end-to-end call journey into discrete stages — contacts loaded, dial attempts made, calls connected, human answered, qualified leads, converted, revenue realized — and measure the conversion rate and drop-off at each stage. This decomposition reveals exactly where campaigns lose contacts and where optimization efforts will have the greatest impact. A campaign might have excellent connection rates but poor qualification rates, suggesting the targeting criteria need refinement. Another might have strong conversion among connected calls but a low connection rate, indicating list quality or dialing time issues.

Funnel optimization is the systematic process of improving conversion rates at each stage. Optimization levers are stage-specific: improving dialing window and timezone handling to increase connect rates, refining contact scoring and prioritization to improve qualification rates, enhancing agent scripts and training to boost conversion rates, and optimizing retry timing to reduce abandonments. The funnel analytics system must provide both diagnostic insights (what's happening at each stage) and prescriptive recommendations (what to do about it) to drive continuous campaign improvement.

## Architecture

```
                   Campaign Funnel Architecture

   Stage 1:           Stage 2:           Stage 3:          Stage 4:
   Contacts Loaded → Dials Attempted →  Calls Connected → Humans Answered
       |                  |                  |                  |
   Drop-off:           Drop-off:           Drop-off:           Drop-off:
   • Invalid numbers   • Timezone blocked  • Voicemail         • Wrong number
   • DNC suppressed    • Rate limited      • Busy signal       • Not interested
   • Duplicates        • Max attempts      • No answer         • Language barrier
   • Opted out          reached            • Failed/SIT tones  • Call screening
       |                  |                  |                  |
       v                  v                  v                  v
   +--------------------------------------------------------------+
   |                  Funnel Analytics Engine                      |
   |                                                               |
   |  - Stage-by-stage conversion rate calculation                 |
   |  - Drop-off cause analysis (by reason code)                   |
   |  - Trend analysis (stage rates over time)                     |
   |  - Peer benchmarking (compare to similar campaigns)           |
   |  - Optimization recommendation engine                         |
   +--------------------------------------------------------------+
       |                  |                  |                  |
       v                  v                  v                  v
   +--------------------------------------------------------------+
   |                  Optimization Levers                          |
   |                                                               |
   |  Stage 2: Adjust dialing     Stage 3: Improve AMD,       Stage 4: Better    |
   |  windows, retry timing,      adjust dialing ratio,       targeting, better  |
   |  timezone handling           pacing strategy             scripts, training  |
   +--------------------------------------------------------------+
```

## Design Decisions

- **Multi-touch attribution across funnel stages:** A single contact may enter the funnel multiple times across retry attempts. The system tracks each attempt as a separate funnel entry, enabling analysis of how conversion rates change across attempt sequence (attempt 1 vs. attempt 3). This reveals diminishing returns and helps set optimal max attempts. Trade-off: multi-touch tracking requires careful handling of contact identity across attempts.

- **Cause-coded drop-off tracking with automated root cause analysis:** Every drop-off event is tagged with a specific cause code (invalid number, timezone blocked, voicemail, busy, no answer, DNC match, opt-out, etc.). The funnel system automatically surfaces which cause codes are driving the highest drop-off at each stage and compares these against campaign benchmarks. Trade-off: detailed cause coding requires comprehensive event instrumentation throughout the dialing pipeline.

- **Optimization recommendation engine with expected impact scoring:** The system generates specific optimization recommendations (e.g., "adjust dialing start time from 8 AM to 9 AM to reduce no-answer rate") with estimated impact scores based on historical data and A/B test results. Each recommendation includes confidence level and expected magnitude of improvement. Trade-off: recommendations are only as good as the underlying data quality and may not account for external factors.

## Implementation Approach

```
interface FunnelStage {
  name: string;
  order: number;
  entryCount: number;
  exitCount: number;
  dropOffCount: number;
  conversionRate: number;        // entryCount / entryCount(previous stage)
  stageConversionRate: number;   // exitCount / entryCount
  dropOffByReason: Record<string, number>;
  avgDuration: number;           // Avg time spent in stage
}

interface FunnelAnalysis {
  campaignId: string;
  dateRange: { start: number; end: number };
  stages: FunnelStage[];
  overallConversionRate: number;
  biggestDropOffStage: string;
  optimizationRecommendations: OptimizationRecommendation[];
}

interface OptimizationRecommendation {
  stage: string;
  issue: string;
  recommendation: string;
  expectedImpact: number;       // Expected improvement in overall conversion
  confidenceLevel: 'high' | 'medium' | 'low';
  effortLevel: 'high' | 'medium' | 'low';
}

class FunnelAnalyzer {
  async analyzeFunnel(campaignId, dateRange) {
    const stages = await this.computeStages(campaignId, dateRange);
    const overallRate = stages[stages.length - 1].exitCount / stages[0].entryCount;
    const recommendations = await this.generateRecommendations(stages, campaignId);

    return {
      campaignId,
      stages,
      overallConversionRate: overallRate,
      biggestDropOffStage: this.findBiggestDropOff(stages),
      optimizationRecommendations: recommendations
    };
  }

  async generateRecommendations(stages, campaignId) {
    const recommendations = [];
    for (const stage of stages) {
      if (stage.dropOffCount > 0) {
        const stageRecommendations = await this.optimizationEngine
          .getRecommendations(stage.name, stage.dropOffByReason, campaignId);
        recommendations.push(...stageRecommendations);
      }
    }
    return recommendations.sort((a, b) => b.expectedImpact - a.expectedImpact);
  }
}
```

## Open-Source Tools

| Tool | License | Purpose |
|------|---------|---------|
| **Apache ECharts** (Apache 2.0) | Visualization | Funnel chart visualization |
| **ClickHouse** (Apache 2.0) | Analytics | Funnel stage event storage |
| **PostgreSQL** (PostgreSQL) | OLTP | Campaign configuration |
| **dbt** (Apache 2.0) | Transformation | Funnel metric transformations |

## Production Considerations

**Scaling:** Funnel queries require scanning all events within the date range and grouping by stage. Pre-aggregate funnel data into hourly materialized views. For drill-down queries (by cause code, by agent, by time of day), maintain pre-computed cubes with ClickHouse AggregatingMergeTree. Implement funnel query timeout limits to prevent expensive queries from blocking dashboard rendering.

**Security:** Funnel data may reveal campaign effectiveness that is commercially sensitive. Restrict funnel visibility to campaign owners and above. Support tenant-level data isolation with row-level security on funnel aggregation tables.

**Monitoring:** Track funnel metric freshness (max time since last materialization), query performance by funnel complexity (p95 under 2 seconds for 8-stage funnels), optimization recommendation accuracy (track implemented recommendations and their actual vs. predicted impact). Build a feedback loop where actual outcomes update recommendation models.
