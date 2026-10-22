# Validation at the Trust Boundary — The Exact Pipeline

> Part VII · Chapter 17 · Sections 17.17–17.19, 17.21 · _Estimated reading time: 20 min_
> **Prerequisite:** [Trust Boundaries, Untrusted Clients, and the Validation Contract](../01-concepts/05-trust-boundaries-clients-and-contracts.md)

## In one sentence

The request pipeline is a **strictly ordered series of guards** — size, media type, authn, parse,
structure, schema, normalize — where each stage owns a distinct failure status and **nothing
downstream runs on input that failed upstream**.

## Why this matters in production

Order bugs here are expensive and quiet: a validator that runs on unverified webhook bytes is a
free CPU faucet; a `413` checked after full buffering is a memory faucet; a `422` emitted for
unparseable JSON trains clients to render empty error lists. Because this pipeline executes on
every request, a one-line ordering mistake multiplies across your entire traffic — and attackers
specifically target the stages you placed wrong.

## The canonical order

```text
           ┌────────────── client ──────────────┐
           ▼                                    ▲
  0. routing / method           405              │
  1. byte cap while reading     413  (abort read)│
  2. media type                 415              │
  3. authn / authz (of route)   401 / 403        │
  4. signature (webhooks only)  400              │
  5. parse (JSON/protobuf)      400              │
  6. complexity guards          400  (depth/keys)│
  7. structure + schema         422 + fields ────┘
  8. normalize (trim/case)  ──▶ re-run affected schema rules
  9. domain (Ch. 18)            409/403/402/422/…
```

Why this exact order:

| Ordering rule | Reason |
| ------------- | ------ |
| Byte cap **during** read, before parse | `Content-Length` can lie (chunked); buffering 2 GB to then say `413` already lost |
| Media type before parse | Parsing `text/html` as JSON wastes CPU and muddies error attribution |
| Authn before expensive validation | Unauthenticated floods must not reach the validator |
| Signature before parse/validate (webhooks) | Unauthenticated bytes get no schema discussion (17.17) |
| Complexity guards after parse, before schema | Depth/keys exist only post-parse; schema walk on a bomb is the amplification |
| Normalize **before** final schema verdict | `"  a@b.com "` should pass format checks after trim, not fail on raw bytes |

> ⚠️ **Hazard — normalize order.** Trim/case too early can mask structure defects; too late and
> users fail format checks on whitespace. Recommended: trim at parse-adjacent normalization, then
> run the full schema; document per-field normalization in the contract.

## Middleware decomposition

Each stage is middleware with **one job and one status code vocabulary** — this is what makes the
pipeline testable in isolation (full middleware treatment in
[Ch. 21](../../../part-08-http-and-api/21-api-boundary-and-middleware-error-handling/README.md)):

```ts
// Composition, not a god-handler: each layer emits only its own statuses.
export const validationPipeline = [
  methodGuard(["POST", "PUT", "PATCH"]),   // 405
  bodyCap(MAX_BYTES),                      // 413  (aborts the stream)
  mediaTypeGuard("application/json"),      // 415
  authenticate(),                          // 401
  parseJson(),                             // 400
  complexityGuard({ depth: 16, keys: 500 }),// 400
  // handler:
  //   validateSchema(dto)  → 422 + field errors
  //   domain call          → Ch. 18 statuses
];
```

**One stage, one owner.** If the JSON parser can return `422`, two stages now produce field
errors and your status policy forks. In code review, ask of every guard: *which status does this
emit, and does any other stage emit the same one?*

## Status attribution table

| Symptom the client sees | Wrong stage that caused it | Right fix |
| ----------------------- | -------------------------- | --------- |
| `422`, `errors: []` | Parser failure handled by the schema error builder | `400 MALFORMED_BODY` |
| `500` + stack on giant body | No byte cap | `413` with abort-on-cap |
| `415` returned as `400` | Media-type check folded into parse catch | Dedicated `415` guard |
| Validator CPU spike on garbage | Schema walking a depth-1000 bomb | Complexity guard before schema |
| Field errors on unsigned webhook | Validate before signature | Verify → parse → validate |
| `200` after truncating body at proxy | Silent clip instead of `413` | Enforce cap in *your* process |

## Oversized: the mechanics of a correct `413`

```python
async def read_body_capped(request, max_bytes: int) -> bytes:
    chunks, total = [], 0
    async for chunk in request.stream():        # stream, never request.body()
        total += len(chunk)
        if total > max_bytes:
            raise PayloadTooLarge(max_bytes)    # aborts connection; middleware → 413
        chunks.append(chunk)
    return b"".join(chunks)
```

