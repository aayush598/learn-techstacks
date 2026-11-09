# Object Type Unions

> Phase 1 · Module 06 · Object Types and Object Properties

**TL;DR** — `A | B` accepts a value of either shape, and you must narrow before using shape-specific properties.

## Syntax
```ts
type Result = { kind: "a"; a: string } | { kind: "b"; b: number };
```

## Examples
### Basic
```ts
type Cat = { kind: "cat"; meow(): void };
type Dog = { kind: "dog"; bark(): void };

type Pet = Cat | Dog;

function speak(pet: Pet): void {
  if (pet.kind === "cat") {
    pet.meow(); // ✅ narrowed to Cat
  } else {
    pet.bark(); // ✅ narrowed to Dog
  }
}

speak({ kind: "cat", meow: () => console.log("meow") });
```

### Practical
```ts
type Result =
  | { status: "ok"; data: string }
  | { status: "error"; message: string };

function unwrap(result: Result): string {
  return result.status === "ok" ? result.data : result.message;
}

console.log(unwrap({ status: "ok", data: "done" }));
```

### Advanced / edge cases
```ts
type Shape =
  | { kind: "circle"; radius: number }
  | { kind: "square"; size: number }
  | { kind: "rect"; width: number; height: number };

function area(shape: Shape): number {
  switch (shape.kind) {
    case "circle":
      return Math.PI * shape.radius ** 2;
    case "square":
      return shape.size ** 2;
    case "rect":
      return shape.width * shape.height;
  }
}

console.log(area({ kind: "circle", radius: 2 }));
```

## Key points
- Before narrowing, only properties common to every member are accessible.
- A shared literal property such as `kind` or `status` acts as a discriminant.
- Control-flow checks (`if`, `switch`, `in`) narrow the union.
- Unions model alternatives; intersections model combinations.
- Exhaustive switches can prove that every variant is handled.

## Gotchas
- `// ❌ Error:` `pet.meow()` — `meow` does not exist on `Dog`.
- `// ❌ Error:` `const s: Shape = { kind: "circle" };` — `radius` is required for that variant.
- Adding a new variant without updating a non-exhaustive consumer can leave runtime gaps.

## Best practice
- Use a literal discriminant field on every variant.
- Let `switch` cover all variants and keep `noImplicitReturns` enabled to catch missing cases.
