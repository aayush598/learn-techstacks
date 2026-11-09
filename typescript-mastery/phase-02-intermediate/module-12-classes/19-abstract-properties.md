# Abstract properties

> Phase 2 · Module 12 · Classes

**TL;DR** — Abstract properties declare required fields on a base class without providing storage or a value.

## Syntax
```ts
abstract class Base {
  abstract readonly id: string;
}
```

## Examples
### Basic
```ts
abstract class Entity {
  abstract readonly id: string;

  describe(): string {
    return `Entity ${this.id}`;
  }
}

class User extends Entity {
  constructor(readonly id: string) {
    super();
  }
}

console.log(new User("u1").describe()); // Entity u1
```

### Practical
```ts
abstract class Widget {
  abstract title: string;
  abstract render(): string;
}

class Button extends Widget {
  title = "Submit";

  render(): string {
    return `<button>${this.title}</button>`;
  }
}

class Input extends Widget {
  title = "Name";

  render(): string {
    return `<input aria-label="${this.title}" />`;
  }
}

console.log(new Button().render());
console.log(new Input().render());
```

### Advanced / edge cases
```ts
abstract class Record {
  abstract readonly createdAt: Date;

  ageInDays(): number {
    return (Date.now() - this.createdAt.getTime()) / 86_400_000;
  }
}

class Order extends Record {
  readonly createdAt = new Date();
  constructor(readonly id: string) {
    super();
  }
}

abstract class Bad {
  // ❌ Error: 'abstract' property cannot have an initializer.
  // abstract status: string = "idle";

  abstract get label(): string; // ✅ abstract accessor
}

class Good extends Bad {
  get label(): string {
    return "good";
  }
}
```

## Key points
- Abstract properties declare a required shape without allocating storage.
- Concrete subclasses must provide the property or accessor.
- Abstract properties can be `readonly` or mutable.
- Abstract getters and setters use the same `abstract` modifier.
- Abstract properties can drive concrete base-class behavior.

## Gotchas
- An abstract property does not exist on the base class at runtime.
- Abstract properties cannot have initializers.
- Optional abstract properties still require compatible implementation on subclasses.

## Best practice
- Use abstract properties for invariants every subclass must expose, such as an `id`.
- Prefer readonly abstract properties when subclasses should not reassign them.
