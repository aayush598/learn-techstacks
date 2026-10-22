# Trust Boundaries, Untrusted Clients, and the Validation Contract

> Part VII · Chapter 17 · Sections 17.17–17.22 · _Estimated reading time: 22 min_
> **Prerequisite:** [Aggregation, Field-Level Representation, and Stable Codes](./04-aggregation-and-field-error-representation.md)

## In one sentence

Validation is a **trust-boundary activity**: the server is the only real check, malformed and
oversized payloads must be rejected before field validation even starts, and the response you send
back must be **localizable, non-leaky, and identical in shape on every endpoint**.

## Why this matters in production

The untrusted side of this file is a security boundary and the trusted side is a compatibility
boundary. Skip server-side checks and an attacker skips your form entirely. Inconsistent envelopes
and messages leak schema details (`project_row_limit_exceeded_by_2_million` reveals your table
limits) and break SDKs on every release. Validation responses are also your highest-volume
*translated* text — if they are hardcoded English sentences, your German customers get English
error toasts forever.

## 17.17 — Validation at trust boundaries

A trust boundary is where data crosses from an actor you do not control into a system you do.
Every crossing gets the full pipeline **in order**, before any stateful work:

```text
 1. transport guards   size, method, content-type, authn   → 413/415/401/405
 2. parse              JSON/protobuf decode                → 400
 3. structure/schema   DTO rules (17.2–17.10), aggregated  → 422 + fields
 4. normalization      trim/case/unicode canonicalization  → (then re-check 3)
 5. domain             invariants, entitlements, state     → 409/403/402/… (Ch. 18)
```

Trust boundaries worth naming:

| Boundary | Entry | Extra rule |
| -------- | ----- | ---------- |
| Public API | browser/mobile → gateway | Full pipeline; strict schema |
| Webhook ingress | Stripe → `WebhookIngest` | **Signature verification first**, then pipeline on the *verified* body |
| Queue/worker | serialized job payload → handler | Schema-version check; poison → DLQ, not `422` |
| Agent tool call | LLM tool args → tool handler | Validate args exactly like an API body ([`AgentRun`](../../../part-16-specialized-saas-scenarios/44-ai-llm-and-tool-calling-application-errors/README.md)) |
| Inter-service | internal service → internal service | Validate too: "internal" ≠ "trusted forever" |
| Import file | uploaded CSV → parser | Size, type, decompression-bomb guards before rows |

```python
# WebhookIngest: authenticate the bytes before validating their meaning.
if not signature_ok(raw_body, sig_header):
    return Response(status=400)          # never 422: we refuse to discuss unverified content
event = json.loads(raw_body)             # parse failure → 400
issues = validate(event_schema, event)   # field errors → but webhooks retry, so log + 400/200 policy
```

> ⚠️ **Hazard.** Validating *before* signature verification lets an attacker use your validator as
> an oracle (and your CPU as a doS target). Verify first, parse second, validate third.

## 17.18 — Never rely on client-side validation

Client-side validation is a **UX optimization, not a control**. The honest model:

| Where | Purpose | Can it be trusted? |
| ----- | ------- | ------------------ |
| Browser/SDK checks | Save a round trip; instant feedback | ❌ Trivially bypassed (curl, older app, hostile script) |
| Server L2/L3 checks | Correctness, integrity, security | ✅ The only control |
| Server after DB write | Constraint backstop (`NOT NULL`, `CHECK`, unique) | ✅ Last line; translate, don't rely on it alone |

Consequences to design for:

- **Every rule is implemented server-side exactly once** (client may *mirror* it, never *be* it).
- **Old clients exist.** A mobile client from 14 months ago sends the shape it knows; your strict
  schema needs a deprecation story (17.22), not a `422` apocalypse.
- **The DB backstop still fires** (`SQLSTATE 23502/23514`) when a path skips validation — that is
  a bug signal (alert), not a normal response ([translation map](../../../part-06-boundaries-and-translation/16-error-translation-and-normalization/03-practical-examples/01-postgres-sqlstate-to-domain-to-http.md)).

## 17.19 — Malformed and oversized input

Handle the ugly inputs *before* field validation, each with its own status — and never let them
become `500`s or silent truncation:

