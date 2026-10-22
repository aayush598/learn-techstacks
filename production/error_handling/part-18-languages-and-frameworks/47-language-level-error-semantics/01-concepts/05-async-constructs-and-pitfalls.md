# Async Constructs and Common Pitfalls

> Part XVIII · Chapter 47 · Sections 47.12–47.13 · _Estimated reading time: 20 min_
> **Prerequisite:** [Language Comparison at a Glance](./02-language-comparison-at-a-glance.md)

## In one sentence

Async is where language idioms diverge hardest: the same product questions — **fail fast or
collect all, cancel or time out, detach or await** — get different primitives in every language,
and each primitive has a signature production bug when used by muscle memory from another one.

## Why this matters in production

AgentRun fans out tool calls; ExportJob retries with deadlines; Checkout races a gateway timeout
against a cancellation. In sync code, a mistake is a stack trace at the call site. In async
code, a mistake is usually a **detached failure**: a rejection nobody observes, a cancellation
misclassified as a 500, a sibling task cancelled mid-write. The language determines which of
these mistakes the compiler can even see — usually none, which is why the rules must be
explicit.

## 47.12 — The async error constructs

| Language | Unit of work | Failure aggregation | Cancellation | Terminal handler | Detached-failure detector |
| -------- | ------------ | ------------------- | ------------ | ---------------- | ------------------------- |
| JS/TS | Promise / `async` fn | `Promise.all` (fail-fast), `allSettled` (collect), `any` + `AggregateError` | `AbortController`/`AbortSignal` | nearest `catch` / rejection handler | `process.on("unhandledRejection")`, lint `no-floating-promises` |
| Node.js | same + streams | same | `AbortSignal.timeout(ms)` | process-level (fatal default) | `unhandledRejection` |
| Python | `asyncio` Task | `gather(return_exceptions=True)`, `TaskGroup` (3.11, raises `ExceptionGroup`) | `task.cancel()`, `asyncio.timeout` | task's coroutine / `TaskGroup` | "Task exception was never retrieved" GC warning |
| Go | goroutine | `errgroup.WithContext` (first error + cancel), `sync.WaitGroup` (manual collect) | `context.WithCancel/Timeout` | every goroutine must return errors to a channel/errgroup | goroutine leak counters, pprof |
| Java | `CompletableFuture` | `allOf` (completes exceptionally on first), `anyOf` | `Future.cancel(true)`, interruption | `exceptionally`/`whenComplete` | unjoined futures (silent) |
| Kotlin | coroutine | `coroutineScope` (fail-fast, cancels siblings), `supervisorScope` (independent), `async`+`await` | `Job.cancel`, `withTimeout` | `CoroutineExceptionHandler` at scope root | structured concurrency (no detached children) |
| C# | `Task`/`async` | `Task.WhenAll` (collect; inspect each), `WhenAny` | `CancellationToken` | await inside `try` | `TaskScheduler.UnobservedTaskException` (GC-time, legacy) |
| Swift | `async` fn / `Task` | `withThrowingTaskGroup` | `Task.checkCancellation()`, `withTaskCancellationHandler` | `do/catch` at `await` | (structured; little detachment) |

### The canonical questions, answered per language

**Q: run three tool calls in parallel — what if one fails?**

```ts
// JS/TS — fail fast (siblings keep running unless you abort them!)
const results = await Promise.all(toolCalls.map(run));          // first rejection wins
// JS/TS — collect all
const settled = await Promise.allSettled(toolCalls.map(run));   // every outcome
```

```python
# Python 3.11+ — fail-fast with automatic sibling cancellation
async with asyncio.TaskGroup() as tg:
    tasks = [tg.create_task(run(t)) for t in tool_calls]        # first failure cancels others
# Python — collect all
results = await asyncio.gather(*calls, return_exceptions=True)  # failures in results
```

```go
// Go — first error cancels the group's context
g, ctx := errgroup.WithContext(ctx)
for _, call := range calls {
    g.Go(func() error { return run(ctx, call) })
}
if err := g.Wait(); err != nil { return fmt.Errorf("agent tools: %w", err) }
```

```kotlin
// Kotlin — fail-fast scope cancels siblings
coroutineScope { calls.map { async { run(it) } }.awaitAll() }
// Kotlin — independent children
supervisorScope { calls.forEach { launch { run(it) } } }  // failures hit the handler
```

