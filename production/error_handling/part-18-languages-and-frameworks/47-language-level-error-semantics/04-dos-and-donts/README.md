# Chapter 47 — Do's and Don'ts

> Part XVIII · Chapter 47 · All sections (47.1–47.16)
>
> A condensed rule set distilled from the chapter, organized by language family. Use it as a
> review checklist and as the language-specific half of your team's error-handling standard.

## Choosing the mechanism

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Pick one mechanism per function — throw *or* return a result | Let one function half-throw and half-return the same condition |
| Encode expected business failures as values (decline, conflict, quota) | Throw an exception for `CARD_DECLINED` and also return a decline code |
| Throw only for exceptional or unrecoverable-at-this-layer conditions | Use exceptions as the primary business API in Go or Rust |
| Write the rule down once and apply it to every module | Let each developer pick per function |

## Exception-first families — Java, C#, Kotlin, Swift, PHP, JS/TS

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Catch the narrowest type that you can actually handle | `catch (Exception e)` / `catch (Throwable t)` in business code |
| Rethrow anything you do not recognize, unchanged | Log-and-continue in a catch that produces a wrong success |
| Preserve the cause with the language's native chaining API | Re-throw `new Error(e.message)` / `throw new Exception(ex.Message)` |
| Use `throw;` (C#) or `ExceptionDispatchInfo` to rethrow | `throw ex;` — it resets the stack trace to the rethrow site |
| Catch `Throwable` at PHP boundaries | Catch `Exception` and let engine `Error`s bypass your handler |
| Never catch `Error`/`OutOfMemoryError` in Java or PHP | Swallow `Error` and keep a dying process alive |
| Use `throw;`/`from`/`cause` chains, then log the whole chain | Log only the outermost message |

## Result-first families — Go, Rust

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Check **every** returned error; enforce with `errcheck`/`staticcheck` | Write `if err != nil { /* ignore */ }` and hope review catches it |
| Wrap with `%w` (Go) so `errors.Is`/`errors.As` still work | `fmt.Errorf("…: %s", err)` — it flattens the chain to prose |
| Use `thiserror` enums for errors callers must branch on | Mix `anyhow::Result` into a library signature |
| Use `anyhow` + `.context()` in binaries and glue code | `anyhow` in a public API — callers lose the ability to match |
| Propagate with `?` and one `#[from]`/`#[source]` link per boundary | `map_err(\|e\| format!("{e}"))` — the typed cause is gone |
| Treat `panic`/`unwrap`/`expect` as bug signals only | `unwrap()` on I/O in a request path or worker loop |
| Return `panic` for a business decline | Panic on a business outcome in a Go server |

## Dynamic families — Python, JavaScript/TypeScript

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Catch specific exception classes and re-raise the rest | Bare `except:` or `except BaseException:` |
| Re-raise `asyncio.CancelledError` explicitly | Swallow cancellation in `except Exception:` around `await` |
| Use `raise X from exc` at every library boundary | `raise AcmeError(str(exc))` — flattens and mislabels the relationship |
| Await every promise; enable `no-floating-promises` | `void doWork()` with no `.catch` — a silent rejection |
| Use `for…of` + `await` for sequential async work | `forEach(async …)` — the handler returns before the work finishes |
| Match Node system errors on `err.code` | Match on `err.message` substrings |
| Match error classes on `code`/`name` when crossing bundles | `instanceof MyError` across realms, workers, or duplicate packages |

## The pitfall catalog (the 46-equivalent traps)

Each row is a real production incident shape, not a style preference.

| Pitfall | Language | Symptom in production | Fix |
| ------- | -------- | --------------------- | --- |
| **Swallowed exception** | Java, C#, PHP, Python | Operation reports success; data silently missing | Rethrow unknown types; make the catch block either recover or propagate |
| **Empty catch / log-only catch** | C#, Java, Python | "Handled" errors never reach metrics or the client | Log *and* rethrow; boundary catches are the only exception |
| **Bare `except:`** | Python | `KeyboardInterrupt`, `SystemExit`, `CancelledError` all swallowed; shutdown hangs | `except Exception:` plus an explicit re-raise of `CancelledError` |
| **Floating promise** | JS/TS, Node.js | `unhandledRejection`; work vanishes after the response is sent | `await`/`return` it, or push it to a queue you own |
| **Typed-nil in an interface** | Go | `err != nil` is **true** for a nil pointer stored in an `error`; the next `err.Error()` panics | Return an untyped `nil` on the error slot, or never return a typed nil pointer |
| **`unwrap()` in production** | Rust | One malformed payload or flaky socket panics the worker; the job is redelivered forever | `map_err` to a typed variant; reserve `unwrap` for tests and local invariants |
| **Shadowed `err`** | Go | `if err := f(); err != nil` hides the outer error; a real failure reads as success | Assign with `=`; enable `shadow` linters |
| **Wrong-status retry** | All | `400`/`402`/`409` retried; the outage amplifies itself | Retry only transient classes, per the registry |
| **Cause flattened to a string** | All | Support tickets have no vendor request id; diagnosis becomes guesswork | Wrap the object, then copy structured fields explicitly |
| **Cancellation classified as failure** | All | Client disconnects logged as `500`; cancelled jobs retried and re-charged | Map cancellation to its own terminal state; never retry it |
| **Async wrapper classified, not unwrapped** | Java, C#, Python | `CompletionException`/`AggregateException` hides the real cause | Unwrap before classifying; keep the sibling set for parallel work |
| **`runCatching` in a coroutine** | Kotlin | Cancellation swallowed; the scope never completes | Rethrow `CancellationException` |

## The Go typed-nil trap, in full

This one deserves its own block because it passes code review, passes `go vet`, and still
crashes production.

```go
type CheckoutError struct{ Code string }

func (e *CheckoutError) Error() string { return e.Code }

// Somewhere deep in a stack:
func loadTenant(id string) (*Tenant, error) {
    t, err := repo.Find(id)
    if err != nil {
        return nil, &CheckoutError{Code: "TENANT_NOT_FOUND"}   // fine
    }
    return t, nil
}

// The trap: a typed nil pointer assigned to the error interface.
func findOrNil(id string) error {
    var tenant *Tenant            // nil pointer
    if tenant == nil {
        return tenant             // ← error interface now holds (*Tenant)(nil): NOT nil
    }
    return nil
}

// At the caller:
err := findOrNil("t_1")
if err != nil {                 // true! err is non-nil
    log.Println(err.Error())    // 💥 nil pointer dereference → panic
}
```

An `error` interface value is a **two-word pair**: a type pointer and a data pointer. `nil`
means *both* words are zero. Assigning a nil `*CheckoutError` sets the type word and leaves
the data word zero — the interface is **non-nil** but dereferencing it panics.

Two safe rules: return the **untyped** `nil` on the error slot, and return the zero value plus
an explicit `nil` instead of a typed nil pointer.

## Cross-language consistency

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Use the same stable error codes in every service | Invent per-language code strings |
| Generate per-language error types from one registry | Hand-maintain the same code list in five languages |
| Keep the registry lookup total — unknown code ⇒ safe default | Let an unknown code throw inside the classifier |
| Translate vendor errors in the adapter layer | Translate vendor errors at the HTTP boundary |
| Exclude cancellation and client disconnects from retry classification | Retry everything that is "an error" |

## Anti-patterns in the wild

1. **The Universal Catch** — `catch (Exception e)` around business logic. Turns every failure
   into a logged string and a false success.
2. **The Flattened Cause** — `new Error(e.message)` / `raise AcmeError(str(exc))`. Root cause
   deleted at the first library boundary.
3. **The Detached Failure** — a floating promise, an un-awaited `async`, a goroutine with no
   error channel. The failure exists only in a log nobody reads.
4. **The Panic-as-Control-Flow** — `unwrap()`/`panic!` used for "this should not happen", on
   paths that external input can reach.
5. **The Interface Trap** — Go's typed-nil error. `err != nil` lies.
6. **The Two-Semantics Function** — a function that throws for one failure and returns a
   result for another. Half of the callers are wrong.

## Chapter checklist

- [ ] Does every function use exactly one failure mechanism, stated in its signature?
- [ ] Is every catch clause either handling a specific type or an owned boundary that maps to `500`?
- [ ] Does every Python `raise` across a boundary use `from`?
- [ ] Is every Go error checked in CI (`errcheck`) and wrapped with `%w`?
- [ ] Are `unwrap`/`expect`/`panic!` confined to tests and provably local invariants?
- [ ] Does every C# rethrow use `throw;` or `ExceptionDispatchInfo`?
- [ ] Are floating promises, bare `except:`, `async void`, and `GlobalScope` banned by lint?
- [ ] Is cancellation classified as cancellation, never as a failure, in every language?
- [ ] Do all services emit the same stable error codes from one registry?
- [ ] Can the classifier survive an error type it has never seen?

## Related

- [Chapter 47 Reference](../05-reference/README.md)
- [Chapter 48 — Framework and Runtime Integration](../../48-framework-and-runtime-integration/README.md)
- [Chapter 46 — Error-Handling Patterns and Anti-Patterns](../../../part-17-organization/46-error-handling-patterns-and-anti-patterns/README.md)
- [Chapter 13 — Catch Blocks and Recovery Logic](../../../part-05-exception-mechanics/13-catch-blocks-and-recovery-logic/README.md)
