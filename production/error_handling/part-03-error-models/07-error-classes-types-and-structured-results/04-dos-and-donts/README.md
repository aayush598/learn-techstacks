# Chapter 7 — Do's and Don'ts

> Part III · Chapter 7 · All sections

A condensed rule set for error classes, types, and structured results.

## Native vs custom classes

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Wrap natives immediately at the edge | Let driver errors reach the domain |
| Give each layer a small error vocabulary | Extend framework exceptions in the domain |
| Justify a class by code + branching | Create a class per message |
| Keep the hierarchy flat (≤ 2 levels) | Build a deep `Domain→Billing→Invoice` tree |
| Name the condition (`PaymentProviderTimeoutError`) | `DataError`, `ServiceError`, `GeneralError` |

## Typed vs untyped

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Declare possible failures in the signature | Leave errors as `unknown` everywhere |
| Narrow `unknown` immediately and totally | Cast with `as any` |
| Use discriminated unions for known failures | Model variants with optional booleans |
| Keep unions closed and documented | Let unions mirror an open vendor list |

## Results and control flow

| ✅ Do | ❌ Don't |
| ----- | -------- |
| "Expected = value, unexpected = throw" | Throw for ordinary not-found/validation |
| Type `Result`'s failure as a union | `Result<T, string>` |
| Use `map`/`flatMap` to sequence | Nest `if (r.ok)` deeply |
| State one conversion boundary | Convert in three places inconsistently |
| Reserve `Result` for expected failures | Put OOM/bugs through `Result` |

## Exhaustiveness and async

| ✅ Do | ❌ Don't |
| ----- | -------- |
| End every `switch` with `never` | Use a silent `default` |
| Use `Record<Union, T>` for mappings | `Partial<Record<...>>` that hides gaps |
| Model open sets with explicit `unknown` | Pretend a vendor list is closed |
| Wrap async edges (`tryCatchAsync`) | Let rejections bypass `Result` |
| Validate serialized errors on rehydrate | Cast `as SerializedError` |
| Use `allSettled` for partial success | Assume `all` preserves sibling errors |

## Anti-patterns in the wild

1. **Class Explosion** — a class per message; nothing uses `instanceof`.
2. **The Deep Tree** — `catch (Base)`, which catches unrelated failures.
3. **Catch-All Routing** — `AppError` as the only type; every catch is identical.
4. **The Boolean Union** — `{ ok?: boolean; error?: string }`; not exhaustive.
5. **String Err** — `Result<T, string>`; no routing, no exhaustiveness.
6. **The Escaping Rejection** — `Promise<Result<...>>` that throws on network errors.
7. **The Realm Check** — `instanceof` across workers, silently false.

## Chapter checklist

- [ ] One primary convention (exceptions or results) with a stated boundary.
- [ ] Expected failures are values; unexpected failures throw.
- [ ] All known-failure unions are discriminated and closed.
- [ ] Every handler is exhaustive (`never` guard).
- [ ] Hierarchies are flat; names are specific.
- [ ] Async edges are wrapped; serialized errors are validated on rehydrate.
- [ ] Reusable primitives live in one shared module.

## Related

- [Chapter 7 Reference](../05-reference/README.md)
- [Chapter 6 — Designing the Application's Error Model](../../06-designing-the-applications-error-model/README.md)
- [Error-Handling Patterns and Anti-Patterns](../../../part-17-organization/46-error-handling-patterns-and-anti-patterns/README.md)
