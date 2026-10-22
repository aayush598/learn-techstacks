# Sync, Async, and Callback Propagation

> Part V · Chapter 12 · Sections 12.2, 12.3, 12.6, 12.7, 12.8 · _Estimated reading time: 18 min_
> **Prerequisite:** [Propagation Through Call Stacks](./01-propagation-through-call-stacks.md)

## In one sentence

Synchronous errors unwind a **real stack**; asynchronous errors move between **separate stacks**
connected by a continuation, a callback, or an event — and every hop is a place the original
context can be silently dropped.

## Why this matters in production

In a synchronous world, an uncaught error surfaces immediately at a known line. In an
asynchronous world, the failure surfaces *somewhere else, later*: as an unhandled rejection log,
as a stuck job, or as nothing at all. Most "lost error" incidents in Node, Python, and Go are not
logic bugs — they are **broken propagation across an async boundary**.

## Core concept

Compare the two models:

```text
SYNC                          ASYNC
main()                        main()  ── schedules ──▶ event loop
  ├ a()                         └ a() returns a Promise immediately
  │  └ b()  throws                    (stack ends here)
  │     ▲ unwinds live                ... later ...
  └─────┘ handler in a()              resume b() on a NEW stack  ← cause/context at risk
```

The key difference: in async code, the frame that *starts* the work is gone by the time the work
*fails*. The continuation resumes with a **fresh stack** that does not contain the request handler
unless you carried it.

### Sync (12.2)

Plain function calls; the stack is intact and the error can be caught by any ancestor frame.
Prefer sync errors when the operation completes immediately.

### Async (12.3)

`async`/`await`, `Future`, `Task`, goroutines, threads. The error is delivered through the
await/join primitive. If you do not await, you do not receive.

### Async callbacks (12.6)

Node-style `(err, result)` callbacks and completion handlers. The error is a *parameter*, not a
throw. Forgetting to check `err` is the classic swallowed error.

### Event handlers (12.7)

Emitted events (`emit('error')`, DOM handlers, message consumers) run on their own stack.
An `error` event with **no listener** is frequently fatal (Node throws it). This is a boundary.

### Promise chains (12.8)

`.then().catch()`: a `.catch` handles rejections from *upstream* links only. A rejection thrown
*inside* a downstream `.then` is caught by a later `.catch` — ordering matters.

## How it works (mechanics)

For `async`/`await`, the mechanics are:

1. Calling an async function returns a promise immediately; the body runs until its first `await`.
2. At `await`, the continuation is registered and control returns to the caller.
3. When the awaited promise settles, the continuation runs as a **microtask** — a new stack.
4. A rejection is stored on the promise's state; if no `.catch`/`await` consumer attaches, the
   runtime reports an **unhandled rejection**.

```text
await p  ──▶ suspend ──▶ (caller continues) ──▶ p settles ──▶ resume continuation
                                                               stack: [resume, ...]  ≠ original
```

For Go, the equivalent: a function returns a `channel`; the caller must receive from it. A panic
inside a goroutine is **not** delivered to the parent — it crashes the process unless the goroutine
has its own `recover` (or `errgroup`/`panic`-to-error wrapper).

## Worked example

Three ways the same failure is dropped, then fixed.

```ts
// ❌ 1. Fire-and-forget: rejection is lost
async function notifyTenant(id: string) { await mailer.send(id); }
function onSignup(id: string) {
  notifyTenant(id); // no await — unhandled rejection
}

// ❌ 2. Callback: err ignored
fs.readFile(path, (err, data) => {
  parse(data); // `data` is undefined when err is set
});

// ❌ 3. Promise chain: catch placed before the failing link
doWork()
  .catch(log)          // does NOT catch errors thrown by the next .then
  .then(transform);    // if transform throws, nobody catches

// ✅ Fixes — each hop carries the error forward
async function onSignup(id: string) {
  try {
    await notifyTenant(id);
  } catch (err) {
    throw new SignupNotificationError("notify after signup failed", { cause: err });
  }
}

fs.readFile(path, (err, data) => {
  if (err) return callback(new FileReadError(path, { cause: err }));
  callback(null, parse(data));
});

doWork()
  .then(transform)
  .catch(log);          // catch LAST to cover the whole chain
```

## Key data / numbers

- **Node.js ≥ 15**: unhandled promise rejection terminates the process (`--unhandled-rejections=throw`).
- **Node.js**: an `'error'` event with no listener throws and, if uncaught, exits the process.
- **Python `asyncio`**: an un-awaited coroutine logs *"coroutine was never awaited"*; a task
  exception surfaces only via `Task.add_done_callback` or `asyncio.gather`.
- **Go `errgroup`**: converts the first goroutine error into the `Wait()` return value; a bare
  `panic` still crashes unless recovered.
- **Java `CompletableFuture`**: an exception in a stage without `exceptionally`/`handle` is dropped
  into the returned future; unobserved futures report nothing.

## Real-world use case — Acme SaaS

Acme's `AgentRun` fired tool calls with `Promise.all` and logged failures via
`promise.catch(log)` at the *end* — but a later `.then` reformatted the tool output and sometimes
threw. Those throws were outside the `catch`, so a formatting bug looked like a successful run
with missing data. The team restructured to `await Promise.allSettled(...)`, recorded per-tool
failures explicitly, and placed the terminal `.catch` last. Lost failures dropped to zero.

## Trade-offs

| Model | How error arrives | Failure to propagate looks like |
| ----- | ----------------- | ------------------------------- |
| `async/await` | thrown at `await` | unhandled rejection |
| Callbacks | `err` parameter | `undefined` result, silent |
| Event emitter | `'error'` event | process crash (no listener) |
| Promise chain | rejection to next `.catch` | dropped future |
| Goroutine + channel | value/`err` on channel | deadlock or process panic |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| `await` or `.catch` every promise | Fire-and-forget unless truly best-effort |
| Check the `err` parameter first | Use a callback result before checking `err` |
| Place the terminal `.catch` at the end | Put `.catch` before failing `.then` links |
| Attach an `'error'` listener at the boundary | Emit `'error'` with no listener |
| Wrap async errors with `cause` across hops | Reject with a bare string |

## Common mistakes

- **`forEach(async …)`** — the loop does not await; rejections vanish. Use `for…of` or
  `Promise.all`.
- **`Promise.all` short-circuits** on the first rejection while other promises keep running
  unobserved. Use `allSettled` when you must know every outcome.
- **Swallowing in a callback** by returning early on `err` without signalling the caller.
- **Assuming `try/catch` around a callback catches async errors** — it only catches synchronous
  throws *before* the callback is scheduled.

## Checklist

- [ ] Every promise is awaited or has a `.catch`.
- [ ] Every callback checks `err` before using the result.
- [ ] Every emitter has an `'error'` listener or an explicit handler.
- [ ] Async wrappers pass the original error as `cause`.
- [ ] No `async` callbacks passed to functions that ignore returned promises.

## Related

- [Concurrent and Cross-Service Propagation](./03-concurrent-and-cross-service-propagation.md)
- [Async Propagation and Unhandled Rejections](../02-deep-dive/02-async-propagation-and-unhandled-rejections.md)
- [Asynchronous Error Handling (Part XII)](../../../part-12-async-and-background-jobs/31-asynchronous-error-handling/README.md)
- [Rethrow, Wrap, and Preserve Cause](./04-rethrow-wrap-and-preserve-cause.md)
