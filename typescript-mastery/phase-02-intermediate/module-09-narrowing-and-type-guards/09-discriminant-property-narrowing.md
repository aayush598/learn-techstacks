# Discriminant property narrowing

> Phase 2 · Module 09 · Type Narrowing and Type Guards

**TL;DR** — A shared literal property (the discriminant) lets TypeScript narrow a union to the exact member in a `switch` or `if`.

## Syntax
```ts
if (shape.kind === "circle") {
  // shape narrowed by the discriminant
}
```

## Examples
### Basic
```ts
type Circle = { kind: "circle"; radius: number };
type Square = { kind: "square"; side: number };
type Shape = Circle | Square;

function area(shape: Shape): number {
  switch (shape.kind) {
    case "circle":
      return Math.PI * shape.radius ** 2; // ✅ Circle
    case "square":
      return shape.side ** 2; // ✅ Square
  }
}
```

### Practical
```ts
type Event =
  | { type: "click"; x: number; y: number }
  | { type: "keydown"; key: string }
  | { type: "scroll"; deltaY: number };

function handle(event: Event): string {
  if (event.type === "click") {
    return `clicked at ${event.x},${event.y}`; // ✅ click
  }
  if (event.type === "keydown") {
    return `pressed ${event.key}`; // ✅ keydown
  }
  return `scrolled ${event.deltaY}`; // ✅ scroll
}
```

### Advanced / edge cases
```ts
type State =
  | { status: "idle" }
  | { status: "loading"; startedAt: number }
  | { status: "success"; data: string[] }
  | { status: "error"; message: string };

function render(state: State): string {
  switch (state.status) {
    case "idle":
      return "Ready";
    case "loading":
      return `Loading since ${state.startedAt}`; // ✅ startedAt exists
    case "success":
      return state.data.join(", "); // ✅ data exists
    case "error":
      return state.message; // ✅ message exists
  }
}
```

## Key points
- Each union member declares the same property with a distinct literal type.
- The discriminant must be a literal union, not just `string`.
- `switch` gives the cleanest narrowing and exhaustiveness checking.
- Nested discriminated unions narrow one level at a time.
- Works well with `never` checks in the `default` branch.

## Gotchas
- Using `string` instead of literals disables narrowing.
- A missing `default` may leave the function returning `undefined`.
- `// ❌ Error:` `type Shape = { kind: string; radius: number } | { kind: string; side: number }` cannot be discriminated.

## Best practice
- Name the discriminant consistently, e.g. `kind`, `type`, or `status`.
- Keep each member's discriminant a unique string literal.
