# Equality narrowing

> Phase 2 · Module 09 · Type Narrowing and Type Guards

**TL;DR** — Comparing a value to a literal, `null`, or `undefined` narrows it by eliminating incompatible union members.

## Syntax
```ts
if (value === "admin") {
  // value is "admin" here
}
```

## Examples
### Basic
```ts
type Role = "admin" | "user" | "guest";

function permissions(role: Role): string[] {
  if (role === "admin") {
    return ["read", "write", "delete"]; // ✅ "admin"
  }
  if (role === "user") {
    return ["read", "write"]; // ✅ "user"
  }
  return ["read"]; // ✅ "guest"
}
```

### Practical
```ts
function normalize(value: string | null | undefined): string {
  if (value === null || value === undefined) {
    return ""; // ✅ null | undefined
  }
  return value.trim(); // ✅ string
}
```

### Advanced / edge cases
```ts
type Shape =
  | { kind: "circle"; radius: number }
  | { kind: "square"; side: number };

function area(shape: Shape): number {
  if (shape.kind === "circle") {
    return Math.PI * shape.radius ** 2; // ✅ circle
  }
  return shape.side ** 2; // ✅ square
}

function isNullish(value: unknown): value is null | undefined {
  return value === null || value === undefined;
}
```

## Key points
- `===` narrows to the exact literal or the matching member.
- `!==` excludes members, narrowing to the remainder.
- `== null` matches both `null` and `undefined`.
- Works with literal unions and object discriminants.
- Equality against `true`/`false` narrows booleans.

## Gotchas
- `==` performs coercion; prefer `===` except for the `== null` idiom.
- Equality does not deep-compare objects.
- `// ❌ Error:` `value === "pending"` when `value: "idle" | "done"` produces a type error.

## Best practice
- Use `===` for predictability, and `== null` for nullish checks.
- Combine equality narrowing with exhaustive `switch` statements.
