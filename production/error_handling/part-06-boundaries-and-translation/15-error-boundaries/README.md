# Chapter 15 — Error Boundaries

> Part VI · _Estimated reading time: 70–95 min_
> **Prerequisite:** [Part IV — Layered Architecture](../../part-04-architecture/09-layered-error-handling-architecture/README.md)

## One-sentence summary

An **error boundary** is a deliberate architectural line where an error is caught, translated,
contained, or safely propagated instead of crossing that line uncontrolled — and the entire
reliability of a system comes down to **where you draw those lines and who owns them**.

## Why this chapter matters

One un-timed-out call or one uncaught exception at the wrong layer turns a local blip into a
tenant-wide outage. Boundaries are how you shrink the **blast radius** of a failure: a degraded
recommendations card instead of a blank dashboard, a single failed job instead of a stalled queue,
a `409` instead of a leaked SQL string. Get boundaries wrong and no amount of retry or fallback
logic saves you, because the error never reached the code that knows what to do with it.

## Chapter map

The chapter has 18 sections. They are grouped into these files:

| File | Subsections covered | What you learn |
| ---- | ------------------- | -------------- |
| [`01-concepts/01-what-error-boundaries-are.md`](./01-concepts/01-what-error-boundaries-are.md) | 15.1, 15.2, 15.14 | Definition, why they are necessary, preventing leakage |
| [`01-concepts/02-code-level-boundaries.md`](./01-concepts/02-code-level-boundaries.md) | 15.3–15.5 | Function-, module-, and domain-level boundaries |
| [`01-concepts/03-runtime-boundaries.md`](./01-concepts/03-runtime-boundaries.md) | 15.6–15.12 | Request, transaction, job, process, service, third-party, and UI boundaries |
| [`01-concepts/04-ownership-granularity-and-fallback.md`](./01-concepts/04-ownership-granularity-and-fallback.md) | 15.13, 15.15, 15.17, 15.18 | Ownership, correct granularity, fallback behavior, isolation vs propagation |
| [`02-deep-dive/01-nested-boundaries.md`](./02-deep-dive/01-nested-boundaries.md) | 15.16 | How inner and outer boundaries compose, swallow, rethrow, and terminate |
| [`02-deep-dive/02-boundary-ownership-and-preventing-leakage.md`](./02-deep-dive/02-boundary-ownership-and-preventing-leakage.md) | 15.13–15.14 | Assigning an owner per boundary; the mechanics of stopping leaks |
| [`03-practical-examples/01-acme-request-boundary-map.md`](./03-practical-examples/01-acme-request-boundary-map.md) | all | A full boundary map for an Acme SaaS request using the recurring cast |
| [`03-practical-examples/02-postgres-sqlstate-boundary-map.md`](./03-practical-examples/02-postgres-sqlstate-boundary-map.md) | all | SQLSTATE codes caught and contained at the repository boundary |
| [`04-dos-and-donts/README.md`](./04-dos-and-donts/README.md) | all | Boundary rules, anti-patterns, checks |
| [`05-reference/README.md`](./05-reference/README.md) | all | Boundary placement guide and decision tree |

## Learning objectives

By the end you can:

- Name the boundary at every level of your stack and state its owner and fallback.
- Decide **correct granularity** — not too broad (one global handler), not too narrow (a
  `try/catch` per line).
- Explain how nested boundaries interact and avoid stealing a decision from an outer layer.
- Prevent information leakage across a boundary (stacks, SQL, vendor payloads).
- Choose between **isolation** (contain now) and **propagation** (let the right owner decide).

## Key takeaways

1. **Place a boundary where the fallback differs from propagating.** If there is no meaningful
   alternative, do not catch — add context and propagate.
2. **Boundaries change ownership.** After the line, a different layer is responsible for the
   decision; make that explicit in code structure, not comments.
3. **Granularity is the hard part.** The right size is the smallest scope that owns a distinct
   fallback.
4. **Nesting requires discipline.** An inner boundary must not convert a recoverable failure into
   a success the outer boundary cannot fix.
5. **Every boundary is also a translation point.** Chapter 16 covers what crosses the line.

## Exercises

1. Draw your main request path and mark every boundary it crosses; label each owner and fallback.
2. Find one `try/catch` in your codebase with no meaningfully different fallback and delete it.
3. Pick your largest dependency and write the boundary that contains it.
4. For a nested boundary pair in your code, decide which layer should own the final outcome.

## Related

- [Chapter 16 — Error Translation and Normalization](../16-error-translation-and-normalization/README.md)
- [Part IV — Centralized and Distributed Error Handling](../../part-04-architecture/10-centralized-and-distributed-error-handling/README.md)
- [Part XI — Timeouts, Circuit Breakers, and Bulkheads](../../part-11-retry-and-resilience/29-timeouts-circuit-breakers-and-bulkheads/README.md)
