# Promise.all vs Promise.allSettled — Mechanics

> Part XII · Chapter 31 · Sections 31.5–31.7 (mechanics) · _Estimated reading time: 15 min_
> **Prerequisite:** [Concurrent Failures and Aggregation](../01-concepts/02-concurrent-failures-and-aggregation.md)

## In one sentence

`Promise.all` **rejects at the first failure but leaves the other promises running**, while
`Promise.allSettled` **waits for every promise and returns a status per input** — the difference
changes both your error visibility and your resource usage.

## Why this matters in production

The subtle part is not the return shape; it is **what happens to the losers**. Developers assume
`Promise.all` "cancels" the rest. It does not. After the first rejection, the remaining operations
continue, consume connections, and may cause side effects. Their eventual rejections are unhandled
unless each promise already has a handler. This is a common source of duplicate writes and
mysterious `unhandledRejection` logs *after* a request has already failed.

## Execution order and timing

```text
t0  all(p1, p2, p3) called; all start immediately
t1  p1 fulfills
t2  p2 rejects  ──▶ all() rejects with p2's reason
t3  p3 still running (not cancelled)
t4  p3 fulfills or rejects — its result is discarded
```

Both primitives start all promises **synchronously and concurrently**. Neither is a scheduler.
"Fail-fast" refers only to when the *aggregate promise* settles, not to stopping the work.

## Return shapes

```ts
const all = await Promise.all([a(), b()]);        // T[] ; throws on first rejection

const settled = await Promise.allSettled([a(), b()]);
// [
//   { status: "fulfilled", value: T },
//   { status: "rejected",  reason: unknown }
// ]
```

Key properties:

| Property | `Promise.all` | `Promise.allSettled` |
| -------- | ------------- | -------------------- |
| Settles on first rejection | ✅ Yes | ❌ No |
| Waits for all | ❌ No | ✅ Yes |
| Number of results | 0 on failure | Always equals input length |
| Result order | Input order | Input order |
| Cancels siblings | ❌ No | ❌ No (but waits) |
| Rejection handler required | Yes | No (never rejects) |

## Why `Promise.all` leaves losers running

The spec composes promises; it has no authority to abort underlying I/O. Aborting requires an
`AbortController` passed into each operation. `Promise.all` only decides **which promise to settle
with**; it cannot stop the others.

```ts
// Siblings keep running after the reject.
await Promise.all([chargeA(), chargeB(), chargeC()]);
```

```ts
// Correct fail-fast: cancel siblings explicitly.
const controller = new AbortController();
try {
  await Promise.all([
    chargeA({ signal: controller.signal }),
    chargeB({ signal: controller.signal }),
    chargeC({ signal: controller.signal }),
  ]);
} catch (err) {
  controller.abort();
  throw err;
}
```

## Preventing orphaned rejections

Even with `Promise.all`, attach handlers so discarded rejections are not unhandled:

```ts
function observed<T>(p: Promise<T>): Promise<T> {
  p.catch((err) => log.warn({ err }, "discarded branch failed")); // observe
  return p;
}

await Promise.all(tasks.map((t) => observed(t.run())));
```

Or use `allSettled`, which observes every outcome by construction.

## Aggregating multiple failures

`Promise.all` surfaces **one** error. When you need all of them, collect and throw:

```ts
const results = await Promise.allSettled(tasks.map((t) => t.run()));
const errors = results.flatMap((r, i) =>
  r.status === "rejected" ? [{ task: tasks[i].name, reason: r.reason }] : [],
);
if (errors.length) {
  throw new AggregateError(
    errors.map((e) => e.reason),
    `${errors.length} of ${tasks.length} failed`,
  );
}
```

`AggregateError` preserves each reason in `.errors`. Log the per-task mapping separately; the
aggregate message alone is not actionable.

## Memory and scheduling effects

- **`allSettled` holds every result** until all settle. For 100k items, that is 100k objects live at
  once. Prefer a bounded pool for large fan-out.
- **`Promise.all` frees the aggregate early** but the losers still hold their closures and buffers
  until they settle.
- **Bounded concurrency** caps in-flight work and is often the real fix:

```ts
async function pool<T>(items: T[], limit: number, fn: (item: T) => Promise<void>) {
  const queue = [...items];
  const workers = Array.from({ length: limit }, async () => {
    while (queue.length) await fn(queue.shift()!);
  });
  await Promise.all(workers); // fail-fast across workers; errors stop the pool
}
```

