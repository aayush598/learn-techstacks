# Interface Fundamentals

> Phase 1 · Module 07 · Interfaces and Type Aliases

**TL;DR** — An `interface` names the shape of an object, listing the properties and methods that any value of that type must have.

## Syntax
```ts
interface User {
  id: number;
  name?: string;
  readonly createdAt: Date;
  greet(message: string): string;
}
```

## Examples
### Basic
```ts
interface User {
  id: number;
  name: string;
}

const user: User = { id: 1, name: "Ada" }; // ✅

// ❌ Error: Property 'name' is missing
// const broken: User = { id: 2 };
```

### Practical
```ts
interface Product {
  readonly sku: string;
  name: string;
  price: number;
  discount?: number;
}

function totalPrice(product: Product): number {
  return product.price - (product.discount ?? 0);
}

const book: Product = { sku: "BK-1", name: "TypeScript", price: 40 };
console.log(totalPrice(book)); // 40
```

### Advanced / edge cases
```ts
interface Logger {
  level: "debug" | "info" | "error";
  log(message: string): void;
  child(scope: string): Logger;
}

const logger: Logger = {
  level: "info",
  log(message) {
    console.log(`[${this.level}] ${message}`);
  },
  child(scope) {
    return { ...this, log: (m: string) => this.log(`${scope}: ${m}`) };
  },
};

logger.child("db").log("connected"); // [info] db: connected
```

## Key points
- An interface describes structure, not an implementation.
- Every required member must be present on an assignable value.
- Optional members use `?`; readonly members use `readonly`.
- Methods can be written as `method(): T` or as a function-typed property.
- Interfaces are erased at runtime; they produce no JavaScript.

## Gotchas
- Extra properties are allowed on variables, but object literals are checked for excess properties.
- `// ❌ Error:` `const p: Product = { sku: "x", name: "n", price: 1, discount: "10" };` — wrong property type.
- An interface cannot describe a primitive or a union directly.

## Best practice
- Model each interface around one cohesive responsibility.
- Keep required members minimal; mark genuinely optional data with `?`.
