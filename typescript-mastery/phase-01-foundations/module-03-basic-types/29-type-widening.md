# Type Widening

> Phase 1 · Module 03 · Basic Types

**TL;DR** — Widening is TypeScript generalizing a literal to its base type, usually with `let` and mutable properties.

## Syntax
```ts
let a = "on";           // string (widened)
const b = "on";         // "on" (literal)
let c = { mode: "on" }; // { mode: string }
```

## Examples
### Basic
```ts
let status = "active";   // string
const fixed = "active";  // "active"

status = "inactive";     // ✅
// ❌ Error: Type '"inactive"' is not assignable to type '"active"'.
// fixed = "inactive";

console.log(status, fixed);
```

### Practical
```ts
function setMode(mode: "light" | "dark"): void {
  console.log(mode);
}

const chosen = "dark"; // "dark" (const)
setMode(chosen);       // ✅

let picked = "dark";   // string (widened)
// ❌ Error: Argument of type 'string' is not assignable to parameter of type '"light" | "dark"'.
// setMode(picked);
```

### Advanced / edge cases
```ts
// Object literals widen their properties
const config = { mode: "dark", level: 3 };
// { mode: string; level: number }

// `as const` prevents widening
const strictConfig = { mode: "dark", level: 3 } as const;
// { readonly mode: "dark"; readonly level: 3 }

// Contextual typing can keep literals narrow without `as const`
const modes: ("light" | "dark")[] = ["light", "dark"];

console.log(config.mode, strictConfig.mode, modes);
```

## Key points
- `let` widens literals; `const` preserves them.
- Mutable object and array properties widen.
- Function parameters widen unless annotated with a literal union.
- `as const` and contextual typing suppress widening.
- Widening is usually desirable for mutable state.

## Gotchas
- A widened value no longer matches a literal-union parameter.
  ```ts
  let mode = "dark"; // string
  // ❌ Error: 'string' is not assignable to '"light" | "dark"'.
  ```
- Arrays widen element types.
  ```ts
  const xs = ["a", "b"]; // string[], not ("a" | "b")[]
  ```
- Annotating a literal with a wider type widens it.
  ```ts
  const x: string = "on"; // string
  ```

## Best practice
- Use `as const` for config objects and lookup tables.
- Annotate parameters with literal unions to catch widened inputs.
