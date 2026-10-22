# Chapter 7 — Reference

> Part III · Chapter 7 · Cheat sheet, decision tables, and glossary.

## Cheat sheet — the core rule

```text
Expected outcome        →  value (Result / typed return)
Unexpected failure      →  throw (caught at a boundary)
Bug / broken invariant  →  throw (fail fast)

One conversion point per direction. Never half-unwrap.
```

## Cheat sheet — `Result<T, E>`

```ts
type Ok<T>  = { readonly ok: true;  readonly value: T };
type Err<E> = { readonly ok: false; readonly error: E };
type Result<T, E> = Ok<T> | Err<E>;
```

| Primitive | Purpose |
| --------- | ------- |
| `ok` / `err` | Construct |
| `map` / `mapErr` | Transform success / failure |
| `flatMap` | Sequence a fallible step |
| `unwrapOr` | Default on failure |
| `match` | Collapse both branches |
| `tryCatch` / `tryCatchAsync` | Wrap a throw into a `Result` |
| `all` | All-or-nothing collection |
| `assertNever` | Exhaustiveness guard |

## Decision table — mechanism by situation

| Situation | Use |
| --------- | --- |
| Validation / business rule failure | `Result` or typed return |
| Not-found as a normal outcome | `Result` variant |
| Bug / invariant violation | Throw (fail fast) |
| Dependency/network error near a boundary | Throw, wrapped, caught at boundary |
| High-volume expected failure | `Result` (avoid stack capture cost) |
| Deep chain, handled only at the top | Throw (avoid threading noise) |
| Parallel independent work | `Promise.allSettled` |

## Decision table — class vs union vs `Result`

| Need | Choose |
| ---- | ------ |
| Behavior on the error (format/chain) | Custom class |
| Exhaustive handling of a closed set | Discriminated union |
| Expected failure flow through functions | `Result<T, E>` |
| Category-wide `instanceof` checks | Shallow class hierarchy |
| JSON/serialization boundary | Plain union + schema validation |

## Decision table — exhaustiveness technique

| Situation | Technique |
| --------- | --------- |
| Closed set of variants | `switch` + `never` |
| Mapping table over a code union | `Record<Union, T>` |
| Open/vendor set | Explicit `unknown` variant + runtime validation |
| External/dynamic data | Schema parse on rehydrate |

## Naming rules

```text
class  := <Layer><Condition>Error      PaymentProviderTimeoutError
factory:= verb/noun, stable            CardDeclined(...) → code PAYMENT_CARD_DECLINED
union  := { kind: "literal"; ...fields }
avoid  := DataError, ServiceError, GeneralError, MyError, Error2
```

## Chapter glossary

| Term | Meaning |
| ---- | ------- |
| Native error | Language/runtime error (`Error`, `TypeError`) |
| Custom error | Application-defined error class |
| Typed error | Failure type visible in the signature |
| Untyped error | `unknown`; forces defensive checks |
| Discriminated union | Union with a literal discriminant field |
| Algebraic data type | Sum (OR) / product (AND) composition |
| `Result<T, E>` | Success-or-failure value type |
| Discriminant | Literal field used to narrow a union |
| Exhaustiveness | Compiler-verified handling of all variants |
| `never` guard | Assignment that fails if a case is unhandled |
| Reusable primitive | Shared helper (`ok`, `tryCatch`, `assertNever`) |
| Rehydrate | Parse a serialized error back into the model |
| Realm | JS execution context; `instanceof` does not cross it |

## Standard references (by name, no links)

- **TypeScript `strict` / `useUnknownInCatchVariables`** — caught values are `unknown`.
- **`Promise.allSettled` (ES2020)** — per-item outcomes.
- **Rust `Result<T, E>` / Haskell `Either` / Kotlin `Result` / Swift `Result`** — language ADTs.
- **ESLint `switch-exhaustiveness-check`** — static exhaustiveness lint.

## Signposts

- Async propagation in depth → [Ch. 31](../../../part-12-async-and-background-jobs/31-asynchronous-error-handling/README.md)
- Codes and unions → [Ch. 8](../../08-error-codes-and-error-registries/README.md)
- Patterns and anti-patterns → [Ch. 46](../../../part-17-organization/46-error-handling-patterns-and-anti-patterns/README.md)

## Related

- [Chapter 7 Do's and Don'ts](../04-dos-and-donts/README.md)
- [Result Type and Union Errors in Practice](../03-practical-examples/01-result-type-and-union-errors.md)
- [Chapter 7 Overview](../README.md)
