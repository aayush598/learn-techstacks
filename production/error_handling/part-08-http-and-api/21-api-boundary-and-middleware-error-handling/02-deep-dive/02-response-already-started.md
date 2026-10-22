# The Response-Already-Started Problem

> Part VIII · Chapter 21 · Sections 21.10, 21.11 · _Estimated reading time: 18 min_
> **Prerequisite:** [Timeouts, Serialization, Streaming, and the Connection Lifecycle](../01-concepts/04-timeouts-streaming-and-connection-lifecycle.md)

## In one sentence

Once the response head is committed, the status code and headers are **immutable** — so an error
at that point cannot become a Problem Details document; the only honest responses are to signal
truncation (abort the connection) or, where the protocol allows, emit an in-band error frame.

## Why this matters in production

This is the single most-missed failure class in HTTP APIs because it is invisible in testing. Mock
responses are small and never fail mid-write; a real response can fail after the head is on the
wire. The naive handler tries `res.status(500).json(problem)` and either throws
`ERR_HTTP_HEADERS_SENT`, appends JSON onto an HTML/chunked body the client cannot parse, or
produces a `200` whose body is silently corrupt. Clients, seeing `200`, treat the truncation as
success. The result is the worst kind of bug: data corruption that looks like a healthy response.
The fix is a discipline — **detect the committed head, then log and abort** — plus protocol-aware
alternatives where they exist.

## Core concept — the commit boundary

A response passes through states:

```text
   idle ──set status/headers──▶ (buffered) ──flush head──▶ HEAD COMMITTED ──write body──▶ ended
                                    │                          │
                          can still change                cannot change:
                          status/headers/body             status, Content-Type, headers
```

| State | `headersSent` (Express) / `sent` (Fastify) | Can send a problem document? |
| ----- | ------------------------------------------ | ---------------------------- |
| Idle (nothing set) | `false` | Yes |
| Status/headers set but not flushed | usually `false` | Yes (may still change) |
| Head flushed (first byte written) | `true` | **No** |
| Body partially written | `true` | No |
| Ended | `true`, `writableEnded` | No |

The check is quick and exact; the hard part is remembering that **buffering frameworks may flush
the head earlier than you think** (large headers, streaming, `flushHeaders()` calls, or a proxy
that forwards eagerly).

## How it works — detection in each framework

```ts
// Express
if (res.headersSent) { /* Zone C */ }
if (res.writableEnded) { /* already finished */ }

// Koa
if (ctx.headerSent) { /* Zone C */ }

// Fastify
if (reply.sent) { /* Zone C */ }
if (reply.raw.destroyed) { /* socket gone */ }
```

`headersSent` becomes `true` the moment the first chunk is written — including when a streaming
API writes its first event, or when a framework flushes headers before a slow body.

## The recovery decision tree

```text
Error occurred.
   │
   ├─ head NOT committed?
   │     → buildProblem → sendProblem (status + problem+json + requestId)
   │
   └─ head committed?
         ├─ protocol has an in-band error channel (SSE)?
         │     → emit an error frame with { code, detail, retryAfterSeconds? }, then close
         ├─ response is a raw byte stream (CSV/file/chunked JSON)?
         │     → abort the connection so the client sees truncation
         └─ already ended?
               → log only; nothing can be sent
```

### Why "abort" and not "append"

Appending an error message to a partial body creates ambiguity the client cannot resolve:

- A partial JSON object plus `{"error":...}` is invalid JSON.
- A partial CSV plus an error line is a valid CSV with a bogus row.
- A partial HTML page plus JSON is neither.

Aborting (closing the socket without a clean end) gives clients a signal they already understand:
the transfer did not complete. With `Content-Length`, a short read is detectable; with chunked
encoding, a missing terminal chunk is detectable; SSE clients see the stream end without an
`event: done`.

### Protocol-aware alternatives

| Response type | Mid-stream error option | Client contract |
| ------------- | ----------------------- | --------------- |
| SSE (`text/event-stream`) | `event: error` frame, then close | Client handles `error` event (documented) |
| NDJSON stream | A line `{"error":{...}}`, document it | Client checks each line for `error` |
| Chunked JSON array | Abort | Truncated JSON is detectable |
| CSV / binary file | Abort, or write a trailing checksum only on success | Truncation detectable via checksum/terminator |
| HTTP trailers (`Trailer` header) | A trailer indicating failure | Rarely supported; do not make it the primary contract |

The SSE `event: error` frame is the only widely used case where an "error inside a `200`" is
legitimate — because the status was necessarily committed before the failure. Even then, the
`code` and `detail` are drawn from the same registry, so clients branch identically.

## How it works — preventing the situation

The best handling is to avoid committing the head before you know the outcome:

1. **Buffer small/medium responses.** Build the full document, then write. A failure during build
   leaves the head uncommitted and a normal problem document available.
2. **Pre-flight streams.** Before the first byte, verify auth, existence, permissions, and that
   the source opens. Only genuinely mid-stream failures remain.
3. **Order writes.** Write the head only after the first meaningful chunk is ready, so an early
   upstream error is still pre-commit.
4. **Use a deadline.** A stream with a deadline converts "stuck forever" into an abort.

