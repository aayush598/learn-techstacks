# Cross-Field, Conditional, Nested, and Collection Rules

> Part VII · Chapter 17 · Sections 17.7–17.10 · _Estimated reading time: 20 min_
> **Prerequisite:** [Field, Shape, and Format Rules](./02-field-shape-and-format-rules.md)

## In one sentence

Once single fields are individually valid, four harder rule classes remain — **cross-field**,
**conditional**, **nested object**, and **array/collection** rules — and each needs a *pointer
convention* so the client knows exactly which field (or which item) is wrong.

## Why this matters in production

These are the rules that make real products work: `endDate` after `startDate`, "seats required when
plan is team", a `billingAddress` object with its own rules, a 2,000-row CSV where 17 rows are bad.
They are also where field-error contracts break: pointers go to the wrong place, errors get
duplicated per item, or a single failure aborts a bulk import of 2,000 good rows. Getting the
pointer convention right is the difference between a form that highlights the broken input and a
form that says "something went wrong".

## 17.7 — Cross-field rules

A cross-field rule is valid only when **two or more individually valid fields are considered
together**. Individually-valid-nevertheless-wrong is the signature:

```json
{ "pointer": "/endDate", "code": "cross_field_invalid",
  "params": { "rule": "end_after_start", "other": "/startDate" } }
```

Rules for reporting:

- **Point at the field the user should change**, not at a synthetic root. If either direction
  could be "wrong" (`startDate` in future vs `endDate` before it), pick one canonical target —
  convention: point at the *second* field in the contract's rule definition.
- **One rule, one error.** `end_after_start` fires once, not twice (`startDate` too early *and*
  `endDate` too late).
- **Suppress when a prerequisite failed.** If `startDate` is missing (`required`), the cross-field
  rule must not also fire — otherwise one root cause yields two errors (see 17.15).

```ts
// Only evaluate when both fields already passed their own checks.
if (start.ok && end.ok && end.value < start.value) {
  issues.push({ pointer: "/endDate", code: "cross_field_invalid",
                params: { rule: "end_after_start" } });
}
```

## 17.8 — Conditional rules

Conditional (dependent) rules activate only under a declared condition — the classic
**if/then in the schema**:

```text
IF   plan = "enterprise"      THEN seats is required and 10..1000
IF   billing = "invoice"      THEN taxId is required
IF   reminder.enabled = true  THEN reminder.offsetMinutes is required
IF   provider = "webhook"     THEN secret must be ≥ 32 chars
```

Report the **condition**, not just the consequence:

```json
{ "pointer": "/seats", "code": "conditional_rule_failed",
  "params": { "rule": "seats_required_for_enterprise", "when": "plan=enterprise" } }
```

Why the `when` param matters: without it, the client shows "seats is required" to a user on the
free plan who has no idea why. With `when`, the UI can render the branch it failed on.

**Conditional ≠ business.** `IF plan=enterprise THEN seats required` is L2 if `plan` is a request
field and 10..1000 is contract-static. `IF plan=enterprise THEN your tenant must have passed KYC`
is L3 — it consults state. Same keyword, different layer ([17.16](./01-syntax-vs-semantic-and-rule-scope.md)).

## 17.9 — Nested objects

Nested rules reuse every single-field rule; the only new thing is the **pointer path**:

```text
/billingAddress/street        required
/billingAddress/postalCode    format_invalid
/settings/defaultView         type_mismatch
/settings/notifications/email type_mismatch
```

Conventions that keep clients sane:

| Convention | Example | Why |
| ---------- | ------- | --- |
| Full path from root, RFC 6901 | `/billingAddress/postalCode` | One renderer handles any depth |
| Parent rule points at parent, not child | `billingAddress` missing → pointer `/billingAddress` | Don't emit `required` for every descendant of an absent object |
| Absent-object short-circuit | If `/billingAddress` is absent, do **not** report its 5 children | Avoids error avalanches from one root cause |
| Depth is bounded | Reject nesting > N (recommended: 8–16) | Defends against parser DoS (`17.19`) |

```json
{ "pointer": "/billingAddress", "code": "required" }
```

— not five entries for `street`, `city`, `postalCode`, `country`, `region`.

## 17.10 — Arrays and collections

Collections add four rule kinds and one hard problem (per-item reporting):

| Rule | Example | Code |
| ---- | ------- | ---- |
| Size | `recipients` max 1,000 | `too_many_items` / `too_few_items` |
| Item validity | item 3 has invalid `email` | item's own code at `/recipients/3/email` |
| Uniqueness within payload | duplicate `email` at index 5 | `duplicate_item` at `/recipients/5/email` |
| Element type of list itself | `tags` given as string, not array | `type_mismatch` at `/tags` |

