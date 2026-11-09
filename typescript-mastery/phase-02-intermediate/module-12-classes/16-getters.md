# Getters

> Phase 2 · Module 12 · Classes

**TL;DR** — Getters compute a value on read and expose it through property syntax.

## Syntax
```ts
class C {
  get name(): Type {
    return value;
  }
}
```

## Examples
### Basic
```ts
class Circle {
  constructor(private radius: number) {}

  get area(): number {
    return Math.PI * this.radius ** 2;
  }
}

const circle = new Circle(2);
console.log(circle.area.toFixed(2)); // 12.57
```

### Practical
```ts
class Temperature {
  constructor(private celsius = 0) {}

  get fahrenheit(): number {
    return (this.celsius * 9) / 5 + 32;
  }

  get isFreezing(): boolean {
    return this.celsius <= 0;
  }
}

const temp = new Temperature(100);
console.log(temp.fahrenheit); // 212
console.log(temp.isFreezing); // false
```

### Advanced / edge cases
```ts
interface Named {
  readonly name: string;
}

class Person implements Named {
  constructor(
    private first: string,
    private last: string,
  ) {}

  get name(): string {
    return `${this.first} ${this.last}`;
  }
}

const p = new Person("Ada", "Lovelace");
console.log(p.name); // Ada Lovelace
// ❌ Error: Cannot assign to 'name' because it is a read-only property.
// p.name = "Grace";

class Lazy {
  private cached?: string;

  get value(): string {
    this.cached ??= expensiveComputation();
    return this.cached;
  }
}

function expensiveComputation(): string {
  return "computed";
}

console.log(new Lazy().value); // computed
```

## Key points
- Getters take no parameters and must return a value.
- A getter without a setter is read-only from the outside.
- Getters can be inferred, but an explicit return type documents the contract.
- Getters participate in interface `readonly` properties.
- Accessors live on the prototype, like methods.

## Gotchas
- A getter that throws makes property access fail at runtime.
- Getter-side effects can make debugging and serialization surprising.
- A getter-only property still appears writable in some JavaScript tooling.

## Best practice
- Keep getters cheap and side-effect free; cache expensive derivations deliberately.
- Use getters to expose derived state without storing redundant fields.