```ts
// Build-then-write: failure before write keeps the head free.
try {
  const document = await buildExportDocument(id);  // may throw
  const body = JSON.stringify(document);           // may throw → caught below
  res.status(200).type("application/json").set("X-Request-Id", req.id).send(body);
} catch (err) {
  if (res.headersSent) { req.log.error({ err }, "post-commit failure"); res.destroy(); }
  else sendProblem(res, buildProblem(err, { instance: req.originalUrl, requestId: req.id }));
}
```

## Worked example — Checkout receipt stream

Acme streams a checkout receipt as SSE so the UI can render progress. Halfway through, the
payment provider returns a `503`.

```http
HTTP/1.1 200 OK
Content-Type: text/event-stream
Cache-Control: no-cache
X-Request-Id: req_ch9

event: step
data: {"step":"validating"}

event: step
data: {"step":"charging"}

event: error
data: {"code":"PAYMENT_PROVIDER_UNAVAILABLE","message":"Payment provider is temporarily unavailable.","retryAfterSeconds":10}
```

The `200` was committed at the first `step` event, so a `503` problem document is impossible. The
in-band `error` frame carries the registry `code` and retry hint, the client switches to its error
UI, and the stream closes. Contrast the `ExportJob` CSV download in the same service: it has no
in-band channel, so a mid-stream failure aborts the connection and the client detects truncation
via the success checksum.

## Key data / numbers

- **`ERR_HTTP_HEADERS_SENT`** is the Node error thrown when a second `writeHead`/status is
  attempted after the head is committed.
- **`res.headersSent`** (Express), **`ctx.headerSent`** (Koa), **`reply.sent`** (Fastify) — the
  detection flags.
- **`res.destroy()`** aborts the socket, signaling truncation; prefer it to a second write.
- **HTTP/2:** `RST_STREAM` cancels a single response stream; `GOAWAY` asks the peer to stop.
- **Chunked transfer:** a missing terminal `0\r\n\r\n` chunk is how clients detect truncation.
- **SSE:** define your `event: error` schema in the API docs; it is a convention, not a standard.

## Real-world use case — Acme SaaS partial-success stream

Acme's `AgentRun` streamed model tokens. When a provider rate limit occurred after a few tokens,
the original handler caught the error and called `res.status(429).json(problem)`. Node threw
`ERR_HTTP_HEADERS_SENT`, an unhandled-rejection log filled the dashboard, and the client saw the
truncated token stream as a successful run with a missing conclusion. The fix: check the committed
head, emit the documented `event: error` frame with `PROVIDER_RATE_LIMITED` and
`retryAfterSeconds`, then close. Client retries dropped into the correct path; the
`ERR_HTTP_HEADERS_SENT` class of log disappeared; and the bogus "successful run" reports stopped
entirely. No client code changed except to handle the already-documented error event.

## Trade-offs

| Mid-stream strategy | Pros | Cons | When to use |
| ------------------- | ---- | ---- | ----------- |
| Abort connection | Simple; universally detectable truncation | No error detail in-band | Raw byte streams |
| SSE `event: error` | Carries `code`/retry; client-actionable | Only for SSE; must be documented | Event streams |
| NDJSON error line | Carries detail | Client must inspect every line | Line-delimited streams |
| HTTP trailers | In-protocol | Poor client/proxy support | Rarely; never primary |
| Buffer whole response | Clean fallback; no partial body | Memory; no live streaming | Small/medium payloads |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Check the committed-head flag before responding | Attempt a second response after the head |
| Abort raw streams on mid-stream failure | Append an error object to a partial JSON body |
| Document an SSE `event: error` schema | Invent an ad hoc mid-stream error format |
| Pre-flight and buffer where feasible | Commit `200` before knowing the outcome |
| Log the true cause with `requestId` | Lose the cause because no body could be sent |
| Emit a metric for post-commit failures | Treat them as ordinary handled errors |

## Common mistakes

- **Assuming small responses never commit early.** A `flushHeaders()`, a big header block, or a
  proxy can commit before you expect it.
- **Catching the post-commit error and calling the normal error path.** It throws again
  (`ERR_HTTP_HEADERS_SENT`), often as an unhandled rejection.
- **Using `res.end(problemJson)` on a committed response.** It writes garbage after valid bytes.
- **No client contract for truncation.** Without a checksum or `Content-Length`, clients cannot
  tell a truncated body from a complete one.
- **Counting a post-commit failure as a server `5xx` metric.** There was no `5xx`; measure it as a
  stream/transmission failure.

## Checklist

- [ ] Every error path checks `headersSent`/`headerSent`/`sent` before responding.
- [ ] Post-commit failures log with `requestId` and abort the connection.
- [ ] Streaming endpoints define and document their mid-stream error behavior.
- [ ] Raw byte streams are verifiable (checksum/terminator/`Content-Length`) so truncation is
      detectable.
- [ ] Post-commit failures emit a distinct metric, not a `5xx` count.
- [ ] A test forces a serialization/stream failure after the head and asserts log-and-abort only.

## Related

- [Timeouts, Serialization, Streaming, and the Connection Lifecycle](../01-concepts/04-timeouts-streaming-and-connection-lifecycle.md)
- [Middleware Ordering Mechanics](./01-middleware-ordering-mechanics.md)
- [Global Handlers and the Request Boundary](../01-concepts/01-global-handlers-and-the-request-boundary.md)
- [Problem Details Mechanics and Versioning (Ch. 20)](../../20-standardized-api-error-responses/02-deep-dive/01-problem-details-mechanics-and-versioning.md)
