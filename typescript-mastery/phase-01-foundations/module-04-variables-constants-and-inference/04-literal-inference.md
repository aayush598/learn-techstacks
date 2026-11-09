# Literal Inference

> Phase 1 · Module 04 · Variables, Constants, and Type Inference

**TL;DR** — TypeScript can infer a specific literal type such as `"on"` or `42` instead of the general primitive.

## Syntax
```ts
const label = "ready";        // literal type
let widened = "ready";        // widened primitive
let pinned: "ready" = "ready"; // explicit literal type
```

## Examples
### Basic
```ts
const mode = "dark";   // "dark"
const retries = 3;     // 3
const ready = true;    // true

let mutableMode = "dark"; // string
let mutableRetries = 3;   // number
```

### Practical
```ts
function setMode(mode: "light" | "dark"): void {
  console.log(mode);
}

const chosen = "dark"; // "dark"
setMode(chosen);       // ✅ literal fits the union

let loose = "dark";    // string
// setMode(loose);     // ❌ Error: Type 'string' is not assignable to type '"light" | "dark"'.
```

### Advanced / edge cases
```ts
const config = {
  mode: "dark",   // string (object properties widen)
  level: 2,       // number
} as const;       // readonly { readonly mode: "dark"; readonly level: 2 }

type Mode = typeof config.mode; // "dark"

const directions = ["up", "down"];        // string[]
const fixed = ["up", "down"] as const;    // readonly ["up", "down"]

function pick<T extends string>(value: T): T {
  return value;
}

const picked = pick("up"); // "up"
const pickedMode = pick("dark"); // "dark"

const same: Mode = pickedMode; // ✅

console.log(config, directions, fixed, picked, same);
```

## Key points
- `const` declarations infer literal types for primitives.
- `let` and mutable properties widen literals to their base type.
- Literal types make unions precise and exhaustiveness possible.
- Generic parameters can preserve a literal argument type.
- `as const` forces literal inference on whole structures.

## Gotchas
- Object properties widen even under `const`: `const o = { k: "v" }; // k: string`.
- Function return types widen literals unless annotated or `as const`.
- Mutating a literal-typed `const` object still requires `readonly` handling.

## Best practice
- Let `const` infer literals for scalar constants.
- Use `as const` when you need literal types inside objects and arrays.
