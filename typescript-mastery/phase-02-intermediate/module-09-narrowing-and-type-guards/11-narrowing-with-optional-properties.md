# Narrowing with optional properties

> Phase 2 · Module 09 · Type Narrowing and Type Guards

**TL;DR** — Optional properties are `T | undefined`, so you must narrow the property itself before using it.

## Syntax
```ts
type User = { name: string; email?: string };
```

## Examples
### Basic
```ts
type User = { name: string; email?: string };

function contact(user: User): string {
  if (user.email !== undefined) {
    return user.email; // ✅ string
  }
  return "no email"; // ✅ undefined branch
}
```

### Practical
```ts
type Config = { host?: string; port?: number };

function endpoint(config: Config): string {
  const host = config.host ?? "localhost"; // ✅ string
  const port = config.port ?? 8080; // ✅ number
  return `http://${host}:${port}`;
}
```

### Advanced / edge cases
```ts
type Payload = { id: string; meta?: { tags?: string[] } };

function tags(payload: Payload): string[] {
  const meta = payload.meta;
  if (!meta) {
    return []; // ✅ meta is undefined
  }
  return meta.tags ?? []; // ✅ tags is string[] | undefined
}

type WithRequired<T, K extends keyof T> = T & Required<Pick<T, K>>;

function assertEmail(user: User): WithRequired<User, "email"> {
  if (user.email === undefined) {
    throw new Error("email required");
  }
  return user as WithRequired<User, "email">;
}
```

## Key points
- `prop?: T` is exactly `prop: T | undefined` (plus optionality).
- `!== undefined`, `!= null`, `??`, and truthiness all narrow optionals.
- `exactOptionalPropertyTypes` changes whether `undefined` may be assigned.
- Nested optionals need each level checked.
- `Required<Pick<T, K>>` expresses a narrowed shape.

## Gotchas
- `in` only checks presence, not that the value is defined.
- Truthiness also rejects `0` and `""`, not just `undefined`.
- `// ❌ Error:` `user.email.toLowerCase()` without a guard under `strictNullChecks`.

## Best practice
- Use `??` for defaults on optional values.
- Prefer `!= null` when both `null` and `undefined` should be excluded.
