# Combining Interfaces

> Phase 2 · Module 08 · Union and Intersection Types

**TL;DR** — Interfaces combine through multiple `extends` clauses, which is equivalent to intersecting their members.

## Syntax
```ts
interface Combined extends A, B {}
```

## Examples
### Basic
```ts
interface Named {
  name: string;
}

interface Aged {
  age: number;
}

interface Person extends Named, Aged {}

// ✅ inherits both property sets
const person: Person = { name: "Ada", age: 36 };
console.log(person);
```

### Practical
```ts
interface Entity {
  id: string;
  createdAt: Date;
}

interface SoftDeletable {
  deletedAt?: Date;
}

interface Auditable {
  updatedAt: Date;
}

interface Record extends Entity, SoftDeletable, Auditable {
  title: string;
}

// ✅ small interfaces compose into a domain record
const record: Record = {
  id: "r_1",
  createdAt: new Date(),
  updatedAt: new Date(),
  title: "Quarterly report",
};
console.log(record.title);
```

### Advanced / edge cases
```ts
interface A {
  id: string;
}

interface B {
  id: string;
  active: boolean;
}

interface Merged extends A, B {} // ✅ compatible duplicate id

// Interfaces with the same name merge across declarations.
interface Config {
  host: string;
}
interface Config {
  port: number;
}
const config: Config = { host: "localhost", port: 3000 }; // ✅

// A type alias intersection is equivalent for object shapes.
type ConfigAlias = { host: string } & { port: number };
const alias: ConfigAlias = config; // ✅
```

## Key points
- `extends A, B` composes interfaces like an intersection.
- Duplicate members must have compatible types.
- Same-name interfaces merge across declarations; type aliases do not.
- Interfaces can extend classes, capturing their instance shape.
- Prefer interfaces for public object contracts that may be extended.

## Gotchas
- An interface cannot extend a union of object types.
- Declaration merging can surprise you when names collide across files.

```ts
type Shape = { kind: "circle" } | { kind: "square" };

// ❌ Error: An interface can only extend an object type or intersection of object types with statically known members.
interface Bad extends Shape {}
```

## Best practice
- Use `extends` for interface composition and `&` for type-alias composition.
- Keep interfaces small and single-purpose so combinations stay readable.
