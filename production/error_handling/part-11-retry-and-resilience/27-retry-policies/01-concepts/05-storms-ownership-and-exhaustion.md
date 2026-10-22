# Storms, Ownership, and Exhaustion

> Part XI · Chapter 27 · Sections 27.15–27.23 · _Estimated reading time: 22 min_
> **Prerequisite:** [Budgets, Deadlines, and Server Guidance](./04-budgets-deadlines-and-server-guidance.md)

## In one sentence

Retries become harmful when they **multiply across layers and synchronize across clients**; the
defenses are one named owner per retry, a global view of nested attempts, and a terminal error that
preserves what actually failed.

## Why this matters in production

A retry is locally reasonable and globally dangerous. One service retrying 3× is fine; five layers
each retrying 3× turns one request into 243. A thousand clients retrying in lockstep turns a
10-second blip into a sustained outage. The teams that survive dependency incidents are the ones that
can answer, for every call: *who retries this, how many times in total, and what does the caller see
when it finally gives up?*

## 27.15 — Avoiding retry storms

A retry storm is a positive feedback loop: failure → retries → more load → more failure.

| Cause | Defense |
| ----- | ------- |
| Synchronized clients | Jitter (27.9) |
| No cap on attempts | `maxAttempts` + deadline |
| Retries during overload | Circuit breaker (Ch. 29) |
| Every layer retries | Single retry owner (27.18) |
| Retry budget unbounded | Budget per dependency (27.10) |
| Retrying non-transient errors | Classification (27.4–27.5) |

> ⚠️ **Hazard.** Retrying during a dependency outage is not resilience; it is a **load amplifier**.
> When the breaker is open, retries must stop, not speed up.

## 27.16 — Retry amplification

Amplification is the product of attempts across layers:

```text
user request
  └─ API gateway        2 attempts
      └─ order service  3 attempts
          └─ SDK client 3 attempts
              └─ provider
total upstream calls = 2 × 3 × 3 = 18
```

If each call fans out to 5 parallel downstream calls, the provider sees **90** calls for one user
action. During an incident this is how a 5% error rate becomes a total outage.

### Containment rules

1. **Only one layer retries a given dependency.** Prefer the layer closest to the dependency that
   still has enough context to classify.
2. **Disable SDK retries** when the service owns the policy (or vice versa).
3. **Make retries visible** in traces: one span per attempt, tagged `retry.attempt`.
4. **Count total attempts, not just configured attempts**, in metrics.

## 27.17 — Nested retries

Nested retries occur when a retried operation internally calls another retried operation.

```text
ExportJob (retries 3×)
  └─ fetch page (retries 3×)
      └─ HTTP client (retries 3×)
```

A failure on page 7 can be attempted 27 times before the job records one failure. Worse, the inner
retries may exhaust the job's deadline before the job-level retry ever runs.

| Pattern | Fix |
| ------- | --- |
| Job retries + call retries | Let the job own retries; call once with a deadline |
| Service retries + SDK retries | Disable one; document which |
| Retry inside a loop over items | Retry the item, not the batch (or vice versa, deliberately) |
| Retry inside a transaction | Roll back, then retry the transaction once at the boundary |

## 27.18 — Retry ownership across layers

Every retry decision needs **one owner**. Write it down.

| Layer | Should it retry? | Rationale |
| ----- | ---------------- | --------- |
| Browser/client | Rarely | User can act; retries hide latency |
| API gateway | Only idempotent `GET`s | Limited context |
| Application service | Yes, for domain calls | Knows semantics and keys |
| Repository | Only DB-specific transient classes | Knows `40001`/`40P01` |
| Provider adapter | Yes, for provider transients | Knows `Retry-After` |
| Job worker | Yes, at the job level | Owns checkpointing and DLQ |
| SDK | Configure off if app owns it | Otherwise invisible multiplication |

**Ownership rule:** the layer that can *classify the error correctly and knows whether the operation
is safe to repeat* owns the retry. For a Stripe charge, that is the payment service (it holds the
idempotency key), not the HTTP client.

## 27.19 — Preserving the final failure

After exhaustion, the caller needs the **last real error**, not a new generic one. Preserve:

- the final error's code, class, and cause;
- the number of attempts made;
- total elapsed time;
- the last `Retry-After`/provider hint, if any;
- per-attempt outcomes (at least in logs/traces).

```ts
class RetryExhaustedError extends Error {
  constructor(
    readonly attempts: number,
    readonly elapsedMs: number,
    readonly lastError: AppError,
  ) {
    super(`retry exhausted after ${attempts} attempts`);
    this.cause = lastError;
  }
}
```

Do **not** replace the cause with `new Error("retries exhausted")`; that destroys the diagnosis.

## 27.20 — Meaningful error after exhaustion

The terminal error must be actionable for its audience:

| Audience | Needs |
| -------- | ----- |
| User | A stable message and whether to retry later |
| Client application | Code, retryability, `Retry-After` |
| On-call engineer | Cause, dependency, attempts, trace id |
| Billing/finance | Whether the side effect may have occurred |

If the operation was a payment and the outcome is genuinely unknown, the terminal error must say
**"unknown outcome — reconcile"**, not "failed". Chapter 28.15 covers this contract.

## 27.21 — Database retries

DB retries are special because the transaction state matters.

