# Narrowing Union Types

> Phase 2 · Module 08 · Union and Intersection Types

**TL;DR** — Narrowing uses runtime checks to reduce a union to the specific member currently in use.

## Syntax
```ts
if (typeof value === "string") {
  // value: string
}
```

## Examples
### Basic
```ts
type Id = string | number;

function pad(id: Id): string {
  if (typeof id === "number") {
    return String(id).padStart(6, "0"); // ✅ number branch
  }
  return id.toUpperCase(); // ✅ string branch
}

console.log(pad(42), pad("ab"));
```

### Practical
```ts
type Payload = string | number | Date | string[];

function describe(payload: Payload): string {
  if (typeof payload === "string") return `text:${payload}`;
  if (typeof payload === "number") return `num:${payload}`;
  if (payload instanceof Date) return `date:${payload.toISOString()}`;
  return `list:${payload.join(",")}`; // ✅ remaining member: string[]
}

console.log(describe("hi"), describe(3), describe(new Date()), describe(["a"]));
```

### Advanced / edge cases
```ts
type Bird = { kind: "bird"; wings: number };
type Fish = { kind: "fish"; fins: number };
type Animal = Bird | Fish;

function isBird(animal: Animal): animal is Bird {
  return animal.kind === "bird";
}

declare const animal: Animal;
if (isBird(animal)) {
  console.log(animal.wings); // ✅ custom predicate narrows
} else {
  console.log(animal.fins);
}

let current: string | number = "start";
if (typeof current === "string") {
  // ❌ Error: Property 'toUpperCase' does not exist on type 'string | number'.
  const read = () => current.toUpperCase();
  console.log(read);
}
```

## Key points
- `typeof` narrows primitives; `instanceof` narrows class instances.
- The `in` operator narrows object unions by property presence.
- `Array.isArray` narrows arrays; equality narrows literals.
- Type predicates (`value is T`) create reusable custom guards.
- Narrowing follows control flow through `if`, `switch`, and early returns.

## Gotchas
- `typeof null` is `"object"`, so null needs its own check.
- Narrowing a mutable variable captured in a closure can be lost.
- Assertions (`as`) bypass narrowing and should not replace guards.

```ts
function length(value: string | null): number {
  // ❌ Error: 'value' is possibly 'null'.
  return value.length;
}
```

## Best practice
- Return early to keep each branch narrowed and flat.
- Prefer custom type predicates over repeated inline checks.
