# Assertion functions (`asserts`)

> Phase 2 · Module 09 · Type Narrowing and Type Guards

**TL;DR** — An assertion function with `asserts condition` throws when the condition is false and narrows the value afterwards.

## Syntax
```ts
function assert(condition: unknown, message: string): asserts condition {
  if (!condition) throw new Error(message);
}
```

## Examples
### Basic
```ts
function assertIsString(value: unknown): asserts value is string {
  if (typeof value !== "string") {
    throw new Error("Expected string");
  }
}

function upper(value: unknown): string {
  assertIsString(value);
  return value.toUpperCase(); // ✅ string after assertion
}
```

### Practical
```ts
function assertDefined<T>(value: T | null | undefined): asserts value is T {
  if (value === null || value === undefined) {
    throw new Error("Value is missing");
  }
}

function firstOrThrow<T>(items: T[]): T {
  const item = items[0];
  assertDefined(item);
  return item; // ✅ T
}
```

### Advanced / edge cases
```ts
type User = { id: string; name: string };

function assertUser(value: unknown): asserts value is User {
  if (
    typeof value !== "object" ||
    value === null ||
    typeof (value as Record<string, unknown>).id !== "string" ||
    typeof (value as Record<string, unknown>).name !== "string"
  ) {
    throw new TypeError("Invalid user");
  }
}

function handle(payload: unknown): string {
  assertUser(payload);
  return payload.name; // ✅ User
}

function assert(condition: unknown, message = "Assertion failed"): asserts condition {
  if (!condition) throw new Error(message);
}

function nonEmpty<T>(values: T[]): T[] {
  assert(values.length > 0, "Array must not be empty");
  return values;
}
```

## Key points
- `asserts value is T` narrows after the call in the same scope.
- `asserts condition` narrows based on the condition expression.
- The function must have an explicit return type annotation.
- Assertions throw instead of returning `false`.
- Works with arrow functions only via explicit annotation.

## Gotchas
- Assertion functions must be declared, not passed around as expressions.
- Narrowing is lost if the asserted variable is reassigned.
- `// ❌ Error:` `const assertString = (v: unknown) => { ... }` — an arrow without a type annotation cannot be an assertion signature.

## Best practice
- Use assertions at module boundaries to fail fast.
- Include descriptive messages for easier debugging.
