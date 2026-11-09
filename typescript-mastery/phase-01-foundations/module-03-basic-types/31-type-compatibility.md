# Type Compatibility

> Phase 1 · Module 03 · Basic Types

**TL;DR** — TypeScript is structural: a type is compatible when it has every member the target requires, regardless of names.

## Syntax
```ts
type Named = { name: string };
type Person = { name: string; age: number };

const person: Person = { name: "Ada", age: 36 };
const named: Named = person; // ✅ extra properties are fine
```

## Examples
### Basic
```ts
type Point2D = { x: number; y: number };
type Point3D = { x: number; y: number; z: number };

const p3: Point3D = { x: 1, y: 2, z: 3 };
const p2: Point2D = p3; // ✅ structural subset

console.log(p2); // { x: 1, y: 2, z: 3 }
```

### Practical
```ts
type HasId = { id: number };

function getId(entity: HasId): number {
  return entity.id;
}

const user = { id: 1, name: "Ada", active: true };
console.log(getId(user)); // ✅ extra fields allowed

// ❌ Error: Property 'id' is missing.
// getId({ name: "Grace" });
```

### Advanced / edge cases
```ts
// Method parameters are bivariant, so a narrower parameter is accepted
type Handler = { handle(event: { type: string }): void };
const specific: Handler = {
  handle(event: { type: "click" }) {
    console.log(event.type);
  },
}; // ✅ method syntax allows the narrower parameter

// Arrays are compatible by element type
const nums: number[] = [1, 2];
const vals: (number | string)[] = nums; // ✅

// Classes compare structurally too
class A { constructor(public x: number) {} }
class B { constructor(public x: number) {} }
const a: A = new B(1); // ✅ same shape

console.log(specific, vals, a);
```

## Key points
- Compatibility is structural, not nominal.
- A source may have more properties than the target requires.
- Function parameter checking is contravariant under `strictFunctionTypes`.
- Classes compare by members unless they have `private` fields.
- Generics add variance rules on top of structure.

## Gotchas
- Excess property checks reject fresh object literals.
  ```ts
  type Id = { id: number };
  // ❌ Error: Object literal may only specify known properties.
  // const x: Id = { id: 1, extra: true };
  ```
- `private` members make classes nominal.
  ```ts
  class A { private secret = 1; }
  class B { private secret = 1; }
  // ❌ Error: Types have separate declarations of a private property.
  // const a: A = new B();
  ```
- Optional properties affect compatibility.
  ```ts
  type A = { x?: number };
  type B = { x: number };
  const b: B = { x: 1 };
  const a: A = b; // ✅
  ```

## Best practice
- Design minimal interfaces that callers can satisfy structurally.
- Use `satisfies` to check shape without widening.
