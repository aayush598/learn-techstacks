# Parsing, Malformed Requests, Content Types, and Payload Size

> Part VIII · Chapter 21 · Sections 21.2, 21.12, 21.13, 21.14 · _Estimated reading time: 17 min_
> **Prerequisite:** [Global Handlers and the Request Boundary](./01-global-handlers-and-the-request-boundary.md)

## In one sentence

The four failures that happen **before your handler ever sees the body** — unparseable syntax
(21.2/21.12), unsupported `Content-Type` (21.13), oversized payloads (21.14) — are not
"validation" and must be classified at the edge as `400`, `415`, and `413`, using the Ch. 20
envelope, before any business logic runs.

## Why this matters in production

These errors are the easiest to get wrong because they originate inside your framework, not your
code. A body parser throws `SyntaxError`; a size guard throws `PayloadTooLargeError`; a missing
`Content-Type` produces `undefined` instead of an error. If those throw into the framework
default, clients get HTML; if they are misclassified, a broken encoder looks like a business
error and SDKs retry the wrong thing. Worse, deciding size or type *after* buffering the body
means an attacker can make you allocate memory before you reject them. Order matters as much as
classification here.

## Core concept — the edge, in order

```text
request bytes
   1. size check (Content-Length / streaming byte cap)   → 413 if exceeded
   2. Content-Type check (supported media type?)          → 415 if unsupported
   3. parse (JSON/schema)                                 → 400 if unparseable
   4. (hand off to route → schema/semantic validation)    → 422 in the handler layer
```

Steps 1 and 2 must precede step 3, and all three precede any authorization decision that
depends on the body. The natural mapping:

| Edge failure | Status | Code (example) | Produced by |
| ------------ | ------ | -------------- | ----------- |
| Body larger than limit | `413` | `PAYLOAD_TOO_LARGE` | size/body-limit middleware |
| Headers too large | `431` | `HEADERS_TOO_LARGE` | HTTP server / proxy |
| Unsupported `Content-Type` | `415` | `UNSUPPORTED_MEDIA_TYPE` | content-type guard |
| Missing `Content-Type` on a body-bearing method | `415` | `UNSUPPORTED_MEDIA_TYPE` | content-type guard |
| Unparseable JSON | `400` | `MALFORMED_JSON` | body parser |
| Wrong JSON shape / bad encoding | `400` | `MALFORMED_REQUEST` | body parser |
| Parseable but invalid values | `422` | `VALIDATION_FAILED` | validation layer (Ch. 17) |

Note the last two rows: `400` is the parser's verdict; `422` belongs to validation. Keeping that
line clean is what makes `400`-vs-`422` mean something to clients (Ch. 19 §19.2).

## 21.2 / 21.12 — Parsing failures and malformed requests

Parsing failures cover more than bad JSON:

- **Syntax errors** — trailing commas, unquoted keys, truncated bodies, raw bytes where JSON is
  expected.
- **Encoding errors** — invalid UTF-8, mismatched charset declarations.
- **Content-Length lies** — the declared length disagrees with the bytes received (often a
  truncated or slow-client problem).
- **Empty body** where a body is required — parseable as "empty," invalid as a request.
- **Wrong root type** — a JSON array or scalar where an object is required. This is structurally
  parseable but semantically wrong; classify it as `400` `MALFORMED_REQUEST` if it cannot even
  be interpreted as the endpoint's envelope, otherwise `422`.

Rules:

- **Never echo the parser's error verbatim.** `SyntaxError` messages include byte offsets and
  fragments of input; both are reflection and fuzzing aids. Say *"The request body is not valid
  JSON."* and log the detail with `requestId`.
- **Distinguish "unparseable" from "invalid."** The client's fix differs: a broken encoder (`400`)
  versus wrong values (`422`).
- **Bound parse work.** Deeply nested JSON and huge arrays can burn CPU; enforce a max depth or
  size before parsing.
- **Do not leak the parser library or version.** `body-parser` / `serde_json` names and versions
  are reconnaissance.

```http
POST /api/v1/projects HTTP/1.1
Content-Type: application/json

{ "name": "Apollo", "seats": 10,
```

```http
HTTP/1.1 400 Bad Request
Content-Type: application/problem+json
X-Request-Id: req_p42

{
  "type": "/problems/malformed-request", "title": "Malformed Request",
  "status": 400, "detail": "The request body is not valid JSON.",
  "instance": "/api/v1/projects", "code": "MALFORMED_JSON", "requestId": "req_p42"
}
```

