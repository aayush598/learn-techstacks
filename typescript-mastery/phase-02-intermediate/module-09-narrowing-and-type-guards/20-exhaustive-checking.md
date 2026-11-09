# Exhaustive checking

> Phase 2 · Module 09 · Type Narrowing and Type Guards

**TL;DR** — Exhaustive checking uses `never` to prove every union member is handled, catching new cases at compile time.

## Syntax
```ts
function assertNever(value: never): never {
  throw new Error(`Unhandled: ${String(value)}`);
}
```

## Examples
### Basic
```ts
type Status = "idle" | "loading" | "done";

function label(status: Status): string {
  switch (status) {
    case "idle":
      return "Idle";
    case "loading":
      return "Loading";
    case "done":
      return "Done";
    default:
      return assertNever(status); // ✅ status is never
  }
}

function assertNever(value: never): never {
  throw new Error(`Unhandled case: ${String(value)}`);
}
```

### Practical
```ts
type Shape =
  | { kind: "circle"; radius: number }
  | { kind: "square"; side: number };

function area(shape: Shape): number {
  switch (shape.kind) {
    case "circle":
      return Math.PI * shape.radius ** 2;
    case "square":
      return shape.side ** 2;
    default: {
      const exhaustive: never = shape; // ✅ all members handled
      return exhaustive;
    }
  }
}
```

### Advanced / edge cases
```ts
type Result<T> =
  | { status: "ok"; value: T }
  | { status: "error"; error: Error }
  | { status: "pending" };

function unwrap<T>(result: Result<T>): T {
  switch (result.status) {
    case "ok":
      return result.value;
    case "error":
      throw result.error;
    case "pending":
      throw new Error("Still pending");
    default:
      return assertNever(result); // ✅ compiler fails if a status is added
  }
}

function assertNever(value: never): never {
  throw new Error(`Unexpected value: ${JSON.stringify(value)}`);
}
```

## Key points
- `never` is the type left when all union members are removed.
- Assigning to `never` produces a compile error for unhandled members.
- Works with `switch`, `if`/`else`, and `assertNever`.
- Adding a union member forces you to update handlers.
- Runtime `assertNever` also guards against bad external data.

## Gotchas
- A `default` that throws a generic error does not give compile-time safety.
- Casting to `never` defeats the check.
- `// ❌ Error:` `const x: never = status;` when `status` still has reachable members.

## Best practice
- End every discriminated union handler with `assertNever`.
- Avoid a bare `default: return ...` that hides new cases.
