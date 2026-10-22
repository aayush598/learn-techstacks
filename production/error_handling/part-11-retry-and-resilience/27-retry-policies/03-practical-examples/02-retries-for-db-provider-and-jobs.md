# Retries for DB, Providers, and Jobs

> Part XI · Chapter 27 · Sections 27.21–27.24 · _Estimated reading time: 22 min_
> **Prerequisite:** [Storms, Ownership, and Exhaustion](../01-concepts/05-storms-ownership-and-exhaustion.md)

## In one sentence

The retry *mechanics* are shared, but the **policy differs by dependency**: databases need rollback
and millisecond backoff, providers need `Retry-After` and idempotency keys, and jobs need
checkpoints and a dead-letter queue.

## Why this matters in production

Copying a provider retry policy onto a database transaction produces "current transaction is
aborted" errors. Copying a request retry policy onto a 2-hour export produces duplicated output and
exhausted worker pools. Each dependency has a different safe unit of retry: the **transaction**, the
**keyed request**, or the **checkpointed job step**. Getting the unit wrong is more dangerous than
getting the delay wrong.

## Database retries (27.21)

### The safe unit is the transaction

A statement that fails inside a Postgres transaction leaves it in an aborted state. Any subsequent
statement returns `25P02` (`in_failed_sql_transaction`) until rollback. Retry the **whole
transaction**, not the statement.

```python
def with_tx_retry(fn, attempts=3, base_ms=20):
    for n in range(attempts):
        try:
            with db.transaction():
                return fn()
        except RetryableDbError as err:
            if n == attempts - 1 or not err.transient:
                raise
            time.sleep(jittered_backoff(n, base_ms=base_ms, cap_ms=500))
```

### Policy table

| SQLSTATE | Meaning | Retry? | Notes |
| -------- | ------- | ------ | ----- |
| `40001` | serialization_failure | Yes | Roll back; jittered backoff |
| `40P01` | deadlock_detected | Yes | Roll back; often 10–50ms base |
| `08006`/`08003` | connection failure | Yes | New connection; transaction is gone |
| `53300` | too many connections | Yes | Backoff; don't add connections |
| `57014` | query_canceled | Conditional | Retry only on timeout, not user cancel |
| `23505` | unique_violation | No | Duplicate/business — reconcile |
| `23503` | foreign_key_violation | No | Missing parent |
| `42P01`/`42703` | undefined table/column | No | Schema/deploy fault — alert |

Keep DB retries **short** (2–3 attempts, tens of milliseconds) because they happen inside a request
holding a connection. Long DB backoff exhausts the pool.

### Do not retry the connection acquisition blindly

If the pool is exhausted (`53300`, pool timeout), retrying immediately makes it worse. Use a short
bounded backoff and let the request fail fast if the pool is still saturated. Circuit breaking or
admission control (Chapter 29) belongs here.

## Provider retries (27.22)

### The safe unit is the keyed request

A provider call is safe to retry when the request carries an idempotency key that the provider
honors, or when the operation is read-only.

```ts
async function callProvider(input: ProviderInput, key: string, deadline: number) {
  return retry(
    (signal) => provider.create(input, { idempotencyKey: key, signal }),
    {
      maxAttempts: 3,
      deadline,
      perAttemptTimeoutMs: 2_500,
      baseDelayMs: 300,
      capDelayMs: 3_000,
      jitter: "full",
    },
    {
      isRetryable: (e) => e.retryClass === "retryable",
      retryAfterMs: (e) => e.retryAfterMs, // parsed from Retry-After / body
    },
  );
}
```

### Provider policy table

| Signal | Retry? | Delay |
| ------ | ------ | ----- |
| `429 Too Many Requests` | Yes | `Retry-After` (or backoff if absent) |
| `503 Service Unavailable` | Yes | `Retry-After`, then backoff |
| `500`/`502`/`504` | Usually | Exponential + jitter |
| `401`/`403` | No | Refresh credentials first |
| `400`/`422` | No | Fix request |
| Network timeout on write | Only with key | Backoff; reconcile if unknown |
| `card_declined` | No | Business outcome |

> ⚠️ **Hazard.** A provider SDK that retries internally plus your loop silently multiplies attempts.
> Set the SDK's retry count explicitly (usually `0`) when your service owns the policy.

## Job retries (27.23)

### The safe unit is the checkpointed step

A job is long-running; retrying it from zero is expensive and often incorrect. Retry the **failed
step**, resuming from a durable checkpoint.

```ts
interface ExportCheckpoint {
  jobId: string;
  lastOffset: number;
  objectKey: string;
}

async function runExport(job: ExportJob) {
  let cp = await store.loadCheckpoint(job.id) ?? { jobId: job.id, lastOffset: 0 };
  while (cp.lastOffset < job.totalRows) {
    const page = await fetchPageWithRetry(job, cp.lastOffset); // step-level retry
    await writer.appendIdempotent(job.objectKey, cp.lastOffset, page);
    cp.lastOffset += page.length;
    await store.saveCheckpoint(cp);
  }
}
```

