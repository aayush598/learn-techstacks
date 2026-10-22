# App Codes, Field Details, and Request IDs

> Part VIII · Chapter 20 · Sections 20.7, 20.8, 20.9 · _Estimated reading time: 18 min_
> **Prerequisite:** [Problem Detail Fields](./02-problem-detail-fields.md)

## In one sentence

RFC 9457 gives you the *shape*; your **stable `code`** gives clients something to branch on,
**`errors[]`** localizes validation failures to fields, and the **`requestId`** ties every
response to a trace — the three extensions that turn a standard document into an operable
API contract.

## Why this matters in production

`type` and `detail` are not enough for real clients. UI code needs `if (code ===
'INSUFFICIENT_ROLE') showUpgradeDialog()` — not substring matching on prose that product
writers will edit next quarter. A form needs to know *which* of eleven fields is wrong, not
that "one or more fields are invalid." And support needs a single opaque string that finds the
exact request in logs across services. Without these three extensions, SDKs grow per-endpoint
parsers, forms re-validate blindly, and support tickets become archaeology.

## Core concept — the three load-bearing extensions

### 20.7 — Application codes (`code`)

`code` is your **stable, machine-readable identifier** for the specific error condition —
the public projection of the error registry (Chapter 8). Rules:

- **Stable forever** (until a versioned deprecation): the value is contract; the prose is not.
- **SCREAMING_SNAKE_CASE**, domain-scoped where helpful: `VALIDATION_FAILED`,
  `INSUFFICIENT_ROLE`, `SLUG_TAKEN`, `RATE_LIMITED`.
- **Public codes only.** Internal codes (`DB_DEADLOCK`, `STRIPE_SDK_TIMEOUT`) are projected
  through the registry's public alias (`SERVICE_UNAVAILABLE`) before serialization — clients
  never learn your internals (§20.17).
- **One-to-one with `type`? No — many-to-one.** Multiple codes may share a coarse `type`
  (`/problems/validation-error` ← `VALIDATION_FAILED`, `INVALID_ENUM_VALUE`…). Clients branch
  on `code`; tooling classifies by `type`.
- Documented in the public API reference, generated from the registry so docs can't drift.

### 20.8 — Field-level details (`errors[]`)

When validation fails on specific fields, a single `detail` sentence is not actionable.
`errors[]` is the conventional extension member (some APIs call it `issues` or `validationErrors`
— pick one and keep it):

```json
"errors": [
  { "field": "seats",     "code": "out_of_range",
    "message": "seats must be between 1 and 500." },
  { "field": "startDate", "code": "cross_field",
    "message": "startDate must be before endDate." }
]
```

Design rules:

- **`field`** is a **dotted path** into the request body (`items[0].qty`, `owner.email`) —
  not a database column name.
- **`code` per field** is a small closed vocabulary (`required`, `type_mismatch`,
  `out_of_range`, `format_invalid`, `cross_field`) — extend deliberately, document each.
- **`message`** is human, localized-able client-side from `code` (send English default;
  clients may map to i18n catalogs).
- **Cross-field failures** attach to the *most relevant* field and use `cross_field`; the
  message names the other field(s).
- **Never leak schema beyond the contract**: `field` names are request-shape names; internal
  column names are not.
- **Bound the array** (e.g. first 20 entries + a truncation note) to keep hostile inputs
  from generating megabyte responses.

### 20.9 — Request IDs and support references

`requestId` (some APIs use `correlationId` or `traceId`; pick one name for the HTTP surface)
is the **opaque handle that ties one response to one trace**:

- Generated at the edge or app boundary **per request**; echoed in the body and (optionally)
  in an `X-Request-Id` response header for curl users.
