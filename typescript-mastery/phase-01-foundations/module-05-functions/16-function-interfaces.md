# Function Interfaces

> Phase 1 · Module 05 · Functions

**TL;DR** — An interface can describe a callable value using a call signature, and it can be extended and merged.

## Syntax
```ts
interface Fn {
  (param: Type): ReturnType;
}
```

## Examples
### Basic
```ts
interface Stringify {
  (value: number): string;
}

const stringify: Stringify = (value) => String(value);

console.log(stringify(42)); // "42"
```

### Practical
```ts
interface Comparator<T> {
  (a: T, b: T): number;
}

const byLength: Comparator<string> = (a, b) => a.length - b.length;

console.log(["ccc", "a", "bb"].sort(byLength)); // ["a", "bb", "ccc"]
```

### Advanced / edge cases
```ts
// Interfaces with call signatures can also hold properties
interface Logger {
  (msg: string): void;
  level: "info" | "warn";
}

interface Comparator<T> {
  (a: T, b: T): number;
}

// ✅ interfaces can extend other interfaces and add data
interface NamedComparator<T> extends Comparator<T> {
  name: string;
}

const byLengthNamed: NamedComparator<string> = Object.assign(
  (a: string, b: string) => a.length - b.length,
  { name: "length" }
);

console.log(byLengthNamed.name); // "length"
```

## Key points
- An interface with only a call signature is a function type.
- Interfaces can be extended and declaration-merged.
- Properties and call signatures can coexist.
- Interface call signatures support overloads naturally.

## Gotchas
- `// ❌ Error:` `interface F { (n: number): number } const f: F = (s: string) => 1;` — parameter mismatch.
- Interfaces cannot be used as values; they are types only.
- Declaration merging can add members you did not intend in one file.

## Best practice
- Prefer interfaces for extendable public contracts; use type aliases for unions.
- Keep callable interfaces focused; move extra data into separate fields.
