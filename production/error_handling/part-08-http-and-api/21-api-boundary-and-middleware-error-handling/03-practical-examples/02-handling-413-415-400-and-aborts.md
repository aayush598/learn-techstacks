# Handling 413, 415, 400, and Client Aborts

> Part VIII · Chapter 21 · Sections 21.12–21.15 applied · _Estimated reading time: 19 min_
> **Prerequisite:** [Parsing, Malformed Requests, Content Types, and Payload Size](../01-concepts/02-parsing-and-malformed-requests.md)

## In one sentence

This walkthrough drives four edge failures — oversized payload (`413`), unsupported media type
(`415`), malformed request (`400`), and aborted client — through the same chain and shows the
exact response (or deliberate non-response) each produces.

## Why this matters in production

These four failures are the ones clients hit most often and the ones frameworks most often
mislabel: a parser `SyntaxError` becomes HTML, a size violation becomes a proxy error, an abort
becomes a false `500` alert. Treating them as first-class, contract-shaped outcomes — with tests
— removes a large fraction of "the API behaved weirdly" support tickets. The aborted-client case
is the inverse: the correct behavior is *no* response, and the discipline is to cancel work and
release resources instead of trying to answer a client that is gone.

## Core concept — four failures, one envelope (or none)

| Case | Produced by | Status | Code | Response |
| ---- | ----------- | ------ | ---- | -------- |
| Oversized payload | size guard | `413` | `PAYLOAD_TOO_LARGE` | Problem document |
| Unsupported media type | content-type guard | `415` | `UNSUPPORTED_MEDIA_TYPE` | Problem document |
| Malformed request | body parser | `400` | `MALFORMED_JSON` | Problem document |
| Aborted client | socket close | — | — | No document; cancel + log |

The first three are Zone A failures: they occur before the handler and before any head is
committed, so the boundary formats them normally. The fourth is Zone C by nature: there is no one
to answer.

## Case 1 — 413 Payload Too Large

Reject on `Content-Length` when present, then enforce a counted cap for chunked/lying clients.

```ts
function sizeGuard(limit: number) {
  return (req: Request, _res: Response, next: NextFunction) => {
    const declared = Number(req.headers["content-length"] ?? "0");
    if (Number.isFinite(declared) && declared > limit) {
      return next(new HttpError("PAYLOAD_TOO_LARGE", { limit }));
    }
    let seen = 0;
    req.on("data", (c: Buffer) => {
      seen += c.length;
      if (seen > limit) { req.destroy(); next(new HttpError("PAYLOAD_TOO_LARGE", { limit })); }
    });
    next();
  };
}
```

```http
POST /api/v1/exports HTTP/1.1
Content-Type: application/json
Content-Length: 12582912

HTTP/1.1 413 Payload Too Large
Content-Type: application/problem+json
X-Request-Id: req_413

{
  "type": "/problems/payload-too-large", "title": "Payload Too Large",
  "status": 413, "detail": "The request body exceeds the 1 MiB limit.",
  "instance": "/api/v1/exports", "code": "PAYLOAD_TOO_LARGE", "requestId": "req_413"
}
```

Make the app limit `≤` the gateway limit so this problem document wins over a proxy default. Test
both the `Content-Length` path and the counted path (send a chunked body with no length header).

## Case 2 — 415 Unsupported Media Type

Reject before parsing; a body-bearing method with no declared type is `415`, not `400`.

```ts
function contentTypeGuard() {
  const hasBody = (m?: string) => ["POST", "PUT", "PATCH"].includes(m ?? "");
  const allowed = new Set(["application/json", "application/vnd.acme.v1+json"]);
  return (req: Request, _res: Response, next: NextFunction) => {
    if (!hasBody(req.method)) return next();
    const ct = (req.headers["content-type"] ?? "").split(";")[0].trim().toLowerCase();
    if (!allowed.has(ct)) return next(new HttpError("UNSUPPORTED_MEDIA_TYPE"));
    next();
  };
}
```