## Language equivalents

| Language | Fail-fast | Collect-all |
| -------- | --------- | ----------- |
| JS/TS | `Promise.all` | `Promise.allSettled` |
| Python | `asyncio.gather(...)` (default) | `asyncio.gather(..., return_exceptions=True)` |
| Python 3.11+ | `TaskGroup` | `TaskGroup` + catch `ExceptionGroup` |
| Go | `errgroup.Group` | results channel / `errors.Join` |
| Kotlin | `coroutineScope` | `supervisorScope` |
| Rust | `try_join!` | `join!` then inspect each `Result` |

> Go's `errgroup.WithContext` cancels the shared context on first error — closer to true fail-fast
> than JavaScript's `Promise.all`.

## Worked example — WebhookIngest fan-out

`WebhookIngest` resolves a Stripe customer to three internal records: `account`, `subscription`, and
`usage`. `account` is required; the other two can be missing.

```ts
// Before: one missing subscription failed the whole webhook and triggered a retry storm.
await Promise.all([resolveAccount(), resolveSubscription(), resolveUsage()]);

// After: required branch fail-fast; optional branches collect-all.
const account = await resolveAccount();               // throws -> reject webhook (retryable)
const optional = await Promise.allSettled([
  resolveSubscription(),
  resolveUsage(),
]);
const degraded = optional.filter((r) => r.status === "rejected").length;
```

The webhook now succeeds when account resolution works, records `degraded` for observability, and
only retries when the required data is unavailable.

## Key data / numbers

- `Promise.all([])` resolves immediately with `[]`; `Promise.allSettled([])` resolves with `[]`.
- `allSettled` result entries are always in **input order**, even if completion order differs.
- `AggregateError.errors` is an array; `message` is a single string and not a contract.
- Python `gather` without `return_exceptions=True` propagates the first exception but does **not**
  cancel the other tasks.
- A fan-out of 10k concurrent sockets commonly hits `EMFILE`; cap concurrency around 10–50 for I/O.

## Real-world use case — Checkout

Checkout ran `Promise.all` over three payment-provider calls (auth, fraud, ledger). When fraud
timed out, `Promise.all` rejected and the API returned `500`, but auth and ledger **continued and
succeeded**. The retry then charged the card a second time. The fix: required steps fail-fast with
an `AbortController` + idempotency keys, and the ledger write became part of a saga with
compensation. Seeing one error was not the problem; ignoring the still-running successes was.

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| `Promise.all` | Early failure, less waiting | Hides other errors, losers run | All required, bounded, no side effects |
| `Promise.allSettled` | Complete picture | Waits for slowest, memory | Optional branches, bulk operations |
| `AggregateError` over settled | All failures visible | More code | Batch jobs, validation |
| Bounded pool | Resource-safe | Backpressure complexity | High-volume fan-out |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Abort siblings when failing fast | Assume `Promise.all` cancels |
| Observe discarded rejections | Let losers emit unhandled rejections |
| Use `allSettled` for optional work | Use `all` and catch one generic error |
| Bound concurrency for large fan-out | Fire 10k promises at once |
| Map failures back to input names | Log only the aggregate message |

## Common mistakes

- **Believing `Promise.all` cancels.** It does not; pass an abort signal.
- **Catching only the first error.** Other failures are lost or surface later as unhandled.
- **Using `allSettled` and ignoring rejections.** Filtering only fulfilled entries hides failure.
- **Unbounded `allSettled`.** Memory grows with the slowest, largest batch.
- **Treating `AggregateError.message` as structured.** Use per-item codes.

## Checklist

- [ ] Is the fan-out fail-fast or collect-all, and is that documented?
- [ ] On fail-fast, are siblings aborted?
- [ ] Is every discarded promise observed?
- [ ] Are failures mapped back to their input/source?
- [ ] Is concurrency bounded for large or network-heavy fan-out?
- [ ] Did you check the language equivalent's cancellation semantics?

## Related

- [Concurrent Failures and Aggregation](../01-concepts/02-concurrent-failures-and-aggregation.md)
- [Partial Success Aggregation Example](../03-practical-examples/01-partial-success-aggregation.md)
- [Chapter 32 — Partial Completion and Failure Contracts](../../32-background-jobs-queues-and-scheduled-tasks/01-concepts/05-partial-completion-and-failure-contracts.md)
- [Concurrent Failures and Aggregation](../01-concepts/02-concurrent-failures-and-aggregation.md)
