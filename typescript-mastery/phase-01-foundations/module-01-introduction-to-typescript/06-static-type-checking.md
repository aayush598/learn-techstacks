# Static Type Checking

> Phase 1 · Module 01 · Introduction to TypeScript

**TL;DR** — Static type checking analyzes source code and rejects incompatible values before the program runs.

## Syntax

```ts
const count: number = 3;
```

## Examples

### Basic

```ts
let count: number = 0;
// ❌ Error: Type 'string' is not assignable to type 'number'. (TS2322)
count = "three";
```

### Practical

```ts
type Shape =
  | { kind: "circle"; radius: number }
  | { kind: "square"; side: number };

function area(shape: Shape): number {
  return shape.kind === "circle"
    ? Math.PI * shape.radius ** 2
    : shape.side ** 2;
}

console.log(area({ kind: "square", side: 3 })); // => 9
```

### Advanced / edge cases

```ts
// Static checks cannot see runtime data, so narrow `unknown` explicitly.
function isString(value: unknown): value is string {
  return typeof value === "string";
}

function printLength(value: unknown): void {
  if (isString(value)) {
    console.log(value.length); // ✅ narrowed to string
  }
}
```

## Key points

- Checks are performed on the source program without executing it.
- The checker verifies assignments, calls, property access, and return types.
- Narrowing refines a broad type based on runtime checks the compiler can prove.
- Static analysis works best when external data enters through `unknown` and is validated.
- The same checker powers both `tsc` and editor feedback.

## Gotchas

- Static types do not validate JSON, HTTP responses, environment variables, or form input.
- Type assertions (`as`) can silence the checker without making the value safe.
- The system is not fully sound; some invalid runtime states remain representable.

## Best practice

- Validate external data once, then rely on static types inside the application.
- Prefer `unknown` over `any` when the runtime shape is not yet known.
