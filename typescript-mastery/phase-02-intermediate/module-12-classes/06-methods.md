# Methods

> Phase 2 · Module 12 · Classes

**TL;DR** — Methods are functions on the class prototype that operate on the instance through `this`.

## Syntax
```ts
class C {
  method(args): ReturnType {
    // body
  }
}
```

## Examples
### Basic
```ts
class Greeter {
  constructor(private name: string) {}

  greet(): string {
    return `Hello, ${this.name}`;
  }

  greetLoudly(): string {
    return this.greet().toUpperCase();
  }
}

console.log(new Greeter("Ada").greetLoudly()); // HELLO, ADA
```

### Practical
```ts
class Inventory {
  private stock = new Map<string, number>();

  add(sku: string, qty: number): void {
    this.stock.set(sku, (this.stock.get(sku) ?? 0) + qty);
  }

  remove(sku: string, qty: number): boolean {
    const current = this.stock.get(sku) ?? 0;
    if (current < qty) return false;
    this.stock.set(sku, current - qty);
    return true;
  }

  quantity(sku: string): number {
    return this.stock.get(sku) ?? 0;
  }
}
```

### Advanced / edge cases
```ts
class Counter {
  count = 0;

  increment(): void {
    this.count++;
  }
}

const c = new Counter();
const inc = c.increment;
// inc(); // ❌ runtime TypeError: this is undefined in strict mode

const bound = c.increment.bind(c); // ✅ explicit binding
bound();
console.log(c.count); // 1

class SafeCounter {
  count = 0;
  increment = (): void => {
    this.count++; // ✅ arrow captures the instance
  };
}

const safe = new SafeCounter();
const safeInc = safe.increment;
safeInc();
console.log(safe.count); // 1
```

## Key points
- Methods live on the prototype and are shared across instances.
- `this` is determined by the call site, not by where the method was defined.
- Arrow-function fields capture `this` and become per-instance properties.
- Methods support optional, default, and rest parameters.
- Methods can be overloaded and can be generic.

## Gotchas
- Passing a method as a callback loses its `this` binding.
- Arrow-function fields are copied per instance and increase memory use.
- Methods and own properties with the same name collide.

## Best practice
- Use normal methods for shared behavior; use arrow fields only when binding is required.
- Keep methods focused on one responsibility and avoid deep chains of `this` mutation.