- Must propagate into logs, traces, and downstream jobs — the same value a customer quotes in
  a ticket must find the full story (Chapter 6's correlation model).
- **Safe to expose**: it's an opaque token, not an internal hostname or sequential ID that
  aids enumeration. Use random/opaque formats (e.g. `req_` + 128 bits of randomness), never
  sequential integers.
- On async acceptance (`202`), the operation's `id` in the `Location`/body is the support
  handle for *that* resource; `requestId` still identifies the create call.

```text
client ──request──▶ edge ──generates requestId──▶ app ──▶ db / provider
   ▲                                                        │
   └──────── 4xx/5xx body: requestId ◀── log(trace: requestId) ◀┘
```

## How it works — assembling the extension block

The serializer receives the **public projection** (registry-derived), not the raw error:

```ts
type FieldError = { field: string; code: string; message: string };

type PublicProblem = {
  type: string; title: string; status: number;
  detail: string; instance: string;
  code: string;               // public app code (aliases applied)
  requestId: string;
  errors?: FieldError[];      // present only for validation-style failures
  retryAfterSeconds?: number; // present only for 429/503
};
```

Only this type reaches `JSON.stringify`. A `stack` property does not exist on it — leaking
one requires a type error, not a forgotten `delete err.stack`.

## Worked example — validation with codes

```json
{
  "type": "/problems/validation-error",
  "title": "Validation Failed",
  "status": 422,
  "detail": "Two fields are invalid.",
  "instance": "/api/v1/projects",
  "code": "VALIDATION_FAILED",
  "requestId": "req_4d2e91aa",
  "errors": [
    { "field": "name", "code": "required",
      "message": "name is required." },
    { "field": "owner.email", "code": "format_invalid",
      "message": "owner.email must be a valid email address." }
  ]
}
```

Client behavior: map `errors[].field` → input; map `errors[].code` → localized message;
never parse `detail`. Support behavior: quote `req_4d2e91aa`; grep finds validation
middleware's log line with the raw payload (redacted per policy).

## Key data / numbers

- **`requestId` format:** opaque, non-sequential (e.g. `req_` + 128-bit random hex/base32).
  Leaking structure (timestamps, worker IDs) is optional and rarely worth the enumeration
  surface.
- **`errors[]` cap:** commonly the first **20** entries; add `errorsTruncated: true` beyond
  the cap.
- **Field-path syntax:** dotted paths + `[index]` for arrays (`items[0].qty`). Document the
  grammar in your API reference.
- **Field `code` vocabulary:** start with ~6 (`required`, `type_mismatch`, `out_of_range`,
  `format_invalid`, `enum_invalid`, `cross_field`); resist per-endpoint codes.
- **Header pairing:** `X-Request-Id` response header echoing the body `requestId` is common
  practice; if you accept inbound correlation (e.g. `X-Request-Id` from a trusted gateway),
  validate/limit its length to prevent log injection.

## Real-world use case — Acme SaaS Checkout form

Acme's web checkout form received `422` responses with only `detail: "One or more fields are
invalid."` The frontend re-ran its own client-side validation, disagreed with the server's
rules, and users hit a loop: submit → generic red error → fix nothing → submit again. Adding
`errors[]` with server-truth `field` + `code` let the form highlight the exact inputs and show
server messages. Support tickets tagged "checkout validation loop" fell by ~80% in a month —
the fix was entirely in the error *shape*, not the validation logic.

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| `code` + coarse `type` | Simple docs; clients branch precisely | Requires registry discipline | Default |
| No `code`; branch on `type` only | Fewer fields | Coarse; type explosion pressure | Untyped/internal APIs |
| `errors[]` with per-field `code` | Renderable forms; i18n-able | Vocabulary governance | Any API with forms |
| `errors[]` as `{field: message}` map | Tiny payload | No machine code; i18n impossible | Never for public APIs |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Project internal codes to public aliases before serialization | Send `DB_DEADLOCK` or vendor names as `code` |
| Give `errors[]` machine `code`s alongside human `message`s | Send `{field: "message string"}` maps |
| Generate opaque, non-sequential `requestId`s | Use sequential ints or internal hostnames |
| Propagate `requestId` into every log/trace hop | Generate a new ID per layer |
| Cap `errors[]` size | Echo unbounded hostile input arrays |

## Common mistakes

- **Field paths that mirror the DB.** `field: "projects.seat_count"` leaks your schema and
  breaks if you rename columns; use request paths (`seats`).
- **`code` values that encode versions.** `VALIDATION_FAILED_V2` can't be deprecated
  cleanly; add members, don't version codes.
- **A new `requestId` in the catch-all** different from the edge's ID — support greps the
  wrong one. One ID per request, generated once, threaded everywhere.
- **Documenting codes by hand.** Hand-written docs drift from the registry within a quarter;
  generate.

## Checklist

- [ ] `code` is present, public-safe, and registry-backed on every problem.
- [ ] Validation failures carry `errors[]` with `field` + `code` + `message`.
- [ ] `requestId` is opaque, echoed consistently, and traceable across services.
- [ ] Internal codes never reach the wire (alias projection tested).
- [ ] `errors[]` is bounded against oversized hostile payloads.

## Related

- [Multiple and Pagination Errors](./04-multiple-and-pagination-errors.md)
- [The Problem Details Envelope in Code](../03-practical-examples/01-problem-details-envelope-in-code.md)
- [The Error Envelope Spec](../05-reference/README.md)
