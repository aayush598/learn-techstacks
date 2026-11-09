# Type Narrowing

> Phase 1 · Module 03 · Basic Types

**TL;DR** — Narrowing refines a broad type to a specific one inside a control-flow branch.

## Syntax
```ts
function f(value: string | number): string {
  if (typeof value === "string") {
    return value.toUpperCase(); // narrowed to string
  }
  return value.toFixed(2);       // narrowed to number
}
```

## Examples
### Basic
```ts
function describe(value: string | null): string {
  if (value === null) {
    return "nothing"; // narrowed to null
  }
  return value.toUpperCase(); // narrowed to string ✅
}

console.log(describe("hi"), describe(null));
```

### Practical
```ts
type Shape =
  | { kind: "circle"; radius: number }
  | { kind: "square"; side: number };

function area(shape: Shape): number {
  switch (shape.kind) {
    case "circle":
      return Math.PI * shape.radius ** 2; // ✅ narrowed
    case "square":
      return shape.side ** 2;             // ✅ narrowed
  }
}

console.log(area({ kind: "circle", radius: 1 })); // ✅
```

### Advanced / edge cases
```ts
// `in`, `instanceof`, and custom guards all narrow
function format(value: Date | string): string {
  if (value instanceof Date) {
    return value.toISOString(); // ✅ Date
  }
  return value; // ✅ string
}

function isStringArray(value: unknown): value is string[] {
  return Array.isArray(value) && value.every((v) => typeof v === "string");
}

function join(value: unknown): string {
  return isStringArray(value) ? value.join(",") : "n/a";
}

// Truthiness narrows out null and undefined
function len(value?: string): number {
  return value ? value.length : 0;
}

console.log(format(new Date(0)), join(["a", "b"]), len("abc"));
```

## Key points
- `typeof`, `===`, `in`, and `instanceof` narrow unions.
- Discriminated unions narrow via a shared literal field.
- Custom type guards (`value is T`) narrow across functions.
- Truthiness removes `null` and `undefined`.
- Narrowing is flow-sensitive and resets after reassignment.

## Gotchas
- `typeof null === "object"`, so guard explicitly.
  ```ts
  function f(x: object | null) {
    // ❌ Error: 'x' is possibly 'null'.
    // return x.toString();
  }
  ```
- Assertions do not narrow; they bypass checking.
  ```ts
  declare const value: unknown;
  const x = value as string; // ✅ compiles, no runtime guarantee
  ```
- Narrowing is lost after an intervening function call on mutable state.

## Best practice
- Prefer discriminated unions and type guards over assertions.
- Keep guards small and reusable; return `value is T`.
