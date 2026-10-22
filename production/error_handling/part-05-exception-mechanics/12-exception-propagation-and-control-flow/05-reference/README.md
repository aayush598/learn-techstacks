# Chapter 12 — Reference

> Part V · Chapter 12 · Cheat sheet, decision tables, and chapter glossary.

## Cheat sheet — the propagation path

```text
detect ──▶ unwind frames ──▶ handler? ──yes──▶ catch (recover/translate/wrap)
                                │no
                                ▼
                          top of stack ──▶ default handler (500 / crash / unhandled)
```

**Wrap rule:** add context above, keep cause below. **Catch rule:** only where the fallback
differs.

## Decision table — catch, wrap, or let it go?

| Situation | Action |
| --------- | ------ |
| Can recover with a safe fallback | Catch and recover (Ch. 13) |
| At a boundary (transport/domain edge) | Catch and translate, preserve cause |
| Can only add context | Wrap with operation name + cause, rethrow |
| Cannot do anything useful | Do nothing; let it propagate |
| Handling cleanup only | `finally`/`defer`; rethrow original |

## Decision table — concurrent collection strategy

| Need | Mechanism | Failure behavior |
| ---- | --------- | ---------------- |
| All steps required | `Promise.all` / `errgroup.Wait` | First failure; siblings may run |
| All outcomes needed | `Promise.allSettled` / `errors.Join` | Collect every result |
| Fastest result | `Promise.race` / first-success | Losers unobserved |
| Sequential + ordered | `for … await` / loop | Stop or continue per policy |

## Cheat sheet — preserving cause by language

| Language | Wrap | Traverse | Retry check |
| -------- | ---- | -------- | ----------- |
| TypeScript | `new E(msg, { cause })` | walk `err.cause` | `instanceof` / `code` |
| Python | `raise E(...) from e` | `__cause__` | `except Subtype` |
| Go | `fmt.Errorf("...: %w", err)` | `errors.Is/As` | `errors.As` |
| Java | `new E(msg, cause)` | `getCause()` | `catch (Subtype)` |
| Rust | `anyhow::Context` / `#[source]` | `source()` | `match` variant |

## Cheat sheet — async observers

| Construct | Observer | Missing observer → |
| --------- | -------- | ------------------ |
| Promise | `await` / `.catch` | unhandled rejection |
| Callback | check `err` | silent `undefined` result |
| EventEmitter | `'error'` listener | process throw |
| Goroutine | `recover` / join | process panic |
| `CompletableFuture` | `exceptionally`/`handle` | dropped throwable |
| `asyncio.Task` | `await` / `add_done_callback` | "never retrieved" |

## Decision table — failure→success detection

| Code smell | Hidden failure | Fix |
| ---------- | -------------- | --- |
| `catch { return null }` | outage looks like "not found" | distinct result/throw |
| `catch { return [] }` | outage looks like "empty" | throw or discriminated result |
| Job marked `completed` on partial | data loss | record partial/failed |
| `200` + error body | client acts on invalid data | use `4xx`/`5xx` |

## Chapter glossary

| Term | Meaning |
| ---- | ------- |
| Unwinding | Discarding frames until a handler is found |
| Boundary | Frame where fallback differs from propagation |
| Wrapping | Adding context above a preserved cause |
| Masking | Discarding/replacing the original cause |
| Cause chain | Linked errors from origin to context |
| Unhandled rejection | A promise failure with no observer |
| Detached work | Async task the parent cannot observe |
| Fail-fast fan-out | Cancel siblings on first failure |
| Collect-all fan-out | Gather every outcome |
| Failure→success | Reporting a failure as a successful result |

## Signposts

- Recovery logic in depth → [Ch. 13 Catch Blocks](../../13-catch-blocks-and-recovery-logic/README.md)
- Cleanup on every path → [Ch. 14 Resource Cleanup](../../14-resource-cleanup-and-failure-safe-execution/README.md)
- Boundaries → [Ch. 15 Error Boundaries](../../../part-06-boundaries-and-translation/15-error-boundaries/README.md)
- Async at scale → [Ch. 31 Asynchronous Error Handling](../../../part-12-async-and-background-jobs/31-asynchronous-error-handling/README.md)

## Related

- [Chapter 12 Do's and Don'ts](../04-dos-and-donts/README.md)
- [Chapter 12 README](../README.md)
- [Part V Index](../../README.md)
