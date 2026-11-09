# Generic Inference

> Phase 2 · Module 11 · Generics

**TL;DR** — The compiler infers type arguments from arguments and context, so callers rarely write them explicitly.

## Syntax
```ts
function identity<T>(value: T): T {
  return value;
}

const result = identity("x"); // T inferred as string
```

## Examples
### Basic
```ts
function wrap<T>(value: T): { value: T } {
  return { value };
}

const wrappedNumber = wrap(1);   // { value: number }
const wrappedString = wrap("a"); // { value: string }
```

### Practical
```ts
function map<T, U>(items: readonly T[], fn: (item: T) => U): U[] {
  return items.map(fn);
}

const lengths = map(["one", "two"], (word) => word.length); // number[]

function find<T>(items: readonly T[], predicate: (item: T) => boolean): T | undefined {
  return items.find(predicate);
}

const found = find([1, 2, 3], (n) => n > 1); // number | undefined
```

### Advanced / edge cases
```ts
function pair<A, B>(first: A, second: B): [A, B] {
  return [first, second];
}

const mixed = pair(1, "a");        // [number, string]
const wide = pair(1, 2 as number); // [number, number]

function empty<T>(): T[] {
  return [];
}

const numbers: number[] = empty(); // context supplies T
const unknownValues = empty();     // unknown[] — no inference site

function twice<T extends number>(value: T): T {
  return value * 2 as T;
}

const four = twice(2); // number

// ❌ Error: Argument of type 'string' is not assignable to parameter of type 'number'.
// twice("x");
```

## Key points
- Inference gets candidates from parameter positions.
- Multiple candidates are combined into a common type.
- Expected return or assignment context can supply a candidate.
- Constraints filter candidates before selection.
- With no inference site and no default, `T` becomes `unknown`.

## Gotchas
- Literal arguments may widen (`"x"` to `string`) without `as const` or a constraint.
- Empty arrays can infer `never[]` in some positions.
- Return-only generics cannot infer; annotate the call site or add a parameter.

## Best practice
- Put inference sites in parameters so callers get useful types.
- Annotate when inference would pick a wider type than intended.
