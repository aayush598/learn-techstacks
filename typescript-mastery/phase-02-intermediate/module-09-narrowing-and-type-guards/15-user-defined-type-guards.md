# User-defined type guards

> Phase 2 · Module 09 · Type Narrowing and Type Guards

**TL;DR** — A user-defined type guard is a function returning `value is T` that teaches the compiler a custom narrowing rule.

## Syntax
```ts
function isString(value: unknown): value is string {
  return typeof value === "string";
}
```

## Examples
### Basic
```ts
function isString(value: unknown): value is string {
  return typeof value === "string";
}

function upper(value: unknown): string {
  if (isString(value)) {
    return value.toUpperCase(); // ✅ string
  }
  return "";
}
```

### Practical
```ts
type User = { id: string; name: string };

function isUser(value: unknown): value is User {
  if (typeof value !== "object" || value === null) {
    return false;
  }
  const candidate = value as Record<string, unknown>;
  return typeof candidate.id === "string" && typeof candidate.name === "string";
}

function renderUser(value: unknown): string {
  if (isUser(value)) {
    return `${value.id}: ${value.name}`; // ✅ User
  }
  return "invalid user";
}
```

### Advanced / edge cases
```ts
type NonEmptyArray<T> = [T, ...T[]];

function isNonEmpty<T>(value: T[]): value is NonEmptyArray<T> {
  return value.length > 0;
}

function head<T>(value: T[]): T | undefined {
  if (isNonEmpty(value)) {
    return value[0]; // ✅ T, not T | undefined
  }
  return undefined;
}

function isNotNull<T>(value: T | null | undefined): value is T {
  return value !== null && value !== undefined;
}

const values: (string | null)[] = ["a", null, "b"];
const clean = values.filter(isNotNull); // ✅ string[]
```

## Key points
- The return type `value is T` is a type predicate.
- The implementation must return a boolean; the compiler trusts the predicate.
- Guards can be generic and can narrow to derived types.
- `filter(guard)` narrows array element types.
- Guards are the safest alternative to `as` casts.

## Gotchas
- The compiler does not verify the predicate logic; a wrong guard lies.
- A guard cannot narrow to a type unrelated to its parameter.
- `// ❌ Error:` `function isString(value: unknown): value is number` — predicate must be assignable to the parameter type.

## Best practice
- Name guards `isX` and keep them pure.
- Unit-test guards, since they are unchecked assertions to the compiler.
