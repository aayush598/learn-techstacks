# Method overriding

> Phase 2 · Module 12 · Classes

**TL;DR** — A subclass overrides a base method by redeclaring it with a compatible signature to change behavior polymorphically.

## Syntax
```ts
class Derived extends Base {
  override method(args): ReturnType {
    // replacement implementation
  }
}
```

## Examples
### Basic
```ts
class Animal {
  speak(): string {
    return "...";
  }
}

class Cat extends Animal {
  override speak(): string {
    return "meow";
  }
}

const animals: Animal[] = [new Animal(), new Cat()];
console.log(animals.map((a) => a.speak())); // ["...", "meow"]
```

### Practical
```ts
class PaymentProcessor {
  process(amount: number): string {
    return `Charged ${amount}`;
  }
}

class RefundProcessor extends PaymentProcessor {
  override process(amount: number): string {
    return `Refunded ${amount}`;
  }
}

function settle(processor: PaymentProcessor, amount: number): string {
  return processor.process(amount); // dynamic dispatch
}

console.log(settle(new RefundProcessor(), 50)); // Refunded 50
```

### Advanced / edge cases
```ts
class Base {
  create(): object {
    return {};
  }
}

class Derived extends Base {
  override create(): { id: string } {
    return { id: "1" }; // ✅ covariant return type
  }
}

class Parent {
  greet(): string {
    return "hi";
  }
}

class Child extends Parent {
  // ❌ Error: Property 'greet' is private in type 'Child' but not in type 'Parent'.
  // private greet(): string { return "hi"; }
}

class Wrapper extends Parent {
  override greet(): string {
    return `${super.greet()} from child`; // ✅ reuse base behavior
  }
}

console.log(new Wrapper().greet()); // hi from child
```

## Key points
- The override must remain assignable to the base method signature.
- Return types may be narrowed covariantly.
- Access modifiers cannot become more restrictive.
- `super.method()` calls the base implementation.
- Dispatch is dynamic based on the runtime instance type.

## Gotchas
- Arrow-function fields shadow base methods instead of overriding the prototype method.
- Static members are hidden, not overridden.
- Changing a method to an incompatible signature breaks substitutability.

## Best practice
- Add `override` to every overriding member for clarity and safety.
- Call `super` only when extending base behavior, not when replacing it entirely.
