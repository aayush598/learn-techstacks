# Practical — Event Consumer with Partial Batch Failure and DLQ

> Part XII · Chapter 33 · Sections 33.13–33.15 · _Estimated reading time: 18 min_
> **Prerequisite:** [Consumer Isolation, DLQ, Partial Batches, and Eventual Consistency](../01-concepts/05-consumer-isolation-and-eventual-consistency.md)

## Scenario

Acme's `BillingProjector` consumes a batch of up to 100 billing events from SQS via a Lambda worker
(the same pattern applies to Kafka/Kinesis). Each event updates a tenant's billing projection. The
consumer must:

- process records independently so one bad record does not fail the batch,
- retry only **transient** failures,
- quarantine **poison** records to a DLQ,
- report **partial batch failures** so SQS redelivers only failed records,
- remain idempotent under redelivery.

## The batch contract

```ts
type SqsBatch = {
  Records: Array<{
    messageId: string;
    body: string;
    attributes: { ApproximateReceiveCount?: string };
    receiptHandle: string;
  }>;
};

type BatchResponse = {
  batchItemFailures: Array<{ itemIdentifier: string }>;
};
```

Returning a `messageId` in `batchItemFailures` tells Lambda/SQS to **leave that message unacked** (it
redelivers). Messages not listed are deleted. An empty list means the whole batch succeeded.

> ⚠️ **Hazard.** Without a partial-batch response, any thrown exception causes **every** record in the
> batch to redeliver, re-applying the successes. That is how a single bad record double-bills 99
> tenants.

## Error classification

```ts
type ErrorClass = "transient" | "permanent" | "unknown";

function classify(err: unknown): ErrorClass {
  if (isTimeout(err) || isConnectionError(err)) return "transient";
  if (isHttpStatus(err, [429, 500, 502, 503, 504])) return "transient";
  if (isSqlState(err, "40001") || isSqlState(err, "40P01")) return "transient";
  if (err instanceof UnsupportedEventVersion) return "permanent";
  if (err instanceof InvalidSchema) return "permanent";
  if (err instanceof TenantNotFound) return "permanent";
  return "unknown"; // treat as permanent + alert until classified
}
```

Treat `unknown` as **permanent with an alert**, not retryable. An unclassified error retried six times
is six times the noise for the same unresolved bug.

## Step 1 — Idempotent apply

```ts
async function applyEvent(event: NormalizedEvent) {
  await db.transaction(async (tx) => {
    const claimed = await tx.query(
      `INSERT INTO consumer_inbox (consumer, event_id)
       VALUES ('BillingProjector', $1)
       ON CONFLICT DO NOTHING
       RETURNING event_id`,
      [event.id],
    );
    if (claimed.rowCount === 0) return; // duplicate: no-op

    // Version guard: ignore stale events for the same aggregate.
    const current = await tx.query(
      `SELECT version FROM billing_projection WHERE tenant_id = $1 FOR UPDATE`,
      [event.tenantId],
    );
    if (current.rows[0] && current.rows[0].version >= event.aggregateVersion) return;

    await tx.query(
      `INSERT INTO billing_projection (tenant_id, status, balance_cents, version, updated_at)
       VALUES ($1, $2, $3, $4, now())
       ON CONFLICT (tenant_id) DO UPDATE
       SET status = EXCLUDED.status,
           balance_cents = EXCLUDED.balance_cents,
           version = EXCLUDED.version,
           updated_at = now()`,
      [event.tenantId, event.status, event.balanceCents, event.aggregateVersion],
    );
  });
}
```

Inbox dedupe and projection update commit together. A redelivery is a no-op; a stale event is a no-op.

## Step 2 — Per-record isolation

```ts
export async function handler(batch: SqsBatch): Promise<BatchResponse> {
  const failures: BatchResponse["batchItemFailures"] = [];

  await Promise.all(
    batch.Records.map(async (record) => {
      const receiveCount = Number(record.attributes.ApproximateReceiveCount ?? "1");

      try {
        const raw = JSON.parse(record.body);
        const event = normalize(raw);      // validates schema + version
        await applyEvent(event);
        metrics.increment("billing_event_applied", { type: event.type });
      } catch (err) {
        const cls = classify(err);

        if (cls === "transient" && receiveCount < 5) {
          failures.push({ itemIdentifier: record.messageId }); // retry only this
          metrics.increment("billing_event_retry", { code: toCode(err) });
          return;
        }

        // Permanent, unknown, or exhausted: quarantine and ack.
        await dlq.publish({
          consumer: "BillingProjector",
          eventId: safeEventId(record),
          messageId: record.messageId,
          receiveCount,
          code: toCode(err),
          class: cls,
          body: record.body,
          quarantinedAt: new Date().toISOString(),
        });
        metrics.increment("billing_event_dlq", { code: toCode(err), class: cls });
      }
    }),
  );

  return { batchItemFailures: failures };
}
```

