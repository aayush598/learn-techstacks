# Result Type Pattern in TypeScript

## Table of Contents

- [Overview](#overview)
- [Result Type Implementation](#result-type-implementation)
- [Ok/Error Pattern](#okerror-pattern)
- [Railway-Oriented Programming](#railway-oriented-programming)
- [Result with Generics](#result-with-generics)
- [Matching on Result](#matching-on-result)
- [Result vs Exceptions](#result-vs-exceptions)
- [neverthrow Library](#neverthrow-library)
- [fp-ts Either Pattern](#fp-ts-either-pattern)
- [Best Practices](#best-practices)
- [Interview Questions](#interview-questions)

---

## Overview

The Result type is a functional programming pattern that represents the outcome of an operation that can either succeed (`Ok`) or fail (`Err`). Instead of throwing exceptions, you return a `Result<T, E>` value that explicitly encodes both possibilities, making error handling part of the type system.

```typescript
// Instead of:
function parseJSON(json: string): any {
  return JSON.parse(json); // throws on invalid JSON
}

// You return a Result:
function parseJSON(json: string): Result<unknown, Error> {
  try {
    return Ok(JSON.parse(json));
  } catch (error) {
    return Err(error as Error);
  }
}
// The caller is FORCED to handle both cases — no unhandled exceptions
```

---

## Result Type Implementation

### Basic Implementation

```typescript
type Result<T, E> = Ok<T> | Err<E>;

interface Ok<T> {
  readonly ok: true;
  readonly value: T;
}

interface Err<E> {
  readonly ok: false;
  readonly error: E;
}

function Ok<T>(value: T): Ok<T> {
  return { ok: true, value };
}

function Err<E>(error: E): Err<E> {
  return { ok: false, error };
}
```

### Full Implementation with Methods

```typescript
type Result<T, E = Error> = Ok<T> | Err<E>;

class Ok<T> {
  readonly ok = true as const;

  constructor(readonly value: T) {}

  isOk(): this is Ok<T> {
    return true;
  }

  isErr(): this is never {
    return false;
  }

  unwrap(): T {
    return this.value;
  }

  unwrapOr(defaultValue: T): T {
    return this.value;
  }

  map<U>(fn: (value: T) => U): Result<U, never> {
    return Ok(fn(this.value));
  }

  flatMap<U>(fn: (value: T) => Result<U, any>): Result<U, any> {
    return fn(this.value);
  }

  tap(fn: (value: T) => void): Ok<T> {
    fn(this.value);
    return this;
  }

  toString(): string {
    return `Ok(${JSON.stringify(this.value)})`;
  }
}

class Err<E> {
  readonly ok = false as const;

  constructor(readonly error: E) {}

  isOk(): this is never {
    return false;
  }

  isErr(): this is Err<E> {
    return true;
  }

  unwrap(): never {
    throw new Error(`Called unwrap on Err: ${this.error}`);
  }

  unwrapOr<T>(defaultValue: T): T {
    return defaultValue;
  }

  map<U>(_fn: (value: any) => U): Err<E> {
    return this; // Err doesn't transform the value
  }

  flatMap<U>(_fn: (value: any) => Result<U, any>): Err<E> {
    return this; // Err doesn't chain
  }

  tap(_fn: (value: any) => void): Err<E> {
    return this; // Err doesn't execute the callback
  }

  toString(): string {
    return `Err(${this.error})`;
  }
}
```

---

## Ok/Error Pattern

### Usage in Practice

```typescript
function divide(a: number, b: number): Result<number, string> {
  if (b === 0) {
    return new Err('Division by zero');
  }
  return new Ok(a / b);
}

// Usage
const result = divide(10, 2);

if (result.ok) {
  console.log(result.value); // 5 — TypeScript knows this is Ok<number>
} else {
  console.log(result.error); // TypeScript knows this is Err<string>
}
```

### Chaining Results

```typescript
function parseAge(input: string): Result<number, string> {
  const num = parseInt(input, 10);
  if (isNaN(num)) {
    return new Err(`"${input}" is not a valid number`);
  }
  if (num < 0 || num > 150) {
    return new Err(`Age must be between 0 and 150, got ${num}`);
  }
  return new Ok(num);
}

function validateAge(age: number): Result<number, string> {
  if (age < 18) {
    return new Err('Must be at least 18 years old');
  }
  return new Ok(age);
}

function registerUser(name: string, ageInput: string): Result<User, string> {
  // Chain multiple Result-returning operations
  return parseAge(ageInput)
    .flatMap((age) => validateAge(age))
    .map((validatedAge) => ({
      name,
      age: validatedAge,
      id: crypto.randomUUID(),
    }));
}

// Usage
const result = registerUser('Alice', '25');
if (result.ok) {
  console.log('Registered:', result.value);
} else {
  console.error('Registration failed:', result.error);
}
```

---

## Railway-Oriented Programming

Railway-Oriented Programming (ROP) is a pattern where success and failure are like two parallel tracks. Once you're on the error track, subsequent operations are skipped until you explicitly switch back.

```
Success Track:  input → [parse] → [validate] → [save] → Ok(result)
                                     ↓              ↓
Failure Track:  Err ← ─ ─ ─ ─ ─ ─Err ─ ─ ─ ─ ─ ─Err
```

### ROP in TypeScript

```typescript
// Each function returns Result, and flatMap chains them
// If any step returns Err, the rest are skipped

type Result<T, E> = Ok<T> | Err<E>;

function Ok<T>(value: T): Ok<T> { return { ok: true, value }; }
function Err<E>(error: E): Err<E> { return { ok: false, error }; }

interface Ok<T> { readonly ok: true; readonly value: T; }
interface Err<E> { readonly ok: false; readonly error: E; }

// ROP chain
function registerUser(data: CreateUserDto): Result<User, string> {
  return validateEmail(data.email)             // Step 1
    .flatMap(() => validatePassword(data.password))  // Step 2
    .flatMap(() => hashPassword(data.password))      // Step 3
    .flatMap((hash) => saveUser({ ...data, password: hash }))  // Step 4
    .map((savedUser) => sendWelcomeEmail(savedUser))  // Side effect on success
    .map(() => ({ id: '123', ...data }));              // Final transformation
}

// Each step:
function validateEmail(email: string): Result<string, string> {
  if (!email.includes('@')) return new Err('Invalid email');
  return new Ok(email);
}

function validatePassword(password: string): Result<string, string> {
  if (password.length < 8) return new Err('Password too short');
  return new Ok(password);
}

function hashPassword(password: string): Result<string, string> {
  // In reality, use bcrypt or argon2
  return new Ok(`hashed_${password}`);
}

function saveUser(user: any): Result<any, string> {
  // Save to database
  return new Ok({ id: '123', ...user });
}

function sendWelcomeEmail(user: any): void {
  // Send email — side effect
}
```

---

## Result with Generics

### Generic Error Types

```typescript
// Domain-specific error types
type UserServiceError =
  | { type: 'NOT_FOUND'; userId: string }
  | { type: 'VALIDATION'; field: string; message: string }
  | { type: 'DUPLICATE_EMAIL'; email: string }
  | { type: 'DATABASE_ERROR'; query: string; originalError: Error };

function findUser(id: string): Promise<Result<User, UserServiceError>> {
  // ...
}

function createUser(data: CreateUserDto): Promise<Result<User, UserServiceError>> {
  // ...
}
```

### Result with Promises

```typescript
type AsyncResult<T, E> = Promise<Result<T, E>>;

async function fetchAndParse(url: string): AsyncResult<ParsedData, string> {
  try {
    const response = await fetch(url);

    if (!response.ok) {
      return new Err(`HTTP ${response.status}`);
    }

    const json = await response.json();
    const parsed = parseData(json);

    if (!parsed.ok) {
      return parsed; // Propagate the error
    }

    return new Ok(parsed.value);
  } catch (error) {
    return new Err(error instanceof Error ? error.message : 'Network error');
  }
}
```

---

## Matching on Result

### Exhaustive Matching

```typescript
function handleResult<T, E>(result: Result<T, E>): string {
  switch (result.ok) {
    case true:
      return `Success: ${JSON.stringify(result.value)}`;
    case false:
      return `Error: ${result.error}`;
  }
}

// With exhaustive checking:
function processResult<T, E>(result: Result<T, E>): void {
  if (result.ok) {
    console.log('Value:', result.value);
  } else {
    console.log('Error:', result.error);
  }
  // TypeScript exhaustiveness check:
  const _exhaustive: never = result;
}
```

### map/flatMap for Chaining

```typescript
// map: transform the success value
const doubled = divide(10, 2).map((v) => v * 2); // Ok(10)

// flatMap: chain operations that return Results
const result = divide(10, 2)
  .flatMap((v) => divide(v, 3))
  .map((v) => v.toFixed(2));

// Combination with pipe:
function pipe<T>(value: T, ...fns: Array<(arg: any) => any>): any {
  return fns.reduce((acc, fn) => fn(acc), value);
}

const finalResult = pipe(
  parseAge('25'),
  (r: Result<number, string>) => r.flatMap(validateAge),
  (r: Result<number, string>) => r.map(createUser),
);
```

---

## Result vs Exceptions

### Comparison

| Feature | Result Type | Exceptions |
|---|---|---|
| Type safety | Explicit in type system | Implicit — types don't show possible errors |
| Control flow | Explicit — caller handles both paths | Can be forgotten — unhandled exceptions |
| Composability | High — map, flatMap, chain | Low — try/catch is not composable |
| Performance | Zero cost (just a value) | Exception throwing has overhead |
| Verbosity | More code at definition | Less code at definition |
| Debugging | Clear error flow | Stack traces can be confusing |

### When to Use Result

```typescript
// USE Result for:
// - Expected failures (validation, not found, auth)
// - Domain logic where errors are part of the flow
// - Library code that should not throw
// - Operations where callers must handle all cases

// USE exceptions for:
// - Programming bugs (null reference, index out of bounds)
// - Truly exceptional conditions (out of memory, disk full)
// - When you want to unwind the call stack
// - Interoperability with libraries that throw
```

---

## neverthrow Library

```typescript
import { ok, err, Result, Ok, Err } from 'neverthrow';

// Basic usage
function divide(a: number, b: number): Result<number, string> {
  if (b === 0) return err('Division by zero');
  return ok(a / b);
}

// Chaining
const result = divide(10, 2)
  .map((v) => v * 2)
  .mapErr((e) => new Error(e));

// Pattern matching
result.match(
  (value) => console.log('Success:', value),
  (error) => console.log('Error:', error)
);

// Async
async function fetchData(): Promise<Result<User, Error>> {
  try {
    const response = await fetch('/api/user');
    const user = await response.json();
    return ok(user);
  } catch (error) {
    return err(error as Error);
  }
}
```

### neverthrow Advanced Features

```typescript
import { ok, err, Result } from 'neverthrow';

// combine: merge multiple Results
import { combine } from 'neverthrow';

const results = combine([
  divide(10, 2),
  divide(20, 4),
  divide(30, 5),
]);

// Result<Array<number>, string>

// fromThrowable: wrap throwing functions
import { fromThrowable } from 'neverthrow';

const safeJsonParse = fromThrowable(JSON.parse);
const result = safeJsonParse('{"valid": true}');
// Result<unknown, SyntaxError>
```

---

## fp-ts Either Pattern

```typescript
import * as E from 'fp-ts/Either';
import { pipe } from 'fp-ts/function';

// Either<L, R> is equivalent to Result<R, L>
// Left = error, Right = success

const divide = (a: number, b: number): E.Either<string, number> =>
  b === 0 ? E.left('Division by zero') : E.right(a / b);

// Chaining with pipe
const result = pipe(
  divide(10, 2),
  E.map((v) => v * 2),
  E.chain((v) => divide(v, 3)),
  E.fold(
    (error) => `Error: ${error}`,
    (value) => `Success: ${value}`
  )
);
```

---

## Best Practices

1. **Use Result for expected failures** — validation, auth, not found. Use exceptions for programming bugs.

2. **Always check both paths** — TypeScript forces you to narrow `ok` before accessing `value` or `error`.

3. **Use `flatMap` for chaining** — each step can fail, and `Err` propagates automatically.

4. **Define domain-specific error types** — don't just use `string` for errors.

5. **Combine with async/await** — `async` functions can return `Promise<Result<T, E>>`.

6. **Use libraries like `neverthrow`** if you don't want to implement Result yourself.

7. **Don't mix Result and exceptions** in the same domain logic.

---

## Interview Questions

### Q1: What is the Result type pattern?

**Answer**: Result is a discriminated union (`Ok<T> | Err<E>`) that represents the outcome of an operation that can succeed or fail. Instead of throwing exceptions, you return a value that explicitly encodes both possibilities, making error handling part of the type system and forcing callers to handle both cases.

### Q2: What is `flatMap` and why is it important for Result?

**Answer**: `flatMap` chains operations that return Results. If the current Result is `Ok`, it applies the function (which returns a new Result). If it's `Err`, it skips the function and propagates the error. This enables clean chaining without nested try/catch blocks.

### Q3: When should you use Result instead of exceptions?

**Answer**: Use Result for expected failures (validation, not found, auth) where the caller should handle the error. Use exceptions for programming bugs, truly exceptional conditions, and when interoperating with throwing libraries. Result makes error handling explicit and composable.

### Q4: How does Result relate to Rust's Result or Haskell's Either?

**Answer**: They're the same concept. Rust's `Result<T, E>` and Haskell's `Either L R` both represent success/failure. TypeScript doesn't have native sum types with exhaustiveness checking, so Result is implemented as a discriminated union. Libraries like `neverthrow` and `fp-ts` provide implementations.

### Q5: What is Railway-Oriented Programming?

**Answer**: A metaphor where success and failure are parallel tracks. Once an operation fails, you're on the "error track" and subsequent operations are skipped. You can switch back to the success track with recovery functions. `flatMap` implements this — it only applies the function on the success track.
