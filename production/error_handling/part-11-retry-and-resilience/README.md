# Part XI — Retry Logic and Resilience

> **Chapters 27–30.** Parts IX and X taught you to *classify* database, network, and provider
> failures. This part answers the operational question that follows: **once you know a dependency
> failed, what do you do about it?** Retrying, deduplicating, time-boxing, isolating, and degrading
> are the five moves that turn a transient dependency blip into a non-event — and the same five
> moves, applied carelessly, turn one failing service into a system-wide outage.

## Learning objectives

By the end of Part XI you will be able to:

1. Decide **whether to retry** an error at all, using retry eligibility rather than optimism.
2. Design **retry policies** with bounded attempts, exponential backoff, jitter, budgets, and
   deadlines — and honor server guidance such as `Retry-After`.
3. Make retried operations **safe** with idempotency keys, duplicate detection, and a clear key
   lifecycle.
4. Bound latency and failure spread with **timeouts, deadline propagation, circuit breakers, and
   bulkheads**.
5. Degrade **deliberately** with fallbacks, cached responses, partial features, and explicit
   fail-open/fail-closed decisions.

## Chapters

| # | Chapter | Focus |
| - | ------- | ----- |
| 27 | [Retry Policies](./27-retry-policies/README.md) | Why and when to retry, classification, attempts, fixed/exponential/jittered backoff, budgets, deadlines, `Retry-After`, retry storms, nested retries, ownership, exhaustion, DB/provider/job retries, reusable framework |
| 28 | [Idempotency and Duplicate-Operation Safety](./28-idempotency-and-duplicate-operation-safety/README.md) | What idempotency means, keys, duplicate detection, storage/TTL, concurrent same-key requests, replay, failure contracts, payments, jobs, webhooks, distributed safety, preventing duplicate billing |
| 29 | [Timeouts, Circuit Breakers, and Bulkheads](./29-timeouts-circuit-breakers-and-bulkheads/README.md) | Connection/request/operation deadlines, propagation, cancellation, breaker states and thresholds, half-open probes, misuse, bulkhead isolation, concurrency limits, queue saturation, admission control, combined mechanisms |
| 30 | [Graceful Degradation and Fallbacks](./30-graceful-degradation-and-fallbacks/README.md) | Required vs optional, fallback responses, cached/stale data, partial features, degraded mode, fallback chains, fallback failure, avoiding silent inaccuracy, communicating degradation, fail-open vs fail-closed, avoiding cascades |

## The one idea that unifies this part

> **Resilience is a sequence of explicit decisions, not a blanket `try { retry() }`.**

```text
 A call fails
     │
     ├─ Is it transient and retry-safe? ──▶ NO  ──▶ fail / compensate / degrade
     │                                      │
     │ YES                                  │
     ▼                                      │
 Can we afford another attempt?              │
 (attempts left, budget, deadline) ──▶ NO ───┤
     │ YES                                  │
     ▼                                      │
 Is the dependency healthy enough? ──▶ NO ───┤  (breaker open / bulkhead full)
     │ YES                                  │
     ▼                                      │
 Retry with backoff + jitter,               │
 carrying the SAME idempotency key ─────────┘
     │
     └─ Still failing? ──▶ degrade, fall back, or return a meaningful terminal error
```

Each box belongs to a specific chapter: eligibility (27), duplicate safety (28), health and
capacity (29), and the terminal decision (30). Skipping any box is how systems develop retry storms,
double charges, and cascading failures.

## How to study this part

- Read Chapter 27 first, then Chapter 28 **immediately** — retries without idempotency are a bug,
  not a policy.
- Keep the recurring cast in mind: `Checkout` (idempotent payments), `ExportJob` (job retries and
  DLQ), `WebhookIngest` (duplicate delivery), `AgentRun` (provider retries and fallback models).
- For every retry in your codebase, ask the four questions: *retryable? idempotent? within budget?
  who owns the retry?*

## Key takeaways

1. **Retry only transient, retry-safe failures.** A `400`, `401`, `404`, `422`, or business decline
   will fail identically forever; retrying it wastes capacity and delays the user.
2. **Backoff without jitter synchronizes your fleet.** Add jitter to break the thundering herd.
3. **Every retry needs a budget and a deadline.** Unbounded retries convert a dependency outage into
   a self-inflicted one.
4. **Idempotency is the precondition for safe retries**, especially for payments, jobs, and webhooks.
   Use a key TTL (commonly 24h) and replay the original success.
5. **Stop calling a failing dependency.** Circuit breakers and bulkheads protect the caller *and*
   give the dependency room to recover.
6. **Degrade explicitly and visibly.** A fallback that silently returns wrong data is worse than an
   honest error.

## Part-level reference map

| Question | Where |
| -------- | ----- |
| Should I retry this error? | [Retry vs Fail guide](./27-retry-policies/05-reference/README.md) |
| How many attempts and how long? | [Backoff math](./27-retry-policies/02-deep-dive/01-backoff-and-jitter-math.md) |
| Can this operation be retried safely? | [Idempotency key lifecycle](./28-idempotency-and-duplicate-operation-safety/02-deep-dive/01-idempotency-key-lifecycle.md) |
| When should the breaker open? | [Breaker state machine](./29-timeouts-circuit-breakers-and-bulkheads/02-deep-dive/01-breaker-state-machine.md) |
| Should this fail open or closed? | [Fail-open vs closed](./30-graceful-degradation-and-fallbacks/05-reference/README.md) |

## Related

- [Part X — External Dependencies and Integration Errors](../part-10-external-dependencies/README.md)
- [Part XII — Asynchronous Processing and Background Jobs](../part-12-async-and-background-jobs/README.md)
- [Part IX — Database, Persistence, and Transaction Errors](../part-09-database-and-transactions/README.md)
- [Glossary](../GLOSSARY.md)
