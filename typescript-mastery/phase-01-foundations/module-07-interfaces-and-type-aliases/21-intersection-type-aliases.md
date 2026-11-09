# Intersection Type Aliases

> Phase 1 · Module 07 · Interfaces and Type Aliases

**TL;DR** — An intersection type alias requires a value to satisfy every member type at once, combining their properties.

## Syntax
```ts
type Named = { name: string };
type Aged = { age: number };
type Person = Named & Aged;
```

## Examples
### Basic
```ts
type Named = { name: string };
type Aged = { age: number };

type Person = Named & Aged;

const person: Person = { name: "Ada", age: 36 }; // ✅ both required

// ❌ Error: Property 'age' is missing
// const broken: Person = { name: "Ada" };
```

### Practical
```ts
type Identified = { readonly id: string };
type Timestamped = { createdAt: Date; updatedAt: Date };
type SoftDeletable = { deletedAt?: Date };

type Entity<T> = Identified & Timestamped & SoftDeletable & { data: T };

const user: Entity<{ name: string }> = {
  id: "u1",
  createdAt: new Date(),
  updatedAt: new Date(),
  data: { name: "Ada" },
};
```

### Advanced / edge cases
```ts
type Named = { name: string };
type Aged = { age: number };

type A = { value: string };
type B = { value: number };

type Conflict = A & B; // value is string & number, which is never

// ❌ Error: Type 'string' is not assignable to type 'never'
// const bad: Conflict = { value: "x" };

// Intersections of function types produce overloads.
type Parse = ((input: string) => number) & ((input: number) => string);

// Flatten an intersection for readable tooltips.
type Prettify<T> = { [K in keyof T]: T[K] } & {};

type Readable = Prettify<Named & Aged>;
const readable: Readable = { name: "Grace", age: 40 };
```

## Key points
- An intersection means "all of these at once".
- The result has every property from every member.
- Conflicting property types collapse to `never`.
- Function intersections behave like overload sets.
- Intersections compose reusable fragments without inheritance.

## Gotchas
- `// ❌ Error:` satisfying an intersection with a conflicting property type.
- `string & number` is `never`; primitive intersections are usually a design error.
- An intersection does not check conflicts until the type is used.

## Best practice
- Use intersections to compose capability fragments (`Identified & Timestamped`).
- Wrap exported intersections in `Prettify` for readable editor hints.
