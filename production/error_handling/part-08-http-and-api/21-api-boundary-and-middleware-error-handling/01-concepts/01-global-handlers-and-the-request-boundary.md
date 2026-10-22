# Global Handlers and the Request Boundary

> Part VIII · Chapter 21 · Sections 21.1, 21.9, 21.10, 21.18 · _Estimated reading time: 18 min_
> **Prerequisite:** [Chapter 21 README](../README.md), [Error Shapes Across Scenarios (Ch. 20)](../../20-standardized-api-error-responses/03-practical-examples/02-error-shapes-across-scenarios.md)

## In one sentence

A **global error handler** is the outermost boundary of one request: it must catch every failure
that occurs **before the handler** (routing, parsing, auth), translate it into the Ch. 19/20
contract, and — when the failure happens **after headers are sent** — switch from "respond" to
"log and abort," because the status line can no longer change.

## Why this matters in production

Every request passes through a chain of code that can fail: the router, the body parser, auth
middleware, the handler, the serializer, and the socket itself. If the global handler misses one
of those segments, the framework's default error page ships to production — HTML where the
client expects `application/problem+json`. If it catches a failure that occurred *after* the
response head was committed, and tries to send a second JSON body, you get
`ERR_HTTP_HEADERS_SENT`, a corrupted response, and a client that cannot tell what happened.
The global handler is not "a nice place to put `console.error`"; it is the enforcement point
that makes every promise in Chapters 19 and 20 true.

## Core concept — a request has three failure zones

```text
   ┌─────────────────────── one request ────────────────────────┐
   │                                                             │
   │  ZONE A: before handler      ZONE B: in handler   ZONE C:   │
   │  routing, parsing, auth,     business logic,      response  │
   │  validation, rate limit      DB, providers        write     │
   │                                                             │
   │  status code still free  ◀── header not sent ──▶  head sent │
   └─────────────────────────────────────────────────────────────┘
                 can still respond          can only log/abort
```

| Zone | Examples (section) | Can set status? | Global handler action |
| ---- | ------------------ | --------------- | --------------------- |
| **A — before handler** | Parsing (21.2, 21.12), content type (21.13), size (21.14), auth/authz (21.3–21.4), rate limit (21.5), timeout before write (21.6) | Yes | Translate → problem document → respond |
| **B — inside handler** | Domain rules, DB errors, provider failures, serialization (21.7) | Yes | Translate → problem document → respond |
| **C — after headers sent** | Streaming/transmission failure (21.8, 21.11), write error, aborted client (21.15) | No | Log with `requestId`, abort/close, never re-write |

21.9 ("errors before the handler") and 21.10 ("errors after headers sent") are exactly this
split. Every design decision in this chapter follows from asking **"has the head been
committed yet?"**

## How the global handler is wired

A global handler has two jobs that are easy to conflate:

1. **Boundary job** — guarantee a response for any error in Zone A or B, in the correct contract
   shape, with the correct status, headers, and `requestId`.
2. **Liveness job** — survive Zone C failures, and additionally survive failures *inside the
   error handler itself* (a serialization throw, a second throw while building the problem).

```ts
// Express-style sketch: the error handler is registered LAST, after all routes.
app.use(router);
app.use(parseBody);
app.use(authenticate);

// ... routes ...

// Global boundary: 4 arguments in Express marks it as the error handler.
app.use((err: unknown, req: Request, res: Response, next: NextFunction) => {
  if (res.headersSent) {
    // Zone C: we cannot change the status or send a problem document.
    log.error({ err, requestId: req.id }, "error after headers sent");
    if (!res.writableEnded) res.destroy();  // abort rather than send a second body
    return;
  }
  const problem = buildProblem(err, {
    instance: req.originalUrl,
    requestId: req.id,
  });
  sendProblem(res, problem);   // sets status, Content-Type, headers, body
});
```

Three properties of this design:

- **It is registered last.** In Express, error-handling middleware must appear after the routes
  and middleware it needs to catch. "Last" is the ordering rule for this framework; see the
  deep-dive for the framework differences.
- **It reads `res.headersSent` before doing anything.** This single check decides between the
  respond path and the log-and-abort path. Forget it and you will attempt an impossible write
  under load.
- **It never trusts `err`.** `err` may be `undefined`, a string, a thrown `HttpError`, or an
  ORM object. `buildProblem` classifies by registry code, with an unknown-error fallback to the
  generic `INTERNAL_ERROR` document.

## 21.9 — Errors before the handler

The most common production leak: **parsing and auth fail before your route ever runs**, so the
handler that builds problem documents never executes. These errors arrive as *middleware
errors*, and they must land in the same global boundary.

