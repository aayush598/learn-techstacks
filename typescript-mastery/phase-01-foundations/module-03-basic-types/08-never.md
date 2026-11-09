# never

> Phase 1 · Module 03 · Basic Types

**TL;DR** — `never` is the type of values that can never occur, used for functions that never return and exhaustive checks.

## Syntax
```ts
function fail(message: string): never {
  throw new Error(message);
}

function loop(): never {
  while (true) {}
}
```

## Examples
### Basic
```ts
function throwError(message: string): never {
  throw new Error(message);
}

try {
  throwError("boom");
} catch (e) {
  console.log((e as Error).message); // ✅
}
```

### Practical
```ts
type Shape =
  | { kind: "circle"; radius: number }
  | { kind: "square"; side: number };

function area(shape: Shape): number {
  switch (shape.kind) {
    case "circle":
      return Math.PI * shape.radius ** 2;
    case "square":
      return shape.side ** 2;
    default:
      return assertNever(shape);
  }
}

function assertNever(value: never): never {
  throw new Error(`Unhandled case: ${JSON.stringify(value)}`);
}

console.log(area({ kind: "circle", radius: 2 })); // ✅
```

### Advanced / edge cases
```ts
// never is assignable to every type, but nothing is assignable to never
// ❌ Error: Type 'number' is not assignable to type 'never'.
// const impossible: never = 1;

// An infinite loop also returns never
function forever(): never {
  while (true) {
    // spin
  }
}

// never disappears from unions
type Only = string | never; // string
const s: Only = "ok";
console.log(s, forever);
```

## Key points
- `never` means "no possible value".
- Functions that throw or loop forever return `never`.
- `never` is the bottom type: assignable to everything, nothing assignable to it.
- Exhaustiveness checks rely on the `never` parameter trick.
- `never[]` is an empty array type, distinct from `any[]`.

## Gotchas
- A function that returns `never` must not fall through.
  ```ts
  // ❌ Error: A function returning 'never' cannot have a reachable end point.
  // function bad(): never { console.log("x"); }
  ```
- `never` is not `void`; `void` returns undefined, `never` returns nothing.
- Forgetting the `default` branch defeats exhaustiveness.
  ```ts
  // If a new Shape kind is added, area() silently returns undefined.
  ```

## Best practice
- Use `assertNever` in exhaustive switches over discriminated unions.
- Return `never` for error helpers and unreachable guards.
