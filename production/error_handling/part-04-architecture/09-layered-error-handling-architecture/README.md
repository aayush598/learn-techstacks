# Chapter 9 — Designing a Layered Error-Handling Architecture

> Part IV · _Estimated reading time: 70–95 min_
> **Prerequisite:** [Part III — Error Models](../part-03-error-models/README.md) (you need an error
> model and stable codes before you can route them through layers)

## One-sentence summary

A layered error-handling architecture assigns **each kind of failure to exactly one owning layer**,
defines where errors are **translated**, **handled**, or **propagated**, and makes the path from
origin to external response **consistent end to end**.

## Why this chapter matters

Without layer ownership, errors are handled wherever a developer happened to be editing. A
database exception gets caught in a controller; a domain invariant violation gets logged in a
repository; an infrastructure error leaks a driver message into a user response. The symptoms are
predictable: **duplicate handling**, **lost context**, **vendor leakage**, and a codebase where
nobody can answer "what happens to a `unique_violation` here?"

This chapter gives you the *static* map — which layer owns which failure — that the rest of Part
IV builds on.

## Chapter map

The chapter has 20 sections, grouped into eleven files:

| File | Subsections covered | What you learn |
| ---- | ------------------- | -------------- |
| [`01-concepts/01-layered-architecture-overview.md`](./01-concepts/01-layered-architecture-overview.md) | 9.1–9.12 | The ten layers, their place in the flow, and an ASCII layer diagram |
| [`01-concepts/02-responsibilities-per-layer.md`](./01-concepts/02-responsibilities-per-layer.md) | 9.13 | A table giving each layer one error-handling job |
| [`01-concepts/03-where-to-handle-translate-and-propagate.md`](./01-concepts/03-where-to-handle-translate-and-propagate.md) | 9.16–9.18 | The handle / translate / propagate decision |
| [`01-concepts/04-preventing-leakage-across-layers.md`](./01-concepts/04-preventing-leakage-across-layers.md) | 9.14–9.15 | Stopping infra detail entering the domain and domain meaning vanishing in wrappers |
| [`01-concepts/05-avoiding-duplicate-handling-and-consistent-flow.md`](./01-concepts/05-avoiding-duplicate-handling-and-consistent-flow.md) | 9.19–9.20 | Handle-once rule and end-to-end consistency |
| [`02-deep-dive/01-layer-contracts-and-translation-points.md`](./02-deep-dive/01-layer-contracts-and-translation-points.md) | 9.3–9.8, 9.13 | What each layer is *allowed* to throw and where translation must occur |
| [`02-deep-dive/02-async-layers-workers-and-scheduled-tasks.md`](./02-deep-dive/02-async-layers-workers-and-scheduled-tasks.md) | 9.9–9.11, 9.12 | Background workers, scheduled tasks, bootstrap, and process boundaries |
| [`03-practical-examples/01-checkout-request-through-every-layer.md`](./03-practical-examples/01-checkout-request-through-every-layer.md) | all | A request flowing through every layer, showing where errors translate |
| [`03-practical-examples/02-exportjob-through-worker-layers.md`](./03-practical-examples/02-exportjob-through-worker-layers.md) | 9.6–9.10 | A background job through worker/domain/repo/infra layers |
| [`04-dos-and-donts/README.md`](./04-dos-and-donts/README.md) | all | Layer rules and anti-patterns |
| [`05-reference/README.md`](./05-reference/README.md) | all | Layer responsibility matrix, translation cheat sheet |

## Learning objectives

By the end you can:

- Name every layer in your request path and the failure class each one owns.
- State, for any error, the exact layer that handles it, the layer that translates it, and the
  layers that must propagate it untouched.
- Detect infrastructure leakage into the domain and domain-meaning loss in wrappers.
- Articulate a single end-to-end flow for one request and one job.

## Key takeaways

1. **Every failure has one owning layer.** Handle-once is the defining invariant of this chapter.
2. **Translate at boundaries, not everywhere.** Translation is a layer-crossing concern.
3. **Infrastructure errors must not reach the domain** as driver/SQL/vendor types.
4. **Domain meaning must survive every wrapper** — an adapter that says "db error" has failed.
5. **Workers and scheduled tasks are layers too** and need the same discipline as HTTP handlers.
6. **Consistency is observable**: the same category of failure produces the same external shape
   regardless of which entry point hit it.

## Exercises

1. Draw your own request path as layers and label where each of `unique_violation`, a domain
   `InsufficientFunds`, and a Stripe `429` is translated and handled.
2. Find one place in your codebase where an infrastructure error reaches a user-facing message.
3. Write the handle-once table for your top ten errors: origin layer, owning layer, external shape.
4. Trace a background job from worker wrapper to S3 upload and mark every boundary.

## Related

- [Chapter 10 — Centralized and Distributed Error Handling](../10-centralized-and-distributed-error-handling/README.md)
- [Chapter 11 — The Error Lifecycle](../11-the-error-lifecycle/README.md)
- [Part VI — Error Boundaries and Translation](../../part-06-boundaries-and-translation/README.md)
- [Part IV Index](../README.md)
