# Assertion Functions

> Phase 1 · Module 05 · Functions

**TL;DR** — An assertion function returns `asserts condition` (or `asserts x is T`) to narrow types after it is called.

## Syntax
```ts
function assert(condition: unknown): asserts condition { /* ... */ }
function assertIs(value: unknown): asserts value is Type { /* ... */ }
```

## Examples
### Basic
```ts
function assert(condition: unknown, message = "assertion failed"): asserts condition {
  if (!condition) throw new Error(message);
}

function head<T>(items: T[]): T {
  assert(items.length > 0, "empty array");
  return items[0];
}

console.log(head([1, 2])); // 1
```

### Practical
```ts
function assertIsString(value: unknown): asserts value is string {
  if (typeof value !== "string") throw new TypeError("expected string");
}

function shout(value: unknown): string {
  assertIsString(value);
  // ✅ value narrowed to string after the assertion
  return value.toUpperCase();
}

console.log(shout("hi")); // "HI"
```

### Advanced / edge cases
```ts
// Assertion predicates can be generic
function assertDefined<T>(value: T): asserts value is NonNullable<T> {
  if (value === null || value === undefined) throw new Error("not defined");
}

// ✅ assertion functions must be explicitly annotated
const assertNumber: (v: unknown) => asserts v is number = (v) => {
  if (typeof v !== "number") throw new TypeError("not a number");
};
```

## Key points
- `asserts condition` tells the compiler the condition holds after the call.
- `asserts x is T` narrows `x` for the rest of the scope.
- Assertion functions must have an explicit return type annotation.
- They throw (or never return) when the assertion fails.

## Gotchas
- `// ❌ Error:` assertion functions require every name in the call target to have an explicit type annotation.
- Returning normally without throwing breaks the contract at runtime.
- Assertion signatures are not allowed on arrow functions unless the variable is annotated.

## Best practice
- Keep assertion functions tiny and always throw on failure.
- Use a shared `assert` helper instead of hand-written checks everywhere.
