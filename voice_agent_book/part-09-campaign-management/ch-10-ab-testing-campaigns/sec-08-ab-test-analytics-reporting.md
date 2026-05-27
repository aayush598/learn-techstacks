# Section 08: A/B Test Analytics & Reporting

## Overview

A/B test analytics and reporting provide comprehensive visibility into test performance, enabling data-driven decisions about campaign optimization. The analytics layer tracks all tests across running, completed, and archived states, providing real-time results for active tests, historical analysis for completed tests, and a learning repository that accumulates insights from all tests. The reporting system serves multiple audiences: test owners need detailed diagnostics, campaign managers need actionable recommendations, and executives need portfolio-level test ROI.

The analytics system addresses key questions for each test: Is the test progressing toward significance? Which variant is currently leading? Are there segment-specific effects (does the variant work better for certain contact types)? What is the expected value of implementing the winner? How does this test's results compare to similar tests run previously? The system also detects anomalies (unexpected allocation imbalances, metric spikes, data quality issues) that could invalidate test results.

## Architecture

```
                  A/B Test Analytics & Reporting

   Data Sources                     Serving Layer
   +------------------+            +------------------+
   | Test Registry    |            | Real-time        |
   | (PostgreSQL)     |            | Dashboard        |
   +------------------+            | (WebSocket)      |
   +------------------+   +--->    +------------------+
   | Variant Outcomes  |    |      | Historical       |
   | (ClickHouse)     |    |      | Reports          |
   +------------------+    |      | (REST API)       |
   +------------------+    |      +------------------+
   | Learning Repository|   |      | Export           |
   | (PostgreSQL)     |    |      | (CSV, PDF)       |
   +------------------+    |      +------------------+
          |                |
          v                v
   +----------------------------------------------------+
   |              Analytics Engine                       |
   |                                                    |
   |  Real-time:                                        |
   |  - Current metric differences per variant          |
   |  - Progress toward required sample size            |
   |  - Allocation balance                              |
   |  - Segment-level breakdowns                        |
   |                                                    |
   |  Historical:                                       |
   |  - Statistical significance calculations           |
   |  - Confidence intervals                            |
   |  - Segment interaction analysis                    |
   |  - Temporal effects (day-of-week, time-of-day)     |
   |                                                    |
   |  Repository:                                       |
   |  - Effect size distribution across all tests       |
   |  - Winning variants by campaign type               |
   |  - Best practices derived from test history       |
   +----------------------------------------------------+
```

## Design Decisions

- **Progressive result disclosure with peeking prevention:** The real-time dashboard shows operational metrics (sample size reached, allocation balance, segment distribution) at all times but only reveals performance comparisons at pre-registered checkpoints (typically at 25%, 50%, 75%, 100% of required sample size). Between checkpoints, the dashboard shows "Data collection in progress — results available at next checkpoint." This prevents peeking-induced stopping while providing operational visibility. Trade-off: periodic disclosure delays access to results but protects statistical validity.

- **Test learning repository with structured insight capture:** Every completed test contributes to a searchable learning repository. Results are captured with standardized metadata: test hypothesis, variables tested, effect sizes, significance levels, segments where effects were strongest, and practitioner comments. The repository enables meta-analysis (what types of changes typically produce the largest effects?) and prevents re-testing of already-answered questions. Trade-off: maintaining a learning repository requires disciplined data entry and ongoing curation to prevent duplication and contradiction.

- **Automated test summary with natural language generation:** At test completion, the system generates a plain-English summary: "Variant B (conversational opening with discount offer) showed a 12.3% improvement in conversion rate (p=0.003, 95% CI [4.1%, 20.5%]) compared to the control. The effect was strongest for warm leads (+18%) and negligible for cold leads (+2%). Recommendation: Implement Variant B for warm leads, continue testing for cold leads." This makes results accessible to non-technical stakeholders. Trade-off: auto-generated summaries may oversimplify complex results and require manual review before distribution.

## Implementation Approach

```
interface TestReport {
  testId: string;
  testName: string;
  status: 'running' | 'completed' | 'stopped';
  progress: {
    requiredSampleSize: number;
    currentSampleSize: number;
    percentageComplete: number;
    estimatedCompletionDate: number;
  };
  results?: {
    primaryMetric: { control: number; variant: number; lift: number; pValue: number; significant: boolean };
    secondaryMetrics: { name: string; control: number; variant: number; lift: number; pValue: number }[];
    segmentResults: { segment: string; value: string; lift: number; pValue: number }[];
    winner: { variantId: string; confidence: string };
    summary: string;  // NL-generated summary
  };
}

class TestAnalyticsService {
  async getTestReport(testId: string, includeResults: boolean): Promise<TestReport> {
    const test = await this.getTest(testId);
    const progress = await this.computeProgress(test);

    if (!includeResults) {
      return { testId: test.name, status: test.status, progress };
    }

    const metrics = await this.computeMetrics(test);
    const segmentAnalysis = await this.analyzeSegments(test);
    const winner = await this.winnerSelector.selectWinner(test, metrics);
    const summary = await this.generateSummary(test, metrics, winner);

    return {
      testId: test.name,
      status: 'completed',
      progress,
      results: { ...metrics, segmentResults: segmentAnalysis, winner, summary }
    };
  }

  async generateSummary(test, metrics, winner): Promise<string> {
    const lift = metrics.primaryMetric.lift;
    const pVal = metrics.primaryMetric.pValue;
    const ci = metrics.primaryMetric.confidenceInterval;
    const segments = metrics.segmentResults
      ?.filter(s => s.pValue < 0.05)
      ?.slice(0, 3);

    let summary = `${winner.variantId} showed a ${lift.toFixed(1)}% `;
    summary += `improvement in ${test.primaryMetric} `;
    summary += `(p=${pVal.toFixed(4)}, 95% CI [${ci[0].toFixed(1)}%, ${ci[1].toFixed(1)}%]).`;

    if (segments?.length > 0) {
      summary += ` The effect was strongest for `;
      summary += segments.map(s => `${s.segment}=${s.value} (+${s.lift.toFixed(1)}%)`).join(', ');
      summary += '.';
    }

    summary += ` Recommendation: ${winner.recommendation === 'auto_rollout' ? 'Implement ' + winner.variantId : winner.recommendation}`;
    return summary;
  }
}
```

## Open-Source Tools

| Tool | License | Purpose |
|------|---------|---------|
| **Apache ECharts** (Apache 2.0) | Visualization | Test result charts |
| **Recharts** (MIT) | React | React chart components |
| **ClickHouse** (Apache 2.0) | Analytics | Result aggregation |
| **PostgreSQL** (PostgreSQL) | Data store | Test registry and config |
| **Redis** (BSD) | Cache | Real-time dashboard data |

## Production Considerations

**Scaling:** Real-time test dashboards poll for updates every 5-30 seconds. Use Redis to cache computed metrics and reduce load on ClickHouse. For high-traffic campaigns (millions of contacts per day), compute test metrics asynchronously using pre-aggregated data rather than querying raw events. Provide an "export to CSV" option that triggers an async job for large result sets.

**Security:** Restrict test access to authorized users within the same tenant. Test results before they are finalized (interim peeking) should be protected. The learning repository should support anonymous aggregation (showing effect sizes without revealing specific campaign details) for cross-tenant benchmarking.

**Monitoring:** Track dashboard load times (p95 < 2s), test registration volume, completion rate (% of registered tests that complete), average time to significance, and repository utilization (searches, reads). Alert on tests running significantly longer than estimated (may indicate sample size miscalculation or traffic shortfall) and on tests where the control is outperforming all variants (may need to stop early).
