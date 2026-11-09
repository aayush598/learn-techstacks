# Exhaustive Union Handling

> Phase 2 · Module 08 · Union and Intersection Types

**TL;DR** — Exhaustive handling ensures every union member is processed, so adding a member produces a compile error instead of a silent gap.

## Syntax
```ts
switch (value.kind) {
  case "a": /* ... */
  case "b": /* ... */
}
```

## Examples
### Basic
```ts
type Status = "idle" | "loading" | "success" | "error";

function label(status: Status): string {
  switch (status) {
    case "idle":
      return "Idle";
    case "loading":
      return "Loading";
    case "success":
      return "Done";
    case "error":
      return "Failed";
  }
}

// ✅ no default needed; all four members return
console.log(label("loading"));
```

### Practical
```ts
type Status = "idle" | "loading" | "success" | "error";

const LABELS: Record<Status, string> = {
  idle: "Idle",
  loading: "Loading",
  success: "Done",
  error: "Failed",
};

function label(status: Status): string {
  return LABELS[status];
}

// ✅ Record<Status, string> forces a value for every member
console.log(label("error"));
```

### Advanced / edge cases
```ts
type Shape =
  | { kind: "circle"; radius: number }
  | { kind: "square"; side: number }
  | { kind: "triangle"; base: number; height: number };

function area(shape: Shape): number {
  if (shape.kind === "circle") {
    return Math.PI * shape.radius ** 2;
  }
  if (shape.kind === "square") {
    return shape.side ** 2;
  }
  // ✅ here shape is narrowed to the final member
  return (shape.base * shape.height) / 2;
}

console.log(area({ kind: "triangle", base: 4, height: 3 }));
```

## Key points
- An exhaustive `switch` over a union needs no `default`.
- `Record<Union, T>` enforces completeness in lookup tables.
- Early returns make the final remaining member explicit.
- Exhaustiveness turns future union changes into compile errors.
- It works for both primitive and object unions.

## Gotchas
- Adding a `default` that returns a fallback hides missing cases.
- A non-exhaustive switch may infer a return type that includes `undefined`.

```ts
type Status = "idle" | "error";

function label(status: Status): string {
  switch (status) {
    case "idle":
      return "Idle";
  }
  // ❌ Error: Function lacks ending return statement and return type does not include 'undefined'.
}
```

## Best practice
- Prefer exhaustive switches without `default` for closed domains.
- Add a `never` check in `default` when a default branch is unavoidable.
