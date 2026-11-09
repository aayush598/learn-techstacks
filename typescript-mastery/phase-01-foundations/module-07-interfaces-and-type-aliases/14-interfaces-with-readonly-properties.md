# Interfaces with Readonly Properties

> Phase 1 · Module 07 · Interfaces and Type Aliases

**TL;DR** — `readonly` prevents reassignment of a property after creation, while still allowing reads.

## Syntax
```ts
interface Post {
  readonly id: string;
  readonly tags: readonly string[];
}
```

## Examples
### Basic
```ts
interface Point {
  readonly x: number;
  readonly y: number;
}

const p: Point = { x: 1, y: 2 };
console.log(p.x); // ✅ read

// ❌ Error: Cannot assign to 'x' because it is a read-only property
// p.x = 10;
```

### Practical
```ts
interface Config {
  readonly apiUrl: string;
  readonly retries: number;
}

const config: Config = { apiUrl: "https://api.test", retries: 3 };

function buildUrl(config: Config, path: string): string {
  return `${config.apiUrl}${path}`;
}

// Readonly arrays reject mutation methods.
interface Tags {
  readonly values: readonly string[];
}

const tags: Tags = { values: ["ts", "types"] };
// ❌ Error: Property 'push' does not exist on type 'readonly string[]'
// tags.values.push("js");
```

### Advanced / edge cases
```ts
interface Account {
  readonly id: string;
  owner: { name: string };
}

const account: Account = { id: "a1", owner: { name: "Ada" } };

// ❌ Error: read-only id
// account.id = "a2";

account.owner.name = "Grace"; // ✅ readonly is shallow

// Readonly<T> makes the top level readonly, not nested objects.
type FrozenAccount = Readonly<Account>;
const frozen: FrozenAccount = { id: "a3", owner: { name: "Lin" } };
frozen.owner.name = "Kai"; // ✅ still allowed
```

## Key points
- `readonly` blocks assignment through that property reference.
- It is a compile-time constraint only; JavaScript still mutates the object.
- `readonly T[]` prevents array mutation methods.
- `Readonly<T>` applies readonly to each top-level property.
- Readonly is shallow unless you apply it recursively.

## Gotchas
- `// ❌ Error:` `tags.values.push("js")` on a `readonly string[]`.
- `readonly` does not freeze nested objects.
- Readonly properties are still structurally assignable to mutable ones, so the guarantee is not enforced across all boundaries.

## Best practice
- Mark identifiers, timestamps, and configuration values `readonly`.
- Accept `readonly T[]` in functions that do not mutate their input.
