# Recursive Type Aliases

> Phase 1 · Module 07 · Interfaces and Type Aliases

**TL;DR** — A recursive type alias refers to itself inside its definition, enabling JSON-like data, trees, and deeply computed types.

## Syntax
```ts
type List<T> = { value: T; next: List<T> | null };
```

## Examples
### Basic
```ts
type Json =
  | string
  | number
  | boolean
  | null
  | Json[]
  | { [key: string]: Json };

const value: Json = {
  name: "Ada",
  tags: ["ts", "types"],
  meta: { active: true, score: null },
};
```

### Practical
```ts
type Tree<T> = {
  value: T;
  children: Tree<T>[];
};

const tree: Tree<number> = {
  value: 1,
  children: [
    { value: 2, children: [] },
    { value: 3, children: [{ value: 4, children: [] }] },
  ],
};

function sum(node: Tree<number>): number {
  return node.value + node.children.reduce((total, child) => total + sum(child), 0);
}

console.log(sum(tree)); // 10
```

### Advanced / edge cases
```ts
type DeepPartial<T> = {
  [K in keyof T]?: T[K] extends object ? DeepPartial<T[K]> : T[K];
};

type DeepReadonly<T> = {
  readonly [K in keyof T]: T[K] extends (infer U)[]
    ? readonly DeepReadonly<U>[]
    : T[K] extends object
      ? DeepReadonly<T[K]>
      : T[K];
};

interface Config {
  port: number;
  db: { host: string; credentials: { user: string } };
}

const partial: DeepPartial<Config> = { db: { host: "localhost" } };

type FrozenConfig = DeepReadonly<Config>;
declare const frozen: FrozenConfig;
// ❌ Error: Cannot assign to 'host' because it is a read-only property
// frozen.db.host = "remote";
```

## Key points
- Recursion needs a structural break: array, object, or union member.
- Recursive aliases are erased at runtime.
- They power `Json`, tree, linked-list, and deep utility types.
- Conditional recursion distributes over unions and object members.
- Depth is bounded by the compiler's recursion limits.

## Gotchas
- `// ❌ Error:` `type T = T;` — a direct self-reference with no structure.
- `type T = T | string` is also circular and invalid.
- Deeply recursive conditional types can slow down checking or hit instantiation limits.

## Best practice
- Prefer interfaces for plain recursive object shapes and aliases for recursive unions.
- Add a depth guard or a non-recursive fallback for very deep utilities.
