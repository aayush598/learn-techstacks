# Bounding Queues, Retries, and Backpressure

> Part XXII · Chapter 57 · Sections 57.5, 57.13, 57.14 · _Estimated reading time: 20 min_
> **Prerequisite:** [Chapter 32 — Background Jobs, Queues, and Scheduled Tasks](../../../part-12-async-and-background-jobs/32-background-jobs-queues-and-scheduled-tasks/README.md)

## In one sentence

A **queue with no depth limit converts a slow dependency into unbounded memory growth**;
bounding the queue, bounding the retries, and rejecting early (backpressure) are the three
controls that keep a backlog from becoming an outage.

## Why this matters in production

Queues are the most patient component in a system, which makes them the most dangerous. A
queue accepts work at any rate, holds it as long as you like, and only tells you about the
problem after the work has been waiting long enough to be useless.

The classic failure:

1. A dependency slows to 10 s per call (not down — slow).
2. Workers keep taking jobs; each takes 10 s instead of 500 ms.
3. Arrival rate exceeds completion rate; the backlog grows by `(arrival − completion) × time`.
4. The queue's memory footprint grows; the broker starts evicting or the consumer group lags.
5. Work in the backlog is now stale — a webhook delivered 2 hours late, an export of data
   that has since changed.
6. Meanwhile the *same* workers are being asked to retry more, so completion rate drops
   further.

The fix is not "more workers" (they are already saturated). The fix is to **bound the
backlog, shed new work, and make the depth visible**.

## Core concept

### 57.5 — Queue buildup

The queue dynamics are a small model you can reason with:

```text
  backlog(t+Δ) = backlog(t) + arrivals(t) × Δ − completion_rate × Δ

  completion_rate = min(worker_count, worker_count / avg_job_duration)
                  = workers / avg_job_duration
```

With 4 workers and an average job duration of 500 ms, the completion rate is 8 jobs/second.
If arrivals are 3/second, the backlog drains. If a dependency slows jobs to 10 s, the
completion rate collapses to 0.4 jobs/second, and a 3/second arrival rate produces a backlog
growth of **2.6 jobs/second**.

The three numbers that matter:

| Quantity | Symbol | Why |
| -------- | ------ | --- |
| **Service rate** | `μ = workers / avg_duration` | How fast the backlog can drain |
| **Arrival rate** | `λ` | How fast work arrives |
| **Utilization** | `ρ = λ / μ` | Above 1.0, the backlog grows without bound |

When `ρ > 1`, the system is **unstable**. The queue is not a buffer anymore; it is a
**delay line** that grows forever.

Three more numbers a queue needs:

| Metric | Meaning | Threshold |
| ------ | ------- | --------- |
| **Depth** | Number of unprocessed messages | Bounded (see below) |
| **Age** | Age of the oldest message | ≤ 1 hour |
| **Lag** | Time since the oldest message was enqueued | Rising steadily = unstable |

### 57.13 — Bounding retries and queues

Four bounds, each answering a different "how much" question:

| Bound | Question | Typical value | Mechanism |
| ----- | -------- | ------------- | --------- |
| **Retry budget** | How many *retries* may I add? | 5–10% of traffic | Token/ratio counter |
| **Retry attempts** | How many times per operation? | ≤ 3 | Policy per dependency |
| **Queue depth** | How many messages may wait? | 10,000 per queue | Enqueue-time check → shed/DLQ |
| **Queue age** | How old may a message be? | 1 hour | Consumer drops / DLQ |

A queue without a depth bound is the most common structural gap. When the enqueue path
checks the depth and refuses, the system degrades *predictably* (new work is rejected with a
clear reason) instead of degrading *mysteriously* (everything gets slow).

```ts
// ✅ Bound the queue at enqueue time.
const depth = await queue.depth(q);
if (depth >= MAX_DEPTH) {
  throw new QueueOverloadedError({ queue: q, depth, maxDepth: MAX_DEPTH });
}
```

### 57.14 — Backpressure and rejection

**Backpressure** is the general idea: when the consumer cannot keep up, the producer must
slow down. In a message queue, the producer cannot be slowed down directly, so the practical
mechanism is **rejection with a retry signal**.

