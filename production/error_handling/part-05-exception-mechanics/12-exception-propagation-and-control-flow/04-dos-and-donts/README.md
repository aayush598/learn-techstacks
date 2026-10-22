# Chapter 12 — Do's and Don'ts

> Part V · Chapter 12 · All sections (12.1–12.20)

A condensed rule set for propagation and control flow. Use it as a code-review checklist.

## Choosing where to catch

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Catch only where the fallback differs from propagating | `try/catch` every function |
| Translate at the boundary, not in the domain | Catch driver errors in domain code |
| Let unexpected errors reach the outermost handler | Swallow unknown errors mid-stack |
| Catch at the lowest frame that can act | Assume the nearest catch is correct |

## Wrapping and preserving cause

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Wrap with the operation name | Write "something failed" |
| Attach `cause` / `raise … from` / `%w` | Re-create the error with no cause |
| Rethrow the original object when unchanged | `throw new Error(err.message)` |
| Attach recovery failures as suppressed | Overwrite the primary with the recovery error |
| Log the structured chain once | `log("error: " + err)` |

## Sync, async, and concurrency

| ✅ Do | ❌ Don't |
| ----- | -------- |
| `await` / `.catch` every promise | Fire-and-forget unless truly best-effort |
| Check the callback `err` first | Use a result before checking `err` |
| Attach an `'error'` listener | Emit `'error'` with no listener |
| Recover or join detached goroutines | `go func(){}()` with no recover/join |
| Declare fail-fast vs collect-all | Default to `Promise.all` everywhere |
| Cancel loser branches in a race | Leave orphaned work running |

## Avoiding silent defects

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Order catches most-specific first | Catch `Exception`/`Error` first |
| Distinguish "none" from "failed" | Return `null` for both |
| Report partial success explicitly | Mark a job `completed` regardless |
| Use results for high-rate expected failures | Throw per invalid field in bulk |

## Anti-patterns in the wild

1. **The Masker** — `throw new Error("failed")` erasing the cause at every layer.
2. **The Lost Promise** — an unawaited async call whose rejection never surfaces.
3. **The Detached Bomb** — a goroutine that panics and kills the process.
4. **The Broad First Catch** — a supertype handler that makes subtype handlers dead code.
5. **The Optimistic Default** — `catch { return [] }` turning an outage into "empty".
6. **The Log-and-Rethrow Duplicator** — catching only to log, at every layer.
7. **The String Logger** — `"error: " + err`, discarding structure and cause.

## Chapter checklist

- [ ] Every error has a named catch frame.
- [ ] Every wrapper preserves cause.
- [ ] No unawaited promise or unjoined goroutine on the failure path.
- [ ] Catches are ordered most-specific first.
- [ ] Partial successes are reported as partial.
- [ ] Exactly one retry owner per operation.

## Related

- [Chapter 12 Reference](../05-reference/README.md)
- [Chapter 13 — Catch Blocks and Recovery Logic](../../13-catch-blocks-and-recovery-logic/README.md)
- [Error-Handling Patterns and Anti-Patterns (Part XVII)](../../../part-17-organization/46-error-handling-patterns-and-anti-patterns/README.md)
