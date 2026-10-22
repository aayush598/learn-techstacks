# Cancellation, Timeouts, and Event-Driven Errors

> Part XII · Chapter 31 · Sections 31.8–31.10 · _Estimated reading time: 17 min_
> **Prerequisite:** [Concurrent Failures and Aggregation](./02-concurrent-failures-and-aggregation.md)

## In one sentence

Cancellation and timeouts are **control signals that must travel with the work**, and event-driven
handlers are **boundaries that own their own failures** — treating either as an afterthought leaves
work running after the user has gone and errors with nowhere to go.

## Why this matters in production

A client disconnects; your handler keeps querying the database for another 40 seconds. A request
times out at 5 seconds; the downstream provider call keeps running and bills you. A retry starts
while the first attempt is still alive, and both write the same row. Cancellation exists to stop
**wasted work and duplicate side effects**. Event handlers exist to **own failures** that no
request can catch.

## 31.8 — Cancellation

Cancellation is a *cooperative* request to stop. It is not a kill signal: the callee must check and
honor it. The mechanics differ, the contract does not.

| Runtime | Signal | Cancel API | "Cancelled" error |
| ------- | ------ | ---------- | ----------------- |
| JavaScript | `AbortSignal` | `controller.abort()` | `DOMException` name `AbortError` |
| Python | `asyncio.CancelledError` | `task.cancel()` | `CancelledError` (inherits `BaseException`) |
| Go | `context.Context` | `cancel()` | `ctx.Err() == context.Canceled` |
| Kotlin | `Job` / `CoroutineScope` | `job.cancel()` | `CancellationException` |
| Rust | drop the future | — | future stops being polled |

### Cancellation is not failure

```ts
try {
  await runAgent(signal);
} catch (err) {
  if (isAbortError(err)) {
    log.info("run cancelled by client");
    return;               // cancellation is an expected outcome, not an error page
  }
  throw err;              // real failure
}
```

If you report cancellation as `500`, you pollute error rates and retries with work the user
deliberately stopped. If you report it as `200`, you claim success for work that did not finish.
Model it as its own terminal state (`cancelled`), separate from `failed`.

### Cancellation must reach every downstream call

```ts
async function runAgent(signal: AbortSignal) {
  const tools = await Promise.all([
    searchDocs({ signal }),        // pass it down
    fetchProfile({ signal }),      // pass it down
    llm.complete({ signal }),      // pass it down
  ]);
  return tools;
}
```

A signal held only at the top is decorative. Every network/DB call must accept and forward it.
Timeout and cancellation are the *same mechanism* with different triggers.

## 31.9 — Timeout propagation (deadlines)

A timeout that merely races a promise does **not stop the underlying work**:

```ts
// ❌ The request "times out" but the provider call keeps running and billing.
await Promise.race([provider.charge(), sleep(5000).then(() => { throw new TimeoutError(); })]);
```

Correct timeout handling uses a **deadline budget** propagated to each hop:

```ts
type Deadline = { at: number }; // epoch ms

function remaining(d: Deadline): number {
  return Math.max(0, d.at - Date.now());
}

async function handler(deadline: Deadline) {
  const res = await fetch(url, { signal: AbortSignal.timeout(remaining(deadline)) });
  return res;
}
```

Rules:

1. **Compute the deadline once** at the request/job boundary (`now + timeout`).
2. **Pass the remaining budget** to each call, not the original timeout, so N sequential calls do
   not each get the full budget.
3. **Abort the underlying operation**, not just the awaiting code.
4. **Reserve cleanup time** — leave, say, 10% of the budget for releasing resources.
5. **Distinguish timeout from cancellation** in logs and metrics: `DEADLINE_EXCEEDED` vs
   `CLIENT_CANCELLED`.

```text
deadline = T+30s
 ├─ call A:  remaining 30s ─▶ finishes 8s
 ├─ call B:  remaining 22s ─▶ finishes 15s
 ├─ call C:  remaining  7s ─▶ times out at 7s, aborts
 └─ cleanup: 2s reserved (slightly over budget if not reserved)
```

> ⚠️ **Hazard.** A per-call timeout of 10 s used five times sequentially creates a 50 s operation
> behind a 30 s gateway timeout. The gateway gives up first; your worker keeps running.

## 31.10 — Event-driven error handling

Event handlers (DOM events, `EventEmitter`, message consumers, webhook handlers) are **implicit
entry points**. There is no caller to return an error to, so the handler must own the outcome:

- **Catch at the handler boundary.** An exception thrown out of an event callback often becomes an
  `uncaughtException` or is swallowed by the emitter.
- **Ack/reject explicitly** when the event source supports it (Chapter 33).
- **Never let one listener's failure stop other listeners** unless that is the documented contract.
- **Make handlers idempotent**, because event sources redeliver.

```ts
// Node EventEmitter: an async listener's rejection is NOT caught by the emitter.
emitter.on("invoice.created", async (event) => {
  try {
    await projectInvoice(event);          // handle inside the boundary
  } catch (err) {
    await deadLetter(event, err);         // terminal, observable
  }
});
```

