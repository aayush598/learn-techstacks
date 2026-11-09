# Intersection Types

> Phase 2 · Module 08 · Union and Intersection Types

**TL;DR** — An intersection type requires a value to satisfy every member at once, written with `&`.

## Syntax
```ts
type Name = TypeA & TypeB;
```

## Examples
### Basic
```ts
type Named = { name: string };
type Aged = { age: number };

type Person = Named & Aged;

// ✅ must include both name and age
const person: Person = { name: "Ada", age: 36 };
console.log(person.name, person.age);
```

### Practical
```ts
type User = { id: string; email: string };
type Permissions = { roles: string[]; canPublish: boolean };

type AdminUser = User & Permissions;

const admin: AdminUser = {
  id: "u_1",
  email: "admin@example.com",
  roles: ["admin"],
  canPublish: true,
};

// ✅ intersections extend shapes without inheritance
console.log(admin.roles);
```

### Advanced / edge cases
```ts
type A = { id: string };
type B = { id: string; active: boolean };

type Merged = A & B; // id stays string, active is added
const merged: Merged = { id: "x", active: true }; // ✅

// ✅ T & {} removes null and undefined from T
type NonNullish<T> = T & {};
type Maybe = string | null | undefined;
const value: NonNullish<Maybe> = "safe"; // ✅

// Primitives usually intersect to never.
type Impossible = string & number;
// ❌ Error: Type 'string' is not assignable to type 'never'.
const bad: Impossible = "text";
```

## Key points
- `A & B` means "A **and** B", not either.
- Object intersections merge properties from all members.
- `T & unknown` is `T`; `T & any` is `any`.
- `T & {}` is a common way to exclude `null` and `undefined`.
- Conflicting primitive or literal members collapse to `never`.

## Gotchas
- Intersecting incompatible primitives produces `never`, not an error at the alias.
- An intersection is not a runtime merge; you must construct the full object.

```ts
type Id = string & { readonly __brand: "Id" };
type NumericId = string & number;

// ❌ Error: Type 'string' is not assignable to type 'never'.
const id: NumericId = "abc";
```

## Best practice
- Use intersections for composition of independent capabilities.
- Keep intersected members compatible; otherwise the type becomes uninhabitable.
