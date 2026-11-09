# Type Inference in Generic Contexts

> Phase 1 · Module 04 · Variables, Constants, and Type Inference

**TL;DR** — In generic calls, TypeScript infers type arguments from the provided arguments, constraints, and contextual return type.

## Syntax
```ts
function identity<T>(value: T): T { return value; }
const a = identity("hello");        // "hello"
const b = identity<number>(1);      // number
```

## Examples
### Basic
```ts
function identity<T>(value: T): T {
  return value;
}

const a = identity("hello"); // "hello"
const b = identity(42);      // 42

function pair<A, B>(first: A, second: B): [A, B] {
  return [first, second];
}

const p = pair("age", 30); // [string, number]
```

### Practical
```ts
function pluck<T, K extends keyof T>(items: T[], key: K): T[K][] {
  return items.map((item) => item[key]);
}

const users = [
  { id: 1, name: "ada" },
  { id: 2, name: "alan" },
];

const ids = pluck(users, "id");     // number[]
const names = pluck(users, "name"); // string[]

// const type parameter keeps literal types
function tuple<const T extends readonly unknown[]>(items: T): T {
  return items;
}

const exact = tuple([1, "one"]); // readonly [1, "one"]

console.log(ids, names, exact);
```

### Advanced / edge cases
```ts
function create<T>(value: T): { value: T } {
  return { value };
}

const inferred = create("x"); // { value: string }

// Contextual return type participates in inference
const explicit: { value: "x" } = create("x");

// Defaults apply when inference finds no candidate
function wrap<T = string>(value?: T): T[] {
  return value === undefined ? [] : [value];
}

const empty = wrap(); // string[]

// Constraints narrow inference
function longest<T extends { length: number }>(a: T, b: T): T {
  return a.length >= b.length ? a : b;
}

const longer = longest("ab", "abc"); // "ab" | "abc"

// Inference failure falls back to the constraint
function keys<T extends object>(obj: T): (keyof T)[] {
  return Object.keys(obj) as (keyof T)[];
}

console.log(inferred, explicit, empty, longer, keys({ a: 1 }));
```

## Key points
- Type parameters infer from argument positions, including nested positions.
- `const` type parameters preserve literal argument types.
- Constraints bound inference and provide a fallback type.
- Contextual return types can drive inference too.
- Defaults apply when no inference candidate exists.

## Gotchas
- Inference prefers the constraint when no candidate is found, not `unknown`.
- Widening still occurs unless the parameter is `const` or annotated.
- Partial inference is not allowed; supply all or none of the type arguments.

## Best practice
- Add `const` type parameters when callers pass literals you must preserve.
- Use constraints to document and enforce the shape inference relies on.
