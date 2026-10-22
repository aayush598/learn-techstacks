# Problem Detail Fields — type, title, detail, instance

> Part VIII · Chapter 20 · Sections 20.3, 20.4, 20.5, 20.6 · _Estimated reading time: 17 min_
> **Prerequisite:** [The Error Envelope and RFC 9457](./01-error-envelope-and-rfc-9457.md)

## In one sentence

RFC 9457's four descriptive members each answer a different question — **`type` "what kind?",
`title` "label?", `detail` "what exactly?", `instance` "which one?"** — and mixing their
roles is what makes envelopes unusable for machines or unsafe for humans.

## Why this matters in production

These fields are where API error design is won or lost. `type` is what SDKs and humans use to
look up documentation; if it changes per occurrence, documentation links break and caching
lies. `detail` is what support reads at 3 a.m.; if it contains stack fragments or unescaped
input, it becomes both a disclosure and a reflection risk. `instance` is how a support engineer
finds the request among millions; if it is absent or generic, every ticket starts with "can
you send a HAR file?" Precision in these four fields is the difference between an API that
**debugs itself** and one that requires a war room.

## Core concept — the four questions

| Field | Question it answers | Audience | Stability |
| ----- | ------------------- | -------- | --------- |
| `type` | What **class** of problem is this? | Machines, docs links, dashboards | **Identical** for every occurrence of the type |
| `title` | What short **label** does this class carry? | Humans scanning logs | **Identical** per type; not localized |
| `detail` | What happened in **this** instance? | Humans (support, logs); safe for end-user display if written well | **Varies** per occurrence |
| `instance` | **Which occurrence** was this? | Log/trace lookup, support | Varies per request; stable format |

### 20.3 — `type` identifiers

`type` is a **URI reference** that identifies the problem type. Design rules:

- **One `type` per problem type**, aligned 1:1 with your public error `code` families.
- **Prefer stable, version-independent identifiers.** `/problems/validation-error` survives
  API versioning; `https://api.acme.example/v2/problems/validation-error` couples the type to
  a version you'll eventually sunset.
- **Root-relative vs absolute:** both valid. Root-relative (`/problems/...`) avoids leaking
  hosts and is the recommended default; absolute URLs to your **public docs domain** are fine
  if you want browser-dereferenceable types.
- **`about:blank`** is the default when `type` is omitted — use it only for truly untyped
  problems (rare in a coded API).
- **Registry alignment:** the set of `type` values is enumerated and versioned alongside the
  error registry; adding one is a reviewed change, not string interpolation.

```text
/problems/validation-error      ← schema/field failures
/problems/malformed-request     ← unparseable syntax
/problems/unauthenticated       ← 401 family
/problems/forbidden             ← 403 family
/problems/not-found             ← 404 family
/problems/conflict              ← 409 family
/problems/rate-limited          ← 429
/problems/service-unavailable   ← 503
/problems/internal-error        ← 500 (untyped detail deliberately)
```

### 20.4 — `title` (and descriptions)

`title` is a **short human-readable summary of the problem type**, per RFC 9457 — the same
string for every occurrence. Rules:

- Fixed per `type`. If two responses of the same type have different `title`s, one is wrong.
- Sentence case, no trailing period clutter, no interpolation: `"Validation Failed"`, not
  `"Validation failed for seats=-4"`.
- **Not for end-user UI directly** — it's English-only and generic by design. UIs localize
  from `code`/`type` via message catalogs (Chapter 38).
- API docs may list `title` per type; treat it as documentation, not contract.

### 20.5 — `detail`

`detail` is **human-readable, instance-specific** explanation. Rules:

- Answers "what exactly happened here?" — name the field, the limit, the conflicting
  condition. One or two sentences.
- **Safe for a semi-technical user or support transcript**: no stack, no SQL, no hostnames,
  no vendor internals (Ch. 19 §19.18).
- **Escape and truncate** any reflected input (e.g. cap at 256 chars).
- Clients may display it as a fallback message — write it accordingly — but machine logic
  must use `code` + `errors[]`.
- For `500`, keep `detail` deliberately vague: `"An unexpected error occurred. Provide the
  requestId to support."` The precision lives in the log keyed by `requestId`.

### 20.6 — `instance`

`instance` **identifies this occurrence** — a URI reference to the specific request,
operation, or resource that produced the problem. Rules:

- Default: the request path (`/api/v1/checkout`) — useful but not unique per occurrence.
- Better: include a per-occurrence handle — the request/operation path *plus* `requestId` as
  an extension, or an operation URI (`/operations/op_123`) for async failures.
