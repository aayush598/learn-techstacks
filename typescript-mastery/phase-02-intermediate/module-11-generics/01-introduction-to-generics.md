# Introduction to Generics

> Phase 2 · Module 11 · Generics

**TL;DR** — Generics let one implementation work across many types while preserving the exact type each caller uses.

## Syntax
```ts
function identity<T>(value: T): T {
  return value;
}
```

## Examples
### Basic
```ts
function identity<T>(value: T): T {
  return value;
}

const n = identity(42);      // number
const s = identity("hello"); // string
```

### Practical
```ts
function first<T>(items: readonly T[]): T | undefined {
  return items[0];
}

const firstNumber = first([1, 2, 3]); // number | undefined
const firstString = first(["a", "b"]); // string | undefined
```

### Advanced / edge cases
```ts
// A union return type loses the relationship between input and output.
function unionIdentity(value: string | number): string | number {
  return value;
}
const widened = unionIdentity("x"); // string | number

// A generic keeps that relationship intact.
function genericIdentity<T>(value: T): T {
  return value;
}
const narrowed = genericIdentity("x"); // string

// Generic arrow function in a .ts file; the comma avoids JSX ambiguity in .tsx.
const pair = <T,>(left: T, right: T): [T, T] => [left, right];
const coords = pair(1, 2); // [number, number]
```

## Key points
- Type parameters are placeholders substituted per use.
- Generics preserve input/output relationships that unions erase.
- They work with functions, interfaces, type aliases, and classes.
- Type arguments are usually inferred, not written by hand.
- Generics are erased at runtime; they exist only for the checker.

## Gotchas
- `// ❌ Error:` in `.tsx`, `<T>(x: T) => x` parses as JSX; write `<T,>(x: T) => x`.
- There is no runtime `T` value to inspect or branch on.
- A generic used in only one position adds noise without safety.

## Best practice
- Reach for generics when two or more positions must share a type.
- Prefer inference over explicit type arguments when the call is unambiguous.
