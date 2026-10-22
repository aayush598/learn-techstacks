# Exhaustiveness and Compiler Assistance

> Part III · Chapter 7 · Section 7.18 · _Estimated reading time: 18 min_
> **Prerequisite:** [Typed vs Untyped Errors and Union Types](../01-concepts/02-typed-vs-untyped-and-unions.md)

## In one sentence

**Exhaustiveness checking** turns "did you handle every failure?" from a code-review question into
a compiler-enforced guarantee, so adding a new failure kind automatically points at every handler
that must change.

## Why this matters in production

The most expensive error-handling bugs are **omissions**: a handler that handles three of four
provider outcomes, a mapper that never learned about a new code, a recovery path with no case for
`nil`. Exhaustiveness checking makes those omissions impossible to compile. The compiler becomes
your failure-path audit — continuously, for free.

## Discriminated unions + `never`

The mechanism: give each variant a **literal discriminant**, then use `never` in the `default`
branch. If a variant is unhandled, it is not `never`, and the assignment fails to compile.

```ts
type DbFailure =
  | { kind: "unique_violation"; constraint: string }
  | { kind: "deadlock" }
  | { kind: "serialization_failure" }
  | { kind: "connection_refused" }
  | { kind: "query_timeout"; ms: number };

function recover(f: DbFailure): Recovery {
  switch (f.kind) {
    case "unique_violation":       return { action: "return_conflict", constraint: f.constraint };
    case "deadlock":               return { action: "retry", backoffMs: 50 };
    case "serialization_failure":  return { action: "retry", backoffMs: 100 };
    case "connection_refused":     return { action: "fail_fast" };
    case "query_timeout":          return { action: "retry", backoffMs: f.ms };
    default: {
      const _exhaustive: never = f;   // <- compile error if a kind is missed
      throw new Error(`Unhandled DbFailure: ${JSON.stringify(_exhaustive)}`);
    }
  }
}
```

Add `{ kind: "lock_timeout" }` and **this function stops compiling** until it is handled. That is the
whole value.

## Exhaustiveness over codes

Codes live in the registry as a string union. The same technique applies.

```ts
type PaymentCode =
  | "PAYMENT_CARD_DECLINED"
  | "PAYMENT_INSUFFICIENT_FUNDS"
  | "PAYMENT_PROVIDER_TIMEOUT"
  | "PAYMENT_INVALID_REQUEST";

const HTTP: Record<PaymentCode, number> = {
  PAYMENT_CARD_DECLINED:     402,
  PAYMENT_INSUFFICIENT_FUNDS: 402,
  PAYMENT_PROVIDER_TIMEOUT:  503,
  PAYMENT_INVALID_REQUEST:   422,
};
```

A `Record<Union, T>` **forces total coverage**: deleting a code from the union is fine, but adding
one without an entry is a compile error. This is the lightest exhaustive pattern and the one to
reach for first for mapping tables.

## Exhaustiveness without a switch

Modern TypeScript offers `satisfies` and assertion helpers.

```ts
// Helper that compiles only when all variants are included.
function assertNever(x: never): never {
  throw new Error(`Unexpected variant: ${JSON.stringify(x)}`);
}

function uiAction(code: PaymentCode): string {
  if (code === "PAYMENT_CARD_DECLINED") return "show_decline_message";
  if (code === "PAYMENT_INSUFFICIENT_FUNDS") return "show_funds_message";
  if (code === "PAYMENT_PROVIDER_TIMEOUT") return "offer_retry";
  return assertNever(code);   // compile error if a code is unhandled
}
```

Rust does this natively (`match` requires all arms or a `_`); Kotlin has `sealed` classes/exhaustive
`when`; Swift has exhaustive `switch` over enums.

## Handling the "unknown" case honestly

Exhaustiveness applies to **closed** sets. When you must handle an **open** set (a vendor's error
list you do not control), do **not** pretend it is closed — provide an explicit `unknown` variant
and map into it.

```ts
type ProviderOutcome =
  | { kind: "succeeded"; id: string }
  | { kind: "declined"; reason: string }
  | { kind: "unknown"; raw: string };   // explicit, not a silent default

function toProviderOutcome(raw: string): ProviderOutcome {
  if (raw === "succeeded") return { kind: "succeeded", id: "" };
  if (raw.startsWith("declined:")) return { kind: "declined", reason: raw.slice(9) };
  return { kind: "unknown", raw };      // logged, not swallowed
}
```

