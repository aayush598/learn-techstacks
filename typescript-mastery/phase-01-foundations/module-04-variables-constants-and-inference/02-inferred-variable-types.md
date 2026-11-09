# Inferred Variable Types

> Phase 1 · Module 04 · Variables, Constants, and Type Inference

**TL;DR** — When you omit the annotation, TypeScript derives the type from the initializer.

## Syntax
```ts
let count = 10;         // number
const label = "ready";  // "ready"
```

## Examples
### Basic
```ts
let count = 10;      // number
let title = "hello"; // string
let enabled = true;  // boolean

const pi = 3.14;     // 3.14
let copy = pi;       // number
```

### Practical
```ts
const user = { id: 1, name: "ada" }; // { id: number; name: string }
let ids = [1, 2, 3];                 // number[]

function greet(name: string): string {
  const greeting = `Hello, ${name}`; // string
  return greeting;
}

console.log(greet(user.name), ids.length);
```

### Advanced / edge cases
```ts
const config = {
  retries: 3,
  endpoint: "https://api.example.com",
}; // { retries: number; endpoint: string }

let tuple = [1, "a"] as const; // readonly [1, "a"]

type Config = typeof config;

const double = (x: number) => x * 2; // (x: number) => number

const pair: Config = config; // ✅ structurally identical
console.log(tuple, double(pair.retries));
```

## Key points
- Inference uses the initializer's type at the declaration site.
- `const` preserves literal types; `let` widens them.
- Objects and arrays infer their members from the values present.
- `typeof` recovers an inferred type for reuse.
- Function expressions infer parameter types only from context, not from bodies.

## Gotchas
- `let x = null;` and `let x = undefined;` infer `any` under `strict` — annotate instead.
- An empty array infers `never[]`: `let list = []; // never[]`.
- Inference is a snapshot; later assignments must fit the inferred type.

## Best practice
- Prefer inference for locals with obvious initializers.
- Add annotations when the initializer is empty, `null`, or ambiguous.
