# Problem Details Mechanics, Negotiation, and Contract Evolution

> Part VIII · Chapter 20 · Sections 20.12, 20.13, 20.18, 20.19, 20.20 · _Estimated reading time: 20 min_
> **Prerequisite:** [Consistency and Information Safety](../01-concepts/05-consistency-and-information-safety.md)

## In one sentence

A Problem Details document becomes a contract only when you control **the bytes you emit, how
you negotiate them, and how they are allowed to change** — serialization, content negotiation,
response versioning, generated-SDK tolerance, and third-party publication are the mechanics
behind the envelope.

## Why this matters in production

The envelope design is necessary but not sufficient. Four mechanical failures ship regularly:

- **Serialization throws while serializing an error.** A `BigInt` amount or a circular `cause`
  makes `JSON.stringify` throw inside the catch-all, so the client gets a reset connection
  instead of a `500` problem document.
- **Negotiation changes the error shape.** A client sends `Accept: application/json`; the
  framework falls back to an HTML error page or a bare `{message}` object.
- **Versioning renames a member.** `detail` becomes `message` in v2; older SDKs throw a
  `TypeError` while handling the error, turning a handled `409` into a crash.
- **Third-party documentation drifts.** An integrator codes against an example that no longer
  matches production, and every support ticket starts with "which shape is real?"

Each is cheap to prevent at the boundary, expensive to diagnose in production.

## Core concept — the error wire pipeline

```text
internal error
  → 1. classify + project   registry: internal → public code, status, type, title
  → 2. build PublicProblem  plain object; no Error, stack, or SQL
  → 3. negotiate            errors always use application/problem+json
  → 4. serialize            JSON.stringify; may still fail, so have a fallback
  → 5. commit head          status + Content-Type + requestId (+ Retry-After)
  → 6. write body           once; never a second error document on this response
```

Skipping a stage produces a predictable failure: leaked internals, a wrong `Content-Type`, a
throw during error handling, a status/body mismatch, or a double write. Serialization is not
"call `res.json()`" — it is a set of guarantees for every error path.

## 20.13 — Serialization mechanics

- **Serialize a plain public object, not an `Error`.** `Error` properties (`message`, `stack`,
  `cause`) are non-enumerable in V8, but libraries attach enumerable fields and `toJSON`
  overrides can expose them. The boundary must receive `PublicProblem`.
- **Use UTF-8 JSON; member order is not semantic.** No `charset` needed on
  `application/problem+json`. Keep a stable order for readable diffs, and **mirror the status as
  an integer** — a mismatch with the status line is a contract bug no client can reconcile.
- **Omit absent optional members.** `"errors": null` is harder for generated clients than a
  missing key; reserve `null` for members whose schema allows it.
- **Never emit values JSON cannot represent.** `NaN`, `Infinity`, `BigInt`, `undefined` in
  arrays, and circular references either become `null` or throw. Normalize money to integer minor
  units or strings first.
- **Bound the body.** Cap `detail` (~256 chars) and `errors[]` (~20 entries), and build the
  whole document before the first write so a failure can fall back cleanly.

```ts
// A serialization boundary that cannot throw its way out of an error response.
export function serializeProblem(problem: PublicProblem): string {
  try {
    return JSON.stringify(problem);
  } catch {
    // Constant fallback: no values derived from the hostile error object.
    const { instance, requestId } = problem;
    return JSON.stringify({
      type: "/problems/internal-error", title: "Internal Server Error", status: 500,
      detail: "An unexpected error occurred. Provide the requestId to support.",
      instance, code: "INTERNAL_ERROR", requestId,
    });
  }
}
```

The fallback is built from primitives only; with `requestId` a string from generation, it cannot
fail on hostile data.

## 20.12 — Content negotiation

Two headers are routinely confused:

| Header | Direction | Governs | Wrong value produces |
| ------ | --------- | ------- | -------------------- |
| `Content-Type` | Request | How to parse the request body | `415 Unsupported Media Type` |
| `Accept` | Request | Which response representation the client prefers | `406 Not Acceptable` (if truly unrepresentable) |

`Accept` is a weighted list (`application/json, application/problem+json;q=0.9, */*;q=0.1`); `q`
is preference, not permission, and `q=0` means "not acceptable."

**Recommended policy: error responses are always `application/problem+json`.** Errors are not a
place to negotiate shapes. A client that asked for JSON still gets a problem document; a client
that asked for `text/html` still gets a problem document, because an HTML error page is not a
usable API response. Document this explicitly so nobody "fixes" it later.

Consequences of that policy:

- **Never switch between `{message}` and Problem Details based on `Accept`.** One request path,
  one error shape.
- **Support `application/problem+xml` only with real end-to-end XML support.** Half-XML doubles
  the serializer and the leak surface for near-zero demand.
- **`Vary: Accept` belongs on success responses whose representation varies**, not on error
  responses that never vary.
