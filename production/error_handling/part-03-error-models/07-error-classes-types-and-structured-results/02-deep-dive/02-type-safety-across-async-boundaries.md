# Type Safety Across Async Boundaries and Reusable Primitives

> Part III · Chapter 7 · Sections 7.19–7.20 · _Estimated reading time: 18 min_
> **Prerequisite:** [Exhaustiveness and Compiler Assistance](./01-exhaustiveness-and-compiler-assistance.md)

## In one sentence

Async boundaries — promises, workers, queues, and serialization — **erase types at runtime**, so
type safety must be reintroduced with explicit wrapping, parsing, and a small set of **reusable
primitives** rather than per-call-site trust.

## Why this matters in production

TypeScript types vanish at runtime. A `Promise<Result<T, E>>` looks safe but a rejected promise is
*not* an `Err`; a code deserialized from a queue is just a string until validated; an error that
crosses a worker boundary loses its class (`instanceof` returns false). Every one of these is a
type-safety hole that compiles cleanly and fails in production. The fix is primitives that convert
the boundary into a typed, validated value.

## The async holes (7.19)

| Boundary | What survives | What breaks |
| -------- | ------------- | ----------- |
| `await` a rejected promise | — | Rejection ≠ `Result.Err`; it throws |
| `Promise.all` | Rejects on first failure | Siblings keep running; their errors are lost |
| `Promise.allSettled` | `status` + value/reason | No typed error; `reason` is `unknown` |
| Worker / iframe / VM | `name`, `message`, `code` strings | `instanceof`, class methods, prototypes |
| Queue / HTTP / disk | JSON values only | `Error`, `Map`, `Date`, methods |
| `structuredClone` | Most data | Functions, class prototypes, symbols |

### Promise rejection is not a typed failure

```ts
// The signature promises a typed failure, but a rejection bypasses E entirely.
async function fetchUser(id: string): Promise<Result<User, FetchError>> {
  const res = await fetch(`/users/${id}`);   // network error REJECTS here
  if (!res.ok) return err({ code: "HTTP_ERROR", status: res.status });
  return ok(await res.json());
}

// Fix: convert rejections into typed Err.
async function safe<T>(p: Promise<T>): Promise<Result<T, unknown>> {
  try { return ok(await p); } catch (e) { return err(e); }
}

async function fetchUser(id: string): Promise<Result<User, FetchError>> {
  const r = await safe(fetch(`/users/${id}`));
  if (!r.ok) return err({ code: "NETWORK_ERROR", cause: r.error });
  const res = r.value;
  if (!res.ok) return err({ code: "HTTP_ERROR", status: res.status });
  return ok(await res.json() as User);
}
```

Rule: **never let a rejection escape a `Result`-returning function.** Wrap at the async edge.

### Parallel work

```ts
// All-or-nothing (fail fast) — use when partial success is unacceptable.
const [a, b] = await Promise.all([stepA(), stepB()]);

// Partial success — use allSettled, then partition.
const settled = await Promise.allSettled([stepA(), stepB()]);
const okValues = settled.filter(isFulfilled).map((s) => s.value);
const failures = settled.filter(isRejected).map((s) => toErrorObject(s.reason));
```

Choose deliberately; `Promise.all` silently discards sibling errors, which is a common source of
"one step failed but we do not know why the other also did."

### Worker and serialization boundaries

```ts
// A worker cannot send a class instance; send the model as plain JSON + a discriminant.
interface SerializedError {
  code: string; category: ErrorCategory; message: string;
  retryable: boolean; metadata: Record<string, unknown>; correlationId?: string;
}

function rehydrate(raw: unknown): AppError {
  const parsed = SerializedErrorSchema.safeParse(raw);   // runtime validation
  if (!parsed.success) return toErrorObject(raw, { metadata: { invalid: "serialized_error" } });
  return new AppErrorClass({
    code: parsed.data.code,
    category: parsed.data.category,
    message: parsed.data.message,
    retryable: parsed.data.retryable,
    metadata: parsed.data.metadata,
    correlationId: parsed.data.correlationId,
  });
}
```

At every serialization boundary, **parse and validate**; never cast (`as SerializedError`).

## Reusable error primitives (7.20)

Rather than re-deriving type safety per call site, build a tiny shared library of primitives. Keep
it small (style guide: "simplest design that satisfies the requirement").

| Primitive | Purpose | Signature (sketch) |
| --------- | ------- | ------------------ |
| `ok` / `err` | Construct results | `<T>(v: T): Ok<T>` |
| `tryCatch` / `safe` | Wrap a throw into `Result` | `<T>(fn: () => T): Result<T, E>` |
| `tryCatchAsync` | Async wrap, catches rejections | `<T>(fn: () => Promise<T>): Promise<Result<T, E>>` |
| `fromThrow` | Convert a throw-based call | `<T>(fn: () => T, mapErr): Result<T, AppError>` |
| `map` / `mapErr` / `flatMap` | Sequence results | pure helpers |
| `unwrapOr` | Default on failure | `<T>(r: Result<T,E>, d: T): T` |
| `assertNever` | Exhaustiveness | `(x: never): never` |
| `isAppError` | Runtime guard | `(e: unknown): e is AppError` |
| `toErrorObject` | Normalize anything | `(e: unknown, ctx?): AppError` |
| `rehydrate` | Parse serialized errors | `(raw: unknown): AppError` |

