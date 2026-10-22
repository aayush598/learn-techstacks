# Chapter 13 — Do's and Don'ts

> Part V · Chapter 13 · All sections (13.1–13.17)

A condensed rule set for catch blocks and recovery. Use it as a code-review checklist.

## Should this catch exist?

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Catch with a stated purpose | Catch to "be safe" |
| Propagate required operations | Fallback a required operation silently |
| Catch optional features locally | Put optional work on the critical path |
| Log once at the boundary | Catch-log-rethrow at every layer |
| Model frequent expected failures as results | Throw/catch them per item |

## What to catch

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Catch the most specific type | Catch `Exception`/`Error`/bare first |
| Order handlers most-specific first | Put the broad handler above specific ones |
| Discriminate on type or stable code | Match human-readable `message` text |
| Keep an unknown branch that rethrows | Assume a wildcard covers everything |
| Group by policy, not by module | Group `DBError` (mixes transient + permanent) |

## What to do inside catch

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Verify preconditions before recovery | Retry on hope |
| Check idempotency before retrying | Retry non-idempotent side effects |
| Roll back / reset to known-good state | Retry on top of dirty state |
| Rethrow after partial recovery | Report success after undoing a step |
| Translate to a domain result at the boundary | Let infra errors leak into the domain |
| Bound retries by attempts AND deadline | Retry until it works |

## Recovery failure and recursion

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Wrap recovery in its own try | Let recovery throw over the primary |
| Attach recovery failure as suppressed | Discard the recovery error |
| Use a bounded loop for retry | Recurse into the failing function |
| Guard fallbacks against re-entry | Let a fallback re-enter the same catch |
| Preserve the primary error | Throw the secondary as the main failure |

## Anti-patterns in the wild

1. **The Empty Catch** — `catch {}` / `except: pass`; failure vanishes.
2. **The Black Hole** — `catch (e) { return null }`; outage looks like "not found".
3. **The Catch-All** — `catch (Exception)` hiding bugs and cancellation.
4. **The Duplicator** — log-and-rethrow at every layer.
5. **The Overwriter** — recovery error replaces the primary.
6. **The Infinite Healer** — recursive retry with no bound.
7. **The Optimist** — "recovered" reported after a partial undo.

## Chapter checklist

- [ ] Every catch has a purpose.
- [ ] Catches are specific and ordered.
- [ ] Unknown errors are logged and rethrown.
- [ ] Recovery checks its preconditions.
- [ ] Retries are bounded and idempotent.
- [ ] Recovery failures are suppressed, not fatal to the primary.
- [ ] Partial recovery rethrows.

## Related

- [Chapter 13 Reference](../05-reference/README.md)
- [Chapter 12 — Exception Propagation](../../12-exception-propagation-and-control-flow/README.md)
- [Chapter 14 — Resource Cleanup](../../14-resource-cleanup-and-failure-safe-execution/README.md)
