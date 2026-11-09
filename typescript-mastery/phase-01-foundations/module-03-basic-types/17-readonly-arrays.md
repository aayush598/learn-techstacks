# Readonly Arrays

> Phase 1 · Module 03 · Basic Types

**TL;DR** — `readonly T[]` forbids mutation at compile time, making functions that only read their input explicit.

## Syntax
```ts
let nums: readonly number[] = [1, 2, 3];
let names: ReadonlyArray<string> = ["Ada"];

function sum(values: readonly number[]): number {
  return values.reduce((a, b) => a + b, 0);
}
```

## Examples
### Basic
```ts
const nums: readonly number[] = [1, 2, 3];
console.log(nums[0], nums.length); // ✅ reads allowed

// ❌ Error: Property 'push' does not exist on type 'readonly number[]'.
// nums.push(4);
```

### Practical
```ts
type Point = { x: number; y: number };

function average(points: readonly Point[]): number {
  return points.reduce((sum, p) => sum + p.x, 0) / points.length;
}

const pts: Point[] = [{ x: 1, y: 2 }, { x: 3, y: 4 }];
console.log(average(pts)); // ✅ mutable array accepted
console.log(average([{ x: 5, y: 6 }])); // ✅
```

### Advanced / edge cases
```ts
// Mutable arrays are assignable to readonly, not vice versa
const mutable: number[] = [1, 2, 3];
const ro: readonly number[] = mutable; // ✅
// ❌ Error: The type 'readonly number[]' is 'readonly' and cannot be assigned to the mutable type 'number[]'.
// const back: number[] = ro;

// Readonly is shallow: element objects stay mutable
type User = { name: string };
const users: readonly User[] = [{ name: "Ada" }];
users[0].name = "Grace"; // ✅ element is not readonly

// Spread to get a mutable copy
const copy: number[] = [...ro];
copy.push(4); // ✅

console.log(users, copy);
```

## Key points
- `readonly T[]` and `ReadonlyArray<T>` are equivalent.
- All mutating methods (`push`, `pop`, `splice`) are removed.
- Mutable arrays are assignable to readonly ones, not the reverse.
- Readonly is shallow; nested objects remain mutable.
- Use it for function parameters you do not modify.

## Gotchas
- Assigning a readonly array to a mutable type fails.
  ```ts
  const ro: readonly number[] = [1];
  // ❌ Error: readonly cannot be assigned to mutable.
  // const m: number[] = ro;
  ```
- Readonly does not deep-freeze objects.
  ```ts
  const ro: readonly { n: number }[] = [{ n: 1 }];
  ro[0].n = 2; // ✅ allowed
  ```
- `sort` and `reverse` mutate, so they are unavailable.

## Best practice
- Type read-only parameters as `readonly T[]`.
- Copy with `[...arr]` before mutating a readonly input.
