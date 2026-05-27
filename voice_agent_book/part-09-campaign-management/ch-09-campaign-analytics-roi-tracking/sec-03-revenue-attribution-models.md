# Section 03: Revenue Attribution Models

## Overview

Revenue attribution models determine how credit for a conversion or sale is assigned across the multiple touchpoints a customer may have with the business. In an outbound calling context, a single customer might receive multiple calls across different campaigns (a sales call followed by a payment reminder followed by a satisfaction survey), interact with other channels (website, email, chat), and eventually convert through any of these touchpoints. Attribution models answer the question: which campaign deserves credit for this revenue?

The choice of attribution model dramatically impacts how campaign performance is evaluated. A first-touch model gives all credit to the campaign that made initial contact, favoring top-of-funnel campaigns. A last-touch model credits the final interaction before conversion, favoring closing campaigns. Linear models distribute credit equally across all touchpoints. Time-decay models give more credit to recent interactions. Position-based models assign 40% to first and last touchpoints, splitting the remaining 20% across middle interactions. Each model has implications for campaign strategy, budget allocation, and agent incentives.

## Architecture

```
                 Revenue Attribution Engine

  Touchpoint Events (Call, Email, Web Visit, Chat, Purchase)
       |
       v
  +---------------------------+
  | Touchpoint Collection     |  Gather all interactions for
  | (Per customer journey)    |  a customer within lookback window
  +---------------------------+
       |
       v
  +---------------------------+
  | Attribution Model         |  First-touch, Last-touch, Linear,
  | Selector                  |  Time-decay, Position-based, Custom
  +---------------------------+
       |
       v
  +---------------------------+
  | Weight Calculation        |  Assign attribution weight to
  |                           |  each touchpoint (0.0 - 1.0)
  +---------------------------+
       |
       v
  +---------------------------+
  | Revenue Distribution      |  Distribute revenue × weight
  | (Per touchpoint)          |  to each campaign/contact
  +---------------------------+
       |
       v
  +---------------------------+
  | Materialized Campaign     |  Pre-computed: revenue by campaign
  | Revenue Views             |  by attribution model, by time period
  +---------------------------+
```

## Design Decisions

- **Multi-model support with default model per campaign:** Each campaign can have a default attribution model that reflects its role in the customer journey (top-of-funnel = first-touch, closing = last-touch), but all models are calculated and available for comparison. Reporting dashboards default to the campaign model but allow switching. Trade-off: calculating and storing all models for all campaigns multiplies storage and computation by the number of models (typically 5-6).

- **Customizable lookback window per campaign type:** The attribution lookback window (maximum time between first touchpoint and conversion) varies by product lifecycle. High-consideration purchases (insurance, education) might use 90-day windows; low-consideration purchases (consumer goods) might use 7-day windows. The window determines which touchpoints are included in the journey. Trade-off: different windows make cross-campaign comparison difficult and require careful labeling in reports.

- **Transactional revenue + LTV-based revenue dual reporting:** Attribution reports on both immediate transactional revenue (the sale amount on conversion day) and estimated Lifetime Value (LTV) revenue (projected total customer value over 12/24/36 months). LTV-based attribution provides a more complete picture of campaign value but introduces estimation uncertainty. Trade-off: LTV models require ongoing calibration against actual retention data to maintain accuracy.

## Implementation Approach

```
type AttributionModel = 'first_touch' | 'last_touch' | 'linear' | 'time_decay' | 'position_based';

interface Touchpoint {
  id: string;
  contactId: string;
  campaignId: string;
  channel: 'call' | 'email' | 'web' | 'chat' | 'sms';
  timestamp: number;
  type: 'outbound' | 'inbound' | 'automated';
  metadata: Record<string, any>;
}

interface AttributionResult {
  touchpointId: string;
  campaignId: string;
  contactId: string;
  conversionId: string;
  revenue: number;
  weight: number;
  attributedRevenue: number; // revenue * weight
  model: AttributionModel;
}

class AttributionEngine {
  async attributeRevenue(
    conversion: { contactId: string; revenue: number; timestamp: number },
    model: AttributionModel,
    lookbackWindow: number
  ): Promise<AttributionResult[]> {
    const touchpoints = await this.getTouchpointsInWindow(
      conversion.contactId,
      conversion.timestamp - lookbackWindow,
      conversion.timestamp
    );

    if (touchpoints.length === 0) {
      return [{ touchpointId: 'unattributed', weight: 1.0, attributedRevenue: conversion.revenue }];
    }

    const weights = this.calculateWeights(touchpoints, model);
    return touchpoints.map((tp, i) => ({
      ...tp,
      conversionId: conversion.id,
      revenue: conversion.revenue,
      weight: weights[i],
      attributedRevenue: conversion.revenue * weights[i],
      model
    }));
  }

  private calculateWeights(touchpoints: Touchpoint[], model: AttributionModel): number[] {
    switch (model) {
      case 'first_touch':
        return touchpoints.map((_, i) => i === 0 ? 1.0 : 0.0);
      case 'last_touch':
        return touchpoints.map((_, i) => i === touchpoints.length - 1 ? 1.0 : 0.0);
      case 'linear':
        return touchpoints.map(() => 1.0 / touchpoints.length);
      case 'time_decay':
        return this.calculateTimeDecayWeights(touchpoints);
      case 'position_based':
        return this.calculatePositionWeights(touchpoints);
    }
  }
}
```

## Open-Source Tools

| Tool | License | Purpose |
|------|---------|---------|
| **ClickHouse** (Apache 2.0) | Analytics | Touchpoint event storage and attribution queries |
| **Apache Spark** (Apache 2.0) | Processing | Batch attribution for large datasets |
| **dbt** (Apache 2.0) | Transformation | Attribution model transformations |
| **Apache ECharts** (Apache 2.0) | Visualization | Model comparison charts |

## Production Considerations

**Scaling:** Full-path attribution (considering all touchpoints across all channels) is computationally expensive. Pre-compute attribution for common models using nightly batch jobs and store results in materialized views. Real-time attribution uses approximate methods (last-touch only) with full re-computation during off-peak hours. Use incremental processing (processing only new/updated touchpoints since last run) to keep batch windows manageable.

**Security:** Revenue attribution data is highly sensitive. Encrypt revenue amounts at rest. Implement strict access controls — only campaign managers, finance, and executives should see attributed revenue. Support attribution data export for external audit with tamper-evident logging.

**Monitoring:** Track attribution coverage (% of conversions successfully attributed to at least one touchpoint), model stability (variance in attributed revenue across models), attribution computation SLA (batch completion within 4 hours), and unattributed conversion rate. Alert when unattributed rate exceeds 15%, as this indicates tracking gaps.
