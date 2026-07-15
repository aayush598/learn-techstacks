# Promises in TypeScript

## Table of Contents

- [Promise Overview](#promise-overview)
- [The Promise<T> Type](#the-promiset-type)
- [Creating Promises](#creating-promises)
- [Promise States](#promise-states)
- [then, catch, finally](#then-catch-finally)
- [Promise Chaining](#promise-chaining)
- [Error Handling Patterns](#error-handling-patterns)
- [Promise.all](#promiseall)
- [Promise.race](#promiserace)
- [Promise.allSettled](#promiseallsettled)
- [Promise.any](#promiseany)
- [Promise.resolve and Promise.reject](#promiseresolve-and-promisereject)
- [Promisification](#promisification)
- [Advanced Patterns](#advanced-patterns)
- [Interview Questions](#interview-questions)

---

## Promise Overview

A Promise represents the eventual completion (or failure) of an asynchronous operation and its resulting value. In TypeScript, promises are strongly typed, allowing you to specify exactly what type of value a promise resolves to.

---

## The Promise<T> Type

`Promise<T>` is a generic interface where `T` is the type of the value the promise resolves to.

```typescript
// Promise that resolves to a string
const promise1: Promise<string> = new Promise((resolve) => {
  resolve("hello");
});

// Promise that resolves to a number
const promise2: Promise<number> = new Promise((resolve) => {
  resolve(42);
});

// Promise that resolves to a complex object
interface User {
  id: number;
  name: string;
  email: string;
}

const promise3: Promise<User> = new Promise((resolve) => {
  resolve({ id: 1, name: "Alice", email: "alice@example.com" });
});

// Promise that resolves to void (no meaningful return value)
const promise4: Promise<void> = new Promise((resolve) => {
  console.log("side effect");
  resolve();
});

// Promise that may resolve to string or null
const promise5: Promise<string | null> = new Promise((resolve) => {
  resolve(null);
});
```

### Promise Type in the Standard Library

```typescript
// The built-in Promise constructor signature
interface PromiseConstructor {
  new <T>(
    executor: (
      resolve: (value: T | PromiseLike<T>) => void,
      reject: (reason?: any) => void
    ) => void
  ): Promise<T>;
}

// A PromiseLike is anything with a .then() method
interface PromiseLike<T> {
  then(
    onfulfilled?: ((value: T) => TResult | PromiseLike<TResult>) | null,
    onrejected?: ((reason: any) => TResult2 | PromiseLike<TResult2>) | null
  ): Promise<TResult | TResult2>;
}
```

---

## Creating Promises

```typescript
// Basic promise creation
function fetchUser(id: number): Promise<User> {
  return new Promise((resolve, reject) => {
    setTimeout(() => {
      if (id > 0) {
        resolve({ id, name: "User" + id, email: `user${id}@example.com` });
      } else {
        reject(new Error("Invalid user ID"));
      }
    }, 1000);
  });
}

// Promise that wraps a callback-based API
function readFilePromise(path: string): Promise<string> {
  return new Promise((resolve, reject) => {
    // Simulating fs.readFile with callback
    const fakeFs = (p: string, cb: (err: Error | null, data?: string) => void) => {
      cb(null, `contents of ${p}`);
    };

    fakeFs(path, (err, data) => {
      if (err) reject(err);
      else resolve(data!);
    });
  });
}

// Promise with immediate resolution
const immediate = Promise.resolve(42);
const immediateStr = Promise.resolve("hello");

// Promise with immediate rejection
const immediateError = Promise.reject(new Error("fail"));

// Void promise for side effects
function logAction(action: string): Promise<void> {
  return new Promise((resolve) => {
    console.log(`Action: ${action}`);
    resolve();
  });
}
```

---

## Promise States

A promise is in one of three states:

1. **Pending**: Initial state, neither fulfilled nor rejected
2. **Fulfilled**: The operation completed successfully
3. **Rejected**: The operation failed

```typescript
// Once settled, a promise cannot change state
const settled: Promise<string> = new Promise((resolve) => {
  resolve("first");
  resolve("second"); // ignored
  throw new Error("third"); // ignored
});

// A rejected promise
const rejected: Promise<never> = new Promise((_, reject) => {
  reject(new Error("failed"));
});

// Detecting promise state (not recommended in production, but useful for debugging)
function isFulfilled<T>(promise: Promise<T>): promise is Promise<T> {
  // Promise.prototype.status is not standard, but useful conceptually
  return true; // Simplified
}
```

---

## then, catch, finally

```typescript
// then - transforms the resolved value
const result: Promise<number> = Promise.resolve(5)
  .then((value) => value * 2) // 10
  .then((value) => value + 1); // 11

// then with rejection handler (second argument)
const withFallback: Promise<string> = fetchUser(-1)
  .then(
    (user) => user.name,
    (error) => `Error: ${(error as Error).message}` // fallback value on rejection
  );

// catch - handles rejections
const withCatch: Promise<User | string> = fetchUser(-1)
  .then((user) => user)
  .catch((error) => `Failed to fetch: ${(error as Error).message}`);

// catch returns a new promise that resolves with the fallback value
const recovered: Promise<string> = fetchUser(-1)
  .then((user) => user.name)
  .catch((error) => "Unknown User") // recovers the chain
  .then((name) => `Hello, ${name}`); // continues the chain

// finally - runs regardless of fulfillment or rejection
const withFinally: Promise<User> = fetchUser(1)
  .then((user) => {
    console.log("Success:", user.name);
    return user;
  })
  .catch((error) => {
    console.error("Failed:", error);
    throw error; // re-throw to maintain rejection
  })
  .finally(() => {
    console.log("Cleanup regardless of outcome");
    // finally does NOT receive the resolved/rejected value
    // but it can still pass through the original value
  });

// finally returning a value overrides the original
const override: Promise<number> = Promise.resolve(1)
  .finally(() => 2); // resolves to 1, not 2 (finally ignores return unless it rejects)

const overrideReject: Promise<never> = Promise.resolve(1)
  .finally(() => {
    throw new Error("override"); // this DOES override - chain rejects
  });
```

---

## Promise Chaining

```typescript
// Proper chaining pattern
function processOrder(orderId: number): Promise<string> {
  return fetchOrder(orderId)
    .then((order) => validateOrder(order))
    .then((order) => processPayment(order))
    .then((payment) => sendConfirmation(payment))
    .then((confirmation) => confirmation.referenceId)
    .catch((error) => {
      console.error("Order processing failed:", error);
      throw new OrderError(`Failed to process order ${orderId}`, { cause: error });
    });
}

// Anti-pattern: promise nesting (pyramid of doom)
// AVOID THIS:
function badChaining(): Promise<string> {
  return fetchUser(1).then((user) => {
    return fetchPosts(user.id).then((posts) => {
      return fetchComments(posts[0].id).then((comments) => {
        return comments[0].content;
      });
    });
  });
}

// Good: flat chaining
function goodChaining(): Promise<string> {
  return fetchUser(1)
    .then((user) => fetchPosts(user.id))
    .then((posts) => fetchComments(posts[0].id))
    .then((comments) => comments[0].content);
}

// Chaining with type narrowing
function processValue(input: unknown): Promise<string> {
  return Promise.resolve(input)
    .then((val) => {
      if (typeof val !== "string") throw new TypeError("Expected string");
      return val;
    })
    .then((str) => str.toUpperCase())
    .then((str) => `Result: ${str}`);
}
```

---

## Error Handling Patterns

```typescript
// Pattern 1: Catch at the end of the chain
function fetchData(): Promise<Data> {
  return apiCall()
    .then((response) => parseResponse(response))
    .then((data) => transformData(data))
    .catch((error) => {
      logger.error("fetchData failed", error);
      return fallbackData();
    });
}

// Pattern 2: Typed error handling
interface ApiError {
  code: number;
  message: string;
  details?: Record<string, unknown>;
}

class TypedApiError extends Error {
  constructor(
    public statusCode: number,
    message: string,
    public details?: Record<string, unknown>
  ) {
    super(message);
    this.name = "TypedApiError";
  }
}

function typedFetch(url: string): Promise<Response> {
  return fetch(url).then((response) => {
    if (!response.ok) {
      throw new TypedApiError(response.status, response.statusText);
    }
    return response;
  });
}

// Pattern 3: Error recovery chain
function resilientFetch(url: string): Promise<Data> {
  return fetch(url)
    .then((r) => r.json())
    .catch((error) => {
      if (error instanceof TypeError) {
        // Network error - retry
        return fetch(url).then((r) => r.json());
      }
      throw error; // re-throw non-network errors
    })
    .catch((error) => {
      // Final fallback
      return getCachedData(url);
    });
}

// Pattern 4: Aggregate errors
class AggregateError extends Error {
  constructor(
    public errors: Error[],
    message?: string
  ) {
    super(message ?? `${errors.length} errors occurred`);
    this.name = "AggregateError";
  }
}

function fetchAllOrNothing(urls: string[]): Promise<Response[]> {
  return Promise.all(
    urls.map((url) =>
      fetch(url).then((r) => {
        if (!r.ok) throw new Error(`HTTP ${r.status}`);
        return r;
      })
    )
  );
}
```

---

## Promise.all

```typescript
// Promise.all resolves when ALL promises resolve
// If ANY promise rejects, the whole thing rejects

interface Post {
  id: number;
  title: string;
}

interface Comment {
  id: number;
  body: string;
}

// Fetch multiple resources in parallel
function loadDashboard(userId: number): Promise<{
  user: User;
  posts: Post[];
  comments: Comment[];
}> {
  return Promise.all([
    fetchUser(userId),
    fetchPosts(userId),
    fetchComments(userId),
  ]).then(([user, posts, comments]) => ({
    user,
    posts,
    comments,
  }));
}

// Type inference with Promise.all
const mixedResults = Promise.all([
  Promise.resolve(1),         // Promise<number>
  Promise.resolve("hello"),   // Promise<string>
  Promise.resolve(true),      // Promise<boolean>
]);
// Type: Promise<[number, string, boolean]>

// Using the Awaited utility type
type DashboardResult = Awaited<ReturnType<typeof loadDashboard>>;

// Promise.all with empty array
const empty = Promise.all([]); // Promise<never[]>
const emptyTyped = Promise.all<never>([]); // Promise<never[]>
```

---

## Promise.race

```typescript
// Promise.race resolves/rejects with the FIRST settled promise
// Useful for timeouts

function withTimeout<T>(promise: Promise<T>, ms: number): Promise<T> {
  const timeout = new Promise<never>((_, reject) => {
    setTimeout(() => reject(new Error(`Timeout after ${ms}ms`)), ms);
  });
  return Promise.race([promise, timeout]);
}

// Usage
const result = withTimeout(fetch("https://api.example.com"), 5000);

// Race with multiple sources
function fastestResponse(url: string): Promise<Response> {
  const sources = [fetch(url), fetch(url), fetch(url)];
  return Promise.race(sources);
}

// ⚠️ Warning: race rejects if the FIRST settled promise is a rejection
// even if other promises resolve successfully
```

---

## Promise.allSettled

```typescript
// Promise.allSettled resolves when ALL promises settle (resolve or reject)
// Never rejects - always resolves

interface FulfilledResult<T> {
  status: "fulfilled";
  value: T;
}

interface RejectedResult {
  status: "rejected";
  reason: unknown;
}

type PromiseSettledResult<T> = FulfilledResult<T> | RejectedResult;

function fetchMultipleUsers(
  ids: number[]
): Promise<PromiseSettledResult<User>[]> {
  return Promise.allSettled(ids.map((id) => fetchUser(id)));
}

// Processing results
async function processResults(ids: number[]): Promise<{
  successful: User[];
  failed: number[];
}> {
  const results = await fetchMultipleUsers(ids);
  const successful: User[] = [];
  const failed: number[] = [];

  results.forEach((result, index) => {
    if (result.status === "fulfilled") {
      successful.push(result.value);
    } else {
      failed.push(ids[index]);
      console.error(`User ${ids[index]} failed:`, result.reason);
    }
  });

  return { successful, failed };
}

// Type narrowing
function handleResult(result: PromiseSettledResult<User>): string {
  if (result.status === "fulfilled") {
    return result.value.name; // TypeScript knows result.value is User
  } else {
    return `Error: ${result.reason}`;
  }
}
```

---

## Promise.any

```typescript
// Promise.any resolves with the FIRST fulfilled promise
// Only rejects if ALL promises reject (AggregateError)
// Useful for fallback strategies

function fetchFromMultipleSources(urls: string[]): Promise<Response> {
  return Promise.any(urls.map((url) => fetch(url)));
}

// With fallback chain
function fetchWithFallback(
  primary: string,
  secondary: string,
  tertiary: string
): Promise<Response> {
  return Promise.any([
    fetch(primary),
    fetch(secondary),
    fetch(tertiary),
  ]).catch((errors: AggregateError) => {
    // All sources failed
    console.error("All sources failed:", errors.errors);
    throw new Error("All data sources unavailable");
  });
}

// Promise.any vs Promise.race
// - Promise.race: settles with first settled (resolve OR reject)
// - Promise.any: settles with first FULFILLED (ignore rejections until all fail)

const urls = [
  "https://api1.example.com",
  "https://api2.example.com",
  "https://api3.example.com",
];

// If api1 fails, race stops. any continues to api2.
const result = Promise.any(urls.map((url) => fetch(url)));
```

---

## Promise.resolve and Promise.reject

```typescript
// Promise.resolve - wraps a value in a resolved promise
const resolved: Promise<number> = Promise.resolve(42);
const resolvedPromise: Promise<string> = Promise.resolve(Promise.resolve("hello"));

// Promise.reject - wraps a reason in a rejected promise
const rejected: Promise<never> = Promise.reject(new Error("fail"));

// Useful for consistent API (always return a promise)
function maybeAsync(value: string): Promise<string> {
  if (value.length > 0) {
    return Promise.resolve(value);
  }
  return Promise.reject(new Error("Empty string"));
}

// Promise.reject should always use an Error object
// BAD:
const badReject = Promise.reject("string error");
// GOOD:
const goodReject = Promise.reject(new Error("descriptive error"));
```

---

## Promisification

Converting callback-based APIs to promise-based:

```typescript
// Original callback API
function getUserCallback(
  id: number,
  callback: (error: Error | null, user?: User) => void
): void {
  // Simulated async operation
  setTimeout(() => {
    if (id > 0) {
      callback(null, { id, name: "User" + id, email: "" });
    } else {
      callback(new Error("Invalid ID"));
    }
  }, 100);
}

// Promisified version
function getUser(id: number): Promise<User> {
  return new Promise((resolve, reject) => {
    getUserCallback(id, (error, user) => {
      if (error) reject(error);
      else resolve(user!);
    });
  });
}

// Generic promisification helper
function promisify<TArgs extends unknown[], TResult>(
  fn: (...args: [...TArgs, (error: Error | null, result?: TResult) => void]) => void
): (...args: TArgs) => Promise<TResult> {
  return (...args: TArgs) =>
    new Promise((resolve, reject) => {
      fn(...args, (error, result) => {
        if (error) reject(error);
        else resolve(result!);
      });
    });
}

// Usage
const getUserAsync = promisify(getUserCallback);
const user = await getUserAsync(1);

// Node.js style promisify
import { promisify } from "util";
import { readFile } from "fs";

const readFileAsync = promisify(readFile);
const content = await readFileAsync("file.txt", "utf-8");
```

---

## Advanced Patterns

```typescript
// Promise pooling - limit concurrency
async function pool<T>(
  items: T[],
  concurrency: number,
  fn: (item: T) => Promise<unknown>
): Promise<void> {
  const executing = new Set<Promise<unknown>>();

  for (const item of items) {
    const p = fn(item).then(() => {
      executing.delete(p);
    });
    executing.add(p);

    if (executing.size >= concurrency) {
      await Promise.race(executing);
    }
  }

  await Promise.all(executing);
}

// Promise retry
function retry<T>(
  fn: () => Promise<T>,
  attempts: number = 3,
  delay: number = 1000
): Promise<T> {
  return fn().catch((error) => {
    if (attempts <= 1) throw error;
    return new Promise((resolve) => setTimeout(resolve, delay))
      .then(() => retry(fn, attempts - 1, delay));
  });
}

// Lazy promise (deferred execution)
function lazy<T>(factory: () => Promise<T>): () => Promise<T> {
  let promise: Promise<T> | null = null;
  return () => {
    if (!promise) {
      promise = factory();
    }
    return promise;
  };
}

// Typed deferred pattern
interface Deferred<T> {
  promise: Promise<T>;
  resolve: (value: T | PromiseLike<T>) => void;
  reject: (reason?: unknown) => void;
}

function createDeferred<T>(): Deferred<T> {
  let resolve!: Deferred<T>["resolve"];
  let reject!: Deferred<T>["reject"];

  const promise = new Promise<T>((res, rej) => {
    resolve = res;
    reject = rej;
  });

  return { promise, resolve, reject };
}

// Usage
const deferred = createDeferred<User>();
deferred.promise.then((user) => console.log(user));
// Later:
deferred.resolve({ id: 1, name: "Alice", email: "" });

// Promise.tee - consume a promise multiple times
function tee<T>(promise: Promise<T>): [Promise<T>, Promise<T>] {
  let cached: T | undefined;
  let error: unknown;
  let settled = false;

  const shared = promise.then(
    (val) => { cached = val; settled = true; return val; },
    (err) => { error = err; settled = true; throw err; }
  );

  const duplicate = promise.then(
    (val) => { if (settled) return cached as T; return val; },
    (err) => { if (settled) throw error; throw err; }
  );

  return [shared, duplicate];
}
```

---

## Interview Questions

1. **What is the difference between `Promise.all` and `Promise.allSettled`?**
   `Promise.all` rejects immediately if any promise rejects. `Promise.allSettled` waits for all promises to settle and returns their results regardless of success or failure.

2. **How do you handle errors in promise chains?**
   Use `.catch()` at the end of the chain, or use `.then(onFulfilled, onRejected)` with both handlers. Always ensure errors are either handled or re-thrown.

3. **What is the difference between `.then().catch()` and `.catch()` on its own?**
   `.then(fn).catch(handler)` catches errors from both the previous promise AND `fn`. `.then(fn, errorHandler)` only catches errors from the previous promise, not from `fn`.

4. **What is Promise.any and when would you use it?**
   `Promise.any` resolves with the first fulfilled promise. Use it for fallback strategies where you have multiple sources for the same data.

5. **Explain the deferred pattern and its use cases.**
   A deferred separates promise creation from resolution. Useful when the resolver needs to be stored and called from a different context.

6. **What is promisification and why is it useful?**
   Converting callback-based functions to return promises. It enables using async/await and modern error handling with legacy APIs.

7. **How does `Promise.allSettled` handle typing?**
   Each element is typed as `PromiseSettledResult<T>` with discriminated union on `status` property ("fulfilled" | "rejected").

8. **What happens if you call `resolve` multiple times on a promise?**
   Only the first call takes effect. Subsequent calls are ignored. The promise stays in its first settled state.

9. **What is the difference between `Promise.resolve(x)` and `new Promise(r => r(x))`?**
   Functionally equivalent, but `Promise.resolve` has special handling for thenables (objects with a `.then` method), unwrapping them immediately.

10. **What is the "unhandled rejection" problem?**
    When a promise rejects without a `.catch()` handler, the rejection goes unhandled. In Node.js, this triggers a warning or crash depending on the version.

11. **How do you implement a promise-based timeout?**
    Use `Promise.race` with the actual promise and a timer promise that rejects after the specified delay.

12. **What is `Promise.try`?**
    A proposal that wraps synchronous or async functions, catching both sync errors and async rejections. Currently Stage 4 and available in most runtimes.

13. **Can you convert `Promise.all` to `Promise.allSettled` behavior manually?**
    Yes, by wrapping each promise with `.then(v => ({status: 'fulfilled', value: v})).catch(e => ({status: 'rejected', reason: e}))`.

14. **What is the Promise constructor anti-pattern?**
    Wrapping an already-promise-based function in `new Promise()`, which can cause subtle bugs like unhandled rejections or lost error context.

15. **How do you limit promise concurrency?**
    Implement a pool that tracks executing promises and waits for at least one to complete before starting new ones.
