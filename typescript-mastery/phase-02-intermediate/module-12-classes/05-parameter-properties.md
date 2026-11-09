# Parameter properties

> Phase 2 · Module 12 · Classes

**TL;DR** — Prefix a constructor parameter with an access modifier, `readonly`, or both to declare and assign a field in one place.

## Syntax
```ts
class C {
  constructor(
    public a: string,
    private b: number,
    protected c: boolean,
    readonly d: Date,
  ) {}
}
```

## Examples
### Basic
```ts
class Person {
  constructor(
    public name: string,
    public age: number,
  ) {}
}

const p = new Person("Ada", 36);
console.log(p.name, p.age); // Ada 36
```

### Practical
```ts
class Repository {
  constructor(
    private readonly baseUrl: string,
    private readonly fetchImpl: typeof fetch = fetch,
  ) {}

  async get<T>(path: string): Promise<T> {
    const res = await this.fetchImpl(`${this.baseUrl}${path}`);
    return (await res.json()) as T;
  }
}

const repo = new Repository("https://api.example.com");
void repo;
```

### Advanced / edge cases
```ts
class Base {
  constructor(
    public id: string,
    protected created = new Date(),
  ) {}
}

class Child extends Base {
  constructor(id: string) {
    super(id); // ✅ parameter properties assigned by super
  }

  describe(): string {
    return `${this.id} created ${this.created.toISOString()}`;
  }
}

class NotAProperty {
  constructor(name: string) {
    void name; // plain parameter, no field created
  }
}
```

## Key points
- Modifiers are `public`, `private`, `protected`, and `readonly`; they can be combined.
- The generated field is assigned before the constructor body runs.
- `readonly` alone is enough to create a parameter property.
- Parameter properties work in base and derived constructors.
- A parameter without a modifier remains an ordinary parameter.

## Gotchas
- `#private` names cannot be used as parameter properties.
- Removing a modifier silently turns the field into a local parameter, breaking `this.name` references.
- Parameter properties cannot be used in type-only constructs such as interfaces.

## Best practice
- Use parameter properties for small immutable inputs to cut boilerplate.
- Switch to explicit fields when initialization needs validation or transformation.
