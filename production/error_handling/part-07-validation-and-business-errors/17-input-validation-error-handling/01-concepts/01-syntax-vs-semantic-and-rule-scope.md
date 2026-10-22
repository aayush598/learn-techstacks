# Syntax vs Semantic Validation — and Where Rules Stop

> Part VII · Chapter 17 · Sections 17.1, 17.16 · _Estimated reading time: 16 min_
> **Prerequisite:** [Chapter 17 overview](../README.md)

## In one sentence

A **syntactic** check asks "can this request be parsed at all?", a **semantic** check asks "does
this payload fit my schema?", and a **business rule** asks "is this action allowed right now?" —
**three different owners, three different status codes, three different failure shapes**.

## Why this matters in production

When teams collapse these layers, three recurring bugs appear:

- **Business rules answered with `400`.** "Coupon EXPIRED10 no longer applies" arrives as a bare
  `400 Bad Request`, so the frontend cannot tell the user to remove the coupon instead of fixing
  their JSON.
- **Schema rules implemented in the service layer.** A `seats` range check runs after the DB
  round trip, so every bad request still costs a transaction.
- **Parse errors reported as `422` with zero fields.** The client renders "0 errors found" and
  retries the identical body forever.

Each mistake erases information the client needs to act. The layering is what makes the response
**actionable**.

## The three layers

```text
 ┌────────────────────────────────────────────────────────────────────┐
 │ L1 SYNTACTIC   "Is it a message I can read?"      owner: transport │
 │    bytes → JSON.parse / Content-Type / headers    → 400, 413, 415  │
 ├────────────────────────────────────────────────────────────────────┤
 │ L2 SEMANTIC    "Does it fit the contract?"        owner: DTO/schema│
 │    required, type, range, format, cross-field     → 422 + fields   │
 ├────────────────────────────────────────────────────────────────────┤
 │ L3 BUSINESS    "Is it allowed in this state?"     owner: domain    │
 │    invariants, entitlements, transitions, quota   → 409/403/402/…  │
 └────────────────────────────────────────────────────────────────────┘
```

| Layer | Question | Example | Fails when | Owner | Typical status |
| ----- | -------- | ------- | ---------- | ----- | -------------- |
| L1 syntactic | Can I parse it? | Body is valid JSON; `Content-Type` is JSON | Before any field exists | transport/parse | `400`, `413`, `415` |
| L2 semantic | Does it match the schema? | `seats` is an integer in 1–500; `name` present | Payload exists but is invalid | DTO/validator | `422` (+ field errors) |
| L3 business | May this happen now? | Plan already active; seat quota full | Payload is valid; world says no | domain | `409`, `403`, `402`, `422` |

**The hand-off matters.** L2 must complete before L3 runs: the domain should never check
`typeof x === "number"` — it was promised a `Seats(1..500)` already. If the domain still guards
types, validation is duplicated; if the domain *doesn't* guard invariants, a bug bypasses L2.

## 17.1 — Syntax vs semantic in practice

```ts
// L1: syntactic. Nothing exists yet — no fields, no pointers, no 422s.
let body: unknown;
try {
  body = JSON.parse(raw);
} catch (err) {
  return res.status(400).json({
    type: "https://errors.acme.example/malformed-request",
    title: "MALFORMED_BODY",
    status: 400,
    detail: "The request body is not valid JSON.",
    instance: req.path,
  });
}

// L2: semantic. The payload parsed; now each field can be named and reported.
const parsed = CreateProjectDto.safeParse(body);
if (!parsed.success) return res.status(422).json(toProblem(parsed.error, req));
```

A tell-tale bug: **`422` with `errors: []`**. That means a semantic response was built from a
syntactic failure — there are no fields to point at, because parsing never produced any.

## 17.16 — Where validation stops and business rules start

Validation and business rules can *look* identical (`"seats must be at least 1"`), so use three
tests to decide the layer:

| Test | Validation (L2) | Business rule (L3) |
| ---- | --------------- | ------------------ |
| **State test** — does the answer change with tenant/state/time? | No: `1–500` is true everywhere | Yes: "your plan allows 25 seats" |
| **Data test** — can it be decided from the payload alone? | Yes | No: needs DB, subscription, clock |
| **Owner test** — who fixes it? | The caller edits the field | The caller changes the action (pick another plan, wait, ask an admin) |
| **Reuse test** — would a CLI, job, and webhook all apply it? | Yes, identically | Varies per path |

Concrete splits people get wrong:

