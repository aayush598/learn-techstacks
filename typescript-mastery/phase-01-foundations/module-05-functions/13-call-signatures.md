# Call Signatures

> Phase 1 · Module 05 · Functions

**TL;DR** — A call signature describes how an object can be invoked: `(args): Return`.

## Syntax
```ts
type Callable = {
  (param: Type): ReturnType;
};
```

## Examples
### Basic
```ts
type Greet = {
  (name: string): string;
};

const greet: Greet = (name) => `Hi, ${name}`;

console.log(greet("Ada")); // "Hi, Ada"
```

### Practical
```ts
type Counter = {
  (): number;
  reset(): void;
};

function makeCounter(): Counter {
  let n = 0;
  const c = (() => ++n) as Counter;
  c.reset = () => {
    n = 0;
  };
  return c;
}

const c = makeCounter();
c();
c.reset();
```

### Advanced / edge cases
```ts
// Multiple call signatures form an overload set on an object type
type Parse = {
  (input: string): number;
  (input: string, radix: number): number;
};

const parse: Parse = (input: string, radix: number = 10) => parseInt(input, radix);

// ✅ call signatures can coexist with ordinary properties
type Tagged = {
  (text: string): string;
  version: string;
};
```

## Key points
- A call signature lives inside an object/interface type.
- Multiple call signatures create overloads.
- Call signatures can mix with data properties and methods.
- Function type aliases are shorthand for a single call signature.

## Gotchas
- `// ❌ Error:` `type F = { (a: number): number; } ; const f: F = "x";` — a string is not callable.
- Attaching properties to a function requires a cast or declaration merging.
- Overload implementations must be compatible with every call signature.

## Best practice
- Use a call signature when the value is callable and also has properties.
- Keep overloads in one type so callers see a single contract.
