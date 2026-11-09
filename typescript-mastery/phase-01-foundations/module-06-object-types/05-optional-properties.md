# Optional Properties

> Phase 1 · Module 06 · Object Types and Object Properties

**TL;DR** — Mark a property with `?` when it may be absent, and handle the resulting `undefined`.

## Syntax
```ts
type T = { required: string; optional?: number };
```

## Examples
### Basic
```ts
type User = {
  name: string;
  nickname?: string;
};

const a: User = { name: "Ada" };
const b: User = { name: "Grace", nickname: "Amazing Grace" };

// ✅ reading an optional property yields string | undefined
console.log(a.nickname?.toUpperCase() ?? "none");
```

### Practical
```ts
type SearchOptions = {
  query: string;
  limit?: number;
  caseSensitive?: boolean;
};

function search(options: SearchOptions): string {
  const limit = options.limit ?? 10;
  return `${options.query} (${limit})`;
}

console.log(search({ query: "typescript" }));
```

### Advanced / edge cases
```ts
type Config = {
  readonly retries?: number;
  nested?: { enabled?: boolean };
};

const config: Config = { nested: {} };

// ✅ optional chaining composes through nested optionals
console.log(config.retries ?? 3, config.nested?.enabled ?? false);
```

## Key points
- `?` means the property may be missing from the object.
- Under `strict`, reading an optional property includes `undefined` in its type.
- Optional properties can also be `readonly`.
- Optional chaining (`?.`) and nullish coalescing (`??`) are the usual consumers.
- Optional is independent of the property's value type.

## Gotchas
- Optional is not the same as nullable: `null` still needs an explicit `| null`.
- `// ❌ Error:` `const u: User = { name: "Ada", nickname: null };` — `null` is not allowed.
- With `exactOptionalPropertyTypes`, `{ nickname: undefined }` is rejected because the property must be absent, not present with `undefined`.

## Best practice
- Use `?` only when absence is a valid state; use `| null` for an explicit null value.
- Normalize optional values once at the boundary with `??` or a default.
