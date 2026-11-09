# `private`

> Phase 2 · Module 12 · Classes

**TL;DR** — `private` restricts member access to the declaring class at compile time and supports encapsulation of internal state.

## Syntax
```ts
class C {
  private field: string = "hidden";
  private method(): void {}
}
```

## Examples
### Basic
```ts
class Counter {
  private count = 0;

  increment(): void {
    this.count++;
  }

  get value(): number {
    return this.count;
  }
}

const c = new Counter();
c.increment();
console.log(c.value); // 1
// ❌ Error: Property 'count' is private and only accessible within class 'Counter'.
// c.count;
```

### Practical
```ts
class PasswordHasher {
  private readonly salt: string;

  constructor(salt: string) {
    if (salt.length < 8) throw new Error("Salt too short");
    this.salt = salt;
  }

  private mix(input: string): string {
    return `${this.salt}:${input}`;
  }

  hash(password: string): string {
    return this.mix(password).split("").reverse().join("");
  }
}

const hasher = new PasswordHasher("long-enough-salt");
console.log(hasher.hash("secret"));
```

### Advanced / edge cases
```ts
class Cache {
  private store = new Map<string, string>();

  private key(namespace: string, id: string): string {
    return `${namespace}:${id}`;
  }

  set(ns: string, id: string, value: string): void {
    this.store.set(this.key(ns, id), value);
  }

  get(ns: string, id: string): string | undefined {
    return this.store.get(this.key(ns, id));
  }
}

class A {
  private id = "a";
}

class B {
  private id = "b";
}

// ❌ Error: Property 'id' is private in type 'A' but not in type 'B'.
// const a: A = new B();
```

## Key points
- Private members are accessible only inside the declaring class body.
- Private members are still emitted to JavaScript and exist at runtime.
- A `private` member makes class compatibility nominal for that member.
- Private methods and static private members are supported.
- Constructors can be private to force factory-based creation.

## Gotchas
- `private` is not a runtime security boundary; casts and plain JavaScript can bypass it.
- Subclasses cannot access private members of their base class.
- Two classes with the same private member name are not interchangeable.

## Best practice
- Make internal state private and expose intention-revealing methods or accessors.
- Use ECMAScript `#private` when runtime privacy actually matters.
