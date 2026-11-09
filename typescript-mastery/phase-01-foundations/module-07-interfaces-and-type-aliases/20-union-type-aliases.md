# Union Type Aliases

> Phase 1 · Module 07 · Interfaces and Type Aliases

**TL;DR** — A union type alias says a value is one of several alternatives, and the compiler narrows to the correct one at runtime checks.

## Syntax
```ts
type Status = "idle" | "loading" | "success" | "error";
```

## Examples
### Basic
```ts
type Status = "idle" | "loading" | "success" | "error";

let status: Status = "idle"; // ✅
status = "loading"; // ✅

// ❌ Error: Type '"done"' is not assignable to type 'Status'
// status = "done";
```

### Practical
```ts
type Result<T> =
  | { ok: true; value: T }
  | { ok: false; error: string };

function divide(a: number, b: number): Result<number> {
  return b === 0
    ? { ok: false, error: "division by zero" }
    : { ok: true, value: a / b };
}

const result = divide(10, 2);
if (result.ok) {
  console.log(result.value); // ✅ narrowed to the success branch
} else {
  console.log(result.error); // ✅ narrowed to the failure branch
}
```

### Advanced / edge cases
```ts
type Shape =
  | { kind: "circle"; radius: number }
  | { kind: "square"; side: number }
  | { kind: "rectangle"; width: number; height: number };

function area(shape: Shape): number {
  switch (shape.kind) {
    case "circle":
      return Math.PI * shape.radius ** 2;
    case "square":
      return shape.side ** 2;
    case "rectangle":
      return shape.width * shape.height;
    default: {
      const exhaustive: never = shape;
      throw new Error(`Unhandled shape: ${JSON.stringify(exhaustive)}`);
    }
  }
}

console.log(area({ kind: "square", side: 3 })); // 9
```

## Key points
- A union means "one of these", not "all of these".
- Literal unions model finite state sets precisely.
- Discriminants (`kind`, `ok`, `type`) enable safe narrowing.
- Only members common to every alternative are accessible before narrowing.
- An exhaustive `never` check catches unhandled cases at compile time.

## Gotchas
- `// ❌ Error:` `console.log(shape.radius)` before checking `shape.kind`.
- A union of object types is not merged; you cannot read a member that only some branches have.
- `// ❌ Error:` assigning a widened `string` where a literal union is expected.

## Best practice
- Use discriminated unions for results, events, and state machines.
- Add an exhaustive `never` check in every switch over a union.
