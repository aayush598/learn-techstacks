# Narrowing with intersections

> Phase 2 · Module 09 · Type Narrowing and Type Guards

**TL;DR** — Intersections combine members; narrowing one part does not remove the others, and guards can refine them.

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

function describe(person: Person): string {
  return `${person.name} (${person.age})`; // ✅ both parts present
}
```

### Practical
```ts
type Entity = { id: string };
type Timestamped = { createdAt: Date };

type User = Entity & Timestamped & { email: string };

function toRecord(user: User): Record<string, string> {
  return {
    id: user.id,
    email: user.email,
    createdAt: user.createdAt.toISOString(),
  };
}
```

### Advanced / edge cases
```ts
type A = { kind: "a"; value: string };
type B = { kind: "b"; count: number };
type AB = A & B; // ⚠️ kind is "a" & "b" = never

type WithMeta<T> = T & { meta: { version: number } };

function attachMeta<T extends object>(value: T): WithMeta<T> {
  return { ...value, meta: { version: 1 } }; // ✅ intersection built by spread
}

function isWithMeta<T extends object>(value: T): value is WithMeta<T> {
  return "meta" in value && typeof (value as { meta?: unknown }).meta === "object";
}
```

## Key points
- Intersection means "has all members", not "either member".
- Narrowing an intersection refines shared properties.
- Guards like `in` add confidence about optional intersected parts.
- Generic intersections model decoration (`T & { meta: ... }`).
- Conflicting literal properties collapse to `never`.

## Gotchas
- `A & B` with conflicting discriminants is uninhabitable.
- Intersections do not merge methods with different signatures.
- `// ❌ Error:` `const ab: AB = { kind: "a", value: "x", count: 1 }` — `kind` cannot satisfy both.

## Best practice
- Use intersections to compose reusable capabilities.
- Avoid intersecting types that declare the same literal key.
