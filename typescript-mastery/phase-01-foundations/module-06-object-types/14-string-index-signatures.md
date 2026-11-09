# String Index Signatures

> Phase 1 · Module 06 · Object Types and Object Properties

**TL;DR** — `[key: string]: T` describes a dictionary whose string keys all map to `T`.

## Syntax
```ts
type Dict = { [key: string]: string };
type DictRecord = Record<string, string>;
```

## Examples
### Basic
```ts
type Dictionary = { [word: string]: string };

const dict: Dictionary = {};
dict["hello"] = "hola";
dict.hello = "hola"; // ✅ dot access uses the same index signature

console.log(dict["hello"]);
```

### Practical
```ts
type Env = Record<string, string>;

function readEnv(env: Env, key: string): string {
  return env[key] ?? "";
}

console.log(readEnv({ NODE_ENV: "development" }, "NODE_ENV"));
```

### Advanced / edge cases
```ts
type HeaderMap = {
  [name: string]: string | undefined;
};

const headers: HeaderMap = {};
headers["content-type"] = "application/json";
headers["x-trace"] = undefined;

const trace = headers["x-trace"] ?? "none";
console.log(trace);
```

## Key points
- The signature covers every string key, not just the ones currently present.
- Dot access and bracket access use the same signature.
- `Record<string, T>` is a shorthand for the same idea.
- Named properties must also be assignable to the index value type.
- Numeric keys are ultimately strings at runtime, but TypeScript tracks them separately.

## Gotchas
- `// ❌ Error:` `type Bad = { [key: string]: string; count: number };` — `count` violates the signature.
- Accessing a key that does not exist at runtime returns `undefined` even if the static type says `T`.
- Inherited names such as `toString` exist on ordinary objects, which can surprise `key in obj` checks.

## Best practice
- Use `Record<string, T>` for maps and `{ [key: string]: T | undefined }` when missing keys are normal.
- Validate keys at runtime rather than trusting the index signature to guarantee presence.
