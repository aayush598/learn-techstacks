# Section 04: Campaign Comparison Dashboard

## Overview

The campaign comparison dashboard enables side-by-side evaluation of multiple campaigns across key performance indicators, helping campaign managers identify top performers, diagnose underperforming campaigns, and make data-driven decisions about resource allocation. The dashboard supports comparing campaigns by type (sales vs. survey vs. reminder), by time period (current week vs. previous week, month-over-month), by team, and by channel. Core comparison metrics include cost per contact, conversion rate, revenue per call, ROI percentage, abandonment rate, connect rate, and agent utilization.

Effective comparison requires normalized metrics that account for differences in campaign difficulty, list quality, seasonality, and dialing mode. A campaign targeting "warm" leads will naturally outperform one targeting "cold" prospects — the dashboard must surface these contextual differences rather than presenting raw rankings. The system supports peer group comparison where campaigns are automatically grouped by similar characteristics (industry, contact source, dialing mode, campaign type) for more meaningful benchmarking.

## Architecture

```
                  Campaign Comparison Dashboard Architecture

  +------------------+  +------------------+  +------------------+
  | Campaign A       |  | Campaign B       |  | Campaign C       |
  | Metrics: 15      |  | Metrics: 12      |  | Metrics: 8       |
  | KPIs computed    |  | KPIs computed    |  | KPIs computed    |
  +------------------+  +------------------+  +------------------+
           |                    |                     |
           v                    v                     v
  +---------------------------------------------------------+
  |              Metrics Normalization Engine               |
  |                                                         |
  |  - Adjusts for campaign type baselines                  |
  |  - Normalizes for list quality (warm/cold ratio)        |
  |  - Adjusts for dialing mode differences                  |
  |  - Applies statistical significance testing             |
  |  - Computes percentile rankings within peer groups      |
  +---------------------------------------------------------+
           |                    |                     |
           v                    v                     v
  +---------------------------------------------------------+
  |              Comparison Data Model                       |
  |                                                         |
  |  - Side-by-side KPI grid (rows=campaigns, cols=metrics) |
  |  - Trend sparklines for each campaign/metric pair       |
  |  - Color-coded performance indicators (green/yellow/red)|
  |  - Statistical significance indicators                  |
  |  - Peer group percentile rankings                       |
  +---------------------------------------------------------+
           |
           v
  +---------------------------------------------------------+
  |              Rendering (Apache ECharts / Recharts)       |
  |                                                         |
  |  - Bar chart comparisons                                |
  |  - Radar charts for multi-dimensional comparison        |
  |  - Scatter plots for metric correlation analysis        |
  |  - Heat maps for campaign × metric matrices             |
  +---------------------------------------------------------+
```

## Design Decisions

- **Normalized metrics with raw metrics toggle:** The default view shows normalized metrics (adjusted for campaign characteristics) to enable fair comparison, but users can toggle to raw metrics to see absolute performance. Normalization adjusts for campaign type baseline, list source difficulty, seasonality factors, and dialing mode efficiency. Trade-off: normalization introduces model risk — if normalization factors are wrong, comparisons can be misleading.

- **Peer group auto-classification with manual override:** The system automatically groups campaigns into peer groups based on shared characteristics (type, channel, industry, list source) using clustering algorithms. Groups are reviewed with suggested labels. Campaign managers can manually override peer group assignments or create custom peer groups. Trade-off: auto-classification may miss nuanced similarities that human operators recognize.

- **Statistical significance indicators on all comparisons:** Every comparison between campaigns includes a statistical significance indicator (e.g., "95% confidence that Campaign A conversion rate is higher than Campaign B"). This prevents over-interpretation of differences that could be noise. Significance is computed using appropriate statistical tests based on metric distribution (z-test for rates, t-test for means). Trade-off: significance testing adds computational overhead and requires sufficient sample sizes.

## Implementation Approach

```
interface CampaignComparisonRequest {
  campaignIds: string[];
  metrics: string[];
  timeRange: { start: number; end: number };
  normalization: 'raw' | 'adjusted' | 'peer_percentile';
  peerGroupId?: string;
}

interface CampaignComparisonRow {
  campaignId: string;
  campaignName: string;
  campaignType: string;
  metrics: {
    [metricName: string]: {
      raw: number;
      adjusted: number;
      peerPercentile: number;
      trend: number[];           // Trend over time period
      significance: {            // Compared to group average
        isSignificant: boolean;
        confidenceLevel: number;
        direction: 'above' | 'below' | 'same';
      };
    };
  };
  overallRank: number;
  peerGroupId: string;
}

class CampaignComparisonService {
  async compareCampaigns(request: CampaignComparisonRequest) {
    const rawMetrics = await this.metricsService.getMetrics(
      request.campaignIds, request.metrics, request.timeRange
    );
    const peerGroups = await this.getPeerGroups(request.campaignIds);
    const normalized = await this.normalizationEngine.normalize(
      rawMetrics, peerGroups, request.normalization
    );
    return this.buildComparisonMatrix(normalized, peerGroups);
  }

  private async getPeerGroups(campaignIds: string[]) {
    return this.queryEngine.query(`
      SELECT campaign_id, campaign_type, dialing_mode, list_source, industry
      FROM campaign_profiles
      WHERE campaign_id IN ({campaignIds})
    `, { campaignIds });
  }
}
```

## Open-Source Tools

| Tool | License | Purpose |
|------|---------|---------|
| **Apache ECharts** (Apache 2.0) | Visualization | Comparison charts and radar plots |
| **Recharts** (MIT) | React | React-based chart components |
| **ClickHouse** (Apache 2.0) | Analytics | Metrics data storage |
| **PostgreSQL** (PostgreSQL) | OLTP | Campaign profile and peer group config |
| **Redis** (BSD) | Cache | Dashboard data caching |

## Production Considerations

**Scaling:** Comparison dashboards query multiple campaigns simultaneously, which can stress the analytics database. Pre-compute comparison data in hourly or nightly materialized views. Use Redis caching with 5-minute TTL for real-time dashboard views. For large comparisons (50+ campaigns), implement progressive loading — display the top 10 campaigns immediately while computing the full set asynchronously.

**Security:** Campaign comparison data should be restricted by user role and tenant. Campaign managers should only see campaigns they manage unless explicitly granted cross-campaign access. Executives should see all campaigns aggregated with drill-down permission control.

**Monitoring:** Track dashboard load times (p95 under 3 seconds for 20-campaign comparison), normalization engine health (detect drift in normalization factors), peer group clustering quality score, and user engagement (which comparisons are most frequently viewed). Alert when any metric crosses threshold boundaries for any campaign in the comparison set.
