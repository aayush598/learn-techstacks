# Field Rules: Structure, Required, Type, Range, Format

> Part VII · Chapter 17 · Sections 17.2–17.6 · _Estimated reading time: 20 min_
> **Prerequisite:** [Syntax vs Semantic and Rule Scope](./01-syntax-vs-semantic-and-rule-scope.md)

## In one sentence

The five **shape-level rule classes** — structure, required, type mismatch, range, and format —
form the backbone of every validation contract, and each must map to **one stable field code with
one pointer** in the response.

## Why this matters in production

These five classes cover the large majority of all validation failures. If their representation is
inconsistent — `400` for missing fields here, `422` for missing fields there, `"email is required"`
as prose in one endpoint and a code in another — then your SDK, your frontend error renderer, and
your support macros all fork per endpoint. Consistency at this level is what makes a **single
error renderer** possible across an entire API.

## The five classes

| # | Class | Question | Example payload defect | Field code |
| - | ----- | -------- | ---------------------- | ---------- |
| 17.2 | Structure | Is the payload shaped as the contract says? | Unknown top-level key; `project` is a string where an object is declared; missing object wrapper | `unknown_field`, `unexpected_shape` |
| 17.3 | Required | Is the field present (and non-empty)? | `"name"` absent, `null`, or `""` | `required` |
| 17.4 | Type mismatch | Is it the declared type? | `"seats": "many"` (string vs number); `"active": 1` vs boolean | `type_mismatch` |
| 17.5 | Range/boundary | Is the value inside numeric/temporal bounds? | `seats: 0`, `seats: 10_000`, date before 1970 | `out_of_range`, `out_of_bounds` |
| 17.6 | Format | Does the string match its declared pattern? | `"not-an-email"`, bad UUID/slug/URI | `format_invalid` |

Run them **in this order** — it is cheapest-to-explain first for the caller and stops the noise:
structure → required → type → range → format. A field that is absent should produce `required`,
not also `type_mismatch` (see [avoiding duplicates](./04-aggregation-and-field-error-representation.md)).

## 17.2 — Request structure

Structure rules govern the payload *container*: unknown keys, wrong nesting, wrong top-level shape.

```ts
// Strict by default: unknown keys are a contract violation, not a shrug.
const dto = z.object({
  name: z.string().min(1).max(80),
  seats: z.number().int(),
}).strict();   // → issue code "unrecognized_keys", pointer "/", keys: ["naem"]
```

Design choice — **strict vs permissive**:

| Mode | Behavior | Recommendation |
| ---- | -------- | -------------- |
| Strict (`.strict()`, `additionalProperties: false`) | Unknown key → `422 unknown_field` | ✅ Default for **public/written** APIs: catches client typos (`naem`) that would otherwise silently drop data |
| Passthrough | Unknown keys ignored | Acceptable for **inbound webhooks/events** where producers evolve ahead of you (`WebhookIngest`) |
| Strip | Unknown keys silently removed | ❌ Hides typos; turns a `422` into silent data loss |

> ⚠️ **Hazard.** Passthrough is fine for consumption, dangerous for creation. A `POST /projects`
> that silently ignores a misspelled `visibilty` field creates resources with wrong defaults, and
> nobody finds out until the customer's audit.

## 17.3 — Required

"Present" has three variants; pick one and state it in the contract:

```text
missing        key absent                → required
null           "name": null              → required (unless nullable by contract)
empty          "name": "" or [] or {}    → required  (recommended for strings/collections)
```

Trim-before-check is the norm for user text: `"   "` should fail `required`, not pass and become
a blank project name. Decide whether **defaults** make a field optional: if `seats` defaults to
`1`, it is not "required" — it is "optional with a default", and the response should never
complain about it.

## 17.4 — Type mismatch

Type checks must run **before** any other value check, because downstream rules assume the type:

```ts
// Order matters: a string must not be range-checked with < and >.
if (typeof raw !== "number" || !Number.isFinite(raw)) {
  return { pointer: "/seats", code: "type_mismatch", params: { expected: "integer" } };
}
if (!Number.isInteger(raw)) return { pointer: "/seats", code: "type_mismatch" }; // 3.5
if (raw < 1 || raw > 500)   return { pointer: "/seats", code: "out_of_range", params: { min: 1, max: 500 } };
```

Two sneaky cases:

- **JSON has no integer type.** `"seats": 3.0` and `"seats": 3` are indistinguishable after parse
  in many stacks; `"seats": 3.5` must be `type_mismatch` (not a range error) if the contract says
  integer.
- **Numeric strings that look numeric.** `"seats": "5"` is `type_mismatch` — *not* "coerce and
  continue". Silent coercion (query params excepted) is how `"5"` and `5` diverge across services.

## 17.5 — Range and boundary

Bounds come from the contract, are inclusive/exclusive by declaration, and always report the bound:

```json
{ "pointer": "/seats", "code": "out_of_range", "params": { "min": 1, "max": 500, "inclusive": true } }
```