| Input defect | Detection point | Status | Note |
| ------------ | --------------- | ------ | ---- |
| Wrong/missing `Content-Type` | guard | `415` | Reject early; do not sniff-and-guess on write endpoints |
| Body over limit | before/at read | `413` | Per-route limits (e.g. 100 KB JSON, 10 MB upload) |
| Headers over limit | server | `431` | Cookie explosions, giant auth headers |
| Invalid JSON / truncated | parse | `400` | Zero field errors — nothing to point at |
| Wrong top-level type (`[]` vs `{}`) | parse/structure | `400` or `422` | Pick one; recommended: `400` when the *container* type mismatches |
| Deeply nested / many keys (bomb) | guard during parse | `400` | Enforce depth ≤ ~16, key/byte caps |
| Huge array | structure | `422 too_many_items` | Check size before per-item work |
| Duplicate JSON keys | parser policy | `400` | Last-wins vs first-wins must be *decided*; ambiguity is a smuggling vector |
| Wrong encoding / bad Unicode | normalize | `400` | Reject lone surrogates, overlong sequences |

```ts
// Order is the whole point: guards before parse, parse before schema.
if (req.headers["content-type"] !== "application/json") return respond(415, "UNSUPPORTED_MEDIA_TYPE");
if (req.contentLength > MAX_JSON_BYTES)                return respond(413, "PAYLOAD_TOO_LARGE");
const raw = await readBody(req, MAX_JSON_BYTES);       // hard stop while reading, not after
let parsed: unknown;
try   { parsed = JSON.parse(raw); }
catch { return respond(400, "MALFORMED_BODY"); }
if (depth(parsed) > MAX_DEPTH || keys(parsed) > MAX_KEYS) return respond(400, "PAYLOAD_TOO_COMPLEX");
return validate(parsed);                                // here be 422s
```

Design notes:

- **Read with a hard stop.** Enforcing `contentLength` alone is not enough (chunked bodies lie);
  abort the read at the byte cap so `413` is guaranteed, not hoped for.
- **Truncation is never a fix.** Silently clipping a body converts `413` into corrupt data.
- **`400` vs `413` vs `415` are cheap consistency wins** — most APIs get them wrong per-route;
  centralize the guards in middleware (Ch. 21).

## 17.20 — Localization

Separate **code** (stable, locale-free) from **message** (presentation, locale-dependent):

```json
{ "pointer": "/seats", "code": "out_of_range",
  "message": "Seats must be between 1 and 500.",
  "params": { "min": 1, "max": 500 } }
```

Three strategies, in increasing maturity:

| Strategy | How | Trade-off |
| -------- | --- | --------- |
| Client-side by code (recommended start) | Client maps `code` → its own i18n string using `params` | Server never needs locales; stale translations possible in old clients |
| Server-side message key | Server sends `messageKey: "validation.out_of_range"` + `params` | Server controls wording; still no raw text |
| Server-side per-request locale | `Accept-Language` → server picks string | Fastest to ship; needs translation pipeline; CDN/cache pitfalls |

Rules that make any strategy work:

- **Never branch on `message`.** Codes are the API; sentences are not (also 17.14).
- **`params` must contain everything a translator needs** (`min`, `max`, `when`, `other`) — no
  parsing numbers out of sentences.
- **Do not interpolate raw user input into server messages** without escaping rules; keep typed
  values in `params` (see 17.13).

## 17.21 — Preventing schema leakage

A validation error describes *your contract*, not *your implementation*:

| ❌ Leaks | ✅ Safe alternative |
| -------- | ------------------- |
| `column "seat_count" does not exist` | `type_mismatch` at `/seats` |
| `SQLSTATE 23505 on projects_slug_key` | `format_invalid` / `409` duplicate |
| `expected 8 fields, got 11` (internal DTO shape) | one `unknown_field` per offending key |
| `limit exceeded: max 100 rows (table projects has 2.1M rows)` | `too_many_items` + `params.max` |
| Full expected regex (`/^[a-z]+(?:-[a-z]+)*$/`) | `format_invalid` + `params.format: "slug"` |
| Stack trace / framework version header | `code`, `pointer`, `requestId` |

Guiding question: **"Does this text help the caller fix the request, or does it describe my
internals?"** First is contract, second is a leak (full treatment in
[Part XIII](../../../part-13-security-aware/34-security-principles-for-error-handling/README.md)).

One subtlety: *contract* detail is not leakage. Telling a caller `max 500 seats` when 500 is a
published product limit is helpful; telling them your `projects.seats` column is `int4` is not.

## 17.22 — Consistent contracts

Consistency is what lets one SDK, one error renderer, and one support macro serve the whole API:

