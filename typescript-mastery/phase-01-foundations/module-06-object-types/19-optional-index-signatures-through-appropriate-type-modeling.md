# Optional Index Signatures Through Appropriate Type Modeling

> Phase 1 · Module 06 · Object Types and Object Properties

**TL;DR** — TypeScript has no optional index signature syntax, so model missing keys by including `undefined` in the value type.

## Syntax
```ts
type T = { [key: string]: number | undefined };
type P = Partial<Record<string, number>>;
```

## Examples
### Basic
```ts
type MaybeScores = Partial<Record<string, number>>;

const scores: MaybeScores = {};
scores["alice"] = 10;

// ✅ reading an absent key includes undefined
console.log(scores["bob"]);
```

### Practical
```ts
type Options = {
  [key: string]: string | undefined;
};

const options: Options = {};
options["color"] = "blue";
options["size"] = undefined;

const color = options["color"] ?? "default";
console.log(color);
```

### Advanced / edge cases
```ts
type Role = "admin" | "editor" | "viewer";
type RoleFlags = Partial<Record<Role, boolean>>;

const flags: RoleFlags = { admin: true };

console.log(flags.editor ?? false);
// ✅ `in` distinguishes an absent key from a present false value
console.log("admin" in flags, flags.admin ?? false);
```

## Key points
- `// ❌ Error:` `type T = { [key: string]?: number };` — `?` is not allowed on an index signature.
- Adding `| undefined` to the value type models keys that may be missing.
- `Partial<Record<K, V>>` is the idiomatic form for a fixed set of optional keys.
- Reading an optional index always requires handling `undefined`.
- The `in` operator checks presence without relying on the value.

## Gotchas
- `| undefined` permits a key to be present with an explicit `undefined` value.
- Without an `in` check you cannot tell "absent" from "present but undefined".
- `exactOptionalPropertyTypes` affects optional named properties, not index signatures.

## Best practice
- Use `Partial<Record<K, V>>` when the key set is known and finite.
- Use `{ [key: string]: V | undefined }` for dynamic dictionaries with missing keys.
