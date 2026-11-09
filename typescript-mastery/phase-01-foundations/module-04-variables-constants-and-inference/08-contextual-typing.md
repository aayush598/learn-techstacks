# Contextual Typing

> Phase 1 · Module 04 · Variables, Constants, and Type Inference

**TL;DR** — Contextual typing infers a value's type from the position where it is used rather than from the value itself.

## Syntax
```ts
const handler: (e: Event) => void = (e) => { /* e inferred */ };
const items: string[] = ["a", "b"].map((x) => x.toUpperCase());
```

## Examples
### Basic
```ts
const label: string = "hello"; // context supplies string

const numbers = [1, 2, 3].map((n) => n * 2); // n: number

const handler: (value: number) => string = (value) => `${value}`;
```

### Practical
```ts
type Point = { x: number; y: number };

const points: Point[] = [
  { x: 0, y: 0 },
  { x: 1, y: 2 },
]; // object literals checked against Point

const startPoint: Point = { x: 0, y: 0 };

const printAll = (items: readonly string[]): void => {
  items.forEach((item) => console.log(item.toUpperCase())); // item: string
};

printAll(["a", "b"]);
console.log(points, startPoint);
```

### Advanced / edge cases
```ts
type Handler = (event: { type: string }) => void;

const onClick: Handler = (event) => {
  console.log(event.type); // ✅ event contextually typed
};

// Without context, parameters are implicitly any
// const loose = (event) => event.type; // ❌ Error under noImplicitAny: Parameter 'event' implicitly has an 'any' type.

const tuple: [number, string] = [1, "one"];

const options = {
  retries: 3,
  onRetry: (attempt: number) => console.log(attempt),
}; // no contextual type — members infer from values

const withContext: { retries: number; onRetry: (attempt: number) => void } = {
  retries: 3,
  onRetry: (attempt) => console.log(attempt), // attempt inferred
};

console.log(onClick, tuple, options, withContext);
```

## Key points
- Context comes from annotations, parameters, returns, and generic constraints.
- Callback parameters are inferred from the expected function type.
- Object literals get excess-property checks against the contextual type.
- Context can narrow literal types (`"a"` in a `"a" | "b"` slot).
- Without context, unannotated parameters fall back to implicit `any`.

## Gotchas
- Context is lost when you extract an expression into an unannotated variable.
- `const x = ...` in a new statement has no context from its later use.
- Contextual types do not flow backwards through arbitrary assignments.

## Best practice
- Annotate the destination (variable, parameter, return) to type callbacks for free.
- Keep inline callbacks when context matters; annotate when extracted.