Now the union is closed *and* honest, and `unknown` is a deliberate, observable case.

## Worked example — the registry as a closed union

```ts
// The single source of truth: a const tuple drives the union.
export const ERROR_CODES = [
  "VALIDATION_FAILED",
  "PAYMENT_CARD_DECLINED",
  "PAYMENT_PROVIDER_TIMEOUT",
  "DB_DEADLOCK",
  "INTERNAL_UNEXPECTED",
] as const;

export type ErrorCode = typeof ERROR_CODES[number];

// Every code must have an HTTP mapping or the build fails.
export const HTTP_STATUS: Record<ErrorCode, number> = {
  VALIDATION_FAILED: 422,
  PAYMENT_CARD_DECLINED: 402,
  PAYMENT_PROVIDER_TIMEOUT: 503,
  DB_DEADLOCK: 503,
  INTERNAL_UNEXPECTED: 500,
};
```

Adding `"AGENT_TOKEN_LIMIT"` to `ERROR_CODES` immediately breaks `HTTP_STATUS`, the retry table, and
the user-message table until each is updated — exactly the review you wanted.

## Key data / numbers

- **TypeScript `switch` narrowing + `never`** is the standard exhaustiveness idiom; `strictNullChecks`
  is required.
- **`Record<Union, T>`** is the lightest total-coverage construct and works for mapping tables.
- **`assertNever`/`assertExhaustive`** helpers are common; ESLint's `@typescript-eslint/switch-
  exhaustiveness-check` can flag missing cases statically.
- **Open sets** must include an explicit `unknown` variant; never rely on a silent `default`.
- **Tagged unions** with a literal discriminant are required — booleans/optionals do not narrow.

## Real-world use case — Acme SaaS

Acme's HTTP mapper was a chain of `if (err.code === ...)` returning defaults for anything unknown.
When a new `PAYMENT_REQUIRES_3DS` code shipped, it silently fell through to `500`, so customers saw
"something went wrong" and support had no actionable code. After modeling `ErrorCode` as a closed
union and every mapper as `Record<ErrorCode, T>`, adding the code failed the build across the HTTP,
retry, and UI-message tables until all three were updated. The class of "forgot to map the new
code" bugs disappeared.

## Trade-offs

| Technique | Guarantees | Cost |
| --------- | ---------- | ---- |
| `switch` + `never` | Exhaustive handling | Boilerplate per handler |
| `Record<Union, T>` | Total mapping tables | One shape per table |
| `satisfies` | Type-checked literal | Newer TS only |
| Runtime registry validation | Catches untyped/dynamic gaps | Runtime-only, later failure |
| No exhaustiveness | None | Missing cases ship |

Use **compile-time** exhaustiveness for closed sets and **runtime** checks for dynamic data that
crosses a process boundary (a code from an old client).

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Use literal discriminants + `never` | Rely on a silent `default` |
| Model open sets with explicit `unknown` | Pretend a vendor list is closed |
| Use `Record<Union, T>` for mappings | `Partial<Record<...>>` (hides gaps) |
| Add runtime validation at boundaries | Trust compile-time only for external data |
| Let new variants break the build | Add variants without updating handlers |

## Common mistakes

- **Silent `default`** that returns a generic value instead of asserting `never`.
- **`Partial<Record<...>>`** mapping tables that allow missing codes.
- **Non-literal discriminants** (`boolean`, optional) that do not narrow.
- **Treating an open set as closed**, so a new vendor code falls into a wrong branch.
- **No runtime check** for codes arriving from clients/queues.

## Checklist

- [ ] Do all failure unions have a literal discriminant?
- [ ] Does every `switch` end in a `never` guard?
- [ ] Are mapping tables `Record<Union, T>`, not partial?
- [ ] Are open sets modeled with an explicit `unknown` variant?
- [ ] Is there runtime validation for external/dynamic codes?

## Related

- [Typed vs Untyped Errors and Union Types](../01-concepts/02-typed-vs-untyped-and-unions.md)
- [Type Safety Across Async Boundaries](./02-type-safety-across-async-boundaries.md)
- [Chapter 8 — Error Codes and Error Registries](../../08-error-codes-and-error-registries/README.md)
