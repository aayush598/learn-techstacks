# Failure Domains and Fault Boundaries

> Part I · Chapter 1 · Sections 1.16, 1.18 · _Estimated reading time: 18 min_

## In one sentence

A **failure domain** is the set of components affected when one component fails, and a **fault
boundary** is a deliberate line you draw to stop a failure from crossing into another domain.

## Why this matters in production

Without boundaries, one flaky function takes down the whole request, worker, or process. With
them, a failure is *localized*: a degraded recommendations widget, not a blank page; a failed
single job, not a stalled queue. Boundaries are how you turn a 100% outage into a 2% degradation.

## Failure domain

Think of your system as overlapping sets. A failure domain is the smallest set that shares fate.

```text
┌─────────────────────────── Process (shared fate: a crash kills all) ──┐
│                                                                       │
│  ┌── Request A ──┐   ┌── Request B ──┐   ┌── Worker pool ──────────┐  │
│  │ DB conn pool  │   │ same pool ◀───┼───▶ shares pool → shared   │  │
│  └───────────────┘   └───────────────┘   │   failure domain        │  │
│                                          └─────────────────────────┘  │
│  Shared: memory, file descriptors, thread pool, connection pool       │
└───────────────────────────────────────────────────────────────────────┘
```

Common failure domains:

- A single process (uncaught exception, OOM, deadlock).
- A connection pool (exhaustion affects every request using it).
- A shared thread/worker pool (one blocking task starves others).
- A tenant's data partition (noisy neighbor).
- A whole dependency (every caller of Stripe).
- A region/AZ.

**Blast radius** is how far a failure spreads. Your job is to shrink it.

## Fault boundary

A fault boundary is where you *choose* to catch and contain. Examples:

| Boundary | Contains | Fallback |
| -------- | -------- | -------- |
| HTTP middleware | Any error in a request | JSON error envelope |
| Per-feature try/catch | Optional widget failure | Empty/placeholder UI |
| Per-job worker wrapper | A single job crashing | Retry / DLQ |
| Circuit breaker around provider | Provider outage | Degraded mode |
| Per-tenant quota/bulkhead | One tenant's load | 429 for that tenant only |

```ts
// Per-feature boundary: recommendations failure must not break the page.
let recommendations: Item[] = [];
try {
  recommendations = await recommend(productId); // optional dependency
} catch (err) {
  log.warn({ err, productId }, "recommendations unavailable, degrading");
  // fallback: empty list; the page still renders
}
```

## Choosing boundary granularity

- **Too broad** (one global handler only): one failure = whole request fails; no degradation.
- **Too narrow** (try/catch around every line): noise, masking, and unmaintainable code.
- **Right-sized**: at points where a *decision* exists — can we continue safely, or must we fail?

Rule of thumb: **place a boundary where the fallback behavior is meaningfully different from
propagating.**

## Blast-radius reduction techniques

| Technique | Reduces blast radius of |
| --------- | ----------------------- |
| Bulkheads / separate pools | Pool exhaustion |
| Circuit breakers | Dependency outage |
| Per-tenant rate limits | Noisy neighbor |
| Timeouts everywhere | Hanging requests and workers |
| Worker wrappers | A single bad job |
| Feature flags | A buggy feature |
| Cell/partition architecture | Regional or tenant-wide failures |

(These are expanded in Chapters 29 and 57.)

## What "production-grade" actually means

Production-grade error handling is not "lots of try/catch." It is a set of properties:

1. **Every failure path has a defined outcome.** No path leaves state undefined.
2. **Errors are never silently discarded.** Swallowing is a bug.
3. **Failures are contained at chosen boundaries**, and blast radius is bounded.
4. **Recoverable failures recover** without human intervention, within defined limits.
5. **Unrecoverable failures terminate safely** and never corrupt data.
6. **Nothing sensitive leaks** to users or third parties (Chapter 34).
7. **Every error is classifiable, routable, and observable** through the information it carries.
8. **Behavior is consistent and predictable** across the codebase.
9. **It is maintainable**: routine errors are easy, unusual ones are explicit.
10. **It is testable**: failure paths can be triggered deliberately (property: correctness is
    verifiable even though full testing strategy is out of scope).

> A useful test: pick any line that can fail. Can you name its class, its boundary, its fallback,
> and its exit status? If not, it is not production-grade yet.

## Real-world use case — Acme SaaS

Acme's dashboard embeds an LLM "summarize" feature. Initially, an LLM timeout propagated and
500-ed the whole dashboard. They introduced a fault boundary around the summary call: on failure,
show a cached summary or a "summary unavailable" placeholder. Blast radius shrank from "whole
dashboard inaccessible" to "one card degraded." The LLM stayed on the critical path *as a
feature*, not as a dependency of the page.

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Draw boundaries where fallback differs | Wrap every line in try/catch |
| Isolate pools per dependency/tenant | Share one pool across everything |
| Measure and shrink blast radius | Assume redundancy without isolation is enough |

## Common mistakes

- **Boundary at the wrong layer** — catching in the domain when the fallback belongs at the edge.
- **Shared fate by accident** — using one HTTP client/pool for independent providers.
- **Unbounded blast radius** — a memory leak in one endpoint exhausting the process.

## Checklist

- [ ] Have you listed the failure domains in your request path?
- [ ] Does each optional feature have its own boundary and fallback?
- [ ] Are dependencies isolated (separate pools/timeouts/breakers)?
- [ ] Can you express the blast radius of your biggest dependency failing?

## Related

- [The Classification Dimensions of Failure](../01-concepts/02-the-fifteen-dimensions.md)
- [Error Boundaries](../../../part-06-boundaries-and-translation/15-error-boundaries/README.md)
- [Timeouts, Circuit Breakers, and Bulkheads](../../../part-11-retry-and-resilience/29-timeouts-circuit-breakers-and-bulkheads/README.md)
