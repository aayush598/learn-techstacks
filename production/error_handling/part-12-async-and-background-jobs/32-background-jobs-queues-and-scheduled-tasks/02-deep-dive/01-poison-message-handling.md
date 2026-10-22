# Poison Message Handling — Mechanics

> Part XII · Chapter 32 · Sections 32.7–32.9, 32.17 (mechanics) · _Estimated reading time: 16 min_
> **Prerequisite:** [Poison Messages, DLQ, and Replay](../01-concepts/03-poison-messages-dlq-and-replay.md)

## In one sentence

Poison handling is a **receive-count-driven eviction** from the live queue into a quarantine, backed
by an alarm and a replay procedure — the queue must be able to stop trying even when your handler
cannot decide.

## Why this matters in production

The handler usually *cannot* know a message is poison on the first attempt: a `503` and a `TypeError`
look different, but a transient outage and a bad payload both fail now. The queue, however, knows how
many times the message has been delivered. `maxReceiveCount` is therefore the reliable poison
detector, and the DLQ is where the message waits for a human instead of blocking the pipeline.

## The redelivery loop

```text
        ┌──────────────────────────────────────────────┐
        │                                              │
        ▼                                              │
  ┌──────────┐  receive   ┌──────────┐  handler fails  │
  │ visible  │ ─────────▶ │ in-flight│ ────────────────┘
  └──────────┘            └──────────┘   (no delete/ack)
        ▲                       │
        │ visibility timeout    │ receiveCount > maxReceiveCount
        │ expires               ▼
        │                 ┌───────────┐
        └─────────────────│   DLQ     │
                          └───────────┘
```

Key nuance: `maxReceiveCount` counts **receives**, not failures. Every time the message becomes
visible and is handed to a consumer, the count increments. A worker crash without a delete also
increments it on redelivery.

## SQS visibility timeout mechanics

- When a consumer receives a message, it becomes **invisible** for the queue's visibility timeout.
- If the consumer deletes it before the timeout, it is gone.
- If not, it becomes visible again with an incremented `ApproximateReceiveCount`.
- `ChangeMessageVisibility` extends or shortens the lease for one message (max 12 h total).
- The redrive policy moves the message to the DLQ when `ApproximateReceiveCount` exceeds
  `maxReceiveCount`.

```json
{
  "QueueUrl": "https://sqs.us-east-1.amazonaws.com/123456789012/export-jobs",
  "Attributes": {
    "VisibilityTimeout": "300",
    "RedrivePolicy": "{\"deadLetterTargetArn\":\"arn:aws:sqs:us-east-1:123456789012:export-dlq\",\"maxReceiveCount\":\"5\"}"
  }
}
```

> ⚠️ **Hazard.** If the visibility timeout is shorter than the job's runtime, the message is
> redelivered *while the first worker is still running*. The receive count climbs due to slowness,
> not poison, and the job lands in the DLQ even though nothing was wrong with it.

## Distinguishing poison from slow from flaky

| Pattern | Receive count | Error code | Last attempt result |
| ------- | ------------- | ---------- | ------------------- |
| Poison | High | **Same every time** | Same failure |
| Slow / lease too short | High | Timeout / none | Still running elsewhere |
| Flaky dependency | Medium | Varies (429/503) | Sometimes succeeds |
| Crash loop | High | None (process dies) | Worker restarts |

Only the first should be treated as a data problem. The second needs a longer lease or a heartbeat.
The third needs backoff and circuit breaking. The fourth needs crash-loop detection that ties the
crash to the message being processed.

## RabbitMQ comparison

RabbitMQ does not have a receive-count redrive policy. Instead:

- A consumer `nack`s without `requeue`, and the message routes to a **dead-letter exchange** configured
  via `x-dead-letter-exchange`.
- A `x-message-ttl` or `x-max-length` on the queue can also expire/overflow messages to the DLX.
- To emulate a max-receive-count, track a header (`x-death` count) or use a retry queue with TTL.

```yaml
queues:
  export-jobs:
    arguments:
      x-dead-letter-exchange: export-dlx
      x-dead-letter-routing-key: export-dlq
  export-retry-5s:
    arguments:
      x-message-ttl: 5000
      x-dead-letter-exchange: ""          # back to default exchange
      x-dead-letter-routing-key: export-jobs
```

## Kafka comparison

Kafka has **no DLQ primitive**. Consumers implement it:

1. Attempt processing.
2. On poison, publish the record + error metadata to a `*-dlq` topic.
3. Commit the offset past the bad record (otherwise the partition is stuck forever).

```java
try {
    handler.process(record);
    consumer.commitSync();
} catch (NonRetryableException e) {
    producer.send(new ProducerRecord<>("export-dlq", record.key(), dlqEnvelope(record, e)));
    consumer.commitSync(); // move past the poison record
}
```

This is a deliberate trade: you **do not retry** at the Kafka layer; retries live in a separate topic
or in application state.

