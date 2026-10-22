# Exceptions vs Explicit Returns

> Part XVIII · Chapter 47 · Section 47.1 · _Estimated reading time: 16 min_
> **Prerequisite:** [Chapter 7 — Error Classes, Types, and Structured Results](../../../part-03-error-models/07-error-classes-types-and-structured-results/README.md)

## In one sentence

Languages split into two families — **exceptions signal failure out-of-band** past the return
type, while **explicit returns (Result/error values) put failure in the signature** — and the
family you code in decides what callers can forget.

## Why this matters in production

The choice is not aesthetic. With exceptions, a function's signature lies about what it can
return: `charge(card)` looks like it returns a receipt, but it can also abort the stack with a
decline. With explicit returns, the signature tells the truth: `charge(card) -> Result<Receipt,
CheckoutError>` cannot be called without acknowledging both outcomes. Teams that ignore which
family they are in produce the two classic production bugs: **forgotten failure paths** (the
language let callers forget) and **exception-driven business flow** (the language made forgetting
too easy on the writer's side, too).

## The two families

```text
  EXCEPTIONS (out-of-band)                RESULTS (in-band)
  ┌──────────────────────┐                ┌──────────────────────────┐
  │ charge() ──▶ receipt │  happy path    │ charge() ──▶ Ok(receipt)  │
  │      ╎               │                │      │                    │
  │      ╎ throw Decline │  error path    │      └────▶ Err(declined) │
  │      ▼               │                │                           │
  │  caller's catch      │  may be        │  caller must match        │
  │  (any frame away)    │  anywhere      │  (immediately visible)    │
  └──────────────────────┘                └──────────────────────────┘
   Signature hides the failure              Signature shows the failure
```

| Property | Exceptions | Explicit results |
| -------- | ---------- | ---------------- |
| Failure visible in signature | No | Yes |
| Caller can silently ignore | Yes (JS/Python/C#/PHP; Java only if unchecked) | Only by explicitly discarding (`let _ =`, `_ =`, `?` without handling in some designs) |
| Cost when hot | Higher (stack capture) | Cheap (value) |
| Happy-path readability | High | Lower (`if err != nil` / `match`) |
| Deep propagation | Free unwinding | Each frame must pass it through (`?`, `%w`, `from`) |
| Exhaustiveness | Catch clauses rarely exhaustive | `match` can be compiler-checked |
| Idiomatic languages | Java, C#, Python, PHP, JS/TS, Kotlin, Swift | Go, Rust |

## 47.1.1 — What exceptions force and what they hide

Exceptions are a **side channel on the call stack**. A function can raise from three frames below
the one you are reading; the compiler in JS/Python/C#/PHP never mentions it. Java's *checked*
exceptions (subclasses of `Exception` that are not `RuntimeException`) are the historical
attempt to put the failure back into the signature via `throws` clauses — an attempt most
languages abandoned or never adopted.

```ts
// TypeScript: the signature says nothing about the three failure modes.
function charge(card: Card, amount: Money): Promise<Receipt> {
  // can reject: network, decline, bug — none are typed
}
```

**Forced:** nothing — every JS/TS error is runtime.
**Hidden:** everything not caught at the boundary — the caller sees one return type.

```java
// Java: checked exceptions put SOME failures back in the signature.
Receipt charge(Card card, Money amount) throws CheckoutException { … }
```

**Forced:** callers must catch or declare `CheckoutException`.
**Hidden:** every unchecked (`RuntimeException`) failure still escapes silently.

## 47.1.2 — What results force and what they hide

Result-returning languages make the failure **a value you must look at** to get the success
value. Rust takes this to its extreme: `Result<T, E>` is `#[must_use]`, and the `?` operator
propagates explicitly while forcing every function in the chain to admit it can fail.

```rust
// Rust: the signature is honest; every frame admits propagation.
fn charge(card: &Card, amount: Money) -> Result<Receipt, CheckoutError> {
    let auth = authorize(card, amount)?;   // propagate, do not hide
    capture(auth).map_err(CheckoutError::from)
}
```

**Forced:** the caller cannot receive `Receipt` without handling `CheckoutError` (or `?`-ing it
into an enclosing fallible function).
**Hidden:** nothing — but a lazy Go programmer can still write `if err != nil { /* ignore */ }`,
because Go forces *receipt*, not *checking*.

## 47.1.3 — Go: the deliberate middle

Go's `error` is an interface value, returned in-band as the last result. The compiler forces you
to *receive* it — you cannot call `os.ReadFile` and pretend it returns one value — but nothing
forces you to *test* it. Go's position: explicitness without ceremony.

```go
data, err := os.ReadFile(path)
if err != nil {
    return fmt.Errorf("read export %s: %w", path, err)
}
```

The `if err != nil` idiom is verbose on purpose: **propagation is written, never implied**. The
cost is the well-known failure mode of the unchecked error — a whole section of
[type-safe handling](../02-deep-dive/02-type-safe-handling-and-common-architecture.md) is dedicated to it.

## 47.1.4 — Hybrids: every language is drifting toward both

Modern languages converge on offering *both* mechanisms and letting libraries choose:

| Language | Built-in exceptions | Built-in result type | Community convention |
| -------- | ------------------- | -------------------- |-------------------- |
| JS/TS | `throw` | none (use discriminated unions) | custom `Error` subclasses + `unknown` catches |
| Python | `raise` | none in stdlib (libraries: `returns`) | exceptions dominate |
| Java | yes (checked + unchecked) | `Optional` only | exceptions dominate |
| C# | yes | none in stdlib (NuGet: LanguageExt, CSharpFunctionalExtensions) | exceptions dominate |
| PHP | yes (`Throwable`) | none | exceptions dominate |
| Kotlin | yes (all unchecked) | `Result<T>` since 1.3 (stable 1.5) | exceptions by default, `Result` in APIs |
| Swift | yes (`throws`) | `Result<Success, Failure>` since Swift 5; typed `throws` since Swift 6 | `throws` for expected, `Result` when composing |
| Go | panic (unrecoverable only) | `error` interface | results only |
| Rust | panic (bugs only) | `Result<T, E>` | results only |

> The drift matters: **Kotlin and Swift now give you a stdlib `Result`, and Swift 6's typed
> throws makes `throws` encode the error type too.** The exception/result dichotomy is blurring
> into "how much does the signature admit?"

## 47.1.5 — Choosing inside a language that offers both

When a language offers both (Kotlin, Swift, modern JS with a Result pattern, Java with Optional
+ exceptions), the decision rule is the same everywhere:

1. **Exceptions for exceptional, unrecoverable-at-this-layer conditions** — bugs, violated
   preconditions, cancellation signals.
2. **Results/typed outcomes for expected, recoverable business outcomes** — card declined,
   idempotency conflict, tenant quota exceeded — anything a caller might branch on.
3. **Never both for the same condition.** If `checkout()` sometimes throws `DeclineException`
   and sometimes returns `Err(Decline)`, every caller needs two code paths and one will be
   forgotten.

## Key data / numbers

- Java has shipped **checked exceptions since JDK 1.0 (1996)**; the debate to remove them is
  older than most languages in this chapter.
- Rust's `?` operator: stable since **Rust 1.13 (2016)**; `#[must_use]` on `Result` is what
  makes ignored results a hard compiler error.
- Go 1 release notes state the design intent: errors are **values**, and `panic` is reserved for
  exceptional conditions the programmer cannot recover from at the call site.
- Kotlin `Result<T>`: experimental in **1.3**, stable in **1.5**; `runCatching` is its
  exception-catching constructor (with a famous cancellation pitfall — see
  [47.13](./05-async-constructs-and-pitfalls.md)).
- Swift `Result`: **Swift 5.0**; typed throws (`throws (some Error)`) arrived in **Swift 6**
  (SE-0413).
- ES2022 standardized `new Error(msg, { cause })` — before that, every JS library invented its
  own `cause` field.

## Real-world use case — Acme SaaS

Acme's billing service was Java (exceptions), its ingest was Go (error returns), and its API was
TypeScript. A `Checkout` decline raised in Java passed through a Go gRPC client that mapped *any*
non-nil error to `INTERNAL`, so the TypeScript frontend showed "something went wrong" instead of
"card declined." The fix was not "convert Java to results" — it was
[translating at the boundary](../02-deep-dive/02-type-safe-handling-and-common-architecture.md): Java
kept throwing `CheckoutException(code=CARD_DECLINED, retryable=false)`, the gRPC layer mapped the
code to a typed gRPC status, and TS matched on the code. Same taxonomy, three idioms.

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| Exceptions everywhere | Concise happy path | Invisible signatures; catch-all risk | Scripts, tools, truly exceptional paths |
| Results everywhere | Honest signatures; exhaustive matching | Verbose propagation | Libraries, Go/Rust, business-critical paths |
| Hybrid by rule | Right tool per condition | Requires a written team rule | Any language with both (Kotlin, Swift, TS+Result) |
| Hybrid by habit | — | Two paths per error; one gets forgotten | Never |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Encode expected business failures as values/results | Throw for "card declined" and also return a decline code |
| Throw only for exceptional or unrecoverable conditions | Use exceptions as the primary business API in Go/Rust |
| Write the team rule for which condition uses which mechanism | Let each developer decide per function |
| Preserve the cause with the native chaining API when throwing | Re-throw `new Error(e.message)` and drop the cause |

## Common mistakes

- **Exception-driven business flow** — a `try/catch` around a decline that is really a `switch`
  on a result. Symptom: stack traces in logs for routine declines. Fix: return the outcome.
- **Result-shaped exceptions** — throwing a typed exception and catching it one frame up.
  Symptom: unreachable code between throw and catch. Fix: return it.
- **Mixed semantics on one function** — half the failure modes throw, half return. Symptom:
  callers with duplicate handling. Fix: pick one per function, document it in the signature.
- **Forgetting Java's unchecked half** — treating "Java has checked exceptions" as "the
  compiler catches my errors." `NullPointerException` and framework exceptions still escape.

## Checklist

- [ ] Can a caller see every *expected* failure of this function from its signature alone?
- [ ] Is each condition classified once: exceptional → throw, expected → return?
- [ ] Does every thrown error preserve its cause via the native chaining API?
- [ ] In Go, is every `err` checked (enforced with `errcheck`/`staticcheck`)?
- [ ] In Rust, have you avoided `unwrap`/`expect` outside tests and genuinely fatal paths?

## Related

- [Language Comparison at a Glance](./02-language-comparison-at-a-glance.md)
- [Native Chaining and Wrapping](../02-deep-dive/01-native-chaining-and-wrapping-capabilities.md)
- [Type-Safe Error Handling](../02-deep-dive/02-type-safe-handling-and-common-architecture.md)
- [Chapter 7 — Exception vs Result Control Flow](../../../part-03-error-models/07-error-classes-types-and-structured-results/README.md)