The rejection contract matters more than the mechanism:

| Property | Rule | Why |
| -------- | ---- | --- |
| Status | `429 Too Many Requests` for tenant-level limits; `503 Service Unavailable` for server-level saturation | Distinguishes "you" from "us" |
| `Retry-After` | Always present, 1–30 s, integer seconds | The client needs a number |
| Body | RFC 9457 problem document with a stable code | Clients branch on codes, not text |
| Correlation ID | Present | The user can quote it to support |
| Idempotency | The rejected request must be safe to retry | Otherwise rejecting creates duplicates |

```ts
// ✅ Rejection with a complete contract.
res.setHeader("Retry-After", "5");
res.status(429).json({
  type: "https://acme.example/problems/tenant-throttled",
  title: "Too many requests for this tenant",
  status: 429,
  detail: "Limit of 10 concurrent requests reached for this tenant. Retry in 5 seconds.",
  instance: req.path,
  code: "TENANT_CONCURRENCY_LIMIT",
  correlationId: req.id,
});
```

### The shedding order

When the system is saturated, **not all requests are equal**. The shedding order decides
which customers bear the pain:

```text
  1. Optional, non-urgent features      → shed silently (AI summaries, export previews)
  2. Read-only, cacheable requests       → shed or serve stale (dashboards)
  3. Idempotent background work          → defer to the queue (if it has room)
  4. Standard write requests              → reject with 429 + Retry-After
  5. Premium/critical path                → serve
  6. Payments, auth, webhooks             → serve last, never shed
```

> ⚠️ **Hazard.** Rejecting a **write** that was already partially applied creates a
> duplicate-side-effect hazard. Acme's rule: a request may only be shed **before** any side
> effect occurs. Once the payment provider has been called, the request must complete or
> compensate — never be shed.

### 57.13 — Queue bounds and the DLQ

A bounded queue needs a place to put the work it refuses. Three choices:

| Choice | Behaviour | Use when |
| ------ | --------- | -------- |
| **Shed** (drop, do not enqueue) | The work never happens | The work is recomputable or optional |
| **Defer** (enqueue to a lower-priority queue) | The work happens later | The work matters but not now |
| **DLQ** (dead-letter) | The work happens after human/automated inspection | The work failed repeatedly and needs attention |

The mistake is **silently dropping**. If work is dropped, it must be *counted and reported* —
a dropped export is a customer who never gets their file.

## How it works (mechanics)

### A bounded queue with depth checks and age-based expiry

```ts
export class BoundedQueue<T> {
  private depth = 0;

  constructor(
    private readonly broker: Broker,
    private readonly name: string,
    private readonly maxDepth: number,
    private readonly maxAgeMs: number,
  ) {}

  async enqueue(payload: T, opts: { priority?: "high" | "normal" | "low" } = {}): Promise<void> {
    if (this.depth >= this.maxDepth) {
      // Bounded: refuse explicitly rather than grow.
      throw new QueueOverloadedError({ queue: this.name, depth: this.depth, maxDepth: this.maxDepth });
    }
    this.depth++;
    await this.broker.send(this.name, JSON.stringify(payload), {
      priority: opts.priority ?? "normal",
      expiresInMs: this.maxAgeMs,       // the broker drops stale messages
    });
  }

  onDequeue(): void {
    this.depth = Math.max(0, this.depth - 1);
  }
}
```

### Consumer-side age check (drop stale work)

```ts
// ✅ A worker refuses to process work that is already useless.
const age = Date.now() - message.enqueuedAt;
if (age > MAX_JOB_AGE_MS) {
  await message.deadLetter({ reason: "EXPIRED", ageMs: age });
  metrics.increment("export.job.expired");
  return;   // do not even attempt it
}
```

For `WebhookIngest`, the age check is different: a webhook is never stale in the same way —
it carries the *current* state of the world. Stripe retries for up to 3 days. So webhooks
should not be expired, but they must be **deduplicated** and processed in order where the
event type requires it.

### Backpressure at the producer

