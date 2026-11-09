# Optional Tuple Elements

> Phase 1 · Module 03 · Basic Types

**TL;DR** — A trailing `?` makes a tuple element optional, so it may be omitted but never reordered.

## Syntax
```ts
let entry: [string, number?] = ["count"];
let full: [string, number?] = ["count", 10];
```

## Examples
### Basic
```ts
const a: [string, number?] = ["total"];
const b: [string, number?] = ["total", 5];

console.log(a.length, b.length); // 1 2 ✅
```

### Practical
```ts
type Range = [min: number, max?: number];

function inRange(value: number, [min, max]: Range): boolean {
  return value >= min && (max === undefined || value <= max);
}

console.log(inRange(5, [0, 10])); // true ✅
console.log(inRange(50, [0]));    // true ✅
```

### Advanced / edge cases
```ts
// Optional elements must come after required ones
const ok: [number, string?] = [1]; // ✅
// ❌ Error: A required element cannot follow an optional element.
// const bad: [number?, string] = [1, "x"];

// Accessing an optional element yields T | undefined
const tuple: [string, number?] = ["a"];
const maybe = tuple[1]; // number | undefined
console.log(maybe ?? 0); // ✅

// Optional elements and unions interact with length checks
const short: [boolean, ...string[]] = [true]; // ✅
console.log(ok, tuple, short);
```

## Key points
- `?` marks an element optional; it must be trailing.
- Optional elements are typed `T | undefined` on access.
- Length becomes a union of allowed sizes.
- Destructuring an optional element yields `T | undefined`.
- They model "required + maybe more" records.

## Gotchas
- Required elements cannot follow optional ones.
  ```ts
  // ❌ Error: A required element cannot follow an optional element.
  // type Bad = [number?, string];
  ```
- Optional does not mean "may be `null`".
  ```ts
  const t: [number?] = [null]; // ❌ null is not undefined
  ```
- Tuple length checks may reject spreads of uncertain length.

## Best practice
- Keep optional tuple elements last.
- Prefer named optional fields in objects when order is not meaningful.
