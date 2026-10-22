# Chapter 10 — Centralized and Distributed Error Handling

> Part IV · _Estimated reading time: 65–90 min_
> **Prerequisite:** [Chapter 9 — Designing a Layered Error-Handling Architecture](../09-layered-error-handling-architecture/README.md)
> (layer ownership must exist before you centralize anything)

## One-sentence summary

Centralized handling (global handlers, middleware, interceptors, decorators, shared utilities)
owns the **mechanical** end of error handling — serialization, correlation, safety-net behavior —
while **business decisions stay local**, and both halves must share one **contract** that
survives module and service boundaries.

## Why this chapter matters

Centralization is seductive: one `ErrorHandler` class and the codebase "handles errors." Two
failure modes follow, and every mature SaaS hits both:

- **Over-centralization** — the global handler starts deciding business outcomes it cannot know
  (retry? compensate? is this a conflict?), producing wrong statuses, hidden logic, and handlers
  nobody dares touch.
- **Under-centralization** — every module invents its own envelope, status mapping, and logging
  shape; clients see five error formats, and cross-service incidents take hours to correlate.

This chapter draws the line precisely: **what belongs in one place, what must stay local, and how
the same discipline scales from a modular monolith to independently deployed services.**

## Chapter map

The chapter has 17 sections, grouped into eleven files:

| File | Subsections covered | What you learn |
| ---- | ------------------- | -------------- |
| [`01-concepts/01-centralized-vs-local-handling.md`](./01-concepts/01-centralized-vs-local-handling.md) | 10.1, 10.2, 10.9 | The two halves: one policy engine, many local decisions |
| [`01-concepts/02-the-machinery-of-centralized-handling.md`](./01-concepts/02-the-machinery-of-centralized-handling.md) | 10.3–10.8 | Global handlers, framework handlers, middleware, interceptors, decorators, shared utilities |
| [`01-concepts/03-limits-of-a-global-handler.md`](./01-concepts/03-limits-of-a-global-handler.md) | 10.10, 10.11 | Why a global handler cannot make business decisions — and how they sneak in |
| [`01-concepts/04-contracts-across-modules-and-services.md`](./01-concepts/04-contracts-across-modules-and-services.md) | 10.14–10.17 | Modular monoliths, microservices, deploy boundaries, one contract |
| [`02-deep-dive/01-avoiding-coupling-and-the-giant-module.md`](./02-deep-dive/01-avoiding-coupling-and-the-giant-module.md) | 10.12, 10.13 | Dependency direction, the error "god module," and splitting it |
| [`02-deep-dive/02-composition-ordering-and-fallthrough.md`](./02-deep-dive/02-composition-ordering-and-fallthrough.md) | 10.5–10.7 | Middleware/interceptor/decorator ordering, double-serialization, headers already sent |
| [`03-practical-examples/01-global-handler-and-local-recovery.md`](./03-practical-examples/01-global-handler-and-local-recovery.md) | 10.1–10.11 | A global handler and a local `AgentRun` recovery, working together |
| [`03-practical-examples/02-consistent-contracts-across-services.md`](./03-practical-examples/02-consistent-contracts-across-services.md) | 10.14–10.17 | One error contract across Checkout API, billing worker, webhook consumer |
| [`04-dos-and-donts/README.md`](./04-dos-and-donts/README.md) | all | Centralization rules and anti-patterns |
| [`05-reference/README.md`](./05-reference/README.md) | all | Mechanism chooser, global-vs-local table, contract checklist |

## Learning objectives

By the end you can:

- Split error handling into a **central policy layer** and **local decision points** without
  overlap, and say which mechanisms implement each.
- Choose the right mechanism per job: global exception filter, middleware, interceptor,
  decorator, or plain utility function.
- Detect business logic hiding inside global handlers and move it to the owning layer.
- Keep one error **contract** intact across modules, services, and independently deployed
  components — including old clients meeting new codes.

## Key takeaways

1. **Centralize mechanics, localize decisions.** Serialization, correlation IDs, and the
   unclassified-error safety net are global; retry, compensation, and conflict verdicts are not.
2. **A global handler is a safety net, not an oracle.** It sees the error without the business
   state that would justify a decision (10.10).
3. **Mechanisms are interchangeable; policy is not.** Middleware, filters, interceptors, and
   decorators are transport-specific packaging of the same two jobs: *catch at the edge* and
   *serialize consistently*.
4. **Coupling kills centralization** — if the handler imports every domain type (10.12) it
   becomes the god module everyone fears to change (10.13).
5. **The contract is the product of this chapter.** Across a modular monolith it is a shared
   package; across services it is a versioned envelope plus stable codes that old consumers
   tolerate (10.14–10.17).

## Exercises

1. List everything your global handler currently does. Label each line *mechanical* or
   *business*. Move the business lines to their owning layer.
2. For one endpoint, write which mechanism (middleware / filter / decorator / utility) handles
   parsing failures, auth failures, domain failures, and unknown errors — in that order.
3. Take two services that return errors to each other and diff their envelopes field by field;
   write the one shared schema you wish you had.
4. Simulate "new service emits code `BILLING_PROVIDER_DEGRADED`" and describe exactly what an
   old client does with it.

## Related

- [Chapter 9 — Layered Error-Handling Architecture](../09-layered-error-handling-architecture/README.md)
- [Chapter 11 — The Error Lifecycle](../11-the-error-lifecycle/README.md)
- [Chapter 45 — Organizing Error-Handling Modules](../../part-17-organization/45-organizing-error-handling-modules/README.md)
- [Part IV Index](../README.md)
