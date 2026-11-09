# TypeScript's Design Goals

> Phase 1 · Module 01 · Introduction to TypeScript

**TL;DR** — TypeScript aims to be a JavaScript-compatible, gradually typed language that catches likely errors without adding runtime overhead.

## Syntax

```ts
const values: number[] = [1, 2, 3];
```

## Examples

### Basic

```ts
// Goal: stay close to JavaScript while adding optional type information.
const values: number[] = [1, 2, 3];
const sum = values.reduce((total, value) => total + value, 0); // => 6
```

### Practical

```ts
// Goal: catch likely runtime errors at compile time.
type Order = { id: string; total: number };

function applyDiscount(order: Order, rate: number): Order {
  return { ...order, total: order.total * (1 - rate) };
}

// ❌ Error: Argument of type 'string' is not assignable to parameter of type 'number'. (TS2345)
applyDiscount({ id: "A1", total: 100 }, "0.1");
```

### Advanced / edge cases

```ts
// Goal: scale to large codebases with structural, gradual typing.
type HasId = { id: string };
type Entity = HasId & { createdAt: Date };

const user = { id: "u1", name: "Ada", createdAt: new Date() };
const entity: Entity = user; // ✅ extra properties are allowed
```

## Key points

- Be a strict superset of JavaScript and preserve runtime behavior.
- Provide a type system that catches likely mistakes, not every possible mistake.
- Emit clean, idiomatic JavaScript with no runtime type metadata.
- Support gradual typing so JavaScript can be migrated incrementally.
- Scale from small scripts to large multi-package codebases.
- Align with ECMAScript standards and avoid inventing runtime semantics.

## Gotchas

- The type system is intentionally unsound in places; it favors practicality over proof.
- Design goals do not include runtime validation or polyfilling missing APIs.
- Escape hatches such as `any` bypass the goals entirely.

## Best practice

- Use the type system to reject invalid states, not to model every theoretical constraint.
- Keep types simple enough that the compiler and your teammates stay fast.
