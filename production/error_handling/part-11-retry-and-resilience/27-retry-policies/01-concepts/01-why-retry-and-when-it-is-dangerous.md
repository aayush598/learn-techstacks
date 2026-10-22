# Why Retry — and When It Is Dangerous

> Part XI · Chapter 27 · Sections 27.1–27.3 · _Estimated reading time: 16 min_
> **Prerequisite:** [Chapter 26 — Network and Distributed Communication Errors](../../../part-10-external-dependencies/26-network-and-distributed-communication-errors/README.md)

## In one sentence

A retry is a **bet that a failure was transient**; it pays off on network blips and deadlocks and
destroys you on validation errors, non-idempotent side effects, and overloaded dependencies.

## Why this matters in production

Most production failures are not binary. A TCP reset, a deadlock, a `503` during a deploy, or a
rate-limit `429` usually succeeds on the next attempt. Without retries, every one of those becomes a
user-visible error. With a naive retry, a dependency that is already struggling receives *more*
traffic precisely when it can least afford it. The same code path therefore either **absorbs** a
blip or **amplifies** an outage; the difference is whether the retry is justified, bounded, and
targeted.

## 27.1 — Why retries exist

Distributed systems fail partially and temporarily. The failure taxonomy from Part II separates
**transient** from **permanent** errors for exactly this reason. Retries exploit that distinction:

| Failure | Without retry | With a correct retry |
| ------- | ------------- | -------------------- |
| Transient TCP reset | User sees an error | Succeeds on attempt 2 |
| Postgres deadlock (`40P01`) | Job fails permanently | Retried automatically |
| Provider `429` | Export stalls | Waits `Retry-After`, then succeeds |
| Deploy-time `503` | Checkout fails | Retried after a short backoff |
| Validation `422` | — | Fails identically on every attempt |

Retries buy **availability** at the cost of **latency, capacity, and duplicate risk**. They are not
free, and they are not a substitute for fixing the fault.

## 27.2 — When a retry is appropriate

Use the following four-part test. All four must hold:

1. **Transient** — the error class is expected to succeed later (timeout, reset, `503`, `429`,
   deadlock, serialization failure).
2. **Idempotent or keyed** — re-executing has the same effect as executing once, or the operation
   carries an idempotency key (Chapter 28).
3. **Bounded** — you have attempts, a budget, and a deadline; you can stop.
4. **Owned** — exactly one layer owns this retry decision, and the layers below have not already
   retried.

```text
retryable(err) AND safe_to_repeat(op) AND budget_remaining() AND deadline_not_exceeded() AND owns_retry(layer)
```

If any term is false, do not retry. Fail, compensate, or degrade instead.

## 27.3 — When retries are dangerous

### 1. Non-idempotent side effects

Retrying `POST /charges` after a timeout can charge twice when the first request actually succeeded
but the response was lost. This is the **ambiguous outcome** problem (Chapter 26, 28.15). The fix is
an idempotency key, not a shorter timeout.

### 2. Permanent errors

Retrying `400`, `401`, `403`, `404`, `409`, `422`, or a business decline wastes capacity and delays
the inevitable. It can also trigger account lockouts and rate-limit penalties.

### 3. Overload and retry storms

If a dependency is saturated, retries add load. Without jitter, synchronized clients retry in
lockstep. The dependency never gets the quiet period it needs to recover.

### 4. Nested retries

If the SDK retries 3×, your service retries 3×, and the gateway retries 2×, a single user request
can become 18 upstream calls. This is **retry amplification** (27.16).

### 5. Tight deadlines

A retry that cannot finish before the caller's deadline is pure waste. It consumes a connection and
a worker slot, then fails anyway.

### 6. Long-running or stateful operations

Retrying a job that has already written half its output can duplicate rows or corrupt a checkpoint.
Job retries need checkpointing and idempotent writes (27.23).

> ⚠️ **Hazard.** The most expensive retry bug is not a failed retry — it is a *successful duplicate*.
> A retry that charges a card twice looks like success in every dashboard.

