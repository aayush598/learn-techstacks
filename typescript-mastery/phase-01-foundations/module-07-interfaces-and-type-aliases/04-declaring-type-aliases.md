# Declaring Type Aliases

> Phase 1 · Module 07 · Interfaces and Type Aliases

**TL;DR** — Declare a type alias with `type`, an `=` sign, and any type expression on the right-hand side.

## Syntax
```ts
export type Id = string | number;
export type CacheEntry<T> = { value: T; expiresAt: number };
```

## Examples
### Basic
```ts
type Id = string | number;
type Point = { x: number; y: number };
type Pair = [number, number];

const id: Id = "abc";
const point: Point = { x: 1, y: 2 };
const pair: Pair = [1, 2];
```

### Practical
```ts
export type Handler = (event: Event) => void;

export type CacheEntry<T> = {
  value: T;
  expiresAt: number;
};

export function readCache<T>(entry: CacheEntry<T>, now: number): T | undefined {
  return now < entry.expiresAt ? entry.value : undefined;
}

const entry: CacheEntry<string> = { value: "hello", expiresAt: Date.now() + 1000 };
console.log(readCache(entry, Date.now()));
```

### Advanced / edge cases
```ts
interface User {
  id: string;
  name: string;
}

// Alias an existing interface
type Account = User;

// Alias a tuple with labels
type Range = [start: number, end: number];

// Alias a union of function signatures
type Listener = ((value: string) => void) | ((value: number) => void);

// Alias a utility result
type PublicUser = Omit<User, "id"> & { readonly id: string };

const publicUser: PublicUser = { id: "u1", name: "Ada" };
```

## Key points
- The right side can be any type expression.
- Aliases can be exported, generic, and parameterized with defaults.
- An alias can point at an interface, another alias, or a utility type.
- Aliases do not emit runtime code.
- Aliases are best for unions, tuples, functions, and computed types.

## Gotchas
- `// ❌ Error:` `type User = { name: string }; type User = { age: number };` — aliases cannot be redeclared.
- `// ❌ Error:` `type Status = "on" | "off"; interface Status {}` — a type alias and interface with the same name conflict.
- A self-reference needs a structural break: `type T = T[]` is fine, `type T = T` is not.

## Best practice
- Keep the alias body readable; extract nested pieces into named aliases.
- Use `export type` for types only, so consumers do not import runtime values.
