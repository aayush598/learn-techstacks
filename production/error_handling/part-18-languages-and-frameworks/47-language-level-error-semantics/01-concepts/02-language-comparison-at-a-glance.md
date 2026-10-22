# Language Comparison at a Glance

> Part XVIII · Chapter 47 · Sections 47.2–47.11 · _Estimated reading time: 22 min_
> **Prerequisite:** [Exceptions vs Explicit Returns](./01-exceptions-vs-returns.md)

## In one sentence

Ten languages, ten combinations of **primary mechanism, chaining API, type-safety level, and async
construct** — and the fastest way to write consistent code in a polyglot system is to know each
combination before you write the first line.

## Why this matters in production

Acme SaaS runs ingest in Go, the public API in TypeScript, billing in Java, AgentRun in Python,
and a Rust edge proxy. Without a shared comparison, every service re-invents error handling in
its local dialect and cross-service debugging becomes archaeology. With one comparison table as
the team's front page, "how does Go say this?" is a lookup, not a design meeting.

## The master comparison

| Language | Primary mechanism | Checked by compiler? | Native chaining | Async construct | Notable stdlib errors |
| -------- | ----------------- | -------------------- | --------------- | --------------- | ---------------------- |
| **JS/TS** | `throw` (untyped) | No (`unknown` in `catch` under strict) | `new Error(msg, { cause })` (ES2022) | Promises, `async/await`, `AbortSignal` | `TypeError`, `RangeError`, `AggregateError`, `DOMException` |
| **Node.js** | `throw` + error-first callbacks (legacy) | No | `Error.cause`; `err.code` on system errors | `unhandledRejection`, `EventEmitter` `'error'` | `ErrnoException` (`ENOENT`, `ECONNRESET`), `AbortError` (`ABORT_ERR`) |
| **Python** | `raise` (hierarchy of exceptions) | No | `raise X from Y` (sets `__cause__`) | `asyncio`, `TaskGroup` (3.11), `gather(return_exceptions=)` | `OSError`/`errno`, `ValueError`, `ExceptionGroup` (3.11) |
| **Java** | Exceptions (checked + unchecked) | Checked only (`Exception` ≠ `RuntimeException`) | Cause constructors, `initCause`, `addSuppressed` | `CompletableFuture`, `ExecutorService` | `IOException`, `SQLException`, `CompletionException` |
| **Go** | `error` values (interface) | Receipt forced; checking not | `fmt.Errorf(…, %w)` + `errors.Is/As` | Goroutines, `context`, `errgroup` | `io.EOF`, `context.Canceled`, `context.DeadlineExceeded` |
| **Rust** | `Result<T, E>` + `?` | Yes (`#[must_use]`, exhaustive `match`) | `thiserror` `#[from]`/`#[source]`; `anyhow` `.context()` | `async`/`.await`, `tokio`, `JoinError` | `std::io::Error`, `ParseIntError`, `JoinError` |
| **C#/.NET** | Exceptions | No | Inner-exception constructors; `ExceptionDispatchInfo` | `async/await`, `Task`, `CancellationToken` | `HttpRequestException`, `OperationCanceledException`, `AggregateException` |
| **PHP** | `Throwable` (`Exception` + `Error`) | No | `parent::__construct($msg, $code, $previous)` | Promises (libraries), fibers | `TypeError`, `ArgumentCountError`, `ValueError` |
| **Kotlin** | Exceptions (all unchecked) + `Result<T>` | No | Manual `cause` property (no stdlib chaining) | Coroutines, `CoroutineExceptionHandler` | `CancellationException`, `NumberFormatException` |
| **Swift** | `throws`/`try` + `Result` | `try` must be handled; typed `throws` (Swift 6) | Store `underlying` in the error type | `async`/`await`, `Task`, cancellation | `CancellationError`, `DecodingError`, bridged `NSError` |

## Survey cards

Each card is the minimum a working engineer needs before opening that language's codebase.

### 47.2 — JavaScript / TypeScript

- **Throw anything**: JS permits `throw "string"`, `throw 42`, `throw new Error(…)`. Production
  code standardizes on `Error` subclasses with a `code`.
- **No static contract**: nothing in a `.d.ts` says a function throws. TypeScript 4.4+'s strict
  mode types the `catch` variable as `unknown`, forcing you to narrow before use.
- **Chaining**: ES2022 `new Error("capture failed", { cause: err })`. Older code and most
  libraries still assign `.cause` manually or lose it.
- **Pitfall**: `instanceof CustomError` breaks across JS realms (iframes, `vm`, some bundlers)
  — match on `err.name`/`code` instead. See [pitfalls](./05-async-constructs-and-pitfalls.md).

```ts
class CheckoutError extends Error {
  constructor(message: string, readonly code: string, options?: { cause?: unknown }) {
    super(message, options);       // native cause (ES2022)
    this.name = "CheckoutError";
  }
}
```

### 47.3 — Node.js

