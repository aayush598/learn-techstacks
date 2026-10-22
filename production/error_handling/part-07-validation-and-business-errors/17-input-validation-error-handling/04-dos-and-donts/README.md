# Chapter 17 — Do's and Don'ts

> Part VII · Chapter 17 · All sections

A condensed rule set distilled from the chapter. Use it as a validation review checklist.

## Layering and scope

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Distinguish parse (`400`), schema (`422`), business (Ch. 18) | Return `400` for everything |
| Complete L2 before invoking the domain | Re-check types inside the domain |
| Keep stateful rules (uniqueness, entitlement) out of DTOs | Hardcode plan limits into schemas |
| Guarantee ≥1 field error on every `422` | Send `422` with an empty `errors` array |

## Field rules

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Check in order: structure → required → type → range → format | Stack `required` + `type_mismatch` on one field |
| Report bounds/formats in `params` | Make clients guess `min`, `max`, format |
| Reject unknown keys on write endpoints | Silently drop typo'd fields |
| Reject `3.5` for an integer as `type_mismatch` | Coerce `"5"` → `5` silently |
| Point cross-field errors at the canonical field, once | Fire both directions of a date rule |

## Collections and bulk

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Enforce size before per-item validation | Walk a million items, then reject |
| Use zero-based indexed pointers (`/rows/17/x`) | One vague error pointing at `/rows` |
| Decide all-or-nothing vs partial before any write | Write 1,197 rows and return `422` |
| Count invalid **rows** in `summary.invalid` | Count issues as rows |

## Representation and codes

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Send `pointer` + `code` (+ `params`) as the contract | Send prose-only errors |
| Use one registry-listed code per rule | Invent `EMAIL_FORMAT` + `INVALID_EMAIL` |
| Dedup by (pointer, code); one primary per field | Emit derivative errors from one root cause |
| Cap `errors[]` and set `errorsTruncated` | Return unbounded issue lists |
| Keep messages replaceable; localize via code + params | Branch on message text anywhere |

## Trust boundaries and contracts

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Run ordered guards: size → media type → auth → parse → schema | Validate wherever the handler "feels like it" |
| Verify webhook signatures before parsing | Return field errors to unsigned callers |
| Cap bytes **during** read; abort the stream | Buffer 2 GB, then say `413` |
| Keep SQLSTATE, columns, regexes, stacks out of responses | Ship "helpful" framework internals |
| Use one envelope builder and one status policy repo-wide | Hand-roll a different shape per endpoint |
| Mirror client checks as UX only | Treat client validation as a control |

## Anti-patterns in the wild

1. **The Empty 422** — semantic envelope built from a parse failure; `errors: []`.
2. **The Round-Tripper** — fail-fast field validation; one fix per submit.
3. **The Message Key** — `"Please enter a name"` used as the machine code.
4. **The Code Sprinkler** — per-field codes (`SLUG_INVALID`, `SKU_INVALID`) multiplying weekly.
5. **The Silent Dropper** — unknown keys ignored on write; typos become wrong defaults.
6. **The Partial Writer** — `422` after side effects; clients retry into duplicates.
7. **The Validator Oracle** — field-level webhook errors before signature verification.
8. **The Bufferizer** — full-body read before the size check.
9. **The Limit Leaker** — `max 500 (table projects has 2.1M rows)` in `detail`.
10. **The Dual Contract** — framework default 422 shape on one route, custom on another.

## Chapter checklist

- [ ] Status policy written: `400` parse/guards, `413`/`415`/`431` guards, `422` schema.
- [ ] One strict DTO layer; domain free of `typeof`/regex checks.
- [ ] Aggregation everywhere; caps + truncation flag documented.
- [ ] Field contract: `pointer` (RFC 6901) + `code` + `params`; registry + CI checks.
- [ ] Dependent rules gated on clean inputs; one primary code per field.
- [ ] Bulk: guards → indexed pointers → summary → write policy.
- [ ] Ingress pipeline ordered; signatures first on webhooks.
- [ ] No schema/implementation leakage in any validation response.
- [ ] Localization strategy (client dict by code) documented.
- [ ] Golden `422` snapshots per endpoint family in CI.

## Related

- [Chapter 17 Reference](../05-reference/README.md)
- [Validation DTO → 422 Envelope](../03-practical-examples/01-create-project-dto-to-422-envelope.md)
- [Chapter 18 — Domain and Business Logic Errors](../../18-domain-and-business-logic-errors/README.md)
