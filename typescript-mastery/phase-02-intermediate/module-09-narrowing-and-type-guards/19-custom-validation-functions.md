# Custom validation functions

> Phase 2 · Module 09 · Type Narrowing and Type Guards

**TL;DR** — Custom validators combine runtime checks with type predicates to turn untrusted data into typed values.

## Syntax
```ts
function validate(value: unknown): value is Model {
  return check(value);
}
```

## Examples
### Basic
```ts
type Point = { x: number; y: number };

function isPoint(value: unknown): value is Point {
  if (typeof value !== "object" || value === null) return false;
  const point = value as Record<string, unknown>;
  return typeof point.x === "number" && typeof point.y === "number";
}
```

### Practical
```ts
type User = {
  id: string;
  email: string;
  roles: ("admin" | "user")[];
};

function isUser(value: unknown): value is User {
  if (typeof value !== "object" || value === null) return false;
  const user = value as Record<string, unknown>;
  return (
    typeof user.id === "string" &&
    typeof user.email === "string" &&
    Array.isArray(user.roles) &&
    user.roles.every((role) => role === "admin" || role === "user")
  );
}

function parseUsers(input: unknown): User[] {
  if (!Array.isArray(input)) {
    throw new Error("Expected an array");
  }
  return input.filter(isUser); // ✅ User[]
}
```

### Advanced / edge cases
```ts
type Validator<T> = (value: unknown) => value is T;

function optional<T>(validate: Validator<T>): Validator<T | undefined> {
  return (value): value is T | undefined =>
    value === undefined || validate(value);
}

function arrayOf<T>(validate: Validator<T>): Validator<T[]> {
  return (value): value is T[] =>
    Array.isArray(value) && value.every(validate);
}

const isNumber = (value: unknown): value is number => typeof value === "number";
const isNumberArray = arrayOf(isNumber); // ✅ Validator<number[]>

const result: unknown = [1, 2, 3];
if (isNumberArray(result)) {
  result.map((n) => n * 2); // ✅ number[]
}
```

## Key points
- Validators return predicates, not throw, for composability.
- Combine small validators into larger ones.
- Always handle `null` and non-objects first.
- `Array.isArray` narrows to `unknown[]` before element checks.
- Validation at boundaries keeps internal code fully typed.

## Gotchas
- `typeof value === "object"` alone lets `null` through.
- Validators that mutate input are unsafe for reuse.
- `// ❌ Error:` `user.roles.every(...)` when `user.roles` is still `unknown`.

## Best practice
- Validate once at the edge; trust types inside.
- Compose generic validators instead of duplicating checks.
