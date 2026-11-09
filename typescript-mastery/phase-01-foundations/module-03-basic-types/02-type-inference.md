# Type Inference

> Phase 1 · Module 03 · Basic Types

**TL;DR** — TypeScript derives types from values and context so you can omit most annotations.

## Syntax
```ts
let count = 0;                 // inferred number
const name = "Ada";            // inferred "Ada" (literal)
const ids = [1, 2, 3];         // inferred number[]
function double(n: number) {   // return inferred number
  return n * 2;
}
```

## Examples
### Basic
```ts
const title = "TypeScript";     // "TypeScript"
let version = 5.4;              // number
const active = true;            // true

console.log(title, version, active);
```

### Practical
```ts
const users = [
  { id: 1, name: "Ada" },
  { id: 2, name: "Grace" },
];
// inferred: { id: number; name: string }[]

const names = users.map((u) => u.name); // string[]
console.log(names); // ✅
```

### Advanced / edge cases
```ts
// Contextual typing: the expected type flows into the callback
const lengths: number[] = ["a", "bb", "ccc"].map((s) => s.length);

// Return type is inferred from all return paths
function classify(n: number) {
  if (n < 0) return "negative";
  return "non-negative";
}
// inferred: (n: number) => "negative" | "non-negative"

// An empty array needs an annotation to have a usable element type
const empty: string[] = [];
const safe: string[] = [];
console.log(lengths, classify(-1), empty, safe);
```

## Key points
- `let` widens literals to their base type; `const` keeps the literal type.
- Array literals infer a union of element types, then widen.
- Function return types are inferred from the body.
- Contextual typing uses the expected type to infer parameters.
- Inference is bidirectional: values flow up, expectations flow down.

## Gotchas
- Empty arrays and `null`/`undefined` initializers fall back to `any`.
  ```ts
  const list = []; // any[]
  // ❌ Error under noImplicitAny when used without annotation later
  ```
- Inference can widen more than you expect.
  ```ts
  let status = "active"; // string, not "active"
  ```
- Recursive functions may need an explicit return type to avoid circular inference.
  ```ts
  function fact(n: number): number {
    return n <= 1 ? 1 : n * fact(n - 1); // ✅ annotation breaks the cycle
  }
  ```

## Best practice
- Let inference do the work for locals and simple returns.
- Add annotations where a wider inferred type would be wrong.
