# Best Practices for Reusable Contracts

> Phase 1 · Module 07 · Interfaces and Type Aliases

**TL;DR** — Reusable contracts stay small, compose from focused pieces, accept readonly inputs, and express outcomes as discriminated unions.

## Syntax
```ts
interface Entity {
  readonly id: string;
}

interface Timestamped {
  readonly createdAt: Date;
}

type Combined = Entity & Timestamped;
type Outcome<T> = { ok: true; value: T } | { ok: false; error: string };
```

## Examples
### Basic
```ts
interface Entity {
  readonly id: string;
}

interface Timestamped {
  readonly createdAt: Date;
  readonly updatedAt: Date;
}

interface User extends Entity, Timestamped {
  readonly name: string;
}
```

### Practical
```ts
interface Entity {
  readonly id: string;
}

interface User extends Entity {
  readonly name: string;
}

interface Repository<T extends Entity> {
  find(id: string): Promise<T | undefined>;
  list(): Promise<readonly T[]>;
  save(entity: T): Promise<T>;
}

type QueryResult<T> =
  | { status: "ok"; items: readonly T[] }
  | { status: "error"; message: string };

async function loadUsers(
  repository: Repository<User>
): Promise<QueryResult<User>> {
  try {
    return { status: "ok", items: await repository.list() };
  } catch (error) {
    return {
      status: "error",
      message: error instanceof Error ? error.message : "unknown error",
    };
  }
}
```

### Advanced / edge cases
```ts
// Accept readonly input; return a new value instead of mutating.
function sortByName<T extends { readonly name: string }>(
  items: readonly T[]
): T[] {
  return [...items].sort((a, b) => a.name.localeCompare(b.name));
}

// Constrain generics only as much as the implementation needs.
interface Cache<TKey extends string, TValue> {
  get(key: TKey): TValue | undefined;
  set(key: TKey, value: TValue): void;
}

// Compile-time assignability checks document intended relationships.
type Assert<T extends true> = T;
type IsAssignable<From, To> = [From] extends [To] ? true : false;

interface User {
  readonly id: string;
  readonly name: string;
}

interface Admin extends User {
  permissions: readonly string[];
}

type AdminIsUser = Assert<IsAssignable<Admin, User>>; // ✅

// Validate literals without widening them.
interface RetryOptions {
  retries: number;
  timeoutMs: number;
}

const defaults = { retries: 3, timeoutMs: 1_000 } satisfies RetryOptions;
```

## Key points
- One contract should have one reason to change.
- Compose small interfaces instead of building deep hierarchies.
- Accept `readonly` arrays and objects; return fresh values.
- Use discriminated unions for success and failure.
- Constrain generics only where the implementation reads those members.
- Prefer `unknown` at boundaries, then narrow explicitly.

## Gotchas
- Over-general contracts with many optional fields are hard to satisfy and easy to misuse.
- `// ❌ Error:` `function save(items: T[])` rejects callers holding a `readonly T[]`.
- Intersecting many wide contracts can produce unreadable types and `never` conflicts.

## Best practice
- Treat exported types as a compatibility promise and evolve them additively.
- Add a compile-time assignability check when one contract must remain a subtype of another.
