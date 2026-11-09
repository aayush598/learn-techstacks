# `as const`

> Phase 1 · Module 04 · Variables, Constants, and Type Inference

**TL;DR** — `as const` freezes an expression's types as deeply `readonly` literals.

## Syntax
```ts
const mode = "dark" as const;       // "dark"
const tuple = [1, "one"] as const;  // readonly [1, "one"]
```

## Examples
### Basic
```ts
const mode = "dark" as const;        // "dark"
const level = 3 as const;            // 3
const tuple = [1, "one"] as const;   // readonly [1, "one"]
const config = { retries: 3 } as const; // { readonly retries: 3 }
```

### Practical
```ts
type Status = "idle" | "loading" | "done";

const statuses = ["idle", "loading", "done"] as const;
type StatusFromArray = (typeof statuses)[number]; // "idle" | "loading" | "done"

const STATUS = {
  idle: "idle",
  loading: "loading",
  done: "done",
} as const;

type StatusFromObject = (typeof STATUS)[keyof typeof STATUS]; // same union

const s1: Status = statuses[0];  // ✅
const s2: StatusFromObject = STATUS.done; // ✅

console.log(s1, s2);
```

### Advanced / edge cases
```ts
const matrix = [
  [1, 2],
  [3, 4],
] as const; // readonly [readonly [1, 2], readonly [3, 4]]

const nested = {
  user: { name: "ada", roles: ["admin", "dev"] },
} as const; // deeply readonly, literal members

// as const applies to the expression, not the binding
let mutable = [1, 2] as const;
// mutable.push(3); // ❌ Error: Property 'push' does not exist on type 'readonly [1, 2]'.

// Spread can re-widen a readonly tuple
const widened: number[] = [...matrix[0]]; // ✅ number[]

// Arrays of const-asserted objects stay readonly
const points = [{ x: 0, y: 0 }] as const;
// points[0].x = 1; // ❌ Error: Cannot assign to 'x' because it is a read-only property.

console.log(nested, mutable, widened, points);
```

## Key points
- Applies `readonly` recursively to objects and arrays.
- Preserves literal types for every member.
- Works on any expression, not just declarations.
- Turns array literals into readonly tuples.
- Useful for deriving unions with `typeof`.

## Gotchas
- It does not deep-freeze at runtime; it is a type-level assertion only.
- `as const` on an already-widened variable cannot restore literals.
- Readonly tuples reject mutating methods like `push` and `sort`.

## Best practice
- Use `as const` for constant tables, config, and union sources.
- Derive unions from const data instead of duplicating literal unions.
