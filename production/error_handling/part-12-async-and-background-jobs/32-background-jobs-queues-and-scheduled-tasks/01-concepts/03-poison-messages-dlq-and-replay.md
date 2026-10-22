# Poison Messages, DLQ, and Replay

> Part XII · Chapter 32 · Sections 32.7, 32.8, 32.17 · _Estimated reading time: 18 min_
> **Prerequisite:** [Retries, Backoff, and Exhaustion](./02-retries-backoff-and-exhaustion.md)

## In one sentence

A **poison message** fails deterministically on every delivery, so it must be **evicted by a receive
count into a dead-letter queue**, inspected, fixed, and replayed — never retried forever at the head
of the queue.

## Why this matters in production

Queues are usually ordered enough that a poison message blocks the partition, or at minimum burns
worker capacity on every redelivery. One malformed payload can stall a tenant's exports, inflate
error rates, and page on-call repeatedly. The DLQ is the pressure valve: it keeps the main queue
flowing while preserving the bad message for analysis. But a DLQ without a replay procedure is just
a slower data-loss mechanism.

## 32.7 — Poison messages

A poison message is characterized by **deterministic failure**:

- It fails with the same error on every attempt (schema mismatch, `TypeError`, invalid FK).
- Retries do not change the outcome because the input is wrong, not the environment.
- It can block ordered partitions or monopolize a worker.

How poison messages arise:

| Cause | Example |
| ----- | ------- |
| Producer bug | Missing required field in the job payload |
| Schema drift | Consumer expects `v2`, message is `v1` |
| Corrupt data | Truncated JSON, invalid UTF-8, oversized body |
| Referential gap | `tenantId` no longer exists |
| Code bug | Null dereference in the handler |
| Poison combination | Specific tenant + specific date triggers an edge case |

### Detect it by behavior, not by guess

The reliable signal is **repeated failure with the same code on the same message**. Track
`receiveCount` and the last error code; if `receiveCount` exceeds a threshold and the code is
identical, treat it as poison.

```ts
if (message.receiveCount >= 3 && errorCode === message.lastErrorCode) {
  await dlq.send({ message, reason: "poison", attempts: message.receiveCount });
}
```

## 32.8 — Dead-letter queue (DLQ)

A DLQ is a separate queue for messages that exhausted retries. It is **not** a trash can; it is a
quarantine with three obligations: **retain**, **observe**, **replay**.

### Design rules

1. **Separate queue per source** — so replay targets and retention can differ.
2. **Alarm on non-empty** — a growing DLQ is an incident, not a dashboard.
3. **Preserve the original payload and metadata** — attempt count, error code, timestamps.
4. **Same retention as or longer than the source** — messages must survive until triage.
5. **Access-controlled** — replay is a privileged operation.

### SQS redrive policy

```json
{
  "deadLetterTargetArn": "arn:aws:sqs:us-east-1:123456789012:export-dlq",
  "maxReceiveCount": 5
}
```

SQS moves the message automatically once it has been received `maxReceiveCount` times without
being deleted. The DLQ receives the message **body unchanged**; the receive count is available via
the `ApproximateReceiveCount` message attribute.

### DLQ record envelope

```json
{
  "originalQueue": "export-jobs",
  "jobType": "ExportJob",
  "jobId": "job_01HX...",
  "tenantId": "ten_42",
  "attempts": 5,
  "errorCode": "EXPORT_INVALID_QUERY",
  "errorClass": "input",
  "firstFailedAt": "2026-10-21T09:12:04Z",
  "lastFailedAt": "2026-10-21T09:22:10Z",
  "payload": { "query": "...", "format": "csv" }
}
```

Keep the payload plus enough context to reproduce the failure offline.

## 32.17 — DLQ replay

Replay is a **write operation**: it puts messages back into the live queue. It must be deliberate,
auditable, and idempotent.

### Replay procedure

```text
1. Triage      → group by errorCode, tenant, jobType
2. Fix cause   → deploy code, correct data, restore dependency
3. Dry run     → replay one message to a staging queue
4. Approve     → named operator + change ticket
5. Replay      → batch, rate-limited, oldest first
6. Verify      → watch success rate and duplicate side effects
7. Purge/retain→ delete or archive replayed messages
```

### Replay safely

```ts
async function replayDLQ(dlqUrl: string, limit: number, ratePerSec: number) {
  const messages = await dlq.receive({ max: limit, waitSeconds: 20 });

  for (const m of messages) {
    const record = parseDlqRecord(m);
    // Preserve the original job id so idempotency keys stay stable.
    await jobs.requeue(record.jobId, record.payload, {
      resetAttempts: true,
      idempotencyKey: record.jobId,
      source: "dlq-replay",
    });
    await dlq.delete(m);
    await sleep(1000 / ratePerSec);
  }
}
```

Rules:

