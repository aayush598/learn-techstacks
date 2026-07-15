# Recursive Types in TypeScript

Recursive types are types that reference themselves. They enable modeling of deeply nested structures, trees, JSON data, and other self-referential data structures. TypeScript supports recursive type aliases, recursive conditional types, and recursive mapped types.

---

## Table of Contents

1. [Recursive Type Aliases](#recursive-type-aliases)
2. [Recursive Conditional Types](#recursive-conditional-types)
3. [Recursive Mapped Types](#recursive-mapped-types)
4. [Recursive Object Types](#recursive-object-types)
5. [Deep Readonly](#deep-readonly)
6. [Deep Partial](#deep-partial)
7. [Type-Safe Paths for Nested Objects](#type-safe-paths-for-nested-objects)
8. [JSON Type](#json-type)
9. [Recursive Tuple Types](#recursive-tuple-types)
10. [Tree Types](#tree-types)
11. [Best Practices](#best-practices)
12. [Interview Questions](#interview-questions)

---

## Recursive Type Aliases

A type alias is recursive when it references itself. This is useful for modeling naturally recursive data structures.

### Simple recursive type

```typescript
type NestedNumber = number | NestedNumber[];

type Matrix = NestedNumber[];
const matrix: Matrix = [1, [2, 3], [[4, 5], 6]];
```

### Linked list

```typescript
type LinkedList<T> = {
  value: T;
  next: LinkedList<T> | null;
};

const list: LinkedList<number> = {
  value: 1,
  next: {
    value: 2,
    next: {
      value: 3,
      next: null,
    },
  },
};
```

### Deeply nested object

```typescript
type NestedObject = {
  value: string;
  children: NestedObject[];
};

const tree: NestedObject = {
  value: "root",
  children: [
    { value: "child1", children: [] },
    { value: "child2", children: [{ value: "grandchild", children: [] }] },
  ],
};
```

### Recursive union type

```typescript
type Expression =
  | number
  | { op: "+" | "-" | "*" | "/"; left: Expression; right: Expression };

const expr: Expression = {
  op: "+",
  left: 1,
  right: { op: "*", left: 2, right: 3 },
};
```

---

## Recursive Conditional Types

Recursive conditional types use `extends` and reference themselves in either the true or false branch. These enable powerful type-level computations.

### Flatten nested arrays

```typescript
type FlattenDeep<T extends any[]> = T extends [infer Head, ...infer Rest]
  ? Head extends any[]
    ? [...FlattenDeep<Head>, ...FlattenDeep<Rest>]
    : [Head, ...FlattenDeep<Rest>]
  : T;

type A = FlattenDeep<[1, [2, 3], [4, [5, 6]]]>; // [1, 2, 3, 4, 5, 6]
type B = FlattenDeep<[[[[1]]]]>;                 // [1]
type C = FlattenDeep<[1, 2, 3]>;                 // [1, 2, 3]
```

### String to union

```typescript
type StringToUnion<T extends string> = T extends `${infer Head}${infer Rest}`
  ? Head | StringToUnion<Rest>
  : never;

type A = StringToUnion<"hello">; // "h" | "e" | "l" | "l" | "o"
```

### Replace all occurrences in a string

```typescript
type ReplaceAll<
  S extends string,
  From extends string,
  To extends string
> = From extends ""
  ? S
  : S extends `${infer Before}${From}${infer After}`
  ? `${Before}${To}${ReplaceAll<After, From, To>}`
  : S;

type A = ReplaceAll<"hello world world", "world", "universe">;
// "hello universe universe"
```

### String length

```typescript
type Length<S extends string> = S extends `${infer _Head}${infer Rest}`
  ? 1 + Length<Rest>
  : 0;

type A = Length<"hello">; // 5
type B = Length<"">;      // 0
```

### Deep equals

```typescript
type DeepEqual<A, B> = A extends B
  ? B extends A
    ? true
    : false
  : false;

type A = DeepEqual<{ a: string }, { a: string }>; // true
type B = DeepEqual<{ a: string }, { a: number }>; // false
```

### Tuple to union recursively

```typescript
type TupleToUnion<T extends any[]> = T extends [infer Head, ...infer Rest]
  ? Head | TupleToUnion<Rest>
  : never;

type A = TupleToUnion<[string, number, boolean]>; // string | number | boolean
```

---

## Recursive Mapped Types

Mapped types that transform deeply nested structures by recursing into each property.

### Deep mapped type

```typescript
type DeepMap<T, From, To> = T extends From
  ? To
  : T extends object
  ? { [K in keyof T]: DeepMap<T[K], From, To> }
  : T;

type Original = {
  name: string;
  data: {
    value: number;
    nested: { text: string };
  };
};

type Mapped = DeepMap<Original, string, string[]>;
// {
//   name: string[];
//   data: { value: number; nested: { text: string[] } };
// }
```

### Deep make all required

```typescript
type DeepRequired<T> = T extends object
  ? { [K in keyof T]-?: DeepRequired<T[K]> }
  : T;

type Config = {
  db?: { host?: string; port?: number };
  cache?: { ttl?: number };
};

type RequiredConfig = DeepRequired<Config>;
// { db: { host: string; port: number }; cache: { ttl: number } }
```

### Deep make all nullable

```typescript
type DeepNullable<T> = T extends object
  ? { [K in keyof T]: DeepNullable<T[K]> | null }
  : T | null;

type Config = { host: string; port: number };
type NullableConfig = DeepNullable<Config>;
// { host: string | null; port: number | null }
```

---

## Recursive Object Types

Modeling recursive data structures like trees, graphs, and linked lists.

### Binary tree

```typescript
type TreeNode<T> = {
  value: T;
  left: TreeNode<T> | null;
  right: TreeNode<T> | null;
};

const tree: TreeNode<number> = {
  value: 1,
  left: { value: 2, left: null, right: null },
  right: {
    value: 3,
    left: { value: 4, left: null, right: null },
    right: null,
  },
};
```

### Generic tree (n-ary)

```typescript
type Tree<T> = {
  value: T;
  children: Tree<T>[];
};

const menu: Tree<string> = {
  value: "root",
  children: [
    { value: "file", children: [{ value: "new", children: [] }] },
    { value: "edit", children: [{ value: "undo", children: [] }] },
  ],
};
```

### Nested comments (like Reddit)

```typescript
type Comment = {
  id: string;
  author: string;
  text: string;
  replies: Comment[];
};

const thread: Comment = {
  id: "1",
  author: "Alice",
  text: "Great post!",
  replies: [
    {
      id: "2",
      author: "Bob",
      text: "Thanks!",
      replies: [
        { id: "3", author: "Charlie", text: "I agree!", replies: [] },
      ],
    },
  ],
};
```

---

## Deep Readonly

Make all properties deeply readonly using recursive types.

```typescript
type DeepReadonly<T> = T extends (infer U)[]
  ? ReadonlyArray<DeepReadonly<U>>
  : T extends Map<infer K, infer V>
  ? ReadonlyMap<DeepReadonly<K>, DeepReadonly<V>>
  : T extends Set<infer V>
  ? ReadonlySet<DeepReadonly<V>>
  : T extends object
  ? { readonly [K in keyof T]: DeepReadonly<T[K]> }
  : T;

type Config = {
  db: { host: string; port: number };
  cache: { ttl: number; keys: string[] };
};

type ReadonlyConfig = DeepReadonly<Config>;
// {
//   readonly db: { readonly host: string; readonly port: number };
//   readonly cache: { readonly ttl: number; readonly keys: readonly string[] };
// }
```

### Usage with React state

```typescript
type AppState = {
  user: { name: string; preferences: { theme: string } };
  todos: { id: number; text: string }[];
};

type FrozenState = DeepReadonly<AppState>;
// All properties are readonly at all levels
```

---

## Deep Partial

Make all properties optional at all levels.

```typescript
type DeepPartial<T> = T extends object
  ? { [K in keyof T]?: DeepPartial<T[K]> }
  : T;

type Config = {
  db: { host: string; port: number; ssl: boolean };
  cache: { host: string; ttl: number };
};

type PartialConfig = DeepPartial<Config>;
// {
//   db?: { host?: string; port?: number; ssl?: boolean };
//   cache?: { host?: string; ttl?: number };
// }

// Usage: partial updates
function updateConfig(base: Config, overrides: DeepPartial<Config>): Config {
  return {
    db: { ...base.db, ...overrides.db },
    cache: { ...base.cache, ...overrides.cache },
  };
}

const updated = updateConfig(defaultConfig, {
  db: { port: 5432 }, // only override port
});
```

### Deep Partial with arrays

```typescript
type DeepPartial<T> = T extends (infer U)[]
  ? DeepPartial<U>[]
  : T extends object
  ? { [K in keyof T]?: DeepPartial<T[K]> }
  : T;
```

---

## Type-Safe Paths for Nested Objects

Generate type-safe dot-notation paths for deeply nested objects.

### Basic path generation

```typescript
type Path<T, Prefix extends string = ""> = T extends object
  ? {
      [K in keyof T & string]: T[K] extends object
        ? Path<T[K], `${Prefix}${K}.`>
        : `${Prefix}${K}`;
    }[keyof T & string]
  : Prefix;

type Config = {
  db: {
    host: string;
    port: number;
    ssl: { enabled: boolean };
  };
  cache: { ttl: number };
};

type ConfigPath = Path<Config>;
// "db" | "db.host" | "db.port" | "db.ssl" | "db.ssl.enabled" | "cache" | "cache.ttl"
```

### Type-safe get function

```typescript
type Get<T, Path extends string> = Path extends `${infer Head}.${infer Rest}`
  ? Head extends keyof T
    ? Get<T[Head], Rest>
    : never
  : Path extends keyof T
  ? T[Path]
  : never;

type Config = {
  db: { host: string; port: number };
  cache: { ttl: number };
};

type Host = Get<Config, "db.host">;     // string
type Ttl = Get<Config, "cache.ttl">;   // number

function get<T, P extends Path<T>>(obj: T, path: P): Get<T, P> {
  return path.split(".").reduce((obj: any, key) => obj[key], obj) as any;
}

const config: Config = { db: { host: "localhost", port: 5432 }, cache: { ttl: 3600 } };
const host = get(config, "db.host"); // string
const ttl = get(config, "cache.ttl"); // number
```

---

## JSON Type

A recursive type that represents valid JSON values.

```typescript
type JSONValue =
  | string
  | number
  | boolean
  | null
  | JSONValue[]
  | { [key: string]: JSONValue };

type JSONObject = { [key: string]: JSONValue };

const data: JSONValue = {
  name: "Alice",
  age: 30,
  address: { street: "123 Main St", city: "Springfield" },
  hobbies: ["reading", "gaming"],
  active: true,
  metadata: null,
};

// Parse JSON safely
function parseJSON<T extends JSONValue>(json: string): T {
  return JSON.parse(json) as T;
}

// Stringify JSON safely
function stringifyJSON<T extends JSONValue>(value: T): string {
  return JSON.stringify(value);
}
```

### Strict JSON type (no undefined, no functions)

```typescript
type StrictJSON =
  | string
  | number
  | boolean
  | null
  | StrictJSON[]
  | { [key: string]: StrictJSON };

function validateJSON(input: unknown): input is StrictJSON {
  if (input === null || typeof input === "string" || typeof input === "number" || typeof input === "boolean") {
    return true;
  }
  if (Array.isArray(input)) {
    return input.every(validateJSON);
  }
  if (typeof input === "object") {
    return Object.values(input).every(validateJSON);
  }
  return false;
}
```

---

## Recursive Tuple Types

### Build tuple of length N

```typescript
type BuildTuple<N extends number, T extends any[] = []> = T["length"] extends N
  ? T
  : BuildTuple<N, [...T, any]>;

type A = BuildTuple<3>; // [any, any, any]
type B = BuildTuple<0>; // []
```

### Add to tuple end

```typescript
type Push<T extends any[], V> = [...T, V];

type A = Push<[1, 2], 3>; // [1, 2, 3]
```

### Zip two tuples

```typescript
type Zip<A extends any[], B extends any[]> = A extends [infer AH, ...infer AR]
  ? B extends [infer BH, ...infer BR]
    ? [[AH, BH], ...Zip<AR, BR>]
    : []
  : [];

type A = Zip<[1, 2, 3], ["a", "b", "c"]>; // [[1, "a"], [2, "b"], [3, "c"]]
```

### Repeat type N times

```typescript
type Repeat<T, N extends number, Acc extends T[] = []> = Acc["length"] extends N
  ? Acc
  : Repeat<T, N, [...Acc, T]>;

type A = Repeat<string, 3>; // [string, string, string]
type B = Repeat<number, 0>; // []
```

---

## Tree Types

### File system tree

```typescript
type FileNode = {
  type: "file";
  name: string;
  size: number;
};

type DirectoryNode = {
  type: "directory";
  name: string;
  children: FileSystemNode[];
};

type FileSystemNode = FileNode | DirectoryNode;

const fs: DirectoryNode = {
  type: "directory",
  name: "src",
  children: [
    { type: "file", name: "index.ts", size: 1024 },
    {
      type: "directory",
      name: "components",
      children: [
        { type: "file", name: "Button.tsx", size: 2048 },
        { type: "file", name: "Input.tsx", size: 1024 },
      ],
    },
  ],
};
```

### Org chart

```typescript
type Employee = {
  name: string;
  title: string;
  reports: Employee[];
};

const org: Employee = {
  name: "CEO",
  title: "Chief Executive Officer",
  reports: [
    {
      name: "CTO",
      title: "Chief Technology Officer",
      reports: [
        { name: "Dev Lead", title: "Lead Developer", reports: [] },
        { name: "QA Lead", title: "QA Lead", reports: [] },
      ],
    },
    {
      name: "CFO",
      title: "Chief Financial Officer",
      reports: [],
    },
  ],
};
```

### Helper functions for tree types

```typescript
function mapTree<T, U>(node: Tree<T>, fn: (value: T) => U): Tree<U> {
  return {
    value: fn(node.value),
    children: node.children.map((child) => mapTree(child, fn)),
  };
}

function findInTree<T>(node: Tree<T>, predicate: (value: T) => boolean): Tree<T> | null {
  if (predicate(node.value)) return node;
  for (const child of node.children) {
    const found = findInTree(child, predicate);
    if (found) return found;
  }
  return null;
}

function flattenTree<T>(node: Tree<T>): T[] {
  return [node.value, ...node.children.flatMap(flattenTree)];
}
```

---

## Best Practices

1. **Use recursive types for naturally recursive data** — trees, linked lists, nested objects
2. **Use recursive conditional types for type-level computation** — string manipulation, tuple operations
3. **Use `DeepPartial` and `DeepReadonly`** — common patterns for nested objects
4. **Limit recursion depth** — TypeScript has limits (about 50 levels) to prevent infinite recursion
5. **Use tail recursion when possible** — helps TypeScript handle deep recursion
6. **Combine with `infer`** — for extracting types from recursive structures
7. **Test recursive types with simple cases first** — then add complexity

---

## Interview Questions

### Q1: What are recursive types in TypeScript?

**Answer:** Recursive types are types that reference themselves. They are used for modeling naturally recursive data structures like trees, linked lists, and nested objects. TypeScript supports recursive type aliases, recursive conditional types, and recursive mapped types.

### Q2: How do you create a deep Partial type?

**Answer:** Use a recursive mapped type: `type DeepPartial<T> = T extends object ? { [K in keyof T]?: DeepPartial<T[K]> } : T`. This makes all properties optional at every level of nesting.

### Q3: What are the limits of recursive types?

**Answer:** TypeScript has a recursion depth limit (approximately 50 levels). If you exceed this, the compiler may fail or produce unexpected results. Tail-recursive types help mitigate this issue.

### Q4: How do you represent JSON in TypeScript?

**Answer:** Use a recursive union type: `type JSONValue = string | number | boolean | null | JSONValue[] | { [key: string]: JSONValue }`. This represents all valid JSON values.

### Q5: How do you generate type-safe paths for nested objects?

**Answer:** Use recursive template literal types to build dot-notation paths: `type Path<T> = T extends object ? { [K in keyof T & string]: T[K] extends object ? \`${K}.${Path<T[K]>}\` : K }[keyof T & string] : never`. Then use a `get` function with those paths.

### Q6: Can you use recursive types with mapped types?

**Answer:** Yes. Recursive mapped types apply transformations at every level of a nested structure. For example, `DeepReadonly<T>` recursively applies the `readonly` modifier to all properties at all levels.
