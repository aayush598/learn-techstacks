# Callbacks, Streams, and Reactive Pipelines

> Part XII · Chapter 31 · Sections 31.11–31.13 · _Estimated reading time: 16 min_
> **Prerequisite:** [Sync vs Async Error Semantics](./01-sync-vs-async-error-semantics.md)

## In one sentence

Every async abstraction — **error-first callbacks, streams, reactive pipelines** — has exactly one
place where errors surface and one rule for termination; if you do not wire that channel, the
failure is lost or the pipeline hangs.

## Why this matters in production

Streams and reactive pipelines fail *partway through*. Half your data was written, the subscriber
already received 40 000 events, and then the socket resets. If you only handle the "success"
callback, you neither commit nor roll back — you leave partial state with no error signal. These
abstractions are common in file processing (`ExportJob`), event fan-out, and real-time dashboards,
where partial delivery is normal and silent truncation is unacceptable.

## 31.11 — Callbacks

The **error-first callback** convention (Node.js) is the original async error contract:

```ts
function readConfig(path: string, cb: (err: Error | null, data?: string) => void): void {
  fs.readFile(path, "utf8", (err, data) => {
    if (err) return cb(err);   // error is the FIRST argument
    cb(null, data);            // success: first arg is null
  });
}
```

Rules that prevent the classic bugs:

1. **Check `err` before using `data`.** A non-null error means `data` is undefined.
2. **Return after calling `cb`.** Otherwise execution continues and calls back twice.
3. **Never call the callback twice.** Double-callback is the callback-era equivalent of a double
   side effect and causes "headers already sent" bugs.
4. **Never throw inside the callback.** It escapes to the emitter, not the caller.
5. **Convert to a promise at the boundary** so the rest of the code uses one model.

```ts
import { promisify } from "node:util";
const readConfigAsync = promisify(readConfig); // error-first → promise
```

## 31.12 — Streams

A stream is a sequence of chunks with **three error surfaces** and **one completion event**:

| Surface | Where it appears | What to do |
| ------- | ---------------- | ---------- |
| Source error | `readable.on("error")` | Abort downstream, clean temp files |
| Transform error | the transform's `callback(err)` / `on("error")` | Destroy the pipeline |
| Sink error | `writable.on("error")` | Roll back / delete partial output |
| Completion | `"finish"` (writable) / `"end"` (readable) | Only then publish/commit |

```ts
import { pipeline } from "node:stream/promises";

try {
  await pipeline(
    db.streamRows(job.query),       // readable
    new CsvTransform(),             // transform
    s3.createWriteStream(tempKey),  // writable
  );
  await s3.copy(tempKey, finalKey); // commit only after full pipeline
} catch (err) {
  await s3.delete(tempKey).catch(() => {}); // cleanup partial output
  throw err;
}
```

Pitfalls:

- **`pipe()` does not forward errors** to the destination by default; use `pipeline()`.
- **A destroyed stream may still emit `error`.** Attach a listener before destroying.
- **Completion is not durability.** `"finish"` means the sink accepted the bytes, not that a remote
  write committed.
- **Backpressure failures look like timeouts.** A slow sink stalls the source; add a deadline.

## 31.13 — Reactive pipelines

Reactive streams (RxJS, Reactor, Akka Streams) define an **error channel that terminates the
stream** unless you explicitly recover. That is the key semantic:

```text
observable:  next* ──▶ complete
                    └─▶ error   (terminal: no more next after this)
```

```ts
import { catchError, retry, of } from "rxjs";

source$
  .pipe(
    retry({ count: 3, delay: 1000 }),      // retries the whole subscription
    catchError((err) => {
      metrics.increment("stream_failed");
      return of([]);                        // fallback: empty, not silent success
    }),
  )
  .subscribe({
    next: (rows) => render(rows),
    error: (err) => showBanner(err),        // only if catchError did not recover
    complete: () => hideSpinner(),
  });
```

Rules:

1. **An error terminates the stream.** If you need to continue after a failed item, handle it
   *inside* (`map` to a result type), not at the outer `catchError`.
2. **`retry` re-subscribes**, which may re-run side effects. Make the source idempotent or use
   `retryWhen` with a bounded policy.
3. **`catchError` returning a value converts failure into success.** That is sometimes right
   (optional widget), sometimes a bug (required data). Name it explicitly.
