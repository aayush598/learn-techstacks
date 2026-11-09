# Type Inference in Callbacks

> Phase 1 · Module 04 · Variables, Constants, and Type Inference

**TL;DR** — Callback parameters are inferred from the expected function type supplied by the surrounding call.

## Syntax
```ts
[1, 2, 3].map((n) => n * 2);            // n inferred from array
const handler = (e: { type: string }) => e.type; // explicit parameter
[1, 2].forEach((n) => console.log(n));  // n inferred from array
```

## Examples
### Basic
```ts
const nums = [1, 2, 3];

const doubled = nums.map((n) => n * 2); // n: number
const evens = nums.filter((n) => n % 2 === 0); // n: number

const total = nums.reduce((sum, n) => sum + n, 0); // sum, n: number
```

### Practical
```ts
const users = [
  { id: 1, name: "ada" },
  { id: 2, name: "alan" },
];

const names = users.map((u) => u.name.toUpperCase()); // u inferred
const found = users.find((u) => u.id === 2); // { id: number; name: string } | undefined

const button = {
  addEventListener(_event: string, handler: (e: { target: unknown }) => void): void {
    handler({ target: null });
  },
};

button.addEventListener("click", (e) => {
  console.log(e.target); // ✅ e inferred
});

console.log(names, found);
```

### Advanced / edge cases
```ts
type Comparator = (a: number, b: number) => number;

function sort(values: number[], compare: Comparator): number[] {
  return [...values].sort(compare);
}

const sorted = sort([3, 1, 2], (a, b) => a - b); // a, b inferred as number

// Extracted callbacks lose context
// const loose = (e) => console.log(e); // ❌ Error: Parameter 'e' implicitly has an 'any' type.

const typed = (e: { target: unknown }): void => console.log(e.target);

// Generic callbacks infer from the call
function mapAll<T, U>(items: T[], fn: (item: T) => U): U[] {
  return items.map(fn);
}

const lengths = mapAll(["a", "bb"], (s) => s.length); // s: string

console.log(sorted, typed, lengths);
```

## Key points
- Context flows from the function being called into the callback parameters.
- Array methods infer element types from the receiver.
- Generic callbacks infer type parameters from arguments.
- Return types of callbacks are inferred from their bodies.
- Context is lost when a callback is assigned to an unannotated variable first.

## Gotchas
- Unannotated standalone callbacks are implicit `any` under `noImplicitAny`.
- Overloaded callbacks may infer the last compatible signature.
- Excess parameters are allowed in callbacks but excess properties are not.

## Best practice
- Keep callbacks inline so they inherit context.
- Annotate callbacks when extracting them for reuse or testing.
