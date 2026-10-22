# Native Chaining and Wrapping Capabilities

> Part XVIII · Chapter 47 · Section 47.14 · _Estimated reading time: 18 min_
> **Prerequisite:** [Language Comparison at a Glance](../01-concepts/02-language-comparison-at-a-glance.md), [Exception-First Languages in Depth](../01-concepts/03-exception-first-languages.md), [Result-First Languages in Depth](../01-concepts/04-result-first-languages.md)

## In one sentence

Every mainstream language ships **exactly one blessed way to attach a cause to an error** — Go's
`%w` + `errors.Is/As`, Rust's `#[source]`/`#[from]`, Python's `raise … from`, Java's cause
constructors plus `addSuppressed`, .NET's inner exceptions and `ExceptionDispatchInfo`, JS's
`Error.cause`, PHP's `$previous` — and using it is the difference between a diagnosis and a
guess.

## Why this matters in production

A wrapped cause is the only thing that survives a crash: the outer error tells you *what
operation failed*, the inner cause tells you *why the vendor said no*. Acme's `Checkout` incident
review opened with "gateway error" in 100% of tickets, because the payment provider's request
id — the one thing that made Stripe's support answer in minutes — was destroyed at the first
`catch`. Every hour of a vendor outage was spent re-deriving facts the process already had and
had thrown away.

The rule is therefore mechanical: **wrap with the native API, always, and never flatten to a
string.** `fmt.Errorf("…: %s", err)`, `new Error(err.message)`, `raise CheckoutError(str(exc))`,
and `throw new Exception(ex.Message)` are all the same mistake in four languages — they
convert a structured cause into prose that no classifier can read.

## Core concept — the shape of a cause chain

```text
  boundary error (app code, stable, classified)
        │  cause
        ▼
  adapter error (vendor-shaped, translated)
        │  cause
        ▼
  driver error (HTTP status, errno, vendor payload)
```

Three properties decide whether the chain is useful:

| Property | Question | Languages that get it right |
| -------- | -------- | --------------------------- |
| **Preservation** | Is the original object still reachable, or only its text? | All seven (if you use the native API) |
| **Traversability** | Can a classifier walk the chain without string matching? | Go (`Is`/`As`), Rust (`source()`), Python (`__cause__`), Java (`getCause()`), .NET (`InnerException`), PHP (`getPrevious()`), JS (**no built-in walker — you write one**) |
| **Fidelity** | Does the chain keep *structured* metadata (status code, errno, retry-after)? | Only if you wrap the object, never the message |

⚠️ **The chain is not the same as a set of siblings.** Java's `addSuppressed`, JS's
`AggregateError.errors`, Python's `ExceptionGroup.exceptions`, and Go's `errors.Join` all hold
*multiple parallel failures* — not a linear cause chain. Classifiers that assume "one previous
error" will silently drop the other failures. Handle chains (walk) and sets (iterate)
separately.

## How it works — the exact API per language

### Go — `%w` + `errors.Is` / `errors.As`

```go
// Wrap: %w keeps the cause inspectable. %v flattens it to text (breaks the chain).
return nil, fmt.Errorf("capture %s: gateway: %w", idemKey, err)

// Inspect: Is() for identity/sentinels, As() for typed extraction.
var netErr *net.OpError
if errors.As(err, &netErr) { /* typed */ }
if errors.Is(err, context.DeadlineExceeded) { /* identity through the chain */ }
if errors.Is(err, stripe.ErrCardDeclined) { /* sentinel through the chain */ }

// Unwrap one level: errors.Unwrap(err)
// Multi-failure: errors.Join(a, b) — Is/As traverse all of them (Go 1.20).
```

`errors.Is` and `errors.As` walk the chain by calling `Unwrap() error` (or `Unwrap() []error`)
repeatedly. A custom type may implement its own `Is(target error) bool` or `As(target any) bool`
so the walk can match on a *field* rather than a type.

### Rust — `thiserror` for libraries, `anyhow` for applications

```rust
#[derive(Debug, thiserror::Error)]
pub enum CheckoutError {
    #[error("gateway timeout after {attempt_ms}ms")]
    Timeout {
        attempt_ms: u64,
        #[source]                                  // exposes .source() for the chain
        source: GatewayError,
    },
    #[error("gateway error")]
    Gateway(#[from] GatewayError),                // From<GatewayError> → `?` auto-converts
    #[error(transparent)]                          // delegate Display AND source to the inner
    Inner(Box<dyn std::error::Error + Send + Sync>),
}
```

