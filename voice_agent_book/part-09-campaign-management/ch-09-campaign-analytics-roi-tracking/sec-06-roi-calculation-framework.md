# Section 06: ROI Calculation Framework

## Overview

The ROI (Return on Investment) calculation framework provides a standardized methodology for measuring campaign profitability across the entire organization. ROI is calculated as (Revenue Attributed - Total Cost) / Total Cost × 100, expressed as a percentage. A campaign that generates $50,000 in revenue at a cost of $10,000 has a 400% ROI. While the basic formula is simple, accurate implementation requires careful definition of what counts as "revenue" (immediate transactional revenue, LTV, or both), what counts as "cost" (direct costs only or fully loaded), and what time horizon to use for measurement.

The framework supports multiple ROI perspectives: campaign-level ROI (is this individual campaign profitable?), portfolio ROI (is our campaign mix generating target returns?), marginal ROI (does increasing spend on this campaign generate proportional returns?), and comparative ROI (which campaigns generate the best return per dollar spent?). Each perspective informs different decisions — campaign-level ROI guides campaign activation/deactivation, portfolio ROI guides budget allocation, and marginal ROI guides spend optimization. The system also computes breakeven analysis (how many conversions needed to recover costs) and payback period (how long until cumulative revenue exceeds cumulative cost).

## Architecture

```
                 ROI Calculation Framework

   +------------------+     +------------------+
   | Revenue Data     |     | Cost Data        |
   | • Transactional  |     | • Telephony      |
   | • LTV estimates  |     | • Agent time     |
   | • Attribution    |     | • Platform       |
   |   weights        |     | • Compliance     |
   +------------------+     +------------------+
           |                        |
           v                        v
   +------------------------------------------+
   |         ROI Calculation Engine           |
   |                                          |
   |  ROI = (Revenue - Cost) / Cost × 100     |
   |                                          |
   |  Variants:                               |
   |  • Direct ROI (direct costs only)        |
   |  • Fully Loaded ROI (all costs)          |
   |  • LTV ROI (includes lifetime value)     |
   |  • Marginal ROI (incremental analysis)   |
   |  • Breakeven (units to recover cost)     |
   |  • Payback Period (time to break even)   |
   +------------------------------------------+
           |                        |
           v                        v
   +------------------+     +------------------+
   | ROI Reports      |     | ROI Dashboards   |
   | • Campaign ROI   |     | • Portfolio view |
   | • Comparative    |     | • Trend analysis |
   | • Trend analysis |     | • What-if sims   |
   +------------------+     +------------------+
```

## Design Decisions

- **Tiered ROI reporting (Direct / Fully Loaded / LTV) with unified view:** The default dashboard shows all three tiers side-by-side so users understand the range of ROI values depending on cost and revenue assumptions. Direct ROI answers "should we keep dialing?"; Fully Loaded ROI answers "is this campaign worth running?"; LTV ROI answers "what is the long-term value of acquiring customers through this channel?" Trade-off: multiple ROI values can create confusion — clear labeling and guidance is essential.

- **Campaign comparison ROI with statistical significance:** When comparing ROI across campaigns, the system computes confidence intervals around each ROI estimate and flags comparisons where the difference is not statistically significant at the 95% confidence level. This prevents overinvestment in campaigns that appear to have higher ROI due to random variation rather than true performance differences. Trade-off: statistical significance requirements may delay ROI-based decisions until sufficient data accumulates.

- **Time-phased ROI with cumulative tracking:** ROI is calculated over multiple time horizons (7-day, 30-day, 90-day, cumulative-to-date) and displayed as a cumulative curve showing how ROI improves over time as revenue accrues while costs remain fixed. This reveals the payback period — the point where cumulative revenue crosses cumulative cost. Trade-off: time-phased tracking adds complexity to the data model and requires long-term event storage.

## Implementation Approach

```
interface ROIRequest {
  campaignId: string;
  dateRange: { start: number; end: number };
  costModel: 'direct' | 'fully_loaded';
  revenueModel: 'transactional' | 'ltv' | 'both';
  timeHorizon?: number;  // Days for LTV projection
}

interface ROIResult {
  campaignId: string;
  totalCost: number;
  totalRevenue: number;
  roi: number;                // (Revenue - Cost) / Cost × 100
  breakevenUnits: number;     // Conversions needed to break even
  paybackPeriod: number;      // Days to cumulative breakeven
  confidenceInterval: {
    lower: number;             // 95% CI lower bound
    upper: number;             // 95% CI upper bound
  };
  components: {
    telephonyCost: number;
    agentCost: number;
    platformCost: number;
    complianceCost: number;
    overheadCost: number;
    transactionalRevenue: number;
    ltvRevenue: number;
  };
}

class ROICalculator {
  async calculateROI(request: ROIRequest): Promise<ROIResult> {
    const costs = await this.costService.getCampaignCosts(
      request.campaignId, request.dateRange, request.costModel
    );
    const revenue = await this.revenueService.getCampaignRevenue(
      request.campaignId, request.dateRange, request.revenueModel
    );

    const totalCost = Object.values(costs).reduce((a, b) => a + b, 0);
    const totalRevenue = Object.values(revenue).reduce((a, b) => a + b, 0);

    const roi = totalCost > 0 ? ((totalRevenue - totalCost) / totalCost) * 100 : 0;
    const avgRevenuePerConversion = revenue.transactionalRevenue / (
      await this.getConversionCount(request.campaignId, request.dateRange)
    );
    const breakevenUnits = avgRevenuePerConversion > 0
      ? Math.ceil(totalCost / avgRevenuePerConversion) : Infinity;

    return {
      campaignId: request.campaignId,
      totalCost,
      totalRevenue,
      roi,
      breakevenUnits,
      paybackPeriod: await this.computePaybackPeriod(request),
      confidenceInterval: this.computeConfidenceInterval(costs, revenue),
      components: { ...costs, ...revenue }
    };
  }
}
```

## Open-Source Tools

| Tool | License | Purpose |
|------|---------|---------|
| **ClickHouse** (Apache 2.0) | Analytics | ROI data aggregation |
| **Apache ECharts** (Apache 2.0) | Visualization | ROI waterfall charts |
| **PostgreSQL** (PostgreSQL) | OLTP | ROI configuration and assumptions |
| **dbt** (Apache 2.0) | Transformation | ROI calculation models |

## Production Considerations

**Scaling:** ROI calculations aggregate cost and revenue data across potentially millions of calls and conversions. Pre-compute daily ROI snapshots for each campaign in materialized views. For ad-hoc what-if analysis (changing assumptions), use approximate query techniques (sampling) with explicit accuracy warnings. Implement ROI calculation caching with campaign-level cache invalidation when new data arrives.

**Security:** ROI data is among the most sensitive business metrics. Implement role-based access with minimum role of "campaign manager" to view campaign ROI. Executive dashboards should show aggregate portfolio ROI with drill-down permission checks. Encrypt ROI data at rest. Maintain audit log of all ROI report access.

**Monitoring:** Track ROI calculation completeness (have all cost and revenue components been received for the period?), ROI variance (week-over-week ROI changes exceeding 25%), breakeven point trends, and payback period trends. Alert when campaign ROI drops below minimum threshold (configurable per campaign, default 0%) for 3 consecutive days, as this signals a campaign that may need to be paused.
