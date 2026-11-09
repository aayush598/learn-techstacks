# Intersection Conflicts

> Phase 2 · Module 08 · Union and Intersection Types

**TL;DR** — When intersected members disagree on a property type, the result is usually `never`, making the type impossible to satisfy.

## Syntax
```ts
type Conflict = { value: A } & { value: B };
```

## Examples
### Basic
```ts
type A = { status: "draft" };
type B = { status: "published" };

type Post = A & B;

// status becomes "draft" & "published", which is never.
// ❌ Error: Type '"draft"' is not assignable to type 'never'.
const post: Post = { status: "draft" };
```

### Practical
```ts
type ApiUser = { id: string; name: string };
type LocalUser = { id: number; name: string };

type User = ApiUser & LocalUser;

// id becomes string & number, which is never.
// ❌ Error: Type '{ id: string; name: string; }' is not assignable to type 'User'.
const user: User = { id: "u_1", name: "Ada" };
```

### Advanced / edge cases
```ts
// Optional vs required can also conflict.
type MaybeName = { name?: string };
type RequiredName = { name: number };
type Contact = MaybeName & RequiredName; // name: never

// ❌ Error: Type 'number' is not assignable to type 'never'.
const contact: Contact = { name: 1 };

// Function intersections do NOT become never; they become overloads.
type StringFn = (value: string) => void;
type NumberFn = (value: number) => void;
type Overloaded = StringFn & NumberFn;

declare const fn: Overloaded;
fn("text"); // ✅ matches the first overload
fn(42); // ✅ matches the second overload
```

## Key points
- Conflicting literal, primitive, or object property types intersect to `never`.
- A type containing a `never` property is effectively uninhabitable.
- Function intersections create overloads rather than `never`.
- Arrays and tuples can conflict on element types or length.
- TypeScript reports the conflict at assignment, not at the alias.

## Gotchas
- The alias itself does not error; only using it reveals the impossibility.
- `never` can propagate silently through conditional and mapped types.

```ts
type A = { items: string[] };
type B = { items: number[] };
type C = A & B;

// ❌ Error: Type 'string[]' is not assignable to type 'never'.
const c: C = { items: ["a"] };
```

## Best practice
- Audit duplicate keys before intersecting two domain types.
- Model genuinely exclusive cases as a union, not a conflicting intersection.
