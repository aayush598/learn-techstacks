# At-least-once vs Exactly-once — Mechanics

> Part XII · Chapter 32 · Section 32.13 (mechanics) · _Estimated reading time: 16 min_
> **Prerequisite:** [Worker Failures, Timeouts, Shutdown, and Isolation](../01-concepts/04-worker-failures-timeouts-and-isolation.md)

## In one sentence

Most queues give you **at-least-once** delivery, "exactly-once" is only achievable as
**at-least-once delivery plus idempotent processing**, and the gap between the two is where duplicate
charges and duplicate exports live.

## Why this matters in production

Engineers routinely assume a queue delivers each job once because the payload is unique or because
the docs mention "exactly-once." In practice, the window between "the side effect happened" and "the
message was acknowledged" is where crashes occur, and any crash inside it produces a redelivery. If
the side effect is not idempotent, the customer is charged twice or the export contains duplicate
rows.

## The delivery guarantees

| Guarantee | Meaning | Duplicates | Loss | Typical systems |
| --------- | ------- | ---------- | ---- | --------------- |
| At-most-once | Deliver, never retry | None | Possible | Fire-and-forget, UDP-ish |
| At-least-once | Retry until acked | **Possible** | None if retention holds | SQS, RabbitMQ, Kafka (manual commit), most job queues |
| Exactly-once | Each message processed once | None | None | Kafka transactions in narrow pipelines, some brokers |

"Exactly-once" is a property of an **end-to-end pipeline**, not a single component. The moment your
consumer writes to an external system (Stripe, S3, email) outside the broker's transaction, you are
back to at-least-once.

## Where duplicates come from

```text
claim ──▶ side effect ──▶ ack
            │              │
            │              └─ crash here → redelivery → effect runs twice
            │
            └─ crash here → redelivery → effect runs once (fine)

claim ──▶ side effect (slow) ──▶ visibility expires → redelivery
                                  → two workers run concurrently
```

| Cause | Trigger |
| ----- | ------- |
| Crash after effect, before ack | OOM, `SIGKILL`, deploy |
| Visibility timeout too short | Slow job |
| Network error on ack | Ack lost in transit |
| Producer retry after timeout | Enqueue appeared to fail but succeeded |
| DLQ replay | Deliberate second run |
| Consumer rebalance | Partition reassigned mid-processing |

## Why exactly-once is hard across systems

A broker can make **its own** consume→produce transaction atomic (Kafka transactions, SQS FIFO dedupe
within 5 minutes). It cannot atomically include Stripe's charge or S3's `PutObject`. That requires a
distributed transaction, which most systems avoid. So the industry pattern is:

```text
at-least-once delivery  +  idempotent effect  =  effectively-once
```

This is sometimes called **effectively-once** or **exactly-once processing** (as opposed to
delivery). Name it honestly in your docs.

## Idempotency strategies for jobs

### 1. Deterministic effect key

```ts
const key = `export:${job.id}`;                       // stable across retries
const existing = await exports.findByKey(key);
if (existing) return existing;
await exports.create({ key, ...job.data });
```

### 2. Insert-first, unique constraint

```sql
INSERT INTO exports (job_id, tenant_id, status)
VALUES ($1, $2, 'running')
ON CONFLICT (job_id) DO NOTHING
RETURNING id;
```

Zero rows returned means another attempt already claimed it.

### 3. State transition guard

```sql
UPDATE jobs
SET status = 'succeeded', finished_at = now()
WHERE id = $1 AND status = 'running';
-- 0 rows => already terminal; skip side effects
```

### 4. Provider idempotency key

```ts
await stripe.charges.create(
  { amount, currency, customer },
  { idempotencyKey: `charge:${job.id}` },
);
```

### 5. Dedupe store with TTL

```ts
if (!(await dedupe.claim(`email:${job.id}`, { ttlSec: 86_400 }))) return;
await mailer.send(...);
```

Cache-based dedupe is best-effort; prefer a durable unique constraint for money.

## What "exactly-once" buys you

Kafka's transactional producer + `read_committed` consumer can make **stream processing** atomic
across topics:

```text
consume input → transform → produce output + commit offset (one transaction)
```

This removes duplicates *within Kafka*. If the output is consumed by a job that calls Stripe, Stripe
still needs an idempotency key. So even here, the boundary matters.

