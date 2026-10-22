# Typed vs Untyped Errors and Union Types

> Part III · Chapter 7 · Sections 7.7, 7.10 · _Estimated reading time: 15 min_
> **Prerequisite:** [Native vs Custom Exceptions](./01-native-vs-custom-exceptions.md)

## In one sentence

An **untyped** error is `unknown` and forces defensive checks everywhere; a **typed** error declares
which failures a function can produce, and a **union type** enumerates exactly those failures so the
compiler can verify each is handled.

## Why this matters in production

Untyped errors are the default in JavaScript and most dynamic languages: any call can throw
anything. That means every catch is a guess, and a missed case is a silent bug in production. Typed
failures — especially discriminated unions — move that knowledge into the type system, where a
forgotten case is a compile error, not a 2am incident.

## Typed vs untyped (7.7)

| Dimension | Untyped | Typed |
| --------- | ------- | ----- |
| Type of a caught error | `unknown` | A named union/class |
| Failure documentation | Comments/README | The signature |
| Missed case | Silent runtime bug | Compile error |
| Refactor safety | Low | High |
| Language support | Everywhere | TS, Rust, Haskell, Kotlin (sealed), Swift |

```ts
// Untyped: the signature lies about what can happen.
function parseConfig(raw: string): Config { /* may throw anything */ }

// Typed: the possible failures are part of the contract.
function parseConfig(raw: string): Result<Config, ConfigError> { /* ... */ }
```

> ⚠️ **Hazard.** `catch (e)` in TypeScript types `e` as `unknown` (with
> `useUnknownInCatchVariables`) — good. Do not cast `as any` to "make it compile"; that discards the
> only safety you have.

## Narrowing untyped errors

When you must accept `unknown`, **narrow immediately** into known buckets, then handle.

```ts
function classify(e: unknown): AppError {
  if (e instanceof AppError) return e;                 // already ours
  if (e instanceof TypeError) return toErrorObject(e, { code: "INTERNAL_TYPE_ERROR" });
  if (isDbError(e)) return mapDbError(e);              // structural check
  return toErrorObject(e);                             // safe fallback
}
```

Order matters: check **most specific first**, and always end with a total fallback so no path
returns `undefined`.

## Union types for known failures (7.10)

A **discriminated union** tags each variant with a literal field (the discriminant), usually `kind`
or `type`. The compiler can then narrow exhaustively.

```ts
type PaymentFailure =
  | { kind: "card_declined"; declineCode: string }
  | { kind: "insufficient_funds" }
  | { kind: "provider_timeout"; provider: string }
  | { kind: "invalid_request"; field: string; reason: string };

function handle(f: PaymentFailure): string {
  switch (f.kind) {
    case "card_declined":     return `Declined: ${f.declineCode}`;
    case "insufficient_funds": return "Insufficient funds";
    case "provider_timeout":  return `Provider ${f.provider} timed out`;
    case "invalid_request":   return `Bad field ${f.field}`;
    default: {
      const _never: never = f;        // compile error if a variant is unhandled
      return _never;
    }
  }
}
```

Key properties of a good union:

- **Literal discriminant** (`kind`, `type`, `status`, `code`) — never a boolean soup.
- **Minimal per-variant data** — a variant carries only the fields that make sense for it.
- **Closed set** — adding a variant should be a deliberate act that ripples to all handlers.

## Union vs class hierarchy

| | Discriminated union | Class hierarchy |
| - | ------------------- | --------------- |
| Exhaustiveness | ✅ Compiler-checked | ❌ Usually not |
| Serialization | Trivial (plain objects) | Needs custom code |
| Methods/behavior | None (data only) | Yes |
| Extensibility | Must update consumers | Open for extension |
| Best for | Known, closed failure sets | Behavior-rich taxonomies |

Unions shine for **known failures** (validation, provider outcomes) where the set is closed and the
data is simple. Classes shine when errors have **behavior** (custom `format()`, chaining helpers)
or when a taxonomy genuinely benefits from inheritance.

## Worked example

```ts
// A union that models every outcome of an idempotent charge attempt.
type ChargeOutcome =
  | { kind: "succeeded"; chargeId: string }
  | { kind: "duplicate"; chargeId: string }             // idempotency replay
  | { kind: "declined"; code: string }
  | { kind: "retryable"; provider: string; retryAfterMs: number };

async function charge(idemKey: string, amount: Money): Promise<ChargeOutcome> {
  try {
    const res = await stripe.charges.create({ amount: amount.amount }, { idempotencyKey: idemKey });
    return { kind: "succeeded", chargeId: res.id };
  } catch (e) {
    if (isIdempotencyHit(e)) return { kind: "duplicate", chargeId: idOf(e) };
    if (isCardDeclined(e)) return { kind: "declined", code: declineCodeOf(e) };
    if (isRetryable(e)) return { kind: "retryable", provider: "stripe", retryAfterMs: 2000 };
    throw toErrorObject(e);                             // truly unexpected
  }
}
```

The caller sees the whole outcome space in the return type and cannot forget `duplicate`.

## Key data / numbers

- **`useUnknownInCatchVariables`** became default under TypeScript `strict` in 4.4; caught values
  are `unknown`, not `any`.
- **Discriminant field names in the wild:** `kind` (Rust `enum`-style), `type` (tagged unions,
  Redux), `status` (state machines), `code` (API errors).
- **Stripe decline codes** (`card_declined`, `insufficient_funds`, `expired_card`,
  `processing_error`) map naturally to union variants.
- Keep unions **closed**; adding a variant is a breaking change for exhaustive consumers.

## Real-world use case — Checkout

Acme's `Checkout` service returned `Promise<Charge>` and threw for every non-success. Callers could
not distinguish a **duplicate** (safe, return the existing order) from a **retryable timeout**
(retry) from a **decline** (show a message). By returning `ChargeOutcome` as a union, the saga
handler became an exhaustive `switch`, and a new engineer adding a `requires_3ds` variant got a
compile error pointing at every place that needed updating. The result: no missed outcome, and
duplicate-charge bugs vanished.

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| Untyped `unknown` + narrow | Works everywhere | No compile-time safety | Legacy/dynamic code, adapters |
| Closed union | Exhaustive, serializable | Must update consumers | Known failure sets |
| Class hierarchy | Behavior, open | No exhaustiveness | Behavior-rich taxonomies |
| Union of classes | Both | More ceremony | Shared behavior + exhaustive set |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Give each variant a literal discriminant | Model variants with optional fields |
| Narrow `unknown` immediately | Cast with `as any` |
| Keep unions closed and documented | Add variants without updating consumers |
| Use a total fallback in narrowing | Return `undefined` for unclassified errors |

## Common mistakes

- **Boolean-soup unions** (`{ ok?: boolean; error?: string }`) — not discriminated, not exhaustive.
- **Overlapping variants** with no discriminant; `kind` inferred unreliably.
- **Unbounded unions** that mirror an open vendor error list.
- **Casting caught errors to `any`**, discarding the only compile-time check.

## Checklist

- [ ] Do functions declare their possible failures in the type signature?
- [ ] Is every untyped `unknown` narrowed before use?
- [ ] Do unions have a literal discriminant and a `never` guard?
- [ ] Is the union closed and documented?
- [ ] Are new variants impossible to add without compiler feedback?

## Related

- [Result Types and Algebraic Data Types](./03-result-types-and-adts.md)
- [Exhaustiveness and Compiler Assistance](../02-deep-dive/01-exhaustiveness-and-compiler-assistance.md)
- [Result Type and Union Errors in Practice](../03-practical-examples/01-result-type-and-union-errors.md)
