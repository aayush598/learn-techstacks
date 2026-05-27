# Section 02: Cost Per Contact Calculations

## Overview

Cost per contact (CPC) calculations provide the unit economics foundation for campaign ROI analysis. Every outbound call incurs multiple cost components: telephony costs (carrier origination, termination, minute rates), agent time costs (hourly wage × call duration + after-call work time), platform costs (per-seat licensing, API usage, storage), compliance costs (DNC scrubbing, consent storage), and overhead allocation (management, facilities, technology infrastructure). Accurate CPC calculation requires tracking all these components at the individual call level and aggregating them up through campaign, team, and organizational hierarchies.

The complexity arises from mixed cost types: direct variable costs (telephony minutes scale linearly with call volume), indirect variable costs (agent time has step-function costs based on shift scheduling), and fixed costs (platform licensing doesn't change with volume). CPC calculations must attribute fixed and semi-fixed costs appropriately to avoid distortion at different volume levels. A campaign running at 10,000 calls/day has very different per-unit economics than one at 100 calls/day due to fixed cost absorption.

## Architecture

```
                  Cost Per Contact Calculation Pipeline

  Cost Component Sources                  Cost Allocation Engine
  +------------------+                  +-----------------------+
  | Telephony Usage  |                  | Direct Cost           |
  | (Carrier CDRs)   | ---+             | (Per-call attribution)|
  +------------------+    |             |                       |
  +------------------+    +--->         | Minutes × Rate = Cost |
  | Agent Time Logs  |    |    +------->+-----------------------+
  | (ACW, Talk, Hold)| ---+    |        | Indirect Cost         |
  +------------------+         |        | (Allocation by volume)|
  +------------------+    +----+        |                       |
  | Platform Usage   |    |    +------->+-----------------------+
  | (API calls,      | ---+             | Fixed Cost            |
  |  Storage, Seats) |                  | (Equal split,         |
  +------------------+                  |  or by utilization)   |
                                        +-----------------------+
  +------------------+                             |
  | Compliance Costs | ---+                        v
  | (Scrubbing,      |    |             +-----------------------+
  |  Consent Store)  |    +--->         | Cost Aggregator       |
  +------------------+                  | (Per-campaign,        |
                                        |  Per-day, Per-contact)|
                                        +-----------------------+
```

## Design Decisions

- **Activity-based costing (ABC) over simple average cost:** ABC assigns costs based on actual resource consumption at the call level. Telephony costs are driven by duration and destination; agent costs are driven by talk time, hold time, and after-call work; platform costs are driven by feature usage. Simple average costing hides inefficiencies and produces misleading CPC for campaigns with different call profiles. Trade-off: ABC requires detailed instrumentation and increases calculation complexity.

- **Fully loaded cost reporting with drill-down to marginal cost:** Default reporting shows fully loaded CPC (including fixed cost allocation) for true profitability analysis, but provides drill-down to marginal cost (incremental cost of one more call) for capacity decisions. Operations teams use marginal cost for "should we dial more?" decisions; finance uses fully loaded cost for P&L reporting. Trade-off: maintaining both views doubles calculation requirements and can cause confusion if users don't understand the difference.

- **Time-weighted agent cost allocation:** Agent cost per call accounts for total handle time (talk + hold + after-call work) × agent effective hourly rate (including benefits, overhead). This prevents quick calls from appearing cheap when they still consume agent availability and prevent handling of other calls. Trade-off: time-weighted costing requires accurate agent status tracking and can be gamed by agents who rush after-call work.

## Implementation Approach

```
interface CostComponents {
  telephony: {
    origination: number;    // Per-minute cost from carrier
    termination: number;    // Per-minute cost to destination
    surcharges: number;     // Regulatory/911 fees
    total: number;
  };
  agent: {
    talkTimeCost: number;   // Agent hourly rate × talk minutes / 60
    holdTimeCost: number;   // Agent hourly rate × hold minutes / 60
    acwCost: number;        // After-call work time cost
    total: number;
  };
  platform: {
    apiCalls: number;       // Per-API-call cost
    storage: number;        // Recording storage cost
    licensing: number;      // Per-seat license allocation
    total: number;
  };
  compliance: {
    scrubbing: number;      // DNC scrub per-contact cost
    consentStorage: number;
    total: number;
  };
  overhead: number;         // Allocated management/tech overhead
  totalCost: number;
}

class CostCalculator {
  async calculateCostPerContact(callId) {
    const components = await Promise.all([
      this.getTelephonyCost(callId),
      this.getAgentCost(callId),
      this.getPlatformCost(callId),
      this.getComplianceCost(callId)
    ]);
    const overhead = await this.getAllocatedOverhead(callId);

    const totalCost = components.reduce((sum, c) => sum + c.total, 0) + overhead;
    return { components, overhead, totalCost };
  }

  async getCampaignCostPerContact(campaignId, dateRange) {
    const calls = await this.queryEngine.query(`
      SELECT
        count(*) as total_calls,
        sum(telephony_cost) as telephony,
        sum(agent_cost) as agent,
        sum(platform_cost) as platform,
        sum(compliance_cost) as compliance,
        sum(overhead_cost) as overhead
      FROM call_costs
      WHERE campaign_id = {campaignId}
        AND call_date BETWEEN {start} AND {end}
    `, { campaignId, ...dateRange });

    return {
      totalCalls: calls.total_calls,
      totalCost: calls.telephony + calls.agent + calls.platform + calls.compliance + calls.overhead,
      costPerContact: (calls.telephony + calls.agent + calls.platform + calls.compliance + calls.overhead) / calls.total_calls
    };
  }
}
```

## Open-Source Tools

| Tool | License | Purpose |
|------|---------|---------|
| **ClickHouse** (Apache 2.0) | Analytics | Cost event storage and aggregation |
| **TimescaleDB** (TSL) | Time-series | Cost time-series analysis |
| **Apache ECharts** (Apache 2.0) | Visualization | Cost breakdown charts |
| **PostgreSQL** (PostgreSQL) | OLTP | Cost configuration and rate tables |

## Production Considerations

**Scaling:** Cost calculation per call can be computationally expensive. Pre-calculate costs during call completion using a background job worker, storing results in a materialized cost table. For historical re-calculation (rate changes, retroactive adjustments), use a batch reprocessing pipeline that can handle millions of calls without impacting active cost tracking.

**Security:** Cost data is commercially sensitive. Implement row-level security to restrict cost visibility to authorized roles (finance, campaign managers for their campaigns, executives). Agent-level cost breakdown should be accessible only to managers and HR, not peer agents.

**Monitoring:** Track cost per contact trends over time, cost component distribution, cost outliers (calls with abnormally high telephony or agent costs), and cost allocation accuracy. Alert when CPC exceeds budgeted CPC by more than 20% for a rolling 7-day window.
