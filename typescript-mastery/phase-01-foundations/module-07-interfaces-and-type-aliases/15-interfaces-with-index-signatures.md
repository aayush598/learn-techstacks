# Interfaces with Index Signatures

> Phase 1 · Module 07 · Interfaces and Type Aliases

**TL;DR** — An index signature describes a type with an arbitrary number of keys of a given kind, all mapping to the same value type.

## Syntax
```ts
interface Scores {
  [name: string]: number;
}

interface StringList {
  [index: number]: string;
}
```

## Examples
### Basic
```ts
interface Scores {
  [name: string]: number;
}

const scores: Scores = { ada: 10, grace: 20 };
scores["lin"] = 30; // ✅
console.log(scores.ada);
```

### Practical
```ts
interface Environment {
  NODE_ENV: "development" | "production";
  [key: string]: string;
}

const env: Environment = {
  NODE_ENV: "development",
  API_URL: "https://api.test",
};

// Numeric keys describe array-like objects.
interface StringList {
  [index: number]: string;
}

const list: StringList = ["a", "b", "c"];
```

### Advanced / edge cases
```ts
interface Hybrid {
  [key: string]: string | number;
  name: string; // ✅ assignable to string | number
  length: number;
}

interface ReadonlyDict {
  readonly [key: string]: string;
}

const dict: ReadonlyDict = { a: "1" };
// ❌ Error: Index signature in type 'ReadonlyDict' only permits reading
// dict.a = "2";

// Record is the utility-type equivalent.
type Flags = Record<string, boolean>;
const flags: Flags = { dark: true, beta: false };
```

## Key points
- String index signatures type all string-keyed access.
- Number index signatures type numeric access, such as array indices.
- Named properties must be assignable to the index signature type.
- Index signatures allow adding keys after creation.
- `Record<K, V>` is often clearer than a bare index signature.

## Gotchas
- `// ❌ Error:` `interface Bad { [key: string]: number; name: string }` — `name` is not a `number`.
- With `noUncheckedIndexedAccess`, lookups produce `T | undefined`.
- An index signature also permits keys like `"toString"`, so inherited members can collide.

## Best practice
- Prefer `Record<K, V>` for fixed key unions and index signatures for open maps.
- Enable `noUncheckedIndexedAccess` and handle missing keys explicitly.