- `#[from]` generates a `From` impl so `?` converts automatically — **the cleanest wrapping in
  any language**, because the compiler performs it.
- `#[source]` marks the field returned by `Error::source()`; `#[error(transparent)]` forwards
  both the message and the source to the inner error.
- `anyhow::Error` is the application-level equivalent: `.context("capturing checkout")` pushes a
  **context layer** onto a stack that `anyhow` prints top-down. Downcast with
  `err.downcast_ref::<CheckoutError>()` when a caller must branch on a typed error.

```rust
let receipt = gateway.capture(&auth)
    .context("capturing checkout")?;              // anyhow context layer
```

### Python — `raise … from`

```python
try:
    receipt = stripe.capture(amount, idempotency_key=key)
except stripe.error.CardError as exc:
    raise CheckoutError("PAYMENT_CARD_DECLINED", retryable=False) from exc
except stripe.error.APIConnectionError as exc:
    raise CheckoutError("PAYMENT_PROVIDER_TIMEOUT", retryable=True) from exc
```

- `from exc` sets `__cause__` **and** `__suppress_context__ = True`. The traceback reads "The
  above exception was the direct cause of…".
- Without `from`, Python still records `__context__` implicitly and prints "During handling of
  the above exception, another exception occurred" — which asserts *consequence*, not *cause*.
  That wording difference is why `from` matters even when you never read `__cause__`.
- `raise X from None` deliberately hides the inner error (use only when it is noise).
- Python 3.11 `ExceptionGroup` holds **siblings**: `group.exceptions`, and
  `except* CheckoutError:` handles the matching subset — the members remain in the group.

### Java — cause constructors, `initCause`, `addSuppressed`

```java
throw new CheckoutException("PAYMENT_PROVIDER_TIMEOUT", true, cause);

// initCause for the rare no-cause constructor:
IllegalStateException ise = new IllegalStateException("bad state");
ise.initCause(original);                          // throws IllegalStateException if cause already set

// Suppressed: the close() failure is attached to the primary failure.
try (var conn = dataSource.getConnection()) {
    return conn.query(sql);
}   // if close() throws, it is added via addSuppressed — primary error still wins
```

- `Throwable.getCause()` walks **one** link (it is the *cause*, not a chain walker — the chain
  is traversed by your own code or by `initCause`).
- `getSuppressed()` returns an array of **sibling** failures auto-added by try-with-resources.
  Java 7+; suppressed exceptions never replace the primary one.
- `cause` is set by the `(String, Throwable)` constructor; `initCause` cannot be called twice.

### .NET — inner exceptions, `throw;`, `ExceptionDispatchInfo`

```csharp
throw new CheckoutException("PAYMENT_PROVIDER_TIMEOUT", retryable: true, innerException: ex);

// Re-throw preserving the original stack:
catch (HttpRequestException ex)
{
    logger.LogWarning(ex, "gateway timeout");
    throw;                                        // ✅ stack preserved
    // throw ex;                                 // ❌ stack reset to this line
}

// Across await/thread boundaries:
ExceptionDispatchInfo.Capture(ex).Throw();       // preserves stack + locals
```

- `Exception.InnerException` is the single cause link; `ex.Data` is an `IDictionary` for
  structured context; `ex.TargetSite` gives the throwing method.
- `ExceptionDispatchInfo.Capture(ex).Throw()` is the same mechanism `Task` uses internally to
  re-throw with the original stack — use it in custom retry/aggregate helpers.
- `AggregateException.InnerExceptions` holds siblings; `Task.WhenAll` throws it — **unwrap or
  flatten before classifying** or you will see one anonymous failure type.

### JavaScript / TypeScript — `Error.cause` (ES2022)

```ts
throw new CheckoutError("PAYMENT_PROVIDER_TIMEOUT", {
  cause: err,                                    // ES2022 native cause
  retryable: true,
});

// Multiple failures → AggregateError (ES2021), siblings in .errors
throw new AggregateError([a, b], "export batch failed", { cause: a });
```