| Boundary kind | Typical defect | Note |
| ------------- | -------------- | ---- |
| Numeric min/max | `seats: 0`, `seats: 100000` | Report `min`/`max` so the client can fix in place |
| String length | 400-char project name | Use *code points*, not bytes, for user text |
| Temporal | end before start, date in 1901 | Prefer cross-field (17.7) over two independent ranges |
| Collection size | 10k recipients | Often a **contract limit** (413-adjacent), not a value error |

## 17.6 — Format

Format rules validate *shape of a string*, not its meaning: email, slug, UUID, ISO-8601 datetime,
IANA timezone, currency code.

```json
{ "pointer": "/slug", "code": "format_invalid", "params": { "format": "slug" } }
```

Rules of the road:

- **Report `format` as a parameter, not as the code.** `format_invalid` + `{"format":"slug"}`
  keeps one code; `"SLUG_FORMAT"`, `"EMAIL_FORMAT"`, `"UUID_FORMAT"` as three codes is how code
  registries rot (and see 17.15).
- **Format ≠ existence.** `not-an-email@` failing a regex tells you nothing about whether the
  mailbox exists — that is verification (an L3/async concern), never an L2 format check.
- **Normalize before you validate**: case-fold slugs, trim whitespace, then check. Validating the
  raw bytes punishes users for casing.

## Worked example — the five classes in one response

```json
{
  "type": "https://errors.acme.example/validation",
  "title": "VALIDATION_FAILED",
  "status": 422,
  "detail": "The request contains 4 invalid fields.",
  "instance": "/projects",
  "requestId": "req_8f2c1a",
  "errors": [
    { "pointer": "/",          "code": "unknown_field",  "params": { "key": "naem" } },
    { "pointer": "/name",      "code": "required" },
    { "pointer": "/seats",     "code": "type_mismatch",  "params": { "expected": "integer", "received": "string" } },
    { "pointer": "/startAt",   "code": "format_invalid", "params": { "format": "iso8601-datetime" } }
  ]
}
```

Each entry: **pointer** (where), **code** (what class), **params** (the numbers/names needed to
fix it). `message` is optional presentation — see [17.20](./05-trust-boundaries-clients-and-contracts.md).

## Key data / numbers

- Code vocabulary (recommended, one per class): `unknown_field`, `unexpected_shape`, `required`,
  `type_mismatch`, `out_of_range`, `format_invalid`, `too_long`, `too_short`, `duplicate_item`.
- Every `422` carries `errors[]`; every entry carries `pointer` + `code`.
- Pointer syntax: **JSON Pointer (RFC 6901)** — `/seats`, `/items/2/sku`, `""` (or `/`) for root.
- Inclusive-by-default bounds; state `inclusive` explicitly when it matters.

## Real-world use case — Acme SaaS

Acme's `POST /projects` used hand-written `if` checks that returned the *first* error as prose:
`"Name is required"`. A typo'd key (`archived`) was silently dropped (structure), a string seat
count produced a `500` downstream (`"seats": "five"` passed a truthiness check and hit a DB
numeric cast — `SQLSTATE 22P02`), and users had to resubmit four times to fix three fields.
After adopting the five-class schema with aggregation: the string seat count became
`type_mismatch` at the edge, the typo became `unknown_field`, and one round trip carried all four
field errors. The `22P02` path — a validation defect surfacing as a DB error — disappeared.

## Trade-offs

| Approach | Pros | Cons | When to use |
|----------|------|------|-------------|
| Hand-written `if` chains | No dependency | Order bugs, prose codes, first-error-only | Never at scale |
| Schema library (Zod, Pydantic, `go-playground/validator`) | Consistent issues, aggregation, types | Learning curve, config drift | ✅ Default |
| Generated contract (OpenAPI → validators) | One source of truth | Generated messages are generic | Public APIs with SDKs |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Check in order: structure → required → type → range → format | Emit `required` *and* `type_mismatch` for one missing field |
| Report bounds in `params` | Make users guess `min`/`max` |
| Reject unknown keys on write endpoints | Silently drop typo'd fields |
| Reject `3.5` for an integer contract as `type_mismatch` | Coerce `"5"` → `5` silently |

## Common mistakes

- **Coercing then validating** — `"seats": "1e999"` coerces to `Infinity` and slips past naive
  range checks.
- **Length in bytes for user text** — a 100-emoji name "fails" a `max: 100` byte check.
- **Format checks that encode business meaning** — a regex "for company domains" belongs to L3.
- **`required` on a defaulted field** — contradictions between schema and default generate
  impossible-to-reproduce errors.

## Checklist

- [ ] One code per class; params carry the specifics.
- [ ] Type checked before range/format.
- [ ] Unknown-key policy is explicit per endpoint family (strict vs passthrough).
- [ ] Bounds and formats are reported back in the error.
- [ ] No coercion of user body values outside documented behavior.

## Related

- [Cross-Field, Conditional, Nested, and List Rules](./03-cross-field-conditional-nested-and-lists.md)
- [Aggregation and Field-Level Representation](./04-aggregation-and-field-error-representation.md)
- [Validation DTO → 422 Envelope](../03-practical-examples/01-create-project-dto-to-422-envelope.md)
- [Validation Reference](../05-reference/README.md)
