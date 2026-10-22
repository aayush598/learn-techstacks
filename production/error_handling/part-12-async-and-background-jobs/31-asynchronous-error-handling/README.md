# Chapter 31 — Asynchronous Error Handling

> Part XII · _Estimated reading time: 50–70 min_
> **Prerequisite:** [Chapter 12 — Exception Propagation and Control Flow](../../part-05-exception-mechanics/12-exception-propagation-and-control-flow/README.md)

## One-sentence summary

Async code **breaks the call-stack contract** that sync error handling relies on, so you must make
every failure path explicit: attach handlers, aggregate concurrent failures deliberately, propagate
cancellation and deadlines, and never let a promise reject into the void.

## Why this chapter matters

In synchronous code, an uncaught exception unwinds to a boundary you can see. In asynchronous code,
a rejected promise with no handler is a **detached failure**: the caller has already moved on, the
request may have returned `200`, and the only signal is a process-level event — or nothing at all.
Production incidents caused by async failures usually look like "the data silently stopped
updating," not like a stack trace. This chapter gives you the patterns that make those failures
visible and owned.

## Chapter map

The chapter has 16 sections grouped into twelve files:

| File | Subsections covered | What you learn |
| ---- | ------------------- | -------------- |
| [`01-concepts/01-sync-vs-async-error-semantics.md`](./01-concepts/01-sync-vs-async-error-semantics.md) | 31.1–31.3 | Why async errors detach; unhandled rejections; propagation across boundaries |
| [`01-concepts/02-concurrent-failures-and-aggregation.md`](./01-concepts/02-concurrent-failures-and-aggregation.md) | 31.4–31.7 | Concurrent failures, aggregation, fail-fast vs collect-all, partial success |
| [`01-concepts/03-cancellation-timeouts-and-events.md`](./01-concepts/03-cancellation-timeouts-and-events.md) | 31.8–31.10 | Cancellation, deadline propagation, event-driven error flow |
| [`01-concepts/04-callbacks-streams-and-reactive-pipelines.md`](./01-concepts/04-callbacks-streams-and-reactive-pipelines.md) | 31.11–31.13 | Error-first callbacks, stream errors, reactive terminal signals |
| [`01-concepts/05-async-cleanup-and-detached-failures.md`](./01-concepts/05-async-cleanup-and-detached-failures.md) | 31.14–31.16 | Async cleanup, preventing detached failures, conventions |
| [`02-deep-dive/01-promise-all-vs-allsettled.md`](./02-deep-dive/01-promise-all-vs-allsettled.md) | 31.5–31.7 (mechanics) | Execution order, rejection timing, `AggregateError`, memory effects |
| [`02-deep-dive/02-cancellation-and-timeout-propagation.md`](./02-deep-dive/02-cancellation-and-timeout-propagation.md) | 31.8–31.9 (mechanics) | `AbortSignal`, deadline budgets, cleanup on abort |
| [`02-deep-dive/03-detached-failures-and-async-context.md`](./02-deep-dive/03-detached-failures-and-async-context.md) | 31.2, 31.15 (mechanics) | Detecting orphaned promises, async context, process handlers |
| [`03-practical-examples/01-partial-success-aggregation.md`](./03-practical-examples/01-partial-success-aggregation.md) | 31.5–31.7 + 31.10 | Acme dashboard aggregation with per-source failure reporting |
| [`03-practical-examples/02-cancellation-in-agentrun.md`](./03-practical-examples/02-cancellation-in-agentrun.md) | 31.8–31.9, 31.14 | Cancelling parallel LLM tool calls and cleaning up |
| [`04-dos-and-donts/README.md`](./04-dos-and-donts/README.md) | all | Rules and anti-patterns |
| [`05-reference/README.md`](./05-reference/README.md) | all | Decision tables, API cheatsheet, chapter glossary |

## Learning objectives

By the end you can:

- Explain why `throw` inside a `.then()` does not throw at the call site.
- Choose `all`, `allSettled`, `any`, or a bounded pool for a given product requirement.
- Return a **partial-success result** instead of losing successful work when one branch fails.
- Propagate an `AbortSignal`/`context.Context` through every downstream call.
- Guarantee cleanup on success, failure, and cancellation.
- Detect and eliminate detached promises in code review.

## Key takeaways

1. **A promise is a value; a rejection is not an exception at the call site.** Someone must attach a
   handler or the failure is unowned.
2. **Fail-fast and collect-all are product decisions.** Use `Promise.all` only when all results are
   required; use `allSettled` when partial results are useful.
3. **Cancellation is not an error by default.** Distinguish `AbortError` / `CancelledError` from a
   genuine failure so you do not retry cancelled work.
4. **Timeouts must propagate as deadlines**, not just as a race that leaves the underlying call
   running.
5. **Cleanup is not optional in async code.** `finally` runs on rejection too, but not on a
   fire-and-forget promise you abandoned.

## Exercises

1. Find a `.then()` chain with no `.catch()` in your codebase and add an owner and a terminal log.
2. Replace a `Promise.all` fan-out with `allSettled` and return a partial-success result; write the
   API contract for the failure list.
3. Add an `AbortController` to a multi-call async operation and assert cleanup runs on abort.
4. Write your team's rule for when a promise may be intentionally detached (`void`, `spawn`) and
   what handler it must still have.

## Related

- [Chapter 32 — Background Jobs, Queues, and Scheduled Tasks](../32-background-jobs-queues-and-scheduled-tasks/README.md)
- [Chapter 12 — Exception Propagation and Control Flow](../../part-05-exception-mechanics/12-exception-propagation-and-control-flow/README.md)
- [Chapter 29 — Timeouts, Circuit Breakers, and Bulkheads](../../part-11-retry-and-resilience/29-timeouts-circuit-breakers-and-bulkheads/README.md)
- [Glossary](../../GLOSSARY.md)