```ts
// ✅ The producer applies backpressure before enqueuing.
export async function requestExport(tenantId: string): Promise<ExportAccepted> {
  const limiter = limits.forTenant(tenantId);
  const slot = limiter.tryAcquire("export");
  if (!slot.ok) {
    throw new TenantOverloadedError({ retryAfterSeconds: slot.retryAfterSeconds });
  }
  try {
    const jobId = await exportsQueue.enqueue({ tenantId, requestedAt: Date.now() });
    return { ok: true, jobId };
  } finally {
    slot.release();
  }
}
```

### Computing drain time

```text
  drain_time = depth / (μ − λ)        when λ < μ
  unbounded  = ∞                        when λ ≥ μ
```

With `depth = 8,000`, `μ = 8/s`, `λ = 3/s`: `drain_time = 8000 / 5 = 1,600 s ≈ 27 minutes`.
If the retry window of the slowest consumer is 1 hour, the queue recovers — but only if no
new work arrives at a rate above 5/s. If `λ` rises to 9/s, `μ − λ < 0` and the queue never
drains. This is the calculation that determines whether a depth limit is enough.

## Worked example — `ExportJob` (Acme SaaS)

Acme's export queue was unbounded. During a 20-minute S3 degradation:

| Time | Backlog | Worker completion rate | Note |
| ---- | ------- | ---------------------- | ---- |
| 00:00 | 12 | 8/s | Normal |
| 02:00 | 1,050 | 1.2/s | S3 slow; workers retrying |
| 05:00 | 2,880 | 0.9/s | Backlog growing at ~2/s |
| 10:00 | 5,640 | 1.0/s | Customers requesting more exports |
| 20:00 | 9,150 | 1.1/s | Oldest job is 3.5 hours old |
| 45:00 | 14,800 | 1.0/s | **Queue at 12 GB; broker started evicting** |

The broker evicted the *oldest* messages — which were the exports customers had been
waiting for. Acme's "export never arrived" tickets spiked to 380/week, and each of those
customers had a *successful* request that was silently discarded.

The fix had four parts:

1. **Depth limit** (57.13): `MAX_DEPTH = 10,000` per queue. Enqueue beyond that returns
   `429` + `Retry-After: 30` — the customer knows to retry later rather than waiting
   forever.
2. **Age limit** (57.13): messages older than 1 hour are dead-lettered with reason
   `EXPIRED` and counted, instead of being evicted invisibly. The customer sees "your export
   expired — please re-run it".
3. **Retry ownership** (57.3): the worker retries S3 once with backoff and then fails the
   attempt; the *queue* provides the delay between attempts. The worker no longer spins
   inside one attempt for 30 s.
4. **Shed new work** (57.14): while the queue is above 80% depth, new export requests are
   rejected with `429` rather than accepted and queued for hours.

The result: the backlog now drains predictably, no work is lost silently, and the customer
experience is "try again in 30 seconds" rather than "wait 3 hours for nothing".

## Key data / numbers

| Item | Value | Notes |
| ---- | ----- | ----- |
| Queue depth limit | 10,000 messages per queue | Start shedding/DLQ beyond |
| Queue max age | 1 hour | Older work is usually worthless (not for webhooks) |
| Queue service rate target `μ` | ≥ 1.5 × peak arrival `λ` | Headroom for bursts |
| Stability requirement | `λ < μ` | Otherwise the backlog never drains |
| Drain time target | < 15 min at peak | Otherwise users see stale results |
| Retry budget | 5–10% of traffic | Per dependency, 10 s window |
| Max retry attempts | 3 | |
| `Retry-After` on rejection | 1–30 s (integer seconds) | Always present |
| Rejection status | `429` (tenant), `503` (server) | Never `500` |
| Shedding threshold | Start shedding at 80% of queue depth | Fail before you must |
| Worker count per queue | `arrival_rate × avg_duration × 1.5` | Plus 50% headroom |
| Max job duration | 15 min | Longer jobs need checkpointing |
| DLQ retention | 7 days | Then manual review |

## Real-world use case — `WebhookIngest` (Acme SaaS)

Webhook processing is the opposite of exports: the work is **never stale**, and the producer
is **Stripe**, who does not accept backpressure.

That changes the design:

