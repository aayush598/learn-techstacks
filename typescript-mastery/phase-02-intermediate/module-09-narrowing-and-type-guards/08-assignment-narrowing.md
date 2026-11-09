# Assignment narrowing

> Phase 2 · Module 09 · Type Narrowing and Type Guards

**TL;DR** — TypeScript narrows a variable based on its assigned value and resets narrowing when it is reassigned.

## Syntax
```ts
let value: string | number;
value = "hello";
value.toUpperCase(); // ✅ narrowed by assignment
```

## Examples
### Basic
```ts
let state: "idle" | "loading" | "done" = "idle";
state = "loading";
console.log(state.toUpperCase()); // ✅ "loading"

state = "done";
console.log(state.toUpperCase()); // ✅ "done"
```

### Practical
```ts
type Result = { ok: true; value: number } | { ok: false; error: string };

function compute(): Result {
  const raw = Math.random();
  let result: Result;

  if (raw > 0.5) {
    result = { ok: true, value: raw }; // ✅ success shape
  } else {
    result = { ok: false, error: "too small" }; // ✅ failure shape
  }

  return result;
}
```

### Advanced / edge cases
```ts
let value: string | number = "start";

if (typeof value === "string") {
  value = 42; // reassignment widens back to number
  value.toFixed(); // ✅ number
}

function fill(input?: string): string {
  let value = input; // string | undefined
  if (value === undefined) {
    value = "default"; // ✅ now string
  }
  return value; // ✅ string
}
```

## Key points
- Assignment gives the variable the type of the assigned expression.
- The declared type is still the ceiling; narrowing only refines it.
- Reassignment updates the flow type at that point.
- `const` keeps its narrowed type for the whole scope.
- Assignment narrowing works with `let` and `var` too.

## Gotchas
- Reassigning to a broader value loses the previous narrowing.
- Narrowing does not persist across a closure that reassigns.
- `// ❌ Error:` `let value: string | number = "x"; value = null;` violates the declared type.

## Best practice
- Prefer `const` when a value never changes.
- Assign a fully typed value in one branch instead of partial mutation.
