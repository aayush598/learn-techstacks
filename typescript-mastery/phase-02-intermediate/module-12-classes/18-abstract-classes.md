# Abstract classes

> Phase 2 · Module 12 · Classes

**TL;DR** — Abstract classes cannot be instantiated and may declare members that concrete subclasses must implement.

## Syntax
```ts
abstract class Base {
  abstract method(): Type;
  concrete(): void {}
}
```

## Examples
### Basic
```ts
abstract class Shape {
  abstract area(): number;

  describe(): string {
    return `Area: ${this.area().toFixed(2)}`;
  }
}

class Square extends Shape {
  constructor(private side: number) {
    super();
  }

  area(): number {
    return this.side ** 2;
  }
}

console.log(new Square(3).describe()); // Area: 9.00
// ❌ Error: Cannot create an instance of an abstract class.
// new Shape();
```

### Practical
```ts
abstract class Repository {
  abstract findById(id: string): Promise<string | undefined>;

  async exists(id: string): Promise<boolean> {
    return (await this.findById(id)) !== undefined;
  }
}

class MemoryRepository extends Repository {
  private items = new Map<string, string>();

  async findById(id: string): Promise<string | undefined> {
    return this.items.get(id);
  }

  async save(id: string, value: string): Promise<void> {
    this.items.set(id, value);
  }
}

const repo = new MemoryRepository();
await repo.save("1", "value");
console.log(await repo.exists("1")); // true
```

### Advanced / edge cases
```ts
abstract class Worker {
  protected constructor(readonly name: string) {}

  abstract run(): void;

  start(): void {
    this.run(); // ✅ calls the subclass implementation
  }
}

class Job extends Worker {
  constructor() {
    super("job");
  }

  run(): void {
    console.log("running");
  }
}

class NotAbstract {
  // ❌ Error: Abstract methods can only appear within an abstract class.
  // abstract run(): void;
}
```

## Key points
- Abstract classes can mix implemented and unimplemented members.
- `abstract` members have no body and must be implemented by concrete subclasses.
- Abstract classes can have constructors and can implement interfaces.
- A class with any abstract member must itself be abstract.
- Abstract classes are useful as base classes and as parameter types.

## Gotchas
- Abstractness is compile-time only and erased at runtime.
- A subclass inherits the obligation to implement abstract members unless it is also abstract.
- You cannot use `new` on an abstract class even through a concrete-looking variable.

## Best practice
- Use abstract classes for shared implementation plus enforced extension points.
- Keep the abstract surface small and expose behavior through concrete methods.
