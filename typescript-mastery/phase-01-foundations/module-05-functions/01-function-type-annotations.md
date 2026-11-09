# Function Type Annotations

> Phase 1 · Module 05 · Functions

**TL;DR** — Describe a function's parameters and return type with `(a: T) => R` syntax used as a type.

## Syntax
```ts
type Fn = (param: Type, other: Type) => ReturnType;
const fn: Fn = (param, other) => { /* ... */ };
```

## Examples
### Basic
```ts
const add: (a: number, b: number) => number = (a, b) => a + b;

// ✅ parameters and return are inferred from the annotation
add(1, 2);
```

### Practical
```ts
type Formatter = (value: number, unit: string) => string;

const format: Formatter = (value, unit) => `${value}${unit}`;

console.log(format(42, "px")); // "42px"
```

### Advanced / edge cases
```ts
// A function type can be a union of signatures
type Handler = ((e: MouseEvent) => void) | ((e: KeyboardEvent) => void);

const handler: Handler = (e: MouseEvent | KeyboardEvent) => {
  // e is MouseEvent | KeyboardEvent here
  console.log(e.type);
};

// ✅ parentheses are required when returning a function type
const factory: () => (n: number) => string = () => (n) => String(n);
```

## Key points
- `(a: T) => R` is a type, not an implementation.
- Annotating a variable makes parameter inference flow into the body.
- Contextual typing removes the need to repeat annotations on arrow parameters.
- Use parentheses when a function type is nested or part of a union.

## Gotchas
- `(a: number) => string` and `(a: number) => string | number` are different types.
- `type Fn = (a: number) => string | (b: string) => void` is ambiguous; wrap each side in parentheses.
- `// ❌ Error:` `let f: (a: number) => number = (a) => a.toFixed();` — returning `string` where `number` is expected.

## Best practice
- Prefer a named `type` alias for signatures reused in multiple places.
- Let contextual typing infer parameter types instead of repeating them on both sides.