| Property | Export | Webhook |
| -------- | ------ | ------- |
| Expire stale work | Yes (1 h) | **No** — Stripe retries for up to 3 days |
| Reject on depth | `429` to the customer | **Cannot** — Stripe would retry, adding load |
| Bound the queue | Yes | Yes, but **overflow goes to the DLQ**, not a rejection |
| Dedup | By `jobId` | By `Stripe-Event-Id` |
| Order | Not required | Required per event type (e.g. subscription updates) |

The overflow rule for webhooks is critical: when the webhook queue is full, Acme must
**acknowledge with `200` and write to the DLQ** — no wait, that's wrong, because acking
means Stripe will not retry, and the event is lost.

The correct behaviour under webhook-queue saturation:

1. If the event can be processed **inline** within the request budget → process it.
2. Otherwise, if the queue has room → enqueue and ack.
3. If the queue is full → **do not ack**; return `503` with `Retry-After: 5`. Stripe will
   retry with its own backoff, and the load is absorbed by Stripe's schedule rather than
   Acme's queue.
4. After 3 days of retries, Stripe gives up — so Acme's DLQ replay must cover that window.

The measurable result: during a 45-minute webhook backlog, Acme's duplicate rate stayed at
0.0% (because every write is keyed by `Stripe-Event-Id`) and event loss was 0 — every
delivered event was applied exactly once, eventually.

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| Unbounded queue | Never rejects work | Grows without limit; loses work silently | Never |
| Depth-bounded queue + rejection | Predictable; explicit | Rejects work the customer wanted | Exports, user-triggered jobs |
| Depth-bounded queue + DLQ | No work lost | Requires a replay process | Webhooks, payment events |
| Expire by age | Frees stale work | Customer must re-run | Exports, reports |
| Shedding by feature | Protects the core | Requires a feature classification | Any multi-feature product |
| More workers | Raises `μ` | Costs money; may saturate the dependency | Only if the dependency has headroom |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Bound the queue depth at enqueue time | Let the queue grow without limit |
| Bound the queue age | Process work that is hours old |
| Dead-letter overflow instead of dropping it | Drop expired messages silently |
| Reject with `429`/`503` **and** `Retry-After` | Return `500` on rejection |
| Compute `λ` and `μ` and confirm `λ < μ` | Assume more workers fix a backlog |
| Shed optional features before rejecting writes | Shed uniformly |
| Never shed a request after a side effect | Reject mid-flight after charging |

## Common mistakes

- **No depth limit.** The queue becomes a memory leak that reports itself only when the
  broker starts evicting.
- **Silent expiry.** The broker drops old messages and the customer is told nothing.
- **Retrying inside the worker without backing off to the queue.** Workers spin, throughput
  collapses, and the backlog grows.
- **Rejecting writes after a side effect.** A shed request that already charged a card is a
  duplicate-charge incident waiting to happen.
- **Adding workers to fix `λ ≥ μ`.** If the bottleneck is the dependency, more workers
  just amplify the load on it.
- **Rejecting webhooks with `429`.** The producer (Stripe) will retry, which is exactly the
  load you cannot accept.

## Checklist

- [ ] Every queue has a depth limit enforced at enqueue time.
- [ ] Every queue has an age policy (expire for exports, never for webhooks).
- [ ] Overflow goes to the DLQ (webhooks) or to a `429` (user-triggered work) — never
      silently dropped.
- [ ] `λ` and `μ` are measured; `λ < μ` holds at peak with 50% headroom.
- [ ] Rejections carry `429`/`503`, a `Retry-After`, and a stable error code.
- [ ] The shedding order is written down, per endpoint class.
- [ ] No request is shed after a side effect has occurred.
- [ ] Worker retries are backed off by the queue, not spun inside one attempt.

## Related

- [Failure Amplification and Error Storms](./01-failure-amplification-and-error-storms.md)
- [Isolation: Tenants, Features, and Dependencies](./02-isolation-tenants-features-dependencies.md)
- [Retry Budget and Queue Bounding](../02-deep-dive/02-retry-budget-and-queue-bounding.md)
- [Chapter 32 — Background Jobs, Queues, and Scheduled Tasks](../../../part-12-async-and-background-jobs/32-background-jobs-queues-and-scheduled-tasks/README.md)
