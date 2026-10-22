# Chapter 8 — Do's and Don'ts

> Part III · Chapter 8 · All sections

A condensed rule set for error codes and registries.

## Codes: stability and naming

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Name the behavior (`PAYMENT_CARD_DECLINED`) | Encode the mechanism (`PG_23505`, `ECONNRESET`) |
| Keep vendor codes in metadata | Use the vendor's code as your code |
| Treat codes as append-only contracts | Rename or reuse codes |
| Use `SCREAMING_SNAKE_CASE`, 2–5 segments | Mix camel/dot/sentence styles |
| Keep codes header/metric-safe | Use `.`, `:`, or spaces |

## Scoping and visibility

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Reserve domains centrally | Let teams invent prefixes ad hoc |
| Default codes to internal | Expose every code to clients |
| Map internal codes to a public alias | Leak `DB_*`/`INTERNAL_*` codes |
| Keep auth codes enumeration-safe | Split `INVALID_USER` vs `WRONG_PASSWORD` |

## Registry

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Make the registry a typed code module | Keep it in a wiki/spreadsheet |
| Declare each code exactly once | Re-declare codes across modules |
| Enforce uniqueness/format/domains in CI | Trust reviewer discipline |
| Derive mapping tables and docs from it | Hand-maintain parallel tables |
| Give every code an owner and `since` | Leave codes ownerless |
| Require a public alias for internal codes | Publish internal meaning |

## Mapping to behavior

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Derive HTTP/retry/action/message from the registry | Hardcode per handler |
| Map code → i18n key | Map code → English string |
| Retry only transient codes | Retry permanent/business codes |
| Give internal codes generic user messages | Expose internals to users |
| Keep client actions a small closed set | Invent an action per code |

## Lifecycle

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Deprecate before removing | Delete a public code outright |
| Dual-emit or alias through a window | Rename in a single deploy |
| Gate removal on zero-consumption telemetry | Remove because "we announced it" |
| Make consumers forward-compatible | Throw on unknown codes |
| Version meaning via a new code | Repurpose an existing code |

## Anti-patterns in the wild

1. **The Vendor Passthrough** — using `stripe_card_declined` as your code.
2. **The SQLSTATE Leak** — `PG_23505` exposed to clients.
3. **The Duplicate Twin** — `USER_NOT_FOUND` and `USER_DOES_NOT_EXIST`.
4. **The Wiki Registry** — a doc that lagged the code months ago.
5. **The Invisible Code** — thrown but never registered; maps to `500`.
6. **The Silent Rename** — no alias, broke an old mobile app.
7. **The Enumeration Split** — distinct auth codes reveal which emails exist.

## Chapter checklist

- [ ] Every code is behavior-derived and stable.
- [ ] Every code is registered exactly once.
- [ ] Uniqueness, format, and reserved domains are enforced in CI.
- [ ] Every code has HTTP, retry, action, message, owner, and visibility.
- [ ] Internal codes map to a public alias.
- [ ] Deprecation uses aliases/dual-emit gated on telemetry.
- [ ] A static scan catches thrown-but-unregistered codes.

## Related

- [Chapter 8 Reference](../05-reference/README.md)
- [The Sample Error Registry](../03-practical-examples/01-sample-error-registry.md)
- [Error-Handling Patterns and Anti-Patterns](../../../part-17-organization/46-error-handling-patterns-and-anti-patterns/README.md)
