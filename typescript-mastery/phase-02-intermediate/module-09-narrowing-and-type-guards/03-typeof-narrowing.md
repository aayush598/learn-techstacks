# `typeof` narrowing

> Phase 2 · Module 09 · Type Narrowing and Type Guards

**TL;DR** — `typeof` checks narrow primitive unions to the exact runtime type they describe.

## Syntax
```ts
if (typeof value === "string") {
  // value is string here
}
```

## Examples
### Basic
```ts
function stringify(value: string | number | boolean): string {
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
type Primitive = string | number | bigint | boolean | symbol | null | undefined;

function isPrimitive(value: unknown): value is Primitive {
  return (
    value === null ||
    value === undefined ||
    ["string", "number", "bigint", "boolean", "symbol"].includes(typeof value)
  );
}
```

### Advanced / edge cases
```ts
function pad(value: string | number, width: number): string {
  if (typeof value === "number") {
    return value.toFixed(2).padStart(width, "0"); // ✅ number
  }
  return value.padStart(width, " "); // ✅ string
}

function isFunction(value: unknown): value is (...args: unknown[]) => unknown {
  return typeof value === "function"; // ✅ functions are object-typed but typeof detects them
}
```

## Key points
- `typeof` returns one of: `"string"`, `"number"`, `"bigint"`, `"boolean"`, `"symbol"`, `"undefined"`, `"object"`, `"function"`.
- It narrows primitives well and `null` is reported as `"object"`.
- `typeof x === "object"` does not exclude `null`; check `null` first.
- Arrays and plain objects both report `"object"`.
- Works with `unknown` and unions containing primitives.

## Gotchas
- `typeof null === "object"` — a classic trap.
- `typeof []` is `"object"`, not `"array"`; use `Array.isArray`.
- `// ❌ Error:` `typeof value === "number"` does not narrow `number | string` inside a nested function.

## Best practice
- Order checks so `null`/`undefined` are handled before `"object"`.
- Prefer `Array.isArray` for arrays instead of `typeof`.
