# Async Propagation and Unhandled Rejections

> Part V · Chapter 12 · Sections 12.3, 12.9 (mechanics) · _Estimated reading time: 19 min_
> **Prerequisite:** [Sync, Async, and Callback Propagation](../01-concepts/02-sync-async-and-callback-propagation.md)

## In one sentence

Every async hop **detaches the error from its original stack**, so propagation must be
*re-established explicitly* at each `await`, callback, or goroutine — otherwise the failure
becomes an **unhandled rejection** or a **crashed process**.

## Why this matters in production

Asynchronous failures are the most common "invisible" errors in production. A rejected promise
with no observer is logged by the runtime at best, ignored at worst. A goroutine panicking in
isolation kills the whole server. A Python task that raises internally surfaces nowhere until
you attach a callback. Understanding the mechanics lets you place *observers* deliberately.

## Core concept

The async runtime decouples *where work starts* from *where it fails*. Three structures matter:

1. **Promise / Future / Task** — a value that will settle later; a rejection is stored, not thrown.
2. **Continuation** — the code after an `await`; runs on a fresh stack.
3. **Observer** — whoever attaches `.then`/`.catch`, `await`, `add_done_callback`, or channel
   receive. **No observer = no propagation.**

```text
producer            runtime                     consumer
─────────           ───────                     ────────
async fn ─────────▶ pending Promise ─────────▶ await / .catch / gather
   (runs)             │  holds result/reason       │ observes
   throws ──────────▶ rejected state ────────▶ if no observer: UNHANDLED
```

## How it works (mechanics)

### Microtask resumption