| Failure | Producer | Status | Code |
| ------- | -------- | ------ | ---- |
| Malformed JSON body | body parser | `400` | `MALFORMED_JSON` |
| Body over size limit | body parser / size guard | `413` | `PAYLOAD_TOO_LARGE` |
| Unsupported request `Content-Type` | content-type guard | `415` | `UNSUPPORTED_MEDIA_TYPE` |
| Missing/invalid credentials | auth middleware | `401` | `UNAUTHENTICATED` / `TOKEN_EXPIRED` |
| Authenticated but not permitted | authz middleware | `403` | `INSUFFICIENT_ROLE` |
| Rate limit exceeded | rate-limit middleware | `429` | `RATE_LIMITED` |

The rule: **middleware translates or throws a typed error; it never writes the response body
itself.** When middleware writes responses directly, three things happen: the shape drifts from
the envelope, `requestId` is missing, and a later error handler cannot reconcile what was sent.

```ts
// ❌ Middleware responds itself — a second, inconsistent error shape.
function requireAuth(req, res, next) {
  if (!req.headers.authorization) {
    return res.status(401).json({ error: "no auth" });
  }
  next();
}

// ✅ Middleware throws a typed error; the boundary owns serialization.
function requireAuth(req, res, next) {
  if (!req.headers.authorization) {
    return next(new AuthError("TOKEN_MISSING"));  // registry: 401
  }
  next();
}
```

The nice property of `next(new AuthError(...))` is that it composes: whether auth, authz, or
rate limiting fails, exactly one global handler formats the response.

## 21.10 — Errors after headers sent

Once the status line and headers are on the wire, **the status code is immutable**. Any error
after that point is a Zone C failure. Common triggers:

- A stream fails midway (client disconnects, upstream provider stalls, disk read fails).
- A `write()` to a closed socket throws `EPIPE`/`ECONNRESET`.
- The serializer throws while streaming an already-started response.
- The client aborts while the handler is still producing data.

What the global handler may do in Zone C:

| Action | Allowed? | Notes |
| ------ | -------- | ----- |
| Change the status code | ❌ No | Already sent; impossible |
| Send a problem document | ❌ No | Would append bytes to a committed response |
| Append an error trailer | ⚠️ Sometimes | Some frameworks/HTTP support trailers; do not rely on it for the contract |
| Log with `requestId` and cause | ✅ Yes | The only reliable record of what happened |
| Abort/close the connection | ✅ Yes | Signals truncation instead of a plausible-looking partial body |
| Increment a failure metric | ✅ Yes | Feeds dashboards and alerts |

> ⚠️ **Hazard.** Appending a JSON error to an already-started `text/event-stream` or chunked
> response produces a stream the client cannot parse — a "successful" `200` that silently
> contains corruption. Detect the zone and abort instead.

The detection itself is one line; the discipline is remembering to check it everywhere.

## 21.18 — The catch-all boundary

The catch-all is the global handler understood as a **system-wide invariant**:

> For every request, either the handler produced a response, or the catch-all produced a
> contract-shaped error response, or the connection was deliberately aborted. There is no
> fourth outcome.

To make that true, the catch-all must:

- Be **outermost** — nothing that can throw executes outside it.
- Handle **unknown values**, not just `Error` instances.
- **Never throw while handling**. A throw inside the catch-all escapes to the framework default.
- **Normalize** framework-generated errors (a `404`-from-router, a `PayloadTooLargeError` from
  the parser) into registry codes.
- **Preserve `requestId`** so the log and the client response correlate.

```text
request
  │
  ├─ router ──────────▶ catch-all (404 METHOD/ROUTE normalized)
  ├─ parser ──────────▶ catch-all (400/413/415 normalized)
  ├─ auth/authz ──────▶ catch-all (401/403)
  ├─ rate limit ──────▶ catch-all (429 + Retry-After)
  ├─ handler ─────────▶ catch-all (domain/provider → registry)
  └─ serializer ──────▶ catch-all (or Zone C: log + abort)
```

## Worked example — three failures, one boundary

`POST /api/v1/checkout` receives three different bad requests.

```http
// 1. Zone A — malformed JSON
POST /api/v1/checkout HTTP/1.1
Content-Type: application/json

{ "cartId": "cart_1", "amount": 25
```

```http
HTTP/1.1 400 Bad Request
Content-Type: application/problem+json
X-Request-Id: req_a1

{
  "type": "/problems/malformed-request", "title": "Malformed Request",
  "status": 400, "detail": "The request body is not valid JSON.",
  "instance": "/api/v1/checkout", "code": "MALFORMED_JSON", "requestId": "req_a1"
}
```

