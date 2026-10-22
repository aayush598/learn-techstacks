# Timeouts, Serialization, Streaming, and the Connection Lifecycle

> Part VIII · Chapter 21 · Sections 21.6, 21.7, 21.8, 21.11, 21.15 · _Estimated reading time: 18 min_
> **Prerequisite:** [Global Handlers and the Request Boundary](./01-global-handlers-and-the-request-boundary.md)

## In one sentence

Timeouts (21.6) bound how long the server will wait, serialization (21.7) turns a result into
bytes, streaming (21.8) sends bytes over time, transmission failures (21.11) can occur mid-write,
and aborted clients (21.15) mean the other end is gone — each has a different error path, and only
the first two happen **before** the response head is committed.

## Why this matters in production

Long-running endpoints — `ExportJob` generation, `AgentRun` streaming, bulk operations — are
where the "errors after headers sent" problem becomes routine rather than theoretical. A timeout
that fires after you have started streaming cannot become a `504`; the head is already `200`. A
client that disconnects mid-upload should not leave you writing to a dead socket or holding a
transaction open. Serialization can throw *after* work succeeded, wasting the operation. Getting
the lifecycle right is the difference between an honest, retryable failure and a corrupt
"success."

## Core concept — where the head is

```text
  [ request ]  [ work ]  [ serialize ]  [ write head + body ]  [ stream more ]
       │           │           │                  │                    │
       └── timeout ─┴─ timeout ─┘          HEAD COMMITTED        transmission
           → 504/503 possible              → Zone C: no status    → Zone C
```

Everything before the head commit can still produce any status. Everything after can only be
logged and aborted (file 01, §21.10).

| Section | Event | Before head? | Response path |
| ------- | ----- | ------------ | ------------- |
| 21.6 | Timeout | Usually yes | `504` (gateway) / `503`/`408`-class by policy |
| 21.7 | Serialization error | Yes | `500` generic (or a fallback document) |
| 21.8 | Streaming | Head committed at first chunk | Mid-stream failures → Zone C |
| 21.11 | Transmission failure | No | Log + abort |
| 21.15 | Client abort | No | Cancel work + release resources |

## 21.6 — Timeouts

A timeout is a decision that waiting longer is not worth it. Three distinct timeouts exist per
request, and they must be ordered:

| Timeout | Applies to | Typical owner | Response if it fires |
| ------- | ---------- | ------------- | -------------------- |
| **Connection/header timeout** | Time to receive request headers | HTTP server/proxy | `408 Request Timeout` or connection close |
| **Request/read timeout** | Time to receive the full body | Server/proxy | `408` / close |
| **Handler/operation deadline** | Time to produce a response | Application | `503` or `504` by policy |
| **Upstream timeout** | Time waiting on a dependency | Application | `504` (our upstream) → client sees `503`/`504` |

Rules:

- **Edge timeouts must be longer than app deadlines**, so the app's classified error (with the
  envelope) wins over the gateway's anonymous `504`. If the reverse holds, every slow path
  becomes a bodyless gateway error and your taxonomy disappears.
- **Enforce deadlines in the application**, not only at the proxy. A deadline lets you stop work,
  release resources, and return a contract response; a proxy timeout just severs the connection.
- **Decide `503` vs `504` on purpose.** `504` is "an upstream/gateway did not respond in time";
  `503` is "we are temporarily unable to handle." For a self-imposed handler deadline, `503` with
  `Retry-After` is often the more honest choice for the client.
- **Propagate deadlines.** A 5s client deadline should not spawn 30s downstream work; pass the
  remaining budget down (Part XI, Ch. 29).
- **Timeouts are not cancellations, but they should cancel.** When the deadline fires, abort the
  in-flight work so it stops consuming resources.

```ts
async function withDeadline<T>(ms: number, work: (signal: AbortSignal) => Promise<T>) {
  const ac = new AbortController();
  const t = setTimeout(() => ac.abort(), ms);
  try {
    return await work(ac.signal);
  } catch (err) {
    if (ac.signal.aborted) throw new ServiceUnavailableError("HANDLER_TIMEOUT");
    throw err;
  } finally {
    clearTimeout(t);
  }
}
```

## 21.7 — Serialization errors

Serialization (Ch. 20 §20.13) can fail in two places:

1. **Serializing the success result** — a `BigInt` amount, a circular object graph, a `Date`
   outside range. The work may have succeeded (e.g. the export was generated) but the response
   cannot be built.