| Condition | Retry? | Note |
| --------- | ------ | ---- |
| `40001` serialization failure | Yes | Roll back the whole transaction first |
| `40P01` deadlock detected | Yes | Roll back, jittered backoff |
| `08xxx` connection failure | Yes | New connection; transaction is gone |
| `53300` too many connections | Yes | Backoff; do not open more connections |
| `57014` query canceled | Conditional | Retry only if the cancel was a timeout, not a user cancel |
| `23xxx` integrity | No | Fix the data/request |
| `42xxx` schema | No | Deploy/migration fault — alert |

Keep DB retries **short** (2–3 attempts, tens of milliseconds) and inside the transaction boundary
that can roll back cleanly.

## 27.22 — Provider retries

Provider retries combine classification, `Retry-After`, and idempotency.

| Provider signal | Action |
| --------------- | ------ |
| `429` + `Retry-After` | Wait the hint, retry within deadline |
| `503` + `Retry-After` | Same |
| `500`/`502`/`504` | Exponential backoff with jitter |
| `401`/`403` | Do not retry; refresh credentials first |
| `400`/`422` | Do not retry; fix the request |
| Network timeout on a write | Retry **only with an idempotency key** |

Provider SDKs often retry by default. Check the configuration and either adopt or disable their
policy explicitly — never run two silently.

## 27.23 — Job retries

Background jobs have a different budget: minutes or hours, not seconds.

| Concern | Job retry approach |
| ------- | ------------------ |
| Max attempts | 3–5 (plus a DLQ) |
| Delay | Exponential, minutes-scale (e.g. 30s, 2m, 10m) |
| Idempotency | Checkpoint + idempotent writes |
| Partial work | Resume from the last checkpoint, don't restart blindly |
| Poison messages | Cap attempts, then DLQ (Chapter 32) |
| Deadlines | Per-attempt timeouts plus an overall job SLA |

A job retry that restarts from zero after processing 90% of a 2-hour export is a capacity bug even
when it is "correct."

## Worked example — one owner, end to end

```text
Checkout request (deadline 8s)
  └─ payment service: owns retry (3 attempts, full jitter, 8s deadline)
      └─ Stripe SDK: retries DISABLED
          └─ HTTP client: no retry, 2s timeout
```

If Stripe returns `429 Retry-After: 2`, the payment service waits 2s and retries with the **same**
idempotency key. The gateway and SDK do not add attempts. Exhaustion returns
`PAYMENT_UNAVAILABLE` (retryable, `Retry-After` preserved) with the last Stripe error as cause.

## Key data / numbers

- Amplification = product of attempts per layer (`2 × 3 × 3 = 18`).
- Typical job backoff: 30s, 2m, 10m; typical user-facing backoff: 100–500ms base.
- A retry budget of 10–20% caps aggregate amplification.
- Postgres `40P01`/`40001` require rollback before retry.
- Provider `Retry-After` is authoritative; parse both seconds and HTTP-date forms.
- DLQ threshold commonly equals `maxAttempts` (e.g. 5).

## Real-world use case — WebhookIngest

`WebhookIngest` received duplicate Stripe events. The handler retried failed processing 3×, the
queue redelivered 5×, and the HTTP client retried 3× — up to 45 attempts for one event. Because
handlers were not idempotent, each retry could send a duplicate receipt email. The team disabled SDK
and client retries, made the queue the single retry owner (5 attempts with minutes-scale backoff and
a DLQ), and keyed processing by `event.id`. Duplicate emails stopped, and the DLQ caught genuinely
poisoned events instead of hiding them in retry loops.

## Trade-offs

| Choice | Pros | Cons |
| ------ | ---- | ---- |
| Retry high in the stack | Full context, one owner | Longer feedback loop |
| Retry low in the stack | Fast, local | Multiplies invisibly |
| Long job retries | Survives long outages | Slow failure detection |
| Short job retries + DLQ | Fast detection, replayable | Requires DLQ operations |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Name one retry owner per dependency | Let gateway, service, and SDK all retry |
| Count total attempts in metrics | Report only configured attempts |
| Preserve the last error and attempt count | Throw a fresh generic error |
| Retry the transaction after rollback | Retry a statement in an aborted transaction |
| Use a DLQ for exhausted jobs | Retry forever |
| Disable SDK retries explicitly | Assume the SDK does not retry |

## Common mistakes

- **Silent SDK retries** stacking with application retries.
- **Job retries without checkpoints**, repeating hours of work.
- **Exhaustion errors without causes**, making incidents un-debuggable.
- **Retrying during an open breaker**, defeating its purpose.
- **Treating `57014` as always retryable**, including user-initiated cancellation.

## Checklist

- [ ] Each dependency has exactly one documented retry owner.
- [ ] Total worst-case attempts are calculated and acceptable.
- [ ] Job retries use checkpoints and end in a DLQ.
- [ ] Exhaustion preserves the last cause, attempts, and elapsed time.
- [ ] Provider SDK retry settings are explicit.
- [ ] DB retries roll back before retrying.

## Related

- [Retry Amplification and Budgets](../02-deep-dive/02-retry-amplification-and-budgets.md)
- [Retries for DB, Providers, and Jobs](../03-practical-examples/02-retries-for-db-provider-and-jobs.md)
- [Chapter 32 — Background Jobs, Queues, and Scheduled Tasks](../../../part-12-async-and-background-jobs/32-background-jobs-queues-and-scheduled-tasks/README.md)
- [Retry vs Fail Decision Guide](../05-reference/README.md)
