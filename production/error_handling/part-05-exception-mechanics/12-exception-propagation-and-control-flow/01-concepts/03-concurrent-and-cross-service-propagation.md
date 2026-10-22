# Concurrent and Cross-Service Propagation

> Part V · Chapter 12 · Sections 12.5, 12.9 · _Estimated reading time: 15 min_
> **Prerequisite:** [Sync, Async, and Callback Propagation](./02-sync-async-and-callback-propagation.md)

## In one sentence

Concurrency forks one call path into **many that fail independently**, and a service boundary
turns an in-process error into a **serialized message** — so both require an explicit rule for
collecting, prioritizing, and reconstructing failures.

## Why this matters in production

Sequential code has one failure at a time. Concurrent code has *N* failures that can happen in any
order, some of which you never observe because the first one "won". Distributed code has failures
that arrive as `503`s, timeouts, or half-open sockets — with the original stack left on the other
machine. Getting propagation right here is the difference between "one item in the batch failed"
and "the whole batch silently lost two items".

## Core concept

### Concurrent operations (12.9)

When you fan out work, each branch has its own failure channel. There are three collection
strategies, and choosing the wrong one is a classification bug:

| Strategy | Behavior | Use when |
| -------- | -------- | -------- |
| **Fail-fast** | Cancel remaining work on first failure | All parts are required (atomic batch) |
| **Collect-all** | Run everything, gather every outcome | Independent items; report partial success |
| **First-success** | Return as soon as one succeeds | Redundant replicas; race for lowest latency |

```text
        ┌─ worker A ─▶ ok
fan-out ├─ worker B ─▶ FAIL   ── fail-fast: cancel A, C; report B's error
        └─ worker C ─▶ ???    ── collect-all: wait for C; report [A ok, B fail, C ok]
```

### Across service boundaries (12.5)

A boundary destroys the live stack. What crosses is:

- a **status/error code** (HTTP status, gRPC status, SQLSTATE),
- a **serialized message**,
- optionally a **correlation ID** and a **retry hint** (`Retry-After`),
- and, if you are disciplined, a **cause chain** you deliberately serialize.

The receiving service must treat this as a *new* error and re-attach its own context; it cannot
see the original frames.

## How it works (mechanics)

Local fan-out (Go `errgroup`) reduces many errors to one, but only the **first**:

```go
g, ctx := errgroup.WithContext(ctx)
for _, item := range items {
    item := item
    g.Go(func() error { return process(ctx, item) })
}
err := g.Wait() // first non-nil error; ctx cancelled for the rest
```

To keep *every* failure you need a collector:

```go
var mu sync.Mutex
var errs []error
g, ctx := errgroup.WithContext(ctx)
for _, item := range items {
    item := item
    g.Go(func() error {
        if err := process(ctx, item); err != nil {
            mu.Lock(); errs = append(errs, fmt.Errorf("item %s: %w", item.ID, err)); mu.Unlock()
        }
        return nil // always nil so g.Wait() doesn't short-circuit
    })
}
_ = g.Wait()
return errors.Join(errs...) // Go 1.20+
```

Cross-service, the mechanics are serialization and translation:

1. Sender maps its internal error to a **stable external code** at the boundary (Chapter 16).
2. Receiver parses the response; a `4xx` is a *caller* error (do not retry), a `5xx`/timeout is a
   *remote* error (may be transient).
3. Receiver **creates a new error** carrying the remote status, `retry-after`, and a correlation
   ID, optionally as `cause` if the transport exposes a body.

## Worked example

`ExportJob` processes 10,000 rows in parallel chunks. The old code used `Promise.all`, so the
first chunk failure aborted the export and *discarded* the three chunks that had already written
to S3 — leaking storage and leaving a half-written manifest.

```ts
// ✅ Collect-all with explicit per-chunk outcomes
const results = await Promise.allSettled(
  chunks.map((chunk) => exportChunk(chunk)),
);

const failures = results.flatMap((r, i) =>
  r.status === "rejected" ? [{ chunk: i, error: r.reason }] : [],
);

if (failures.length > 0) {
  // Partial success is a first-class outcome, not an exception.
  throw new ExportPartialFailure(failures, {
    succeeded: results.length - failures.length,
    failed: failures.length,
  });
}
```

The job now records `succeeded`/`failed` counts and only fails the job when *all* chunks fail;
otherwise it completes with a partial-success report (Chapter 39).

## Key data / numbers

- **HTTP `429`** carries `Retry-After` (seconds or HTTP-date) — the canonical cross-service hint.
- **gRPC status `UNAVAILABLE` (14)** and **`DEADLINE_EXCEEDED` (4)** are typically retryable;
  `INVALID_ARGUMENT (3)` is not.
- **PostgreSQL `40001`** serialization failure on one concurrent transaction means the *other*
  may have committed; retry the loser.
- **Go `errors.Join`** (1.20+) accumulates multiple causes; `errors.Is/As` traverses the tree.
- **Java `Throwable.getSuppressed()`** carries failures from parallel/sub-tasks alongside the
  primary.
- **Python `asyncio.gather(return_exceptions=True)`** returns exceptions in the result list
  instead of raising the first.

## Real-world use case — Acme SaaS

Acme's `Checkout` reserved inventory, charged the card, and sent a receipt — three concurrent
steps guarded by one `Promise.all`. When the receipt email failed, `Promise.all` rejected and the
service reported the whole checkout as failed, even though the card was charged. Alerting said
"checkout failed" while money moved. They switched to a saga with `allSettled`, treated the receipt
as a best-effort side effect, and only failed the checkout on charge/inventory errors. Propagation
was reclassified by **business criticality**, not by concurrency convenience.

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| Fail-fast | Simple; stops wasted work | Discards done work | Atomic multi-step ops |
| Collect-all | Accurate partial state | More code; must aggregate | Batch/job processing |
| First-success | Lowest latency | Orphaned slower branches | Redundant replicas |
| Raw rethrow across service | Fast to write | Loses cause; misclassifies | Never at a real boundary |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Choose fail-fast vs collect-all per operation | Default to `Promise.all` everywhere |
| Translate remote errors at the boundary | Rethrow a remote `500` as your own `500` |
| Attach a correlation ID across services | Assume the receiver sees your stack |
| Use `errors.Join` / suppressed for many causes | Keep only the first error silently |
| Cancel loser branches in a race | Leave orphaned work running unobserved |

## Common mistakes

- **`Promise.all` for independent work** — first failure hides the rest and abandons completed work.
- **Retrying a remote `400`** — client errors are permanent; only `5xx`/timeout are candidates.
- **No correlation ID** — you cannot join the caller's log line to the callee's.
- **Assuming the remote error message is stable** — providers change wording; key off status/code.

## Checklist

- [ ] Does each fan-out declare fail-fast, collect-all, or first-success?
- [ ] Are concurrent errors collected, not just the first?
- [ ] Does every service boundary map to a stable code?
- [ ] Is there a correlation ID on every cross-service error?
- [ ] Are remote `4xx` and `5xx` classified differently?

## Related

- [Sync, Async, and Callback Propagation](./02-sync-async-and-callback-propagation.md)
- [Rethrow, Wrap, and Preserve Cause](./04-rethrow-wrap-and-preserve-cause.md)
- [Partial Failures and Multi-Step Operations (Part XV)](../../../part-15-distributed-failures/39-partial-failures-and-multi-step-operations/README.md)
- [Network and Distributed Communication Errors (Part X)](../../../part-10-external-dependencies/26-network-and-distributed-communication-errors/README.md)