2. **Serializing the error document** — the failure-prevention for this is a constant fallback
   (Ch. 20). It must not throw.

Handling:

- **A success-serialization failure is a `500`** — but be careful: if it happened after a side
  effect (payment captured, job enqueued), the error response is misleading. That is an
  **ambiguous outcome** class (Part XV): the client sees `500` but the operation may have
  succeeded. Prefer idempotency keys (Part XI, Ch. 28) so a retry is safe.
- **Never stream a success body incrementally if the serializer can throw late.** Build the
  document, serialize it, then write. This keeps a fallback possible.
- **Log the real cause** with `requestId`; the client still gets the generic `INTERNAL_ERROR`.

## 21.8 — Streaming responses

Streaming commits the head early, so it changes the rules:

| Pattern | Head commit | Mid-stream failure path |
| ------- | ----------- | ----------------------- |
| SSE (`text/event-stream`) — `AgentRun` tokens | At first event | Emit an in-band error event if the protocol allows, then close; else abort |
| Chunked JSON array | At first chunk | Cannot emit a problem document; abort the connection |
| File/CSV download — `ExportJob` result | At first byte | Abort; the partial file is corrupt |
| Multipart/HTTP2 push | At first part | Abort the stream |

Rules:

- **Pre-flight what you can before the head.** Auth, existence, permissions, and "can we even
  open the source" are checkable before the first byte. Fail *before* streaming whenever
  possible, so a clean `4xx`/`5xx` envelope is still available.
- **For SSE, design an in-band error event.** A `200 text/event-stream` cannot carry a problem
  document, but it can carry an `event: error` frame with a `code` the client understands. This
  is the one place a "protocol-level error inside a 200" is legitimate — because the HTTP status
  was necessarily committed.
- **For raw byte streams (CSV, files), there is no in-band error channel.** On mid-stream
  failure, abort; clients detect truncation (missing terminator, content-length mismatch) and
  retry.
- **Set a deadline for the whole stream**; an idle stream with no data and no timeout pins a
  connection forever.

## 21.11 — Transmission failures

A transmission failure is the write itself failing:

- `EPIPE` / `ECONNRESET` when writing to a socket the peer closed.
- `ERR_HTTP_HEADERS_SENT` when code attempts a second response.
- Partial write followed by a broken pipe.
- HTTP/2 `RST_STREAM` or a `GOAWAY` from the peer.

Handling: **log, stop writing, clean up.** There is nothing to send — the peer is gone. Do not
attempt a problem document; the status is committed and the connection is broken. Emit a metric
so this is visible (a spike in write failures often precedes a client-side problem or an
infrastructure issue).

## 21.15 — Aborted client connections

Clients abort (navigation, timeout, cancel button) all the time. The server must notice and stop:

- **Detect the abort** via the socket/request `close`/`aborted` events (Node: `req.on("close")`
  with `req.aborted` or `res.on("close")`), or an `AbortSignal`.
- **Cancel downstream work.** Propagate the abort to DB queries, provider calls, and the queue
  producer, so a cancelled `AgentRun` stops spending tokens and a cancelled `ExportJob` request
  stops reading rows.
- **Release resources in `finally`.** An aborted request must still close streams, return pooled
  connections, and roll back transactions (Part V, Ch. 14).
- **Do not log aborts as errors.** A user navigating away is normal; log at `info`/`debug` and
  distinguish it from a transmission failure.
- **Do not treat an abort as success.** The operation may have completed server-side or not; mark
  ambiguous outcomes explicitly (Part XV).

```ts
function trackAborts(req: Request, res: Response) {
  const ac = new AbortController();
  const onClose = () => {
    if (!res.writableEnded) {
      ac.abort();                       // propagate cancellation downstream
      log.info({ requestId: req.id }, "client aborted");
    }
  };
  res.on("close", onClose);
  return ac.signal;
}
```

## How it works — the lifecycle decision table

```text
Is the request complete and the result ready?
  yes → serialize (build fully) → write head+body
          write fails? → transmission failure → log + abort
  no  → deadline exceeded?
          yes, head not sent → 503/504 problem document
          yes, head sent     → abort stream
        client gone?
          yes → cancel work, release resources, log aborted
        stream event fails mid-way?
          yes → SSE: in-band error frame; else abort
```

## Worked example — AgentRun streaming