- **A `406` is still an error.** If success negotiation fails, return a problem document with
  `type: /problems/not-acceptable`, `status: 406`, and a `detail` listing supported types.
- **Request `Content-Type` handles 415 (§21.13).** Media-type verdicts happen before parsing.

## 20.18 — Versioning the response

Version the **API**, not the **error envelope**. The envelope is infrastructure shared by every
endpoint; versioning it multiplies the combinations clients must support.

| Change | Compatible? | Why |
| ------ | ----------- | --- |
| Add an optional member or a new `code`/`type` | ✅ Yes | Old clients ignore unknown keys and default on new codes |
| Rename `detail` → `message` | ❌ No | Old clients read `detail`; new clients read `message` |
| Remove `requestId` | ❌ No | Support and clients lose the trace handle |
| Change a member's type or an existing code's status | ❌ No | Deserializers and retry/UX logic silently shift |
| Make an optional member required | ❌ No | Old producers do not send it |
| Put a version in `type` (`/v2/problems/...`) | ❌ No | Every version forces a type migration |

Rules that keep the envelope stable:

1. **Additive-only within a major API version.** New optional members and codes are fine;
   renames, removals, and semantic changes are not.
2. **`type` and `title` are version-independent.** `/problems/validation-error` should outlive
   `/api/v1` and `/api/v2`.
3. **Deprecate codes, do not mutate them.** Keep emitting the old code until the announced
   sunset, publish the replacement, and signal timing with `Deprecation` and `Sunset` (RFC 8594)
   headers.
4. **Dual-emit during a rename.** Emit old and new members for one deprecation window; remove
   the old only in a major version, updating docs and changelog with the code.

A media-type parameter such as `profile` (RFC 6906) identifies a documented profile of Problem
Details, but it is not a version negotiation mechanism.

## 20.19 — Generated-SDK compatibility

Generated clients amplify small schema choices into crashes. Design the published error schema
for **tolerance**:

- **Open the object.** `additionalProperties: true` so new optional members do not fail strict
  deserializers.
- **Do not generate closed enums for `code`.** Publish `code` as a string with a documented
  catalog, or generate an open enum with an `unknown` variant.
- **Keep the required members small and stable.** Requiring `code` and `requestId` is
  reasonable; a long required extension list makes every future addition breaking.
- **Preserve the raw body on unknown errors.** An SDK that discards an unrecognized payload
  cannot help its user debug.
- **Test regeneration.** One contract fixture per public code plus one unknown code and one
  unknown member catches schema changes that only affect generated code.

```ts
// Tolerant SDK error mapping: known code first, unknown last.
type SdkError =
  | { kind: "rate_limited"; retryAfterSeconds: number }
  | { kind: "validation"; fields: FieldError[] }
  | { kind: "unknown"; status: number; code?: string; raw: unknown };

function toSdkError(status: number, body: unknown): SdkError {
  const p = body as Partial<PublicProblem>;
  if (p.code === "RATE_LIMITED") {
    return { kind: "rate_limited", retryAfterSeconds: p.retryAfterSeconds ?? 30 };
  }
  if (p.code === "VALIDATION_FAILED" && Array.isArray(p.errors)) {
    return { kind: "validation", fields: p.errors };
  }
  return { kind: "unknown", status, code: p.code, raw: body }; // never throw here
}
```

The `unknown` branch is the compatibility contract; it must not assume the body is a string.

## 20.20 — Contracts for third parties

When external integrators depend on your errors, the envelope stops being an implementation
detail and becomes a published product surface. Publish:

- **A problem catalog:** `type`, `title`, `code`, HTTP status, retryability, client action, and
  deprecation state.
- **The stability promise:** guaranteed vs optional members and the additive-only rule.
- **A support path:** `requestId` in the body and `X-Request-Id` header, plus a contact page.
- **Examples for high-traffic cases** (`400`, `401`, `403`, `404`, `409`, `422`, `429`, `500`,
  `503`) generated from the same contract fixtures used in CI.
- **The schema:** OpenAPI/JSON Schema with `additionalProperties: true` and an open code type.
- **A change log and deprecation policy:** notice period, headers, and what old clients see.

The catalog answers what integrators ask: which codes to handle, whether fields will be renamed,
how to report a failure (`requestId`), what is retryable (`429`/`503` + `Retry-After`), and what
is stable (members and codes, not `detail` prose).

For inbound webhooks (`WebhookIngest`), the same envelope applies to your responses, but
providers often care only about the 2xx/non-2xx distinction. Send a problem document for your
operators and reject invalid signatures with `400`; do not rely on the provider parsing it.

## Worked example — adding a retry hint without breaking SDKs

Acme `Checkout` returns `PAYMENT_PROVIDER_UNAVAILABLE` as `503`. Version 2 adds two optional
members: `retryAfterSeconds` (mirroring the header) and `declineCode` (a provider-neutral
reason). Nothing is renamed or removed.