```text
2. Zone B — provider unavailable, thrown by the handler
   → 503 + Retry-After: 10, code PAYMENT_PROVIDER_UNAVAILABLE

3. Zone C — client disconnects while the handler is streaming a receipt
   → no response possible; log  { requestId, cause: EPIPE }, destroy socket
```

Cases 1 and 2 are indistinguishable to the client from the outside: same envelope, same
handling path, same `Content-Type`. Case 3 produces no problem document — and that is correct,
because there is no longer a response to shape.

## Key data / numbers

- **Zone decision header:** `res.headersSent` (Express), `reply.sent` (Fastify),
  `res.writableEnded` — the check that separates 21.9 from 21.10.
- **Statuses owned by Zone A middleware:** `400`, `413`, `415`, `429` (`431` for oversized
  headers), `401`, `403`.
- **`Retry-After`** must accompany `429` and `503`.
- **`X-Request-Id`** should be set by the boundary if the edge did not already set it; the body
  `requestId` must equal it.
- **`431 Request Header Fields Too Large`** comes from the HTTP layer before your code runs — it
  may bypass the catch-all entirely, so test it at the proxy/gateway too.

## Real-world use case — Acme SaaS Checkout

Acme's checkout endpoint occasionally returned HTML error pages under a specific condition: the
client sent `Content-Type: application/json` with a trailing-comma body, the body parser threw
*before* the route ran, and the framework's default error renderer answered with an HTML page.
SDKs saw `200 OK`-shaped HTML, failed to parse, and reported a generic "server error." Adding a
catch-all that normalized parser exceptions into `MALFORMED_JSON` turned those failures into
proper `400` problem documents. The team then found a second leak: an upstream payment timeout
during response streaming returned `200` with a half-written JSON body. The boundary now checks
`headersSent`; on Zone C it logs the timeout and aborts, so clients see a truncated connection
(retryable) instead of a corrupt "success."

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| One global catch-all, middleware throws typed errors | Consistent shape; one place to change | Requires discipline not to respond early | Default |
| Each middleware responds directly | Self-contained | Shape drift, missing `requestId`, unmergeable | Never for public APIs |
| Framework default errors + per-route handling | Zero setup | HTML/raw errors leak; no contract | Prototypes only |
| Catch-all that also retries internally | Recovers transient Zone B errors | Hides failures; retry belongs in the domain | Almost never at the boundary |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Register the catch-all so nothing throws outside it | Let the framework's default error page render |
| Check `headersSent` before responding | Attempt a problem document after the head is sent |
| Normalize parser/router/framework errors into registry codes | Expose `SyntaxError` text or `PayloadTooLargeError` |
| Keep `requestId` consistent between body and `X-Request-Id` | Generate a new ID inside the catch-all |
| Log full cause server-side; send the projection client-side | Serialize the caught `Error` |
| Abort the connection on Zone C failures | Append an error body to a started stream |

## Common mistakes

- **Registering the catch-all before routes.** In frameworks where order defines scope, routes
  and middleware declared after it are not covered. It must be last/outermost.
- **A catch-all that throws.** Calling a serializer that can throw inside the handler, without
  a fallback, converts a handled error into the framework default page.
- **Assuming `err` is an `Error`.** `throw "bad"` and framework errors arrive as non-`Error`
  values; classify defensively.
- **Writing the response in middleware *and* the catch-all.** Double-write errors, truncated
  bodies, and logs that disagree with what the client saw.
- **Forgetting `431` and gateway-generated errors.** They can occur outside application code.

## Checklist

- [ ] The global handler is registered outermost/last and covers routes, parser, and auth.
- [ ] Middleware throws typed errors instead of writing responses.
- [ ] `headersSent` is checked; Zone C logs and aborts.
- [ ] Unknown and non-`Error` throws map to the generic `INTERNAL_ERROR` document.
- [ ] Framework/parser/router errors are normalized to registry codes.
- [ ] `requestId` is set once and appears in both the body and `X-Request-Id`.

## Related

- [Middleware Ordering Mechanics](../02-deep-dive/01-middleware-ordering-mechanics.md)
- [The Response-Already-Started Problem](../02-deep-dive/02-response-already-started.md)
- [Parsing, Malformed Requests, Content Types, and Payload Size](./02-parsing-and-malformed-requests.md)
- [The Error Envelope and RFC 9457 (Ch. 20)](../../20-standardized-api-error-responses/01-concepts/01-error-envelope-and-rfc-9457.md)