## Worked example

```ts
// Dangerous: retries every error, including validation and non-idempotent charges.
async function createChargeBad(input: ChargeInput) {
  for (let i = 0; i < 3; i++) {
    try {
      return await gateway.charge(input); // may succeed server-side, then time out
    } catch {
      continue; // retries 422 forever-ish, and can double-charge
    }
  }
  throw new Error("failed");
}
```

```ts
// Safer: classify, require a key, bound attempts.
async function createCharge(input: ChargeInput, key: string) {
  return retry(
    () => gateway.charge({ ...input, idempotencyKey: key }),
    {
      maxAttempts: 3,
      isRetryable: (e) => e.transient && e.status !== 422,
      deadlineMs: 8_000,
      baseDelayMs: 200,
      jitter: "full",
    },
  );
}
```

The second version only retries transient errors, reuses the same key so the provider collapses
duplicates, and stops at a deadline.

## Key data / numbers

- Retryable HTTP statuses: `408`, `429`, `500` (provider-dependent), `502`, `503`, `504`.
- Non-retryable HTTP statuses: `400`, `401`, `403`, `404`, `405`, `409`, `413`, `415`, `422`.
- Retryable Postgres classes: `40001` (serialization), `40P01` (deadlock), `08xxx` (connection),
  `53300` (too many connections).
- Non-retryable Postgres classes: `23xxx` (integrity), `42xxx` (schema/syntax).
- `Retry-After` is authoritative for `429` and `503` when present.
- A common starting policy: 3 attempts, 100–500ms base, ×2 multiplier, full jitter, cap 10–30s.

## Real-world use case — Checkout

Checkout called Stripe's charge endpoint with a 3-attempt retry on *every* exception. During a
provider incident, a request timed out **after** Stripe had captured the payment; the retry created a
second charge. Customers were double-billed and finance spent two days reconciling. The fix was
threefold: mark only `429`/`5xx`/network errors retryable, attach a per-order idempotency key, and
reuse it across attempts. Duplicate charges dropped to zero, and the retry still absorbed normal
transient failures.

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| No retry | Simple, no duplicates | Every blip is visible | Non-idempotent, strict latency |
| Immediate retry | Fast recovery | Hammers a struggling dependency | Almost never |
| Backoff + jitter | Absorbs blips, spreads load | Adds latency | Default for transient errors |
| Retry with key | Safe for side effects | Requires key storage | Payments, jobs, webhooks |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Retry only classified-transient errors | Retry everything in a `catch` |
| Require idempotency for side effects | Retry `POST /charges` blindly |
| Bound by attempts, budget, and deadline | `while (true)` with a sleep |
| Name one retry owner per dependency | Let SDK, service, and gateway all retry |
| Log attempts and the final cause | Log only "retry failed" |

## Common mistakes

- **Retrying validation errors.** The user waits longer for the same rejection.
- **Retrying after a timeout without a key.** The first attempt may have succeeded.
- **Retrying inside a transaction that is already aborted.** Postgres requires a rollback first.
- **Adding retries to hide a permanently failing dependency.** It delays detection and grows queues.
- **Forgetting that the SDK already retries.** You silently multiply attempts.

## Checklist

- [ ] Every retry has an explicit retryability predicate.
- [ ] Side-effecting operations carry an idempotency key before retrying.
- [ ] Each dependency has exactly one retry owner.
- [ ] Attempts, budget, and deadline are all bounded.
- [ ] Permanent errors short-circuit immediately.
- [ ] Exhaustion returns the last real cause, not a generic failure.

## Related

- [Retry Classification and Eligibility](./02-retry-classification-and-eligibility.md)
- [Attempts, Delays, and Jitter](./03-attempts-delays-and-jitter.md)
- [Chapter 28 — Idempotency and Duplicate-Operation Safety](../../28-idempotency-and-duplicate-operation-safety/README.md)
- [Retry vs Fail Decision Guide](../05-reference/README.md)
