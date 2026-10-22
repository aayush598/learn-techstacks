# Practical: A `Result<T, E>` Implementation with Union Errors

> Part III · Chapter 7 · Sections 7.8–7.13 · _Estimated reading time: 24 min_
> **Prerequisite:** [Result Types and Algebraic Data Types](../01-concepts/03-result-types-and-adts.md)

## In one sentence

This file is a **complete, copy-ready `Result<T, E>`** with the combinators you actually need, union
error types, and an end-to-end example that shows how a caller handles every outcome without a
single `throw` for expected failures.

## Why this matters in production

Most teams either adopt a heavy library or hand-roll a `Result` that has no combinators (so call
sites nest `if`s) and no typed errors (so `E` is `string`). This implementation is small enough to
read in one sitting and complete enough to use in a real service.

## The core type

```ts
export type Ok<T> = { readonly ok: true; readonly value: T };
export type Err<E> = { readonly ok: false; readonly error: E };
export type Result<T, E> = Ok<T> | Err<E>;

export const ok = <T>(value: T): Ok<T> => ({ ok: true, value });
export const err = <E>(error: E): Err<E> => ({ ok: false, error });

export const isOk = <T, E>(r: Result<T, E>): r is Ok<T> => r.ok;
export const isErr = <T, E>(r: Result<T, E>): r is Err<E> => !r.ok;
```

## Combinators

```ts
// Transform a success; pass failures through untouched.
export function map<T, U, E>(r: Result<T, E>, f: (t: T) => U): Result<U, E> {
  return r.ok ? ok(f(r.value)) : r;
}

// Transform a failure; pass successes through untouched.
export function mapErr<T, E, F>(r: Result<T, E>, f: (e: E) => F): Result<T, F> {
  return r.ok ? r : err(f(r.error));
}

// Sequence a step that can itself fail.
export function flatMap<T, U, E>(r: Result<T, E>, f: (t: T) => Result<U, E>): Result<U, E> {
  return r.ok ? f(r.value) : r;
}

// Extract a value or a default.
export function unwrapOr<T, E>(r: Result<T, E>, fallback: T): T {
  return r.ok ? r.value : fallback;
}

// Collapse both branches into one value.
export function match<T, E, R>(
  r: Result<T, E>,
  onOk: (t: T) => R,
  onErr: (e: E) => R,
): R {
  return r.ok ? onOk(r.value) : onErr(r.error);
}

// Exhaustiveness helper.
export function assertNever(x: never): never {
  throw new Error(`Unexpected variant: ${JSON.stringify(x)}`);
}
```

## Async helpers

```ts
import { AppErrorClass, toErrorObject } from "../../../shared/errors";

// Convert a throw (including a rejected promise) into Result.
export async function tryCatchAsync<T, E = AppErrorClass>(
  fn: () => Promise<T>,
  mapError: (cause: unknown) => E = (c) => toErrorObject(c) as unknown as E,
): Promise<Result<T, E>> {
  try {
    return ok(await fn());
  } catch (cause) {
    return err(mapError(cause));
  }
}

// Synchronous version.
export function tryCatch<T, E = AppErrorClass>(
  fn: () => T,
  mapError: (cause: unknown) => E = (c) => toErrorObject(c) as unknown as E,
): Result<T, E> {
  try {
    return ok(fn());
  } catch (cause) {
    return err(mapError(cause));
  }
}

// Collect results; fails with all errors if any failed.
export function all<T, E>(results: Result<T, E>[]): Result<T[], E[]> {
  const values: T[] = [];
  const errors: E[] = [];
  for (const r of results) r.ok ? values.push(r.value) : errors.push(r.error);
  return errors.length ? err(errors) : ok(values);
}
```

## The union error type

```ts
export type CreateUserError =
  | { code: "VALIDATION_FAILED"; details: FieldError[] }
  | { code: "EMAIL_TAKEN"; email: string }
  | { code: "DB_UNAVAILABLE"; cause: unknown };

export interface FieldError { field: string; code: string; message: string }
```

Note `E` is a **closed union**, so callers can `switch (result.error.code)` exhaustively.

## End-to-end example — create a user

```ts
import { ok, err, Result, map } from "./result";

export function validate(dto: unknown): Result<CreateUserDTO, CreateUserError> {
  const problems: FieldError[] = [];
  const { email, name } = (dto ?? {}) as Record<string, unknown>;
  if (typeof email !== "string" || !email.includes("@")) {
    problems.push({ field: "email", code: "INVALID_FORMAT", message: "Enter a valid email" });
  }
  if (typeof name !== "string" || !name.trim()) {
    problems.push({ field: "name", code: "REQUIRED", message: "name is required" });
  }
  return problems.length
    ? err({ code: "VALIDATION_FAILED", details: problems })
    : ok({ email: email as string, name: name as string });
}

export async function createUser(
  repo: UserRepository,
  dto: unknown,
): Promise<Result<User, CreateUserError>> {
  const validated = validate(dto);
  if (!validated.ok) return validated;

  const existing = await repo.findByEmail(validated.value.email);
  if (!existing.ok) return err({ code: "DB_UNAVAILABLE", cause: existing.error });
  if (existing.value) {
    return err({ code: "EMAIL_TAKEN", email: validated.value.email });
  }

  const created = await repo.create(validated.value);
  if (!created.ok) return err({ code: "DB_UNAVAILABLE", cause: created.error });
  return ok(created.value);
}
```

