# Job Lifecycle and Failure States

> Part XII · Chapter 32 · Sections 32.1–32.3, 32.9, 32.18 · _Estimated reading time: 18 min_
> **Prerequisite:** [Chapter 31 — Asynchronous Error Handling](../../31-asynchronous-error-handling/README.md)

## In one sentence

A job is a **durable state machine**, not a function call: it moves through queued → running →
(succeeded | failed | cancelled | dead), and the queue must be able to recover the machine after a
crash at any point.

## Why this matters in production

If a job exists only as "a message and a handler," crash recovery is undefined. Was it processed?
Should the message be redelivered? Did the side effect happen? Without explicit states, teams answer
these questions by reading logs — after the fact. Explicit lifecycle states give the queue, the
worker, and the operator a shared vocabulary, and they make the difference between "retry" and
"stop" a stored decision rather than a guess.

## 32.1 — The job lifecycle

```text
             enqueue                 claim                  finish
  ┌────────┐ ───────▶ ┌────────┐ ─────────▶ ┌──────────┐ ─────────▶ ┌───────────┐
  │ queued │          │ ready  │            │ running  │            │ succeeded │
  └────────┘          └────────┘            └──────────┘            └───────────┘
                           ▲                     │  │
                           │  retry (delay)      │  │ terminal error / exhausted
                           └─────────────────────┘  ▼
                                              ┌──────────────────────────┐
                                              │ failed  │ cancelled      │
                                              └──────────────────────────┘
                                                       │ after DLQ
                                                       ▼
                                              ┌────────────────┐
                                              │ dead (in DLQ)  │
                                              └────────────────┘
```

| State | Meaning | Who sets it | Observable as |
| ----- | ------- | ----------- | ------------- |
| `queued` | Accepted, not yet due | Producer | `GET /jobs/:id` |
| `ready` | Due and available to a worker | Queue | queue depth |
| `running` | Claimed by a worker | Worker | heartbeat / lease |
| `succeeded` | Completed durably | Worker | job record |
| `failed` | Terminal failure, may be replayed | Worker/queue | error metric |
| `cancelled` | Stopped deliberately | Operator/client | audit log |
| `dead` | Exhausted attempts, parked in DLQ | Queue | DLQ depth alarm |

> **`failed` and `dead` are not synonyms.** `failed` is a terminal outcome you may retry manually.
> `dead` means the queue gave up automatically and a human must decide.

### The lease is the state

Most queues do not store an explicit `running` state; they use a **lease** (visibility timeout,
ack deadline, lock). If the worker does not renew or ack before the lease expires, the message
becomes visible again and is redelivered. This is why **crashes look like retries** and why every
job must assume it can run twice.

## 32.2 — Job boundaries

A job is the unit that the queue can retry, so its boundary determines the retry semantics:

| Boundary choice | Consequence |
| --------------- | ----------- |
| One job per record (1 export row) | Fine-grained retries, high overhead |
| One job per batch (10k rows) | Efficient, but one poison row fails the batch |
| One job per tenant operation | Clean idempotency key, larger blast radius |
| One job per external API call | Many retries, risk of duplicate side effects |

Pick the boundary at a point where **re-running has a well-defined business meaning**. "Regenerate
the invoice PDF for invoice `inv_123`" is a good unit. "Process everything since yesterday" is a
bad unit — retrying it reprocesses unrelated records.

## 32.3 — Retryable vs terminal

Classify **before** deciding to retry:

| Class | Examples | Action |
| ----- | -------- | ------ |
| Transient | network reset, `503`, `429`, deadlock (`40001`) | Retry with backoff |
| Configuration | bad credentials, missing bucket, wrong region | Terminal; page an operator |
| Input/data | malformed payload, schema mismatch, missing FK | Terminal; DLQ + fix data |
| Business | tenant suspended, quota exceeded | Terminal; notify product/tenant |
| Programming | `TypeError`, null dereference | Terminal; alert engineering |
| Capacity | pool exhausted, disk full | Retry with delay + backpressure |

```ts
type JobErrorClass = "transient" | "config" | "input" | "business" | "programming";

function classifyJobError(err: unknown): JobErrorClass {
  if (isTimeout(err) || isHttpStatus(err, [429, 502, 503, 504])) return "transient";
  if (isSqlState(err, "40001") || isSqlState(err, "40P01")) return "transient"; // serialization/deadlock
  if (isSchemaError(err)) return "input";
  if (isAuthError(err)) return "config";
  return "programming";
}

const retryable = classifyJobError(err) === "transient";
```

> ⚠️ **Hazard.** Retrying a **programming error** is the fastest way to turn one bug into a queue
> full of identical failures. A `TypeError` will fail the same way 100 000 times.

## 32.9 — The failed state

A failed job must be **queryable, not just logged**. Store at minimum:

```json
{
  "jobId": "job_01HX...",
  "type": "ExportJob",
  "status": "failed",
  "attempt": 4,
  "maxAttempts": 5,
  "errorCode": "EXPORT_S3_UNAVAILABLE",
  "retryable": true,
  "tenantId": "ten_42",
  "firstFailedAt": "2026-10-21T09:12:04Z",
  "lastFailedAt": "2026-10-21T09:19:31Z",
  "nextAttemptAt": "2026-10-21T09:27:31Z"
}
```