- For sub-request failures, RFC 9457 explicitly allows `instance` to point at the failing
  sub-operation (e.g. a specific batch item) — use that for bulk errors.
- Never point `instance` at internal-only URLs (admin endpoints, intranet hosts).

## How it works — one error, correctly distributed

```json
{
  "type": "/problems/rate-limited",
  "title": "Too Many Requests",
  "status": 429,
  "detail": "Export creation is limited to 5 per minute. Retry in 42 seconds.",
  "instance": "/api/v1/exports",
  "code": "RATE_LIMITED",
  "requestId": "req_s8",
  "retryAfterSeconds": 42
}
```

Distribution check: `type` stable ✓; `title` generic ✓; `detail` names the limit and the
action ✓; `instance` locates the endpoint ✓; `requestId` (extension) makes it unique ✓. The
next rate-limited request from anyone shares `type`/`title`/`status` and differs in
`detail`/`instance`/`requestId`.

Contrast — all four fields abused:

```json
{
  "type": "ERROR",                                  ← not an identifier
  "title": "Too Many Requests for key abc123",      ← instance data in title
  "detail": "limit hit",                            ← useless for support
  "instance": "none"                                ← no occurrence pointer
}
```

## Key data / numbers

- **RFC 9457 member semantics:** `type` = problem type identifier; `title` = short summary of
  the type; `detail` = instance-specific explanation; `instance` = occurrence identifier.
  `about:blank` = default type.
- **URI-reference forms allowed:** absolute URL, root-relative path, or fragment-only. Pick
  one convention; Acme uses root-relative `/problems/...`.
- **`detail` length budget:** 1–2 sentences; hard-cap reflections at ~256 chars.
- **Type namespace size discipline:** most SaaS APIs need **10–30** problem types; if you
  have 100+, you're encoding per-field conditions as types (put those in `errors[].code`
  instead).
- **`instance` + `requestId`:** `instance` locates the *what* (endpoint/operation);
  `requestId` uniquely identifies the *occurrence*. Both together close the support loop.

## Real-world use case — Acme SaaS

Support escalation: "customer says exports are broken." Early Acme envelopes had
`title: "Error"` and `detail: "rate limited"` for every 429, with no `instance` or
`requestId`. Triage required guessing which of five export endpoints was involved. After
adopting the field discipline above, the same ticket arrives with `detail` naming the limit,
`instance: /api/v1/exports`, and `requestId: req_s8` — one log grep, root cause found
(per-tenant limiter misconfigured to 5/min for an enterprise tenant on a rollout). The fix
took 20 minutes; the *classification* had previously taken a day.

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| Coarse types (~15) + rich `code`/`errors[]` | Simple docs; clients branch on `code` | Requires good registry | Default, recommended |
| Fine-grained types (one per code) | Precise dereferenceable docs | Type explosion; doc churn | Public developer platforms with heavy docs investment |
| `about:blank` + body codes only | Minimal RFC usage | Tooling can't classify by `type` | Quick internal APIs |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Freeze `type`/`title` per problem type | Interpolate IDs, fields, or amounts into either |
| Write instance-specific, safe `detail` | Put stack/SQL/vendor names in `detail` |
| Include `instance` + `requestId` on every problem | Return bodies support cannot locate in logs |
| Keep types coarse; push field detail to `errors[]` | Create a new `type` per validation rule |

## Common mistakes

- **Versioned `type` URIs.** `/v1/problems/...` forces a type migration at every major
  version; types should outlive versions.
- **`detail` as the only identifier.** Clients start substring-matching; one copy edit breaks
  production.
- **`instance` pointing to internal hosts.** `http://checkout-svc:8080/...` is topology
  disclosure.
- **Localizing `title` via `Accept-Language`.** Breaks "fixed per type" and confuses caches;
  localize client-side from `code`.

## Checklist

- [ ] Every problem type has a registry row with fixed `type` + `title`.
- [ ] `detail` names the specific field/limit/conflict, and is safe to show support.
- [ ] `instance` + `requestId` are always present.
- [ ] No dynamic values appear in `type` or `title`.
- [ ] Type count is coarse; field conditions live in `errors[]`.

## Related

- [App Codes, IDs, and Field Details](./03-app-codes-ids-and-field-details.md)
- [Problem Details Mechanics, Negotiation, and Contract Evolution](../02-deep-dive/01-problem-details-mechanics-and-versioning.md)
- [Error Shapes Across Scenarios](../03-practical-examples/02-error-shapes-across-scenarios.md)
