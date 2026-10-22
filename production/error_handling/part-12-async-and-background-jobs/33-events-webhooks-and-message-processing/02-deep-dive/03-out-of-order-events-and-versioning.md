# Out-of-order Events and Versioning — Mechanics

> Part XII · Chapter 33 · Sections 33.7–33.9 (mechanics) · _Estimated reading time: 16 min_
> **Prerequisite:** [Schema Validation and Version Incompatibility](../01-concepts/03-schema-validation-and-versioning.md)

## In one sentence

Ordering is only guaranteed **per partition key**, and schemas evolve independently, so consumers
need a **monotonic version per aggregate** plus an **explicit compatibility policy** to avoid applying
stale events or crashing on new shapes.

## Why this matters in production

Two failure modes dominate event-driven systems:

1. **Stale overwrite** — a delayed `subscription.updated` (`canceled`) arrives after a newer
   `subscription.updated` (`active`) and flips the record back.
2. **Version stall** — a producer ships `v2`; the consumer throws on every event and the partition
   stops.

Both are solved by the same discipline: every event carries **identity, version, and ordering
metadata**, and the consumer uses them to decide apply/skip/quarantine.

## Ordering guarantees are local

| Transport | Guarantee |
| --------- | --------- |
| SQS standard | None |
| SQS FIFO | Per `MessageGroupId` |
| Kafka | Per partition (key → partition) |
| RabbitMQ | Per queue, single consumer |
| Pub/Sub | Per ordering key (if enabled) |
| Stripe webhooks | **None** |

If two events share an aggregate, they must share the **partition key** for order to hold:

```ts
await producer.send({
  topic: "subscriptions",
  key: event.data.subscriptionId,   // same key -> same partition -> ordered
  value: event,
});
```

Changing the key (e.g., from `tenantId` to `subscriptionId`) changes the partition assignment and
therefore the ordering. Treat partition keys as a schema-level contract.

## Versioning per aggregate

Use a **monotonically increasing version per aggregate**, not per global stream:

```ts
type DomainEvent = {
  id: string;                 // dedupe key
  type: string;
  aggregateId: string;
  aggregateVersion: number;   // 1, 2, 3... per aggregate
  occurredAt: string;         // wall clock, for humans
  schemaVersion: number;      // event shape version
  payload: unknown;
};
```

`aggregateVersion` answers "is this newer?"; `schemaVersion` answers "can I parse this?" Mixing them
is a common bug: a `v2` schema event can still be aggregate version 7.

### Apply/skip/gap decision

```ts
async function apply(event: DomainEvent) {
  const current = await projections.get(event.aggregateId);

  if (!current) {
    if (event.aggregateVersion !== 1) return buffer(event); // wait for genesis
    return write(event);
  }

  if (event.aggregateVersion <= current.version) {
    metrics.increment("event_stale");
    return; // duplicate or stale
  }

  if (event.aggregateVersion > current.version + 1) {
    return buffer(event); // gap: 1,2,4 -> wait for 3
  }

  await write(event);
  await drainBuffered(event.aggregateId, event.aggregateVersion);
}
```

```text
current version 2
incoming 2 -> skip (duplicate/stale)
incoming 3 -> apply
incoming 5 -> buffer (gap; waiting for 4)
incoming 4 -> apply 4, then drain 5
```

## Gap handling policies

| Policy | How | Use when |
| ------ | --- | -------- |
| Buffer | Hold out-of-order events with a TTL | Gaps are short and memory is bounded |
| Refetch | Read the aggregate from the source of truth | Source is authoritative and fast |
| Retry later | Nack/requeue with delay | Gaps resolve on redelivery |
| Ignore | Apply newer, accept a missing intermediate | Events are snapshots, not deltas |

Buffer memory must be bounded per aggregate and per key, with a TTL; otherwise a permanently missing
event becomes a slow memory leak.

## Schema versioning and upcasting

```ts
function normalize(raw: RawEvent): NormalizedEvent {
  switch (raw.schemaVersion) {
    case 1: return upcastV1ToV2(raw);
    case 2: return raw as NormalizedEvent;
    default: throw new UnsupportedEventVersion(raw.type, raw.schemaVersion);
  }
}
```

| Change | Compatibility | Action |
| ------ | ------------- | ------ |
| Add optional field | Backward compatible | Ignore in old consumers |
| Add required field | Breaking | New major schema version |
| Rename field | Breaking | New major + dual-write window |
| Change type | Breaking | New field + migration |
| Add enum value | Usually compatible | Default branch + metric |
| Remove field | Breaking | Deprecation window |