- Same throw semantics as JS, plus **runtime-specific failure shapes**: system errors carry
  `err.code` (`ENOENT`, `ECONNREFUSED`, `ECONNRESET`), `err.errno`, `err.syscall`.
- **Unhandled promise rejections** terminate the process by default (Node ≥ 15,
  `--unhandled-rejections=throw`).
- An `EventEmitter` that emits `'error'` with no listener **throws** — a missing listener is a
  crash, not a silent drop.
- Legacy **error-first callbacks** `(err, result)` still appear in older SDKs; modern code
  prefers promises/`await`.

### 47.4 — Python

- Everything except `BaseException` subclasses is catchable; `Exception` is the workhorse
  hierarchy. Custom app errors subclass `Exception` (or an app base like `AcmeError`).
- **Chaining is native**: `raise CheckoutError(...) from stripe_err` sets `__cause__` and
  suppresses the implicit `__context__` chain; without `from`, Python chains *implicitly* but
  the traceback shows "During handling of the above exception."
- `except:` (bare) and `except BaseException:` are banned by every serious linter — they catch
  `KeyboardInterrupt`, `SystemExit`, and `asyncio.CancelledError`.
- **`ExceptionGroup` / `except*` (3.11)** for parallel failures; `asyncio.TaskGroup` uses it.

```python
try:
    receipt = stripe.capture(amount)
except stripe.error.CardError as exc:
    raise CheckoutError("CARD_DECLINED", retryable=False) from exc
```

### 47.5 — Java

- **Checked vs unchecked is the defining rule.** Checked (`Exception` subtypes other than
  `RuntimeException`): the compiler forces `catch` or `throws`. Unchecked: escape silently.
- **Cause chain** via `new AppException(msg, cause)` or `initCause`; try-with-resources
  auto-attaches `addSuppressed` for close failures.
- `try`-with-resources, multi-catch (`catch (A | B e)`) since Java 7; **sealed classes**
  (Java 17) enable exhaustive error hierarchies with pattern-matching `switch` (Java 21).
- Catching `Exception` or `Throwable` wholesale is the classic anti-pattern — it swallows
  `Error`s (`OutOfMemoryError`) you must never catch.

### 47.6 — Go

- **Errors are values**: the `error` interface with a single `Error() string` method. `nil` is
  the only "no error" — there is no sum type, so callers test `if err != nil`.
- **Wrapping**: `fmt.Errorf("load export %s: %w", id, err)`; inspection via `errors.Is(err,
  ErrNotFound)` and `errors.As(err, &target)` (both Go 1.13); multi-error `errors.Join` (Go
  1.20).
- **`panic` is for programmer errors** and unrecoverable states, not business outcomes; an
  unrecovered panic crashes the process.
- The compiler forces you to *receive* every error, not to *check* it — pair with `errcheck` or
  `staticcheck` (see [type safety](../02-deep-dive/02-type-safe-handling-and-common-architecture.md)).

### 47.7 — Rust

- **`Result<T, E>` is the only fallible return type**, and it is `#[must_use]`: ignoring it is a
  compiler warning (denial in most projects). `?` propagates; `match` handles exhaustively.
- **Two standard library-culture crates**: `thiserror` (define library error enums with
  `#[derive(Error)]`, `#[from]` for conversion) and `anyhow::Result` with `.context()` /
  `.with_context()` for application code that wants a context stack instead of a typed error.
- **`panic!`/`unwrap`/`expect` are for bugs**, not conditions. In a server, `unwrap` on a
  network result is a crash waiting for one flaky packet.
- `From` impls make `?` auto-convert error types — the cleanest "wrapping" in any language.

### 47.8 — C# / .NET

- Exceptions all the way down; no stdlib result type. Libraries (LanguageExt,
  CSharpFunctionalExtensions) supply `Result<T>` if the team wants in-band failures.
- **`throw;` preserves the stack; `throw ex;` resets it** to the rethrow site — a review-level
  rule in every .NET shop.
- **`ExceptionDispatchInfo.Capture(e).Throw()`** re-throws while keeping the original stack
  across `await`/thread boundaries (used by `Task` internals).
- Inner exceptions via constructors; `when` filters (`catch (Exception e) when (IsRetryable(e))`)
  keep catch clauses selective; `async void` is only for event handlers — anywhere else its
  exceptions crash the process unpredictably.

### 47.9 — PHP

- Since **PHP 7, `Throwable`** unifies the hierarchy: `Exception` (userland, throwable via
  `throw`) and `Error` (engine: `TypeError`, `ArgumentCountError`, `DivisionByZeroError`,
  `ValueError`, `AssertionError`). `catch (Throwable $e)` catches both — `catch (Exception $e)`
  misses engine errors.
- Chaining via the third constructor parameter: `new CheckoutException($msg, 0, $previous)`.
- PHP itself throws little; **frameworks (Laravel, Symfony) define the HTTP-adjacent
  hierarchies** you will actually catch. Warnings/notices are *not* exceptions unless a handler
  converts them.
- No checked exceptions; type declarations (`: void`, `: array`) constrain returns but never
  failures.

### 47.10 — Kotlin

