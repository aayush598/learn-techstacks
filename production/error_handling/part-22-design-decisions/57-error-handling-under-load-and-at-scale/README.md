# Chapter 57 — Error Handling Under Load and at Scale

> Part XXII · _Estimated reading time: 120–150 min_
> **Prerequisite:** [Chapter 29 — Timeouts, Circuit Breakers, and Bulkheads](../../part-11-retry-and-resilience/29-timeouts-circuit-breakers-and-bulkheads/README.md), [Chapter 32 — Background Jobs, Queues, and Scheduled Tasks](../../part-12-async-and-background-jobs/32-background-jobs-queues-and-scheduled-tasks/README.md)

## One-sentence summary

Under load, errors **amplify**: one failure produces extra retries, extra log volume, extra
memory, and extra queue depth — so production error handling is mostly about **bounding the
amplification** and **isolating the blast radius**.

## Why this chapter matters

A system that handles errors perfectly at 10 requests/second can be the direct cause of an
outage at 10,000. The mechanisms are well known individually; what makes them dangerous is
that they **compose**:

- A dependency starts returning `503`. Callers **retry** it (3×). Each original request now
  becomes 3 downstream requests. The dependency's load triples at exactly the moment it can
  least afford it.
- Each failed attempt **throws an exception**, and each exception carries a stack trace. At
  10,000 failures/second, stack-trace capture and logging become a measurable share of CPU
  — the error path becomes a denial-of-service vector against your own service.
- Retries **hold connections**. The pool is exhausted, and now *unrelated* requests fail with
  "too many clients" — a healthy dependency is collateral damage.
- Queues **accumulate**. Workers spend their time retrying poison jobs instead of making
  progress, the backlog grows, and the queue's own retention starts deleting messages.

Each of these is survivable. Together they are the classic **error storm**: a small
percentage failure becomes a total outage.

This chapter gives you the arithmetic (amplification factors, retry budgets, queue drain
times) and the structures (bulkheads, per-tenant limits, admission control) to keep that
from happening — and to make the system *fail in a controlled way* when it does.

## Chapter map

The chapter has 18 subsections. They are grouped into five concept files, three deep dives,
and two worked examples:

| File | Subsections covered | What you learn |
| ---- | ------------------- | -------------- |
| [`01-concepts/01-failure-amplification-and-error-storms.md`](./01-concepts/01-failure-amplification-and-error-storms.md) | 57.1, 57.2, 57.3, 57.12, 57.15 | Error storms, failure amplification, retry storms, "overload without added overload", resource-aware recovery |
| [`01-concepts/02-isolation-tenants-features-dependencies.md`](./01-concepts/02-isolation-tenants-features-dependencies.md) | 57.4, 57.9, 57.10, 57.11 | Pool exhaustion, tenant isolation, feature isolation, and one dependency exhausting shared resources |
| [`01-concepts/03-bounding-queues-retries-and-backpressure.md`](./01-concepts/03-bounding-queues-retries-and-backpressure.md) | 57.5, 57.13, 57.14 | Queue buildup, bounding retries and queues, backpressure and rejection |
| [`01-concepts/04-resource-cost-of-errors.md`](./01-concepts/04-resource-cost-of-errors.md) | 57.6, 57.7, 57.8 | The CPU/memory cost of errors and stack traces, high-volume validation failures, errors during degradation |
| [`01-concepts/05-scaling-and-instance-consistency.md`](./01-concepts/05-scaling-and-instance-consistency.md) | 57.16, 57.17, 57.18 | Horizontal scaling, consistent policy across instances, avoiding shared mutable state |
| [`02-deep-dive/01-error-storm-math.md`](./02-deep-dive/01-error-storm-math.md) | 57.1, 57.2, 57.3, 57.12 | The amplification formula, worked storm scenarios, how far a 10% error rate travels |
| [`02-deep-dive/02-retry-budget-and-queue-bounding.md`](./02-deep-dive/02-retry-budget-and-queue-bounding.md) | 57.3, 57.5, 57.13, 57.14 | Retry budget calculation, queue depth limits, drain time, backpressure arithmetic |
| [`02-deep-dive/03-resource-cost-model.md`](./02-deep-dive/03-resource-cost-model.md) | 57.6, 57.7 | The cost of an error in CPU, memory, and log volume — and how to budget for it |
| [`03-practical-examples/01-load-shedding-and-admission-control-acme.md`](./03-practical-examples/01-load-shedding-and-admission-control-acme.md) | 57.12, 57.13, 57.14 (applied) | A complete load-shedding and admission-control implementation for Acme SaaS |
| [`03-practical-examples/02-noisy-neighbor-tenant-isolation.md`](./03-practical-examples/02-noisy-neighbor-tenant-isolation.md) | 57.9, 57.10, 57.11 (applied) | Per-tenant concurrency limits and bulkheads, with a worked noisy-neighbor incident |
| [`04-dos-and-donts/README.md`](./04-dos-and-donts/README.md) | all | Rules for load-time error handling, and the anti-patterns behind each outage |
| [`05-reference/README.md`](./05-reference/README.md) | all | Decision matrices for both chapters, load-shedding checklist, sizing tables |