`await p` suspends the function; when `p` settles, the continuation is scheduled as a microtask.
The stack captured at throw time ends at the `await`; the continuation begins a new stack. That
is why async stack traces are short unless the runtime implements **async stack traces** (Node
with `--async-stack-traces`, V8's zero-cost async stack traces).

### Unhandled rejection lifecycle (Node.js)

1. A promise is rejected.
2. At the end of a microtask checkpoint, the runtime checks for a rejection handler.
3. None → `unhandledRejection` event fires; since Node 15 the default is to **throw**, which
   becomes `uncaughtException` and **exits the process**.

You can observe-but-not-crash:

```ts
process.on("unhandledRejection", (reason) => {
  log.error({ reason }, "unhandled rejection"); // log, then decide
  // Do NOT silently ignore; ideally crash after flushing (fail-fast on unknown state).
});
```

### Cancellation and detached work

Goroutines and fire-and-forget promises are **detached**: the parent does not wait, so it cannot
observe. The rule: if the parent cares about the outcome, it must *join* (await, `WaitGroup`,
channel) or *observe* (callback). If it truly does not care, the task must still have an internal
observer so failures are logged (best-effort side effects).

### Aggregation

Parallel work needs an accumulator. Three mechanisms:

| Mechanism | Behavior on failure |
| --------- | ------------------- |
| `Promise.all` / `errgroup.Wait` | Reject/return first failure; siblings may keep running |
| `Promise.allSettled` / `errors.Join` | Gather all outcomes; no short-circuit |
| `Promise.race` | First settle wins; losers unobserved |

## Worked example — one script, four leaks and their fixes

```ts
// ❌ leak 1: fire-and-forget
startBackgroundSync();

// ❌ leak 2: async callback ignored by forEach
ids.forEach(async (id) => { await sync(id); });

// ❌ leak 3: Promise.all discards siblings on first reject
await Promise.all(ids.map(sync));

// ❌ leak 4: catch on the wrong link
doA().then(doB).catch(log); // does not catch doB's throw if written as a fresh chain

// ✅ fixes
void startBackgroundSync().catch(observeOnly);      // explicit best-effort observer

for (const id of ids) {                              // sequential, ordered
  await sync(id);
}
const results = await Promise.allSettled(ids.map(sync)); // collect-all
const failures = results.filter(r => r.status === "rejected");

doA().then(doB).catch(log);                          // already correct: catch is terminal
```

Go equivalent — never detach without a recover or a joined error:

```go
// ❌ detached panic = process death
go func() { doWork() }()

// ✅ isolated with recovery, reported through a channel
errCh := make(chan error, 1)
go func() {
    defer func() {
        if r := recover(); r != nil {
            errCh <- fmt.Errorf("worker panicked: %v", r)
        }
    }()
    errCh <- doWork()
}()
```

## Key data / numbers

- **Node ≥ 15**: unhandled rejection = process exit; `--unhandled-rejections=warn|none|strict`.
- **Node `--async-stack-traces`**: on by default since v12; links async frames.
- **Go**: a panic in any goroutine, unrecovered, terminates the process with a stack dump.
- **Python `asyncio`**: tasks not awaited produce *"Task was destroyed but it is pending"*;
  exceptions unretrieved from a `Task` log *"Task exception was never retrieved"*.
- **Java `CompletableFuture`**: `exceptionally`, `handle`, `whenComplete` are the observers;
  missing them drops the throwable into the future.
- **`Promise.allSettled`** never rejects — you must inspect `status`.

## Real-world use case — Acme SaaS

Acme's `WebhookIngest` acknowledged Stripe webhooks immediately and processed them in a detached
promise so the response would be fast. When the database was briefly unavailable, those promises
rejected; because nobody observed them, the events were **silently dropped** and billing state
drifted. The fix was structural: put processing on a durable queue (Chapter 32) and, for the
remaining best-effort async work, attach an explicit `.catch` that reports to the metrics
pipeline. The lesson: **"fast ack + background" is fine only if the background work is durable or
observed.**

## Trade-offs

| Pattern | Pros | Cons | When |
| ------- | ---- | ---- | ---- |
| `await` sequentially | Simple, ordered, observed | Slow; head-of-line blocking | Small N; ordering required |
| `Promise.all` | Fast; fail-fast | Discards siblings; partial state | Atomic fan-out |
| `allSettled` + inspect | Accurate outcomes | More code | Batch/export/jobs |
| Detached + queue | Fast ack; durable | Needs infrastructure | Webhooks, notifications |
| Detached fire-and-forget | Trivial | Silent loss; process crash risk | Only truly ignorable work |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Attach an observer to every promise/task | Leave a rejection unhandled |
| Recover or join detached goroutines | `go func(){...}()` with no recover/join |
| Use `allSettled` when outcomes matter | Assume `Promise.all` reports all failures |
| Make background work durable or observed | Ack then forget non-idempotent work |
| Configure `unhandledRejection` deliberately | Ignore the event and hope |

## Common mistakes

- **`async` in `Array.forEach`** — the loop does not await the returned promises.
- **`process.on('unhandledRejection', () => {})`** — an empty observer that merely hides failures.
- **Unbounded fire-and-forget** — an outage silently loses thousands of operations.
- **Assuming a short async stack** points to the true origin.
- **Not cancelling siblings** after `Promise.all` rejects — orphaned work mutates state.

## Checklist

- [ ] Every promise/task has an observer (await, catch, callback, or join).
- [ ] Detached goroutines have `recover` or are joined.
- [ ] Parallel fan-out declares fail-fast vs collect-all.
- [ ] `unhandledRejection` / uncaught handlers are configured on purpose.
- [ ] Best-effort background work is either durable or explicitly observed.

## Related

- [Sync, Async, and Callback Propagation](../01-concepts/02-sync-async-and-callback-propagation.md)
- [Concurrent and Cross-Service Propagation](../01-concepts/03-concurrent-and-cross-service-propagation.md)
- [Asynchronous Error Handling (Part XII)](../../../part-12-async-and-background-jobs/31-asynchronous-error-handling/README.md)
- [Process, Runtime, and Resource Failures (Part XV)](../../../part-15-distributed-failures/41-process-runtime-and-resource-failures/README.md)