## 21.13 — Unsupported content types

`Content-Type` describes how the **request body** is encoded; it is not the response format
(that is `Accept`, Ch. 20 §20.12). Rules:

- **Reject unsupported media types with `415`, before parsing.** Do not attempt to parse CSV as
  JSON and then complain about values.
- **Missing `Content-Type` on a body-bearing method is `415`**, not `400` — you cannot parse a
  representation whose type is undeclared. (`GET`/`DELETE` without a body are fine.)
- **Be liberal only where you mean to be.** Accepting `application/json; charset=utf-8` and
  `application/vnd.acme.v1+json` is reasonable; accepting `text/plain` "just in case" invites
  ambiguity.
- **Advertise what you accept.** `Accept-Post` (for write methods) and the documented API
  reference tell clients the allowed types; the `415` `detail` should name them.
- **`415` should not echo the offending type unescaped.** Truncate and escape; a fuzzer will
  otherwise use it as a reflection channel.

```http
POST /api/v1/webhooks/stripe HTTP/1.1
Content-Type: text/xml

<event/>
```

```http
HTTP/1.1 415 Unsupported Media Type
Content-Type: application/problem+json
Accept-Post: application/json
X-Request-Id: req_w7

{
  "type": "/problems/unsupported-media-type", "title": "Unsupported Media Type",
  "status": 415, "detail": "This endpoint accepts application/json only.",
  "instance": "/api/v1/webhooks/stripe", "code": "UNSUPPORTED_MEDIA_TYPE",
  "requestId": "req_w7"
}
```

## 21.14 — Oversized payloads

`413 Payload Too Large` is a **protective** response: reject before you allocate. There are two
distinct limits:

- **Buffered-body limit** — for JSON bodies you parse into memory. Enforce a byte cap
  (`Content-Length` first, then a streaming byte counter for chunked bodies).
- **Streaming/upload limit** — for file uploads (`ExportJob` inputs, media) that are streamed to
  storage. Use a multipart parser with a max size, or stream manually and abort when the cap is
  crossed.

Design points:

- **Check `Content-Length` first** when present; reject immediately without reading the body.
  When it is absent (chunked), count bytes as they arrive and abort at the cap.
- **Return `413` in the Ch. 20 envelope**, with the limit in `detail` (e.g. "maximum 1 MiB").
- **Set the same limit at the gateway/proxy** (Nginx `client_max_body_size`, ALB limits, etc.).
  The app limit should be `≤` the gateway limit so your `413` shape wins over a proxy default.
- **Oversized headers are `431`, not `413`.** That decision is made by the HTTP layer, often
  before your middleware.
- **Do not trust `Content-Length`.** A lying length is a classic framing attack; enforce a
  counted cap regardless.

```ts
// Size guard: reject on Content-Length, then enforce a counted cap during body read.
const MAX_JSON_BYTES = 1_048_576; // 1 MiB

function sizeGuard(limit: number) {
  return (req: Request, res: Response, next: NextFunction) => {
    const declared = Number(req.headers["content-length"] ?? "0");
    if (Number.isFinite(declared) && declared > limit) {
      return next(new PayloadTooLargeError());  // registry: 413
    }
    let seen = 0;
    req.on("data", (chunk: Buffer) => {
      seen += chunk.length;
      if (seen > limit) {
        req.destroy();                          // stop reading; do not buffer more
        next(new PayloadTooLargeError());
      }
    });
    next();
  };
}
```

The `req.destroy()` is deliberate: once the cap is crossed you stop consuming the body entirely,
so a hostile client cannot force unbounded memory use by streaming forever.

## How it works — the guard order, end to end

```text
1. Content-Length / counted cap   → 413 (reject without full read)
2. Content-Type allowlist          → 415
3. JSON parse (bounded depth)      → 400 (MALFORMED_JSON)
4. registry-driven 413/415/400     → sendProblem() → application/problem+json
5. route matches?                  → else 404 (or 405 + Allow if path exists)
6. schema/field validation         → 422 (validation layer)
```

Each guard throws or `next()`s a typed error; the catch-all from file 01 formats the response.
No guard writes a body directly.

## Worked example — ExportJob upload rejection

