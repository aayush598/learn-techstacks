# Error Handling — Interview Questions

## Overview

This document contains 25+ interview questions covering TypeScript error handling: try/catch/finally, custom errors, Result type pattern, exhaustive handling, and error boundaries. Each question includes a detailed answer.

---

## Questions

### Q1: What is `useUnknownInCatchVariables` and why should you enable it?

**Answer**: `useUnknownInCatchVariables` (default in `strict` mode since TS 4.4) makes the catch clause variable type `unknown` instead of `any`. This forces you to narrow the error type before accessing properties, preventing runtime errors from accessing non-existent properties on unknown thrown values. Always enable it for type-safe error handling.

---

### Q2: How do you create a custom error class in TypeScript?

**Answer**: Extend `Error`, call `super(message)`, set `this.name`, and call `Object.setPrototypeOf(this, CustomError.prototype)` to fix the prototype chain for `instanceof` to work. The `setPrototypeOf` call is necessary because TypeScript/Babel compilation can break the prototype chain for classes extending built-ins.

---

### Q3: What is the Result type pattern?

**Answer**: Result is a discriminated union (`Ok<T> | Err<E>`) that represents success or failure as a value instead of throwing exceptions. It makes errors explicit in the type system — callers must handle both cases. Operations are chained with `map` (transform success) and `flatMap` (chain operations that may fail).

---

### Q4: What is Railway-Oriented Programming?

**Answer**: A functional programming pattern where success and failure are parallel "tracks." Once an operation fails, subsequent operations are skipped (you stay on the error track). `flatMap` implements this — it only applies the function on the success track and propagates errors. This eliminates nested try/catch and makes error flow explicit.

---

### Q5: How does the `never` type enable exhaustive error handling?

**Answer**: `never` represents a value that can never exist. In an exhaustive switch on a discriminated union, after handling all cases, the remaining type should be `never`. If a case is missing, the type is not `never`, causing a compile error. This catches missing error handlers at compile time.

---

### Q6: What is the difference between operational and programming errors?

**Answer**: Operational errors are expected failures (validation, not found, auth) — the system should handle them gracefully. Programming errors are bugs (null reference, type error) — they indicate code defects. Operational errors should be caught and returned as responses; programming errors should be allowed to crash.

---

### Q7: Can you explain `finally` block behavior with `return`?

**Answer**: The `finally` block always executes, even after `return` or `throw`. The return value is "set but not delivered" when `finally` runs. If `finally` also contains a `return`, it overrides the return from `try`/`catch`. This is a common source of bugs — avoid returning from `finally`.

---

### Q8: How do you handle errors in async/await?

**Answer**: Wrap `await` calls in `try/catch`. Without it, rejected promises become unhandled rejections (which crash Node.js 15+). For parallel operations, use `Promise.allSettled` to handle partial failures gracefully. Always attach `.catch()` to promises even when using `await`.

---

### Q9: What is an error catalog pattern?

**Answer**: A centralized registry of all possible application errors with their codes, messages, HTTP status codes, and categories. Instead of scattering error definitions, the catalog provides a single source of truth. Errors are thrown using catalog keys, ensuring consistency and enabling centralized error-to-status mapping.

---

### Q10: Why do you need `Object.setPrototypeOf` in custom errors?

**Answer**: TypeScript compiles class syntax to ES5/ES6, which can break the prototype chain for classes extending built-ins like `Error`. Without `Object.setPrototypeOf(this, CustomError.prototype)`, `instanceof CustomError` may return `false` in some environments (especially when transpiled with Babel or TypeScript targeting ES5).

---

### Q11: How do React error boundaries work?

**Answer**: Error boundaries are class components that catch errors in their child tree during rendering, lifecycle methods, and constructors. They implement `componentDidCatch` and `getDerivedStateFromError` to catch errors and display fallback UI. They don't catch errors in event handlers, async code, or server-side rendering.

---

### Q12: What is the difference between `Promise.all` and `Promise.allSettled`?

**Answer**: `Promise.all` rejects immediately on the first rejected promise — you lose other results. `Promise.allSettled` waits for all promises and returns their status (`fulfilled` or `rejected`) with values/reasons. Use `allSettled` when partial failures are acceptable and you need all results.

---

### Q13: How do you serialize Error objects for logging?

**Answer**: `JSON.stringify(error)` returns `{}` because Error properties are non-enumerable. Solutions: implement `toJSON()` on the error class, manually extract properties with `Object.getOwnPropertyNames()`, or create a plain object with explicit fields (name, message, stack, code).

---

### Q14: What is an error boundary in server-side applications?

**Answer**: In server apps, error boundaries are middleware functions that catch errors from request handlers and return structured error responses. In Express, it's an error-handling middleware `(err, req, res, next)`. In NestJS, it's an `@Catch()` exception filter. They prevent errors from crashing the server.

