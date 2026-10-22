# Chapter 47 — Reference

> Part XVIII · Chapter 47 · Cheat sheets, the language matrix, and the chapter glossary.

## The language matrix

| Language | Mechanism | Native chaining | Typed catching | Async construct | Fatal handling |
| -------- | --------- | --------------- | -------------- | --------------- | -------------- |
| **JS/TS** | `throw` (any value) | `new Error(msg, { cause })` (ES2022) | `instanceof` (realm-fragile) — prefer `code`/`name` | `Promise`, `async/await`, `AbortSignal` | Unhandled rejection = fatal (Node ≥ 15) |
| **Node.js** | `throw` + error-first callbacks | `Error.cause`; `err.code` on system errors | `err.code` (`ENOENT`, `ECONNRESET`) | `unhandledRejection` event, streams | `unhandledRejection` throws by default |
| **Python** | `raise` (runtime hierarchy) | `raise X from Y` → `__cause__` | `except SpecificError` (no static checking) | `asyncio`, `TaskGroup` (3.11), `gather` | Uncaught exception exits the process; `CancelledError` is a `BaseException` |
| **Java** | Exceptions (checked + unchecked) | `(msg, cause)` ctor, `initCause`, `addSuppressed` | `catch (A \| B e)`; sealed + pattern `switch` (21) | `CompletableFuture`, `ExecutorService` | Uncaught exception kills the thread; `Error` is fatal by design |
| **Go** | `error` interface returned in-band | `fmt.Errorf("…: %w", err)` | `errors.Is` / `errors.As` (Go 1.13) | Goroutines, `context`, `errgroup` | Unrecovered `panic` kills the process; `recover()` only in the same goroutine |
| **Rust** | `Result<T, E>` + `?` | `thiserror` `#[from]` / `#[source]`; `anyhow` `.context()` | Exhaustive `match` on an enum | `async`/`.await`, `tokio` | `panic!` unwinds (or aborts with `panic = abort`); `#[must_use]` on `Result` |
| **C#/.NET** | Exceptions | Inner-exception ctor; `ExceptionDispatchInfo` | `catch (T e) when (…)` filters; `AggregateException` | `Task`, `async/await`, `CancellationToken` | Unhandled exception in `async void` kills the process |
| **PHP** | `Throwable` (`Exception` + `Error`) | `parent::__construct($msg, 0, $previous)` | `catch (\Throwable)` at boundaries | Promises (library-level), fibers | Uncaught `Throwable` is a fatal error |
| **Kotlin** | Exceptions (all unchecked) + `Result<T>` | Manual `cause` property (no stdlib chaining) | `is` + exhaustive `when` over `sealed` types | Coroutines, `supervisorScope` | Uncaught exception cancels the scope, then reaches the `CoroutineExceptionHandler` |
| **Swift** | `throws`/`try` + `Result` | Store `underlying` in your error enum | `catch CheckoutError.cardDeclined` | `async`/`await`, `Task` | Uncaught `try!` failure traps the process |

## Idiom cheat sheet

### The one call that preserves the cause

| Language | Call | What it sets |
| -------- | ---- | ------------ |
| Go | `fmt.Errorf("ctx: %w", err)` | `Unwrap()` link — `Is`/`As` traverse it |
| Rust | `#[source]` field / `#[from]` variant | `Error::source()` link; `?` auto-converts |
| Python | `raise AppError(...) from exc` | `__cause__` (and suppresses `__context__`) |
| Java | `new AppError(msg, cause)` | `Throwable.getCause()` |
| C# | `new AppError(msg, inner)` / `throw;` | `InnerException`; `throw;` keeps the stack |
| TypeScript | `new Error(msg, { cause: err })` | `error.cause` (own, non-enumerable) |
| PHP | `new AppError($msg, 0, $previous)` | `getPrevious()` |
| Kotlin | `cause` property on your error class | Manual — no stdlib helper |
| Swift | `case unavailable(underlying: any Error)` | Manual — no stdlib helper |

### Classify, don't string-match

| Language | Identity test | Typed extraction | Never |
| -------- | ------------- | --------------- | ----- |
| Go | `errors.Is(err, ErrCardDeclined)` | `errors.As(err, &target)` | `strings.Contains(err.Error(), "declined")` |
| Rust | `matches!(e, CheckoutError::Declined)` | `match` / `if let` | `e.to_string().contains(...)` |
| Python | `except stripe.error.CardError` | `isinstance(exc, AppError)` | `if "declined" in str(exc)` |
| Java | `catch (CardDeclinedException e)` | `instanceof` + `getCause()` | `e.getMessage().startsWith(...)` |
| C# | `catch (CardDeclinedException ex) when (…)` | `ex is AppError` | `ex.Message.Contains(...)` |
| TypeScript | `err.code === "CARD_DECLINED"` | `err instanceof AppError` | `err.message.includes(...)` |
| PHP | `catch (CardDeclinedException $e)` | `$e instanceof AppError` | `str_contains($e->getMessage(), ...)` |
| Kotlin | `is AppError.Declined` | `when` over a sealed type | `(e as? AppError)?.message` |
| Swift | `catch AppError.declined` | `catch let e as AppError` | `(error as NSError).code == 1` |

### The lint gate for each language's honesty gap

