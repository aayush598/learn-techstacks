# Result-First Languages in Depth — Go, Rust, Kotlin, Swift

> Part XVIII · Chapter 47 · Sections 47.6–47.7, 47.10–47.11 · _Estimated reading time: 22 min_
> **Prerequisite:** [Language Comparison at a Glance](./02-language-comparison-at-a-glance.md)

## In one sentence

Go and Rust put failure **in the return value** (an `error` interface and a `Result` type) so
every frame must admit propagation, while Kotlin and Swift are **hybrids** that reward you for
using their result/typed-throw features on expected failures and their exception machinery only
on exceptional ones.

## Why this matters in production

Result-first code has a different failure topology: errors are visible at every call site, which
makes propagation bugs *local* (you can see the `if err != nil` you forgot) instead of *global*
(a catch three frames away never ran). But the style introduces its own production risks — the
unchecked Go error, the Rust `unwrap` in a request path, the Kotlin `runCatching` that eats
cancellation. This file covers the idioms and the exact traps.

## 47.6 — Go

### Errors are values

```go
type CheckoutError struct {
    Code      string // stable machine code, e.g. "CARD_DECLINED"
    Retryable bool
    err       error  // wrapped cause
}

func (e *CheckoutError) Error() string { return "checkout: " + e.Code + ": " + e.err.Error() }
func (e *CheckoutError) Unwrap() error { return e.err } // enables errors.Is/As
```

Every fallible call returns `(T, error)`. The idiomatic chain:

```go
func Capture(ctx context.Context, key string) (*Receipt, error) {
    auth, err := authorize(ctx, key)
    if err != nil {
        // %w wraps: the cause stays inspectable by errors.Is/As
        return nil, fmt.Errorf("capture %s: authorize: %w", key, err)
    }
    receipt, err := gateway.Capture(ctx, auth)
    if err != nil {
        if errors.Is(err, stripe.ErrCardDeclined) {
            return nil, &CheckoutError{Code: "CARD_DECLINED", Retryable: false, err: err}
        }
        return nil, fmt.Errorf("capture %s: gateway: %w", key, err)
    }
    return receipt, nil
}
```

### The Go toolkit (all stdlib, all Go 1.13+ unless noted)

| Tool | Use |
| ---- | --- |
| `errors.Is(err, target)` | Identity/sentinel test through the wrap chain |
| `errors.As(err, &target)` | Extract the first `*T` in the chain |
| `fmt.Errorf("…: %w", err)` | Wrap with context; `%w` keeps the chain |
| `errors.Unwrap(err)` | One layer up the chain |
| `errors.Join(errs...)` | Multi-error (Go 1.20); `Is`/`As` search all |
| `errors.New` / sentinels | `var ErrNotFound = errors.New("not found")` — package-level |

### Go's two hard rules

1. **Check every error.** The compiler forces receipt, not inspection. `errcheck`/`staticcheck`
   in CI is non-negotiable — see [type safety](../02-deep-dive/02-type-safe-handling-and-common-architecture.md).
2. **`panic` is a bug signal.** Panics crash the process (unless a top-level `recover` at a
   boundary converts to a 500). Never panic for `CARD_DECLINED` — return it.

```go
// Go's shadowing bug — the oldest in the language:
if _, err := stat(path); err != nil {          // NEW err shadows the outer one
    return err
}
return nil                                      // outer err looked "handled" but wasn't
```

`go vet` does not catch shadowed errors; `shadowcheck` does. This single bug class has filled
more Go postmortems than any other.

## 47.7 — Rust

### `Result` is the only fallible return type

```rust
#[derive(Debug, thiserror::Error)]
pub enum CheckoutError {
    #[error("card declined")]
    CardDeclined {
        #[source]                     // chain: source() returns the gateway error
        source: GatewayError,
    },
    #[error("gateway unavailable: {0}")]
    Unavailable(#[from] GatewayError), // From<GatewayError> → `?` auto-converts
    #[error("checkout for {key} failed: {source}")]
    Context {
        key: String,
        #[source]
        source: Box<CheckoutError>,
    },
}

pub async fn capture(client: &Client, key: &str) -> Result<Receipt, CheckoutError> {
    let auth = authorize(client, key).await?;   // `?` = early-return Err(...) via From
    match client.capture(&auth).await {
        Ok(receipt) => Ok(receipt),
        Err(GatewayError::CardDeclined(source)) => {
            Err(CheckoutError::CardDeclined { source })
        }
        Err(other) => Err(CheckoutError::from(other)),  // `?` would do the same
    }
}
```

### The Rust toolkit

| Tool | Crate/std | Use |
| ---- | --------- | --- |
| `?` | std | Propagate `Err` after `From` conversion |
| `#[derive(thiserror::Error)]` | thiserror | Library-quality error enums with Display + source |
| `#[from]` | thiserror | Generate `From` impls so `?` converts |
| `#[source]` / `#[error(transparent)]` | thiserror | Chain the cause explicitly |
| `anyhow::Result` + `.context()` | anyhow | App-level: stack of contexts, no enum |
| `Box<dyn Error>` | std | When the error type is genuinely dynamic |
| `match` exhaustiveness | rustc | Compiler rejects unhandled variants |

