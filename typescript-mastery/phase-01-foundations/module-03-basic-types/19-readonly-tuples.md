# Readonly Tuples

> Phase 1 · Module 03 · Basic Types

**TL;DR** — A `readonly` tuple locks both length and positions, preventing `push`, reassignment, and mutation.

## Syntax
```ts
let pair: readonly [string, number] = ["age", 36];
let rgb: Readonly<[number, number, number]> = [255, 128, 0];
```

## Examples
### Basic
```ts
const entry: readonly [string, number] = ["count", 10];
const [key, value] = entry;
console.log(key, value); // ✅ reads allowed

// ❌ Error: Cannot assign to '0' because it is a read-only property.
// entry[0] = "total";
```

### Practical
```ts
type Range = readonly [min: number, max: number];

function clamp(value: number, [min, max]: Range): number {
  return Math.min(Math.max(value, min), max);
}

const bounds: Range = [0, 100];
console.log(clamp(150, bounds)); // 100 ✅
console.log(clamp(-5, [0, 100])); // 0 ✅
```

### Advanced / edge cases
```ts
// `as const` infers a readonly tuple automatically
const config = [8080, "localhost"] as const;
// readonly [8080, "localhost"]

// Mutable tuples assign to readonly ones, not the reverse
const mutable: [number, number] = [1, 2];
const ro: readonly [number, number] = mutable; // ✅
// ❌ Error: readonly cannot be assigned to mutable.
// const back: [number, number] = ro;

// Spread copies into a mutable tuple
const copy: [number, number] = [...mutable];
copy[0] = 9; // ✅

console.log(config, ro, copy);
```

## Key points
- `readonly [A, B]` prevents element assignment and mutation.
- `as const` produces readonly tuples from literals.
- Mutable tuples are assignable to readonly tuples.
- Destructuring still yields precise per-position types.
- Use them for constants and public fixed records.

## Gotchas
- Readonly tuples cannot be passed where mutable ones are required.
  ```ts
  const ro = [1, 2] as const;
  // ❌ Error: readonly [1, 2] is not assignable to number[].
  // const m: number[] = ro;
  ```
- `Readonly<[A, B]>` and `readonly [A, B]` are similar but prefer the shorthand.
- Readonly is shallow for object elements.
  ```ts
  const ro: readonly [{ n: number }] = [{ n: 1 }];
  ro[0].n = 2; // ✅ still mutable
  ```

## Best practice
- Use `as const` for literal tuples you pass around.
- Accept `readonly [A, B]` in functions that only read.