```ts
export async function tryCatchAsync<T>(
  fn: () => Promise<T>,
  mapError: (cause: unknown) => AppErrorClass = (c) => toErrorObject(c),
): Promise<Result<T, AppErrorClass>> {
  try {
    return ok(await fn());
  } catch (cause) {
    return err(mapError(cause));
  }
}
```

These primitives do three jobs: (1) they **convert** boundaries into typed values, (2) they
**normalize** unexpected errors into the model, and (3) they **eliminate boilerplate** so the
easiest path is the correct one (Chapter 53).

## Worked example — an async job with typed outcomes

```ts
type FetchPageError =
  | { code: "NETWORK_ERROR"; cause: unknown }
  | { code: "HTTP_ERROR"; status: number }
  | { code: "INVALID_BODY"; cause: unknown };

async function fetchPage(url: string): Promise<Result<Page, FetchPageError>> {
  const net = await tryCatchAsync(
    () => fetch(url),
    (cause) => new AppErrorClass({
      code: "NETWORK_ERROR", category: "external",
      message: `GET ${url} failed`, cause,
    }),
  );
  if (!net.ok) return err({ code: "NETWORK_ERROR", cause: net.error });

  if (!net.value.ok) return err({ code: "HTTP_ERROR", status: net.value.status });

  const body = await tryCatchAsync(() => net.value.json() as Promise<unknown>,
    (cause) => toErrorObject(cause));
  if (!body.ok) return err({ code: "INVALID_BODY", cause: body.error });

  return ok(parsePage(body.value));
}
```

Every await is guarded; the failure union lists the entire error space; the caller can switch
exhaustively. No rejection can escape.

## Key data / numbers

- **`Error.cause` / `structuredClone`**: functions and prototypes are not cloneable; class identity
  does not survive `structuredClone` in the same way `instanceof` expects.
- **`Promise.all` rejects fast** and discards results; **`allSettled` never rejects** and returns
  every outcome (Node ≥ 12.9 / ES2020).
- **`AbortController`** is the standard cancellation primitive; a cancelled async op should surface a
  distinguishable (often non-error) outcome, not a random rejection.
- **Runtime validation** (e.g. schema parse) is mandatory at serialization boundaries; casts are not
  validation.

## Real-world use case — ExportJob worker

Acme's `ExportJob` ran in a worker and returned a `Result`. The main process assumed `result.error`
was an `AppError` and called `.category`, but when the worker crashed it sent a plain serialized
object without `category`, causing `undefined` to flow into the retry engine — which retried a
permanent failure forever. The fix: define `SerializedError`, validate with a schema on rehydrate,
and default missing fields via `toErrorObject`. The retry engine now always receives a complete
`AppError`, and malformed worker payloads are counted as a metric instead of corrupting recovery.

## Trade-offs

| Approach | Safety | Cost | When to use |
| -------- | ------ | ---- | ----------- |
| Trust types across boundary | None (unsafe) | Zero | Never |
| Cast with `as` | None | Zero | Never |
| Runtime schema validation | High | Parse cost | All external/serialized boundaries |
| `tryCatchAsync` + normalization | High for async | Wrap boilerplate | Every async edge |
| Shared primitive library | High, consistent | Initial build | Any non-trivial codebase |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Wrap async with `tryCatchAsync`/`safe` | Let rejections bypass `Result` |
| Parse & validate serialized errors | Cast `as SerializedError` |
| Use `allSettled` for partial success | Assume `Promise.all` preserves sibling errors |
| Centralize primitives in one module | Reinvent wrappers per file |
| Rehydrate to a full `AppError` | Assume class methods survive serialization |

## Common mistakes

- **Rejection ≠ `Err`** — a `Promise<Result<...>>` that throws on network errors.
- **`instanceof` across workers** — always false; use `code`.
- **`as` casts** where schema validation is needed.
- **`Promise.all` partial failure** losing sibling errors.
- **Per-call-site wrappers** that drift in behavior.

## Checklist

- [ ] Are all rejections converted to typed failures at async edges?
- [ ] Are parallel operations using `all` or `allSettled` deliberately?
- [ ] Is every serialized error parsed and validated on rehydrate?
- [ ] Are class methods/prototypes never assumed across boundaries?
- [ ] Are primitives centralized and reused, not reimplemented?

## Related

- [Exhaustiveness and Compiler Assistance](./01-exhaustiveness-and-compiler-assistance.md)
- [Result Types and Algebraic Data Types](../01-concepts/03-result-types-and-adts.md)
- [Chapter 31 — Asynchronous Error Handling](../../../part-12-async-and-background-jobs/31-asynchronous-error-handling/README.md)
