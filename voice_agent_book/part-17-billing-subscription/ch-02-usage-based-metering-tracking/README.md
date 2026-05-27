# Chapter 02: Usage-Based Metering & Tracking

> **Part:** 17 - Billing, Subscription & Monetization

---

## Sections

| # | Section | Description |
|---|---------|-------------|
| 01 | [Usage Event Pipeline](sec-01-usage-event-pipeline.md) | Event emission from services, event bus architecture, batch vs streaming, idempotent event processing |
| 02 | [Metering Data Model](sec-02-metering-data-model.md) | Usage records schema, meter definition, aggregation dimensions, unit types (minutes, calls, tokens) |
| 03 | [Real-Time Usage Aggregation](sec-03-real-time-usage-aggregation.md) | Redis counters, sliding window aggregation, pre-aggregated rollups, eventual consistency trade-offs |
| 04 | [Usage Event Validation](sec-04-usage-event-validation.md) | Schema validation, duplicate detection, out-of-order handling, quota check at ingestion |
| 05 | [Billing Period Alignment](sec-05-billing-period-alignment.md) | Monthly/ annual billing cycles, usage reset at period boundaries, pro-ration for mid-cycle changes |
| 06 | [Usage Deduplication](sec-06-usage-deduplication.md) | Idempotency keys, exactly-once processing, dedup window, conflict resolution |
| 07 | [Metering Latency](sec-07-metering-latency.md) | Near-real-time vs batch trade-offs, latency SLAs, eventual consistency tolerance |
| 08 | [Usage Data Reconciliation](sec-08-usage-data-reconciliation.md) | Stripe vs internal usage comparison, discrepancy detection, manual adjustment tools, audit reports |

---

## Usage Event Pipeline

```
[Service] → Emit Usage Event → Event Bus (Kafka/RabbitMQ)
                                    ↓
                          [Usage Validator]
                            ├── Schema check
                            ├── Dedup (idempotency key)
                            └── Tenant verification
                                    ↓
                          [Usage Aggregator]
                            ├── Redis counter (real-time)
                            └── ClickHouse (analytics)
                                    ↓
                          [Billing Engine]
                            └── Send metered events to Stripe
```

---

## Learning Objectives

- Design usage event pipeline with idempotent processing
- Build metering data model supporting multiple dimensions
- Implement real-time usage aggregation with Redis counters
- Create usage event validation and deduplication
- Align usage tracking with billing period boundaries
- Ensure exactly-once processing with idempotency keys
- Manage metering latency trade-offs
- Build usage data reconciliation against Stripe
