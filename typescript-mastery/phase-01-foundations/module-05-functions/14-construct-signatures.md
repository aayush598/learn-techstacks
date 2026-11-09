# Construct Signatures

> Phase 1 · Module 05 · Functions

**TL;DR** — A construct signature uses `new` to describe a class-like value: `new (args) => Instance`.

## Syntax
```ts
type Ctor = {
  new (param: Type): InstanceType;
};
```

## Examples
### Basic
```ts
type PointCtor = {
  new (x: number, y: number): { x: number; y: number };
};

const Point: PointCtor = class {
  constructor(public x: number, public y: number) {}
};

const p = new Point(1, 2);
console.log(p.x, p.y); // 1 2
```

### Practical
```ts
type Ctor<T> = new (...args: any[]) => T;

function create<T>(C: Ctor<T>, ...args: ConstructorParameters<Ctor<T>>): T {
  return new C(...args);
}

class User {
  constructor(public name: string) {}
}

const u = create(User, "Ada");
console.log(u.name); // "Ada"
```

### Advanced / edge cases
```ts
// Distinguish callable from constructable
type Factory = {
  (): string;
  new (): { value: string };
};

// ✅ abstract construct signatures cannot be `new`-ed directly
type AbstractCtor<T> = abstract new (...args: any[]) => T;
declare const Base: AbstractCtor<{ id: number }>;
```

## Key points
- `new (...) => T` types values usable with `new`.
- Construct signatures do not describe ordinary calls.
- `ConstructorParameters` and `InstanceType` extract from a constructor type.
- Generic constructors are written with a type parameter list after `new`.

## Gotchas
- `// ❌ Error:` a plain arrow function does not satisfy a construct signature.
- `// ❌ Error:` `type C = new () => number; const c: C = () => 1;` — arrows are not constructors.
- Abstract classes need `abstract new`, not `new`.

## Best practice
- Use `new (...args: any[]) => T` for generic constructor constraints.
- Prefer class types (`typeof MyClass`) when the exact class is known.
