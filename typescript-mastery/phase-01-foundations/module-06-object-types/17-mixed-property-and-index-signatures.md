# Mixed Property and Index Signatures

> Phase 1 · Module 06 · Object Types and Object Properties

**TL;DR** — Named properties and index signatures can coexist, but every named property must conform to the index value type.

## Syntax
```ts
type T = {
  known: string;
  [key: string]: string;
};
```

## Examples
### Basic
```ts
type User = {
  id: string;
  [key: string]: string;
};

const user: User = { id: "u1", name: "Ada", role: "admin" };

console.log(user.id, user["name"]);
```

### Practical
```ts
type Config = {
  version: number;
  [key: string]: number;
};

const config: Config = { version: 1, retries: 3, timeout: 5000 };

console.log(config.version, config["timeout"]);
```

### Advanced / edge cases
```ts
type Mixed = {
  [key: string]: string | number;
  [index: number]: number;
};

const mixed: Mixed = { version: 1, 0: 42 };

console.log(mixed[0], mixed["version"]);
```

## Key points
- Named properties must be assignable to the index signature's value type.
- A number index type must also be assignable to a coexisting string index type.
- Optional named properties include `undefined`, so the index type must include `undefined` too.
- Access through the index signature returns the index value type, not the specific named property type.
- Dot access and bracket access both use the same index signature rules.

## Gotchas
- `// ❌ Error:` `type T = { name?: string; [key: string]: string };` — `name` is `string | undefined`.
- `// ❌ Error:` `type T = { [key: string]: string; [index: number]: number };` — number values violate the string index.
- A named property does not override the index signature; it must be compatible with it.

## Best practice
- Include `undefined` in the index value type when named optional properties coexist with it.
- Keep the named properties few and semantically fixed; let the index signature handle dynamic keys.
