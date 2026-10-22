# Result Types and Algebraic Data Types

> Part III · Chapter 7 · Sections 7.8–7.9 · _Estimated reading time: 16 min_
> **Prerequisite:** [Typed vs Untyped Errors and Union Types](./02-typed-vs-untyped-and-unions.md)

## In one sentence

A **`Result<T, E>`** is a value that is either a success carrying `T` or a failure carrying `E` —
modeling expected failure as ordinary data instead of an out-of-band control flow transfer.

## Why this matters in production

Exceptions are excellent for **unexpected** failures but poor for **expected** ones that are part of
normal business flow. When "not found" and "insufficient funds" are thrown, callers forget to handle
them, global handlers make business decisions they cannot make, and the type system cannot help.
`Result` makes every expected failure **visible in the signature** and impossible to ignore.

## Algebraic data types (7.8)

An **algebraic data type** (ADT) is a type built by combining simpler types in two ways:

- **Sum ("OR")** — a value is one of several variants: `Success | Failure`. This is a tagged union.
- **Product ("AND")** — a value has several fields together: `{ id: string; amount: number }`.
  This is a record/struct.

`Result` is a **sum type of two product types**:

```text
Result<T, E>  =  Success<T>  |  Failure<E>
                  { value: T }    { error: E }
```

Contrast with how we usually code (exceptions as a hidden third "channel"):

| Model | Success channel | Failure channel | Visible in type? |
| ----- | --------------- | --------------- | ---------------- |
| Exceptions | return value | thrown exception | ❌ No |
| `Result` | `Ok(value)` | `Err(error)` | ✅ Yes |

Languages encode this differently: Rust `Result<T, E>`, Haskell `Either`, Kotlin `Result`,
Swift `Result<Success, Failure>`, and TypeScript via a discriminated union.

## Success/failure result types (7.9)

A minimal, ergonomic `Result` in TypeScript:

```ts
type Ok<T> = { readonly ok: true; readonly value: T };
type Err<E> = { readonly ok: false; readonly error: E };
type Result<T, E> = Ok<T> | Err<E>;

const ok = <T>(value: T): Ok<T> => ({ ok: true, value });
const err = <E>(error: E): Err<E> => ({ ok: false, error });
```

The discriminant is `ok`. Consumers must check it before accessing `value`, and exhaustive
narrowing works automatically.

### Why `E` should be typed

`Result<T, AppError>` is better than `Result<T>` because the failure type tells the caller **which**
failures are possible — a specific union of domain errors, not "anything".

```ts
type CreateUserError =
  | { code: "VALIDATION_FAILED"; details: FieldError[] }
  | { code: "EMAIL_TAKEN"; email: string };

function createUser(dto: CreateUserDTO): Result<User, CreateUserError> { /* ... */ }
```

Now the caller's `switch` over `result.error.code` is exhaustive, and adding a new failure kind is a
compile error at every call site.

### Combinators

Real code needs to sequence results without nesting `if`s.

```ts
function map<T, U, E>(r: Result<T, E>, f: (t: T) => U): Result<U, E> {
  return r.ok ? ok(f(r.value)) : r;
}

function flatMap<T, U, E>(r: Result<T, E>, f: (t: T) => Result<U, E>): Result<U, E> {
  return r.ok ? f(r.value) : r;
}
```

`map` transforms a success; `flatMap` (a.k.a. `andThen`, `chain`) sequences a step that itself can
fail. These two plus `mapErr` cover most needs without a library.

## Worked example

```ts
type ParseError =
  | { code: "EMPTY" }
  | { code: "NOT_JSON"; cause: unknown };

function parseJSON(raw: string): Result<unknown, ParseError> {
  if (!raw.trim()) return err({ code: "EMPTY" });
  try {
    return ok(JSON.parse(raw));
  } catch (cause) {
    return err({ code: "NOT_JSON", cause });
  }
}

function parseAmount(raw: string): Result<number, ParseError> {
  return map(parseJSON(raw), (v) => {
    if (typeof v !== "object" || v === null || typeof (v as any).amount !== "number") {
      throw new TypeError("amount is not a number");
    }
    return (v as { amount: number }).amount;
  });
}
```

Used at an API boundary, the handler can now distinguish `EMPTY` (204?) from `NOT_JSON` (400) from a
real bug — all without exceptions.

## When `Result` is the wrong tool

- **Deeply unexpected failures** (OOM, a bug, a broken invariant) — let them propagate and be
  caught at the boundary. Forcing every one into `Result` pollutes every signature.
- **Large call graphs with no local recovery** — threading `Result` through ten layers adds noise
  if only the top handles it.
- **Async combinators already exist:** `Promise.allSettled` returns per-item outcomes; do not
  reinvent it.

## Key data / numbers

- **`Promise.allSettled`** returns `{ status: "fulfilled", value }` or `{ status: "rejected",
  reason }` — a built-in result type for parallel work.
- **Go** returns `(T, error)` — a two-value result; **Rust** `Result<T, E>` is a first-class enum;
  **Kotlin** has `runCatching`/`Result`.
- Typical combinator set: `map`, `mapErr`, `flatMap`/`andThen`, `unwrapOr`, `match`, `fromThrow`.
- Keep `Result` in the **domain/application** layer; translate to exceptions or HTTP at the edge.

## Real-world use case — Acme SaaS

Acme's `ExportJob` builder chained several fallible steps (parse query, resolve schema, plan
shards). Using exceptions, any step's throw skipped remaining validation and produced a generic
`EXPORT_FAILED`. Rewritten with `Result<ExportPlan, ExportError>`, each step returned a typed
`ExportError` and the builder combined them with `flatMap`. The API could now return a specific,
actionable code per validation problem, and the scheduler knew exactly which failures were
retryable. No behavior was hidden in a catch block.

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| Exceptions | Familiar, propagate deep, keep signatures clean | Invisible in types, easy to forget | Unexpected failures |
| `Result` | Explicit, exhaustive, testable | Verbose, threading cost | Expected failures, validation, parsing |
| Hybrid | Each tool where it fits | Requires a stated rule | Most real systems |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Type `Result`'s failure as a union | `Result<T, any>` |
| Use `map`/`flatMap` to sequence | Deeply nest `if (r.ok)` |
| Reserve `Result` for expected failures | Force OOM/bugs through `Result` |
| Provide `fromThrow` for native calls | Wrap every native error manually |

## Common mistakes

- **`Result<T, string>`** — a message instead of a typed error; loses routing.
- **Ignoring the `Err` variant** (TS cannot force you without lint, but exhaustive checks help).
- **Mixing conventions** — half the module throws, half returns `Result`, with no boundary rule.
- **Reinventing `allSettled`** for parallel independent work.

## Checklist

- [ ] Is `Result` used only for expected, recoverable failures?
- [ ] Is the failure type a specific union, not `any`/`string`?
- [ ] Are `map`/`flatMap` used to avoid nested checks?
- [ ] Is there a rule for where `Result` stops and exceptions/H TTP begin?
- [ ] Are parallel outcomes handled with `allSettled`, not a custom type?

## Related

- [Exception vs Result Control Flow](./04-exception-vs-result-control-flow.md)
- [Typed vs Untyped Errors and Union Types](./02-typed-vs-untyped-and-unions.md)
- [Result Type and Union Errors in Practice](../03-practical-examples/01-result-type-and-union-errors.md)