```http
POST /api/v1/projects HTTP/1.1
Content-Type: text/csv

name,seats
Apollo,10

HTTP/1.1 415 Unsupported Media Type
Content-Type: application/problem+json
Accept-Post: application/json
X-Request-Id: req_415

{
  "type": "/problems/unsupported-media-type", "title": "Unsupported Media Type",
  "status": 415, "detail": "This endpoint accepts application/json only.",
  "instance": "/api/v1/projects", "code": "UNSUPPORTED_MEDIA_TYPE", "requestId": "req_415"
}
```

Do not parse first: rejecting after parsing means you attempted to interpret a representation you
already declared unsupported.

## Case 3 — 400 Malformed Request

Normalize any parser error to `MALFORMED_JSON`; never echo `SyntaxError` offsets or input
fragments.

```ts
function parseJson() {
  const parser = express.json({ limit: 1_048_576 });
  return (req: Request, res: Response, next: NextFunction) =>
    parser(req, res, (err: unknown) => (err ? next(new HttpError("MALFORMED_JSON")) : next()));
}
```

```http
POST /api/v1/projects HTTP/1.1
Content-Type: application/json

{ "name": "Apollo", "seats": 10,

HTTP/1.1 400 Bad Request
Content-Type: application/problem+json
X-Request-Id: req_400

{
  "type": "/problems/malformed-request", "title": "Malformed Request",
  "status": 400, "detail": "The request body is not valid JSON.",
  "instance": "/api/v1/projects", "code": "MALFORMED_JSON", "requestId": "req_400"
}
```

Bound parse work: cap JSON depth and array length before parsing, or reject in the guard, so a
deeply nested hostile body cannot burn CPU. A structurally valid body whose *values* are wrong is
`422` (`VALIDATION_FAILED`), not `400` — keep that line clean.

## Case 4 — Aborted client connection

The client disconnects (navigation, timeout, cancel). Detect it, cancel downstream work, release
resources, and log at info level — never send a response and never alert as an error.

```ts
function trackAbort(req: Request, res: Response) {
  const ac = new AbortController();
  res.on("close", () => {
    if (!res.writableEnded) {
      ac.abort();                                     // cancel DB/provider/queue work
      log.info({ requestId: (req as any).id }, "client aborted");
    }
  });
  return ac.signal;
}

router.post("/api/v1/agent/runs", wrap(async (req, res) => {
  const signal = trackAbort(req, res);
  const result = await agentRun(req.body, { signal });  // honors cancellation
  if (res.writableEnded) return;                         // client already gone
  res.status(200).json(result);
}));
```

Rules:

- **`finally`-release everything.** Aborted requests must still close streams and return pooled
  connections/transactions.
- **Cancel expensive work.** A cancelled `AgentRun` should stop spending tokens; a cancelled
  `ExportJob` create should stop reading rows.
- **Do not confuse abort with transmission failure.** Abort is client-initiated (info); a write
  failure to a live peer is server-side (error, metered).
- **Do not treat abort as success.** The operation's server-side outcome may be ambiguous; use
  idempotency keys so a later retry is safe.

```text
res.on("close") + !writableEnded  →  client abort  →  abort downstream, log info, release
write throws EPIPE/ECONNRESET     →  transmission  →  log error, meter, stop writing
```

## How it works — one test suite for all four

```text
test 413 declared  : POST with Content-Length over limit          → status 413, code PAYLOAD_TOO_LARGE
test 413 chunked   : POST chunked body over limit (no length)     → status 413 (counted cap)
test 415 wrong type: POST Content-Type: text/csv                  → status 415
test 415 missing   : POST with no Content-Type                    → status 415
test 400 syntax    : POST invalid JSON                            → status 400, code MALFORMED_JSON
test 422 semantic  : POST valid JSON, bad value                   → status 422, errors[]
test abort         : client disconnects mid-handler               → no response; work cancelled; log info
test both-headers  : each document matches golden fixture (minus requestId)
```

The golden fixtures come from Ch. 20's scenario set; running them against the chain is the
contract test.

## Worked example — WebhookIngest under mixed failures

`POST /api/v1/webhooks/stripe` receives three problem requests in a row:

