# Generic Constraints

> Phase 2 · Module 11 · Generics

**TL;DR** — Constraints restrict a type parameter to types that provide certain members, so the implementation can use them safely.

## Syntax
```ts
function getLength<T extends { length: number }>(value: T): number {
  return value.length;
}
```

## Examples
### Basic
```ts
function longest<T extends { length: number }>(a: T, b: T): T {
  return a.length >= b.length ? a : b;
}

const word = longest("abc", "de");     // string
const list = longest([1, 2], [3, 4]);  // number[]
```

### Practical
```ts
interface Identifiable {
  id: string;
}

function indexById<T extends Identifiable>(items: readonly T[]): Map<string, T> {
  return new Map(items.map((item) => [item.id, item]));
}

const users = [
  { id: "u1", name: "Ada" },
  { id: "u2", name: "Grace" },
];

const byId = indexById(users); // Map<string, { id: string; name: string }>
```

### Advanced / edge cases
```ts
function assign<T extends object, U extends object>(target: T, source: U): T & U {
  return Object.assign(target, source);
}

const merged = assign({ name: "Ada" }, { age: 36 });
// { name: string } & { age: number }

// Combine constraints with an intersection.
function serialize<T extends object & { toJSON(): unknown }>(value: T): string {
  return JSON.stringify(value.toJSON());
}

// ❌ Error: Property 'length' does not exist on type 'T'.
// function broken<T>(value: T): number {
//   return value.length;
// }
```

## Key points
- `T extends Constraint` requires every candidate to be assignable to the constraint.
- Constraints enable member access that is otherwise illegal on `T`.
- Constraints can be inline object types, interfaces, unions, or intersections.
- Constraints affect checking only; they add no runtime behavior.
- The inferred type remains the concrete argument type, not the constraint.

## Gotchas
- Unconstrained `T` exposes no members except those on `unknown`/`Object`.
- Over-constraining rejects valid callers and hurts reuse.
- `T extends any` or `T extends unknown` constrains nothing.

## Best practice
- Constrain to the smallest structural shape your body actually uses.
- Give reusable constraints a descriptive name such as `Identifiable`.