Pointer convention for items: **zero-based index path** — `/items/2/sku`, `/rows/17/columns/3`.

```json
{ "pointer": "/recipients/5/email", "code": "duplicate_item",
  "params": { "firstIndex": 1 } }
```

Practical guards:

- **Bound item counts before per-item validation.** Validating 2,000,000 items one by one is a
  cheap way to burn a CPU second per request. Enforce the max first (`too_many_items`), then
  validate at most that many (see [17.19](./05-trust-boundaries-clients-and-contracts.md)).
- **Report per-item errors with a cap.** 17 bad rows out of 2,000: report all 17 if under your cap;
  if a row has 40 bad cells, consider one error per row with a `firstError` hint — but never
  unbounded arrays (cap recommendation: **100 field errors per response**, label it as a
  recommendation and document it).
- **Distinguish list-shape from item errors.** `tags: "a,b"` (string where array expected) is one
  `type_mismatch` at `/tags`, not 3 item errors.

## The pointer cheat sheet

```text
""  or  "/"            whole payload (structure errors)
/name                  top-level field
/items/2/sku           nested array item
/billingAddress/city   nested object
/rows/17               bulk row (when reporting row-level errors)
```

JSON Pointer (RFC 6901) escapes: `~0` for `~`, `~1` for `/` — relevant if a key itself contains
slashes (rare; still, use a library).

## Key data / numbers

- Pointer format: **JSON Pointer RFC 6901**, zero-based array indices.
- One error per cross-field rule; skip dependent rules whose inputs already failed.
- Nesting depth recommendation: **≤ 8–16 levels** enforced at parse time.
- Collection guard order: `type → size → item validity → cross-item uniqueness`.
- Recommended cap: **≤ 100 field errors per response**; excess reported as
  `"errorsTruncated": true` (document it — it is a contract detail).

## Real-world use case — Checkout

`Checkout` accepts a scheduled upgrade: `{ plan, seats, startDate, endDate }` plus a conditional
invoice-billing block. The first implementation reported cross-field errors from *both* sides
("startDate too early" and "endDate too early"), and when `startDate` was missing it also emitted
`end_after_start`, so one empty field produced three errors. The client highlighted the wrong
input and users corrected `endDate` twice. The fix: suppress dependent rules when inputs failed,
emit a single `cross_field_invalid` pointing at `/endDate` with `params.other`, and gate the
invoice block behind `conditional_rule_failed` with `when: "billing=invoice"`. Submissions fixed on
the first round trip went from 61% to 89%.

## Trade-offs

| Approach | Pros | Cons | When to use |
|----------|------|------|-------------|
| Evaluate all rules always | Simple code | Duplicate/derivative errors from one root cause | Small DTOs only |
| Dependency-aware evaluation | Clean, minimal error sets | Needs a rule dependency graph | ✅ Default for real forms |
| First-error-per-field | Compact | Hides additional defects | Only under response caps |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Point at the field to change; report `params.other` for context | Point cross-field errors at `/` |
| Suppress dependent rules when prerequisites failed | Report missing `startDate` + invalid `endDate` twice |
| Report one `required` for an absent object | 5 `required` errors for an absent object's children |
| Enforce collection size before item validation | Validate 10⁶ items then reject the array |
| Include `when`/`rule` in conditional params | Return a bare "invalid" for a conditional rule |

## Common mistakes

- **Index pointers that are one-based** (`/items/3` for the 3rd item) — off-by-one highlights the
  wrong row in every bulk UI.
- **Conditional rule written as plain `required`** — the user on the free plan cannot act on it.
- **Uniqueness checked per item without global view** — duplicates 2 and 9 both pass because each
  only compares to its own prefix.
- **Uncapped `errors[]`** — one pathological body produces a multi-megabyte response (your own
  amplification bug).

## Checklist

- [ ] Every cross-field rule has a single canonical pointer and fires at most once.
- [ ] Dependent rules are skipped when their inputs failed.
- [ ] Conditional errors carry the `when` condition in `params`.
- [ ] Absent parents short-circuit their children.
- [ ] Collection size is enforced before per-item validation; `errors[]` is capped.

## Related

- [Aggregation and Field-Level Representation](./04-aggregation-and-field-error-representation.md)
- [Aggregation Mechanics (deep dive)](../02-deep-dive/01-aggregation-mechanics.md)
- [Bulk, Cross-Field, and Cast Examples](../03-practical-examples/02-bulk-cross-field-and-cast.md)
- [Validation Reference](../05-reference/README.md)
