# Aggregation, Field-Level Representation, and Stable Codes

> Part VII · Chapter 17 · Sections 17.11–17.15 · _Estimated reading time: 22 min_
> **Prerequisite:** [Cross-Field, Conditional, Nested, and List Rules](./03-cross-field-conditional-nested-and-lists.md)

## In one sentence

Validation failures must be **collected, not thrown one at a time** (aggregate vs fail-fast is a
per-stage choice), and every collected failure must be a **field-level entry with a pointer and a
stable code** — with exactly one code per rule across the whole API.

## Why this matters in production

Three failures of this file's ideas produce three classic support problems:

- **Fail-fast field validation** → the user fixes one field per round trip. For a 6-field form that
  is up to 6 submits; for a bulk import it is a support ticket.
- **Prose-as-code** → `"Name is required"` used as the machine key breaks the moment you reword it
  or translate it, and analytics by error type becomes impossible.
- **Duplicate codes for one rule** → `EMAIL_INVALID`, `EMAIL_FORMAT`, `INVALID_EMAIL` all exist;
  nobody knows which to branch on, so clients special-case all three.

Aggregation + field representation + a code registry are three facets of one goal: **a response the
machine can act on without guessing**.

## 17.12 — Aggregated vs fail-fast: a per-stage decision

There is no global answer. The right strategy differs *by stage*:

| Stage | Strategy | Why |
| ----- | -------- | --- |
| Transport/guard (size, content-type) | **Fail fast** | Nothing downstream can run |
| JSON parse | **Fail fast** | No fields exist to aggregate |
| Field rules (type/required/range/format) | **Aggregate** | User fixes all at once |
| Cross-field/conditional | **Aggregate** (after inputs pass) | Independent rule groups |
| DB write / uniqueness (L3) | Sequential or first-conflict | Stateful checks interact |
| Bulk import (17.11) | **Aggregate per row**, continue or stop per policy | Partial success is the product |

```text
        fail fast                    aggregate                    fail fast
bytes ──────────▶ parse ──▶ schema/semantic checks ──▶ domain ──▶ persist
 (413/415/400)             (collect ALL field errors)  (first/    (DB conflict)
                                                     grouped)
```

**Fail-fast is not "throw the first error".** It means: *stop the stage*, because continuing is
meaningless (no parsed body) or unsafe. Field validation is never that — continuing costs
microseconds and yields a complete answer.

## 17.11 — Bulk failures

Bulk endpoints (import rows, batch invites, `ExportJob` job specs) need a **two-level contract**:
per-item outcome + overall outcome.

```json
{
  "status": 422,
  "title": "BULK_VALIDATION_FAILED",
  "detail": "3 of 1,200 rows are invalid.",
  "errors": [
    { "pointer": "/rows/17/email",   "code": "format_invalid", "params": { "format": "email" } },
    { "pointer": "/rows/42/seats",   "code": "out_of_range",   "params": { "min": 1, "max": 500 } },
    { "pointer": "/rows/900/name",   "code": "required" }
  ],
  "summary": { "total": 1200, "invalid": 3, "valid": 1197, "rejected": true }
}
```

Decide and document the **policy**:

| Policy | Behavior | Use when |
| ------ | -------- | -------- |
| All-or-nothing (recommended default) | Any invalid row → whole batch rejected, nothing written | Writes must stay consistent; cheapest to reason about |
| Partial accept | Valid rows written, invalid returned with row pointers | Large imports, resume-friendly; needs a result id and audit trail |
| First-error stop | Stop at row 1 | Interactive CLI tools only |

⚠️ **Hazard.** "Partial accept" silently (or not) writing 1,197 rows while returning `422` makes
`422` mean *two different things* — and clients that treat 422 as "nothing happened" will
double-submit. If rows were written, return `207`-style explicit results or a `200` with a result
body — never a bare `422` after partial writes.

## 17.13 — Field-level representation

The canonical entry — this is the contract, memorize it:

```json
{
  "pointer": "/billingAddress/postalCode",
  "code": "format_invalid",
  "message": "Enter a valid postal code.",
  "params": { "format": "postal-code", "country": "DE" }
}
```

| Member | Required | Purpose | Owned by |
| ------ | -------- | ------- | -------- |
| `pointer` | ✅ | Where — JSON Pointer RFC 6901 | validator |
| `code` | ✅ | What class — stable, machine-readable | validator / registry |
| `message` | ⬜ | Human courtesy text; may be localized/reworded freely | presentation layer |
| `params` | ⬜ | Values needed to fix or interpolate (`min`, `max`, `when`, `other`) | validator |

Rules:

- **`pointer` + `code` is the identity of an error.** Clients branch on that pair; the message is
  decoration (17.20).
- **Never put values the user typed back into `message` in a way that implies safety** — keep
  user content in `params` and let the client render it (XSS-safety at the contract level).
- **Container-level errors** (whole payload) use pointer `"/"` or `""` — declare which and be
  consistent.

Two standard shapes you can adopt instead of inventing: **RFC 9457 Problem Details** with an
extension `errors` array (used throughout this chapter), or **JSON:API error objects**, where the
field lives at `source.pointer`:

```json
{ "errors": [ { "status": "422", "code": "format_invalid",
                "title": "Unprocessable Content",
                "detail": "Enter a valid postal code.",
                "source": { "pointer": "/billingAddress/postalCode" } } ] }
```

Either is fine; **mixing both across endpoints is not**.

## 17.14 — Stable codes

A stable field code is a **contract identifier**, versioned like an API:

