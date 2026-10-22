# Chapter 14 — Do's and Don'ts

> Part V · Chapter 14 · All sections (14.1–14.18)

A condensed rule set for resource cleanup and failure-safe execution. Use it as a code-review
checklist.

## Acquire and release

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Acquire and release in the same scope | Acquire here, release in a caller |
| Register release immediately after acquire | Release only on the happy path |
| Use `finally`/`using`/`with`/`defer` | Hand-roll release at end of function |
| Acquire before the cleanup scope | Acquire inside `try` then release in `finally` |
| Use LIFO for nested resources | Release in acquisition order |

## Per-resource discipline

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Return connections to the pool in `finally` | Hold a connection across unrelated awaits |
| Rollback on failure, commit on success | Close a transaction without rollback |
| Flush then close streams | Close without flushing |
| Delete partial temp files on every path | Delete only on success |
| Gracefully close sockets; respect `Connection: close` | Abort sockets mid-response |

## Locks and temporary resources

| ✅ Do | ❌ Don't |
| ----- | -------- |
| `defer`/`with` lock release immediately | Release a lock manually at the end |
| TTL + fencing on distributed locks | Hold a distributed lock indefinitely |
| Delete temp dirs/files in `finally` | Leave scratch dirs on failure |
| Add a periodic sweeper | Assume cleanup always runs |
| Avoid holding locks across slow calls | Serialize a pool on a slow dependency |

## Errors during cleanup

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Keep the first failure as primary | Let cleanup overwrite the primary |
| Attach cleanup failures as suppressed | Discard cleanup failures |
| Wrap cleanup in its own try | Let cleanup throw over the primary |
| Cap aggregated/suppressed errors | Attach unbounded error lists |

## Cancellation, timeouts, idempotency

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Give cleanup its own short deadline | Reuse the expired request deadline |
| Use a detached context for cleanup | Let cancellation skip cleanup |
| Make release idempotent | Assume release runs exactly once |
| Bound shutdown cleanup within the grace period | Hang past `terminationGracePeriodSeconds` |
| CAS/token-check distributed lock release | `DEL` a lock unconditionally |

## Anti-patterns in the wild

1. **The Happy-Path Release** — release after the last statement; skipped on throw.
2. **The Overwriter** — plain `finally { close() }` that replaces the primary error.
3. **The Cancelled Cleanup** — cleanup on the request context, skipped on timeout.
4. **The Non-Idempotent Close** — a second close throws and hides the first failure.
5. **The Forever Lock** — a distributed lock with no TTL, held after a crash.
6. **The Temp Overflow** — scratch files deleted only on success.
7. **The Unbounded Shutdown** — cleanup that outlives the grace period and gets `SIGKILL`ed.

## Universal cleanup policy (adopt verbatim)

> Every acquired resource is released by its acquirer, in the same scope, using the language's
> scope mechanism, with a bounded independent (detached) deadline, on every exit path including
> panic and cancellation, idempotently; and cleanup failures are attached as suppressed to the
> primary error.

## Chapter checklist

- [ ] Every acquire has a scoped release.
- [ ] Cleanup runs on throw, panic, cancel, and timeout.
- [ ] Cleanup uses a detached, bounded deadline.
- [ ] Release is idempotent.
- [ ] Primary errors survive cleanup failures.
- [ ] Sweepers backstop crash residue.

## Related

- [Chapter 14 Reference](../05-reference/README.md)
- [Chapter 13 — Catch Blocks and Recovery Logic](../../13-catch-blocks-and-recovery-logic/README.md)
- [Chapter 12 — Exception Propagation](../../12-exception-propagation-and-control-flow/README.md)
