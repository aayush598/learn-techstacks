# Object Union Types

> Phase 2 · Module 08 · Union and Intersection Types

**TL;DR** — A union of object types represents a value that is exactly one of several object shapes.

## Syntax
```ts
type Shape = { /* shape A */ } | { /* shape B */ };
```

## Examples
### Basic
```ts
type Circle = { radius: number };
type Square = { side: number };

type Shape = Circle | Square;

const circle: Shape = { radius: 2 };
const square: Shape = { side: 3 };

// ✅ each value matches one member
console.log(circle, square);
```

### Practical
```ts
type Circle = { kind: "circle"; radius: number };
type Square = { kind: "square"; side: number };
type Shape = Circle | Square;

function area(shape: Shape): number {
  switch (shape.kind) {
    case "circle":
      return Math.PI * shape.radius ** 2;
    case "square":
      return shape.side ** 2;
  }
}

// ✅ the shared discriminant narrows the object union
console.log(area({ kind: "circle", radius: 2 }));
console.log(area({ kind: "square", side: 3 }));
```

### Advanced / edge cases
```ts
type ApiUser = { id: string; name: string };
type ApiError = { status: number; message: string };
type ApiResult = ApiUser | ApiError;

function isUser(value: ApiResult): value is ApiUser {
  return "name" in value;
}

declare const result: ApiResult;
if (isUser(result)) {
  console.log(result.name); // ✅ narrowed to ApiUser
} else {
  console.log(result.message); // ✅ narrowed to ApiError
}
```

## Key points
- Only properties present on every member are accessible before narrowing.
- Object unions are "one of these shapes", not a merged object.
- A shared discriminant property makes narrowing reliable.
- Type predicates and the `in` operator narrow object unions.
- Excess property checks apply to fresh object literals.

## Gotchas
- Accessing a property unique to one member fails until narrowed.
- A fresh object literal with a typo can match the wrong member or fail entirely.

```ts
type A = { kind: "a"; value: number };
type B = { kind: "b"; label: string };
declare const item: A | B;

// ❌ Error: Property 'value' does not exist on type 'A | B'.
console.log(item.value);
```

## Best practice
- Add a literal discriminant to every object union used in branching.
- Write a type predicate when a discriminant is not available.
