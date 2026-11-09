# Interfaces with Construct Signatures

> Phase 1 · Module 07 · Interfaces and Type Aliases

**TL;DR** — A construct signature uses `new` to describe a value that can be called with `new` and returns a typed instance.

## Syntax
```ts
interface Point {
  x: number;
  y: number;
}

interface PointConstructor {
  new (x: number, y: number): Point;
}
```

## Examples
### Basic
```ts
interface Point {
  x: number;
  y: number;
}

interface PointConstructor {
  new (x: number, y: number): Point;
}

class PointImpl implements Point {
  constructor(public x: number, public y: number) {}
}

const PointClass: PointConstructor = PointImpl; // ✅ classes have construct signatures
const point = new PointClass(1, 2);
```

### Practical
```ts
interface User {
  name: string;
}

interface UserConstructor {
  new (name: string): User;
}

function createUser(Ctor: UserConstructor, name: string): User {
  return new Ctor(name);
}

class Admin implements User {
  constructor(public name: string) {}
}

console.log(createUser(Admin, "Ada").name); // "Ada"
```

### Advanced / edge cases
```ts
interface User {
  name: string;
}

interface Entity {
  id: string;
}

type Ctor<T> = new (...args: never[]) => T;

class ConcreteEntity implements Entity {
  id = "e1";
}

function instantiate<T>(Ctor: Ctor<T>): T {
  return new Ctor();
}

console.log(instantiate(ConcreteEntity).id); // "e1"

// Abstract classes require an abstract construct signature.
type AbstractCtor<T> = abstract new (...args: never[]) => T;

// Construct and call signatures can coexist.
interface Factory {
  new (name: string): User;
  (name: string): User;
}
```

## Key points
- `new (...) => T` describes a constructor, not a plain function.
- Classes and `typeof Class` satisfy construct signatures.
- Construct signatures enable dependency injection and factories.
- Abstract classes need `abstract new`.
- `InstanceType<T>` extracts the instance type from a constructor type.

## Gotchas
- `// ❌ Error:` `const f: PointConstructor = (x, y) => ({ x, y });` — arrow functions are not constructable.
- A normal function signature `(...) => T` is not a construct signature.
- `new (...args: any[])` weakens type safety; prefer explicit parameters.

## Best practice
- Use construct signatures for factory parameters, not for concrete class types.
- Type constructor parameters narrowly so callers get useful errors.
