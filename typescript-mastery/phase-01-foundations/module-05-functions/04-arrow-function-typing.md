# Arrow Function Typing

> Phase 1 · Module 05 · Functions

**TL;DR** — Arrow functions inherit `this` lexically and get their types from an annotation or from context.

## Syntax
```ts
const fn = (param: Type): ReturnType => expression;
const block = (param: Type): ReturnType => {
  return value;
};
```

## Examples
### Basic
```ts
const inc = (n: number): number => n + 1;

console.log(inc(1)); // 2
```

### Practical
```ts
type Mapper<T, U> = (value: T, index: number) => U;

const lengths: Mapper<string, number> = (s, i) => s.length + i;

// ✅ contextual typing: s is string, i is number
console.log(["a", "bb"].map(lengths)); // [1, 3]
```

### Advanced / edge cases
```ts
// Returning an object literal needs parentheses
const make = (id: number): { id: number } => ({ id });

// ✅ lexical `this` inside a class field
class Counter {
  private count = 0;
  increment = (): void => {
    this.count++;
  };
}

const c = new Counter();
const run = c.increment;
run(); // still bound to c
```

## Key points
- Arrow functions do not have their own `this`, `arguments`, `super`, or `new.target`.
- Parenthesize object-literal bodies: `() => ({ ... })`.
- Contextual typing infers parameter types from the expected function type.
- Concise bodies return the expression automatically.

## Gotchas
- `// ❌ Error:` `const f = (): { a: number } => { a: 1 };` — block body returns nothing.
- Arrow functions cannot be used as constructors.
- Annotate generics explicitly: `<T>(x: T) => T` in `.ts`, but `.tsx` needs `<T,>` or `extends`.

## Best practice
- Use arrows for callbacks and anywhere lexical `this` is desired.
- Annotate the variable's function type rather than every parameter.
