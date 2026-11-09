# Array Types

> Phase 1 · Module 03 · Basic Types

**TL;DR** — Arrays are typed as `T[]` or `Array<T>`, and every element must be a `T`.

## Syntax
```ts
let nums: number[] = [1, 2, 3];
let names: Array<string> = ["Ada", "Grace"];
let grid: number[][] = [[1, 2], [3, 4]];
```

## Examples
### Basic
```ts
const scores: number[] = [90, 85, 77];
scores.push(100); // ✅

const tags: Array<string> = ["ts", "js"];
console.log(scores.length, tags[0]); // ✅
```

### Practical
```ts
type User = { id: number; name: string };

const users: User[] = [
  { id: 1, name: "Ada" },
  { id: 2, name: "Grace" },
];

const names: string[] = users.map((u) => u.name);
const active: User[] = users.filter((u) => u.id > 1);

console.log(names, active); // ✅
```

### Advanced / edge cases
```ts
// Readonly element access can still be undefined under noUncheckedIndexedAccess
const values: number[] = [1, 2, 3];
const first = values[0]; // number (or number | undefined with the flag)

// Union element types
const mixed: (string | number)[] = [1, "two", 3]; // ✅

// Arrays are covariant in practice
const animals: string[] = ["cat"];
const things: (string | number)[] = animals; // ✅
things.push(42); // ⚠️ mutates the original through the wider view

console.log(first, mixed, things);
```

## Key points
- `T[]` and `Array<T>` are equivalent.
- `T[][]` is an array of arrays, not a matrix type.
- `push`, `map`, and `filter` preserve or transform element types.
- Array literals infer a union of element types.
- Indexing yields `T` (or `T | undefined` with `noUncheckedIndexedAccess`).

## Gotchas
- Mixed literals widen to a union, not `any`.
  ```ts
  const xs = [1, "two"]; // (string | number)[]
  ```
- Mutating through a wider alias is allowed but unsafe.
  ```ts
  const nums: number[] = [1];
  const wide: (number | string)[] = nums;
  wide.push("oops"); // ✅ compiles, ❌ breaks nums' invariant
  ```
- `new Array(3)` creates holes, not typed elements.
  ```ts
  const holes = new Array(3); // any[]
  ```

## Best practice
- Prefer `T[]` for readability; use `Array<T>` when `T` is complex.
- Enable `noUncheckedIndexedAccess` for safer indexing.
