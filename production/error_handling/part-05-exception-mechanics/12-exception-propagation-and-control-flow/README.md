# Chapter 12 — Exception Propagation and Control Flow

> Part V · _Estimated reading time: 60–80 min_
> **Prerequisite:** [Part IV — The Error Lifecycle](../../part-04-architecture/11-the-error-lifecycle/README.md)

## One-sentence summary

An exception **unwinds the control flow** from the point of detection outward until something
catches it — and the *shape of that path* (synchronous, asynchronous, concurrent, or across a
service boundary) determines what the caller can still learn about the original failure.

## Why this chapter matters

The same error can be loud, silent, or misleading depending entirely on how it propagates. A
database timeout caught at the repository and rethrown as a generic `Error` loses the retry
metadata. A promise rejection that nobody `await`s disappears. A panic in a detached goroutine
takes down the process. Propagation is where production systems silently convert *recoverable*
failures into *invisible* ones.

## Chapter map

The chapter has 20 sections, grouped into 11 files:

| File | Subsections covered | What you learn |
| ---- | ------------------- | -------------- |
| [`01-concepts/01-propagation-through-call-stacks.md`](./01-concepts/01-propagation-through-call-stacks.md) | 12.1, 12.4, 12.10, 12.11 | How the stack unwinds; nested calls; boundaries; choosing the catch level |
| [`01-concepts/02-sync-async-and-callback-propagation.md`](./01-concepts/02-sync-async-and-callback-propagation.md) | 12.2, 12.3, 12.6, 12.7, 12.8 | Sync vs async, callbacks, event handlers, promise chains |
| [`01-concepts/03-concurrent-and-cross-service-propagation.md`](./01-concepts/03-concurrent-and-cross-service-propagation.md) | 12.5, 12.9 | Failures across service boundaries and concurrent operations |
| [`01-concepts/04-rethrow-wrap-and-preserve-cause.md`](./01-concepts/04-rethrow-wrap-and-preserve-cause.md) | 12.12, 12.13, 12.14, 12.15, 12.18 | Rethrowing, wrapping with context, preserving stack/cause, avoiding masking |
| [`01-concepts/05-unreachable-handlers-and-conventions.md`](./01-concepts/05-unreachable-handlers-and-conventions.md) | 12.16, 12.17, 12.19, 12.20 | Unreachable handlers, failure→success conversion, handling cost, conventions |
| [`02-deep-dive/01-stack-traces-and-cause-chains.md`](./02-deep-dive/01-stack-traces-and-cause-chains.md) | mechanics | How stacks and causes are captured; before/after views |
| [`02-deep-dive/02-async-propagation-and-unhandled-rejections.md`](./02-deep-dive/02-async-propagation-and-unhandled-rejections.md) | mechanics | Async context loss, unhandled rejections, detached work |
| [`03-practical-examples/01-propagation-across-languages.md`](./03-practical-examples/01-propagation-across-languages.md) | 12.1–12.9 | ts, python, go, java propagation in one scenario |
| [`03-practical-examples/02-preserving-cause-before-after.md`](./03-practical-examples/02-preserving-cause-before-after.md) | 12.12–12.18 | Before/after stack views; wrapping without masking |
| [`04-dos-and-donts/README.md`](./04-dos-and-donts/README.md) | all | Rules of thumb and anti-patterns |
| [`05-reference/README.md`](./05-reference/README.md) | all | Cheat sheet, propagation decision table, chapter glossary |

## Learning objectives

By the end you can:

- Trace an error's path through sync calls, promise chains, callbacks, and concurrent work.
- Identify the single correct level to catch a given error.
- Wrap an error with context while preserving its **original cause and stack**.
- Spot unreachable handlers, masked causes, and failure→success conversions in review.

## Key takeaways

1. **Propagation is the default action.** Catch only where the fallback differs from propagating
   (12.10–12.11).
2. **Context is additive, the cause is immutable.** Wrap to add breadcrumbs; never replace the
   original error or its stack (12.13–12.15).
3. **Async breaks the stack.** Each `await`, callback, or event hop is a new stack; carry the cause
   explicitly or lose it (12.3, 12.6–12.9).
4. **A dropped failure is worse than a loud one.** Unawaited promises and detached goroutines hide
   failures (12.7, 12.9).
5. **Never turn a failure into a success.** Silent conversion corrupts state and violates the
   caller's contract (12.17).

## Exercises

1. Pick one request in your system and draw its propagation path; mark every boundary and catch.
2. Find a `catch` that rethrows a *new* generic error; show what metadata the caller lost.
3. Find an unawaited promise or fire-and-forget callback; describe what happens when it rejects.

## Related

- [Chapter 13 — Catch Blocks and Recovery Logic](../13-catch-blocks-and-recovery-logic/README.md)
- [Chapter 14 — Resource Cleanup and Failure-Safe Execution](../14-resource-cleanup-and-failure-safe-execution/README.md)
- [Part VI — Error Boundaries and Translation](../../part-06-boundaries-and-translation/README.md)
- [Glossary: exception, cause, boundary](../../GLOSSARY.md)
