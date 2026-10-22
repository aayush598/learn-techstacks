# Chapter 27 — Retry Policies

> Part XI · _Estimated reading time: 95–120 min_
> **Prerequisite:** [Chapter 26 — Network and Distributed Communication Errors](../../part-10-external-dependencies/26-network-and-distributed-communication-errors/README.md)

## One-sentence summary

A retry policy is an **explicit, bounded contract** that says *which failures may be retried, how
many times, how long to wait, how long the caller is willing to wait overall, and who owns the
retry* — and it is only safe when the operation is idempotent.

## Why this chapter matters

Retries are the cheapest reliability win available: most dependency failures are transient, and a
short backoff often turns a visible error into a non-event. They are also the easiest way to turn a
small outage into a large one. A retry loop with no cap, no jitter, no deadline, and no idempotency
does not "handle" failure — it **amplifies** it, charges customers twice, and synchronizes every
client into a retry storm. The difference between the two outcomes is a policy, not a `catch` block.

## Chapter map

The chapter has 25 sections. They are grouped into these files:

| File | Subsections covered | What you learn |
| ---- | ------------------- | -------------- |
| [`01-concepts/01-why-retry-and-when-it-is-dangerous.md`](./01-concepts/01-why-retry-and-when-it-is-dangerous.md) | 27.1–27.3 | Why retries help, when they are appropriate, and the exact conditions that make them dangerous |
| [`01-concepts/02-retry-classification-and-eligibility.md`](./01-concepts/02-retry-classification-and-eligibility.md) | 27.4, 27.5, 27.24 | Retryable vs non-retryable; a classification table; side-effect retry rules |
| [`01-concepts/03-attempts-delays-and-jitter.md`](./01-concepts/03-attempts-delays-and-jitter.md) | 27.6–27.9 | Max attempts, fixed delay, exponential backoff, and jitter |
| [`01-concepts/04-budgets-deadlines-and-server-guidance.md`](./01-concepts/04-budgets-deadlines-and-server-guidance.md) | 27.10–27.14 | Retry budgets, retry deadlines, total vs per-attempt timeout, server instructions, `Retry-After` |
| [`01-concepts/05-storms-ownership-and-exhaustion.md`](./01-concepts/05-storms-ownership-and-exhaustion.md) | 27.15–27.23 | Retry storms, amplification, nested retries, layer ownership, preserving the final failure, meaningful exhaustion, DB/provider/job retries |
| [`02-deep-dive/01-backoff-and-jitter-math.md`](./02-deep-dive/01-backoff-and-jitter-math.md) | 27.6–27.9, 27.11 | The AWS full-jitter formula, expected delay, total elapsed time, choosing caps |
| [`02-deep-dive/02-retry-amplification-and-budgets.md`](./02-deep-dive/02-retry-amplification-and-budgets.md) | 27.10, 27.15–27.18 | Fan-out math, nested retry multiplication, and how budgets bound load |
| [`03-practical-examples/01-reusable-retry-utility-with-jitter.md`](./03-practical-examples/01-reusable-retry-utility-with-jitter.md) | 27.25, all | A production-shaped TypeScript retry utility with classification, jitter, deadline, and budget hooks |
| [`03-practical-examples/02-retries-for-db-provider-and-jobs.md`](./03-practical-examples/02-retries-for-db-provider-and-jobs.md) | 27.21–27.24 | Postgres, Stripe, `ExportJob`, and side-effect retry configurations |
| [`04-dos-and-donts/README.md`](./04-dos-and-donts/README.md) | all | Retry rules, anti-patterns, and a review checklist |
| [`05-reference/README.md`](./05-reference/README.md) | all | Retry-vs-fail decision guide, status/code table, policy defaults |

## Learning objectives

By the end you can:

- Explain why a retry is a bet on *transient* failure and name when that bet is wrong.
- Classify any error as retryable, retryable-with-preconditions, or non-retryable.
- Choose `maxAttempts`, base delay, multiplier, jitter, cap, budget, and deadline for a dependency.
- Honor `Retry-After` and other server instructions instead of guessing.
- Identify nested retries and assign **one owner** per retry decision.
- Produce a meaningful terminal error after exhaustion instead of a generic `500`.

## Key takeaways

1. **Retry eligibility is a property of the error, not of the call site.** Classify first, retry
   second.
2. **Retries multiply across layers.** Two layers each doing 3 attempts = 9 calls. Name one owner.
3. **Backoff must be bounded and jittered.** `min(cap, base × 2^attempt) × random()` is the default.
4. **A deadline beats an attempt count.** Stop when the caller's remaining budget is exhausted.
5. **Honor `Retry-After`.** The server knows when it will be ready; your backoff does not.
6. **Never retry a non-idempotent side effect without a key** (see Chapter 28).
7. **Preserve the final failure and its cause.** "Retries exhausted" must still carry the last
   real error, attempt count, and elapsed time.

## Exercises

1. Find every retry loop in your codebase and label its owner (client, service, worker, SDK).
2. Take one provider integration and write its retry table: status → retryable? → hint.
3. Compute the worst-case elapsed time for a 3-attempt policy with a 2s per-attempt timeout and
   1s base exponential backoff.
4. Simulate 1,000 clients retrying with no jitter, then with full jitter — compare peak RPS.
5. Add a deadline to a retry loop that currently only counts attempts.

## Related

- [Chapter 28 — Idempotency and Duplicate-Operation Safety](../28-idempotency-and-duplicate-operation-safety/README.md)
- [Chapter 29 — Timeouts, Circuit Breakers, and Bulkheads](../29-timeouts-circuit-breakers-and-bulkheads/README.md)
- [Part X — External Dependencies and Integration Errors](../../part-10-external-dependencies/README.md)
- [Glossary](../../GLOSSARY.md)