| Language | Gap | Gate |
| -------- | --- | ---- |
| Go | Errors received but not checked | `errcheck` / `staticcheck` in CI; `shadow` linter for shadowed `err` |
| Rust | `Result` discarded; `unwrap` in prod | `#![deny(warnings)]`, `clippy::unwrap_used` denied outside tests |
| TypeScript | `catch` var untyped; floating promises | `strict` (`useUnknownInCatchVariables`), `no-floating-promises` |
| Python | Bare `except:`; broad `except Exception` | `flake8`/`ruff` rules; `mypy --strict` |
| Java | `catch (Exception)`/`catch (Throwable)` | Error Prone / Checkstyle rules; sealed types for exhaustiveness |
| C# | `catch (Exception)`; `async void` | Roslyn analyzers (CA1031, CA2007, VSTHRD103) |
| Kotlin | `runCatching` swallowing cancellation | Detekt `TooGenericExceptionCaught`; explicit `CancellationException` rethrow |
| Swift | `try!` on external input | SwiftLint `force_try`/`force_unwrapping` |
| PHP | `catch (Exception)` missing engine errors | PHPStan rules; `catch (\Throwable)` at boundaries |

### Cancellation is not failure

| Language | Cancellation signal | Terminal state |
| -------- | -------------------- | -------------- |
| JS/TS | `AbortError` (`code: "ABORT_ERR"`) | `cancelled` |
| Python | `asyncio.CancelledError` (a `BaseException` since 3.8) | `cancelled` |
| Go | `context.Canceled` / `context.DeadlineExceeded` | `cancelled` / `timeout` |
| Java | `InterruptedException` / `CancellationException` | `cancelled` |
| C# | `OperationCanceledException` (check `ct.IsCancellationRequested`) | `cancelled` |
| Rust | `tokio::task::JoinError` with `is_cancelled()` | `cancelled` |
| Kotlin | `CancellationException` | `cancelled` |
| Swift | `CancellationError` | `cancelled` |
| PHP | `Error` from an aborted fiber | `cancelled` |

## Error object fields worth carrying

| Field | Why | Present in |
| ----- | --- | --- |
| `code` | Stable, machine-readable, survives messages | All |
| `category` / `severity` | Drives retry, alerting, and status mapping | All |
| `retryable` | The single most consequential boolean | All |
| `ambiguous` | The outcome is unknown (timeouts on side effects) | Payment-like flows |
| `cause` | The original vendor/driver error, traversable | All (see cheat sheet above) |
| `requestId` / `correlationId` | Joins logs across services | All |
| `providerRequestId` | The vendor's own id — what support will ask for | External-API flows |
| `safeContext` | Allow-listed metadata only | All |
| `timestamp` / `durationMs` | Timing evidence for SLOs and incidents | All |

## Chapter glossary

| Term | Meaning |
| ---- | ------- |
| Exception-first | A language whose primary failure mechanism is throwing (`Java`, `C#`, `Python`, `PHP`, `JS/TS`, `Kotlin`, `Swift`) |
| Result-first | A language whose primary mechanism returns a failure value (`Go`, `Rust`) |
| Out-of-band signal | Failure delivered past the return type — the caller must be told by a `catch` |
| In-band signal | Failure delivered in the signature as a value (`Result<T, E>`, `(T, error)`) |
| Cause chain | The linked sequence of errors from the original failure up to the boundary error |
| Sibling set | Parallel failures held together (`errors.Join`, `AggregateError`, `ExceptionGroup`, `addSuppressed`) |
| Typed catching | Selecting a failure by type or code rather than by message text |
| Honesty spectrum | How much of error handling the compiler enforces, per language |
| Total classifier | A lookup that produces a decision for every input, including unknown ones |
| Ambiguous outcome | A failure where the side effect may or may not have happened |
| Floating promise | A promise nobody awaits or catches — a detached failure |
| Typed-nil interface | Go's interface holding a nil pointer: `err != nil` is true, dereferencing panics |
| `#[must_use]` | Rust's compiler warning when a `Result` is discarded |
| `useUnknownInCatchVariables` | TypeScript's strict flag typing a `catch` variable as `unknown` |

## Signposts

- Mechanism families in depth → [Exceptions vs Explicit Returns](../01-concepts/01-exceptions-vs-returns.md)
- Per-language survey cards → [Language Comparison at a Glance](../01-concepts/02-language-comparison-at-a-glance.md)
- Async constructs and cancellation → [Async Constructs and Common Pitfalls](../01-concepts/05-async-constructs-and-pitfalls.md)
- Chaining APIs → [Native Chaining and Wrapping Capabilities](../02-deep-dive/01-native-chaining-and-wrapping-capabilities.md)
- Type-safety spectrum → [Type-Safe Handling and the Common Architecture](../02-deep-dive/02-type-safe-handling-and-common-architecture.md)
- Rules per family → [Chapter 47 Do's and Don'ts](../04-dos-and-donts/README.md)
- Framework layer → [Chapter 48 — Framework and Runtime Integration](../../48-framework-and-runtime-integration/README.md)
- Shared vocabulary → [Glossary](../../../GLOSSARY.md)

## Related

- [Chapter 47 Do's and Don'ts](../04-dos-and-donts/README.md)
- [Chapter 47 Overview](../README.md)
- [Part XVIII Index](../../README.md)
