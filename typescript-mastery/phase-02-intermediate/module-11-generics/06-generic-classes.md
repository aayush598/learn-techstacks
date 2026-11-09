# Generic Classes

> Phase 2 · Module 11 · Generics

**TL;DR** — A generic class declares type parameters on the class so every instance method and field can use one shared element type.

## Syntax
```ts
class Box<T> {
  constructor(private value: T) {}

  get(): T {
    return this.value;
  }
}
```

## Examples
### Basic
```ts
class Box<T> {
  constructor(private value: T) {}

  get(): T {
    return this.value;
  }

  set(value: T): void {
    this.value = value;
  }
}

const box = new Box(42); // Box<number>
box.set(7);
const value = box.get(); // number
```

### Practical
```ts
class Stack<T> {
  private readonly items: T[] = [];

  push(item: T): void {
    this.items.push(item);
  }

  pop(): T | undefined {
    return this.items.pop();
  }

  peek(): T | undefined {
    return this.items.at(-1);
  }

  get size(): number {
    return this.items.length;
  }
}

const stack = new Stack<string>();
stack.push("a");
const top = stack.peek(); // string | undefined
```

### Advanced / edge cases
```ts
class Collection<T> {
  private readonly items: T[];

  constructor(items: readonly T[] = []) {
    this.items = [...items];
  }

  map<U>(fn: (item: T) => U): Collection<U> {
    return new Collection(this.items.map(fn));
  }

  toArray(): T[] {
    return [...this.items];
  }

  static of<T>(...items: T[]): Collection<T> {
    return new Collection(items);
  }
}

const lengths = Collection.of("a", "bb").map((word) => word.length);
// Collection<number>

// ❌ Error: Static members cannot reference class type parameters.
// class Broken<T> {
//   static create(value: T): Broken<T> {
//     return new Broken(value);
//   }
// }
```

## Key points
- Class type parameters are visible in instance fields, methods, and accessors.
- Static members cannot use the class type parameters; declare their own.
- `new Box(42)` infers `Box<number>` from the constructor argument.
- Generic classes can implement generic interfaces.
- Nested generic methods may add their own parameters (`map<U>`).

## Gotchas
- `// ❌ Error:` using `T` inside a static method (TS2302).
- A class cannot declare type parameters directly on its constructor.
- Runtime code cannot check `T`; use a value or constructor reference instead.

## Best practice
- Keep type parameters on the class only when state itself is generic.
- Use static factories with their own `<T>` when construction needs inference.
