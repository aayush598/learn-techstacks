# `protected`

> Phase 2 · Module 12 · Classes

**TL;DR** — `protected` allows access inside the declaring class and its subclasses, but not from outside code.

## Syntax
```ts
class Base {
  protected field: string = "shared";
}
```

## Examples
### Basic
```ts
class Shape {
  protected constructor(protected readonly name: string) {}

  describe(): string {
    return this.name;
  }
}

class Circle extends Shape {
  constructor(readonly radius: number) {
    super("circle");
  }

  area(): number {
    return Math.PI * this.radius ** 2;
  }
}

console.log(new Circle(2).describe()); // circle
// ❌ Error: Constructor of class 'Shape' is protected.
// new Shape("shape");
```

### Practical
```ts
abstract class Exporter {
  protected abstract serialize(): string;

  protected header(): string {
    return "--- export ---";
  }

  run(): string {
    return `${this.header()}\n${this.serialize()}`;
  }
}

class JsonExporter extends Exporter {
  constructor(private readonly data: unknown) {
    super();
  }

  protected serialize(): string {
    return JSON.stringify(this.data);
  }
}

console.log(new JsonExporter({ ok: true }).run());
```

### Advanced / edge cases
```ts
class Base {
  protected value = 1;
}

class Derived extends Base {
  read(): number {
    return this.value; // ✅ through this
  }

  compare(other: Base): number {
    // ❌ Error: Property 'value' is protected and only accessible
    // through an instance of class 'Derived'.
    // return this.value - other.value;
    return this.value;
  }
}

const d = new Derived();
// ❌ Error: Property 'value' is protected and only accessible within
// class 'Base' and its subclasses.
// d.value;
```

## Key points
- Protected members are visible in the declaring class and all subclasses.
- Protected constructors prevent direct instantiation while allowing extension.
- Access through an instance is limited to instances of the current class or below.
- Protected members affect class compatibility nominally, like private members.
- Protected is compile-time only and erased at runtime.

## Gotchas
- A subclass cannot read a protected member through a base-typed reference.
- Protected does not make a member safe from runtime inspection.
- Reducing visibility from protected to private in a subclass is an error.

## Best practice
- Use protected for extension points intended for subclasses, not for general helpers.
- Prefer composition or protected abstract methods over exposing mutable protected state.
