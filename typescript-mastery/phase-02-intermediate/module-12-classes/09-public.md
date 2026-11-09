# `public`

> Phase 2 · Module 12 · Classes

**TL;DR** — `public` is the default visibility marking a member as part of the class's accessible surface.

## Syntax
```ts
class C {
  public field: string = "value";
  public method(): void {}
}
```

## Examples
### Basic
```ts
class User {
  public name: string;
  public role: "admin" | "member" = "member";

  constructor(name: string) {
    this.name = name;
  }

  public greet(): string {
    return `Hi ${this.name}`;
  }
}

const user = new User("Ada");
user.role = "admin"; // ✅ public mutable member
console.log(user.greet());
```

### Practical
```ts
class ApiClient {
  public constructor(public readonly baseUrl: string) {}

  public get(path: string): Promise<Response> {
    return fetch(`${this.baseUrl}${path}`);
  }

  public async json<T>(path: string): Promise<T> {
    const res = await this.get(path);
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    return (await res.json()) as T;
  }
}

const client = new ApiClient("https://api.example.com");
console.log(client.baseUrl); // https://api.example.com
```

### Advanced / edge cases
```ts
class Counter {
  public count = 0; // same as no modifier

  public increment(): void {
    this.count++;
  }
}

const c = new Counter();
c.count = 10; // ✅ public fields are writable unless readonly
c.increment();
console.log(c.count); // 11

class Config {
  public constructor(public readonly name: string) {}
}
const config = new Config("app");
// ❌ Error: Cannot assign to 'name' because it is a read-only property.
// config.name = "other";
```

## Key points
- Omitting a modifier is exactly equivalent to writing `public`.
- Public members form the structural type used for compatibility checks.
- Public does not imply immutable; combine with `readonly` when needed.
- Explicit `public` can document intended API surface.
- Public constructor parameters become public fields via parameter properties.

## Gotchas
- Public mutable fields expose internals and invite invalid states.
- Changing or removing a public member is a breaking API change.
- `public` provides no runtime protection, only compile-time visibility.

## Best practice
- Use explicit `public` on API-facing members to signal intent.
- Prefer `public readonly` or accessor methods over writable public fields.
