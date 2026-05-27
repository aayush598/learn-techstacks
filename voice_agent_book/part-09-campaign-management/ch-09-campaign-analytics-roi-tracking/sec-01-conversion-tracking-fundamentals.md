# Section 01: Conversion Tracking Fundamentals

## Overview

Conversion tracking fundamentals define how the system captures, attributes, and reports on desired outcomes from outbound calls. A conversion is any measurable action that results from a call — completing a sale, scheduling an appointment, collecting a payment, confirming an appointment, or completing a survey. The conversion tracking system must capture these events reliably, attribute them to the correct campaign and contact, handle multiple attribution windows (same-day, 24-hour, 7-day, custom), and support both first-touch and last-touch attribution models.

The fundamental challenge is bridging the gap between call events and business outcomes. A call happens in seconds within the voice platform, but a conversion might occur hours, days, or weeks later — perhaps on a website, in a mobile app, at a point-of-sale terminal, or during a subsequent call. The tracking system must correlate these disparate events into a unified conversion record. This requires a flexible event ingestion system, a robust identity resolution layer, configurable attribution rules, and a materialized view layer that pre-computes conversion metrics for dashboard performance.

## Architecture

```
                  Conversion Tracking Data Flow

  Call Event (Connect, Duration, Disposition, Recording)
       |
       v
  +-----------------------+
  | Identity Resolution   |  Phone, Email, Customer ID, Cookie
  | (Unify contact across |  → Unified Contact ID
  |  multiple channels)   |
  +-----------------------+
       |
       v
  +-----------------------+
  | Attribution Engine    |  Window: Same-day, 24h, 7d, 30d, Custom
  |                      |  Model: First-touch, Last-touch, Linear, Time-decay
  +-----------------------+
       |
       v
  +-----------------------+
  | Conversion Event Bus  |  Kafka / RabbitMQ
  | (Ingest external      |  Webhook, API, File Import
  |  conversion events)   |
  +-----------------------+
       |
       v
  +-----------------------+
  | Materialized Views    |  ClickHouse AggregatingMergeTree
  | (Pre-computed         |  Per-campaign, per-agent, per-day
  |  conversion metrics)  |
  +-----------------------+
```

## Design Decisions

- **Event-sourced conversion tracking over state-based tracking:** Every conversion attempt (success, failure, partial) is recorded as an immutable event with timestamp and source attribution. This enables replay, audit, and retrospective re-attribution when rules change. Trade-off: event storage grows linearly with conversion volume and requires careful data lifecycle management.

- **Configurable attribution windows per campaign rather than global setting:** Different campaign types have different conversion timeframes. A flash sale campaign might use a 2-hour window while a high-consideration purchase might use a 30-day window. Making windows campaign-configurable increases accuracy but adds complexity to cross-campaign reporting where contacts appear in multiple campaigns.

- **Probabilistic + deterministic identity resolution:** Deterministic matching uses exact phone number, email, or customer ID. Probabilistic matching uses fuzzy matching on name, address, device fingerprint, or IP address. The hybrid approach maximizes match rate while minimizing false positives. Trade-off: probabilistic matching introduces potential misattribution errors that require manual review and correction workflows.

## Implementation Approach

```
interface ConversionEvent {
  id: string;
  contactId: string;
  campaignId: string;
  callId?: string;
  type: 'sale' | 'appointment' | 'payment' | 'survey' | 'custom';
  value: number;          // Monetary value if applicable
  currency: string;
  timestamp: number;
  source: 'api' | 'webhook' | 'import' | 'system';
  attributes: Record<string, string>;
}

class ConversionTracker {
  async trackConversion(event: ConversionEvent) {
    const resolvedContact = await this.identityResolver.resolve(event);
    const attributedCall = await this.attributionEngine.findAttribution(
      resolvedContact.id,
      event.timestamp,
      event.campaignId
    );
    const enrichedEvent = {
      ...event,
      contactId: resolvedContact.id,
      callId: attributedCall?.id,
      campaignId: attributedCall?.campaignId || event.campaignId
    };
    await this.eventStore.append('conversions', enrichedEvent);
    await this.materializedViews.update(enrichedEvent);
    return enrichedEvent;
  }

  async getConversionRate(campaignId, dateRange) {
    return this.queryEngine.query(`
      SELECT
        countIf(call_id IS NOT NULL) / count(*) as conversion_rate,
        sum(value) as total_value,
        count(*) as total_conversions
      FROM conversions
      WHERE campaign_id = {campaignId}
        AND timestamp BETWEEN {start} AND {end}
    `, { campaignId, ...dateRange });
  }
}
```

## Open-Source Tools

| Tool | License | Purpose |
|------|---------|---------|
| **ClickHouse** (Apache 2.0) | Analytics | Conversion event storage and aggregation |
| **Apache Kafka** (Apache 2.0) | Streaming | Conversion event ingestion |
| **Redis** (BSD) | Cache | Attribution window member check |
| **PostgreSQL** (PostgreSQL) | OLTP | Conversion rule configuration |

## Production Considerations

**Scaling:** Attribution queries scan large event windows for matching. Index contact_id, phone, and email on conversion events. Use ClickHouse partitioning by month and sampling for approximate conversion rate queries when sub-1% error is acceptable. Implement conversion event TTL aligned with the maximum attribution window (e.g., 90 days) to bound storage growth.

**Security:** Conversion value data is sensitive — implement field-level encryption for monetary values and PII fields. Audit all conversion event modifications. Multi-tenant isolation on conversion data must prevent tenant A from viewing tenant B's conversion performance.

**Monitoring:** Track attribution success rate (% of conversions successfully attributed to a call), attribution latency (time between conversion event and attribution completion), duplicate conversion events, and conversion value outliers. Alert when attribution rate drops below 95% or when conversion value spikes beyond 3 standard deviations from the mean.