- **All exceptions are unchecked** — Java's checked half is gone. `try` is an expression.
- **`Result<T>`** (stable since 1.5) with `runCatching { … }`, `getOrNull()`, `getOrElse`,
  `exceptionOrNull()`. ⚠️ `runCatching` catches `Throwable`, **including
  `CancellationException`** — rethrow it or coroutines stop cancelling correctly.
- Sealed error hierarchies (`sealed interface CheckoutFailure`) give exhaustive `when` — the
  idiomatic replacement for typed exceptions in API surfaces.
- Coroutine failures propagate to the `CoroutineExceptionHandler` at the scope root; a failing
  child cancels its sibling unless you use `supervisorScope`.

### 47.11 — Swift

- `throws` + `try`; the compiler **forces handling** (`try` must appear in a `do/catch`, be
  marked `try?` → optional, or `try!` → trap on failure).
- **`Result<Success, Failure: Error>`** (Swift 5) for composing fallible work; **typed throws**
  (Swift 6, SE-0413) lets `throws (CheckoutError)` appear in signatures.
- Pattern-match errors: `catch CheckoutError.cardDeclined { … }`, `catch let e as DecodingError`.
- Foundation `Error` values are often `NSError`-bridged; `localizedDescription` is the
  lossy user-facing string — keep your own `code` for contracts.

## Key data / numbers

- **ES2022** shipped `Error.cause`; before it, roughly every library rolled its own — check
  third-party errors still do.
- **Go 1.13** (2019) gave Go `%w`, `errors.Is`, `errors.As`; pre-1.13 Go code still shows
  `strings.Contains(err.Error(), …)` — never copy that pattern.
- **Python 3.11** (2022) added `ExceptionGroup` and `except*`; `asyncio.TaskGroup` builds on it.
- **Java 17** sealed classes + **Java 21** pattern-matching `switch` = first-class exhaustive
  error handling in modern Java.
- **Kotlin 1.5** stabilized `Result`; **Swift 5.0** shipped `Result`; **Swift 6** typed throws.
- **Node ≥ 15**: unhandled rejections default to fatal; Node 22-era `AbortSignal`/`fetch` make
  `AbortError` (`ABORT_ERR`) a routine classification.

## Real-world use case — Acme SaaS

Acme's incident review of "Checkout returns 500 instead of 402" found five contributing idioms:
Java threw `CheckoutException` with no code field; the Go gRPC client dropped it into a generic
`fmt.Errorf("grpc: %w")` without `errors.As`; the TS API caught with `instanceof Error` (always
true) and mapped everything to 500. The fix was one table — the master comparison above — turned
into a shared convention doc, plus generated per-language error types from a single registry
(see [47.16](../02-deep-dive/02-type-safe-handling-and-common-architecture.md)). Repeat incidents of the
same class dropped to zero in the following quarter.

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| Memorize per-language idioms | Fastest day-to-day coding | Drift as languages evolve | Individual contributors |
| One shared convention doc + table (this file) | Polyglot consistency | Needs ownership | Teams ≥ 2 languages |
| Force one language's style everywhere | One mental model | Fight the language; bugs multiply | Never across languages |
| Generate types from one registry | Single source of truth | Tooling cost | 3+ services sharing a taxonomy |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Look up a language's chaining + async idioms before porting code | Port Java try/catch idioms into Go line-by-line |
| Encode the same taxonomy in each language's native shape | Build one "universal error class" that fits none |
| Treat this table as the team's front page for onboarding | Assume "exceptions work the same everywhere" |
| Verify stdlib version gates (`Error.cause`, `ExceptionGroup`) | Copy snippets from pre-2020 Stack Overflow without checking |

## Common mistakes

- **Assuming Java-level checking in Kotlin** — Kotlin removed checked exceptions; `throws` in a
  Kotlin signature is documentation, not enforcement.
- **Using `instanceof` for TS error classes across bundles** — fails across realms; match
  `code`/`name`.
- **`runCatching` in coroutines** — swallows cancellation; always rethrow `CancellationException`.
- **Treating PHP `Exception` as "everything throwable"** — engine errors are `Error`; catch
  `Throwable`.
- **`try!`/`unwrap` in Swift/Rust on external input** — a trap is not error handling.

## Checklist

- [ ] Does your team doc state each primary language's mechanism, chaining API, and async idiom?
- [ ] Can every engineer name the one native chaining call in their language?
- [ ] Are version gates (`Error.cause`, `ExceptionGroup`, typed throws) recorded for your runtimes?
- [ ] Is the polyglot taxonomy shared, even though encodings differ per language?
- [ ] Do new hires get this comparison in week one?

## Related

- [Exception-First Languages in Depth](./03-exception-first-languages.md)
- [Result-First Languages in Depth](./04-result-first-languages.md)
- [Native Chaining and Wrapping](../02-deep-dive/01-native-chaining-and-wrapping-capabilities.md)
- [Translating to a Common Architecture](../02-deep-dive/02-type-safe-handling-and-common-architecture.md)