**Q: how do I time out?** JS: `AbortSignal.timeout()` passed into the call (never
`Promise.race` alone — the loser keeps running and may still charge). Python:
`asyncio.timeout(ms)`. Go: `context.WithTimeout` + `defer cancel()`. Kotlin: `withTimeout(ms)`
(throws `TimeoutCancellationException`). Java: `orTimeout` on `CompletableFuture` (Java 9+).
C#: `CancellationTokenSource(TimeSpan)`. Swift: `withThrowingTaskGroup` + race, or task
cancellation.

**Q: is cancellation a failure?** Almost never retry it: JS `AbortError` (`ABORT_ERR`), Python
`CancelledError` (a `BaseException`), Go `context.Canceled`, Kotlin `CancellationException`,
Swift `CancellationError`, C# `OperationCanceledException`. Map them to *cancelled*, not 500 —
see the [terminal-state vocabulary](../../../part-12-async-and-background-jobs/31-asynchronous-error-handling/05-reference/README.md).

## 47.13 — The pitfall catalog (by language)

### JavaScript / TypeScript / Node.js

| Pitfall | Symptom | Fix |
| ------- | ------- | --- |
| Floating promise | `unhandledRejection`; work vanishes after 200 | `no-floating-promises`; `await`/`return`/owned `spawn` |
| `forEach(async …)` | Handler returns before work finishes | `for…of` + `await`, or `Promise.all` |
| `Promise.race` as timeout | Loser still executes (duplicate charge!) | `AbortSignal.timeout` into the request |
| `instanceof` error check fails | Cross-bundle/realm class mismatch | Match `code`/`name` |
| Unhandled `'error'` event | Process crash on first emitter failure | Attach listener at creation |

### Python

| Pitfall | Symptom | Fix |
| ------- | ------- | ----- |
| Bare `except:` around `await` | Cancellation becomes a logged 500; task never dies | `except Exception:` + re-raise `CancelledError`… better: catch specific types |
| `gather(...)` without `return_exceptions` | First failure hides others' outcomes | Decide fail-fast vs collect per operation |
| Fire-and-forget `create_task` | Task GC'd mid-flight; "exception never retrieved" | Hold references; use `TaskGroup` |
| `except asyncio.TimeoutError` too broad | Swallows unrelated timeouts | Scope timeouts to the operation with `asyncio.timeout` |

### Go

| Pitfall | Symptom | Fix |
| ------- | ------- | ----- |
| Goroutine leaks `err` | Error observed by no one | Send to channel / errgroup only |
| `panic` in a goroutine | Whole process dies (recover must be in the same goroutine) | Return errors; recover only at owned boundaries |
| Forgotten `defer cancel()` | Context leak; downstream hangs | Lint rule after every `WithTimeout` |
| `WaitGroup` without error collection | "Done" with failures unreported | Prefer `errgroup` |

### Java

| Pitfall | Symptom | Fix |
| ------- | ------- | ----- |
| Unjoined `CompletableFuture` | Silent failure at GC | Store and join/await; `whenComplete` logs |
| Wrapping in `CompletionException` | Classifier sees the wrapper, not the cause | `throw ex.getCause()`-style unwrap before mapping |
| `Future.get()` without timeout | Worker hang → request hang | Always pass timeout; use `orTimeout` |
| Swallowing `InterruptedException` | Cancellation ignored; shutdown stalls | Restore interrupt flag: `Thread.currentThread().interrupt()` |

### Kotlin

| Pitfall | Symptom | Fix |
| ------- | ------- | ----- |
| `runCatching` in coroutines | Cancellation swallowed; scope never ends | Rethrow `CancellationException` |
| `GlobalScope.launch` | Detached, unmanaged failures | Inject a scope; structured concurrency |
| `async` without `await` | Failure invisible until scope cancels mysteriously | `await()` or treat as deliberate fan-out |
| Blocking calls in coroutines | Thread starvation of the dispatcher | `withContext(Dispatchers.IO)` |

### C#

| Pitfall | Symptom | Fix |
| ------- | ------- | ----- |
| `async void` | Exceptions bypass pipeline; process crash | `async Task` everywhere but event handlers |
| Swallowing `OperationCanceledException` | Client disconnects logged as 500 | `when (ct.IsCancellationRequested)` branch |
| Ignoring `AggregateException.InnerExceptions` | Only first failure classified | `Flatten()` / iterate |
| Not passing `CancellationToken` | Abandoned work continues after response | Thread the token through every call |

### Swift

| Pitfall | Symptom | Fix |
| ------- | ------- | ----- |
| `try!` on external input | Trap → crash | `do/catch` or `try?` with explicit nil handling |
| Ignoring `Task.checkCancellation()` | Long export ignores user cancel | Check in loops; use cancellation handlers |
| Swallowing all errors with `try?` | Decline and outage both become `nil` | Typed `catch`; keep `Result` when composing |

