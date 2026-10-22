# Chapter 16 — Do's and Don'ts

> Part VI · Chapter 16 · All sections

A condensed rule set distilled from the chapter. Use it as a translation review checklist.

## Why and where to translate

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Translate at the boundary, once | Translate at every consumer |
| Define one canonical error shape | Let each subsystem invent its own |
| Translate inbound dialects into the domain | Let driver/vendor types into the domain |
| Have an explicit outbound domain→transport map | Guess HTTP statuses per handler |

## The seven directions

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Give each direction a named translation function | Mix directions (domain→DB, SQL→user) |
| Classify native errors by context (user vs provider) | Map every `TypeError` to `400` |
| Map DB constraints to precise domain codes | Collapse all DB errors into one |
| Map vendor → stable internal codes | Leak `card_error`/`SlowDown` to clients |
| Extract framework field details | Drop actionable validation detail |
| Preserve `code`+`cause` into the DLQ | Store an unhelpful `"failed"` |
| Classify OS `errno` transient vs permanent | Treat all I/O errors the same |

## Preserving information

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Attach the original error as `cause` | `throw new Error("failed")` in a catch |
| Carry `transient` + `retryAfterMs` | Default to retryable, or drop retry hints |
| Keep field details, requestId, tenantId | Replace detailed errors with a generic one |
| Keep chains to 2–4 links | Wrap at every layer |
| Keep `cause` server-side only | Serialize the cause tree to clients |

## Avoiding overgeneralization and unknowns

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Map at the class level; detail in `meta` | One `DB_ERROR`/`PROVIDER_ERROR` for everything |
| Have an explicit unknown branch | `default: throw err` inside a translator |
| Default unknown 5xx → transient, 4xx → permanent | Default everything to retryable |
| Log/alert unmapped codes | Silently pass raw payloads through |
| Make clients fall back to status for unknown codes | Crash on an unrecognized code |

## Tables, cycles, and versioning

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Keep mappings in one declarative table | Scatter inline `switch` mappings |
| Co-locate policy (retry/alert/degrade) with mapping | Recompute policy ad hoc |
| Test entries + coverage + ordering | Let unknowns fall through silently |
| Refuse to re-wrap normalized errors | Build circular `cause` chains |
| Add/deprecate codes; snapshot the public map | Rename/remove/redefine a public code |

## Anti-patterns in the wild

1. **The Leaky Translator** — passes the raw vendor body through "to be helpful."
2. **The Collapser** — maps every DB/provider error to one vague code.
3. **The Throwing Translator** — `default: throw err`, so handling fails during handling.
4. **The Cause Amnesiac** — rethrows a new error with no chained `cause`.
5. **The Retry Eraser** — translates transient errors without the `transient` flag.
6. **The Cycle Weaver** — a generic `wrap()` that re-wraps normalized errors into a loop.
7. **The Redefiner** — changes an existing code's meaning/status in place.

## Chapter checklist

- [ ] Exactly one canonical error shape exists.
- [ ] Every inbound dialect has a translation function.
- [ ] Every translation preserves `cause` and retry class.
- [ ] Unknown codes get a safe branch and an alert.
- [ ] Mappings live in a table with coverage tests.
- [ ] No circular chains; depth ≤ 4.
- [ ] Public mappings are snapshot-tested and versioned.

## Related

- [Chapter 16 Reference](../05-reference/README.md)
- [Translation Directions](../01-concepts/02-translation-directions.md)
- [Part XVII — Error-Handling Patterns and Anti-Patterns](../../../part-17-organization/46-error-handling-patterns-and-anti-patterns/README.md)
