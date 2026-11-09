# Tuple Types

> Phase 1 · Module 03 · Basic Types

**TL;DR** — A tuple is a fixed-length array where each position has its own type.

## Syntax
```ts
let pair: [string, number] = ["age", 36];
let rgb: [number, number, number] = [255, 128, 0];
let empty: [] = [];
```

## Examples
### Basic
```ts
const entry: [string, number] = ["count", 10];
const [key, value] = entry;

console.log(key.toUpperCase(), value.toFixed(0)); // ✅
```

### Practical
```ts
type ApiResult = [ok: boolean, data: string];

function parseResponse(raw: string): ApiResult {
  try {
    return [true, JSON.parse(raw) as string];
  } catch {
    return [false, "invalid"];
  }
}

const [ok, data] = parseResponse('"hello"');
console.log(ok, data); // ✅
```

### Advanced / edge cases
```ts
// Tuples enforce length and position
const point: [number, number] = [1, 2]; // ✅
// ❌ Error: Source has 3 element(s) but target allows only 2.
// const bad: [number, number] = [1, 2, 3];

// Position types differ, so order matters
const pair: [string, number] = ["x", 1];
// ❌ Error: Type 'number' is not assignable to type 'string'.
// const swapped: [string, number] = [1, "x"];

// Tuples are arrays at runtime
console.log(Array.isArray(pair), pair.length); // true 2
```

## Key points
- Tuples encode both length and per-position types.
- Destructuring gives each element its exact type.
- Tuples are regular arrays at runtime.
- They are ideal for fixed records and multiple return values.
- Excess or missing elements are compile errors.

## Gotchas
- Order is part of the type.
  ```ts
  const t: [string, number] = ["a", 1];
  // ❌ Error: Type 'number' is not assignable to type 'string'.
  // t[0] = 2;
  ```
- `push` still works on mutable tuples and breaks the length guarantee.
  ```ts
  const t: [number, number] = [1, 2];
  t.push(3); // ✅ compiles! prefer readonly tuples
  ```
- Inferred literals become arrays, not tuples.
  ```ts
  const arr = [1, 2]; // number[], not [number, number]
  ```

## Best practice
- Use tuples for fixed, positional data; use objects for named fields.
- Prefer `as const` or readonly tuples when length must not change.
