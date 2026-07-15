# Try/Catch/Finally in TypeScript

## Table of Contents

- [Overview](#overview)
- [Basic Syntax](#basic-syntax)
- [Typing Catch Clauses](#typing-catch-clauses)
- [Error Objects](#error-objects)
- [Error instanceof Checks](#error-instanceof-checks)
- [Finally Block Execution](#finally-block-execution)
- [Async Error Handling](#async-error-handling)
- [Error in Async Functions](#error-in-async-functions)
- [Best Practices](#best-practices)
- [Interview Questions](#interview-questions)

---

## Overview

TypeScript inherits JavaScript's `try/catch/finally` error handling mechanism but adds static typing to catch clauses. Proper error handling is essential for building robust applications — unhandled errors crash Node.js processes and break browser functionality.

---

## Basic Syntax

```typescript
try {
  // Code that might throw an error
  const result = riskyOperation();
  return result;
} catch (error) {
  // Handle the error
  console.error('Something went wrong:', error);
} finally {
  // Always executes — regardless of success or failure
  cleanup();
}
```

### Try-Catch with Return Values

```typescript
function divide(a: number, b: number): number {
  try {
    if (b === 0) {
      throw new Error('Division by zero');
    }
    return a / b;
  } catch (error) {
    console.error(error);
    return NaN;
  }
  // Note: finally runs before the return
}

// The finally block executes BEFORE the return from try/catch:
function example(): number {
  try {
    return 1; // return is set but not yet delivered
  } finally {
    console.log('finally'); // this runs first
    // return 2; // if finally also returns, it overrides the try return
  }
  // Returns 1, but "finally" is logged first
}
```

### Nested Try-Catch

```typescript
function complexOperation(): string {
  try {
    const data = fetchUserData();
    try {
      const parsed = JSON.parse(data);
      return parsed.name;
    } catch (parseError) {
      console.error('JSON parse failed:', parseError);
      return 'default';
    }
  } catch (fetchError) {
    console.error('Fetch failed:', fetchError);
    return 'error';
  }
}
```

---

## Typing Catch Clauses

### TypeScript 4.0 and Earlier (implicit `any`)

```typescript
// Before TS 4.4: catch clause variable is implicitly `any`
try {
  riskyOperation();
} catch (error) {
  // error is `any` — no type safety
  console.log(error.message); // no type checking
  console.log(error.code);    // no type checking — might not exist
}
```

### TypeScript 4.4+ (useUnknownInCatchVariables)

```jsonc
// tsconfig.json
{
  "compilerOptions": {
    "useUnknownInCatchVariables": true  // default in strict mode since TS 4.4
  }
}
```

```typescript
// With useUnknownInCatchVariables: error is `unknown`
try {
  riskyOperation();
} catch (error) {
  // error is `unknown` — must narrow before use
  if (error instanceof Error) {
    console.log(error.message); // OK — narrowed to Error
  } else if (typeof error === 'string') {
    console.log(error);         // OK — narrowed to string
  } else {
    console.log(String(error)); // fallback
  }
}
```

### Explicit `any` Catch (When Needed)

```typescript
// If you explicitly type catch as `any`:
try {
  riskyOperation();
} catch (error: any) {
  // error is `any` — you opted out of safety
  console.log(error.message);
  console.log(error.code);
  // But you lose type safety — avoid this
}
```

### Custom Type Guard for Errors

```typescript
function isErrorLike(value: unknown): value is { message: string; code?: number } {
  return (
    typeof value === 'object' &&
    value !== null &&
    'message' in value &&
    typeof (value as any).message === 'string'
  );
}

try {
  riskyOperation();
} catch (error) {
  if (isErrorLike(error)) {
    console.log(error.message);  // safe
    console.log(error.code);     // safe — might be undefined
  }
}
```

---

## Error Objects

### Standard Error Properties

```typescript
const error = new Error('Something went wrong');

console.log(error.message);    // 'Something went wrong'
console.log(error.name);       // 'Error'
console.log(error.stack);      // stack trace string
```

### Creating Errors

```typescript
// Basic Error
throw new Error('Basic error');

// Error with options (ES2022+)
throw new Error('Not found', { cause: originalError });

// TypeError
throw new TypeError('Expected a string');

// ReferenceError
throw new ReferenceError('variable is not defined');

// SyntaxError
throw new SyntaxError('Unexpected token');

// RangeError
throw new RangeError('Value out of range');
```

### Error with Cause Chain

```typescript
async function fetchData(url: string) {
  try {
    const response = await fetch(url);
    return await response.json();
  } catch (error) {
    throw new Error(`Failed to fetch data from ${url}`, { cause: error });
  }
}

async function getUserData() {
  try {
    return await fetchData('https://api.example.com/users');
  } catch (error) {
    if (error instanceof Error) {
      console.log('Error:', error.message);
      console.log('Cause:', error.cause);
    }
    throw error;
  }
}
```

---

## Error instanceof Checks

### Basic Instanceof

```typescript
function handleResponse(response: Response) {
  try {
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }
    return response.json();
  } catch (error) {
    if (error instanceof TypeError) {
      // Network error or invalid JSON
      console.error('Network error:', error.message);
    } else if (error instanceof SyntaxError) {
      // Invalid JSON response
      console.error('Parse error:', error.message);
    } else if (error instanceof Error) {
      // Generic error
      console.error('Error:', error.message);
    } else {
      // Non-Error thrown value
      console.error('Unknown error:', String(error));
    }
  }
}
```

### Checking Custom Error Types

```typescript
class ValidationError extends Error {
  constructor(
    public field: string,
    public value: any,
    message: string
  ) {
    super(message);
    this.name = 'ValidationError';
  }
}

class NotFoundError extends Error {
  constructor(resource: string, id: string) {
    super(`${resource} with id ${id} not found`);
    this.name = 'NotFoundError';
  }
}

function processUser(data: any) {
  try {
    validateUser(data);
    return saveUser(data);
  } catch (error) {
    if (error instanceof ValidationError) {
      console.error(`Invalid ${error.field}: ${error.message}`);
      return { status: 400, field: error.field };
    } else if (error instanceof NotFoundError) {
      console.error(error.message);
      return { status: 404 };
    }
    throw error; // re-throw unexpected errors
  }
}
```

---

## Finally Block Execution

### Basic Finally

```typescript
function readFile(path: string): string | null {
  let file: FileHandle | null = null;
  try {
    file = openFile(path);
    return file.read();
  } catch (error) {
    console.error('Read error:', error);
    return null;
  } finally {
    if (file) {
      file.close(); // Always close the file
    }
  }
}
```

### Finally and Return

```typescript
// Finally ALWAYS executes — even after return or throw
function example(): number {
  try {
    console.log('try');
    return 1;
  } catch (error) {
    console.log('catch');
    return 2;
  } finally {
    console.log('finally'); // Always runs
    // If you return from finally, it overrides the try/catch return
    // return 3; // Would override the return value!
  }
  // Returns 1 (finally runs but doesn't override)
}

// WARNING: returning from finally overrides the try/catch return:
function dangerous(): number {
  try {
    return 1;
  } finally {
    return 2; // This overrides the try return! Returns 2.
  }
}
```

### Finally with Async/Await

```typescript
async function processWithCleanup(): Promise<string> {
  const resource = await acquireResource();
  try {
    const result = await processData(resource);
    return result;
  } catch (error) {
    console.error('Processing failed:', error);
    throw error;
  } finally {
    await resource.release(); // Always release, even on error
  }
}
```

---

## Async Error Handling

### try/catch in Async Functions

```typescript
async function fetchUserData(id: string): Promise<User> {
  try {
    const response = await fetch(`/api/users/${id}`);

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }

    const data = await response.json();
    return data as User;
  } catch (error) {
    if (error instanceof TypeError) {
      // Network error
      throw new Error('Network error — are you online?');
    } else if (error instanceof Error) {
      throw new Error(`Failed to fetch user: ${error.message}`);
    }
    throw new Error('Unknown error occurred');
  }
}
```

### Parallel Error Handling

```typescript
// Promise.all — fails on first error
async function loadAll() {
  try {
    const [users, posts, comments] = await Promise.all([
      fetchUsers(),
      fetchPosts(),
      fetchComments(),
    ]);
    return { users, posts, comments };
  } catch (error) {
    // One of them failed
    console.error('Failed to load:', error);
    throw error;
  }
}

// Promise.allSettled — handles individual failures
async function loadAllGracefully() {
  const results = await Promise.allSettled([
    fetchUsers(),
    fetchPosts(),
    fetchComments(),
  ]);

  const errors: Error[] = [];
  for (const result of results) {
    if (result.status === 'rejected') {
      errors.push(result.reason);
    }
  }

  if (errors.length > 0) {
    console.warn(`${errors.length} operations failed:`, errors);
  }

  return results
    .filter((r) => r.status === 'fulfilled')
    .map((r) => (r as PromiseFulfilledResult<any>).value);
}
```

---

## Error in Async Functions

### Unhandled Promise Rejection

```typescript
// BAD: No error handling — unhandled rejection
async function riskyOperation() {
  const data = await fetch('/api/data');
  return data.json();
}
// If fetch fails, this creates an unhandled promise rejection

// GOOD: Properly handled
async function safeOperation() {
  try {
    const data = await fetch('/api/data');
    return await data.json();
  } catch (error) {
    console.error('Operation failed:', error);
    return null;
  }
}
```

### Fire-and-Forget Async

```typescript
// BAD: Unhandled rejection if processItem throws
async function processItems(items: Item[]) {
  for (const item of items) {
    processItem(item); // missing await!
  }
}

// GOOD: With error handling
async function processItemsSafe(items: Item[]) {
  for (const item of items) {
    try {
      await processItem(item);
    } catch (error) {
      console.error(`Failed to process item ${item.id}:`, error);
      // Continue processing other items
    }
  }
}

// ALSO GOOD: Using Promise.allSettled for parallel processing
async function processItemsParallel(items: Item[]) {
  const results = await Promise.allSettled(
    items.map((item) => processItem(item))
  );

  const failures = results.filter((r) => r.status === 'rejected');
  if (failures.length > 0) {
    console.error(`${failures.length} items failed to process`);
  }
}
```

### Global Unhandled Rejection Handler

```typescript
// Node.js
process.on('unhandledRejection', (reason, promise) => {
  console.error('Unhandled Rejection at:', promise, 'reason:', reason);
  // Log to error reporting service
  // Optionally exit the process
});

process.on('uncaughtException', (error) => {
  console.error('Uncaught Exception:', error);
  // Clean up and exit
  process.exit(1);
});

// Browser
window.addEventListener('unhandledrejection', (event) => {
  console.error('Unhandled rejection:', event.reason);
  event.preventDefault(); // Prevents console error
});
```

---

## Best Practices

1. **Always type catch clauses as `unknown`** — use `useUnknownInCatchVariables: true` and narrow with `instanceof`.

2. **Never catch and ignore errors silently** — at minimum, log them.

3. **Use `finally` for cleanup** — file handles, connections, locks.

4. **Don't throw in `finally`** — it overrides the return/throw from try/catch.

5. **Always handle async errors** — use try/catch with await, or `.catch()`.

6. **Use `Promise.allSettled`** when partial failures are acceptable.

7. **Add global unhandled rejection handlers** in Node.js and browser apps.

8. **Re-throw unexpected errors** — catch specific types, re-throw everything else.

9. **Use error cause chains** (`{ cause: error }`) to preserve error context.

10. **Don't use try/catch for control flow** — use it for exceptional cases only.

---

## Interview Questions

### Q1: What is the difference between `catch (error)` and `catch (error: any)`?

**Answer**: With `useUnknownInCatchVariables: true` (default in strict mode since TS 4.4), `catch (error)` makes `error` type `unknown`, requiring narrowing before use. `catch (error: any)` explicitly opts into `any`, giving no type safety. Always prefer `unknown` for type-safe error handling.

### Q2: Does `finally` run before or after `return`?

**Answer**: `finally` runs BEFORE the return value is delivered to the caller. The return value is set but not yet delivered, so finally executes first. If `finally` itself contains a `return`, it overrides the return from `try` or `catch`.

### Q3: How do you handle errors in async/await?

**Answer**: Wrap `await` calls in `try/catch`. The `catch` block receives any rejected promise from the awaited call. Without try/catch, the rejected promise becomes an unhandled rejection. For parallel operations, use `Promise.allSettled` to handle partial failures.

### Q4: What is an unhandled promise rejection?

**Answer**: When a Promise rejects and no `.catch()` handler or `try/catch` (with `await`) is attached, it's an "unhandled rejection." In Node.js 15+, unhandled rejections terminate the process. Always handle promise rejections.

### Q5: Can you catch errors from `Promise.all`?

**Answer**: `Promise.all` rejects immediately on the first rejected promise. You can catch with try/catch (if awaited) or `.catch()`. However, you only get the first error. Use `Promise.allSettled` if you need to handle all results including failures.
