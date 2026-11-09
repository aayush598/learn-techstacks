# `let` Inference

> Phase 1 · Module 04 · Variables, Constants, and Type Inference

**TL;DR** — `let` bindings infer the widened base type of their initializer so they remain reassignable.

## Syntax
```ts
let count = 0;         // number
let label: string;     // explicit type, no initializer
```

## Examples
### Basic
```ts
let count = 0;        // number
let message = "hi";   // string
let running = false;  // boolean

count = 1;            // ✅
message = "hello";    // ✅
running = true;       // ✅
```

### Practical
```ts
let total = 0; // number
for (const n of [1, 2, 3]) {
  total += n; // ✅ mutation fits number
}

let label = "ada"; // string
// label = null;   // ❌ Error: Type 'null' is not assignable to type 'string'.

let nameOrNull: string | null = "ada"; // ✅ explicit union
nameOrNull = null;

console.log(total, label, nameOrNull);
```

### Advanced / edge cases
```ts
let values = [1, 2];      // number[]
values.push(3);           // ✅

let mixed = [1, "two"];   // (string | number)[]
// mixed.push(true);      // ❌ Error: Argument of type 'boolean' is not assignable to parameter of type 'string | number'.

let maybe;                // any — no initializer, no annotation
maybe = 1;
maybe = "two";

let safe: string | undefined;
safe = "value";
safe = undefined;

// Literal widening with let
let mode = "dark";        // string
// const narrowed: "dark" = mode; // ❌ Error: Type 'string' is not assignable to type '"dark"'.

console.log(values, mixed, maybe, safe, mode);
```

## Key points
- `let` widens literals to primitives, arrays to element arrays.
- Reassignment is checked against the inferred type.
- No initializer and no annotation produces `any`.
- An explicit annotation overrides widening.
- `let` with a union keeps all members available.

## Gotchas
- `let x = null;` infers `any`, not `null`.
- `let xs = [];` infers `never[]` and rejects pushes.
- Widening means `let mode = "dark"` will not satisfy `"dark"`-only APIs.

## Best practice
- Prefer `const`; use `let` only for values that truly change.
- Annotate `let` when the initializer is empty, `null`, or a literal you must keep.