**`thiserror` vs `anyhow` rule of thumb:** libraries and anything a caller must *branch on*
(business failures) use `thiserror` enums; binaries and glue code that only *logs/propagates*
use `anyhow` with `.context("capturing checkout")`.

### Rust's two hard rules

1. **`Result` is `#[must_use]`** — ignoring one is a warning, and `#![deny(warnings)]` makes it
   an error. This is the compiler doing what Go's linters must be told to do.
2. **`unwrap`/`expect`/`panic!` are for bugs and tests.** In a server request path, `unwrap` on
   I/O is a crash with extra steps. `expect("…")` documents *why* it cannot fail — use it only
   where the invariant is truly local. For "should not happen but might," return an error.

```rust
// ❌ production hazard
let payload: ExportPayload = serde_json::from_slice(&bytes).unwrap();
// ✅ typed propagation
let payload: ExportPayload = serde_json::from_slice(&bytes)
    .map_err(|e| ExportError::MalformedPayload { source: e })?;
```

## 47.10 — Kotlin

### Exceptions are unchecked; `Result` is opt-in

Kotlin removed Java's checked half: every exception is unchecked, and `throws` clauses are
documentation. For expected failures, the stdlib `Result<T>` plus `runCatching` offer the
result style:

```kotlin
suspend fun capture(idemKey: String): Result<Receipt> = runCatching {
    val auth = gateway.authorize(idemKey)            // may throw IOException
    gateway.capture(auth)
}.mapCatching { receipt ->
    receipt
}.recoverCatching { err ->
    if (err is StripeCardException) throw CheckoutException("CARD_DECLINED", retryable = false, err)
    throw err
}
```

⚠️ **The `runCatching` pitfall**: it catches `Throwable`, **including
`CancellationException`**. Inside a coroutine, that silently converts cancellation into a
"failure" you might retry — breaking structured concurrency. Two accepted fixes:

```kotlin
// 1) rethrow cancellation
runCatching { … }.onFailure { if (it is CancellationException) throw it }
// 2) don't use runCatching in suspend code; use try/catch with narrow types
```

### Kotlin's real strength: sealed hierarchies

For API surfaces, prefer sealed outcomes over thrown exceptions — exhaustive `when`:

```kotlin
sealed interface CheckoutOutcome {
    data class Success(val receipt: Receipt) : CheckoutOutcome
    data class Declined(val reason: String) : CheckoutOutcome
    data class Unavailable(val retryAfter: Duration?) : CheckoutOutcome
}

when (val outcome = checkout.capture(key)) {
    is CheckoutOutcome.Success -> accept(outcome.receipt)
    is CheckoutOutcome.Declined -> respond(402, outcome.reason)
    is CheckoutOutcome.Unavailable -> respond(503, retryAfterHeader(outcome.retryAfter))
}
```

### Coroutine failure semantics

- A failing child **cancels its siblings** in `coroutineScope`; use `supervisorScope` for
  independent children.
- Uncaught exceptions in non-supervisor scopes propagate to the parent and eventually crash
  unless a `CoroutineExceptionHandler` is installed at the scope root.
- `async` defers the failure to `await()` — an un-awaited `async` failure is still handled by
  the scope, not forgotten (unlike a JS floating promise), but the *caller* never sees it.

## 47.11 — Swift

### `throws` is checked; `Result` is for composition

Swift's `throws` is not like Java's: **the compiler requires every `try` to be handled** —
wrapped in `do/catch`, converted with `try?` (→ optional), or explicitly asserted with `try!`
(trap on failure). Since Swift 6, typed throws puts the error set in the signature
(`throws (CheckoutError)`); before that, functions throw `any Error`.

```swift
func capture(idemKey: String) async throws -> Receipt {
    let auth = try await gateway.authorize(idemKey)
    do {
        return try await gateway.capture(auth)
    } catch GatewayError.cardDeclined(let reason) {
        throw CheckoutError.cardDeclined(reason)   // typed translation
    } catch {
        throw CheckoutError.unavailable(underlying: error)  // wrap with cause
    }
}

// Call sites: pick your handling style explicitly.
do      { let receipt = try await capture(idemKey: key) }
catch let e as CheckoutError { respond(402, e.code) }
catch                       { respond(500, "INTERNAL") }

let receipt: Receipt? = try? await capture(idemKey: key)   // nil on any failure — use rarely
```

### Swift rules

- Model **`Result<Success, Failure>`** when composing multiple fallible steps or when the
  failure must travel through non-throwing APIs (callbacks, Combine-style pipelines).
