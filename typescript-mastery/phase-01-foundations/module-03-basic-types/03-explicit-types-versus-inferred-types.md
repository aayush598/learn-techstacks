# Explicit Types Versus Inferred Types

> Phase 1 · Module 03 · Basic Types

**TL;DR** — Explicit annotations document intent and guard boundaries; inference keeps local code terse and accurate.

## Syntax
```ts
// explicit
const explicit: number = 42;

// inferred
const inferred = 42;

// explicit signature, inferred body
function sum(a: number, b: number): number {
  return a + b;
}
```

## Examples
### Basic
```ts
const inferred = "hello";        // "hello"
const explicit: string = "hello"; // string

console.log(inferred.toUpperCase(), explicit.toUpperCase());
```

### Practical
```ts
type User = { id: number; name: string };

// Explicit at the boundary: the contract is visible to callers
export function createUser(id: number, name: string): User {
  return { id, name }; // body still checked by inference
}

// Inferred locally: less noise, same safety
const user = createUser(1, "Ada");
const label = `${user.name} (#${user.id})`;
console.log(label); // ✅
```

### Advanced / edge cases
```ts
// Explicit annotation controls widening
const a = "on";          // "on"
let b: string = "on";    // string

// `as const` combines inference with literal precision
const config = { mode: "dark" } as const; // { readonly mode: "dark" }

// Explicit return type catches accidental contract drift
function parseId(raw: string): number {
  return Number(raw); // ✅ must return a number
}

console.log(a, b, config.mode, parseId("7"));
```

## Key points
- Inference is the default; annotations are opt-in.
- Annotate exported functions, public APIs, and object contracts.
- Skip annotations for obvious locals like `const n = 0`.
- Explicit types prevent accidental widening at boundaries.
- `as const` gives you literal inference without writing annotations.

## Gotchas
- Redundant annotations add noise but not safety.
  ```ts
  const n: number = 1; // ✅ valid, just unnecessary
  ```
- Over-annotating can mask a wrong value by widening it.
  ```ts
  let id: string | number = "42"; // hides that callers expect a number
  ```
- Explicit return types surface errors earlier.
  ```ts
  function f(): number {
    // ❌ Error: Type 'string' is not assignable to type 'number'.
    return "nope";
  }
  ```

## Best practice
- Annotate the edges, infer the middle.
- Prefer explicit return types on exported functions.
