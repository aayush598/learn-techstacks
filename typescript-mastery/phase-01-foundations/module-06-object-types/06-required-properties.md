# Required Properties

> Phase 1 · Module 06 · Object Types and Object Properties

**TL;DR** — Every property is required by default, so the value must provide it explicitly.

## Syntax
```ts
type T = { key: string };
const value: T = { key: "value" }; // key cannot be omitted
```

## Examples
### Basic
```ts
type User = {
  id: string;
  name: string;
  active: boolean;
};

const user: User = { id: "u1", name: "Ada", active: true };

console.log(user.name);
```

### Practical
```ts
type Draft = { title?: string; body?: string };
type Post = Required<Draft>;

const post: Post = { title: "Hello", body: "World" };

console.log(post.title);
```

### Advanced / edge cases
```ts
type MaybeName = { name: string | undefined };

const present: MaybeName = { name: undefined }; // ✅ present but undefined
// const missing: MaybeName = {};              // ❌ Error: name is required

type Options = { retries?: number };

function withOptions(options: Required<Options>): number {
  return options.retries;
}

console.log(withOptions({ retries: 3 }));
```

## Key points
- Properties are required unless explicitly marked with `?`.
- `Required<T>` removes optionality from every top-level property.
- A required property can still hold `undefined` if its type includes it.
- Missing required properties are reported on the object literal.
- `Required<T>` is shallow; nested optional properties stay optional.

## Gotchas
- `// ❌ Error:` `const u: User = { name: "Ada" };` — `id` and `active` are missing.
- `// ❌ Error:` `const m: MaybeName = {};` — requiredness is about presence, not the value.
- `Required<T>` does not recurse into nested objects.

## Best practice
- Keep domain entities fully required; use separate `Input` or `Draft` types for partial data.
- Apply `Required<T>` at the point where defaults have already been resolved.