- `cause` is an **own, non-enumerable property** set only when the options object has its own
  `cause` key; it is **not** part of `Error.prototype`, so `error.cause` is `undefined` on
  errors created without it. There is **no standard chain walker**: `instanceof` breaks across
  realms and bundlers, so classify on `err.name` / `err.code` and walk `cause` yourself.
- `Error.captureStackTrace` is **V8-only** (not part of the spec) — never rely on it in
  portable code, and never assume `error.stack` exists in every engine.

### PHP — the `$previous` argument

```php
throw new CheckoutException('PAYMENT_PROVIDER_TIMEOUT', 0, $previous: $e);
// parent::__construct($message, $code, $previous)
```

- `getPrevious()` returns the cause; PHP's `Throwable` covers both `Exception` and `Error`.
- PHP has no exception chaining syntax — the link is always the constructor's third argument.
  Loggers that print `getTraceAsString()` plus the previous chain are the norm.
- PHP 8's `ValueError`/`TypeError` are `Error`s, not `Exception`s — catch `Throwable` at the
  boundary.

## Worked example — one provider timeout, seven representations

The same Stripe timeout, expressed with each language's native chaining API:

```text
stripe.timeout(request_id=req_9f2, elapsed_ms=2000)
        ↓ translated at the adapter layer
PAYMENT_PROVIDER_TIMEOUT (retryable=true, provider_request_id=req_9f2)
        ↓ propagated
boundary → HTTP 504 / problem+json { code, requestId }
```

| Language | Representation of `PAYMENT_PROVIDER_TIMEOUT` |
| -------- | ------------------------------------------ |
| Go | `&CheckoutError{Code: "PAYMENT_PROVIDER_TIMEOUT", Retryable: true, ProviderRequestID: timeoutErr.RequestID, err: err}` |
| Rust | `CheckoutError::Timeout { attempt_ms: 2000, source: GatewayError::Timeout }` |
| Python | `raise CheckoutError("PAYMENT_PROVIDER_TIMEOUT", retryable=True, provider_request_id=exc.request_id) from exc` |
| Java | `throw new CheckoutException("PAYMENT_PROVIDER_TIMEOUT", true, ex);` |
| C# | `throw new CheckoutException("PAYMENT_PROVIDER_TIMEOUT", retryable: true, innerException: ex);` |
| TypeScript | `throw new CheckoutError("PAYMENT_PROVIDER_TIMEOUT", { cause: ex, retryable: true });` |
| PHP | `throw new CheckoutException('PAYMENT_PROVIDER_TIMEOUT', 0, $previous: $e);` |

⚠️ **None of the seven preserves the provider's request id automatically** — the adapter must
copy it into structured metadata. Wrapping preserves *the cause object*; it does not hoist its
fields.

## Key data / numbers

- Go `%w`, `errors.Is`, `errors.As`: **Go 1.13** (2019). Go **1.20** (2023) added `errors.Join`
  and allowed multiple `%w` verbs in one `fmt.Errorf`.
- Rust `?` operator: stable since **Rust 1.13** (2016); `thiserror` 1.0 and `anyhow` 1.0 are
  the community-standard crates.
- Python `raise … from`: **Python 3.0**; `ExceptionGroup`/`except*`: **Python 3.11** (2022);
  `CancelledError` moved to `BaseException` in **3.8** (2019).
- Java try-with-resources + `addSuppressed`/`getSuppressed`: **Java 7** (2011).
- .NET `ExceptionDispatchInfo`: **.NET Framework 4.5 / .NET Core 1.0** (2015 era).
- JS `Error.cause`: **ES2022**; `AggregateError`: **ES2021**. Both are "recent" — a large share
  of production libraries still hand-roll a `cause` field, and those are *own enumerable*
  properties, so `JSON.stringify(err)` leaks them.
- PHP `Throwable` unification and the `$previous` argument: **PHP 7.0** (2015).

## Real-world use case — Acme SaaS `Checkout`

Acme's billing service was Python. The Stripe SDK's timeout was caught in the adapter and
re-raised like this:

```python
except stripe.error.APIConnectionError as exc:
    raise CheckoutError("PAYMENT_FAILED")          # ❌ cause dropped, message flattened
```

