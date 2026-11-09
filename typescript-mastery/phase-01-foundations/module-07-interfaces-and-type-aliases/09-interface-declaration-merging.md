# Interface Declaration Merging

> Phase 1 · Module 07 · Interfaces and Type Aliases

**TL;DR** — Declaring the same interface name more than once merges all declarations into a single type.

## Syntax
```ts
interface Box {
  width: number;
}

interface Box {
  height: number;
}

// Box now has both width and height.
```

## Examples
### Basic
```ts
interface Box {
  width: number;
}

interface Box {
  height: number;
}

const box: Box = { width: 10, height: 20 }; // ✅ both members required
```

### Practical
```ts
interface Config {
  env: "dev" | "prod";
}

interface Config {
  apiUrl: string;
}

interface Config {
  retries?: number;
}

const config: Config = { env: "dev", apiUrl: "https://api.test" };
```

### Advanced / edge cases
```ts
interface Converter {
  convert(value: string): number;
}

interface Converter {
  convert(value: number): string;
}

// The two declarations merge into an overloaded method.
declare const converter: Converter;
const asNumber: number = converter.convert("42");
const asString: string = converter.convert(42);

// ❌ Error: Subsequent property declarations must have the same type
// interface Conflict { value: string }
// interface Conflict { value: number }
```

## Key points
- Multiple interface declarations with the same name merge.
- Members from every declaration are combined.
- Identical duplicate members are allowed.
- Same-named methods merge as overloads.
- Merging is resolved at compile time and emits no code.

## Gotchas
- `// ❌ Error:` merging declarations that give the same property different types.
- A type alias cannot merge: `// ❌ Error:` `type Box = {}; type Box = {};`
- Merging is scoped to a module; use module augmentation to merge across files.

## Best practice
- Use merging intentionally for extensible plugin or theme contracts.
- Avoid accidental merges by keeping type names specific and scoped.