1. **Rate-limit** the replay. Replaying 50k messages at once re-creates the outage.
2. **Reuse the original job id** as the idempotency key so the work is not duplicated.
3. **Reset or preserve attempts deliberately** — resetting gives a fresh budget; preserving prevents
   infinite replay loops.
4. **Never replay without fixing the cause.** Otherwise the messages return to the DLQ.
5. **Record who replayed what** (operator, timestamp, count).
6. **Skip non-replayable classes** (e.g., a deleted tenant) and archive them with a reason.

### Replay is not guaranteed once

Because the queue is at-least-once, a replayed job can still run twice. That is acceptable only if
the job is idempotent (Chapter 28). If it is not, fix idempotency before replaying.

## Worked example — ExportJob DLQ

`ExportJob` payloads include a SQL `query` string. A producer bug emits `query: null`. The handler
throws `TypeError: Cannot read properties of null` on every delivery. Without a DLQ, the message
redelivers forever, and because the queue is FIFO with a single group, every tenant's export stalls.

```yaml
# Infrastructure policy (conceptual)
queue: export-jobs
  visibilityTimeout: 300s
  retention: 4d
  redrivePolicy:
    deadLetterTarget: export-dlq
    maxReceiveCount: 5
dlq: export-dlq
  retention: 14d
  alarm: ApproximateNumberOfMessagesVisible > 0 for 5m
```

After the DLQ alarm fires, on-call groups the messages by `errorCode`, confirms all are
`EXPORT_INVALID_QUERY`, fixes the producer to reject null queries, and replays the affected messages
with a 10 msg/s limit. The job id is preserved, so each export runs once.

## Key data / numbers

- SQS `maxReceiveCount` typical: **3–5** before DLQ redrive.
- SQS DLQ retention: up to **14 days** (same limit as source queues).
- SQS standard queues do not guarantee order; FIFO queues block a message group while unacked.
- RabbitMQ dead-lettering uses `x-dead-letter-exchange` and optional `x-message-ttl`.
- Kafka has no native DLQ; consumers publish poison records to a dedicated topic and commit past them.
- Replay rate recommendation: **start at 1–10 msg/s**, ramp only after success rate is green.

## Real-world use case — Acme SaaS

Acme's FIFO `ExportJob` queue stalled for 6 hours when one message with a malformed `dateRange`
looped. There was no DLQ; the only mitigation was to delete the message blindly, losing the export.
After adding `maxReceiveCount: 5`, a separate DLQ, an alarm, and a replay CLI that preserves job ids,
the next poison message was quarantined in minutes, the queue kept flowing, and the fixed message was
replayed once with no duplicate rows.

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| Infinite retry | No data loss | Blocks queue, burns capacity | Never |
| Drop after N attempts | Unblocks queue | Silent loss | Only for disposable work |
| DLQ + manual replay | Safe, inspectable | Operational cost | Default for real jobs |
| DLQ + automatic replay | Fast recovery | Replays before fix, loops | Only known-transient windows |
| Per-message TTL to DLQ | Bounded wait | Time-based, not error-based | Time-sensitive work |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Evict poison messages by receive count | Retry deterministically failing messages forever |
| Alarm on DLQ depth | Let the DLQ fill silently |
| Preserve payload + metadata | Store only "job failed" |
| Fix the cause before replaying | Blindly replay the whole DLQ |
| Rate-limit replay | Replay 50k messages at once |
| Reuse the original job id | Generate new ids and duplicate work |

## Common mistakes

- **No DLQ at all** — one bad message stalls a FIFO group indefinitely.
- **DLQ but no alarm** — discovered only when a customer complains.
- **Replaying without idempotency** — duplicate exports, invoices, or emails.
- **Resetting attempts on every replay** — an infinite replay loop.
- **DLQ retention shorter than triage time** — evidence expires before anyone looks.

## Checklist

- [ ] Is there a `maxReceiveCount` / retry cap that routes to a DLQ?
- [ ] Is the DLQ a separate queue with its own retention?
- [ ] Does the DLQ record include payload, attempts, error code, and tenant?
- [ ] Is there an alarm on DLQ depth?
- [ ] Is there a documented, rate-limited replay procedure?
- [ ] Is replay idempotent (original job id as key)?
- [ ] Is replay access-controlled and audited?
- [ ] Are non-replayable messages archived with a reason?

## Related

- [Poison Message Handling — Mechanics](../02-deep-dive/01-poison-message-handling.md)
- [Retries, Backoff, and Exhaustion](./02-retries-backoff-and-exhaustion.md)
- [Chapter 28 — Idempotency](../../../part-11-retry-and-resilience/28-idempotency-and-duplicate-operation-safety/README.md)
- [ExportJob Worker with DLQ and Backoff](../03-practical-examples/01-exportjob-worker-with-dlq-and-backoff.md)
