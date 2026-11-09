# Structural Typing

> Phase 1 · Module 06 · Object Types and Object Properties

**TL;DR** — TypeScript compares object types by their shape, so any value with the required properties is accepted.

## Syntax
```ts
type Requirements = { key: string };
const value: Requirements = { key: "value" };
```

## Examples
### Basic
```ts
type Named = { name: string };

class Person {
  constructor(public name: string) {}
}

const person: Named = new Person("Ada"); // ✅ matches by shape, not by name

console.log(person.name);
```

### Practical
```ts
type Point = { x: number; y: number };

const point3d = { x: 1, y: 2, z: 3 };
const point2d: Point = point3d; // ✅ extra properties are allowed

console.log(point2d.x, point2d.y);
```

### Advanced / edge cases
```ts
type Serializable = { serialize(): string };

class User {
  constructor(private name: string) {}

  serialize(): string {
    return JSON.stringify({ name: this.name });
  }
}

const serializable: Serializable = new User("Ada"); // ✅ method shape matches

// empty object type accepts any non-nullish value
const anything: {} = 42;
const nonPrimitive: object = { ok: true };

console.log(serializable.serialize(), anything, nonPrimitive);
```

## Key points
- Assignability is based on members, not on the declared name of a type or class.
- The target's required properties must exist in the source; extras are ignored.
- Classes can satisfy object types if their public shape matches.
- `{}` means "any non-nullish value", not "empty object only".
- `object` means any non-primitive value.

## Gotchas
- Classes with `private` or `protected` members are matched nominally; two unrelated classes with the same private field are not interchangeable.
- `// ❌ Error:` `class A { private x = 1 } class B { private x = 1 } const a: A = new B();` — private origins differ.
- Structural compatibility can hide a renamed or semantically different property that happens to share a type.

## Best practice
- Model behavior with the smallest shape a function actually needs.
- Use distinct branded types when two structurally identical types must not be confused.
