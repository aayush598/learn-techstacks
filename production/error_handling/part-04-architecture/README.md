# Part IV — Error-Handling Architecture and System Boundaries

> **Chapters 9–11.** Error handling is not a set of `try/catch` statements scattered by taste; it
> is an *architecture*. This part defines where errors are created, owned, translated, propagated,
> recovered, and finally terminated — across every layer and every deployable component. Get this
> wrong and even a perfect taxonomy (Part II) and error model (Part III) leak, duplicate, and drift.

## Learning objectives

By the end of Part IV you will be able to:

1. Draw your system as **layers** (presentation → transport → controller → application → domain →
   repository → infrastructure → integration) and state each layer's error-handling
   **responsibility**.
2. Decide, for any given failure, whether it is **handled, translated, or propagated** — and stop
   handling the same error twice.
3. Design **centralized** handling (global handlers, middleware, interceptors, decorators) that
   remains honest about business decisions it cannot make.
4. Choose between **local recovery, centralized recovery, and termination**, and detect the
   hidden business logic that creeps into global handlers.
5. Trace an error through the **eight-stage lifecycle** from origin to terminal state, including
   cleanup, double-handling prevention, and failures inside the error handler itself.
6. Keep error **contracts consistent** across a modular monolith and across independently deployed
   services.

## Chapters

| # | Chapter | Focus |
| - | ------- | ----- |
| 9 | [Designing a Layered Error-Handling Architecture](./09-layered-error-handling-architecture/README.md) | Layer inventory, per-layer responsibility, where to handle / translate / propagate, preventing leakage |
| 10 | [Centralized and Distributed Error Handling](./10-centralized-and-distributed-error-handling/README.md) | Global handlers, middleware, interceptors, decorators, local vs global recovery, multi-service contracts |
| 11 | [The Error Lifecycle](./11-the-error-lifecycle/README.md) | Origin → detect → represent → classify → enrich → propagate → translate → recover → respond → finalize |

## How the three chapters fit together

```text
        Chapter 9  ── the STATIC view ──▶  "which layer owns this error?"
        Chapter 10 ── the CONTROL view ─▶  "one handler or many? local or central?"
        Chapter 11 ── the DYNAMIC view ─▶  "what happens to an error over time?"
```

Chapter 9 answers *where*, Chapter 10 answers *who acts*, and Chapter 11 answers *in what order*.
A design that is layered but centrally-handled inconsistently (9 without 10) or that handles
correctly but loses the causal chain (9+10 without 11) is the most common half-finished state.

## The recurring cast in Part IV

| Cast member | Layer path exercised |
| ----------- | -------------------- |
| **Checkout** | transport → controller → application → domain → repository → integration (Stripe) |
| **WebhookIngest** | transport → integration (signature verify) → application → repository |
| **ExportJob** | background worker → application → domain → repository → infrastructure (S3) |
| **Scheduled task** (nightly billing rollup) | scheduler → application → repository |
| **AgentRun** | application → integration (LLM provider) → integration (tool APIs) |

## Key takeaways

- **Layers are error *ownership* boundaries, not just import boundaries.** Each layer owns a class
  of failure and a translation step.
- **Handle once.** Every error has exactly one layer that decides its outcome; everything else
  translates or propagates.
- **A global handler is a safety net, not a decision engine.** It cannot know business intent.
- **The lifecycle is the same every time**, even for manual/adhoc code — only the actors change.
- **Contracts cross service boundaries; implementations do not.** A stable error code outlives the
  code that produced it.

## Related

- [Part III — Error Models and Representation](../part-03-error-models/README.md)
- [Part V — Exception Handling Mechanics](../part-05-exception-mechanics/README.md)
- [Part VI — Error Boundaries and Translation](../part-06-boundaries-and-translation/README.md)
- [Glossary](../GLOSSARY.md)
