# Constraints Using `keyof`

> Phase 2 · Module 11 · Generics

**TL;DR** — `K extends keyof T` restricts a key parameter to real keys of `T`, letting you return the precise `T[K]` type.

## Syntax
```ts
function get<T, K extends keyof T>(source: T, key: K): T[K] {
  return source[key];
}
```

## Examples
### Basic
```ts
const user = { id: "u1", name: "Ada" };

const id = get(user, "id");     // string
const name = get(user, "name"); // string

// ❌ Error: Argument of type '"age"' is not assignable to parameter of type '"id" | "name"'.
// get(user, "age");
```

### Practical
```ts
function pluck<T, K extends keyof T>(items: readonly T[], key: K): T[K][] {
  return items.map((item) => item[key]);
}

const users = [
  { id: "u1", name: "Ada", active: true },
  { id: "u2", name: "Grace", active: false },
];

const actives = pluck(users, "active"); // boolean[]
const names = pluck(users, "name");     // string[]
```

### Advanced / edge cases
```ts
function set<T, K extends keyof T>(target: T, key: K, value: T[K]): T {
  return { ...target, [key]: value };
}

const updated = set(user, "name", "Grace"); // { id: string; name: string }

type Keys<T> = keyof T;
type UserKey = Keys<typeof user>; // "id" | "name"

// Restrict to string keys when iterating.
function keysOf<T extends object>(value: T): Array<Extract<keyof T, string>> {
  return Object.keys(value) as Array<Extract<keyof T, string>>;
}

// ❌ Error: Argument of type 'number' is not assignable to parameter of type 'string'.
// set(user, "id", 1);
```

## Key points
- `keyof T` is the union of `T`'s keys.
- `K extends keyof T` guarantees `source[key]` is valid.
- `T[K]` is the precise value type for that key.
- It works with interfaces, type aliases, mapped types, and generics.
- `Extract<keyof T, string>` filters out symbol and number keys.

## Gotchas
- `keyof` can include `number` and `symbol`; string-only APIs need `Extract`.
- Index signatures make `keyof T` collapse to `string | number`.
- `// ❌ Error:` a literal key not present in `T` is rejected.

## Best practice
- Use `K extends keyof T` for typed accessors instead of returning a union.
- Return `T[K]` rather than widening to `T[keyof T]` when the key is known.
