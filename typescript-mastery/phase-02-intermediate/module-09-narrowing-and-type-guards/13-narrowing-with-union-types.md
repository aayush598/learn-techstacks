# Narrowing with union types

> Phase 2 · Module 09 · Type Narrowing and Type Guards

**TL;DR** — Narrowing a union removes members that fail a runtime check, leaving only the compatible ones.

## Syntax
```ts
type Value = string | number | boolean;
```

## Examples
### Basic
```ts
type Value = string | number | boolean;

function toText(value: Value): string {
  if (typeof value === "string") {
    return value; // ✅ string
  }
  if (typeof value === "number") {
    return value.toString(); // ✅ number
  }
  return value ? "true" : "false"; // ✅ boolean
}
```

### Practical
```ts
type Shape =
  | { kind: "circle"; radius: number }
  | { kind: "rect"; width: number; height: number }
  | { kind: "triangle"; base: number; height: number };

function area(shape: Shape): number {
  switch (shape.kind) {
    case "circle":
      return Math.PI * shape.radius ** 2;
    case "rect":
      return shape.width * shape.height;
    case "triangle":
      return (shape.base * shape.height) / 2;
  }
}
```

### Advanced / edge cases
```ts
type Result<T> =
  | { status: "ok"; value: T }
  | { status: "err"; error: Error };

function map<T, U>(result: Result<T>, fn: (value: T) => U): Result<U> {
  if (result.status === "err") {
    return result; // ✅ err passes through
  }
  return { status: "ok", value: fn(result.value) }; // ✅ ok
}

function coalesce(value: string | number | null | undefined): string | number {
  if (value == null) {
    return "none"; // ✅ null | undefined removed
  }
  return value; // ✅ string | number
}
```

## Key points
- Guards remove union members one branch at a time.
- After all members are handled, the remainder is `never`.
- Narrowing respects nested unions and generics.
- `switch` on a discriminant is the most readable approach.
- Unions of object shapes narrow best with a shared literal key.

## Gotchas
- A union of structurally identical members cannot be narrowed.
- Overlapping optional properties may leave a member unreachable.
- `// ❌ Error:` `shape.radius` before checking `shape.kind`.

## Best practice
- Keep unions small and discriminated.
- Let the compiler find unhandled members via `never`.
