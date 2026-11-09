# Building a Type-Safe Codebase

> Phase 2 · Module 10 · Type Assertions and Type Safety

**TL;DR** — Combine strict compiler settings, `unknown` at boundaries, validators, and disciplined assertion use to keep safety end to end.

## Syntax

```ts
const tsconfig = {
  compilerOptions: {
    strict: true,
    noUncheckedIndexedAccess: true,
    exactOptionalPropertyTypes: true,
    useUnknownInCatchVariables: true,
  },
} as const;
```

## Examples

### Basic

```ts
const tsconfig = {
  compilerOptions: {
    strict: true,
    noUncheckedIndexedAccess: true,
    exactOptionalPropertyTypes: true,
    noImplicitOverride: true,
  },
} as const;

type CompilerOptions = typeof tsconfig.compilerOptions;
const strict: true = tsconfig.compilerOptions.strict; // ✅
console.log(strict);
```

### Practical

```ts
type Result<T> =
  | { ok: true; value: T }
  | { ok: false; error: string };

type User = { id: number; name: string };

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === "object" && value !== null;
}

function parseUser(value: unknown): Result<User> {
  if (!isRecord(value)) return { ok: false, error: "not an object" };
  if (typeof value.id !== "number") return { ok: false, error: "invalid id" };
  if (typeof value.name !== "string") return { ok: false, error: "invalid name" };
  return { ok: true, value: { id: value.id, name: value.name } };
}

console.log(parseUser({ id: 1, name: "Ada" })); // { ok: true, value: { id: 1, name: "Ada" } }
```

### Advanced / edge cases

```ts
type User = { id: number; name: string };

function isUser(value: unknown): value is User {
  if (typeof value !== "object" || value === null) return false;
  const record = value as Record<string, unknown>;
  return typeof record.id === "number" && typeof record.name === "string";
}

async function loadUser(): Promise<User> {
  const response = await fetch("/api/user");
  if (!response.ok) throw new Error(`HTTP ${response.status}`);

  const payload: unknown = await response.json(); // boundary: unknown
  if (!isUser(payload)) throw new TypeError("Invalid user payload");

  return payload; // ✅ validated, no assertion needed
}

loadUser().then((user) => console.log(user.name));
```

## Key points

- Turn on `strict` first, then add `noUncheckedIndexedAccess` and `exactOptionalPropertyTypes`.
- Treat every external value as `unknown` and validate before use.
- Prefer guards, generics, and `satisfies` over assertions and `any`.
- Confine unavoidable casts to small, documented adapter functions.
- Normalize `catch` values and return `Result` for fallible operations.

## Gotchas

- `noUncheckedIndexedAccess` turns `items[0]` into `T | undefined`; assertions do not make it present.
- `as` written to satisfy the compiler can silently drift when types change.
- One `any` from an untyped dependency can untype large parts of the codebase.

```ts
declare function legacy(): any;
const id: number = legacy(); // ✅ compiles, no guarantee
console.log(id.toFixed()); // may throw at runtime
```

## Best practice

- Add lint rules that ban `any` and require justification for assertions.
- Review boundary modules first: they determine whether the rest of the codebase is trustworthy.