4. **Unsubscribe on teardown.** A leaked subscription keeps producing errors after the UI is gone.
5. **Backpressure is not optional.** A fast producer + slow consumer = memory growth, then OOM.

## Worked example — WebhookIngest event fan-out

`WebhookIngest` receives a Stripe event and maps it to internal domain events on an RxJS subject.
A bad event handler previously killed the whole subject, silently stopping all subsequent events.

```ts
subject$
  .pipe(
    // Isolate each event: one failure must not terminate the shared stream.
    mergeMap((event) =>
      handleEvent(event).pipe(
        catchError((err) => {
          deadLetter(event, err);
          return EMPTY; // drop just this event, keep the stream alive
        }),
      ),
    ),
  )
  .subscribe({ error: (err) => log.fatal({ err }, "shared stream died") });
```

The fix is per-item isolation (`mergeMap` + inner `catchError`) instead of a single outer handler.

## Key data / numbers

- Node `stream.pipeline` forwards errors and destroys all streams; `pipe()` does not.
- RxJS: after `error`, the observable is **closed**; you cannot receive more values.
- Reactive Streams default request size is often **1** (Reactor) or unbounded; configure
  `limitRate`/`flatMap(maxConcurrency)` to bound memory.
- Node readable highWaterMark defaults: **16 KiB** (bytes) or **16 objects**.
- A transform that calls `callback(err)` must not also call `callback(null, chunk)`.

## Real-world use case — ExportJob

`ExportJob` used `readable.pipe(csv).pipe(s3Write)` and resolved when the S3 stream emitted
`"finish"`. When the DB connection dropped mid-stream, the readable emitted `error`, but `pipe()`
did not forward it; the S3 stream finished with a truncated file and the job was marked **succeeded**.
The CSV was missing 30% of rows. The fix: `pipeline()` plus write-to-temp-then-copy, so an error
deletes the partial object and the job transitions to `failed`.

## Trade-offs

| Abstraction | Pros | Cons | When to use |
| ----------- | ---- | ---- | ----------- |
| Error-first callbacks | Universal, low-level | Double-callback, nesting | Legacy APIs; wrap immediately |
| Async iterators / `for await` | Readable, backpressure-friendly | Slower per item | Sequential streaming |
| Streams `pipeline` | Error forwarding, cleanup | Complex error surfaces | Large file/data transfer |
| Reactive | Composition, operators | Error terminates stream | Event fan-out, UI state |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Check the error argument first | Use `data` when `err` is set |
| `return` after invoking a callback | Continue after calling back |
| Use `pipeline()` / `for await` | Use bare `.pipe()` for error-prone work |
| Commit output only after completion | Publish a partial file as final |
| Isolate per-item errors in a stream | Let one item kill the shared stream |
| Unsubscribe/teardown | Leak subscriptions and timers |

## Common mistakes

- **Double callback** — the second call causes duplicate writes or "headers already sent."
- **Ignoring `"error"` on one of three stream stages** — the pipeline appears to hang or truncates.
- **`catchError(() => of(null))` in a required path** — failure becomes silent success.
- **Retrying a reactive stream with side effects** — duplicates on re-subscription.
- **Unbounded `mergeMap`** — thousands of concurrent inner subscriptions exhaust resources.

## Checklist

- [ ] Are all callbacks error-first and invoked exactly once?
- [ ] Does every stream stage have an `error` handler, and is `pipeline()` used?
- [ ] Is output committed only after the completion event?
- [ ] Are partial artifacts cleaned up on failure?
- [ ] Does one bad event avoid terminating a shared reactive stream?
- [ ] Are subscriptions and timers torn down on completion/error/unsubscribe?
- [ ] Is backpressure/concurrency bounded?

## Related

- [Concurrent Failures and Aggregation](./02-concurrent-failures-and-aggregation.md)
- [Async Cleanup and Detached Failures](./05-async-cleanup-and-detached-failures.md)
- [Chapter 33 — Consumer Isolation and Eventual Consistency](../../33-events-webhooks-and-message-processing/01-concepts/05-consumer-isolation-and-eventual-consistency.md)
- [Chapter 33 — Events, Webhooks, and Message Processing](../../../part-12-async-and-background-jobs/33-events-webhooks-and-message-processing/README.md)
