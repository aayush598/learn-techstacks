# Numeric Literal Types

> Phase 1 · Module 03 · Basic Types

**TL;DR** — A numeric literal type pins a value to one exact number, useful for status codes, priorities, and flags.

## Syntax
```ts
type StatusCode = 200 | 201 | 400 | 404 | 500;
type Priority = 1 | 2 | 3;

let code: 200 = 200;
```

## Examples
### Basic
```ts
const ok: 200 = 200;
const notFound: 404 = 404;
console.log(ok, notFound); // ✅

// ❌ Error: Type '201' is not assignable to type '200'.
// const wrong: 200 = 201;
```

### Practical
```ts
type Priority = 1 | 2 | 3;

function label(priority: Priority): string {
  switch (priority) {
    case 1:
      return "low";
    case 2:
      return "medium";
    case 3:
      return "high";
  }
}

console.log(label(1), label(3)); // ✅
// ❌ Error: Argument of type '4' is not assignable to parameter of type 'Priority'.
// label(4);
```

### Advanced / edge cases
```ts
// Numeric literals work in tuple and object positions
type Version = { major: 1; minor: 0 | 1 | 2 };
const v: Version = { major: 1, minor: 2 }; // ✅

// Computed numeric constants need `as const` to stay literal
const LIMIT = 10 as const; // 10, not number

// Negative and floating literals are allowed
type Tuning = -1 | 0 | 0.5 | 1;
const t: Tuning = 0.5; // ✅

console.log(v, LIMIT, t);
```

## Key points
- Numeric literal types accept exactly one numeric value.
- They are erased at runtime; only the value remains.
- Unions of numeric literals model small finite sets well.
- Negative, zero, and fractional literals are valid.
- Numeric literals combine naturally with discriminated unions.

## Gotchas
- Arithmetic on a literal widens to `number`.
  ```ts
  const a: 2 = 2;
  const b = a + 1; // number, not 3
  ```
- `let` widens numeric literals to `number`.
  ```ts
  let code = 200; // number
  ```
- Enum members and numeric literals are not interchangeable in both directions.
  ```ts
  // ❌ Error in strict enum contexts: number is not assignable to an enum.
  ```

## Best practice
- Prefer literal unions over `number` when only a few values are legal.
- Use `as const` to keep computed constants literal.
