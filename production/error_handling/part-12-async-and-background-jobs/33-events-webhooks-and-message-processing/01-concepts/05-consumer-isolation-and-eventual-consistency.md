# Consumer Isolation, DLQ, Partial Batches, and Eventual Consistency

> Part XII · Chapter 33 · Sections 33.6, 33.13–33.17 · _Estimated reading time: 19 min_
> **Prerequisite:** [Webhook Signatures, Retries, and Timeouts](./04-webhook-signatures-retries-timeouts.md)

## In one sentence

One poison event must not stop the stream, one failing record must not fail the whole batch, and every
downstream projection must be designed for a window of **eventual consistency** with an explicit
**compensation** path.

## Why this matters in production

Message systems amplify small mistakes. A single unparseable record in a 1,000-record batch can cause
the entire batch to be retried, re-applying 999 good records. A consumer group that shares fate across
event types means a bug in `invoice.disputed` stops `invoice.paid`. And a projection that assumes
synchronous consistency shows users stale or contradictory data for minutes. Isolation, partial-batch
reporting, and explicit consistency semantics are how you keep blast radius small.

## 33.6 — Poison events

A poison event fails deterministically and will never succeed on retry:

| Cause | Example |
| ----- | ------- |
| Malformed envelope | Missing `id`, invalid JSON |
| Unsupported version | `v3` when consumer knows `v1`/`v2` |
| Invalid payload | `amount` is a string |
| Unknown type | A new event the consumer cannot handle |
| Bad reference | `tenantId` no longer exists |
| Handler bug | Null dereference on a specific shape |

Unlike transient failures, poison events should go to the **DLQ/quarantine quickly** rather than
consume the retry budget. Retrying them only delays the inevitable and blocks the partition.

```ts
if (isNonRetryable(err) || err instanceof UnsupportedEventVersion) {
  await dlq.publish({ event: raw, code: toCode(err), consumer: CONSUMER_ID });
  return; // ack the original, do not requeue
}
```

## 33.13 — Consumer isolation

Consumers fail together when they share fate. Isolate along these axes:

| Axis | Shared-fate risk | Isolation |
| ---- | ---------------- | --------- |
| Event type | One bad type stalls all | Separate consumer groups/topics |
| Tenant | Noisy/broken tenant affects all | Per-tenant partition key + concurrency cap |
| Batch | One record fails the batch | Partial-batch response |
| Dependency | One provider exhausts the pool | Bulkhead per dependency |
| Handler | One exception kills the loop | Per-record try/catch |
| Rebalance | One slow handler delays the group | `max.poll.interval.ms` tuning |

```ts
// Per-record isolation inside a batch.
const failures: BatchItemFailure[] = [];

for (const record of batch.records) {
  try {
    await handle(record);
  } catch (err) {
    if (isRetryable(err)) failures.push({ itemIdentifier: record.messageId });
    else await dlq.publish(record, err); // poison: quarantine, do not retry
  }
}

return { batchItemFailures: failures }; // only retryable failures are redelivered
```

AWS Lambda's SQS integration supports exactly this **partial batch response** shape. Without it, any
exception causes the entire batch to be retried.

## 33.14 — DLQ and replay for events

The same principles as Chapter 32 apply, with event-specific nuances:

1. **DLQ envelope includes the raw event and consumer id.**
2. **Group by event type + error code** during triage.
3. **Replay into the same consumer** (not the producer) after a consumer fix.
4. **Replay is idempotent** because the dedupe key is the event id.
5. **Unknown-version events may be replayed after deploying the new consumer.**

```text
DLQ record:
{
  "consumer": "BillingProjector",
  "eventId": "evt_1P...",
  "type": "invoice.paid",
  "version": 2,
  "code": "UNSUPPORTED_EVENT_VERSION",
  "attempts": 4,
  "raw": { ... },
  "quarantinedAt": "2026-10-21T09:22:10Z"
}
```

## 33.15 — Partial batch failure

A batch can partially succeed. Do **not** convert a partial success into a full failure or a full
success:

| Record | Result | Action |
| ------ | ------ | ------ |
| r1 | success | ack |
| r2 | transient failure | retry (report in failures) |
| r3 | permanent/poison | DLQ, then ack |
| r4 | success | ack |

```ts
type BatchResult = { batchItemFailures: Array<{ itemIdentifier: string }> };
```

Rules:

1. **Return only retryable failures** in `batchItemFailures`.
2. **Quarantine poison records** and do not include them in the retry list.
3. **Commit successes** before returning; a retry of the batch must not redo them.
4. **Keep per-record idempotency** because a batch retry may redeliver all records.
5. **Bound batch size** so one retry does not replay thousands of good records.

## 33.16 — Eventual consistency

Event-driven projections are eventually consistent by construction. The interval between the write
and the projection is the **consistency window**.

| Read pattern | Problem | Mitigation |
| ------------ | ------- | ---------- |
| Read-your-writes | User writes, immediately reads projection | Read from source, or wait/poll |
| Cross-entity join | Order projected, customer not yet | Denormalize or join source |
| Counters/aggregates | Lagging totals | Label as "as of," recompute |
| Search | Document not indexed yet | Index synchronously or show "processing" |
| Billing entitlement | Paid but not yet entitled | Grace window / entitlement from source |