### Job policy table

| Concern | Value |
| ------- | ----- |
| Attempts | 3–5 per step, then DLQ |
| Backoff | 30s, 2m, 10m (exponential, jittered) |
| Per-attempt timeout | Minutes |
| Overall SLA | Hours; alert before breach |
| Resume | Checkpoint, not restart |
| Terminal | DLQ with cause and checkpoint |
| Dedup | Job id + step offset key |

Queue redelivery is itself a retry layer. A queue with 5 receives and a handler with 3 attempts is
15 executions — count it (27.16).

## Side-effect retries (27.24)

| Operation | Safe unit | Rule |
| --------- | --------- | ---- |
| `POST /charges` | Keyed request | Same key across attempts |
| `POST /refunds` | Keyed request | Same key; verify before retry |
| Send email | Message id | Dedup by id |
| Publish event | Outbox | One transaction writes row + outbox |
| Increment counter | Absolute value or version | Never retry a relative increment blind |
| File upload | Multipart/part id | Resume parts, not whole file |

If the outcome is unknown and no key exists, **reconcile before retrying**: query the provider for
the result by your own correlation id. Retrying blind is how duplicates are born.

## Worked example — one request, three policies

```text
POST /invoices (deadline 10s)
  ├─ DB transaction (3 attempts, 20ms base, 500ms cap)  ← rollback each time
  └─ Stripe charge (3 attempts, Retry-After-aware)      ← same idempotency key
       └─ SDK retries disabled, HTTP retries disabled
Job "send-invoice-email" (retries 4×, 30s base, DLQ)
  └─ idempotent by message id
```

Each dependency has its own unit and schedule; the request deadline constrains the synchronous ones.

## Key data / numbers

- DB base backoff: **10–50ms**, cap **500ms–1s**; 2–3 attempts.
- Provider base backoff: **200–500ms**, cap **3–10s**; honor `Retry-After`.
- Job backoff: **30s → 2m → 10m**; 3–5 attempts then DLQ.
- Postgres `40001`/`40P01` require rollback before retry.
- Queue `max receives` multiplies handler attempts.
- Idempotency key TTL commonly **24h** (Chapter 28).

## Real-world use case — Acme SaaS

Acme applied one generic "retry 3× with 1s delay" policy to everything. Database deadlocks retried a
statement inside an aborted transaction and always failed with `25P02`. Provider `429`s ignored
`Retry-After`, worsening rate limiting. `ExportJob` restarted a 90-minute export from zero on each
failure. Split policies fixed all three: DB retries wrapped the transaction with a 20ms base; the
provider adapter honored `Retry-After`; the export resumed from a checkpoint and sent exhausted steps
to a DLQ. Export success rate rose from 71% to 99.2% without increasing provider request volume.

## Trade-offs

| Dependency | Fast retry | Slow retry |
| ---------- | ---------- | ---------- |
| DB | Holds a connection briefly | Exhausts pool |
| Provider | May hit `Retry-After` | Wastes user latency |
| Job | Wastes attempts on a blip | Survives long outages |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Retry the whole DB transaction | Retry a statement in an aborted tx |
| Reuse the idempotency key | Generate a new key per attempt |
| Honor `Retry-After` | Use a fixed 1s delay for `429` |
| Checkpoint job progress | Restart long jobs from zero |
| Count queue redelivery | Treat the queue as retry-free |
| Reconcile unknown outcomes | Retry an unkeyed write blind |

## Common mistakes

- **Long DB backoff inside a request** exhausting the pool.
- **Provider SDK retries left on** alongside application retries.
- **Job retry with non-idempotent output**, duplicating rows.
- **DLQ configured but never monitored**, so poison jobs vanish silently.
- **Retrying `57014` after user cancellation**, wasting work the user abandoned.

## Checklist

- [ ] DB retries wrap the transaction and roll back first.
- [ ] Provider retries reuse one idempotency key.
- [ ] `Retry-After` is parsed and applied.
- [ ] Job retries resume from a checkpoint.
- [ ] Queue redelivery is included in attempt math.
- [ ] Exhausted jobs land in a monitored DLQ.
- [ ] Unkeyed ambiguous writes trigger reconciliation, not retry.

## Related

- [Storms, Ownership, and Exhaustion](../01-concepts/05-storms-ownership-and-exhaustion.md)
- [Chapter 23 — Transaction and Rollback Error Handling](../../../part-09-database-and-transactions/23-transaction-and-rollback-error-handling/README.md)
- [Chapter 32 — Background Jobs, Queues, and Scheduled Tasks](../../../part-12-async-and-background-jobs/32-background-jobs-queues-and-scheduled-tasks/README.md)
- [Chapter 28 — Idempotency and Duplicate-Operation Safety](../../28-idempotency-and-duplicate-operation-safety/README.md)
