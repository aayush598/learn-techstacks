# Chapter 11 — The Error Lifecycle

> Part IV · _Estimated reading time: 65–90 min_
> **Prerequisite:** [Chapter 9 — Layered Architecture](../09-layered-error-handling-architecture/README.md)
> and [Chapter 10 — Centralized Handling](../10-centralized-and-distributed-error-handling/README.md)

## One-sentence summary

Every error — from a validation miss to a crashed worker — travels the **same ordered lifecycle**:
originate → detect → represent → classify → enrich → preserve cause → propagate → translate →
decide → apply recovery → render → finalize → clean up, and a production standard is nothing more
than making every stage **explicit and total**.

## Why this chapter matters

Chapter 9 tells you *where* errors may live; Chapter 10 tells you *who acts*; this chapter tells
you *in what order, with what artifacts, until when*. Without a lifecycle model:

- Errors lose their cause at stage 6 and become untriageable at stage 11.
- Recovery is applied twice (stage 9 in the service, stage 10 in the worker) with multiplied
  side effects.
- Failed operations are never *finalized* — a checkout stuck `pending` forever, a job that
  exhausted retries but was never marked failed.
- Cleanup is skipped on the failure path, leaking connections and locks.
- And the scariest class: **failures during error handling** (11.15), which corrupt the very
  mechanism meant to contain them.

This chapter is the dynamic view: one error, start to terminal state, every time.

## Chapter map

The chapter has 17 sections, grouped into eleven files:

| File | Subsections covered | What you learn |
| ---- | ------------------- | -------------- |
| [`01-concepts/01-lifecycle-overview.md`](./01-concepts/01-lifecycle-overview.md) | 11.1–11.4 | Origins, detection, representation, classification — with the ASCII lifecycle diagram |
| [`01-concepts/02-enriching-and-preserving-cause.md`](./01-concepts/02-enriching-and-preserving-cause.md) | 11.5, 11.6 | Safe context enrichment and the unbroken cause chain |
| [`01-concepts/03-propagation-translation-and-recovery.md`](./01-concepts/03-propagation-translation-and-recovery.md) | 11.7–11.10 | Moving up layers, translating at boundaries, deciding and applying recovery |
| [`01-concepts/04-response-finalize-and-cleanup.md`](./01-concepts/04-response-finalize-and-cleanup.md) | 11.11–11.13 | Rendering external responses, finalizing failed operations, cleanup after failure |
| [`01-concepts/05-terminal-state-and-standard-lifecycle.md`](./01-concepts/05-terminal-state-and-standard-lifecycle.md) | 11.14–11.17 | Double-handling prevention, handler failures, terminal state, the project-wide template |
| [`02-deep-dive/01-double-handling-and-error-during-handling.md`](./02-deep-dive/01-double-handling-and-error-during-handling.md) | 11.14, 11.15 | Detecting duplicate handling; what to do when the handler itself throws |
| [`02-deep-dive/02-finalization-cleanup-and-terminal-states.md`](./02-deep-dive/02-finalization-cleanup-and-terminal-states.md) | 11.12, 11.13, 11.16 | Ambiguous outcomes, terminal vs recoverable states, cleanup on the failure path |
| [`03-practical-examples/01-webhookingest-lifecycle-walkthrough.md`](./03-practical-examples/01-webhookingest-lifecycle-walkthrough.md) | all (11.1–11.17) | One failing Stripe webhook traced through every stage |
| [`03-practical-examples/02-exportjob-retry-compensation-terminal.md`](./03-practical-examples/02-exportjob-retry-compensation-terminal.md) | 11.9–11.16 | `ExportJob` deciding, retrying, compensating, and terminating |
| [`04-dos-and-donts/README.md`](./04-dos-and-donts/README.md) | all | Lifecycle rules and anti-patterns |
| [`05-reference/README.md`](./05-reference/README.md) | all | Stage table, decision trees, per-project template |

## Learning objectives

By the end you can:

- Trace any failure from origin to terminal state and name the **owner and artifact** of every
  stage.
- Keep the original cause intact through translations (11.6) and enrich errors only with **safe**
  context (11.5).
- Decide recovery once (11.9), apply retries/compensation once (11.10), and detect double
  handling (11.14).
- Finalize failed operations, run cleanup on the failure path, and choose terminal vs recoverable
  states — including when the error handler itself fails (11.15).

## Key takeaways

1. **The lifecycle is universal** — HTTP requests, jobs, webhooks, CLIs, and scheduled runs share
   it; only the actors and renderers differ (11.17).
2. **Cause preservation is not optional politeness** — a chain broken at translation makes every
   later stage (triage, retry classification, DLQ replay) guesswork (11.6).
3. **Recovery is decided once and applied by one owner**; retries and compensation are stage-10
   actions with explicit attempt budgets (11.9–11.10).
4. **Every failed operation must reach a terminal state** — `failed`, `compensated`, or
   `succeeded_after_retry`; `pending forever` is a defect, not a state (11.16).
5. **The handler is code**: it can throw, hang, and double-write; guard it like any other
   boundary (11.15, and Ch. 10's ordering rules).

## Exercises

1. Pick your most important endpoint and write its last ten lifecycle stages with owners and
   artifacts.
2. Take a real incident's error object and walk it backward: which stage dropped the cause?
3. List every place in one module that could produce a second response or second side effect for
   the same failure (double-handling audit).
4. Define the terminal states for one job type and prove `pending` cannot persist past its
   deadline.

## Related

- [Chapter 9 — Layered Error-Handling Architecture](../09-layered-error-handling-architecture/README.md)
- [Chapter 10 — Centralized and Distributed Error Handling](../10-centralized-and-distributed-error-handling/README.md)
- [Chapter 12 — Exception Propagation and Control Flow](../../part-05-exception-mechanics/12-exception-propagation-and-control-flow/README.md)
- [Part IV Index](../README.md)
