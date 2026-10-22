# Chapter 6 — Do's and Don'ts

> Part III · Chapter 6 · All sections

A condensed rule set for designing the application error model. Use it as a code-review checklist.

## The model

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Define one internal error shape used everywhere | Let each module invent its own |
| Treat errors as data, not a mechanism | Design around `try/catch` |
| Route every error through one constructor/factory | Hand-build error literals |
| Keep identity fields stable | Derive meaning from prose |

## Identity fields

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Keep `code` stable and append-only | Reuse `name` as `code` |
| Use a small closed category set | Add a category per feature |
| Derive severity/retryable from category, allow overrides | Copy the same metadata per throw |
| Keep `message` single-line and secret-free | Put PII/tokens in `message` |
| Branch on `code`, never on `message` | `err.message.includes("timeout")` |

## Cause, context, correlation

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Preserve the original `cause` on every wrap | `throw new Error("failed")` |
| Allowlist safe metadata keys | Spread `req.body`/`process.env` |
| Propagate `correlationId` across queues | Generate a new ID per hop |
| Bound cause-chain depth and detect cycles | Append a cause per retry unbounded |
| Send stacks to logs only | Serialize `stack` to clients |

## Validation and chaining

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Return structured `details` arrays | Return a flat "invalid input" |
| Use stable per-field codes and request paths | Use human labels as identifiers |
| Deduplicate and cap details | Return unbounded arrays |
| Mark the primary error in aggregates | Make handlers guess |

## Safety and evolution

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Freeze error objects; wrap to enrich | Mutate errors mid-flight |
| Write separate log and client serializers | `JSON.stringify(error)` |
| Coerce safely in prod, assert in dev/tests | Throw from the error constructor in prod |
| Make changes additive or versioned | Rename/repurpose fields or codes silently |
| Ignore unknown fields as a consumer | Throw on unknown fields |

## Anti-patterns in the wild

1. **The String Courier** — an error that is just `"failed"`; unroutable.
2. **The Lost Cause** — catch-and-rethrow that drops the original error.
3. **The Metadata Glutton** — `metadata: { ...req.body }`; leaks and bloats.
4. **The Cycle Bomb** — storing live objects that break serialization during an incident.
5. **The Chameleon Code** — one code string whose meaning changes between releases.
6. **The Two Dialects** — a class shape and a literal shape that drift apart.

## Chapter checklist

- [ ] Every error conforms to one documented interface.
- [ ] Every error has a stable `code` and a closed `category`.
- [ ] Every wrap preserves its cause; chain depth is bounded.
- [ ] Metadata is allowlisted; no secrets, PII, or live objects.
- [ ] One constructor enforces invariants, one factory handles natives.
- [ ] Client responses are safe projections, never raw errors.
- [ ] Additive changes only, or an explicit `schemaVersion`.

## Related

- [Chapter 6 Reference](../05-reference/README.md)
- [Chapter 7 — Error Classes, Types, and Structured Results](../../07-error-classes-types-and-structured-results/README.md)
- [Error-Handling Patterns and Anti-Patterns](../../../part-17-organization/46-error-handling-patterns-and-anti-patterns/README.md)
