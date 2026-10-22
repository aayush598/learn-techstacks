# Chapter 33 — Reference

> Part XII · Chapter 33 · all sections · _Estimated reading time: 12 min_

## Ack / reject matrix

| Broker / source | Success | Retry | Dead-letter | Notes |
| --------------- | ------- | ----- | ----------- | ----- |
| SQS | `DeleteMessage` | don't delete | redrive policy | visibility-based |
| Kafka | commit offset | don't commit | app-level DLQ topic | per partition |
| RabbitMQ | `basic.ack` | `basic.nack(requeue=true)` | dead-letter exchange | `x-death` header |
| Pub/Sub | `ack()` | `nack()` | dead-letter topic | ack deadline |
| HTTP webhook | `2xx` | `5xx` | sender retry policy | `4xx` = don't retry |
| Lambda + SQS | omit from `batchItemFailures` | list message id | redrive policy | partial batch |

## Webhook checklist

| Check | Value / rule |
| ----- | ------------ |
| Signature header | `Stripe-Signature` (`t`, `v1`) |
| Algorithm | HMAC-SHA256 over `"{t}.{raw_body}"` |
| Timestamp tolerance | **300 s** (Stripe default) |
| Compare | constant-time (`timingSafeEqual`) |
| Body | **raw bytes**, not parsed JSON |
| Ack target | **< 100 ms p99** |
| Dedupe key | `event.id` |
| Ack semantics | `200` = recorded; `5xx` = retry; `4xx` = invalid |
| Retention | keep raw events for audit/replay |

## Event envelope contract

```json
{
  "id": "evt_01HX...",
  "type": "invoice.paid",
  "schemaVersion": 2,
  "aggregateId": "inv_123",
  "aggregateVersion": 7,
  "occurredAt": "2026-10-21T09:22:10Z",
  "producer": "billing-service",
  "payload": { "amountCents": 4900, "currency": "usd" }
}
```

| Field | Purpose |
| ----- | ------- |
| `id` | Dedupe key |
| `type` | Routing / handler selection |
| `schemaVersion` | Parser selection / compatibility |
| `aggregateId` | Ordering partition key |
| `aggregateVersion` | Stale/gap detection |
| `occurredAt` | Human ordering, audit (not a version) |
| `producer` | Ownership / debugging |

## Dedupe decision table

| Effect | Dedupe technique | Atomic with effect |
| ------ | ---------------- | ------------------ |
| DB row | `INSERT ... ON CONFLICT (event_id)` | ✅ same txn |
| Aggregate update | inbox table + update in one txn | ✅ |
| External payment | provider idempotency key | ✅ at provider |
| Email | durable sent table + claim | ✅ in DB, provider not |
| Search index | doc id = event id | ✅ upsert |
| Cache | `SET NX` + TTL | ❌ best-effort |

## Retry classification for events

| Class | Retry | DLQ | Examples |
| ----- | ----- | --- | -------- |
| Transient | ✅ | on exhaustion | timeout, 429, 503, `40001` |
| Input | ❌ | ✅ | invalid JSON, schema mismatch |
| Version | ❌ | ✅ | unsupported `schemaVersion` |
| Business | ❌ | ✅ | tenant suspended, entitlement |
| Programming | ❌ | ✅ + alert | `TypeError`, assertion |
| Duplicate | n/a | ❌ | already processed |

## Out-of-order handling

| Arrival | Current | Action |
| ------- | ------- | ------ |
| v = current | same | skip (duplicate) |
| v < current | newer | skip (stale), metric |
| v = current + 1 | in order | apply |
| v > current + 1 | gap | buffer with TTL or refetch |
| v = 1, no record | genesis | apply |
| v > 1, no record | missing genesis | buffer / retry |

## Webhook status-code guide

| Code | When | Sender retries? |
| ---- | ---- | --------------- |
| `200`/`202` | Signature valid, event durably recorded | No |
| `400` | Bad signature, bad JSON, invalid envelope | Usually no |
| `401`/`403` | Unknown signing key / forbidden | Usually no |
| `404` | Wrong endpoint | Usually no |
| `409` | Optional: duplicate (if you choose) | Usually no |
| `429` | Overloaded, with `Retry-After` | Yes |
| `500`/`503` | Internal/transient failure | Yes |

## Eventual-consistency playbook

| Read path | Strategy |
| --------- | -------- |
| Read-your-writes | Read source of truth, or poll projection |
| Dashboards | Show `asOf` + lag |
| Entitlements | Evaluate from billing source during grace |
| Search | Index synchronously for critical docs |
| Cross-service joins | Denormalize or accept lag |
| Billing totals | Compute from ledger, not projection |

## Chapter glossary

| Term | Meaning |
| ---- | ------- |
| **At-least-once** | Delivery may duplicate but not lose (with retention) |
| **Effectively-once** | At-least-once delivery + idempotent processing |
| **Dedupe key** | Stable event identity used to suppress duplicates |
| **Inbox** | Durable table recording processed event ids |
| **Poison event** | Event that fails deterministically on every delivery |
| **Partial batch failure** | Per-record failure reporting so only failed records retry |
| **Outbox** | Table of events committed with state, relayed to a broker |
| **Upcasting** | Transforming an old schema version into the current internal shape |
| **Quarantine** | A DLQ/topic for events that cannot be processed yet |
| **Eventual consistency** | Projections converge after a bounded lag |
| **Compensation** | Business-level correction of a completed downstream effect |

## Related

- [Chapter 33 Do's and Don'ts](../04-dos-and-donts/README.md)
- [Chapter 32 Reference](../../32-background-jobs-queues-and-scheduled-tasks/05-reference/README.md)
- [Chapter 28 — Idempotency](../../../part-11-retry-and-resilience/28-idempotency-and-duplicate-operation-safety/README.md)
- [Glossary](../../../GLOSSARY.md)
