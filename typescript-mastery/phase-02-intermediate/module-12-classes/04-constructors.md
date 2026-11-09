# Constructors

> Phase 2 · Module 12 · Classes

**TL;DR** — A constructor initializes a new instance, runs once per `new`, and cannot declare a return type other than the instance.

## Syntax
```ts
class C {
  constructor(args) {
    // initialization
  }
}
```

## Examples
### Basic
```ts
class Timer {
  startedAt: number;

  constructor() {
    this.startedAt = Date.now();
  }
}

const timer = new Timer();
console.log(timer.startedAt > 0); // true
```

### Practical
```ts
class Email {
  readonly address: string;

  constructor(address: string) {
    const trimmed = address.trim();
    if (!trimmed.includes("@")) {
      throw new Error("Invalid email address");
    }
    this.address = trimmed;
  }
}

const email = new Email(" ada@example.com ");
console.log(email.address); // ada@example.com
```

### Advanced / edge cases
```ts
class Connection {
  private constructor(readonly url: string) {}

  static open(url: string): Connection {
    if (!url.startsWith("wss://")) {
      throw new Error("Secure connections only");
    }
    return new Connection(url);
  }
}

const conn = Connection.open("wss://api.example.com");
console.log(conn.url); // wss://api.example.com

// ❌ Error: Constructor of class 'Connection' is private.
// const direct = new Connection("wss://api.example.com");

class Point {
  constructor(public x = 0, public y = 0, ...tags: string[]) {
    void tags;
  }
}

new Point(); // ✅ defaults
new Point(1, 2); // ✅ positional args
```

## Key points
- Constructors run after field initializers and before the instance is returned.
- A constructor cannot specify a return type annotation.
- `private` or `protected` constructors control how instances are created.
- Parameters can have defaults, optional markers, and rest elements.
- Throwing inside a constructor aborts creation and propagates the error.

## Gotchas
- A constructor that throws does not leave a usable instance behind.
- Returning an object from a constructor overrides the instance at runtime but is not expressible via a return type.
- Subclass constructors must call `super()` before using `this`.

## Best practice
- Validate inputs in the constructor so an instance is always valid.
- Use static factory methods with a private constructor when creation needs extra logic.
