# Union Types

> Phase 2 · Module 08 · Union and Intersection Types

**TL;DR** — A union type says a value can be one of several types, written with `|`.

## Syntax
```ts
type Name = TypeA | TypeB | TypeC;
```

## Examples
### Basic
```ts
type Id = string | number;

const userId: Id = "u_42";
const orderId: Id = 1001;

// ✅ both assignments are valid
console.log(userId, orderId);
```

### Practical
```ts
function formatId(id: string | number): string {
  return typeof id === "number" ? `#${id}` : id.toUpperCase();
}

// ✅ narrowing lets each branch use type-specific methods
console.log(formatId(7)); // "#7"
console.log(formatId("abc")); // "ABC"
```

### Advanced / edge cases
```ts
type Nullable<T> = T | null;
type MaybeArray<T> = T | T[];

function firstOrNull<T>(value: MaybeArray<T>): T | null {
  if (Array.isArray(value)) {
    return value.length > 0 ? value[0] : null;
  }
  return value;
}

// ✅ generic unions keep call sites flexible
const a = firstOrNull([1, 2, 3]); // number | null
const b = firstOrNull("solo"); // string | null
```

## Key points
- `A | B` means "A **or** B", not "A **and** B".
- A union accepts any value assignable to at least one member.
- You can only use properties and methods common to every member until you narrow.
- Unions compose with generics, arrays, and function parameters.
- `boolean` is effectively the union `true | false`.

## Gotchas
- Reading a member-specific property before narrowing fails.
- A union of object types is not merged; it is a choice between shapes.

```ts
type A = { x: number };
type B = { y: number };
declare const value: A | B;

// ❌ Error: Property 'x' does not exist on type 'A | B'.
value.x;
```

## Best practice
- Keep unions small and meaningful; prefer named aliases over inline unions.
- Narrow with type guards before accessing member-specific data.