Node's `EventEmitter` does not await listeners, so an `async` listener that throws produces an
**unhandled rejection** while the emitter continues. Wrap the body and decide ack/skip explicitly.

### Event handler failure matrix

| Event source | On handler failure | Who retries | Duplicate risk |
| ------------ | ------------------ | ----------- | -------------- |
| In-process `EventEmitter` | Unhandled rejection | Nobody | None (but no durability) |
| SQS/Kafka consumer | Message not acked | Broker | Yes — at-least-once |
| Webhook endpoint | Non-2xx response | Sender | Yes — sender retries |
| Cron/scheduled task | Task marked failed | Scheduler policy | Yes — overlapping runs |

## Worked example — AgentRun cancellation

`AgentRun` calls three tools in parallel, then synthesizes an answer. The user closes the tab.

```ts
async function runAgent(prompt: string, clientSignal: AbortSignal) {
  const deadline: Deadline = { at: Date.now() + 25_000 };
  const controller = new AbortController();
  clientSignal.addEventListener("abort", () => controller.abort(), { once: true });

  const signal = AbortSignal.any([
    controller.signal,
    AbortSignal.timeout(remaining(deadline)),
  ]);

  try {
    const [docs, profile, llm] = await Promise.all([
      searchDocs({ signal }),
      fetchProfile({ signal }),
      llm.complete({ prompt, signal }),
    ]);
    return synthesize(docs, profile, llm);
  } catch (err) {
    if (isAbortError(err)) return { status: "cancelled" as const }; // not a failure
    if (isTimeout(err)) return { status: "timed_out" as const };
    throw err;
  }
}
```

Because the signal reaches all three calls, aborting actually **stops provider work** and releases
the tokens already spent. The result is a `cancelled` terminal state, not a retryable error.

## Key data / numbers

- `AbortSignal.timeout(ms)` (Node 17.3+) aborts with a `TimeoutError` `DOMException`.
- `AbortSignal.any([...])` (Node 20+) composes multiple signals.
- Python `asyncio.CancelledError` inherits `BaseException`, so bare `except Exception` will **not**
  catch it — cancellation still propagates, which is usually correct.
- Go `context.WithTimeout` must be cancelled via the returned `cancel` func to release the timer.
- Common gateway defaults: 30 s (ALB idle), 60 s (many proxies). Keep job budgets below them or
  use async jobs.

## Real-world use case — ExportJob

Acme's `ExportJob` streamed 2 GB from Postgres to S3. When a worker was scaled down, the process
received `SIGTERM`; the job's DB cursor kept streaming until the container was killed, leaving a
partial object with a *complete-looking* key. The fix: pass a cancellation context tied to
`SIGTERM`, abort the query, write to a temp key, and only copy to the final key after a checksum
confirms completion. Cancellation now leaves no half-written artifact.

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| No cancellation | Simplest | Wasted work, duplicate side effects | Trivial CPU-only work |
| `AbortSignal` prop | Precise, composable | Must thread through every call | Network/DB fan-out |
| `Promise.race` timeout | Easy | Underlying work keeps running | Last-resort guard only |
| Deadline budget | Predictable end-to-end | More plumbing | Multi-hop requests/jobs |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Treat cancellation as a distinct terminal state | Report it as `500` or `200` |
| Pass the signal/context to every downstream call | Hold it only at the top |
| Propagate remaining budget as a deadline | Give each hop the full timeout |
| Reserve time for cleanup | Let cleanup overrun the deadline silently |
| Wrap async event listeners and own failures | Assume the emitter catches rejections |

## Common mistakes

- **`Promise.race` as a timeout** — the loser keeps running; you still pay for it.
- **Swallowing `CancelledError`** — Python's `BaseException` base means a bare `except` can hide it.
- **Forgetting `cancel()`** — Go's `context.WithTimeout` leaks a timer until it fires.
- **Aborting after the response is sent** — cleanup never runs; the client sees success.
- **Async `EventEmitter` listeners** — rejections bypass the emitter entirely.

## Checklist

- [ ] Does every network/DB call accept and forward a cancellation signal?
- [ ] Is there one deadline computed at the boundary and propagated as remaining time?
- [ ] Are cancellation, timeout, and failure three distinct terminal states?
- [ ] Does cleanup run on abort, with reserved time?
- [ ] Are event listeners wrapped so their failures have an owner?
- [ ] Are timeout budgets smaller than the caller's/gateway's timeout?

## Related

- [Cancellation and Timeout Propagation — Mechanics](../02-deep-dive/02-cancellation-and-timeout-propagation.md)
- [Cancellation in AgentRun](../03-practical-examples/02-cancellation-in-agentrun.md)
- [Chapter 29 — Timeouts, Circuit Breakers, and Bulkheads](../../../part-11-retry-and-resilience/29-timeouts-circuit-breakers-and-bulkheads/README.md)
- [Chapter 33 — Events, Webhooks, and Message Processing](../../../part-12-async-and-background-jobs/33-events-webhooks-and-message-processing/README.md)