Three consequences, all observed in production: the traceback said "During handling of the
above exception" (consequence language for what was actually a cause); the structured provider
`request_id` was never copied into the error, so Stripe support asked for a request id Acme
did not have; and the classification step downstream could only see the literal string
`PAYMENT_FAILED`, so a provider timeout was reported to the on-call engineer as "payment
failed" — a customer-facing error page — instead of a retryable 504.

The fix was one line, `from exc`, plus one field, `provider_request_id=exc.request_id`, copied
at the adapter boundary. The provider timeout became `PAYMENT_PROVIDER_TIMEOUT` (retryable,
`504`), the vendor's request id reached the log line, and the traceback named the real cause.
The same change was later ported to the Go ingest service, where `fmt.Errorf("…: %w", err)`
replaced `fmt.Errorf("…: %s", err)` — and the incident ticket template stopped asking for a
reproduction, because the cause was finally in the ticket.

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| Wrap with the native API (object preserved) | Classification works; cause survives | One extra type per layer | Every layer that adds context |
| Flatten to a message | Simple code | Root cause lost; unrecoverable | Never at a layer boundary |
| Wrap with structured metadata only (no cause object) | Safe for external payloads | Loses vendor diagnostics | Public API responses, not internal errors |
| One wrapper type for the whole app | Uniform | Loses per-domain typing; shallow hierarchy | Small apps; large apps use a registry + per-domain types |
| Chain plus sibling set (`Join`/`AggregateError`/`ExceptionGroup`) | No failure lost | Two APIs to model | Parallel operations |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Wrap with `%w`, `from`, `cause`, `$previous`, `#[source]`, or the cause constructor | Flatten with `%v`, `str(exc)`, `err.message`, `ex.Message` |
| Copy structured fields (request id, status, errno) into your own error | Assume wrapping hoists the inner fields |
| Keep the provider's cause object reachable for support | Throw away the cause and hope the message is enough |
| Walk chains with the language's walker (`errors.Is/As`, `source()`, `getCause()`) | Match on message substrings |
| Model parallel failures as a set (`errors.Join`, `AggregateError`, `ExceptionGroup`) | Flatten N failures into one string |
| Add one layer of context per meaningful boundary | Wrap on every line until the chain is unreadable |

## Common mistakes

- **The double-wrap.** Adapter wraps the vendor error, service wraps the adapter error, handler
  wraps again — three layers of "at line 12" prose. Fix: wrap once per boundary that adds
  *meaningful* context (operation, tenant, id), not per function.
- **Flat-then-wrap.** `fmt.Errorf("…: %s", err)` followed by `fmt.Errorf("…: %w", err)` — the
  first link is already prose; the chain is decorative. Fix: grep for `%s`/`%v` with an error
  argument.
- **`throw ex;` in C#** — resets the stack trace to the rethrow site. Fix: `throw;` or
  `ExceptionDispatchInfo`.
- **Catching the wrapper in JS.** `err instanceof TimeoutError` misses a wrapped cause because
  the cause is a plain property. Fix: walk `cause` explicitly, and classify on `code`/`name`.
- **Losing siblings.** Go `errors.Join` and Java `addSuppressed` hold parallel failures; a
  classifier that reads only the first cause reports success while two operations failed.
- **Circular chains.** Wrapping an error with itself (or a parent) produces an infinite loop in
  any chain walker. Fix: never store a reference to an ancestor error in a new error.

## Checklist

- [ ] Does every cross-layer error use the language's native chaining call?
- [ ] Is any error ever converted to a string before being wrapped?
- [ ] Are structured vendor fields (request id, status, errno) copied into your error?
- [ ] Does your classifier walk the chain instead of matching message text?
- [ ] Are parallel failures represented as a set, not folded into one error?
- [ ] Is chain depth bounded (one wrap per boundary, ≤ ~4 layers)?

## Related

- [Type-Safe Handling and the Common Architecture](./02-type-safe-handling-and-common-architecture.md)
- [Same Error Across Languages](../03-practical-examples/01-same-error-across-languages.md)
- [Exception-First Languages in Depth](../01-concepts/03-exception-first-languages.md)
- [Chapter 16 — Error Translation and Normalization](../../../part-06-boundaries-and-translation/16-error-translation-and-normalization/README.md)
