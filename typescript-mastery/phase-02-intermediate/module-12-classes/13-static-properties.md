# Static properties

> Phase 2 · Module 12 · Classes

**TL;DR** — `static` properties belong to the class constructor itself and are shared across all instances.

## Syntax
```ts
class C {
  static field: Type = value;
}
```

## Examples
### Basic
```ts
class Counter {
  static count = 0;

  constructor() {
    Counter.count++;
  }
}

new Counter();
new Counter();
console.log(Counter.count); // 2
```

### Practical
```ts
class Connection {
  static readonly defaultTimeout = 5_000;
  static active = 0;

  constructor(readonly url: string) {
    Connection.active++;
  }

  close(): void {
    Connection.active--;
  }
}

const a = new Connection("wss://one");
const b = new Connection("wss://two");
console.log(Connection.active); // 2
a.close();
console.log(Connection.active); // 1
```

### Advanced / edge cases
```ts
class Registry {
  private static instances = new Map<string, Registry>();

  private constructor(readonly name: string) {}

  static create(name: string): Registry {
    const existing = Registry.instances.get(name);
    if (existing) return existing;
    const created = new Registry(name);
    Registry.instances.set(name, created);
    return created;
  }
}

const r1 = Registry.create("db");
const r2 = Registry.create("db");
console.log(r1 === r2); // true

class Base {
  static kind = "base";
}

class Derived extends Base {}

console.log(Derived.kind); // "base" — inherited through the constructor chain
```

## Key points
- Static members are accessed through the class, not through instances.
- All instances share the same static value.
- Private static members are accessible only inside the class body.
- Static properties are inherited by subclasses through the constructor prototype chain.
- Static initialization happens when the class is evaluated.

## Gotchas
- `this` inside a static context refers to the constructor, not an instance.
- Mutating a static property through a subclass can create a shadowing own property.
- Static members cannot reference class type parameters.

## Best practice
- Use static properties for constants and class-level counters, not shared mutable state.
- Prefer private static fields plus static methods to control access.
