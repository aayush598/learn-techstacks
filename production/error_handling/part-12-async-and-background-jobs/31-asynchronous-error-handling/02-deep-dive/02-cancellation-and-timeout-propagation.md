# Cancellation and Timeout Propagation — Mechanics

> Part XII · Chapter 31 · Sections 31.8–31.9 (mechanics) · _Estimated reading time: 16 min_
> **Prerequisite:** [Cancellation, Timeouts, and Event-Driven Errors](../01-concepts/03-cancellation-timeouts-and-events.md)

## In one sentence

A cancellation signal is only real if it is **threaded through every downstream call**, and a
timeout is only real if it **aborts the work rather than just the wait** — otherwise you keep paying
for operations the caller already abandoned.

## Why this matters in production

Provider calls cost money and hold connections. A handler that returns after a 5 s timeout while the
provider call runs for 60 s leaves 55 s of billable, connection-holding work per abandoned request.
Multiply by a traffic spike and you exhaust connection pools and budgets. Correct propagation also
prevents **duplicate side effects** when a retry starts while the first attempt is still alive.

## The two mechanisms

```text
Cancellation: caller decides to stop (client disconnect, shutdown, sibling failed)
Timeout:      a deadline passes (the caller sets a maximum duration)

            both produce the SAME downstream effect: abort
```

Treat them as one concept internally, but keep them **distinguishable in logs and terminal states**.

## AbortSignal composition (JavaScript/TypeScript)

```ts
function operationSignal(clientSignal: AbortSignal, timeoutMs: number): AbortSignal {
  const timeout = AbortSignal.timeout(timeoutMs);      // aborts with TimeoutError
  const combined = AbortSignal.any([clientSignal, timeout]); // Node 20+
  return combined;
}
```

`AbortSignal.any` propagates the **first** abort reason. Inspect it to tell the causes apart:

```ts
function classifyAbort(signal: AbortSignal): "cancelled" | "timed_out" {
  return signal.reason?.name === "TimeoutError" ? "timed_out" : "cancelled";
}
```

## Threading the signal

Every I/O-bearing function accepts a signal last and forwards it:

```ts
type Ctx = { signal: AbortSignal; deadline: number };

async function fetchJson<T>(url: string, ctx: Ctx): Promise<T> {
  const res = await fetch(url, {
    signal: AbortSignal.any([
      ctx.signal,
      AbortSignal.timeout(Math.max(0, ctx.deadline - Date.now())),
    ]),
  });
  return res.json() as Promise<T>;
}
```

Anti-patterns that break propagation:

| Anti-pattern | Effect |
| ------------ | ------ |
| Signal accepted but not passed to `fetch` | Abort does nothing; work continues |
| New `AbortController()` inside each function | Parent cancellation never reaches it |
| `Promise.race([work, timeout])` only | Aggregate settles; work keeps running |
| Catching `AbortError` and continuing | Cancellation is swallowed |
| Passing a cancelled signal to cleanup | Cleanup aborts instantly |

## Deadline budgets

A **deadline** is an absolute time; a **timeout** is a duration. Propagate the deadline so each hop
gets only the remaining budget.

```ts
const deadline = Date.now() + 30_000;

await stepA({ deadline });              // may use up to 30 s
await stepB({ deadline });              // gets 30 s minus stepA's time
await stepC({ deadline });              // gets whatever remains
```

```text
t0 ───────────────────────────────────────────── t30
│ stepA 8s │ stepB 14s │ stepC 6s │ cleanup 2s │
                       ▲ remaining shrinks here
```

Reserve cleanup time explicitly. If the deadline is exhausted, do not start a step that cannot
finish; fail with `DEADLINE_EXCEEDED`.

## Language mechanics

### Python

```python
import asyncio

async def fetch(ctx: dict, url: str) -> str:
    remaining = ctx["deadline"] - asyncio.get_running_loop().time()
    if remaining <= 0:
        raise TimeoutError("deadline exceeded")
    async with asyncio.timeout(remaining):   # 3.11+
        return await client.get(url)
```

`asyncio.CancelledError` inherits `BaseException`; a bare `except Exception` will **not** swallow
it. Do not suppress it unless you are doing cleanup and re-raising.

### Go

```go
ctx, cancel := context.WithTimeout(parent, 30*time.Second)
defer cancel() // releases the timer even on early return

if err := stepA(ctx); err != nil {
    return fmt.Errorf("stepA: %w", err) // preserves context.Canceled / DeadlineExceeded
}
```

Check `errors.Is(err, context.Canceled)` and `errors.Is(err, context.DeadlineExceeded)` to classify.
`defer cancel()` is mandatory; forgetting it leaks the timer until it fires.

### Kotlin