```text
"email must contain @"                     → L2 format        (payload-only)
"email must be unique in this tenant"      → L3 duplicate     (needs DB)
"startDate must be before endDate"         → L2 cross-field   (payload-only)
"startDate cannot be in the past"          → L3 precondition  (needs clock + state)
"seats must be an integer"                 → L2 type          (payload-only)
"seats must not exceed your plan limit"    → L3 entitlement   (needs subscription)
"EXPORT rows ≤ 10_000"                     → L2 range         (contract limit)
"EXPORT blocked while another runs"        → L3 lifecycle     (needs job state)
```

⚠️ **Hazard.** A business rule checked at L2 with a *hardcoded* limit (`seats ≤ 25` in the DTO)
is a validation bug waiting to happen: the plan limit lives in billing, not in a schema constant.
Conversely, a schema rule checked only in the domain (`name` required, deep in a service method)
makes every invalid request pay for auth, tenancy, and a DB read before rejection.

## Decision rule

> **If the check can be answered from the request body and a static contract, it is validation.
> If it needs the database, the clock, or another system, it belongs to the domain.**

## Key data / numbers

- L1 statuses: `400` malformed JSON, `413` body too large, `415` wrong media type, `431` headers
  too large (see [17.19](./05-trust-boundaries-clients-and-contracts.md)).
- L2 status: **`422`** (RFC 9110 *Unprocessable Content*, historically *Unprocessable Entity*) with
  at least one field error — recommended default; using `400` for L2 is allowed but must be
  uniform across your API.
- L3 statuses: `409` conflict, `403`/`404` ownership, `402` balance, `429` quota-rate,
  `422` business rule — full table in
  [Chapter 18 reference](../../18-domain-and-business-logic-errors/05-reference/README.md).
- Rule of thumb: **every `422` must carry ≥ 1 field error**; **every `400` must be a parse/guard
  failure with 0 field errors**.

## Real-world use case — Checkout

`Checkout` validates a subscription upgrade POST. Before the split, one DTO checked `seats ≥ 1`
(L2), `seats ≤ 25` (a copy of the old plan limit — actually L3), and the service checked whether
the tenant had billing enabled (L3), returning `400` for all three. Upgrading a billing-enabled
tenant past 25 seats produced a user-facing "Bad Request" with no field, and support couldn't
triage it. After the split: `seats ≤ 500` stayed in the DTO as `422` with a `pointer`; "plan Pro
allows max 25 seats" became `UPGRADE_EXCEEDS_PLAN_LIMIT` → `409` with the actual limit in
`details.limit`; billing-disabled became `BILLING_NOT_CONFIGURED` → `409`. Ticket volume for
"can't upgrade" dropped because the client could now render the specific reason.

## Trade-offs

| Approach | Pros | Cons | When to use |
| ----------|------|------|-------------|
| L2-only (business rules in DTO) | Fast rejection, one place | Rules need state; duplicated constants; wrong layer | Only for truly static contract limits |
| L3-only (schema checks in service) | One execution path | Invalid input pays full pipeline cost; vague errors | Never — convenience masquerading as design |
| Layered (recommended) | Right cost, right owner, actionable errors | Requires discipline at the seams | Default for every API |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Return `400` only for unparseable/unguarded requests | Return `400` for a field rule you could name |
| Complete L2 before invoking the domain | Run type checks inside the domain layer |
| Put stateful checks (uniqueness, entitlement) in the domain | Hardcode plan limits into DTOs |
| Guarantee ≥1 field error on every `422` | Send `422` with an empty `errors` array |

## Common mistakes

- **Returning `422` for malformed JSON** — no fields exist, so clients that render field errors
  show nothing. Detect parse failure first and return `400`.
- **Validation in the controller *and* the service with different rules** — the two drift; tests
  pass for one path and users hit the other.
- **Business rule as a format check** (`/^…/` regex over a coupon that must be looked up) —
  converts a `409` into a confusing `422`.
- **Skipping L2 because "the frontend already validates"** — the frontend is optional (17.18).

## Checklist

- [ ] Every endpoint distinguishes parse failure (`400`) from schema failure (`422`).
- [ ] No `422` response is ever produced without at least one field error.
- [ ] Every rule is labeled L2 or L3 in code review; stateful rules live in the domain.
- [ ] No plan/quota/time constant is embedded in a schema definition.
- [ ] Domain code contains no `typeof`/regex/format checks.

## Related

- [Field, Shape, and Format Rules](./02-field-shape-and-format-rules.md)
- [What Domain Errors Are](../../18-domain-and-business-logic-errors/01-concepts/01-what-domain-errors-are.md)
- [Validation DTO → 422 Envelope](../03-practical-examples/01-create-project-dto-to-422-envelope.md)
- [Validation Reference](../05-reference/README.md)
