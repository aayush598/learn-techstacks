# Retries, Backoff, and Exhaustion

> Part XII · Chapter 32 · Sections 32.4–32.6, 32.21 · _Estimated reading time: 17 min_
> **Prerequisite:** [Job Lifecycle and Failure States](./01-job-lifecycle-and-failure-states.md)

## In one sentence

Retries are a **bounded, delayed, classified** response to transient failure — and "bounded" means
both a maximum number of attempts and a final outcome (`permanent` or `exhausted`) that a human can
act on.

## Why this matters in production

Unbounded retries turn a broken dependency into a permanent traffic source that outlives the outage.
Instant retries synchronize all workers into a **retry storm** that prevents the dependency from
recovering. And when retries do stop, "job failed" is not enough: the operator must know whether it
will ever succeed without intervention (permanent) or simply ran out of budget (exhausted).

## 32.4 — Delayed retries

A retry must not be immediate. Even a 1–5 s delay breaks tight failure loops and lets a transient
condition clear.

Three implementation styles:

| Style | Mechanism | Pros | Cons |
| ----- | --------- | ---- | ---- |
| In-process sleep | `await sleep(delay)` | Simple | Ties up a worker slot; lost on crash |
| Queue delay | `send(..., delaySeconds)` | Frees worker; durable | Queue must support delay |
| Re-enqueue at time | Store `nextAttemptAt`, scheduler re-emits | Full control | More moving parts |

Prefer **queue delay** for anything longer than a few seconds. An in-process sleep during a 5-minute
backoff wastes a worker and delays every other job behind it.

## 32.5 — Backoff

**Exponential backoff** with **jitter** is the default:

```text
delay(attempt) = min(cap, base * 2^(attempt-1))
jittered       = random(0, delay)            // full jitter
```

| Attempt | Exponential (base 200 ms) | Full jitter range |
| ------- | ------------------------- | ----------------- |
| 1 | 200 ms | 0–200 ms |
| 2 | 400 ms | 0–400 ms |
| 3 | 800 ms | 0–800 ms |
| 4 | 1.6 s | 0–1.6 s |
| 5 | 3.2 s | 0–3.2 s |
| 6 | 6.4 s | 0–6.4 s |
| 7 | 12.8 s | 0–12.8 s |
| 8 | 25.6 s (cap 30 s) | 0–25.6 s |

Jitter matters because identical delay functions make every client retry in lockstep. **Full jitter**
spreads load best; **equal jitter** guarantees a minimum delay.

```ts
function backoff(attempt: number, base = 200, cap = 30_000): number {
  const exp = Math.min(cap, base * 2 ** (attempt - 1));
  return Math.floor(Math.random() * exp); // full jitter
}
```

Honor server instructions before your own schedule: `Retry-After` (seconds or HTTP date) wins over
computed backoff (Chapter 27).

## 32.6 — Max attempts

A maximum attempt count is the only thing standing between a poison message and an infinite loop.

| Setting | Typical value | Rationale |
| ------- | ------------- | --------- |
| `maxAttempts` | 5–8 | Covers short outages without hiding permanent faults |
| `maxReceiveCount` (SQS) | 3–5 | Redrive to DLQ before indefinite redelivery |
| Total retry window | 15 min – 24 h | Match the business tolerance |
| Per-attempt timeout | Job-specific | Must fit inside the visibility timeout |

Two different budgets matter:

- **Attempt budget** — how many tries.
- **Time budget** — how long the job may remain in retry. A job retried 8 times with 30 min backoff
  spans many hours; that may exceed the customer's expectation.

Store `attempt` on the job record, not just in the message, so a re-enqueued retry cannot reset the
count accidentally.

## 32.21 — Permanent vs exhaustion

These are both terminal, but they require different responses:

| Outcome | Meaning | Retry later? | Operator action |
| ------- | ------- | ------------ | --------------- |
| **Permanent** | Retrying cannot help (input/config/business) | No | Fix cause, then replay DLQ |
| **Exhausted** | Transient class, but attempts/time ran out | Maybe | Check dependency health; replay |

```ts
type TerminalReason = "permanent" | "exhausted" | "cancelled";

function terminalReason(err: unknown, attempt: number, max: number): TerminalReason | null {
  const cls = classifyJobError(err);
  if (cls !== "transient") return "permanent";
  if (attempt >= max) return "exhausted";
  return null; // keep retrying
}
```

The distinction drives UI copy and alerting:

- **Permanent** → "This export can't run because the storage bucket is misconfigured." Page the
  owning team; do not retry-storm.
