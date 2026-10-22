# Hierarchies, Composition, and Naming

> Part III · Chapter 7 · Sections 7.14–7.17 · _Estimated reading time: 16 min_
> **Prerequisite:** [Native vs Custom Exceptions](./01-native-vs-custom-exceptions.md)

## In one sentence

Prefer **flat, composed error types over deep inheritance**; avoid **catch-all** types and
**ambiguous names**; and let the compiler, not convention, enforce the distinctions.

## Why this matters in production

Deep `Error` hierarchies look tidy in diagrams and become unmaintainable in code: a catch of the
base class silently catches unrelated failures, and adding a subclass requires understanding the
whole tree. Catch-all types (`AppError`) defeat precise handling. Ambiguous names (`DataError`,
`GeneralError`, `ServiceError`) tell a handler nothing. Each of these turns "handle the error" into
"guess the error."

## Inheritance vs composition (7.14)

**Inheritance** models "is-a": `CardDeclinedError is-a PaymentError is-a AppError`. **Composition**
models "has-a": an error *has* a category, *has* a code, *has* a cause.

| | Inheritance | Composition |
| - | ----------- | ----------- |
| Models | Taxonomy ("is-a") | Data ("has-a") |
| Exhaustiveness | Usually not | With unions, yes |
| Coupling | Child depends on parent internals | Loose |
| Adding a kind | New subclass (tree grows) | New value (set grows) |
| Catch precision | Base catch is broad/dangerous | Reconstruct via `code`/category |

Composition is the better default because **classification lives in data** (`code`, `category`),
not in the type tree. A `catch (e) { if (e.category === "payment") ... }` is precise; a
`catch (e) { if (e instanceof PaymentError) ... }` breaks the moment a sibling is introduced.

```ts
// Composition: one class, meaning in fields.
class AppError extends Error {
  constructor(readonly init: AppErrorInit) { super(init.message, { cause: init.cause }); }
  get category() { return this.init.category; }
  get code() { return this.init.code; }
}
```

## Avoiding deep hierarchies (7.15)

A useful rule: **never more than two levels** below the base (`AppError` → one category class).
Beyond that, inheritance is a smell.

```text
GOOD (flat, 2 levels)          BAD (deep, brittle)
AppError                       AppError
├── ValidationError            └── DomainError
├── PaymentError                   └── BillingError
├── DatabaseError                      └── InvoiceError
└── ExternalError                          └── InvoiceLineError
                                               └── TaxError   ← why?
```

Why depth hurts:

- **A base catch catches too much.** `catch (DomainError)` now catches unrelated failures.
- **Fragile base class.** Changing a parent affects every descendant.
- **Poor serialization.** A deep tree rarely maps cleanly to a flat wire shape.

## Avoiding catch-all types (7.16)

A **catch-all** is a type used for "any failure." Two variants are dangerous:

1. **The universal base** (`AppError` used as the *only* type): callers cannot branch; every catch
   is `catch (AppError)`.
2. **The generic wrapper** (`SomethingFailedError`): conveys no information and invites
   `instanceof` checks that always match.

Both convert precise failures into a single opaque bucket. The fix is not more classes but
**distinct categories/codes** that handlers can switch on. Keep a catch-all only as the
**terminal fallback** for truly unknown errors (`INTERNAL_UNEXPECTED`), never as a routing bucket.

## Avoiding ambiguous names (7.17)

Names must state the **condition**, not the source or the vibe.

| ❌ Ambiguous | ✅ Specific | Why |
| ----------- | ---------- | --- |
| `DataError` | `DatabaseConstraintError` | States the actual problem |
| `ServiceError` | `PaymentProviderTimeoutError` | Names the dependency + condition |
| `BusinessException` | `InsufficientBalanceError` | Names the rule violated |
| `GeneralError` | (delete it) | Means nothing |
| `MyError`, `CustomError` | `ValidationError` | Personal/placeholder names age poorly |
| `Error2`, `NewError` | `WebhookSignatureError` | Version suffixes hide meaning |