## The universal rules (language-independent)

1. **Every async unit of work has an owner and a terminal outcome.** No `void`/fire-and-forget
   without a handler and a queue behind it for anything that must happen.
2. **Fail-fast vs collect-all is a product decision**, written per operation — not a habit.
3. **Cancellation is not failure.** Classify it separately; never retry it.
4. **Timeouts must abort the underlying work** (`AbortSignal`, `context`, `CancellationToken`),
   not just the waiter.
5. **Cleanup must run on all three exits** — success, failure, cancellation — with a *fresh*
   short deadline, not the already-aborted one.

## Key data / numbers

- Node's default `--unhandled-rejections=throw` has been the default since **Node 15**; before
  that, warnings — old runbooks lie.
- Python `asyncio.gather(return_exceptions=True)` returns exceptions *in the results list* —
  check types, don't assume values.
- Go's `errgroup.WithContext` cancels the group context **on the first error**; siblings
  observe cancellation only if they select on `ctx.Done()`.
- Kotlin structured concurrency: children of a failed `coroutineScope` are cancelled before the
  exception propagates — side effects need idempotency (Chapter 28).
- Java `CompletableFuture.exceptionally` receives a `CompletionException` wrapper — unwrap
  before classifying.
- `AggregateError` (JS) carries `.errors[]`; message alone is `"All promises were rejected"` —
  useless for classification.

## Real-world use case — AgentRun

Acme's `AgentRun` in TypeScript used `Promise.all` over six tool calls (fetch, SQL, LLM). One
tool timed out; `Promise.all` rejected, the API returned 500, but the five sibling calls kept
running — two wrote rows to the agent trace table *after* the client had been told to retry, so
the retried run duplicated them. The fix per the universal rules: `AbortController` per run
(aborts siblings on first terminal failure), `allSettled` for the optional tools, and
cancellation mapped to a `cancelled` job state, never 500. Duplicate-trace incidents stopped.

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| Fail-fast + abort siblings | Fast; no wasted work | Partial side effects need cleanup | Required-results operations |
| Collect-all (`allSettled`/`gather(return_exceptions=)`) | Full picture; partial success | Slower; more code to classify | Dashboard fan-out, bulk ops |
| Structured concurrency (Kotlin/Swift/TaskGroup) | No detached failures | Sibling cancellation semantics to learn | Default in those languages |
| Detached tasks with handlers | Unblocks caller | Needs durable ownership | Notifications, metrics, non-critical writes |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Choose aggregation mode per operation, in writing | Copy `Promise.all`/`gather` everywhere by habit |
| Thread cancellation into every I/O call | Accept a token/signal and drop it on the floor |
| Unwrap async wrappers before classifying | Classify `CompletionException`/`AggregateException` directly |
| Rethrow cancellation signals | Retry aborted work |
| Give cleanup its own short deadline | Reuse the aborted context/signal for cleanup |

## Common mistakes

- **Retrying after abort** — the client navigated away; your retry charges a card anyway.
- **`allSettled` then `res.json(results)`** — serializes raw rejection reasons (leaks internals);
  map each to a code first.
- **Python `except Exception` in a task** — logs and holds the task in a weird state;
  prefer `TaskGroup` and let it aggregate.
- **Go `ctx` without `defer cancel()`** — connection-pool pressure that looks like a leak.
- **Kotlin fire-and-forget `launch` in a request scope** — request ends, scope dies, work
  cancelled mid-write; use a supervised app scope or a queue.

## Checklist

- [ ] Does every fan-out have a written fail-fast/collect-all decision?
- [ ] Does every timeout abort the underlying work, not just the waiter?
- [ ] Are cancellation errors excluded from retry classification in every language?
- [ ] Are floating promises, bare excepts, `async void`, and `GlobalScope` banned by lint/CI?
- [ ] Does cleanup run on success, failure, and cancellation with a fresh deadline?

## Related

- [Same Error, Five Languages](../03-practical-examples/01-same-error-across-languages.md)
- [Checkout in Five More Languages](../03-practical-examples/01-same-error-across-languages.md)
- [Chapter 31 — Asynchronous Error Handling](../../../part-12-async-and-background-jobs/31-asynchronous-error-handling/README.md)
- [Chapter 12 — Exception Propagation Across Async Boundaries](../../../part-05-exception-mechanics/12-exception-propagation-and-control-flow/README.md)
