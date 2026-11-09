# Nested Object Types

> Phase 1 · Module 06 · Object Types and Object Properties

**TL;DR** — Object properties can themselves be object types, producing a tree that is checked level by level.

## Syntax
```ts
type Outer = {
  inner: {
    key: string;
  };
};
```

## Examples
### Basic
```ts
type Address = { street: string; city: string };
type User = { name: string; address: Address };

const user: User = {
  name: "Ada",
  address: { street: "1 Main St", city: "London" },
};

console.log(user.address.city);
```

### Practical
```ts
type Profile = {
  name: string;
  contact?: {
    email: string;
    phone?: string;
  };
};

function emailOf(profile: Profile): string | undefined {
  return profile.contact?.email;
}

console.log(emailOf({ name: "Ada" }));
```

### Advanced / edge cases
```ts
type DeepReadonly<T> = {
  readonly [K in keyof T]: T[K] extends object ? DeepReadonly<T[K]> : T[K];
};

type Config = DeepReadonly<{
  server: { host: string; ports: number[] };
}>;

const config: Config = { server: { host: "localhost", ports: [80, 443] } };

// config.server.ports[0] = 8080; // ❌ Error: nested array is read-only

console.log(config.server.ports[0]);
```

## Key points
- Nesting is just an object type used as a property type.
- Each level is checked independently against its declared shape.
- Optional nesting needs optional chaining to reach deep values safely.
- Readonly applies only to the level where it is declared.
- Deep transformations require recursive mapped or conditional types.

## Gotchas
- `readonly` on the outer property does not protect nested properties.
- `// ❌ Error:` `const u: User = { name: "Ada", address: { city: "London" } };` — `street` is missing.
- Recursive mapped types can break on built-ins such as `Date`, `Map`, and functions; add guards.

## Best practice
- Model nested data with small named types composed together rather than one giant literal.
- Keep optionality at the level where absence is actually possible.
