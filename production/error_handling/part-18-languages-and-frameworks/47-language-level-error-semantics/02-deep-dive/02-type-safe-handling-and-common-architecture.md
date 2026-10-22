# Type-Safe Handling and the Common Architecture

> Part XVIII · Chapter 47 · Sections 47.15–47.16 · _Estimated reading time: 20 min_
> **Prerequisite:** [Native Chaining and Wrapping Capabilities](./01-native-chaining-and-wrapping-capabilities.md), [Exceptions vs Explicit Returns](../01-concepts/01-exceptions-vs-returns.md)

## In one sentence

Type safety is a **spectrum the compiler enforces** (Rust exhaustively, Go partially, Java for
checked exceptions only, JS/Python/C#/PHP not at all) — and the way to get one error
architecture across all of them is to fix the **four layers** (error model → translation →
boundary → policy) and let each language supply only the encoding.

## Why this matters in production

Polyglot codebases drift in a predictable way: the strictest language sets the culture, the
loosest language sets the practice. Acme's Rust `AgentRun` matched on error enums; its Python
worker checked `isinstance`; its TypeScript API checked `err.code` — and a new error added in
Rust was forgotten in Python for three weeks, producing a `KeyError` inside the classifier
itself. The classifier crashing is the worst failure mode in this domain: **an unknown error
must never be able to crash the thing that classifies errors.**

The fix is not "be more careful." The fix is that the *architecture* is language-neutral and
each language's job is bounded: encode the taxonomy natively, compile what you can, and let a
single registry decide status codes, retryability, and user-facing text.

## 47.15 — Type-safe handling: the honesty spectrum

### The spectrum

| Language | Enforcement level | What the compiler guarantees | What it does **not** guarantee |
| -------- | ----------------- | --------------------------- | -------------------------------- |
| **Rust** | Highest | Every `Result` must be used (`#[must_use]`); `match` exhaustiveness; `?` propagates; `!` (never) in return position | That you did not `unwrap()`; that an `anyhow::Error` is the type you expect |
| **Java** | Medium | *Checked* exceptions must be caught or declared; `sealed` + pattern `switch` (Java 21) gives exhaustiveness | That unchecked (`RuntimeException`) failures are handled; that you catch the right subclass |
| **Kotlin** | Low-medium | `sealed` hierarchies + exhaustive `when`; `Result<T>` in the stdlib | That `when` branches are exhaustive without a `sealed` subject (a runtime check) |
| **Swift** | Low-medium | `try` must be handled; typed `throws` (Swift 6) names the error type | That a `catch` clause covers the intended case (`catch` without a pattern catches all) |
| **Go** | Low | You must *receive* the `error` value | That you checked it; that you wrapped it; that the type you return is the one you documented |
| **TypeScript** | Low (opt-in) | Discriminated unions give exhaustiveness via `never`; `strict` types `catch` as `unknown` | That a thrown value matches your union — TypeScript does not model throws at all |
| **Python** | Very low | `typing`/`mypy` can check `Literal` codes and `ExceptionGroup` membership | That an `except` clause is reachable; that a raised type matches the declared one |
| **C#/.NET** | Very low | Pattern matching + `switch` exhaustiveness on enums; nullable reference types | That `catch (Exception)` is selective; that the inner exception was unwrapped |
| **PHP** | Very low | Typed properties/params constrain *values*, not failures | Everything about failures |

### The mechanisms that close the gaps

| Gap | Mechanism | Languages |
| --- | --------- | --------- |
| Ignored `error` value | `errcheck` / `staticcheck` in CI | Go |
| Ignored `Result` | `#![deny(warnings)]` (Rust) | Rust |
| Untyped `catch` variable | `strict` + `useUnknownInCatchVariables` (TS 4.4+) | TypeScript |
| Unreachable catch branch | Discriminated union + `never` exhaustiveness | TypeScript |
| Unreachable catch branch | `sealed` interface/classes + exhaustive `when`/`switch` | Kotlin, Java 17/21, C# |
| Catch-all in Python | `mypy --strict` + `flake8` rules banning bare `except:` | Python |
| Wide catch in C# | Analyzer rule banning `catch (Exception)` outside boundary classes | C# |
| Unclassified error | **Registry lookup that cannot throw** — unknown code ⇒ safe default | All |

### Exhaustive handling, concretely

```ts
// TypeScript: the compiler rejects an unhandled variant.
type CheckoutFailure =
  | { code: "PAYMENT_CARD_DECLINED"; retryable: false }
  | { code: "PAYMENT_PROVIDER_TIMEOUT"; retryable: true; providerRequestId: string }
  | { code: "PAYMENT_IDEMPOTENCY_CONFLICT"; retryable: false };

function assertNever(x: never): never { throw new Error("unreachable"); }

function plan(f: CheckoutFailure) {
  switch (f.code) {
    case "PAYMENT_CARD_DECLINED": return "ask_user_for_another_card";
    case "PAYMENT_PROVIDER_TIMEOUT": return "retry_with_same_idempotency_key";
    case "PAYMENT_IDEMPOTENCY_CONFLICT": return "show_existing_result";
    default: return assertNever(f);   // add a variant → this line fails to compile
  }
}
```

```kotlin
// Kotlin: sealed + exhaustive `when` — no `else` needed.
sealed interface CheckoutFailure {
    data class Declined(val reason: String) : CheckoutFailure
    data class Timeout(val providerRequestId: String) : CheckoutFailure
    data object IdempotencyConflict : CheckoutFailure
}

fun plan(f: CheckoutFailure): String = when (f) {
    is CheckoutFailure.Declined -> "ask_user_for_another_card"
    is CheckoutFailure.Timeout -> "retry_with_same_idempotency_key"
    CheckoutFailure.IdempotencyConflict -> "show_existing_result"
}
```

### The rule that matters most

> **The classifier must be total.** Every input — including a type it has never seen — must
> produce a decision. `default: return assertNever(f)` is a *compile-time* check for known
> variants; the *runtime* default for unknown variants must be "unknown error ⇒ 500 + log",
> never a crash.

## 47.16 — One architecture, ten encodings

### The four layers

```text
 ┌─ 1. ERROR MODEL ────────────────────────────────────────────┐
 │  code, category, severity, retryable, cause, safe context,    │
 │  timestamp, correlation id — framework-free, per language,    │
 │  generated from one registry                                 │
 └────────────────────────────┬────────────────────────────────┘
                              ▼
 ┌─ 2. TRANSLATION ────────────────────────────────────────────┐
 │  vendor / driver / ORM / validation errors → your model;     │
 │  happens at the ADAPTER, not at the boundary                 │
 └────────────────────────────┬────────────────────────────────┘
                              ▼
 ┌─ 3. BOUNDARY ───────────────────────────────────────────────┐
 │  where an error becomes an external outcome: HTTP response,  │
 │  job state, exit code, event — ONE boundary per entry point  │
 └────────────────────────────┬────────────────────────────────┘
                              ▼
 ┌─ 4. POLICY ─────────────────────────────────────────────────┐
 │  registry-driven: code → HTTP status, retryability,          │
 │  retry-after, user message, alert level, redaction           │
 └─────────────────────────────────────────────────────────────┘
```

**Why this order matters:** if policy sits above the boundary, the boundary needs to know the
policy; if the model is defined by the framework, the model is unusable in a worker. The
dependency direction is always **policy ← boundary ← translation ← model**.

### How each language realizes the four layers

| Layer | Go | Rust | Python | TypeScript | Java | C# |
| ----- | -- | ---- | ------ | ---------- | ---- | -- |
| **1. Model** | `error` interface + `CheckoutError` struct | `thiserror` enum | `AcmeError` base class | `AppError` class + discriminated unions | `AcmeException` (unchecked) | `AcmeException` |
| **2. Translation** | adapter returns typed error; `errors.As` at the edge | `#[from]` / `map_err` in the adapter | `raise … from` in the adapter | `toAppError(err)` in the adapter | catch vendor → throw domain with cause | catch vendor → throw domain with inner |
| **3. Boundary** | `http.ErrorWriter` / `chi` middleware | `tower` layer / `axum` extractor | middleware / exception handler | Express error middleware / NestJS filter | `@ControllerAdvice` | ASP.NET exception middleware / `IExceptionHandler` |
| **4. Policy** | `registry.go` (map + pure funcs) | `registry.rs` | `registry.py` | `registry.ts` | `ErrorRegistry` bean | `ErrorRegistry` static |

### The registry is the contract

```ts
// policy/registry.ts — pure, framework-free, total.
export const ERROR_REGISTRY = {
  PAYMENT_CARD_DECLINED:        { status: 402, retryable: false, alert: false, title: "Card declined" },
  PAYMENT_PROVIDER_TIMEOUT:     { status: 504, retryable: true,  alert: false, title: "Payment provider timed out" },
  PAYMENT_IDEMPOTENCY_CONFLICT: { status: 409, retryable: false, alert: false, title: "Request already processed" },
} as const;

export function policyFor(code: string) {
  // Total function: unknown codes degrade to a safe default, never throw.
  return (ERROR_REGISTRY as Record<string, unknown>)[code]
      ?? { status: 500, retryable: false, alert: true, title: "Internal error" };
}
```

Everything else — status, retry decision, whether to page, whether to show a friendly message —
is **data derived from the code**, so it is identical in every service and every language. The
per-language part is only how you *get* the code string into the registry lookup.

### Generating the per-language types

Because the taxonomy lives in one registry, the language-specific types can be *generated*:
a script reads the registry and emits a Go struct + constants, a Rust enum, a Python exception
hierarchy, a TS union, a Java enum, a C# enum. Hand-writing them is where polyglot taxonomies
diverge — the Python copy misses the newest code, exactly as Acme's `KeyError` proved.

**Generated** (never hand-edited): code constants, error types (class/enum/struct), HTTP status
and retryability mapping, user-facing messages. **Hand-written** (deliberately): vendor→app
translation (vendor-specific) and boundary adapters (framework-specific).

## Worked example — the same architecture in three languages

```go
// Go — model, translation, boundary, policy
type CheckoutError struct{ Code string; Retryable bool; err error }
func (e *CheckoutError) Error() string { return e.Code }
func (e *CheckoutError) Unwrap() error { return e.err }

func (a *StripeAdapter) Capture(ctx context.Context, amt int) (*Receipt, error) {
    r, err := a.client.Capture(ctx, amt)
    if err != nil {
        var te *stripe.TimeoutError
        if errors.As(err, &te) {
            return nil, &CheckoutError{Code: "PAYMENT_PROVIDER_TIMEOUT", Retryable: true, err: err}
        }
        return nil, fmt.Errorf("stripe capture: %w", err)
    }
    return r, nil
}

// boundary: the only writer of the response body
func WriteError(w http.ResponseWriter, err error, reqID string) {
    e := normalize(err)                       // → app model
    p := policyFor(e.Code)                    // → policy
    w.Header().Set("Content-Type", "application/problem+json")
    w.WriteHeader(p.Status)
    _ = json.NewEncoder(w).Encode(problem(e, p, reqID))
}
```

```rust
// Rust — model, translation, boundary, policy
#[derive(Debug, thiserror::Error)]
pub enum CheckoutError {
    #[error("payment provider timed out")]
    ProviderTimeout { #[source] source: GatewayError },
    #[error("checkout failed")]
    Other { #[source] source: Box<dyn std::error::Error + Send + Sync> },
}

pub async fn capture(svc: &StripeAdapter, amt: i64) -> Result<Receipt, CheckoutError> {
    svc.capture(amt).await.map_err(|source| match source {
        GatewayError::Timeout => CheckoutError::ProviderTimeout { source },
        other => CheckoutError::Other { source: Box::new(other) },
    })
}
```

```python
# Python — model, translation, boundary, policy
class AcmeError(Exception):
    def __init__(self, code: str, *, retryable: bool = False, **ctx):
        super().__init__(code)
        self.code = code
        self.retryable = retryable
        self.ctx = ctx

class StripeAdapter:
    def capture(self, amount: int) -> Receipt:
        try:
            return self._client.capture(amount)
        except stripe.error.APIConnectionError as exc:
            raise AcmeError("PAYMENT_PROVIDER_TIMEOUT", retryable=True,
                            provider_request_id=exc.request_id) from exc
```

Same four layers, same code strings, same policy table — three encodings, one architecture.

## Key data / numbers

- Rust `#[must_use]` on `Result` produces a **warning** by default; `#![deny(warnings)]` in
  CI makes it an **error**. `clippy::unwrap_used` and `clippy::expect_used` are available as
  lint denies.
- TypeScript `useUnknownInCatchVariables` ships with `strict` from **TS 4.4** (2021);
  `assertNever` exhaustiveness is the standard pattern.
- Java sealed interfaces: **Java 17** (2021); pattern-matching `switch` over sealed types:
  **Java 21** (2023) — this is what makes `switch` exhaustiveness checked.
- Kotlin `Result` stable since **1.5** (2021); sealed interfaces since **1.5**.
- Python `mypy --strict` and `ExceptionGroup`/`except*`: **Python 3.11** (2022).
- Go `errcheck`/`staticcheck` are the de-facto CI gates; `errors.As`/`Is` require **Go 1.13**.
- C# pattern matching (`switch` expressions) since **C# 8**; recommended: **one registry,
  generated types, total lookup** — the fallback for an unknown code is always `500` +
  `alert: true`, never an exception.

## Real-world use case — Acme SaaS `AgentRun`

Acme's `AgentRun` (LLM tool-calling) spans a Python worker and a TypeScript API. The Python
worker raised `ToolError("TOOL_HTTP_TIMEOUT")`; the TypeScript API expected
`"AGENT_TOOL_TIMEOUT"`. The mismatch was invisible until a tool failure produced a `KeyError`
inside the TypeScript registry lookup — **the classifier crashed**, so the request returned a
raw Node stack to the client and the job was retried forever.

Two fixes, both architectural rather than local:

1. **The registry became the single source of truth**, and the per-language error types were
   generated from it. A new code now exists in every language or in none.
2. **The lookup became total.** `policyFor(code)` returns a safe default for unknown codes
   instead of throwing; an unknown code is logged, alerted, and mapped to `500` — it can no
   longer crash the boundary.

The follow-up audit found 11 codes that existed in one language but not another; the generator
turned that class of bug into a CI failure.

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| Hand-written per-language error types | No tooling | Diverges silently | One language, small app |
| Generated types from one registry | Cannot diverge | Build step; generator upkeep | 2+ services or languages |
| Exhaustive unions/sealed types | Compiler catches missed variants | Verbose; migrations are code changes | Business failures callers branch on |
| Single catch-all error type with a `code` field | Simple, uniform | No compile-time narrowing | Infrastructure-level errors |
| Policy as data (registry) | One place to change status/retry/alert | Registry is a shared dependency | Any service with an external contract |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Keep the registry total — unknown codes get a safe default | Let an unknown code throw inside the classifier |
| Generate per-language types from the registry | Hand-maintain the same code list in five languages |
| Translate vendor errors in the adapter | Translate at the HTTP boundary |
| Put policy in pure, framework-free functions | Put policy inside the framework filter class |
| Use exhaustive unions where callers branch on the failure | Use `Exception`/`Error` as the public failure API |
| Add a lint gate for the language's honesty gap | Rely on review to catch ignored errors |

## Common mistakes

- **The crashing classifier** — a registry lookup that raises on an unknown code. Fix: total
  lookup with a documented default.
- **Policy inside the boundary** — the Express filter holds the status map, so the worker
  cannot reuse it. Fix: pure `policy.ts` / `policy.go`, imported by every boundary.
- **Translating at the boundary** — the HTTP layer knows about `SQLException`, so an error
  type leaks into the transport and a worker sees a different code for the same failure.
  Fix: translate in the adapter.
- **Over-typed boundaries** — modelling every vendor code in the public API. Fix: translate
  vendor codes into a small set of app codes at the adapter.

## Checklist

- [ ] Is there exactly one registry of codes, and are per-language types generated from it?
- [ ] Is the registry lookup total (unknown code ⇒ safe default)?
- [ ] Do vendor errors get translated in the adapter, not at the boundary?
- [ ] Is policy implemented as pure functions with no framework imports?
- [ ] Does each language's lint gate for ignored errors run in CI?
- [ ] Are business failures modelled as exhaustive types in every language?

## Related

- [Native Chaining and Wrapping Capabilities](./01-native-chaining-and-wrapping-capabilities.md)
- [Same Error Across Languages](../03-practical-examples/01-same-error-across-languages.md)
- [Chapter 8 — Error Codes and Error Registries](../../../part-03-error-models/08-error-codes-and-error-registries/README.md)
- [Chapter 16 — Error Translation and Normalization](../../../part-06-boundaries-and-translation/16-error-translation-and-normalization/README.md)
