# Control-flow analysis

> Phase 2 · Module 09 · Type Narrowing and Type Guards

**TL;DR** — TypeScript tracks the possible types of a variable along every reachable path through your code.

## Syntax
```ts
let value: string | number;

value = "hello";
value.toUpperCase(); // ✅ known to be string here

value = 42;
value.toFixed(); // ✅ known to be number here
```

## Examples
### Basic
```ts
function describe(value: string | number | boolean): string {
  if (typeof value === "boolean") {
    return value ? "yes" : "no"; // ✅ boolean
  }
  if (typeof value === "number") {
    return value.toFixed(0); // ✅ number
  }
  return value.trim(); // ✅ string
}
```

### Practical
```ts
function getLength(value: string | string[] | undefined): number {
  if (value === undefined) {
    return 0; // ✅ undefined eliminated
  }
  if (typeof value === "string") {
    return value.length; // ✅ string
  }
  return value.length; // ✅ string[]
}
```

### Advanced / edge cases
```ts
function assertNever(value: never): never {
  throw new Error(`Unexpected: ${String(value)}`);
}

function area(shape: { kind: "circle"; r: number } | { kind: "square"; s: number }) {
  switch (shape.kind) {
    case "circle":
      return Math.PI * shape.r ** 2;
    case "square":
      return shape.s ** 2;
    default:
      return assertNever(shape); // ✅ shape is never
  }
}
```

## Key points
- The compiler analyzes branches, loops, returns, and throws.
- Early returns refine types for all following statements.
- Unreachable code is detected through `never` narrowing.
- Analysis is flow-sensitive: order of statements matters.
- Narrowing resets when control re-enters an ambiguous point.

## Gotchas
- Code after an unconditional `throw`/`return` is unreachable.
- Closures may not preserve narrowing across calls.
- `let` reassignments can undo a previously narrowed type.

## Best practice
- Use early returns to keep narrowed code flat and readable.
- Add exhaustive `never` checks to catch new union members.
