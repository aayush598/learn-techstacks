# Runtime Validation versus Compile-Time Types

> Phase 2 · Module 10 · Type Assertions and Type Safety

**TL;DR** — Compile-time types describe code you control; runtime validation is required for data that enters at execution time.

## Syntax

```ts
type Result<T> = { ok: true; value: T } | { ok: false; error: string };
```

## Examples

### Basic

```ts
type User = { name: string };

const data: unknown = JSON.parse('{"name":42}');
const user = data as User;

console.log(user.name); // 42 — the type says string, reality says number
```

### Practical

```ts
type User = { name: string };

type Result<T> =
  | { ok: true; value: T }
  | { ok: false; error: string };

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === "object" && value !== null;
}

function validateUser(value: unknown): Result<User> {
  if (!isRecord(value)) return { ok: false, error: "not an object" };
  if (typeof value.name !== "string") return { ok: false, error: "invalid name" };
  return { ok: true, value: { name: value.name } };
}

console.log(validateUser({ name: "Ada" })); // { ok: true, value: { name: "Ada" } }
console.log(validateUser({ name: 42 })); // { ok: false, error: "invalid name" }
```

### Advanced / edge cases

```ts
type Parser<T> = (value: unknown) => T;

const parseString: Parser<string> = (value) => {
  if (typeof value !== "string") {
    throw new TypeError("Expected string");
  }
  return value;
};

const parseArray = <T>(parse: Parser<T>, value: unknown): T[] => {
  if (!Array.isArray(value)) throw new TypeError("Expected array");
  return value.map(parse);
};

console.log(parseArray(parseString, ["a", "b"])); // ["a", "b"]
```

## Key points

- Types are erased; they cannot inspect a value at runtime.
- Validation must be expressed with runtime checks (`typeof`, `in`, `Array.isArray`).
- Schemas (Zod, Valibot, io-ts) automate structural validation and type inference.
- Validation should run at every trust boundary: network, storage, env, messages.
- Return a `Result` or throw a typed error instead of asserting success.

## Gotchas

- `JSON.parse` returns `any`, so unchecked access compiles and fails late.
- TypeScript cannot validate generics at runtime without an explicit validator.
- A cast at the boundary makes every downstream `User` untrustworthy.

## Best practice

- Pair a compile-time type with a runtime validator that produces that type.
- Keep parsing and validation in one module so the contract is enforced centrally.