Consumers should support **N and N−1** for at least one deploy cycle. Producers should not remove a
field until consumers have stopped reading it (observability on field access helps).

## Worked example — Acme subscriptions

Acme's producer keys by `tenantId`. A tenant with 10k subscriptions shares one partition, and a hot
subscription dominates the partition. A delayed `canceled` for subscription A arrives after a newer
`active` for the same subscription because retries reordered them within the partition.

```ts
// Producer: key by the aggregate, not the tenant.
await producer.send({ topic: "subscriptions", key: sub.id, value: toEvent(sub, version++) });

// Consumer: version guard + gap buffer.
async function onEvent(e: DomainEvent) {
  const local = await projections.get(e.aggregateId);
  if (local && e.aggregateVersion <= local.version) return;          // stale
  if (local && e.aggregateVersion > local.version + 1) return buffer(e);
  await projections.upsert({ ...e, version: e.aggregateVersion });
}
```

After the change, per-subscription order held, stale events were dropped, and partition hot-spotting
dropped because the key cardinality increased.

## Version negotiation for webhooks

Webhook providers often expose an API version per endpoint. Pin it:

- Stripe sends `api_version` on the event; your endpoint's configured version determines the shape.
- Store the version with the raw event; parse using the schema for that version.
- On upgrade, run old and new parsers in parallel (shadow mode) before switching.
- Keep raw events so you can re-parse after a parser fix.

## Key data / numbers

- Kafka ordering is **per partition**; keys determine the partition.
- SQS FIFO ordering is per `MessageGroupId`; throughput per group is limited.
- Stripe webhook order is **not guaranteed**; `event.created` is a coarse timestamp.
- A version gap buffer should have a TTL (e.g., **30 s–5 min**) and a per-key size cap.
- Support at least **two schema versions** during a rolling deploy.
- Hot partition risk: one key handling >10% of traffic is a common Kafka warning threshold.

## Real-world use case — Checkout

Checkout's `payment_intent.succeeded` and `charge.refunded` were keyed by `orderId`. A refund event
was retried and arrived after a later `succeeded` event, flipping an order from `refunded` back to
`paid`. The fix added `aggregateVersion` derived from the provider event sequence and a state machine
that rejects backward transitions (`refunded` is terminal). Late events became no-ops, and finance
stopped seeing refunded orders reappear as paid.

## Trade-offs

| Strategy | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| Partition by aggregate | Strong per-entity order | More partitions | Default |
| Version guard | Tolerates disorder | Needs version source | Shared topics |
| Gap buffer | Preserves exact order | Memory, latency | Strict workflows |
| Snapshot events | Order-insensitive | Larger payloads | State projections |
| Refetch on gap | Authoritative | Load on source | Critical entities |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Key by the aggregate id | Key by tenant for per-entity order |
| Version every aggregate | Rely on arrival order |
| Buffer gaps with a TTL | Buffer forever |
| Upcast old schema versions | Branch the whole handler per version |
| Quarantine unknown versions | Crash the consumer |
| Keep raw events | Reparse from a lossy projection |

## Common mistakes

- **Using wall-clock arrival as version** — arrival order is the unreliable part.
- **Global version instead of per-aggregate** — gaps look permanent.
- **Unbounded gap buffer** — memory leak on a lost event.
- **Changing partition key** — silently breaks ordering guarantees.
- **No `schemaVersion` field** — impossible to route parsers.

## Checklist

- [ ] Does every event carry `id`, aggregate id, aggregate version, and schema version?
- [ ] Is the partition key the aggregate id where order matters?
- [ ] Does the consumer skip stale versions?
- [ ] Are gaps buffered with a TTL/bound or refetched?
- [ ] Are old schema versions upcast, not branched?
- [ ] Are unknown versions quarantined?
- [ ] Is at least N−1 supported during deploys?
- [ ] Are raw events retained for re-parsing?

## Related

- [Schema Validation and Version Incompatibility](../01-concepts/03-schema-validation-and-versioning.md)
- [Delivery Guarantees, Duplicates, and Ordering](../01-concepts/02-delivery-guarantees-duplicates-and-ordering.md)
- [Consumer Isolation and Eventual Consistency](../01-concepts/05-consumer-isolation-and-eventual-consistency.md)
- [Schema Validation and Versioning](../01-concepts/03-schema-validation-and-versioning.md)
