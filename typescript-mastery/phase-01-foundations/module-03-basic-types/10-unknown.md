# unknown

> Phase 1 · Module 03 · Basic Types

**TL;DR** — `unknown` accepts any value but forces you to narrow before using it.

## Syntax
```ts
let value: unknown = 42;
value = "text"; // ✅
// value.toUpperCase(); // ❌ must narrow first

if (typeof value === "string") {
  value.toUpperCase(); // ✅
}
```

## Examples
### Basic
```ts
let input: unknown = "hello";

if (typeof input === "string") {
  console.log(input.toUpperCase()); // ✅ narrowed
}

input = 42;
if (typeof input === "number") {
  console.log(input.toFixed(2)); // ✅
}
```

### Practical
```ts
type User = { id: number; name: string };

function isUser(value: unknown): value is User {
  return (
    typeof value === "object" &&
    value !== null &&
    "id" in value &&
    "name" in value &&
    typeof (value as User).id === "number" &&
    typeof (value as User).name === "string"
  );
}

function handle(payload: unknown): string {
  if (isUser(payload)) {
    return `#${payload.id} ${payload.name}`;
  }
  return "invalid payload";
}

console.log(handle({ id: 1, name: "Ada" })); // ✅
```

### Advanced / edge cases
```ts
// unknown is the safe type for catch clauses (useUnknownInCatchVariables)
try {
  throw new Error("boom");
} catch (error: unknown) {
  if (error instanceof Error) {
    console.log(error.message); // ✅
  }
}

// Arrays of unknown require per-element narrowing
const items: unknown[] = [1, "two", true];
const strings = items.filter((x): x is string => typeof x === "string");
console.log(strings); // string[]
```

## Key points
- Every value is assignable to `unknown`.
- `unknown` is assignable only to `unknown` and `any`.
- You must narrow with `typeof`, `in`, `instanceof`, or a type guard.
- It is the safe counterpart to `any`.
- Ideal for untrusted input: JSON, API responses, `catch`.

## Gotchas
- You cannot call or index `unknown` directly.
  ```ts
  const x: unknown = {};
  // ❌ Error: Object is of type 'unknown'.
  // x.toString();
  ```
- A type assertion bypasses safety; validate instead.
  ```ts
  declare const x: unknown;
  const y = x as { id: number }; // ✅ compiles, may be wrong at runtime
  ```
- `unknown` propagates: operations need a narrowed type first.

## Best practice
- Type all untrusted input as `unknown` and narrow at the boundary.
- Write small `isX` type guards to reuse narrowing logic.