## Learning objectives

By the end you can:

1. **Compute the amplification factor** of a retry topology and predict the downstream load
   for a given upstream error rate.
2. Size a **retry budget** so that retries never exceed a stated fraction of total traffic.
3. Explain **why an error path can take down a healthy service** — pool exhaustion, CPU spent
   on stack traces, queues that never drain.
4. Set **queue depth limits** and compute the **drain time** before the queue starts
   discarding work.
5. Design **tenant and feature isolation** so that one workload cannot consume another's
   capacity.
6. Implement **admission control / load shedding** that sheds the *right* requests first.
7. Keep **policy consistent across horizontally scaled instances** without introducing shared
   mutable state into the error path.

## The load-time invariants

| Invariant | Target | Consequence of violating it |
| --------- | ------ | ---------------------------- |
| Retries as a fraction of total requests | ≤ 5–10% | Retry storm |
| In-flight requests per dependency | ≤ 1.5× the healthy capacity | Dependency overload |
| Queue depth | Bounded; oldest item < 1 hour | Work is lost or processed stale |
| DB connection pool utilization at peak | ≤ 70% | Pool exhaustion under retry |
| Error-path CPU share | ≤ 5% of total CPU | The error path becomes the outage |
| Error log volume | Sampled above 100 errors/s | Log pipeline backpressure |
| Per-tenant concurrency | ≤ 10% of a tenant's fair share | Noisy neighbour |
| Shedding order | Optional → premium → standard | Wrong customers pay for capacity |

## Key takeaways

1. **Errors are load.** Every failed request costs CPU (stack capture), memory (allocation
   and buffering), and downstream attempts. An error rate spike is a capacity event.
2. **Amplification is multiplicative.** With 3 layers each retrying 3×, a single failure can
   produce 27 downstream attempts. Nested retries are the single most common storm cause.
3. **One retry owner per dependency.** The layer closest to the failure retries; layers above
   propagate. Two owners mean a 9× amplification instead of 3×.
4. **Bound the queue, not just the worker.** A queue with no depth limit converts a slow
   dependency into unbounded memory growth and stale work.
5. **Isolation is what makes scale real.** Two instances sharing one connection pool, one
   queue, and one breaker is one instance with extra steps.
6. **Shed deliberately.** Load shedding must be *ordered* by request value — shedding
   optional features first, rejecting with `429` and `Retry-After`, and never shedding
   writes that would leave partial state.
7. **Never put shared mutable state in the error path.** A shared "recent errors" counter
   becomes a contention point precisely when everything is failing.

## Exercises

1. Take your retry topology and compute the **amplification factor** using the formula in
   [`02-deep-dive/01-error-storm-math.md`](./02-deep-dive/01-error-storm-math.md). If it is
   above 3, find the layer that owns the retry and remove the others.
2. Set a **retry budget** of 10% for your most-called dependency and implement it. Watch the
   `retry_ratio` metric for a week.
3. Compute your **queue drain time** at peak arrival rate. If it exceeds the retry window of
   your slowest consumer, add a depth limit.
4. Size your **DB connection pool** for peak load *plus* retry headroom. If `max(pool) <
   1.5 × peak RPS × p95 latency`, you have a pool exhaustion incident waiting.
5. Load-test your error path: force 100 errors/second and measure the CPU share and the
   request latency of *successful* requests. If the error path costs more than 5% of CPU,
   sample your logs.
6. Write down your **shedding order**. If you cannot, that is your next outage.

## Related

- [Chapter 56 — Choosing Between Competing Approaches](../56-choosing-between-competing-approaches/README.md)
- [Part XXII index](../README.md)
- [Chapter 29 — Timeouts, Circuit Breakers, and Bulkheads](../../part-11-retry-and-resilience/29-timeouts-circuit-breakers-and-bulkheads/README.md)
- [Chapter 27 — Retry Policies](../../part-11-retry-and-resilience/27-retry-policies/README.md)
- [Glossary](../../GLOSSARY.md)
