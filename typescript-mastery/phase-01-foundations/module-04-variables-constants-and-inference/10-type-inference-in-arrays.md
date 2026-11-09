# Type Inference in Arrays

> Phase 1 · Module 04 · Variables, Constants, and Type Inference

**TL;DR** — Array literals infer one element type from all their elements, usually the best common type.

## Syntax
```ts
const numbers = [1, 2, 3];        // number[]
const typed: number[] = [];       // explicit element type
const pair = [1, "one"] as const; // readonly [1, "one"]
```

## Examples
### Basic
```ts
const nums = [1, 2, 3];      // number[]
const names = ["a", "b"];    // string[]

const empty = [];            // never[]
// empty.push(1);            // ❌ Error: Argument of type 'number' is not assignable to parameter of type 'never'.

const typed: number[] = [];  // number[]
typed.push(1);               // ✅
```

### Practical
```ts
const ids = [1, 2, 3];
const doubled = ids.map((id) => id * 2); // number[]

const users = [
  { id: 1, name: "ada" },
  { id: 2, name: "alan" },
]; // { id: number; name: string }[]

const names = users.map((u) => u.name); // string[]

console.log(doubled, names);
```

### Advanced / edge cases
```ts
const mixed = [1, "two", true]; // (string | number | boolean)[]

const matrix = [
  [1, 2],
  [3, 4],
]; // number[][]

const jagged = [
  [1, 2],
  ["a"],
]; // (string[] | number[])[]

const pair = [1, "one"] as const; // readonly [1, "one"]

const tuple: [number, string] = [1, "one"]; // tuple, not array

// Spread preserves the element type
const base = [1, 2, 3];
const more = [...base, 4]; // number[]

console.log(mixed, matrix, jagged, pair, tuple, more);
```

## Key points
- Elements are widened, then combined into a best common type.
- Empty arrays infer `never[]` until given an annotation.
- Nested arrays infer nested element types, not tuples.
- `as const` turns an array literal into a readonly tuple.
- Spreads and `map` propagate the source element type.

## Gotchas
- `const xs = [1, 2]; xs.push(3); // ✅` — arrays stay mutable.
- Mixed arrays become unions, which can hide type errors.
- Destructuring an inferred array yields `T | undefined` without `noUncheckedIndexedAccess` caveats.

## Best practice
- Annotate empty arrays before pushing into them.
- Use tuples or `as const` when position and literal types matter.