- Store the **underlying error** in your enum (`case unavailable(underlying: any Error)`) —
  Swift has no auto-chaining; `Error` values are flat unless you chain them yourself.
- `try!` is a `preconditionFailure` in disguise: fine for "impossible after launch" file loads,
  never for external input.
- Foundation errors are `NSError`-bridged; `localizedDescription` is user-facing text, not a
  contract — carry your own stable `code` enum.

## Key data / numbers

- Go `errors.Is`/`As`/`%w`: **Go 1.13** (2019); `errors.Join`: **Go 1.20** (2023).
- Go's `Error()` method is the *only* interface method — there is no typed access without
  `errors.As`.
- Rust `?`: **1.13**; `thiserror` and `anyhow` are the de-facto stdlib-adjacent crates (dtolnay),
  used by the majority of Rust services on crates.io conventions.
- Kotlin `Result` stable: **1.5** (2021); `runCatching` has shipped alongside it since 1.3.
- Swift `Result`: **5.0** (2019); typed throws: **Swift 6 / SE-0413** (2024).
- `panic = abort` (Rust profile) trades unwinding for binary size — know which profile your
  server builds with; unwinding is what lets `catch_unwind` contain a panic.

## Real-world use case — ExportJob

Acme's `ExportJob` worker was rewritten from Python to Go. The Python version had a
`try/except Exception` around the whole job that logged and continued; the Go port inherited
that shape as a top-level `recover()` that swallowed panics and marked the job `succeeded`.
During a serde bug, 40 000 exports "succeeded" with empty CSVs. The fix aligned the port with Go
idioms: no top-level recover (panic = crash = redelivery), every `err` checked (`errcheck` in
CI), and the empty-payload invariant became a returned `&ExportError{Code: "EMPTY_PAYLOAD",
Retryable: false}` — a terminal DLQ entry instead of silent success.

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| Go `(T, error)` everywhere | Uniform, greppable, explicit | Verbose; unchecked-error risk | All Go code |
| Rust `Result` + `?` | Compiler-true; exhaustive | Steeper learning; `From` plumbing | All Rust code |
| Kotlin sealed outcomes | Exhaustive; testable | Not throwable across layers | API/layer boundaries |
| Kotlin `Result` + `runCatching` | Familiar result style | Cancellation pitfall | Non-suspend utility code |
| Swift `throws` | Concise; forced handling | Untyped pre-Swift 6 | Default Swift style |
| Swift `Result` | Composable | Verbose for simple cases | Pipelines, callbacks |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Wrap Go errors with `%w` at each layer | `fmt.Errorf("…: %s", err)` — breaks `Is`/`As` |
| Enable `errcheck`/`staticcheck` in Go CI | Trust code review alone to catch ignored errors |
| Use `thiserror` for caller-branchable Rust errors | `unwrap()` on I/O in a request/worker path |
| Rethrow `CancellationException` after `runCatching` | Let `runCatching` swallow coroutine cancellation |
| Chain Swift underlying errors manually | Log `localizedDescription` only and drop the error |
| `panic`/`unwrap` only for genuine bugs | Return a Go `panic` for a business decline |

## Common mistakes

- **Go shadowed `err`** — `if err := f(); err != nil` inside a block shadows the outer `err`;
  the outer one silently stays non-nil/nil incorrectly. Use `=` for reassignment.
- **`errors.Is` against a wrapped value type** — sentinels must be comparable; wrap with
  `Unwrap()` or use `errors.As` for structs.
- **Rust `map_err(|e| format!(…))`** — turns the typed error into a string; the cause is gone.
  Use `.context()` (anyhow) or a `#[from]` variant.
- **Kotlin `supervisorScope` forgotten** — one failed export child cancels siblings mid-write.
- **Swift `try?` chains** — `try? try? f()` collapses distinct failures to one `nil`; you lose
  the difference between declined and unavailable.
- **Mixing `anyhow::Result` into a library signature** — callers cannot match on typed variants;
  reserve `anyhow` for binaries.

## Checklist

- [ ] Go: does CI run `errcheck`/`staticcheck`, and is `-copylocks`-style vetting enabled?
- [ ] Go: are sentinels/typed errors returned with `%w` wrapping at every layer?
- [ ] Rust: are `unwrap`/`expect` limited to tests and provably local invariants?
- [ ] Kotlin: does every `runCatching` in suspend code rethrow `CancellationException`?
- [ ] Kotlin: are public failure contracts sealed types rather than thrown exceptions?
- [ ] Swift: is every underlying error stored in the translated error type?

## Related

- [Exceptions vs Explicit Returns](./01-exceptions-vs-returns.md)
- [Native Chaining and Wrapping](../02-deep-dive/01-native-chaining-and-wrapping-capabilities.md)
- [Type-Safe Error Handling](../02-deep-dive/02-type-safe-handling-and-common-architecture.md)
- [Same Error, Five Languages](../03-practical-examples/01-same-error-across-languages.md)