Why `Promise.all` here? Each record is independent and the loop catches its own errors, so there is no
unhandled rejection. If you need bounded concurrency, use a pool of 10–20 rather than 100 simultaneous
DB transactions.

## Step 3 — Batch size and timing

| Setting | Value | Reason |
| ------- | ----- | ------ |
| SQS batch size | 100 | Throughput |
| Lambda timeout | 60 s | Under the queue visibility timeout |
| Visibility timeout | 300 s | 5× the function timeout |
| `maxReceiveCount` | 5 | Redrive to DLQ |
| Per-record DB timeout | 5 s | Prevent one slow record holding the batch |
| In-flight cap | 20 | Protect the DB pool |

If the visibility timeout is shorter than the function timeout, records are redelivered while the
batch is still running, doubling the work.

## Step 4 — DLQ triage and replay

Group DLQ records by `code`:

```sql
-- Conceptual query over a DLQ table/topic dump
SELECT code, class, count(*)
FROM billing_dlq
GROUP BY code, class
ORDER BY count(*) DESC;
```

Replay after the cause is fixed:

```ts
async function replayBillingDlq(records: DlqRecord[], approve: boolean) {
  if (!approve) throw new Error("replay requires approval");

  for (const r of records) {
    if (r.class === "permanent" && !(await causeFixed(r))) continue; // skip unfixable
    await sqs.send(new SendMessageCommand({
      QueueUrl: BILLING_QUEUE_URL,
      MessageBody: r.body,                 // original event, same event_id
      MessageAttributes: { ReplayOf: { DataType: "String", StringValue: r.messageId } },
    }));
    await dlq.delete(r);
    await sleep(200);                      // ~5 msg/s
  }
}
```

Because the payload keeps the original `event_id`, replay hits the inbox dedupe and cannot double-apply.

## Step 5 — Observe consistency lag

```ts
async function projectionLagSeconds() {
  const row = await db.one(
    `SELECT extract(epoch FROM now() - max(processed_at)) AS lag
     FROM consumer_inbox WHERE consumer = 'BillingProjector'`,
  );
  metrics.gauge("billing_projection_lag_seconds", Number(row.lag ?? 0));
}
```

If the UI reads the projection, return the lag or read from the source for read-your-writes paths.

## Failure-mode review

| Event | Behavior | Result |
| ----- | -------- | ------ |
| 98 valid, 1 transient, 1 poison | Partial failures list has 1; poison DLQ'd | 99 acked, 1 retried |
| Duplicate redelivery | Inbox conflict | No-op |
| Stale version | Version guard | No-op |
| Unknown schema version | Quarantine | Batch continues |
| DB outage | All records transient | Whole batch retried |
| DLQ replay | Same event id | No double-apply |
| Function timeout | Unacked records redeliver | Idempotent reprocess |

## Real-world use case — Acme SaaS

Before partial-batch handling, one `invoice.disputed` event with an unknown status caused a
100-record batch to throw; SQS redelivered the entire batch four times, and the 99 valid `invoice.paid`
events were applied four times. Acme over-credited 37 tenants. After implementing per-record isolation,
partial-batch responses, and inbox dedupe, the same event class was quarantined once while the other
99 records committed exactly once. The incident category disappeared from the next quarter's review.

## Key data / numbers

- SQS batch size: up to **10** per `ReceiveMessage` (Lambda can receive up to **10,000** for standard
  queues, but practical batches are 10–100).
- Lambda timeout **60 s**, visibility timeout **300 s**, `maxReceiveCount` **5**.
- Partial batch response: `{ batchItemFailures: [{ itemIdentifier: messageId }] }`.
- DLQ replay rate: **~5 msg/s**, ramp on green.
- Projection lag alarm: **> 60 s** for billing reads.

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Isolate each record in try/catch | Throw out of the batch loop |
| Return only retryable failures | Include poison records in retries |
| Quarantine unknown/unsupported | Retry them until exhaustion |
| Dedupe by event id in the effect transaction | Dedupe in memory |
| Keep the original payload for replay | Rewrite the event on replay |
| Bound per-record DB time | Let one record hold the batch |

## Checklist

- [ ] Does the handler return `batchItemFailures`?
- [ ] Is every record isolated from the others?
- [ ] Are transient, permanent, and unknown errors classified?
- [ ] Are poison/unknown records quarantined with context?
- [ ] Is dedupe committed with the projection?
- [ ] Is there a version guard for stale events?
- [ ] Is the visibility timeout longer than the function timeout?
- [ ] Is replay idempotent and rate-limited?

## Related

- [Consumer Isolation, DLQ, Partial Batches, and Eventual Consistency](../01-concepts/05-consumer-isolation-and-eventual-consistency.md)
- [At-least-once and Idempotent Consumers — Mechanics](../02-deep-dive/02-at-least-once-and-idempotent-consumers.md)
- [WebhookIngest Dedupe and Signature](./01-webhookingest-dedupe-and-signature.md)
- [Chapter 32 — Background Jobs](../../32-background-jobs-queues-and-scheduled-tasks/README.md)
