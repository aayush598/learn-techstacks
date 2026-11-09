# Union and Intersection Combinations

> Phase 2 · Module 08 · Union and Intersection Types

**TL;DR** — Combine unions and intersections to share common fields across variants or to restrict a whole union.

## Syntax
```ts
type Combined = (A | B) & C;
type Precedence = A | (B & C);
```

## Examples
### Basic
```ts
type Cat = { name: string; meows: boolean };
type Dog = { name: string; barks: boolean };

type Pet = Cat | Dog;
type Owned = Pet & { ownerId: string };

// ✅ ownerId is required for either pet variant
const pet: Owned = { name: "Milo", meows: true, ownerId: "u_1" };
console.log(pet.name, pet.ownerId);
```

### Practical
```ts
type Success = { ok: true; data: string[] };
type Failure = { ok: false; error: string };

type Result = (Success | Failure) & { requestId: string };

function render(result: Result): string {
  return result.ok
    ? `[${result.requestId}] ${result.data.join(", ")}`
    : `[${result.requestId}] ${result.error}`;
}

// ✅ shared metadata stays attached to every variant
console.log(render({ ok: true, data: ["a"], requestId: "req_1" }));
console.log(render({ ok: false, error: "timeout", requestId: "req_2" }));
```

### Advanced / edge cases
```ts
type A = { a: string };
type B = { b: number };
type C = { c: boolean };

// & binds tighter than |, so this is A | (B & C).
type One = A | B & C;
const one: One = { a: "x" }; // ✅ matches A
const two: One = { b: 1, c: true }; // ✅ matches B & C

// Parentheses change the meaning entirely.
type Two = (A | B) & C;
// ❌ Error: Property 'c' is missing in type '{ a: string; }' but required in type 'C'.
const bad: Two = { a: "x" };
```

## Key points
- `&` has higher precedence than `|`.
- `(A | B) & C` distributes to `(A & C) | (B & C)`.
- Intersecting a union with a common shape adds that shape to every variant.
- Always parenthesize when mixing `|` and `&`.
- Distribution is a type-level rule, not a runtime transformation.

## Gotchas
- Missing parentheses silently produce a different type.
- Intersecting a variant with an incompatible field can reduce it to `never`.

```ts
type A = { kind: "a" };
type B = { kind: "b" };
type Forced = (A | B) & { kind: "a" };

// ❌ Error: Type '"b"' is not assignable to type '"a"'.
const forced: Forced = { kind: "b" };
```

## Best practice
- Parenthesize every mixed union/intersection expression.
- Use `(VariantA | VariantB) & Shared` to attach cross-cutting metadata.