`POST /api/v1/exports` accepts a JSON definition up to 1 MiB. A client sends a 12 MiB body with
`Content-Type: application/json`.

```http
HTTP/1.1 413 Payload Too Large
Content-Type: application/problem+json
X-Request-Id: req_x9

{
  "type": "/problems/payload-too-large", "title": "Payload Too Large",
  "status": 413, "detail": "The request body exceeds the 1 MiB limit.",
  "instance": "/api/v1/exports", "code": "PAYLOAD_TOO_LARGE", "requestId": "req_x9"
}
```

The same client then sends the right size but `Content-Type: text/csv`: `415`. Then valid JSON
with a bad `seats` value: `422` with `errors[]`. Same endpoint, three edge-layer verdicts, one
envelope.

## Key data / numbers

- **Statuses:** `400` (unparseable), `413` (too large), `415` (unsupported media type), `431`
  (headers too large), `422` (semantically invalid — later layer).
- **`Accept-Post`** advertises accepted request media types for write methods.
- **Common default JSON body limit:** ~100 KB–1 MiB for API endpoints; uploads use higher,
  streamed limits. Pick per endpoint and document it.
- **`Content-Length`** is a hint, not a guarantee; always enforce a counted cap for chunked
  bodies.
- **Bounded parsing:** cap JSON depth (e.g. 32) and array sizes to prevent CPU-allocation abuse.

## Real-world use case — Acme SaaS uploads

Acme allowed `POST /api/v1/projects/{id}/assets` to accept uploads "up to whatever the proxy
allowed." When the proxy limit was raised for an unrelated migration, the app's in-memory JSON
parser began receiving 50 MB metadata bodies and one worker OOMed, taking down several tenants'
requests. The fix was a counted 1 MiB cap on JSON metadata (with `413` in the envelope) and a
separate streamed path for binary uploads with its own max size. The gateway limit was set to
match. After the change, oversized requests were rejected in the edge guard — before a single
large buffer was allocated — and the OOM class of incident disappeared from the on-call pager.

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| Reject on `Content-Length` first | Zero body read; cheapest | Useless for chunked/lying clients | Always, as the first check |
| Counted streaming cap | Safe against chunked/lying clients | Slightly more code | Required as a backstop |
| Buffered parse then validate size | Simplest code | Allocates before rejecting; DoS risk | Small, trusted clients only |
| Gateway-only limit | One place to configure | Proxy default body, wrong shape | Never alone; pair with app limit |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Check size before content type before parse | Parse first, then check the body size |
| Return `415` for missing/unsupported `Content-Type` | Coerce `text/plain` into JSON silently |
| Return `413` with the limit in `detail` | Return a bare framework error or HTML |
| Enforce a counted cap for chunked bodies | Trust `Content-Length` alone |
| Keep gateway and app limits aligned (gateway ≥ app) | Let the proxy's default page leak |
| Genericize parser messages | Echo `SyntaxError` offsets or input fragments |

## Common mistakes

- **Treating `413`/`415` as validation.** They are edge/transport verdicts; returning `422` for
  a too-large body confuses clients and buries the real cause.
- **Deciding auth before size/type.** An attacker without credentials should still be rejected
  cheaply; but note that authorization that *depends on the body* must run after parsing.
- **Missing `Content-Type` accepted as empty body.** A body-bearing method with no declared type
  must be `415`, not a silent empty object.
- **`431` uncounted.** Header-size limits live at the HTTP layer; test them at the gateway.
- **Reflecting the rejected media type.** Escape and truncate it, or omit it.

## Checklist

- [ ] Size guard runs first and rejects on `Content-Length` when present.
- [ ] A counted cap backstops chunked/lying bodies.
- [ ] `Content-Type` allowlist returns `415` before parsing.
- [ ] Parser errors map to `400` `MALFORMED_JSON`/`MALFORMED_REQUEST`, never echoed verbatim.
- [ ] Gateway and app size limits are documented and aligned.
- [ ] `413`/`415`/`400` all use the Ch. 20 envelope with `requestId`.

## Related

- [Global Handlers and the Request Boundary](./01-global-handlers-and-the-request-boundary.md)
- [Request Content Errors: 400, 413, 415, 422 (Ch. 19)](../../19-http-error-semantics/01-concepts/02-request-content-errors-400-413-415-422.md)
- [A Complete Middleware Chain](../03-practical-examples/01-a-complete-middleware-chain.md)