| Property | Meaning |
| -------- | ------- |
| Stable | Never repurposed; meaning changes are new codes |
| Rule-level, not field-level | `format_invalid` for every field; field identified by `pointer` |
| Field-independent wording | `required`, not `NAME_REQUIRED` |
| Enum, not free text | Members are registered (Ch. 8 registry) |
| Independent of message | Rewording/translation never changes the code |

```text
✅  code: "required"              pointer: "/name"        message: "Name is required."
✅  code: "required"              pointer: "/seats"       message: "Seats is required."
❌  code: "NAME_REQUIRED"         pointer: "/name"        (N codes for N fields → registry rot)
❌  code: "Please enter a name"   pointer: "/name"        (message as code → breaks on i18n)
❌  code: 1007                    pointer: "/name"        (magic numbers → collisions)
```

## 17.15 — Avoiding duplicates

Duplicate codes appear in four ways; each has a mechanical defense:

| Duplicate pattern | Example | Defense |
| ----------------- | ------- | ------- |
| Same rule, two names | `EMAIL_FORMAT` + `INVALID_EMAIL` | One registry entry per rule; lint unknown codes |
| Same name, two rules | `INVALID_FORMAT` for email *and* dates with different params | Rule owns the code; params distinguish |
| Code per field | `SLUG_INVALID`, `SKU_INVALID`, `EMAIL_INVALID` | Rule-level code + `params.format` |
| Error emitted twice | `required` + `type_mismatch` for one absent field | Ordered short-circuit per field (required wins) |

Mechanical defenses (see [deep dive](../02-deep-dive/03-stable-codes-dedup-and-localization.md)):

1. Registry test: every emitted code exists in the registry; CI fails otherwise.
2. Uniqueness test: no two registry rows describe the same rule.
3. One-error-per-field-per-stage: accumulate into a `Map<pointer, Issue[]>` and allow one
   *primary* code per field per stage.

## Key data / numbers

- Recommended response cap: **≤ 100 field errors**; then `"errorsTruncated": true`.
- Bulk `summary`: `total`, `invalid`, `valid`, `rejected` (all four, always).
- Entry fields: `pointer` (required), `code` (required), `message`/`params` (optional).
- Pointer standard: RFC 6901; container pointer `"/"`.
- Field code vocabulary (start here): `required`, `type_mismatch`, `out_of_range`,
  `format_invalid`, `too_long`, `unknown_field`, `unexpected_shape`, `cross_field_invalid`,
  `conditional_rule_failed`, `duplicate_item`, `too_many_items` — register before first use.

## Real-world use case — ExportJob

`ExportJob` accepts `{ range, columns[], filters }` where `columns` may list 50 fields and
`filters` up to 20 clauses. The original handler returned the first invalid column: analysts fixed
one column per attempt, and a filter with an unknown field name returned `"invalid filter"`,
forcing guesswork. Worse, three different teams had added codes (`COL_UNKNOWN`,
`FILTER_FIELD_MISSING`, `UNKNOWN_COLUMN`) for the same rule. After the change: all issues
aggregated with pointers (`/columns/7`, `/filters/3/field`), one registered code
(`unknown_field` + `params.key`), capped at 100 with `errorsTruncated`. Median attempts to a valid
export spec dropped from 4.6 to 1.3, and dashboards grouping by `code` finally had one series per
rule.

## Trade-offs

| Approach | Pros | Cons | When to use |
|----------|------|------|-------------|
| Aggregate all field errors | One round trip; best UX | Slightly more code; needs caps | ✅ Default |
| First field error only | Trivial | N round trips for N defects | Tiny/internal endpoints |
| Aggregate + per-field single primary | Predictable, deduped | Hides secondary issues on same field | ✅ Recommended detail level |
| All issues per field unbounded | Complete | Response bloat, noise | Only behind caps |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Fail fast only at parse/guard stages | Abort field validation on first bad field |
| Give every entry `pointer` + `code` | Return prose-only validation errors |
| Register codes before use; CI-check them | Invent codes per field or per sprint |
| Short-circuit one field: `required` beats `type_mismatch` | Emit 3 stacked errors for one absent field |
| Cap `errors[]` and flag truncation | Return an unbounded errors array |

## Common mistakes

- **Aggregating from a `throw`-based validator** — the first `ValidationException` wins and
  aggregation is impossible; use accumulation (`safeParse`, issue lists, `Result` with lists).
- **Bulk partial write + `422`** — see 17.11 hazard.
- **Registry drift** — codes live in string literals scattered across handlers; nobody notices
  `FORMAT_INVALID` vs `format_invalid` both exist.
- **Cap without a truncation flag** — clients count 100 errors, think that is all, and mislead
  users.

## Checklist

- [ ] Stage strategy documented: fail-fast at parse, aggregate at field level.
- [ ] Every entry has `pointer` + `code`; `params` carries fixable numbers.
- [ ] One code per rule; registry + CI check in place.
- [ ] One primary code per field per stage.
- [ ] `errors[]` capped with explicit truncation marker.
- [ ] Bulk responses carry `summary` and an explicit all-or-nothing/partial policy.

## Related

- [Aggregation Mechanics (deep dive)](../02-deep-dive/01-aggregation-mechanics.md)
- [Stable Codes, Dedup, and Localization (deep dive)](../02-deep-dive/03-stable-codes-dedup-and-localization.md)
- [Validation DTO → 422 Envelope](../03-practical-examples/01-create-project-dto-to-422-envelope.md)
- [Chapter 8 — Error Codes and Registries](../../../part-03-error-models/08-error-codes-and-error-registries/README.md)
