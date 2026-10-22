# The Error Envelope and RFC 9457

> Part VIII · Chapter 20 · Sections 20.1, 20.2 · _Estimated reading time: 16 min_
> **Prerequisite:** [Chapter 20 README](../README.md)

## In one sentence

An **error envelope** is the single structured shape every failure response uses, and RFC 9457
Problem Details is the internet standard for that shape — five defined members, one media
type (`application/problem+json`), and a deliberate extension point for your application
codes.

## Why this matters in production

Before RFC 9457 (which obsoletes RFC 7807), every team invented its own body: `{error:
"..."}`, `{errors: {field: msg}}`, bare strings, arrays, HTML. The cost shows up exactly when
systems meet: an SDK needs one parsing path per endpoint family; a gateway cannot classify
errors; a new hire learns five conventions. RFC 9457 fixes the *outer* shape once, across
organizations — and its media type means intermediaries can recognize "this is a problem"
without parsing your custom fields. Adopting it is not standardization theater; it deletes a
whole category of integration bugs.

## Core concept — the envelope

The envelope is the response's **envelope + letter**: status line and headers carry routing
and retry truth (Ch. 19); the body carries identity, human explanation, and extension data.

```text
HTTP/1.1 422 Unprocessable Content          ◀── status: class + retry semantics
Content-Type: application/problem+json      ◀── media type: "this is a problem document"
Retry-After: (if applicable)                ◀── headers: machine instructions
{                                           ◀── body: the Problem Details document
  "type":   "/problems/validation-error",   ◀── identity of the error TYPE
  "title":  "Validation Failed",            ◀── short human label (generic)
  "status": 422,                            ◀── numeric mirror of the status line
  "detail": "seats must be between 1…",     ◀── human, INSTANCE-specific explanation
  "instance": "/api/v1/checkout",           ◀── pointer to this occurrence
  "code":   "VALIDATION_FAILED",            ◀── your stable app code (extension)
  "requestId": "req_9b44c0d1",             ◀── support/trace handle (extension)
  "errors": [ … ]                           ◀── field details (extension)
}
```

RFC 9457's defined members and their contract:

| Member | Required by RFC 9457 | Type | Contract |
| ------ | -------------------- | ---- | -------- |
| `type` | No (defaults to `about:blank`) | URI reference | **Identifies the problem type.** Stable, documentable, machine-comparable |
| `title` | No | String | Short, human-readable, **same for every response of this type** |
| `status` | No | Number | The HTTP status code, duplicated in the body |
| `detail` | No | String | Human-readable, **specific to this occurrence** |
| `instance` | No | URI reference | Identifies this occurrence (often the request path) |

Extensions (your `code`, `errors`, `requestId`, …) are explicitly permitted by the RFC —
that is the designed growth path.

## How it works — what goes where

The classic failure is cramming instance data into `type`/`title` or identifiers into
`detail`. The rule:

- **`type` = what class of problem.** One canonical `type` URI per problem type. Reused
  verbatim across every occurrence. Clients may dereference it for docs.
- **`title` = the label for that class.** Fixed string per `type`. Not for end users to
  render verbatim (no i18n), not for logic (use `code`/`type`).
- **`detail` = what happened *here*.** One sentence, safe for a support-savvy user, unique
  to this instance: which field, which limit, which conflict.
- **`instance` = *where/which one* it happened.** The request path, an operation ID, a job
  URI — enough to find this occurrence in logs (with `requestId`).
- **`status` = redundant on purpose.** Body-only consumers (queued, logged, emailed) still
  know the class. Keep it exactly equal to the HTTP status line — mismatches are a classic
  bug class.

> ⚠️ **Hazard.** Setting `type` to `about:blank` for everything and stuffing the real
> identity into `detail` makes your API *technically* RFC-compliant and *practically*
> unusable: clients must string-match prose. `about:blank` is for "I have nothing better to
> say," not as a default for a coded API.

## Worked example — one problem, two audiences