Naming rules:

- **Suffix with `Error`** (JS/TS convention) so `instanceof` and tooling recognize it.
- **State the condition**, not the layer only: `PaymentProviderTimeoutError` beats `PaymentError`.
- **Match the code's intent.** If `code = "PAYMENT_CARD_DECLINED"`, the class should be
  `CardDeclinedError` or a category class plus that code — not `PaymentError` alone.
- **No abbreviations** a newcomer must decode (`PDOException` is a framework leak).

## Worked example

```ts
// Before: deep, ambiguous, catch-all.
class ErrorBase {}
class GeneralError extends ErrorBase {}
class ServiceError extends GeneralError {}
class PaymentServiceError extends ServiceError {}
class PaymentServiceDeclinedError extends PaymentServiceError {}
// catch (ServiceError) — catches payments AND user service AND ...
```

```ts
// After: flat categories + precise codes.
class AppError extends Error { /* init as above */ }
class PaymentError extends AppError { /* category: "payment" */ }
class ValidationError extends AppError { /* category: "validation" */ }

// Precision comes from the code, not the depth.
const declined = new PaymentError({
  code: "PAYMENT_CARD_DECLINED",
  category: "payment",
  message: "Card declined",
});
```

Handlers now do `switch (e.code)` or `switch (e.category)` — precise and future-proof.

## Key data / numbers

- **`instanceof` is realm-bound** — it fails across Node worker threads, VM contexts, and
  iframes; use `code`/`category` there.
- **Error name suffix** `Error` is conventional in JS/TS, Java, Python (`...Error`), C# (`...Exception`),
  Go (no suffix; sentinel values), Rust (enum variants).
- **Named error constructors** (Node `Error.captureStackTrace`) let you hide internal frames.
- Common naming taxonomy: `<Layer><Condition>Error` (e.g. `PaymentProviderTimeoutError`).

## Real-world use case — Acme SaaS

Acme's codebase had `AppError` as the only error type, so every catch was `catch (AppError)` and
every handler ran the same generic recovery. A payment outage and a validation failure took
identical paths. Introducing **flat category classes** with distinct codes let the retry engine
retry only `ExternalError`s and the UI map only `ValidationError`s. The class count went from one to
eight — and handling precision went from zero to full, without a single deep subclass.

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| Flat categories + codes | Precise, serializable | Slightly more types | Default |
| Single class + codes | Simplest | No `instanceof` grouping | Small apps |
| Shallow tree (≤2 levels) | Some `instanceof` convenience | Can drift deep | Layered apps |
| Deep hierarchy | Feels organized | Brittle, over-broad catches | Avoid |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Keep hierarchies ≤ 2 levels | Build `Domain→Billing→Invoice→Tax` trees |
| Put meaning in `code`/`category` | Rely on `instanceof` depth |
| Name the condition precisely | `DataError`, `ServiceError`, `GeneralError` |
| Use one catch-all only as terminal fallback | Use a universal type as the only type |
| Suffix classes with `Error` | Name a class `MyError`/`Error2` |

## Common mistakes

- **Deep hierarchy** whose base catch is over-broad.
- **Catch-all as routing bucket** — opaque handling.
- **Ambiguous names** that force reading the implementation.
- **`instanceof` across realms** silently returning false.

## Checklist

- [ ] Is the hierarchy flat (≤ 2 levels)?
- [ ] Is classification in data (`code`, `category`), not in the type tree?
- [ ] Are there no catch-all types used for routing?
- [ ] Do names state the condition, not the source or a placeholder?
- [ ] Are new error kinds added without restructuring the hierarchy?

## Related

- [Native vs Custom Exceptions](./01-native-vs-custom-exceptions.md)
- [Exhaustiveness and Compiler Assistance](../02-deep-dive/01-exhaustiveness-and-compiler-assistance.md)
- [Custom Error Class Design in Practice](../03-practical-examples/02-custom-error-class-design.md)
