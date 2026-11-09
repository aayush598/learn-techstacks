# Interfaces with Call Signatures

> Phase 1 · Module 07 · Interfaces and Type Aliases

**TL;DR** — A call signature makes an interface describe something callable, with typed parameters and a return type.

## Syntax
```ts
interface Formatter {
  (value: number): string;
}
```

## Examples
### Basic
```ts
interface Formatter {
  (value: number): string;
}

const format: Formatter = (value) => value.toFixed(2);

console.log(format(3.14159)); // "3.14"
```

### Practical
```ts
interface Counter {
  (start?: number): number;
  count: number;
  reset(): void;
}

const counter = Object.assign(
  (start = 0) => ++counter.count,
  { count: 0, reset: () => { counter.count = 0; } }
) as Counter;

console.log(counter()); // 1
console.log(counter(10)); // 2
counter.reset();
```

### Advanced / edge cases
```ts
interface Parse {
  (input: string): number;
  (input: number): string;
}

function parse(input: string): number;
function parse(input: number): string;
function parse(input: string | number): number | string {
  return typeof input === "string" ? Number(input) : String(input);
}

const parseFn: Parse = parse; // ✅ overloads satisfy the call signatures

console.log(parseFn("42")); // 42
console.log(parseFn(42)); // "42"
```

## Key points
- Call signatures are written like a function type without a name.
- An interface can combine a call signature with properties and methods.
- Multiple call signatures describe overloads.
- Function declarations with overloads satisfy the interface.
- Call signatures are structural; any compatible function works.

## Gotchas
- `// ❌ Error:` `class Handler implements Formatter { }` — a class type is not callable.
- `// ❌ Error:` assigning a function with the wrong return type: `const f: Formatter = (v) => v;`
- A bare function type alias and a call-signature interface are mostly interchangeable; interfaces add merging.

## Best practice
- Use a call-signature interface when the callable also carries properties.
- Use a function type alias when you only need the signature.
