# `readonly`

> Phase 2 · Module 12 · Classes

**TL;DR** — `readonly` prevents reassignment after initialization and is enforced only by the type checker.

## Syntax
```ts
class C {
  readonly id: string = "fixed";
}
```

## Examples
### Basic
```ts
class Config {
  readonly env: string = "production";

  describe(): string {
    return this.env;
  }
}

const config = new Config();
console.log(config.env); // production
// ❌ Error: Cannot assign to 'env' because it is a read-only property.
// config.env = "development";
```

### Practical
```ts
class User {
  readonly id: string;
  readonly createdAt: Date;
  readonly roles: readonly string[];

  constructor(id: string, roles: string[] = []) {
    this.id = id;
    this.createdAt = new Date();
    this.roles = roles;
  }

  hasRole(role: string): boolean {
    return this.roles.includes(role);
  }
}

const user = new User("u1", ["admin"]);
console.log(user.hasRole("admin")); // true
```

### Advanced / edge cases
```ts
class MutableContents {
  readonly features: string[] = [];

  constructor(readonly appName: string) {
    // ✅ assignment to readonly is allowed in the constructor
    this.appName = appName;
  }

  add(feature: string): void {
    this.features.push(feature); // ✅ readonly reference, mutable array
    // ❌ Error: Cannot assign to 'features' because it is a read-only property.
    // this.features = [];
  }
}

const m = new MutableContents("app");
m.features = ["overwritten"]; // ❌ Error: read-only property
m.features.push("search"); // ✅ mutates the array contents
```

## Key points
- `readonly` can be applied to fields, parameter properties, and index signatures.
- Assignment is allowed inside the constructor but not afterward.
- `readonly` is shallow: referenced objects and arrays remain mutable.
- `readonly T[]` and `ReadonlyArray<T>` prevent mutating methods on the array itself.
- Readonly is erased at runtime and does not freeze objects.

## Gotchas
- `readonly` does not deep-freeze nested data.
- TypeScript treats readonly property compatibility as bidirectional, so it does not prevent all misuse.
- `Object.freeze` is required if runtime immutability is needed.

## Best practice
- Mark fields readonly by default and opt into mutation deliberately.
- Use `readonly` arrays in public APIs to prevent callers from mutating internal state.