```kotlin
coroutineScope {                 // failure/cancellation propagates to all children
    val a = async { stepA() }
    val b = async { stepB() }
    awaitAll(a, b)               // cancels siblings on failure
}
```

Use `supervisorScope` only when child failures must not cancel siblings (collect-all semantics).

## Cleanup on abort

When aborted, you still owe cleanup: delete temp files, release locks, mark the job `cancelled`.

```ts
try {
  await runWithSignal(signal);
} catch (err) {
  if (isAbortError(err)) {
    await markCancelled(job.id).catch((e) => log.error({ e }, "mark cancelled failed"));
    return;
  }
  throw err;
} finally {
  await cleanupWithFreshTimeout(); // do NOT pass the aborted signal
}
```

Cleanup gets a **fresh** short-lived signal. Passing the aborted one makes cleanup fail instantly.

## Worked example — AgentRun with per-tool deadlines

```ts
async function runAgent(runId: string, clientSignal: AbortSignal) {
  const deadline = Date.now() + 25_000;
  const ctx: Ctx = { signal: clientSignal, deadline };

  const results = await Promise.allSettled([
    tool.search({ ctx, query: "..." }),
    tool.profile({ ctx, userId: "..." }),
    llm.complete({ ctx, prompt: "..." }),
  ]);

  if (clientSignal.aborted) return { status: "cancelled" as const };

  const failures = results.filter((r) => r.status === "rejected");
  if (failures.every((f) => isTimeout(f.reason))) return { status: "timed_out" as const };

  return { status: "partial", results }; // some tools may have failed
}
```

Because every tool receives `ctx`, the client abort stops all three provider calls, and a slow tool
cannot exceed the overall deadline.

## Key data / numbers

- `AbortSignal.timeout(ms)` → `DOMException` named `TimeoutError`; `controller.abort()` → `AbortError`.
- Node HTTP `request.setTimeout` is a **socket idle** timeout, not a total-operation deadline.
- Go `context.WithTimeout` creates a timer; always `defer cancel()`.
- Python 3.11 `asyncio.timeout()` replaces the older `wait_for` in most new code.
- gRPC propagates deadlines via the `grpc-timeout` header; the server sees the remaining budget.
- A 30 s gateway timeout with three sequential 15 s internal calls is already over budget.

## Real-world use case — Checkout

Checkout's `capturePayment` called the provider without a signal. When the API gateway timed out at
30 s, the Lambda continued for another 45 s until its own timeout. During that window a client retry
started a second capture. With an `Idempotency-Key` the second was collapsed, but the first still
held a connection and a worker slot. After propagating the gateway deadline to the provider call,
the first attempt aborted at 29 s, freeing the slot before the retry arrived.

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| No cancellation | Simplest | Wasted work, duplicate side effects | Pure CPU, tiny tasks |
| `AbortSignal`/`Context` | Precise, composable | Plumbing through every layer | Any I/O |
| `Promise.race` only | Trivial | Work outlives the caller | Last-resort guard |
| Deadline budget | Predictable latency | Requires boundary computation | Multi-hop operations |
| Per-hop timeout | Local reasoning | Sum can exceed caller budget | Isolated single calls |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Pass signal/context through every I/O call | Accept it and drop it |
| Compute one deadline at the boundary | Give each hop the full timeout |
| Classify `cancelled` vs `timed_out` | Collapse both into `failed` |
| Use a fresh signal for cleanup | Reuse the aborted signal |
| `defer cancel()` in Go | Leak the context timer |

## Common mistakes

- **`Promise.race` mistaken for cancellation** — the underlying call keeps running.
- **Nested controllers with no linkage** — parent abort does not reach children.
- **Swallowing `AbortError`** — the operation reports success after being cancelled.
- **Deadline recomputed per hop** — total latency doubles or triples silently.
- **Cleanup on the aborted signal** — the lock/temp file is never released.

## Checklist

- [ ] Does every I/O function accept and forward a signal/context?
- [ ] Is there a single deadline computed at the boundary?
- [ ] Is cancellation distinguished from timeout in logs and terminal state?
- [ ] Are sibling tasks aborted when one fails (fail-fast)?
- [ ] Does cleanup use a fresh, short timeout?
- [ ] Do retries start only after the previous attempt has aborted?
- [ ] Are context timers always cancelled in Go?

## Related

- [Cancellation, Timeouts, and Event-Driven Errors](../01-concepts/03-cancellation-timeouts-and-events.md)
- [Cancellation in AgentRun](../03-practical-examples/02-cancellation-in-agentrun.md)
- [Chapter 29 — Timeouts, Circuit Breakers, and Bulkheads](../../../part-11-retry-and-resilience/29-timeouts-circuit-breakers-and-bulkheads/README.md)
- [Chapter 14 — Resource Cleanup](../../../part-05-exception-mechanics/14-resource-cleanup-and-failure-safe-execution/README.md)