```json
{
  "type": "/problems/validation-error",
  "title": "Validation Failed",
  "status": 422,
  "detail": "seats must be between 1 and 500 (received -4).",
  "instance": "/api/v1/checkout",
  "code": "VALIDATION_FAILED",
  "requestId": "req_9b44c0d1",
  "errors": [
    { "field": "seats", "code": "out_of_range",
      "message": "seats must be between 1 and 500." }
  ]
}
```

- **Machine reads:** `status: 422` → no retry; `code: VALIDATION_FAILED` → render field
  errors; `errors[0].field` → highlight the input.
- **Human reads:** `detail` for logs/support; `requestId` greps the trace.
- **One occurrence, one document.** A different bad body produces the same `type`/`title`,
  different `detail`/`errors`/`requestId`.

## Key data / numbers

- **RFC 9457** — "Problem Details for HTTP APIs" (obsoletes RFC 7807). Media type:
  **`application/problem+json`** (and `application/problem+xml` for XML APIs).
- **Default `type`:** `about:blank` when omitted — use it only when you truly have no
  specific type.
- **Five defined members**; any number of extension members; collisions avoided by
  reusing your namespace discipline (see file 03 of this chapter).
- **`status` must equal the HTTP status** when present. Mismatches are non-conformant usage.
- **Relative `type`/`instance` references are valid** (RFC 9457 allows URI references);
  absolute URLs are also fine. Pick one style per API and keep it (Acme: root-relative
  `/problems/...`).

## Real-world use case — Acme SaaS

Acme's API had four legacy error shapes (v0 string, v1 `{message}`, v2 `{error:{code}}`,
framework defaults). SDK maintenance consumed ~1.5 engineer-days per release just in error
parsing, and two production incidents were traced to a client that only checked shape v2 and
silently swallowed v0 errors. Adopting one RFC 9457 envelope — with `code` + `requestId` as
the only required extensions — collapsed SDK error handling to a single parser. The breaking
part was not the parser; it was documenting the `type` namespace. The team published
`/problems/*` as a stable contract, and support tickets that used to require reproducing with
a HAR file started resolving from `requestId` alone.

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| RFC 9457 + extensions | Standard, toolable, documented extension path | Slight learning curve | Default for new APIs |
| Custom `{code, message}` only | Minimal | No standard media type; every client reinvents | Internal prototypes |
| GraphQL-style `errors[]` top level | Natural for GraphQL | Not HTTP-native; REST clients confused | GraphQL servers (their own spec) |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Use `application/problem+json` on every 4xx/5xx | Use `text/html` or bare strings for API errors |
| Give each problem type one stable `type` URI | Reuse `about:blank` for coded errors |
| Keep `title` fixed per type; put instance facts in `detail` | Interpolate dynamic values into `title` |
| Mirror the status into `status` | Omit or mismatch `status` |
| Extend with documented members (`code`, `errors[]`, `requestId`) | Invent alternate top-level shapes per endpoint |

## Common mistakes

- **Dynamic `title`s.** `title: "seats must be between 1 and 500"` breaks the "label per
  type" contract and leaks instance data into a field caches/monitors may aggregate on.
- **`detail` used for machine logic.** Clients string-matching `detail` break on every copy
  change; branch on `code`.
- **Forgetting `Content-Type`.** Correct JSON body served as `application/json` — many
  clients accept it, but problem-aware tooling (and the RFC's contract) expects
  `application/problem+json` (see the deep-dive on negotiation).
- **Absolute URLs pointing at internal hosts.** `type: "http://internal-svc:8080/problems/x"`
  leaks topology; use root-relative or your public docs base.

## Checklist

- [ ] Every 4xx/5xx body is a Problem Details document with `application/problem+json`.
- [ ] Each problem type has one stable `type` and one fixed `title`.
- [ ] `status` always mirrors the HTTP status line.
- [ ] Extensions are documented in the public API reference.
- [ ] No endpoint uses a legacy alternate shape.

## Related

- [Problem Detail Fields: type, title, detail, instance](./02-problem-detail-fields.md)
- [Problem Details Mechanics, Negotiation, and Contract Evolution](../02-deep-dive/01-problem-details-mechanics-and-versioning.md)
- [The Problem Details Envelope in Code](../03-practical-examples/01-problem-details-envelope-in-code.md)
