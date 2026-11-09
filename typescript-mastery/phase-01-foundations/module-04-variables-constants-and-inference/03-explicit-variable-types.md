# Explicit Variable Types

> Phase 1 · Module 04 · Variables, Constants, and Type Inference

**TL;DR** — Explicit types state the intended contract, especially where inference would guess wrong or too narrowly.

## Syntax
```ts
let count: number;
let label: string = "ready";
const fixed: boolean = true;
```

## Examples
### Basic
```ts
let pending: boolean;      // declared, assigned later
pending = true;            // ✅

let items: string[] = [];  // empty array with a known element type
items.push("first");       // ✅

let state: "idle" | "busy" = "idle";
```

### Practical
```ts
type Status = "idle" | "loading" | "done";

let current: Status = "idle";
current = "loading"; // ✅
// current = "failed"; // ❌ Error: Type '"failed"' is not assignable to type 'Status'.

const lookup: Record<string, number> = {};
lookup["a"] = 1; // ✅

let onDone: (result: string) => void;
onDone = (result) => console.log(result); // ✅
```

### Advanced / edge cases
```ts
let nullable: string | null = null; // ✅ explicit union keeps null in scope

let values: Array<number | string> = [1, "two", 3]; // ✅

// Avoid: too-wide annotation loses useful precision
const answer: string | number = 42;

// Better: keep the precise type and widen only where needed
const precise = 42;          // 42
const widened: number = 42;  // number

console.log(nullable, values, answer, precise, widened);
```

## Key points
- Required when a variable has no initializer.
- Required when inference would pick `any` or `never`.
- Documents intent at module and API boundaries.
- Can narrow or widen what assignments are allowed.
- Applies to `const` too, overriding literal inference.

## Gotchas
- `let x: string;` read before assignment fails under `strict`.
- Over-annotating widens types and breaks literal-based APIs.
- A mismatched initializer errors immediately: `let n: number = "1"; // ❌ Error`.

## Best practice
- Use explicit types for empty containers, unions, and exported values.
- Keep annotations as narrow as the real contract allows.