| Contract element | Must be identical everywhere |
| ---------------- | ---------------------------- |
| Envelope | Same Problem Details shape; same extension members |
| Status policy | `400` parse / `422` schema (or all `400` — but never mixed) |
| Field entry shape | `pointer` + `code` (+ same optionals) |
| Code vocabulary | One registry, one casing convention |
| Container pointer | `"/"` or `""` — pick one |
| Caps | Same truncation rule, same flag name |
| Bulk summary | Same keys on every bulk endpoint |

Version it: **adding** an optional member or a new code is backward-compatible; **removing/renaming**
or changing a code's meaning is breaking (see
[Ch. 49](../../../part-19-contracts-and-governance/49-error-contract-design-and-versioning/README.md)).
Keep a **snapshot test** of one golden `422` per endpoint family so drift fails CI.

## Key data / numbers

- Guard statuses: `400` malformed, `413` too large, `415` unsupported media type, `431` headers
  too large, `429` rate (Ch. 19).
- Recommended guards: JSON body **≤ 100 KB**, depth **≤ 16**, field errors **≤ 100** per response
  (recommendations — publish your own numbers).
- Webhook rule: **verify signature → parse → validate**; never expose field errors pre-verification.
- Localizable contract: `code` + `params` required; `message` optional and replaceable.
- Golden-file snapshot: 1 `422` fixture per endpoint family in CI.

## Real-world use case — WebhookIngest

Acme's `WebhookIngest` endpoint validated the Stripe payload *before* checking the signature,
returning field-level `422`s to any anonymous caller. That turned the endpoint into a free oracle
for probing the event schema, and a flood of garbage bodies with 1,000-element `items` arrays
burned CPU in the validator (a `57.7`-style error storm from pathological input). The fix moved
verification first, added a 256 KB read cap and depth guard, and mapped *any* pre-auth failure to a
single non-informative `400`. Schema probing stopped immediately, and validator CPU per request
dropped below the noise floor.

## Trade-offs

| Approach | Pros | Cons | When to use |
|----------|------|------|-------------|
| Client-only validation | Feels fast | Security hole | Never |
| Server + mirrored client checks | Best UX, real control | Rules maintained twice (client mirrors, server owns) | ✅ Default |
| Server messages localized per-request | Full control of wording | i18n pipeline, cache issues | Mature global products |
| Client-side translation by code | One server, many languages | Client must ship translations | ✅ Recommended start |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Verify signatures before parsing/validating webhooks | Return field errors on unverified payloads |
| Cap bytes/depth/keys during read | Parse first, hope the body is small |
| Send `code` + `params`; treat `message` as replaceable | Hardcode the only usable text into `message` |
| Keep contract detail (limits, formats) | Leak implementation detail (columns, SQLSTATE, regexes) |
| Keep one envelope/status policy repo-wide | Different shapes per endpoint or per team |

## Common mistakes

- **`413` after fully buffering the body** — the damage (memory) already happened.
- **"Helpful" framework errors passed through** (`detail[].msg` from a framework with internal
  paths) — normalization must strip them ([Ch. 16](../../../part-06-boundaries-and-translation/16-error-translation-and-normalization/README.md)).
- **Localizing codes** (`"nötig"` as `code`) — breaks every client branch and analytics query.
- **Strict schema with no deprecation path** — old mobile clients get mass `422`s on release day.

## Checklist

- [ ] Every entry point (API, webhook, queue, tool call) runs the ordered pipeline.
- [ ] Signature/auth precedes parse on untrusted ingress.
- [ ] Byte/depth/key caps enforced *during* read; distinct `413`/`415`/`400`/`431`.
- [ ] No client-side-only rule; client mirrors server rules.
- [ ] Responses carry `code` + `params`; messages are replaceable.
- [ ] No DB/schema/regex/stack detail in any validation response.
- [ ] One envelope, one status policy, one code registry, snapshot-tested.

## Related

- [Validation at the Trust Boundary (deep dive)](../02-deep-dive/02-validation-at-the-trust-boundary.md)
- [Stable Codes, Dedup, and Localization (deep dive)](../02-deep-dive/03-stable-codes-dedup-and-localization.md)
- [Chapter 21 — API Boundary and Middleware Error Handling](../../../part-08-http-and-api/21-api-boundary-and-middleware-error-handling/README.md)
- [Chapter 34 — Security Principles for Error Handling](../../../part-13-security-aware/34-security-principles-for-error-handling/README.md)
