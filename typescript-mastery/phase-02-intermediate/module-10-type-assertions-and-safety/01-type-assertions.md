# Type Assertions

> Phase 2 · Module 10 · Type Assertions and Type Safety

**TL;DR** — A type assertion tells the compiler to treat a value as a different type, but it changes nothing at runtime.

## Syntax

```ts
const value = expression as Type;
```

## Examples

### Basic

```ts
const raw: unknown = "hello";
const text = raw as string;

console.log(text.length); // 5
```

### Practical

```ts
type ApiUser = { id: number; name: string };

function parseUser(json: string): ApiUser {
  // ✅ Assertion satisfies the compiler; it does not check the JSON.
  return JSON.parse(json) as ApiUser;
}

const user = parseUser('{"id":1,"name":"Ada"}');
console.log(user.name); // "Ada"
```

### Advanced / edge cases

```ts
type Circle = { kind: "circle"; radius: number };
type Square = { kind: "square"; side: number };
type Shape = Circle | Square;

function area(shape: Shape): number {
  if (shape.kind === "circle") {
    return Math.PI * shape.radius ** 2;
  }
  // Narrowing already knows this is Square, so this assertion is redundant.
  const square = shape as Square; // ✅ compiles, but unnecessary
  return square.side ** 2;
}
```

## Key points

- Assertions are erased during compilation; emitted JavaScript is unchanged.
- `as` only changes the compiler's view, never the runtime value.
- Assertions are allowed when the source and target types sufficiently overlap.
- Prefer narrow types at the point of use over asserting a broad `unknown`.
- Assertions do not validate data and do not add missing properties or methods.

## Gotchas

- Asserting between unrelated types is rejected by the compiler.

```ts
const n = 1 as string;
// ❌ Error: Conversion of type 'number' to type 'string' may be a mistake because neither type sufficiently overlaps with the other. (TS2352)
```

- `JSON.parse` returns `any`; asserting the result hides malformed payloads.
- A widened assertion can make later property access compile while failing at runtime.

## Best practice

- Use assertions only at boundaries where you can prove the type out of band.
- Pair every external-data assertion with real runtime validation.
