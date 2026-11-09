# Boolean Literal Types

> Phase 1 · Module 03 · Basic Types

**TL;DR** — `true` and `false` are types too, and unions of them power discriminated unions and exhaustive checks.

## Syntax
```ts
let yes: true = true;
let no: false = false;
type Bit = true | false; // equivalent to boolean
```

## Examples
### Basic
```ts
const isReady: true = true;
const isDone: false = false;
console.log(isReady, isDone); // ✅

// ❌ Error: Type 'false' is not assignable to type 'true'.
// const wrong: true = false;
```

### Practical
```ts
type Result<T> =
  | { success: true; data: T }
  | { success: false; error: string };

function unwrap<T>(result: Result<T>): T {
  if (result.success) {
    return result.data; // ✅ narrowed to success: true
  }
  throw new Error(result.error);
}

console.log(unwrap({ success: true, data: 42 })); // ✅
```

### Advanced / edge cases
```ts
// Boolean literals as discriminants in nested unions
type Loading =
  | { state: "loading"; loading: true }
  | { state: "done"; loading: false; value: string };

function view(l: Loading): string {
  return l.loading ? "spinner" : l.value; // ✅ narrowed by `loading`
}

// `true | false` collapses to boolean
type Bit = true | false;
const b: Bit = false; // ✅

console.log(view({ state: "done", loading: false, value: "ok" }), b);
```

## Key points
- `true` and `false` are distinct singleton types.
- `boolean` is exactly `true | false`.
- Boolean literal fields make great discriminants.
- A `true` annotation cannot hold `false`.
- Narrowing on a boolean literal property works like any discriminant.

## Gotchas
- A `boolean` value is not assignable to a `true` annotation.
  ```ts
  const flag: boolean = true;
  // ❌ Error: Type 'boolean' is not assignable to type 'true'.
  // const t: true = flag;
  ```
- Comparisons widen results to `boolean`.
  ```ts
  const a: true = true;
  const same = a === true; // boolean
  ```
- Using `true | false` instead of `boolean` is usually redundant.

## Best practice
- Use boolean literal discriminants in `Result`-style unions.
- Just write `boolean` when both values are valid.
