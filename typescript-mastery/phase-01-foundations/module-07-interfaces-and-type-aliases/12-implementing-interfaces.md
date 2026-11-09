# Implementing Interfaces

> Phase 1 · Module 07 · Interfaces and Type Aliases

**TL;DR** — A class uses `implements` to promise it satisfies an interface, and the compiler verifies every required member.

## Syntax
```ts
interface Clock {
  now(): Date;
}

class SystemClock implements Clock {
  now(): Date {
    return new Date();
  }
}
```

## Examples
### Basic
```ts
interface Clock {
  now(): Date;
}

class SystemClock implements Clock {
  now(): Date {
    return new Date();
  }
}

const clock: Clock = new SystemClock();
console.log(clock.now());
```

### Practical
```ts
interface Identifiable {
  readonly id: string;
}

interface Persistable {
  save(): Promise<void>;
}

class Entity implements Identifiable, Persistable {
  id: string; // ✅ readonly in the interface does not force readonly here

  constructor(id: string) {
    this.id = id;
  }

  async save(): Promise<void> {
    console.log(`saving ${this.id}`);
  }
}
```

### Advanced / edge cases
```ts
interface Repository<T extends { id: string }> {
  find(id: string): T | undefined;
  save(entity: T): void;
}

class InMemoryRepository<T extends { id: string }> implements Repository<T> {
  private readonly items = new Map<string, T>();

  find(id: string): T | undefined {
    return this.items.get(id);
  }

  save(entity: T): void {
    this.items.set(entity.id, entity);
  }
}

const users = new InMemoryRepository<{ id: string; name: string }>();
users.save({ id: "u1", name: "Ada" });
```

## Key points
- `implements` is a compile-time check only; it emits no runtime code.
- All required members must exist with compatible types.
- Optional interface members do not have to be implemented.
- A class can implement several interfaces.
- Generic interfaces can be implemented with the same type parameters.

## Gotchas
- `// ❌ Error:` `class Incomplete implements Clock {}` — missing `now`.
- `// ❌ Error:` implementing with a private member where the interface expects it public.
- A class cannot implement an interface that has only a call signature, because the class type is not callable.

## Best practice
- Program against interfaces, not concrete classes, at module boundaries.
- Keep implemented interfaces narrow so classes stay easy to test.
