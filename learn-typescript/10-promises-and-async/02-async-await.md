# Async/Await in TypeScript

## Table of Contents

- [Async Function Basics](#async-function-basics)
- [Await Expression](#await-expression)
- [Return Type Inference](#return-type-inference)
- [Error Handling](#error-handling)
- [Parallel vs Sequential Execution](#parallel-vs-sequential-execution)
- [Async IIFE](#async-iife)
- [Async Arrow Functions](#async-arrow-functions)
- [Top-Level Await](#top-level-await)
- [Advanced Patterns](#advanced-patterns)
- [Common Pitfalls](#common-pitfalls)
- [Interview Questions](#interview-questions)

---

## Async Function Basics

An `async` function is a function that implicitly returns a `Promise`. The `await` keyword pauses execution until a promise settles.

```typescript
// Basic async function
async function fetchUser(id: number): Promise<User> {
  const response = await fetch(`/api/users/${id}`);
  const user: User = await response.json();
  return user;
}

// Async function always returns a Promise, even if you return a plain value
async function getString(): Promise<string> {
  return "hello"; // Automatically wrapped in Promise.resolve("hello")
}

async function getNumber(): Promise<number> {
  return 42; // Promise<number>, not number
}

// Explicit return type (recommended for public APIs)
async function getData(): Promise<Data> {
  const result = await fetchData();
  return result;
}

// Implicit return type (works but less explicit)
async function getDataImplicit() {
  const result = await fetchData();
  return result; // TypeScript infers Promise<Data>
}
```

---

## Await Expression

`await` can only be used inside an `async` function (unless using top-level await).

```typescript
// Await a promise
async function example() {
  const result = await Promise.resolve(42);
  console.log(result); // 42, not Promise<number>
}

// Await with destructuring
async function fetchUserWithPosts(id: number): Promise<{
  user: User;
  posts: Post[];
}> {
  const [user, posts] = await Promise.all([
    fetchUser(id),
    fetchPosts(id),
  ]);
  return { user, posts };
}

// Await in conditional
async function maybeFetch(url: string | null): Promise<string | null> {
  if (!url) return null;
  const response = await fetch(url);
  return response.text();
}

// Await in loops (sequential by default)
async function fetchAllUsers(ids: number[]): Promise<User[]> {
  const users: User[] = [];
  for (const id of ids) {
    const user = await fetchUser(id); // Each waits for the previous
    users.push(user);
  }
  return users;
}

// Await in loops (parallel)
async function fetchAllUsersParallel(ids: number[]): Promise<User[]> {
  const promises = ids.map((id) => fetchUser(id));
  return Promise.all(promises); // All run concurrently
}
```

---

## Return Type Inference

TypeScript infers async function return types, but explicit annotations are best practice for exported functions.

```typescript
// TypeScript infers the return type
async function inferred() {
  return { name: "Alice", age: 30 };
}
// Type: Promise<{ name: string; age: number }>

// Explicit return type (recommended)
interface Person {
  name: string;
  age: number;
}

async function explicit(): Promise<Person> {
  return { name: "Alice", age: 30 };
}

// Union return type
async function findUser(id: number): Promise<User | null> {
  try {
    return await fetchUser(id);
  } catch {
    return null;
  }
}

// Generic async function
async function fetchData<T>(url: string): Promise<T> {
  const response = await fetch(url);
  return response.json() as Promise<T>;
}

// Overloaded async functions
function process(id: number): Promise<User>;
function process(name: string): Promise<User[]>;
async function process(input: number | string): Promise<User | User[]> {
  if (typeof input === "number") {
    return fetchUser(input);
  }
  return searchUsers(input);
}

// ReturnType utility type
type FetchResult = ReturnType<typeof fetchUser>; // Promise<User>
type AwaitedFetchResult = Awaited<ReturnType<typeof fetchUser>>; // User

// Async functions with never return type
async function throwError(message: string): Promise<never> {
  throw new Error(message);
}

// Async functions returning Promise<void>
async function logAndForget(message: string): Promise<void> {
  console.log(message);
  // Implicitly returns Promise<void>
}
```

---

## Error Handling

```typescript
// Basic try/catch/finally
async function fetchWithHandling(url: string): Promise<Data> {
  try {
    const response = await fetch(url);
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }
    const data = await response.json();
    return data as Data;
  } catch (error) {
    if (error instanceof TypeError) {
      // Network error
      console.error("Network error:", error.message);
    } else if (error instanceof SyntaxError) {
      // JSON parse error
      console.error("Parse error:", error.message);
    } else {
      console.error("Unknown error:", error);
    }
    throw error; // Re-throw or return fallback
  } finally {
    console.log("Request completed");
  }
}

// Error typing in catch blocks (TypeScript 4.0+)
async function typedCatch() {
  try {
    const response = await fetch("/api/data");
    return await response.json();
  } catch (error) {
    if (error instanceof Error) {
      console.error(error.message); // TypeScript narrows error to Error
    }
    throw error;
  }
}

// Catch without block scope (TS 4.0+)
async function catchClause() {
  try {
    await fetch("/api");
  } catch (e: unknown) {
    if (e instanceof Error) {
      console.log(e.message);
    }
  }
}

// Custom error classes
class AppError extends Error {
  constructor(
    message: string,
    public code: string,
    public statusCode: number = 500
  ) {
    super(message);
    this.name = "AppError";
  }
}

class NotFoundError extends AppError {
  constructor(resource: string) {
    super(`${resource} not found`, "NOT_FOUND", 404);
    this.name = "NotFoundError";
  }
}

// Typed error handling with discriminated unions
type Result<T, E = Error> =
  | { ok: true; value: T }
  | { ok: false; error: E };

async function safeFetch<T>(url: string): Promise<Result<T>> {
  try {
    const response = await fetch(url);
    if (!response.ok) {
      return { ok: false, error: new AppError("HTTP error", "HTTP_ERROR", response.status) };
    }
    const data = await response.json() as T;
    return { ok: true, value: data };
  } catch (error) {
    return {
      ok: false,
      error: error instanceof Error ? error : new Error(String(error)),
    };
  }
}

// Using the Result type
async function handleUser() {
  const result = await safeFetch<User>("/api/user/1");
  if (result.ok) {
    console.log(result.value.name); // TypeScript knows result.value is User
  } else {
    console.error(result.error.message); // TypeScript knows result.error is Error
  }
}
```

---

## Parallel vs Sequential Execution

```typescript
// ❌ Sequential - slow (runs one after another)
async function sequential(): Promise<[User, Post[], Comment[]]> {
  const user = await fetchUser(1);       // 1 second
  const posts = await fetchPosts(1);     // 1 second
  const comments = await fetchComments(1); // 1 second
  return [user, posts, comments];        // Total: ~3 seconds
}

// ✅ Parallel - fast (runs all at once)
async function parallel(): Promise<[User, Post[], Comment[]]> {
  const [user, posts, comments] = await Promise.all([
    fetchUser(1),
    fetchPosts(1),
    fetchComments(1),
  ]);
  return [user, posts, comments]; // Total: ~1 second
}

// Mixed: some parallel, some sequential
async function mixed(): Promise<{
  user: User;
  postsWithComments: Array<Post & { comments: Comment[] }>;
}> {
  // Step 1: Fetch user and posts in parallel
  const [user, posts] = await Promise.all([
    fetchUser(1),
    fetchPosts(1),
  ]);

  // Step 2: Fetch comments for each post (parallel per post)
  const postsWithComments = await Promise.all(
    posts.map(async (post) => {
      const comments = await fetchComments(post.id);
      return { ...post, comments };
    })
  );

  return { user, postsWithComments };
}

// Sequential with accumulator
async function processSequentially<T, R>(
  items: T[],
  fn: (item: T, prev: R) => Promise<R>,
  initial: R
): Promise<R> {
  let accumulator = initial;
  for (const item of items) {
    accumulator = await fn(item, accumulator);
  }
  return accumulator;
}

// Parallel with concurrency limit
async function parallelWithLimit<T>(
  items: T[],
  limit: number,
  fn: (item: T) => Promise<unknown>
): Promise<void> {
  const executing = new Set<Promise<void>>();

  for (const item of items) {
    const task = fn(item).then(() => {
      executing.delete(task);
    });
    executing.add(task);

    if (executing.size >= limit) {
      await Promise.race(executing);
    }
  }

  await Promise.all(executing);
}
```

---

## Async IIFE

```typescript
// Async Immediately Invoked Function Expression
(async () => {
  try {
    const user = await fetchUser(1);
    console.log(user.name);
  } catch (error) {
    console.error(error);
  }
})();

// Async arrow IIFE
const result = (async () => {
  const data = await fetchData();
  return data;
})();

// result is Promise<Data>
const resolved = await result;

// Useful for module-level initialization
const config = (async (): Promise<AppConfig> => {
  const response = await fetch("/config.json");
  return response.json() as Promise<AppConfig>;
})();

// Top-level await is preferred over async IIFE in modern TypeScript
```

---

## Async Arrow Functions

```typescript
// Basic async arrow function
const getUser = async (id: number): Promise<User> => {
  const response = await fetch(`/api/users/${id}`);
  return response.json() as Promise<User>;
};

// One-liner async arrow
const getName = async (id: number) => (await fetchUser(id)).name;

// Async arrow in callbacks
const userIds = [1, 2, 3];
const users = await Promise.all(
  userIds.map(async (id) => {
    const user = await fetchUser(id);
    return { ...user, fetchedAt: new Date() };
  })
);

// Async arrow as event handler
const handleSubmit = async (event: Event) => {
  event.preventDefault();
  const data = await collectFormData();
  await submitData(data);
};

// Generic async arrow function
const fetchData = async <T>(url: string): Promise<T> => {
  const response = await fetch(url);
  return response.json() as Promise<T>;
};

// Curried async function
const fetchWithAuth = (token: string) => async <T>(url: string): Promise<T> => {
  const response = await fetch(url, {
    headers: { Authorization: `Bearer ${token}` },
  });
  return response.json() as Promise<T>;
};

const authedFetch = fetchWithAuth("my-token");
const userData = await authedFetch<User>("/api/user");
```

---

## Top-Level Await

```typescript
// Top-level await allows using await at the module level
// Requires: module: "ESNext" or "ES2022" in tsconfig.json

// Before top-level await (Node.js)
import { readFile } from "fs/promises";
const content = await readFile("file.txt", "utf-8");

// Top-level await (modern)
import { readFile } from "fs/promises";
const content = await readFile("file.txt", "utf-8");
console.log(content);

// Conditional initialization
let db: Database;
try {
  db = await createDatabase();
} catch {
  db = await createFallbackDatabase();
}

// Dynamic imports with top-level await
const module = await import("./heavy-module");
module.doSomething();

// Sequential initialization
const user = await fetchUser(1);
const posts = await fetchPosts(user.id);

// Parallel initialization
const [config, features] = await Promise.all([
  fetchConfig(),
  fetchFeatures(),
]);
```

---

## Advanced Patterns

```typescript
// Async generator usage
async function* fetchPages(url: string): AsyncGenerator<Page> {
  let page = 1;
  while (true) {
    const response = await fetch(`${url}?page=${page}`);
    const data = await response.json();
    if (data.length === 0) break;
    yield data;
    page++;
  }
}

// Async iteration
for await (const page of fetchPages("/api/posts")) {
  console.log(page);
}

// Promise.all with async map
async function mapAsync<T, R>(
  items: T[],
  fn: (item: T) => Promise<R>
): Promise<R[]> {
  return Promise.all(items.map(fn));
}

// Async filter
async function filterAsync<T>(
  items: T[],
  predicate: (item: T) => Promise<boolean>
): Promise<T[]> {
  const results = await Promise.all(items.map(predicate));
  return items.filter((_, i) => results[i]);
}

// Async reduce
async function reduceAsync<T, R>(
  items: T[],
  fn: (acc: R, item: T) => Promise<R>,
  initial: R
): Promise<R> {
  let accumulator = initial;
  for (const item of items) {
    accumulator = await fn(accumulator, item);
  }
  return accumulator;
}

// Async queue
class AsyncQueue<T> {
  private queue: Array<() => Promise<T>> = [];
  private running = 0;
  private concurrency: number;

  constructor(concurrency: number = 1) {
    this.concurrency = concurrency;
  }

  async add(task: () => Promise<T>): Promise<T> {
    return new Promise<T>((resolve, reject) => {
      this.queue.push(async () => {
        try {
          resolve(await task());
        } catch (error) {
          reject(error);
        }
      });
      this.processNext();
    });
  }

  private async processNext(): Promise<void> {
    if (this.running >= this.concurrency || this.queue.length === 0) return;

    this.running++;
    const task = this.queue.shift()!;

    try {
      await task();
    } finally {
      this.running--;
      this.processNext();
    }
  }
}
```

---

## Common Pitfalls

```typescript
// ❌ Pitfall 1: Unnecessary await in return
async function bad(): Promise<string> {
  return await fetch("url").then((r) => r.text()); // Redundant await
}

// ✅ Better
async function good(): Promise<string> {
  return fetch("url").then((r) => r.text()); // Let the caller await
}

// ❌ Pitfall 2: Missing await
async function bad(): Promise<void> {
  fetch("/api/data"); // Fire-and-forget - may cause unhandled rejection
}

// ✅ Better
async function good(): Promise<void> {
  await fetch("/api/data"); // Explicitly handle the promise
}

// ❌ Pitfall 3: Sequential when parallel is fine
async function bad(): Promise<[User, Post[]]> {
  const user = await fetchUser(1);
  const posts = await fetchPosts(1); // Could run in parallel
  return [user, posts];
}

// ✅ Better
async function good(): Promise<[User, Post[]]> {
  return Promise.all([fetchUser(1), fetchPosts(1)]);
}

// ❌ Pitfall 4: Using await in forEach
async function bad(): Promise<void> {
  const ids = [1, 2, 3];
  ids.forEach(async (id) => {
    await fetchUser(id); // forEach doesn't await!
  });
}

// ✅ Better
async function good(): Promise<void> {
  const ids = [1, 2, 3];
  await Promise.all(ids.map((id) => fetchUser(id)));
}
```

---

## Interview Questions

1. **What is the difference between `async/await` and `.then()` chains?**
   Both are syntactic sugar over promises. `async/await` provides imperative-style syntax that's easier to read and debug, with better stack traces.

2. **Can `await` be used outside of `async` functions?**
   Yes, with top-level await in ES modules (requires `"module": "ES2022"` or later in tsconfig.json).

3. **What happens if you forget to `await` a promise?**
   The promise runs in the background. If it rejects, it becomes an unhandled rejection. TypeScript 5.x has the `noUncheckedSideEffectImports` option to warn about this.

4. **How do you handle errors in async functions?**
   Use try/catch/finally, `.catch()` on the returned promise, or implement a Result type for type-safe error handling.

5. **What is the `Promise.all` anti-pattern with async/await?**
   Using `await` sequentially when `Promise.all` could run operations in parallel. Also, wrapping already-async functions in `Promise.all` unnecessarily.

6. **How do you convert a `.then` chain to `async/await`?**
   Replace `.then()` calls with `await` assignments, and move `.catch()` blocks to `try/catch`.

7. **What is an async IIFE and when do you use it?**
   An immediately invoked async function expression, used to run async code at module level before top-level await was available.

8. **What are the TypeScript compiler options for async/await?**
   `target: ES2017` or later for native async/await. Earlier targets use polyfills that add overhead.

9. **How does TypeScript type `async` functions that return `never`?**
   `async function fail(): Promise<never>` - the function always throws.

10. **What is the difference between `Promise.all` and sequential `await`?**
    `Promise.all` runs all promises concurrently. Sequential `await` runs one at a time. Use `Promise.all` when operations are independent.
