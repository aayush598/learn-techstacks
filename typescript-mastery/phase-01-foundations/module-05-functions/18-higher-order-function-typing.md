# Higher-Order Function Typing

> Phase 1 · Module 05 · Functions

**TL;DR** — A higher-order function takes or returns another function; annotate both directions with generic function types.

## Syntax
```ts
function hof<T, U>(fn: (value: T) => U): (value: T) => U { /* ... */ }
```

## Examples
### Basic
```ts
function twice(fn: (n: number) => number, x: number): number {
  return fn(fn(x));
}

console.log(twice((n) => n + 1, 3)); // 5
```

### Practical
```ts
function compose<A, B, C>(f: (b: B) => C, g: (a: A) => B): (a: A) => C {
  return (a) => f(g(a));
}

const trim = (s: string) => s.trim();
const length = (s: string) => s.length;

const trimLength = compose(length, trim);
console.log(trimLength("  hi ")); // 2
```

### Advanced / edge cases
```ts
// Returning a generic function
function identityFactory<T>(): <U extends T>(value: U) => U {
  return (value) => value;
}

// ✅ preserving parameter tuples
function curry<A, B, C>(
  fn: (a: A, b: B) => C
): (a: A) => (b: B) => C {
  return (a) => (b) => fn(a, b);
}

const add = curry((a: number, b: number) => a + b);
console.log(add(1)(2)); // 3
```

## Key points
- Generic parameters propagate types from input functions to output functions.
- Returned functions can themselves be generic.
- `compose`/`pipe`/`curry` are classic higher-order shapes.
- Contextual typing infers inner arrow parameters.

## Gotchas
- `// ❌ Error:` losing generics by annotating `compose` with `any`.
- Overloading curried functions without tuples produces poor inference.
- Function-returning functions need parentheses in type annotations.

## Best practice
- Add type parameters in left-to-right order of appearance.
- Prefer small composable functions over deeply nested generics.