SQS FIFO's `MessageDeduplicationId` suppresses duplicates for **5 minutes**. It does not help with a
retry an hour later.

## Worked example — Checkout charge job

```ts
async function chargeOrder(job: Job<{ orderId: string; amount: number }>) {
  const key = `charge:${job.id}`;

  // 1. Durable claim: one attempt wins.
  const claimed = await db.query(
    `INSERT INTO charges (job_id, order_id, status)
     VALUES ($1, $2, 'pending')
     ON CONFLICT (job_id) DO NOTHING
     RETURNING id`,
    [job.id, job.data.orderId],
  );
  if (claimed.rowCount === 0) {
    const row = await db.charges.findByJob(job.id);
    if (row.status === "succeeded") return row;      // replay: done
    if (row.status === "pending") return;            // another worker is on it
  }

  // 2. External effect with provider idempotency.
  const charge = await stripe.charges.create(
    { amount: job.data.amount, currency: "usd", customer: job.data.orderId },
    { idempotencyKey: key },
  );

  // 3. Commit outcome.
  await db.charges.markSucceeded(job.id, charge.id);
  return charge;
}
```

Three layers — a unique DB constraint, a provider idempotency key, and a terminal-state check — make
the job safe under redelivery, a crash between steps, and DLQ replay.

## Key data / numbers

- SQS FIFO dedupe window: **5 minutes** with `MessageDeduplicationId`.
- Standard SQS queues provide at-least-once; duplicates are possible even without failures.
- Kafka `enable.idempotence=true` prevents producer-side duplicate writes per partition/session.
- Kafka transactions add latency and require `isolation.level=read_committed` consumers.
- Stripe idempotency keys are retained for **24 hours**.
- A visibility timeout shorter than processing time guarantees concurrent duplicates.

## Real-world use case — Acme SaaS

Acme's `SendInvoiceEmail` job used the recipient's email address as its "dedupe key" in an in-memory
set. After a deploy, the set was empty and every redelivered job sent a second email. Customers
received duplicate invoices, and finance had to explain the confusion. The fix: a `sent_emails`
table with a unique `(job_id)` constraint, checked and inserted in one transaction, plus the job id as
the provider's idempotency key. Duplicate emails went to zero across the next three deploys.

## Trade-offs

| Strategy | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| At-most-once | Simple, no duplicates | Data loss | Metrics, best-effort |
| At-least-once, no idempotency | Simple, no loss | Duplicate effects | Read-only work |
| At-least-once + idempotency | No loss, effectively once | Extra state/keys | Default for side effects |
| Broker exactly-once | No app dedupe in-scope | Narrow, external systems still need keys | Stream processing |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Assume every job can run twice | Assume unique payload = once |
| Use a durable unique constraint | Use an in-memory dedupe set |
| Pass the job id as a provider idempotency key | Generate a new key per attempt |
| Check terminal state before effects | Re-run effects on every redelivery |
| Document "effectively-once" | Claim end-to-end exactly-once |

## Common mistakes

- **In-memory dedupe** — lost on deploy/restart.
- **Random idempotency key per attempt** — defeats provider dedupe.
- **Dedupe check and effect not atomic** — two workers both pass the check.
- **Assuming FIFO = exactly-once forever** — only a 5-minute window.
- **Acking before the effect commits** — loss, not duplication, on crash.

## Checklist

- [ ] Is the guarantee documented as at-least-once delivery?
- [ ] Does every side-effecting job have a deterministic key?
- [ ] Is the key enforced by a durable unique constraint?
- [ ] Is the provider idempotency key stable across attempts?
- [ ] Is there a terminal-state check before re-running effects?
- [ ] Is the claim + effect atomic where possible?
- [ ] Does DLQ replay reuse the original job id?

## Related

- [Worker Failures, Timeouts, Shutdown, and Isolation](../01-concepts/04-worker-failures-timeouts-and-isolation.md)
- [At-least-once and Idempotent Consumers (Chapter 33)](../../33-events-webhooks-and-message-processing/02-deep-dive/02-at-least-once-and-idempotent-consumers.md)
- [Chapter 28 — Idempotency](../../../part-11-retry-and-resilience/28-idempotency-and-duplicate-operation-safety/README.md)
- [ExportJob Worker with DLQ and Backoff](../03-practical-examples/01-exportjob-worker-with-dlq-and-backoff.md)
