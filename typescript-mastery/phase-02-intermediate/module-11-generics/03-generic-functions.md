# Generic Functions

> Phase 2 · Module 11 · Generics

**TL;DR** — A generic function declares type parameters that are inferred from its arguments and flow through to its return type.

## Syntax
```ts
function identity<T>(value: T): T {
  return value;
}
```

## Examples
### Basic
```ts
function last<T>(items: readonly T[]): T | undefined {
  return items.length > 0 ? items[items.length - 1] : undefined;
}

const n = last([1, 2, 3]); // number | undefined
const s = last(["a", "b"]); // string | undefined
```

### Practical
```ts
function pluck<T, K extends keyof T>(items: readonly T[], key: K): T[K][] {
  return items.map((item) => item[key]);
}

const users = [
  { id: "u1", name: "Ada" },
  { id: "u2", name: "Grace" },
];

const names = pluck(users, "name"); // string[]
const ids = pluck(users, "id");     // string[]
```

### Advanced / edge cases
```ts
function zip<A, B>(left: readonly A[], right: readonly B[]): Array<[A, B]> {
  const length = Math.min(left.length, right.length);
  return Array.from({ length }, (_, index): [A, B] => [left[index], right[index]]);
}

const pairs = zip([1, 2], ["a", "b"]); // Array<[number, string]>

// A generic function type.
type Apply = <T, R>(value: T, fn: (value: T) => R) => R;

const apply: Apply = (value, fn) => fn(value);
const size = apply("hello", (text) => text.length); // number
```

## Key points
- Type parameters sit between the function name and the parameter list.
- Inference reads arguments and picks the most useful type.
- Return types can depend on inputs (`T`, `T[K]`, `U[]`).
- Generic function types use the same `<T>` syntax.
- The body sees `T` as an opaque type unless it is constrained.

## Gotchas
- The compiler cannot run type-level logic; you cannot `typeof value === "T"`.
- `// ❌ Error:` returning a cast to satisfy `T` hides a real bug.
- Explicit arguments like `identity<string>("x")` are often redundant.

## Best practice
- Let call sites infer arguments; expose explicit parameters only when needed.
- Constrain `T` for every member the body actually uses.
