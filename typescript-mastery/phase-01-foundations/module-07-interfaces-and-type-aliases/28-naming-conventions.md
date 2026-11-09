# Naming Conventions

> Phase 1 · Module 07 · Interfaces and Type Aliases

**TL;DR** — Name types in `PascalCase`, describe the concept rather than the syntax, and avoid `I` prefixes and cryptic abbreviations.

## Syntax
```ts
interface ButtonProps {
  label: string;
}

type UserId = string;
```

## Examples
### Basic
```ts
// ✅ PascalCase, no prefix
interface User {
  id: string;
  name: string;
}

type UserId = string;

// ❌ Hungarian and snake_case
// interface IUser {}
// type user_id = string;
```

### Practical
```ts
// ✅ Role suffixes communicate intent
interface ButtonProps {
  label: string;
  onClick: () => void;
}

interface RequestOptions {
  readonly timeoutMs: number;
}

interface CacheEntry<T> {
  value: T;
  expiresAt: number;
}

type LoadResult<T> =
  | { ok: true; value: T }
  | { ok: false; error: string };

type EventHandler<T> = (event: T) => void;
```

### Advanced / edge cases
```ts
interface User {
  id: string;
  name: string;
}

// ✅ Generic parameters: short but meaningful
function first<T>(items: readonly T[]): T | undefined {
  return items[0];
}

interface Repository<TEntity extends { id: string }, TKey = string> {
  find(key: TKey): TEntity | undefined;
}

// ✅ Map and dictionary names describe the key-value relationship
type UserById = Readonly<Record<string, User>>;
type ModuleName = "auth" | "billing" | "reports";

// ❌ Names that restate the type
// type StringType = string;
// type ArrayOfUsers = User[];

// ❌ A `T` prefix on a concrete interface is misleading
// interface TUser {}
```

## Key points
- Use `PascalCase` for interfaces, aliases, and generic arguments.
- Do not prefix interfaces with `I`; it adds noise and no safety.
- Suffix by role: `Props`, `Options`, `Config`, `State`, `Result`, `Handler`.
- Use `T`, `K`, `V`, or `TValue` for type parameters, not concrete types.
- Prefer full domain words over abbreviations.

## Gotchas
- `// ❌ Error:` naming a type the same as an unrelated value in the same scope can shadow or merge unexpectedly.
- `T` prefixes imply a type parameter; `TUser` confuses readers.
- Casing-only differences (`User` vs `user`) are easy to mix up in imports.

## Best practice
- Read the name aloud; if it does not describe the domain concept, rename it.
- Keep a short suffix vocabulary in the project style guide and stick to it.
