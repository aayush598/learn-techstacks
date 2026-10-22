# Chapter 14 — Reference

> Part V · Chapter 14 · Cheat sheet, resource checklist, and chapter glossary.

## Cheat sheet — the cleanup lifecycle

```text
acquire ─▶ register release ─▶ use ─▶ release (scope end)
              │                         ├─ success  ─▶ release
              │                         ├─ throw    ─▶ release (during unwind)
              │                         ├─ panic    ─▶ release (defer/Drop)
              │                         ├─ cancel   ─▶ release (detached ctx / shield)
              │                         └─ timeout  ─▶ release (detached ctx / shield)
              └─ release failure ─▶ attach as SUPPRESSED to the primary
```

## Scoped mechanism comparison

| Language | Mechanism | Order | On panic? | Close error behavior |
| -------- | --------- | ----- | --------- | -------------------- |
| Java | try-with-resources | LIFO | via finally | suppressed by primary |
| C# | `using` / `await using` | LIFO | via finally | aggregated |
| Python | `with` / `async with` | LIFO | yes | `__exit__` decides |
| Go | `defer` | LIFO | yes | you decide (Join/suppress) |
| JS/TS | `try/finally`, `using` | LIFO (using) | yes (finally) | you decide |
| Rust | `Drop` (RAII) | LIFO | yes | no throw in Drop |

> `defer`/`Drop` do not run on hard exit (`os.Exit`, `SIGKILL`). Use a sweeper as backstop.

## Resource release checklist

| Resource | Release action | Failure release | Idempotency |
| -------- | -------------- | --------------- | ----------- |
| DB connection | return to pool | return to pool | yes (pool tracks) |
| Transaction | `COMMIT` | `ROLLBACK` | guard by state |
| File handle | `close` | `close` | close-if-open |
| Stream | `flush` + `close` | best-effort flush + close | close-if-open |
| Network socket | graceful close/return | abort | yes |
| Mutex/RLock | `unlock`/scope | scope release | do not double-unlock |
| Semaphore | `release`/scope | scope release | flag-guard |
| Distributed lock | CAS release / TTL | lease expiry | token-checked |
| Temp file/dir | `remove`/recursive delete | same | force/ignore-missing |
| Multipart upload | complete or abort | abort | abort-if-exists |

## Decision table — cleanup failure handling

| Situation | Action |
| --------- | ------ |
| Body failed, cleanup failed | Throw primary; attach cleanup as suppressed |
| Body succeeded, cleanup failed | Report cleanup failure (it is the only failure) |
| Cleanup would hang | Bound with a deadline; log if exceeded |
| Request cancelled, cleanup pending | Run cleanup on a detached context/shield |
| Cleanup called twice | No-op if already released |
| Crash skipped cleanup | Sweeper deletes residue later |

## Cheat sheet — preserve the primary by language

| Language | Attach secondary |
| -------- | ---------------- |
| Java | `primary.addSuppressed(secondary)` |
| Go | `errors.Join(primary, wrap(secondary))` |
| Python | `primary.add_note(...)` (3.11+) / `__context__` |
| TypeScript | `suppressed` field on the thrown error |
| C# | `Exception` + inner; `AggregateException` for many |

## Universal cleanup policy

> Every acquired resource is released by its acquirer, in the same scope, via the language's scope
> mechanism, with a bounded detached deadline, on every exit path (success, throw, panic, cancel,
> timeout), idempotently; cleanup failures are attached as suppressed to the primary error.

## Chapter glossary

| Term | Meaning |
| ---- | ------- |
| Acquire/release | Obtain and return a bounded resource |
| Guaranteed cleanup | Release on every exit path |
| Scoped management | Release tied to a lexical block |
| finally-style | Run-regardless block |
| Detached cleanup | Release using a fresh, bounded context |
| Idempotent cleanup | Safe to run more than once |
| Primary error | The first/operation failure |
| Suppressed error | A secondary failure attached to the primary |
| Leak | A resource never released |
| Sweeper | A periodic job cleaning crash residue |

## Signposts

- Recovery logic → [Ch. 13](../../13-catch-blocks-and-recovery-logic/README.md)
- Propagation → [Ch. 12](../../12-exception-propagation-and-control-flow/README.md)
- Transactions and rollback → [Ch. 23](../../../part-09-database-and-transactions/23-transaction-and-rollback-error-handling/README.md)
- Process/runtime failures → [Ch. 41](../../../part-15-distributed-failures/41-process-runtime-and-resource-failures/README.md)

## Related

- [Chapter 14 Do's and Don'ts](../04-dos-and-donts/README.md)
- [Chapter 14 README](../README.md)
- [Part V Index](../../README.md)