```json
{
  "type": "/problems/service-unavailable",
  "title": "Service Unavailable",
  "status": 503,
  "detail": "The payment provider is temporarily unreachable.",
  "instance": "/api/v1/checkout",
  "code": "PAYMENT_PROVIDER_UNAVAILABLE",
  "requestId": "req_c81f",
  "retryAfterSeconds": 10,
  "declineCode": "provider_timeout"
}
```

- **Old SDK:** reads `status`, `code`, `requestId`; ignores the two unknown members.
- **New SDK:** uses `retryAfterSeconds` instead of parsing prose, and maps `declineCode`.
- **Third-party integrator:** sees the same `type`, `title`, `status`, `code`; only optional
  members were added, which the published policy permits.

What would have broken clients: renaming `detail` to `message`, turning `code` into a closed
enum, making `declineCode` required, or returning `200` with an error body for "already
captured."

## Key data / numbers

- **RFC 9457** defines Problem Details; media type **`application/problem+json`** (plus
  `application/problem+xml` with full XML support). It obsoletes RFC 7807.
- **Five standard members:** `type`, `title`, `status`, `detail`, `instance`, plus extensions;
  `about:blank` is the default `type` when omitted (do not use it for a coded API).
- **Content negotiation:** RFC 9110 defines `Accept`, quality values, and `406 Not Acceptable`.
  `Vary: Accept` belongs only on representations that vary.
- **`Sunset`** is standardized by RFC 8594; use it with a documented deprecation window.
- **Common limits:** `detail` ~256 chars, `errors[]` first 20 entries, `requestId` opaque and
  non-sequential. `Retry-After` on `429`/`503`; `500` is report-only, not a hot retry.

## Real-world use case — Acme SaaS and a billing integrator

Acme's public error docs were hand-generated from a wiki page. A billing integrator built
against a `422` example showing `errors[].field`; production had already renamed the member to
`fieldPath`, so every invalid invoice payload crashed the integrator's parser and the retry loop
caused a small traffic spike. The fix was not a new endpoint: Acme restored `field`, added
`fieldPath` as an optional alias for one deprecation window, published the catalog and schema
from the contract tests, and added a generated-SDK fixture that fails CI when a documented
member disappears. The next addition — an optional `retryAfterSeconds` — required no client
change.

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| Always problem JSON for errors, ignore `Accept` | One error shape; predictable | Technically ignores a preference | Default for JSON APIs |
| Negotiate problem JSON and problem XML | Standards-complete | Two serializers, two leak surfaces | Only with real XML clients |
| Additive-only envelope within a major version | Old clients keep working | Occasional dual-emit during deprecations | Any public API |
| Version the envelope media type | Explicit break boundary | Multiplies client combinations | Almost never |
| Closed code enum in generated SDKs | Exhaustive switches | Every new code is a breaking release | Never for a growing registry |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Serialize a typed public object; fall back to a constant 500 document | Let `JSON.stringify` throw inside the catch-all |
| Always send `application/problem+json` for errors | Switch to HTML or `{message}` based on `Accept` |
| Add optional members and new codes; keep old ones | Rename or remove members within a major version |
| Publish an open schema and tolerant SDK mapping | Generate closed enums for a growing code set |
| Publish the problem catalog, examples, and deprecation policy | Let third-party docs drift from fixtures |
| Keep `type` and `title` version-independent | Put `/v2/` in problem type URIs |

## Common mistakes

- **Serializing the caught error after mutating it.** Adding `err.requestId` then calling
  `res.json(err)` can still expose enumerable ORM fields. Project first.
- **Using `Accept` to select the error shape.** Consistency beats negotiation.
- **Adding a required extension.** It looks additive but breaks old producers and strict
  consumers.
- **Documenting codes without an `unknown` branch.** The first new code becomes a downstream
  incident.
- **Forgetting `Content-Type` on hand-built responses.** `res.status(500).send(json)` may emit
  `text/html` or `text/plain` depending on the framework.
- **Treating `Deprecation`/`Sunset` as a compatibility substitute.** Headers announce a change;
  they do not make a renamed field parse.

## Checklist

- [ ] Error bodies are serialized from a `PublicProblem`, never from `Error`, with a constant
      fallback that cannot fail on hostile data.
- [ ] Every error sets `Content-Type: application/problem+json`; `Accept` never changes the shape.
- [ ] Envelope changes are additive; renames/removals wait for a major version.
- [ ] The published schema allows unknown members and unknown `code` values.
- [ ] SDK fixtures cover a known code, an unknown code, and an unknown member; the catalog and
      examples are generated from contract tests.

## Related

- [Consistency and Information Safety](../01-concepts/05-consistency-and-information-safety.md)
- [The Problem Details Envelope in Code](../03-practical-examples/01-problem-details-envelope-in-code.md)
- [Error Shapes Across Scenarios](../03-practical-examples/02-error-shapes-across-scenarios.md)
- [Middleware Ordering Mechanics (Ch. 21)](../../21-api-boundary-and-middleware-error-handling/02-deep-dive/01-middleware-ordering-mechanics.md)