## Preventing poison in the first place

| Layer | Control |
| ----- | ------- |
| Producer | Validate the payload against a schema before enqueue |
| Queue | Message size limit, content-type attribute |
| Consumer | Validate again at the boundary; reject invalid input as non-retryable |
| Contract | Versioned schema; tolerate unknown fields |
| Deploy | Canary consumers before rolling out a schema change |

Validation at enqueue is the cheapest fix: a malformed message never enters the retry loop.

## Worked example — poison detection with SQS

```ts
async function handle(message: SQSMessage) {
  const receiveCount = Number(message.attributes.ApproximateReceiveCount ?? "0");
  const job = parse(message.body); // may throw on malformed JSON

  try {
    await exports.run(job);
    await sqs.deleteMessage({ QueueUrl, ReceiptHandle: message.receiptHandle });
  } catch (err) {
    const code = toCode(err);

    if (isNonRetryable(err)) {
      await dlq.send({ reason: "permanent", code, receiveCount, body: message.body });
      await sqs.deleteMessage({ QueueUrl, ReceiptHandle: message.receiptHandle });
      return;
    }

    // Let it redeliver; the redrive policy handles maxReceiveCount.
    throw err;
  }
}
```

For permanent errors we skip the remaining retries and move straight to the DLQ. For transient
errors we rely on the queue's receive count, which also covers crashes the handler never sees.

## Replay safety checklist (mechanics)

1. **Pause the producer** for the affected job type if replay could race new work.
2. **Group by `errorCode`**; replay only groups whose cause is fixed.
3. **Reuse `jobId`** as the idempotency key.
4. **Rate-limit** with a token bucket; watch the destination queue depth.
5. **Observe** success rate and duplicate-effect metrics for the first N messages.
6. **Record** operator, count, and time range in the incident.

## Key data / numbers

- SQS `maxReceiveCount` accepted range: 1–1000; practical **3–5**.
- SQS visibility timeout: 0 s–12 h; default 30 s.
- SQS `ApproximateReceiveCount` is an **approximate** attribute; treat it as a signal, not a
  transaction boundary.
- DLQ retention: up to 14 days; replay must happen before expiry.
- SQS FIFO dedupe interval: 5 minutes — a replay after that can duplicate.
- RabbitMQ `x-death` header records the queue and count of dead-letterings.

## Real-world use case — WebhookIngest

`WebhookIngest` published parsed Stripe events to an SQS queue processed by `BillingProjector`. A
single event with an unexpected `object` type threw a `TypeError`; with no DLQ, the FIFO group stalled
and **all** billing projections for that customer stopped for 9 hours. The team added
`maxReceiveCount: 4`, a DLQ with a 14-day retention, an alarm, and a non-retryable classification for
unknown event types. The next unknown type was quarantined in under a minute, and billing continued.

## Trade-offs

| Mechanism | Pros | Cons | When to use |
| --------- | ---- | ---- | ----------- |
| `maxReceiveCount` | Queue-driven, crash-safe | Counts slow jobs too | Default on SQS |
| Handler-side poison check | Immediate | Misses crashes | Permanent errors |
| TTL-based DLQ | Time-bounded | Not error-aware | Time-sensitive work |
| Manual triage queue | Full control | Operational cost | High-value jobs |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Set `maxReceiveCount` and a DLQ | Retry forever |
| Alarm on DLQ depth | Discover poison via customer report |
| Classify permanent errors immediately | Burn all attempts on a schema error |
| Keep the lease longer than the job | Let redelivery race the first worker |
| Replay in rate-limited batches | Replay the whole DLQ at once |

## Common mistakes

- **No DLQ on FIFO queues** — one message blocks the group.
- **Visibility timeout shorter than runtime** — false poison, duplicate work.
- **DLQ with no retention/owner** — messages expire untriaged.
- **Replaying before the fix** — the second pass returns to the DLQ.
- **Deleting poison messages as "cleanup"** — data loss without a record.

## Checklist

- [ ] Does the queue have a redrive policy with a sensible `maxReceiveCount`?
- [ ] Is the visibility timeout longer than the typical job runtime (or is there a heartbeat)?
- [ ] Are permanent errors short-circuited to the DLQ?
- [ ] Does the DLQ have retention and an alarm?
- [ ] Can a crash-looping job be identified from the message being processed?
- [ ] Is replay rate-limited, idempotent, and audited?

## Related

- [Poison Messages, DLQ, and Replay](../01-concepts/03-poison-messages-dlq-and-replay.md)
- [At-least-once vs Exactly-once](./02-at-least-once-vs-exactly-once.md)
- [ExportJob Worker with DLQ and Backoff](../03-practical-examples/01-exportjob-worker-with-dlq-and-backoff.md)
- [Chapter 33 — Events, Webhooks, and Message Processing](../../33-events-webhooks-and-message-processing/README.md)
