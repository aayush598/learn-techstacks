# `extends`

> Phase 2 · Module 12 · Classes

**TL;DR** — `extends` links a derived class to exactly one base class or built-in constructor through the prototype chain.

## Syntax
```ts
class Derived extends Base {
  // ...
}
```

## Examples
### Basic
```ts
class Vehicle {
  constructor(protected wheels: number) {}

  describe(): string {
    return `A vehicle with ${this.wheels} wheels`;
  }
}

class Bike extends Vehicle {
  constructor() {
    super(2);
  }
}

console.log(new Bike().describe()); // A vehicle with 2 wheels
```

### Practical
```ts
class ValidationError extends Error {
  constructor(
    message: string,
    readonly field: string,
  ) {
    super(message);
    this.name = "ValidationError";
  }
}

function assertPositive(value: number): void {
  if (value <= 0) {
    throw new ValidationError("Must be positive", "value");
  }
}

try {
  assertPositive(-1);
} catch (error) {
  if (error instanceof ValidationError) {
    console.log(error.field); // value
  }
}
```

### Advanced / edge cases
```ts
const Base = class {
  hello(): string {
    return "hello";
  }
};

class Derived extends Base {}

console.log(new Derived().hello()); // hello

class GenericBase<T> {
  constructor(protected value: T) {}

  get(): T {
    return this.value;
  }
}

class StringBox extends GenericBase<string> {
  upper(): string {
    return this.value.toUpperCase();
  }
}

console.log(new StringBox("abc").upper()); // ABC
```

## Key points
- `extends` accepts a class or any constructor expression, not an interface.
- The derived class inherits instance and static members.
- You must call `super()` in a derived constructor before touching `this`.
- A class can extend only one base class.
- `extends` works with generic base classes by supplying type arguments.

## Gotchas
- Extending built-ins such as `Error` and `Array` requires a modern compile target for correct behavior.
- A derived constructor without `super()` is a compile error.
- Extending an expression evaluates that expression at class definition time.

## Best practice
- Extend your own domain base classes rather than built-ins when possible.
- Use interfaces plus `implements` when you need shared shape without implementation.
