# Chapter 29 — Timeouts, Circuit Breakers, and Bulkheads

> Part XI · _Estimated reading time: 85–105 min_
> **Prerequisite:** [Chapter 28 — Idempotency and Duplicate-Operation Safety](../28-idempotency-and-duplicate-operation-safety/README.md)

## One-sentence summary

Timeouts bound **how long** a failure can consume resources, circuit breakers bound **how often** you
call a failing dependency, and bulkheads bound **how much** of your capacity one dependency or tenant
can consume — together they stop failures from spreading.

## Why this chapter matters

Retries (Chapter 27) assume the dependency will eventually answer. Timeouts ensure it *answers or
gives up*; without them, a hung connection pins a worker forever. Circuit breakers stop the retry
loop when the dependency is clearly down, giving it room to recover. Bulkheads ensure that one slow
dependency or noisy tenant cannot exhaust the pools, queues, and threads shared by everyone else.
These three mechanisms are the difference between a localized degradation and a cascading outage.

## Chapter map

The chapter has 16 sections. They are grouped into these files:

| File | Subsections covered | What you learn |
| ---- | ------------------- | -------------- |
| [`01-concepts/01-why-timeouts-and-deadlines.md`](./01-concepts/01-why-timeouts-and-deadlines.md) | 29.1–29.4 | Why timeouts exist, connection/request/operation deadlines, propagation, timeout vs cancellation |
| [`01-concepts/02-circuit-breaker-states-and-conditions.md`](./01-concepts/02-circuit-breaker-states-and-conditions.md) | 29.5–29.9 | Breaker states, opening conditions, half-open probes, fallback errors, misuse |
| [`01-concepts/03-bulkheads-and-concurrency-limits.md`](./01-concepts/03-bulkheads-and-concurrency-limits.md) | 29.10–29.12 | Bulkhead isolation, concurrency limits, queue saturation |
| [`01-concepts/04-admission-control-and-combining-mechanisms.md`](./01-concepts/04-admission-control-and-combining-mechanisms.md) | 29.13–29.16 | Admission control, combining mechanisms, preventing amplification, dependency resilience policy |
| [`02-deep-dive/01-breaker-state-machine.md`](./02-deep-dive/01-breaker-state-machine.md) | 29.5–29.9, 29.14 | State diagrams, thresholds, sliding windows, probe policy, hysteresis |
| [`02-deep-dive/02-deadline-propagation.md`](./02-deep-dive/02-deadline-propagation.md) | 29.2–29.4, 29.13 | Deadline budgets across hops, gRPC `Deadline`, HTTP timeout headers, cancellation |
| [`03-practical-examples/01-circuit-breaker-implementation.md`](./03-practical-examples/01-circuit-breaker-implementation.md) | 29.5–29.9, 29.14 | A TypeScript breaker with closed/open/half-open and metrics |
| [`03-practical-examples/02-timeouts-and-bulkheads-for-acme.md`](./03-practical-examples/02-timeouts-and-bulkheads-for-acme.md) | 29.1–29.16 | End-to-end policies for Acme's dependencies and tenants |
| [`04-dos-and-donts/README.md`](./04-dos-and-donts/README.md) | all | Rules, thresholds, anti-patterns |
| [`05-reference/README.md`](./05-reference/README.md) | all | Resilience policy template, breaker/ bulkhead defaults, fail-open vs closed guide |

## Learning objectives

By the end you can:

- Separate connection, request, and operation deadlines and set each correctly.
- Propagate a remaining-time budget instead of resetting timeouts at every hop.
- Implement a circuit breaker with sensible thresholds, a sliding window, and half-open probes.
- Isolate dependencies and tenants with bulkheads and concurrency limits.
- Detect queue saturation and apply admission control before overload.
- Combine timeout, retry, breaker, and bulkhead without amplifying failures.

## Key takeaways

1. **Every network call needs a timeout.** No timeout is an infinite lease on a worker.
2. **A deadline is a budget, not a per-hop reset.** Pass the remaining time downstream.
3. **A breaker is a feedback control, not a retry.** It stops traffic so the dependency can recover.
4. **Open the breaker on a *rate* of failures, not a single error**, and probe carefully.
5. **Bulkheads are per dependency and per tenant**, or they do not isolate anything.
6. **Queue depth and wait time are leading indicators** of saturation; reject before collapse.
7. **Combine mechanisms in a fixed order**: deadline → breaker → bulkhead → retry → fallback.

## Exercises

1. Set connection, request, and operation timeouts for one dependency and justify each.
2. Trace a request across three services and verify the deadline shrinks at each hop.
3. Compute a breaker threshold that opens after ~5% failures in a 30s window.
4. Add a per-tenant concurrency limit and measure the effect on p99.
5. Simulate a dependency outage and confirm retries stop once the breaker opens.

## Related

- [Chapter 27 — Retry Policies](../27-retry-policies/README.md)
- [Chapter 30 — Graceful Degradation and Fallbacks](../30-graceful-degradation-and-fallbacks/README.md)
- [Chapter 26 — Network and Distributed Communication Errors](../../part-10-external-dependencies/26-network-and-distributed-communication-errors/README.md)
- [Glossary](../../GLOSSARY.md)
