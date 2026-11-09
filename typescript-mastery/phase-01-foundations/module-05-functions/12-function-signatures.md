# Function Signatures

> Phase 1 · Module 05 · Functions

**TL;DR** — A function signature is the shape `(params) => return` that any implementation must match.

## Syntax
```ts
type Sig = (param: Type) => ReturnType;
```

## Examples
### Basic
```ts
type Increment = (n: number) => number;

const inc: Increment = (n) => n + 1;

console.log(inc(1)); // 2
```

### Practical
```ts
type AsyncFetcher = (url: string, signal?: AbortSignal) => Promise<string>;

const fetchText: AsyncFetcher = async (url, signal) => {
  const res = await fetch(url, { signal });
  return res.text();
};
```

### Advanced / edge cases
```ts
// A signature can describe overloads via an intersection of signatures
type Parser = {
  (input: string): number;
  (input: number): number;
};

// ✅ parameter names in a signature are for documentation only
type Binary = (left: number, right: number) => number;
const add: Binary = (a, b) => a + b;
```

## Key points
- The signature is the contract; the implementation may rename parameters freely.
- Signatures appear in annotations, type aliases, interface members, and overloads.
- Optional and rest positions are part of the signature.
- `void` in a signature means the return value is not to be used.

## Gotchas
- Parameter names in a signature are not checked against the implementation.
- `// ❌ Error:` `const f: (n: number) => number = (n: string) => 1;` — parameter types disagree.
- A signature returning `void` still accepts functions returning a value.

## Best practice
- Name parameters in a signature to document intent.
- Reuse a named signature type instead of repeating inline shapes.