Communicate the window explicitly:

```ts
type ProjectionMeta = { asOf: string; lagSeconds: number };

res.json({ items: await projections.list(), meta: { asOf: new Date().toISOString(), lagSeconds } });
```

> ⚠️ **Hazard.** A UI that says "payment successful" while the entitlement projection lags by 30 s
> will generate support tickets. Either read entitlement from the source on the success page, or show
> "activating…" until the projection catches up.

## 33.17 — Compensation downstream

If a downstream step fails after an event was projected, you cannot "unconsume" the event. You
compensate:

| Completed effect | Compensation |
| ---------------- | ------------ |
| Entitlement granted | Revoke / set `past_due` |
| Invoice marked paid | Reopen invoice / credit |
| Inventory reserved | Release reservation |
| Notification sent | Send correction |
| Search doc indexed | Delete/tombstone document |

```ts
async function onPaymentFailed(event: PaymentFailedV1) {
  await entitlements.revoke(event.data.tenantId, { reason: "payment_failed" });
  await notifications.sendPaymentFailed(event.data.tenantId);
}
```

Compensation rules:

1. **Compensation is an event-driven handler too** — idempotent, deduped, retryable.
2. **Order matters**: compensate in reverse dependency order.
3. **Some effects are irreversible** — prefer corrections and an audit trail.
4. **Do not compensate a successful effect twice** — use the same event-id dedupe.
5. **Alert on failed compensation**; it leaves observable inconsistency.

## Worked example — BillingProjector partial batch

A 100-record batch contains 98 valid `invoice.paid` events, one with an unknown `status`, and one
that hits a transient DB timeout.

```ts
for (const record of batch) {
  try {
    await projector.apply(record);
  } catch (err) {
    if (err instanceof UnsupportedStatus) {
      await dlq.publish(record, err);          // poison, ack
    } else if (isRetryable(err)) {
      failures.push({ itemIdentifier: record.messageId }); // retry only this
    } else {
      await dlq.publish(record, err);          // permanent
    }
  }
}
return { batchItemFailures: failures };
```

Result: 99 records are acked (98 applied + 1 quarantined), one is retried. Under the old
all-or-nothing behavior, the entire batch retried, re-applying 98 invoices and double-crediting them.

## Key data / numbers

- AWS Lambda SQS partial batch response: `{ batchItemFailures: [{ itemIdentifier }] }`.
- Kafka `max.poll.records` default **500**; one poison record can block offset commit for the batch.
- Kafka `max.poll.interval.ms` default **300000 ms** (5 min); slow batches trigger rebalance.
- SQS batch max **10** messages per receive (standard); Lambda batches can be larger.
- Typical projection lag target: **< 5 s** for interactive reads, minutes for analytics.
- DLQ replay rate: start **1–10 msg/s**, ramp on green.

## Real-world use case — Acme SaaS

Acme's `BillingProjector` shared one consumer for invoices, subscriptions, and usage. A new
`invoice.disputed` event type threw an unhandled error, stalling the partition for 6 hours; all billing
projections for the affected shard froze. They split consumers by event family, added a
default-quarantine path for unknown types, and implemented per-record partial batch responses. The
next unknown type was quarantined in seconds while invoice and subscription projections continued.

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| All-or-nothing batch | Simple | Re-applies successes | Tiny batches |
| Partial batch | Minimal retry | More code | Default for batches |
| Per-type consumers | Isolation | More infra | Mixed event families |
| Ignore unknown types | No stalls | Silent loss | Explicitly out of scope |
| Quarantine unknown | No stalls, recoverable | Triage load | Default |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Isolate per-record failures | Let one record fail the batch |
| Report only retryable failures | Retry poison records |
| Quarantine poison events | Loop until attempts exhaust |
| Label eventual-consistency windows | Promise synchronous reads |
| Compensate completed effects | Assume you can unconsume |
| Split consumers by event family | Share fate across all types |

## Common mistakes

- **All-or-nothing batch handling** — re-applies 99 good records.
- **Poison events in the retry list** — batch never succeeds.
- **No quarantine for unknown types** — partition stalls.
- **UI reads a lagging projection** — false failures and support tickets.
- **Compensation without dedupe** — double refunds.
- **Shared consumer for unrelated types** — one bug stops everything.

## Checklist

- [ ] Is there per-record isolation in batch consumers?
- [ ] Does the consumer return partial batch failures?
- [ ] Are poison/unknown events quarantined, not retried?
- [ ] Is there a DLQ with event id, type, version, and consumer id?
- [ ] Is replay idempotent and rate-limited?
- [ ] Is the consistency window documented and surfaced?
- [ ] Do downstream failures have a compensation path?
- [ ] Are compensation handlers idempotent and monitored?

## Related

- [Event Consumer Partial Batch and DLQ](../03-practical-examples/02-event-consumer-partial-batch-and-dlq.md)
- [Delivery Guarantees, Duplicates, and Ordering](./02-delivery-guarantees-duplicates-and-ordering.md)
- [Chapter 32 — Partial Completion and Failure Contracts](../../32-background-jobs-queues-and-scheduled-tasks/01-concepts/05-partial-completion-and-failure-contracts.md)
- [Chapter 33 Reference](../05-reference/README.md)
