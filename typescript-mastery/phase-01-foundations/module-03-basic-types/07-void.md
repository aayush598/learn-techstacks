# void

> Phase 1 · Module 03 · Basic Types

**TL;DR** — `void` is the return type of functions that do not return a useful value.

## Syntax
```ts
function log(message: string): void {
  console.log(message);
}

const handler: () => void = () => {};
```

## Examples
### Basic
```ts
function ping(): void {
  console.log("ping");
}

const result: void = ping();
console.log(result); // undefined
```

### Practical
```ts
type Listener = (event: string) => void;

const listeners: Listener[] = [
  (event) => console.log(`A: ${event}`),
  (event) => console.log(`B: ${event}`),
];

function emit(event: string): void {
  listeners.forEach((listener) => listener(event));
}

emit("save"); // ✅
```

### Advanced / edge cases
```ts
// A void callback may ignore the return value of a function that returns something
const log: () => void = () => 42; // ✅ allowed by design

// void is not the same as undefined in a union
type A = void;
type B = undefined;
const a: A = undefined; // ✅
const b: B = undefined; // ✅

// Async functions return Promise<void>, not void
async function save(): Promise<void> {
  await Promise.resolve();
}

console.log(a, b, log(), save());
```

## Key points
- `void` signals "return value intentionally ignored".
- A `() => void` target accepts functions returning anything.
- `undefined` is assignable to `void`; the reverse is not.
- Async void work is really `Promise<void>`.
- Use `void` for side-effect functions and event handlers.

## Gotchas
- `void` is not a value you can read.
  ```ts
  function f(): void {}
  // ❌ Error: An expression of type 'void' cannot be tested for truthiness.
  // if (f()) {}
  ```
- Returning a value from a `void` function is an error.
  ```ts
  // ❌ Error: Type 'number' is not assignable to type 'void'.
  // function bad(): void { return 1; }
  ```
- Do not type async functions as `void`.
  ```ts
  // ❌ Error: Type 'Promise<void>' is not assignable to type 'void'.
  // const p: void = save();
  ```

## Best practice
- Use `void` for callbacks whose result is ignored.
- Use `Promise<void>` for async functions with no return value.
