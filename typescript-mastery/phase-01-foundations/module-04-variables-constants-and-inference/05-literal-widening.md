# Literal Widening

> Phase 1 · Module 04 · Variables, Constants, and Type Inference

**TL;DR** — Literal widening is TypeScript replacing a literal type with its base primitive in mutable positions.

## Syntax
```ts
let widened = "on";        // string  (widened)
const exact = "on";        // "on"    (not widened)
let pinned: "on" = "on";   // "on"    (annotation blocks widening)
```

## Examples
### Basic
```ts
let a = "on";  // string
let b = 10;    // number
let c = true;  // boolean

const d = "on"; // "on"
const e = 10;   // 10
const f = true; // true
```

### Practical
```ts
type Direction = "up" | "down";

let direction = "up";        // string — widened
// const move = (d: Direction) => d;
// move(direction);          // ❌ Error: Type 'string' is not assignable to type 'Direction'.

const safeDirection = "up";  // "up" — not widened
// move(safeDirection);      // ✅

function move(d: Direction): Direction {
  return d;
}
console.log(move(safeDirection));
```

### Advanced / edge cases
```ts
const settings = {
  theme: "dark", // string (property widening)
};

let theme = settings.theme; // string
// const exact: "dark" = settings.theme; // ❌ Error: Type 'string' is not assignable to type '"dark"'.

const frozen = {
  theme: "dark",
} as const; // { readonly theme: "dark" }

const exact: "dark" = frozen.theme; // ✅

// An annotation stops widening in either direction
let pinned: "dark" = "dark";
// pinned = "light"; // ❌ Error: Type '"light"' is not assignable to type '"dark"'.

console.log(theme, exact, pinned);
```

## Key points
- Widening happens in mutable bindings: `let`, `var`, mutable properties.
- Fresh literal expressions widen; annotations and `as const` stop it.
- Widening keeps variables reassignable to other values of the base type.
- Object and array members widen unless the structure is const-asserted.
- Function return expressions widen unless the return type is literal.

## Gotchas
- `let x = "on"` is `string`, so it cannot satisfy `"on" | "off"`.
- A widened object property loses literal information permanently.
- `readonly` alone does not prevent widening; use `as const` or annotations.

## Best practice
- Use `const` or `as const` when a literal must reach a literal-union API.
- Add a literal annotation when a variable should stay pinned to one value.
