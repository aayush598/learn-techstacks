# Class inheritance

> Phase 2 · Module 12 · Classes

**TL;DR** — Inheritance lets a subclass reuse and extend a base class, modeling an `is-a` relationship.

## Syntax
```ts
class Base {
  method(): void {}
}

class Derived extends Base {
  extra(): void {}
}
```

## Examples
### Basic
```ts
class Animal {
  constructor(protected name: string) {}

  speak(): string {
    return `${this.name} makes a sound`;
  }
}

class Dog extends Animal {
  override speak(): string {
    return `${this.name} barks`;
  }
}

const dog = new Dog("Rex");
console.log(dog.speak()); // Rex barks
console.log(dog instanceof Animal); // true
```

### Practical
```ts
class HttpError extends Error {
  constructor(
    message: string,
    readonly status: number,
  ) {
    super(message);
    this.name = "HttpError";
  }
}

class NotFoundError extends HttpError {
  constructor(resource: string) {
    super(`${resource} not found`, 404);
    this.name = "NotFoundError";
  }
}

function fail(): never {
  throw new NotFoundError("User");
}

try {
  fail();
} catch (error) {
  if (error instanceof HttpError) {
    console.log(error.status); // 404
  }
}
```

### Advanced / edge cases
```ts
class Collection<T> {
  protected items: T[] = [];

  add(item: T): void {
    this.items.push(item);
  }

  get size(): number {
    return this.items.length;
  }
}

class Numbers extends Collection<number> {
  sum(): number {
    return this.items.reduce((a, b) => a + b, 0);
  }
}

const numbers = new Numbers();
numbers.add(1);
numbers.add(2);
console.log(numbers.sum(), numbers.size); // 3 2

// ❌ Error: Classes can only extend a single class.
// class Multiple extends Animal, Collection<number> {}
```

## Key points
- A subclass inherits all public and protected members of its base.
- `protected` members are usable in subclasses; `private` members are not.
- Instances satisfy both the subclass and base class types.
- Overrides dispatch dynamically based on the instance's actual class.
- Inheritance chains are linear: only one base class is allowed.

## Gotchas
- Deep hierarchies become fragile when base-class internals change.
- Inheritance is an `is-a` claim; using it for code reuse often leads to wrong models.
- The base constructor runs before subclass field initializers.

## Best practice
- Inherit only when the subtype can substitute for the base everywhere.
- Prefer composition for `has-a` relationships and shared implementation.