---

### Q15: When should you use the Result type vs exceptions?

**Answer**: Use Result for expected failures (validation, not found, auth) where callers should handle the error. Use exceptions for programming bugs, truly exceptional conditions (out of memory), and when interoperating with throwing libraries. Result is composable and makes error handling explicit; exceptions unwind the call stack.

---

### Q16: How do you implement typed catch blocks in TypeScript?

**Answer**: With `unknown` as the catch type, use a series of `instanceof` checks to narrow: `if (error instanceof ValidationError) { ... } else if (error instanceof NotFoundError) { ... }`. You can also use type predicate functions (`is` keyword) for custom narrowing. Always include a fallback for truly unknown values.

---

### Q17: What is the `cause` option in Error constructors?

**Answer**: ES2022 added an optional `cause` property to Error: `new Error('message', { cause: originalError })`. This creates an error chain that preserves the original error. It's useful for wrapping lower-level errors while maintaining context: `throw new Error('Failed to fetch', { cause: networkError })`.

---

### Q18: How do you handle errors globally in Node.js?

**Answer**: Use `process.on('uncaughtException', handler)` for synchronous uncaught errors and `process.on('unhandledRejection', handler)` for rejected promises. Both are last-resort handlers that should log errors and attempt graceful shutdown. In production, pair with error monitoring services like Sentry.

---

### Q19: What are discriminated unions and why are they useful for errors?

**Answer**: Discriminated unions use a common literal property (`type` or `kind`) to distinguish between union members. For errors, each error type has a unique `type` value. This enables exhaustive switch checking — TypeScript knows exactly which types exist and can flag missing cases.

---

### Q20: How do you prevent error details from leaking in production APIs?

**Answer**: Use the operational vs programming error distinction. For operational errors, return structured responses with error codes and safe messages. For programming errors, log the full error server-side but return a generic "Internal Server Error" to clients. Never expose stack traces, SQL queries, or internal paths in production responses.

---

### Q21: What is the difference between `throw` and `return` in error handling?

**Answer**: `throw` creates an exception that unwinds the call stack until caught by `try/catch`. It stops normal execution. `return` exits the current function and passes a value to the caller. In Result pattern, you `return Err(...)` instead of `throw` — this keeps error handling explicit and doesn't break the call stack.

---

### Q22: Can you use `try/catch` with `async/await` for `Promise.all`?

**Answer**: Yes. `await Promise.all([...])` inside a `try/catch` catches the first rejection. For handling all results (including failures), use `await Promise.allSettled([...])` and check each result's `status`. This is essential for parallel operations where partial failures should not abort the entire batch.

---

### Q23: How do you test error handling code?

**Answer**: Test both the happy path and error paths. Use `expect(fn).toThrow(ErrorClass)` for synchronous errors. For async: `await expect(fn()).rejects.toThrow()`. For Result types: check `result.ok`, `result.value`, and `result.error`. Test that errors carry correct codes, messages, and status codes.

---

### Q24: What is the error middleware pattern in Express?

**Answer**: Express error middleware has 4 parameters: `(err, req, res, next)`. It's registered after all route handlers. When `next(error)` is called in a route, Express skips normal middleware and goes directly to the error handler. This centralizes error handling and ensures consistent error responses.

---

### Q25: How do you handle validation errors with decorators and error handling?

**Answer**: Parameter decorators store validation metadata using `Reflect.defineMetadata`. A method decorator reads this metadata and validates arguments before calling the original method. If validation fails, it throws a `ValidationError`. The error propagates to error middleware which returns a 400 response with field-level error details.

---

### Q26: What are the performance implications of try/catch in TypeScript?

**Answer**: Modern JavaScript engines optimize try/catch well — there's minimal overhead for the try block itself. The cost is primarily in the throw: creating an Error object and capturing a stack trace is expensive (can be 100x slower than a normal return). Don't use exceptions for control flow — use them only for truly exceptional cases.

---

### Q27: How do you implement a retry mechanism with error handling?

**Answer**: Create a loop that attempts the operation, catches errors, and retries after a delay. Use exponential backoff for network operations. Limit retries with a max count. Only retry on specific error types (network errors, rate limits) — don't retry on validation or auth errors. Always have a final error handler after retries are exhausted.

```typescript
async function withRetry<T>(
  fn: () => Promise<T>,
  maxRetries: number = 3,
  delayMs: number = 1000
): Promise<T> {
  let lastError: Error | undefined;
  for (let i = 0; i < maxRetries; i++) {
    try {
      return await fn();
    } catch (error) {
      lastError = error as Error;
      if (i < maxRetries - 1) {
        await new Promise(r => setTimeout(r, delayMs * Math.pow(2, i)));
      }
    }
  }
  throw lastError;
}
```