- **Exhausted** → "The export is temporarily unavailable." Alert on dependency health, replay when
  healthy.

> ⚠️ **Hazard.** Marking an exhausted job as "permanent" hides an outage; marking a permanent error
> as "retryable" hides a bug behind a growing DLQ.

## Worked example — ExportJob retry policy

```ts
const POLICY = { baseMs: 500, capMs: 60_000, maxAttempts: 6, windowMs: 6 * 3_600_000 };

async function onFailure(job: Job, err: unknown) {
  const cls = classifyJobError(err);
  const age = Date.now() - new Date(job.firstFailedAt ?? job.createdAt).getTime();

  if (cls !== "transient") {
    return jobs.failPermanently(job.id, { code: toCode(err), class: cls });
  }

  if (job.attempt >= POLICY.maxAttempts || age >= POLICY.windowMs) {
    return jobs.failExhausted(job.id, { code: toCode(err), attempts: job.attempt });
  }

  const delayMs = Math.min(POLICY.capMs, POLICY.baseMs * 2 ** (job.attempt - 1));
  return jobs.retryAt(job.id, {
    attempt: job.attempt + 1,
    delayMs: Math.floor(Math.random() * delayMs),
  });
}
```

The queue then either redelivers at `nextAttemptAt` or moves the message to the DLQ.

## Key data / numbers

- SQS maximum delay per message: **15 minutes** (`DelaySeconds`); longer delays need a scheduler.
- SQS max retention: **14 days**; retries cannot exceed it.
- `Retry-After` is in seconds or an HTTP-date (RFC 9110); it overrides computed backoff.
- Common base/cap: **200–500 ms** base, **30–60 s** cap, 5–8 attempts.
- Full jitter is recommended by AWS's architecture guidance for avoiding synchronized retries.
- Deadlock/serialization SQLSTATEs (`40P01`, `40001`) are safe to retry; `23505` (unique violation)
  usually is not.

## Real-world use case — Checkout

Checkout's `ChargeRetry` job retried every failure immediately, 20 times. When Stripe had a 90 s
blip, 40 workers produced ~800 requests/second of retries for 20 minutes, prolonging the incident.
They switched to transient-only classification, base 500 ms, full jitter, cap 60 s, 6 attempts, and
`Retry-After` honored. During the next provider incident, retry volume stayed flat and the recovery
time matched Stripe's own status. Permanent errors (declined cards) now skip retries entirely.

## Trade-offs

| Policy | Pros | Cons | When to use |
| ------ | ---- | ---- | ----------- |
| No retry | No storms | Loses transient success | Non-idempotent, unsafe |
| Fixed delay | Predictable | Synchronized retries | Rarely |
| Exponential + jitter | Spreads load | Longer tail latency | Default |
| Many attempts | High eventual success | Long occupancy, cost | Cheap, idempotent jobs |
| Few attempts + DLQ | Fast failure, inspectable | More manual recovery | Expensive/side-effecting jobs |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Classify before retrying | Retry all exceptions |
| Add jitter | Use fixed delays across all workers |
| Honor `Retry-After` | Ignore provider guidance |
| Store attempt count on the job | Reset attempts on re-enqueue |
| Distinguish permanent vs exhausted | Label everything "failed" |
| Bound the total retry window | Retry across days silently |

## Common mistakes

- **Retrying programming errors** — identical failure repeated until the queue fills.
- **Synchronized backoff** — every worker retries at the same instant.
- **Sleeping in-process for minutes** — worker slots wasted.
- **Retry window longer than the DLQ retention** — messages expire before replay.
- **Resetting attempts** — a retry loop that never reaches max.

## Checklist

- [ ] Are errors classified into retryable classes before scheduling retries?
- [ ] Is backoff exponential with jitter?
- [ ] Is `Retry-After` honored when present?
- [ ] Is there a max attempt count **and** a max time window?
- [ ] Is `attempt` persisted on the job record?
- [ ] Are `permanent` and `exhausted` distinct terminal reasons?
- [ ] Does the retry window fit inside queue retention?

## Related

- [Job Lifecycle and Failure States](./01-job-lifecycle-and-failure-states.md)
- [Poison Messages, DLQ, and Replay](./03-poison-messages-dlq-and-replay.md)
- [Chapter 27 — Retry Policies](../../../part-11-retry-and-resilience/27-retry-policies/README.md)
- [ExportJob Worker with DLQ and Backoff](../03-practical-examples/01-exportjob-worker-with-dlq-and-backoff.md)