`POST /api/v1/agent/runs/stream` returns SSE tokens.

```http
HTTP/1.1 200 OK
Content-Type: text/event-stream
Cache-Control: no-cache
X-Request-Id: req_ag1

event: token
data: {"text":"The "}

event: token
data: {"text":"report "}

event: error
data: {"code":"PROVIDER_RATE_LIMITED","message":"Upstream model is rate limited.","retryAfterSeconds":15}
```

The `200` head was committed before the provider failed, so a `429` problem document is
impossible. The SSE `event: error` frame carries the same `code` and retry hint the client needs,
and the stream is then closed. A raw CSV export in the same chapter has no such channel: a
mid-stream failure aborts the connection, and the client treats the truncated file as a retryable
failure.

## Key data / numbers

- **Order:** edge/header timeout ≥ edge/body timeout > app handler deadline > upstream timeout.
  Inverting this erases your error taxonomy behind a gateway `504`.
- **`408 Request Timeout`** is commonly emitted by servers/proxies, not app code.
- **SSE media type:** `text/event-stream`; `event: error` is a convention, not a standard — define
  it in your API docs.
- **HTTP/2:** `RST_STREAM` cancels one stream; `GOAWAY` asks the peer to stop opening streams.
- **Idempotency keys** make retries after ambiguous/aborted outcomes safe (Ch. 28).
- **Common handler deadline:** 5–30s for interactive APIs; longer only for explicitly async
  operations that return `202` + a job handle.

## Real-world use case — Acme SaaS ExportJob

Acme's `ExportJob` download was a raw CSV stream. When generating a large export, a source read
failed mid-file and the connection was aborted; clients, seeing a `200`, saved a truncated CSV
and reported "missing rows" days later in support. The team pre-flighted what it could (existence,
permission, and "open the source"), and for the unavoidable mid-stream failure made partial files
detectable by writing a final checksum row only on success and aborting the connection on failure.
Clients now verify the checksum; a truncated export is a retryable failure, not silent data loss.
Interactive endpoints were also given an app deadline shorter than the gateway's, so a slow
handler returns a `503` envelope instead of a bodyless proxy `504`.

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| App deadline below edge timeout | Classified error with envelope | Must enforce in code | Default |
| Streaming with in-band error events (SSE) | Can report mid-stream errors | Only where protocol allows | Token/event streams |
| Buffered response then write | Clean fallback; no partial body | Higher memory; no live streaming | Small/medium bodies |
| Abort on client close, cancel downstream | Saves resources | Requires cancellation plumbing | All long operations |
| Log aborts as errors | Nothing missed | Alert fatigue | Never — log at info |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Set edge timeouts longer than app deadlines | Let the gateway `504` erase your envelope |
| Pre-flight auth/existence before streaming | Commit `200` then discover a `403`-class problem |
| Detect client aborts and cancel downstream work | Keep writing to a dead socket |
| Design an SSE error event if streaming | Attempt a problem document mid-stream |
| Release resources in `finally` on abort | Hold transactions/streams after the client left |
| Log aborts at info, transmission failures as errors | Treat navigation away as a server error |

## Common mistakes

- **Streaming a success body when the serializer can still throw.** Build-then-write unless you
  truly need streaming.
- **No deadline on long handlers.** A stuck provider call pins the request until the proxy cuts
  it, producing an anonymous failure.
- **Treating a client abort as a `500`.** It floods alerts with non-errors.
- **Assuming a `200` means the body completed.** For streams it means the head was sent.
- **Ignoring ambiguous outcomes.** A `500` after a successful side effect needs an idempotency key
  to be safely retried.

## Checklist

- [ ] Handler deadlines are set and shorter than edge timeouts.
- [ ] Timeout cancellation aborts downstream work.
- [ ] Success bodies are serialized fully before the head when feasible.
- [ ] Streaming endpoints document their mid-stream error behavior (SSE frame or abort).
- [ ] Aborted connections cancel work and release resources.
- [ ] Transmission failures are logged and metered, never re-written.

## Related

- [The Response-Already-Started Problem](../02-deep-dive/02-response-already-started.md)
- [Global Handlers and the Request Boundary](./01-global-handlers-and-the-request-boundary.md)
- [Timeouts, Circuit Breakers, and Bulkheads (Ch. 29)](../../../part-11-retry-and-resilience/29-timeouts-circuit-breakers-and-bulkheads/README.md)