1. A 3 MiB event body → `413 PAYLOAD_TOO_LARGE`; Stripe retries per its policy.
2. A body with `Content-Type: application/x-www-form-urlencoded` → `415`; the sender fixes the
   client.
3. A valid body whose JSON is truncated mid-stream because the sender aborted → the server sees
   `close` before the body completed; it cancels the pending signature verify, releases the read
   stream, logs `info` with `requestId`, and sends nothing.

In a later incident, the queue was briefly unavailable: the enqueue error propagated (not
swallowed) to the boundary, which returned `503` + `Retry-After`, and Stripe's retry delivered the
event once the queue recovered. No event was lost.

## Key data / numbers

- **`413`** — reject on `Content-Length` first; counted cap backstops chunked bodies. Common JSON
  limit 100 KB–1 MiB.
- **`415`** — missing or unsupported `Content-Type`; advertise `Accept-Post`.
- **`400`** — unparseable; `422` is for semantically invalid. Do not echo parser messages.
- **`431`** — oversized headers, emitted by the HTTP layer before your code; test at the gateway.
- **Abort detection:** `res.on("close")` + `!res.writableEnded`; `req.aborted` on older Node.
- **Cancellation:** `AbortController`/`AbortSignal` propagated to DB/provider/queue calls.

## Real-world use case — Acme SaaS upload hardening

Acme's asset endpoint accepted JSON metadata with no size cap, then parsed it in memory. A
misconfigured client sent 40 MB metadata; a worker OOMed and dropped several tenants' in-flight
requests. The team added `sizeGuard` (declared + counted), moved the binary upload to a streamed
path with its own cap, and added the four-case test suite. In the following quarter, oversized and
wrong-type requests were rejected at the edge with proper `413`/`415` documents, the OOM class
disappeared, and a new aborted-download path stopped logging `500`s for users who simply
navigated away — abort logs moved to `info`, and the "false 500" alert stopped firing.

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| Reject on `Content-Length` then count | Cheap; safe vs lying clients | Two code paths | Always |
| Counted streaming cap only | One path | Reads some bytes before rejecting | When length is often absent |
| Normalize parser errors in a guard | No parser text leaks | One adapter per parser | Default |
| Abort: cancel downstream via signal | Saves resources | Requires cancellation plumbing | Long/expensive work |
| Abort: let work finish, discard result | Simpler | Wastes resources/tokens | Trivial work only |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Return `413`/`415`/`400` in the envelope | Let the parser/framework answer |
| Check size and type before parsing | Parse then reject |
| Cancel downstream work on abort | Keep spending tokens/rows for a client that left |
| Log aborts at `info`, transmission failures at `error` | Alert on normal navigations-away |
| Release resources in `finally` on abort | Hold connections/transactions open |
| Keep `400` (syntax) and `422` (semantic) distinct | Collapse both into one code |

## Common mistakes

- **Echoing the parser error.** Byte offsets and input fragments help attackers, not clients.
- **`413` via proxy default.** A gateway page has the wrong shape; align limits so the app's
  document wins.
- **Missing `Content-Type` treated as empty body.** It is `415`.
- **Abort causing a `500`.** A closed socket during handling is not a server error.
- **No cancellation propagation.** The request is answered "gone" but downstream work continues
  to consume resources.

## Checklist

- [ ] `413` fires on declared length and on a counted cap.
- [ ] `415` fires for both missing and unsupported `Content-Type`, with `Accept-Post`.
- [ ] Parser errors normalize to `MALFORMED_JSON`; no parser text echoed.
- [ ] `400` vs `422` boundary is enforced.
- [ ] Aborts cancel downstream work, release resources, and log at `info`.
- [ ] Four-case (plus `422` and both-length) tests run against the golden fixtures.

## Related

- [A Complete Middleware Chain](./01-a-complete-middleware-chain.md)
- [Parsing, Malformed Requests, Content Types, and Payload Size](../01-concepts/02-parsing-and-malformed-requests.md)
- [Request Content Errors: 400, 413, 415, 422 (Ch. 19)](../../19-http-error-semantics/01-concepts/02-request-content-errors-400-413-415-422.md)