Rules for the failed state:

1. **Keep the original error and the last error separately** if retries transform it.
2. **Record the attempt number** so exhaustion is explainable.
3. **Expose it to the product** so the UI can say "export failed" instead of spinning forever.
4. **Do not delete the input payload** until the job is terminal and retention allows it.

## 32.18 — Scheduled tasks

Scheduled (cron) tasks are jobs with a **time trigger** and no external message. They have extra
failure modes:

| Failure mode | Cause | Mitigation |
| ------------ | ----- | ---------- |
| Overlap | Previous run still active | Distributed lock / `FOR UPDATE SKIP LOCKED` |
| Missed run | Scheduler down or worker busy | Catch-up window / idempotent backfill |
| Duplicate run | Two scheduler instances fire | Leader election / idempotency key by window |
| Clock drift | Timezone/DST mistakes | UTC schedules, explicit timezone config |
| Silent failure | No one reads the logs | Job record + "no success in N minutes" alarm |

```ts
// Idempotency key derived from the schedule window, not the wall clock.
const windowKey = `nightly-export:${tenantId}:${dayInUtc}`;
await jobs.enqueueOnce("NightlyExport", { tenantId, day: dayInUtc }, { key: windowKey });
```

A scheduled task that fails should be **visible as a failed job**, not as a missing log line. The
most common production incident is not a crashing cron; it is a cron that silently stopped running.

## Worked example — ExportJob lifecycle

```ts
async function processExport(job: Job<ExportPayload>) {
  await jobs.markRunning(job.id);                // running (lease held)

  try {
    await exports.run(job.data);                 // the actual work
    await jobs.markSucceeded(job.id);            // terminal success
  } catch (err) {
    const cls = classifyJobError(err);
    const retryable = cls === "transient";
    const exhausted = job.attempt >= job.maxAttempts;

    if (retryable && !exhausted) {
      await jobs.scheduleRetry(job.id, { attempt: job.attempt + 1, delayMs: backoff(job.attempt) });
      throw err;                                 // nack -> redelivery later
    }

    await jobs.markFailed(job.id, {
      errorCode: toCode(err),
      retryable,
      attempt: job.attempt,
      exhausted,
    });
    throw err;                                   // queue routes to DLQ if exhausted
  }
}
```

The handler does not decide the final queue mechanics; it records a **state + classification** and
lets the queue apply its policy.

## Key data / numbers

- SQS visibility timeout default **30 s**, maximum **12 h**; redelivery after lease expiry.
- SQS `maxReceiveCount` (redrive policy) commonly **3–5** before DLQ.
- SQS message retention default **4 days**, maximum **14 days**; DLQ same limit.
- Celery `acks_late=True` acks after execution, improving durability at the cost of duplicates.
- Kubernetes `terminationGracePeriodSeconds` default **30 s**; keep job checkpoints within it.
- Cron overlap protection commonly uses a lock TTL slightly longer than the longest run.

## Real-world use case — Acme SaaS

Acme's `ExportJob` had no explicit failed state; the worker caught errors, logged them, and acked the
message. Exports vanished with a `200` in the job-status API. Support told customers to "try again"
with no diagnostic. After introducing lifecycle states and a persisted failure record, the status
endpoint returned `failed` with `EXPORT_S3_UNAVAILABLE`, support could confirm the S3 outage, and
retries recovered automatically when the bucket policy was fixed.

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| Ack immediately, log errors | Simple | Silent loss | Never for real work |
| Ack after success | Durable | Duplicates on crash | Default job semantics |
| Explicit state store | Queryable, auditable | Extra writes | User-facing jobs |
| Queue-native only | Less code | Limited history | Internal best-effort work |
| Scheduled with lock | Prevents overlap | Lock complexity | Cron/catch-up jobs |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Give every job a terminal state | Leave jobs "running" forever |
| Classify errors before retrying | Retry every exception |
| Persist failure context | Only log it |
| Use schedule-window idempotency keys | Key on `Date.now()` |
| Alarm on missed scheduled runs | Assume cron always fires |
| Store attempt count | Discard retry history |

## Common mistakes

- **`failed` vs `dead` conflated** — operators cannot tell whether the queue gave up.
- **Acking before the side effect is durable** — crash loses the job.
- **Retrying input errors** — the queue becomes a slow poison loop.
- **Cron keyed on wall clock** — a retry fires a second run for the same window.
- **No "missed run" alarm** — silent gaps in nightly processing.

## Checklist

- [ ] Does every job path end in a defined terminal state?
- [ ] Is `failed` distinct from `dead`/quarantined?
- [ ] Are errors classified retryable/terminal before scheduling a retry?
- [ ] Is the failed state queryable by the product/support?
- [ ] Do scheduled tasks use window-based idempotency keys?
- [ ] Is there an alarm for missed or overlapping scheduled runs?
- [ ] Is the job boundary the smallest unit with a clear re-run meaning?

## Related

- [Retries, Backoff, and Exhaustion](./02-retries-backoff-and-exhaustion.md)
- [Poison Messages, DLQ, and Replay](./03-poison-messages-dlq-and-replay.md)
- [Chapter 27 — Retry Policies](../../../part-11-retry-and-resilience/27-retry-policies/README.md)
- [Chapter 32 Reference](../05-reference/README.md)