Details that matter:

- **Abort, don't buffer-then-reject.** Node/Python/Go all offer streaming reads; use them.
- **`413` before auth?** No — after auth for user routes (avoid unauthenticated load), but the
  *absolute byte cap* can live in the server layer regardless of route.
- **Chunked transfer-encoding**: no `Content-Length` at all; only the streaming cap is reliable.
- **Do not retry the read.** `413` is terminal; a client may retry with a smaller body, but your
  side must not.

## Malformed: attribution without leakage

```json
{
  "type": "https://errors.acme.example/malformed-request",
  "title": "MALFORMED_BODY",
  "status": 400,
  "detail": "The request body is not valid JSON.",
  "instance": "/projects",
  "requestId": "req_91bb04"
}
```

Safe vs unsafe detail (17.21):

| ✅ Safe (`detail`) | ❌ Unsafe |
| ------------------ | -------- |
| "not valid JSON" | `Unexpected token } at position 812 (line 4 col 3)` |
| `requestId` for support | stack, file paths, framework version |
| the media type we accept (`application/json`) | internal parser name/version |

A parse position *can* be useful for developer APIs; if you include it, bound it and keep it out
of consumer-facing clients' default rendering. Decide once, centrally, in the parse middleware.

## Key data / numbers

- Statuses by stage: `405` method, `413` size, `415` media type, `401/403` auth, `400` parse and
  complexity, `422` schema.
- Recommended guard defaults (publish your own): JSON **≤ 100 KB**, depth **≤ 16**, keys
  **≤ 500**, bulk rows **≤ 1,000**.
- Webhook ingress: signature check precedes *all* parsing.
- Pipeline is **shared middleware**, not per-handler copies — one place to audit.

## Real-world use case — Acme SaaS

Acme's API gateway had a 5 MB global limit, but the API itself buffered the whole body before
schema validation. A burst of 2 MB garbage JSON bodies (valid size, pathological content: 50k
keys, depth 40) drove validator CPU to saturation — a self-inflicted error storm that no retry
policy could fix. The fix: per-route caps (100 KB for JSON APIs), a complexity guard emitting
`400 PAYLOAD_TOO_COMPLEX`, and auth ordering tightened so anonymous requests hit cheaper checks
first. p99 CPU per bad request fell by more than an order of magnitude, and the incident class
disappeared from the runbook.

## Trade-offs

| Approach | Pros | Cons | When to use |
|----------|------|------|-------------|
| Central pipeline middleware | One audit point, consistent statuses | Cross-cutting debug requires tracing | ✅ Default |
| Per-handler ad-hoc checks | Locally obvious | Order drift per handler, status forks | Never at scale |
| Gateway-only limits | Shields app entirely | App still needs its own caps (gateway can be bypassed internally) | Complementary, not sufficient |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Enforce byte caps while streaming | Read fully, then compare to a limit |
| Give each stage exclusive ownership of its status | Let two stages emit `422` |
| Verify signatures before parse on ingress | Return field errors pre-verification |
| Normalize then validate, documented | Trim inside scattered business methods |

## Common mistakes

- **Duplicate media-type handling** in nginx *and* the app with different results — attribute
  failures to one layer.
- **`bodyParser` default limits** (framework defaults like 100 KB in Express) left unexamined —
  know your actual number.
- **Complexity guard after schema** — too late; the schema walk already exploded.
- **Retry on `413`** server-side — terminal; fix the client payload instead.

## Checklist

- [ ] One documented stage order; each stage emits only its own statuses.
- [ ] Caps enforced during read; connection aborted on overflow.
- [ ] Signature → parse → validate on every untrusted ingress.
- [ ] Complexity guard before schema walk.
- [ ] Normalize-then-validate policy written down and applied uniformly.
- [ ] Malformed-body responses carry no parser internals.

## Related

- [Trust Boundaries, Untrusted Clients, and the Validation Contract](../01-concepts/05-trust-boundaries-clients-and-contracts.md)
- [Stable Codes, Dedup, and Localization](./03-stable-codes-dedup-and-localization.md)
- [Chapter 21 — API Boundary and Middleware Error Handling](../../../part-08-http-and-api/21-api-boundary-and-middleware-error-handling/README.md)
- [Chapter 57 — Error Handling Under Load](../../../part-22-design-decisions/57-error-handling-under-load-and-at-scale/README.md)
