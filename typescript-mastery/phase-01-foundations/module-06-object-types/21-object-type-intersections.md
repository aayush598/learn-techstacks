# Object Type Intersections

> Phase 1 · Module 06 · Object Types and Object Properties

**TL;DR** — `A & B` requires a value to satisfy both object types at once, combining all their properties.

## Syntax
```ts
type A = { a: string };
type B = { b: number };
type C = { c: boolean };
type Combined = A & B & C;
```

## Examples
### Basic
```ts
type Named = { name: string };
type Aged = { age: number };

type Person = Named & Aged;

const person: Person = { name: "Ada", age: 36 };

console.log(person.name, person.age);
```

### Practical
```ts
type Identifiable = { id: string };
type Timestamped = { createdAt: Date };

type Entity = Identifiable & Timestamped;

function touch(entity: Entity): Entity {
  return { ...entity, createdAt: new Date() };
}

console.log(touch({ id: "u1", createdAt: new Date(0) }).id);
```

### Advanced / edge cases
```ts
type Identified = { id: string };
type Kinds = { kind: "a" } | { kind: "b" };
type Item = Identified & Kinds;

const item: Item = { id: "1", kind: "a" };

console.log(item.id, item.kind);
```

## Key points
- Intersection requires every member type to be satisfied.
- Properties from all members are available on the result.
- Overlapping properties have their types intersected.
- Intersections distribute over unions.
- Intersections describe types only; they do not merge values at runtime.

## Gotchas
- Conflicting property types collapse to `never`: `{ id: string } & { id: number }` can never be satisfied.
- `// ❌ Error:` `const c: { id: string } & { id: number } = { id: "x" };` — `id` is `never`.
- Intersecting incompatible primitives produces `never`, not a merged type.

## Best practice
- Compose small, non-overlapping capability types with `&`.
- Use object spread (`{ ...a, ...b }`) when you need a runtime merge; `&` is static only.