## The caller — exhaustive handling

```ts
import { match, assertNever } from "./result";

function toResponse(result: Result<User, CreateUserError>): Response {
  if (result.ok) return json(201, { id: result.value.id });

  switch (result.error.code) {
    case "VALIDATION_FAILED":
      return problemResponse(422, "VALIDATION_FAILED", result.error.details);
    case "EMAIL_TAKEN":
      return problemResponse(409, "USER_EMAIL_TAKEN", { email: result.error.email });
    case "DB_UNAVAILABLE":
      throw result.error.cause;                 // unexpected → boundary/global handler
    default:
      return assertNever(result.error);         // compile error if a case is missed
  }
}
```

Expected failures become a `4xx`; the one genuinely unexpected outcome is escalated to the boundary.
No expected condition is hidden in a catch block.

## Using `match` for value-producing handlers

```ts
const message = match(
  await createUser(repo, body),
  (user) => `Created user ${user.id}`,
  (e) => {
    switch (e.code) {
      case "VALIDATION_FAILED": return `Fix ${e.details.length} field(s)`;
      case "EMAIL_TAKEN":       return `Email ${e.email} already registered`;
      case "DB_UNAVAILABLE":    return "Temporary problem, please retry";
      default: return assertNever(e);
    }
  },
);
```

## Testing results is trivial

```ts
import { describe, it, expect } from "vitest";

it("rejects a malformed email", () => {
  const r = validate({ email: "nope", name: "Ada" });
  expect(r.ok).toBe(false);
  if (!r.ok && r.error.code === "VALIDATION_FAILED") {
    expect(r.error.details).toContainEqual(
      expect.objectContaining({ field: "email", code: "INVALID_FORMAT" }),
    );
  }
});
```

Because failure is a value, tests assert on returned data instead of `expect(() => ...).toThrow()`.

## Key data / numbers

- **Combinator count:** `map`, `mapErr`, `flatMap`, `unwrapOr`, `match` cover ~95% of call sites.
- **`Promise.allSettled`** is the standard for partial success; `all()` here is all-or-nothing.
- **`E` as a closed union** enables `assertNever` and exhaustive `switch`.
- Keep the `Result` **inside the domain/application**; convert to HTTP/exception at the boundary.
- **Runtime validation** still required when data crosses a process boundary.

## Real-world use case — Acme SaaS

Acme's user-creation flow had three failure modes that all surfaced as a generic `500` because they
were thrown and caught in one handler. Migrating to `Result<User, CreateUserError>` made the union
explicit: validation returned `422`, `EMAIL_TAKEN` returned `409`, and only `DB_UNAVAILABLE` was
escalated. Support tickets for "couldn't create user" became self-diagnosing, and a new
`DOMAIN_BLOCKED` variant forced every caller to handle it at compile time. The implementation is
under 120 lines with no dependencies.

## Trade-offs

| Choice | Pros | Cons |
| ------ | ---- | ---- |
| Hand-rolled `Result` | No deps, tailored, readable | You own combinator bugs |
| Library (`neverthrow`, `fp-ts`) | Battle-tested, rich | Learning curve, bundle size |
| Exceptions only | Familiar, concise | No exhaustiveness for expected failures |
| `Result` everywhere | Uniform | Noise for truly unexpected failures |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Type `E` as a closed union | `Result<T, string>` |
| Wrap async edges with `tryCatchAsync` | Let rejections bypass `Result` |
| Use `assertNever` in callers | Silent `default` returning a generic error |
| Keep `Result` at domain/application layers | Thread it through infrastructure adapters |
| Test returned values directly | Test only via `toThrow` |

## Common mistakes

- **Forgotten async wrap** — a rejection escapes a `Promise<Result<...>>`.
- **`Partial` handling of the union** via a silent default.
- **`flatMap` with mismatched `E`** — losing the error type through composition.
- **Returning `Result` from the transport layer** instead of translating to a response.
- **Over-threading** `Result` through ten layers when only one boundary handles it.

## Checklist

- [ ] Is `E` a specific union, not `string`/`any`?
- [ ] Are `map`/`flatMap` used instead of nested checks?
- [ ] Is every async edge wrapped?
- [ ] Do callers handle all variants with `assertNever`?
- [ ] Is the exception/`Result` boundary explicit and singular?
- [ ] Are results unit-tested as values?

## Related

- [Result Types and Algebraic Data Types](../01-concepts/03-result-types-and-adts.md)
- [Exception vs Result Control Flow](../01-concepts/04-exception-vs-result-control-flow.md)
- [Custom Error Class Design in Practice](./02-custom-error-class-design.md)
