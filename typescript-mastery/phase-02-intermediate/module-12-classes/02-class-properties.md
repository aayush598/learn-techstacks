# Class properties

> Phase 2 · Module 12 · Classes

**TL;DR** — Instance properties hold per-object state and are declared in the class body, initialized inline or in the constructor.

## Syntax
```ts
class C {
  field: string = "value";
  optional?: number;
  definite!: boolean;
}
```

## Examples
### Basic
```ts
class Counter {
  count = 0;
  label = "clicks";
}

const c = new Counter();
c.count += 1;
console.log(c.count, c.label); // 1 clicks
```

### Practical
```ts
class ShoppingCart {
  items: string[] = [];
  total = 0;

  add(item: string, price: number): void {
    this.items.push(item);
    this.total += price;
  }
}

const cart = new ShoppingCart();
cart.add("Keyboard", 99);
cart.add("Mouse", 49);
console.log(cart.items, cart.total); // ["Keyboard", "Mouse"] 148
```

### Advanced / edge cases
```ts
class Config {
  name: string; // ✅ assigned in constructor
  retries = 3;
  cache?: Map<string, string>; // ✅ optional, undefined by default
  connection!: string; // ✅ definite assignment assertion

  constructor(name: string) {
    this.name = name;
  }
}

// ❌ Error: Property 'value' has no initializer and is not
// definitely assigned in the constructor.
// class Broken {
//   value: number;
// }
```

## Key points
- Properties declared without `static` belong to each instance.
- Inline initializers run before the constructor body executes.
- `optional?` implicitly includes `undefined` in the property type.
- `!` asserts definite assignment to the compiler and has no runtime effect.
- `declare` fields emit no JavaScript and exist only for type checking.

## Gotchas
- With `strictPropertyInitialization`, every non-optional field needs an initializer or constructor assignment.
- Using `!` silences the compiler but leaves the value `undefined` if nothing assigns it.
- Optional fields require null checks before use under `strictNullChecks`.

## Best practice
- Prefer inline initializers for simple defaults and the constructor for required inputs.
- Use `!` only for values assigned by a framework or external lifecycle, and document why.
