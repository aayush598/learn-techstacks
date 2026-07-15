# Promises & Async Patterns - Interview Questions

## Table of Contents

- [Promise Fundamentals](#promise-fundamentals)
- [Async/Await](#asyncawait)
- [Promise Combinators](#promise-combinators)
- [Generators & Iterators](#generators--iterators)
- [Async Generators](#async-generators)
- [Observables](#observables)
- [Code Challenges](#code-challenges)
- [System Design](#system-design)

---

## Promise Fundamentals

### Q1: What is the difference between a Promise and a callback?

**Answer:** A Promise is an object representing the eventual completion of an asynchronous operation. It provides better error handling through `.catch()`, supports chaining with `.then()`, and integrates with `async/await`. Callbacks lead to "callback hell" when nested deeply, while promises provide a linear, readable flow.

```typescript
// Callback hell
getUser(id, (err, user) => {
  getPosts(user.id, (err, posts) => {
    getComments(posts[0].id, (err, comments) => {
      console.log(comments);
    });
  });
});

// Promise chain
getUser(id)
  .then((user) => getPosts(user.id))
  .then((posts) => getComments(posts[0].id))
  .then((comments) => console.log(comments))
  .catch(handleError);
```

### Q2: What are the three states of a Promise?

**Answer:**
1. **Pending**: Initial state, neither fulfilled nor rejected
2. **Fulfilled**: The operation completed successfully
3. **Rejected**: The operation failed

Once settled (fulfilled or rejected), a promise cannot change state.

### Q3: What happens if you call resolve() multiple times?

**Answer:** Only the first call takes effect. Subsequent calls are ignored. The promise remains in its first settled state.

```typescript
const p = new Promise<string>((resolve) => {
  resolve("first");   // Takes effect
  resolve("second");  // Ignored
  resolve("third");   // Ignored
});

p.then((v) => console.log(v)); // "first"
```

### Q4: What is the difference between .then().catch() and .then(onFulfilled, onRejected)?

**Answer:** `.then(onFulfilled).catch(handler)` catches errors from BOTH the original promise AND the `onFulfilled` callback. `.then(onFulfilled, onRejected)` only catches errors from the original promise, not from `onFulfilled`.

```typescript
// This catches the error from the .then callback
Promise.resolve(1)
  .then(() => { throw new Error("error in then"); })
  .catch((e) => console.log("caught:", e)); // ✅ Catches

// This does NOT catch the error from the .then callback
Promise.resolve(1)
  .then(
    () => { throw new Error("error in then"); },
    (e) => console.log("caught:", e) // ❌ Not caught
  );
```

### Q5: What is a thenable?

**Answer:** A thenable is any object with a `.then()` method. `Promise.resolve()` will unwrap thenables, converting them to promises. This enables interoperability with non-standard promise implementations.

```typescript
const thenable = {
  then(resolve: (value: number) => void) {
    resolve(42);
  }
};

Promise.resolve(thenable).then(console.log); // 42
```

### Q6: What is the "unhandled rejection" problem?

**Answer:** When a promise rejects without a `.catch()` handler, it becomes an unhandled rejection. In Node.js, this triggers warnings and can crash the process. Modern runtimes have `unhandledRejection` events.

```typescript
// Unhandled rejection
Promise.reject(new Error("fail"));
// Node.js emits UnhandledPromiseRejectionWarning

// Properly handled
Promise.reject(new Error("fail")).catch(console.error);
```

### Q7: What is the Promise constructor anti-pattern?

**Answer:** Wrapping an already-promise-based function in `new Promise()`. This can cause subtle bugs like swallowed errors or lost stack traces.

```typescript
// ❌ Anti-pattern
function getUser(id: number): Promise<User> {
  return new Promise((resolve, reject) => {
    fetchUser(id).then(resolve).catch(reject);
  });
}

// ✅ Correct
function getUser(id: number): Promise<User> {
  return fetchUser(id);
}
```

### Q8: How do you implement a promise-based delay?

**Answer:**
```typescript
function delay(ms: number): Promise<void> {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

// Usage
async function main() {
  console.log("start");
  await delay(1000);
  console.log("end");
}
```

### Q9: What is the deferred pattern?

**Answer:** A deferred separates promise creation from resolution. The resolve and reject functions are exposed externally, allowing promises to be resolved from a different context.

```typescript
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
```

### Q10: What is the difference between `Promise.resolve(x)` and `new Promise(r => r(x))`?

**Answer:** Functionally equivalent for plain values. However, `Promise.resolve` has special handling for thenables - if `x` is a thenable, `Promise.resolve` will unwrap it synchronously when possible, while `new Promise(r => r(x))` wraps it as a PromiseLike.

---

## Async/Await

### Q11: Can you use `await` outside of an `async` function?

**Answer:** Yes, with top-level await in ES modules. Requires `"module": "ES2022"` or later in tsconfig.json. Before top-level await, you'd use an async IIFE.

```typescript
// Top-level await (ES modules)
import { readFile } from "fs/promises";
const content = await readFile("file.txt", "utf-8");

// Async IIFE (alternative)
(async () => {
  const content = await readFile("file.txt", "utf-8");
})();
```

### Q12: What happens if you forget to `await` a promise?

**Answer:** The promise runs in the background. If it rejects, it becomes an unhandled rejection. TypeScript provides `noUncheckedSideEffectImports` to warn about this.

```typescript
async function example() {
  fetch("/api/data"); // ⚠️ Unawaited promise
  // If this rejects, it's unhandled
}
```

### Q13: How do you handle errors in async functions?

**Answer:** Multiple approaches:

```typescript
// 1. Try/catch
async function example() {
  try {
    await riskyOperation();
  } catch (error) {
    console.error(error);
  }
}

// 2. Result type (functional)
type Result<T> = { ok: true; value: T } | { ok: false; error: Error };

async function safeExample(): Promise<Result<User>> {
  try {
    const user = await riskyOperation();
    return { ok: true, value: user };
  } catch (error) {
    return { ok: false, error: error as Error };
  }
}

// 3. .catch() on the returned promise
async function example2() {
  const result = await riskyOperation().catch(() => defaultValue);
}
```

### Q14: What is the `Promise.all` anti-pattern with async/await?

**Answer:** Using `await` sequentially when operations are independent and could run in parallel.

```typescript
// ❌ Sequential (slow)
async function loadPage() {
  const user = await fetchUser();    // 1s
  const posts = await fetchPosts();  // 1s
  const comments = await fetchComments(); // 1s
  // Total: ~3s
}

// ✅ Parallel (fast)
async function loadPage() {
  const [user, posts, comments] = await Promise.all([
    fetchUser(),
    fetchPosts(),
    fetchComments(),
  ]);
  // Total: ~1s
}
```

### Q15: How do you convert a `.then` chain to `async/await`?

**Answer:** Replace `.then()` with `await`, and `.catch()` with `try/catch`.

```typescript
// .then chain
function loadDashboard(id: number) {
  return fetchUser(id)
    .then((user) => fetchPosts(user.id))
    .then((posts) => processPosts(posts))
    .catch((error) => fallback(error));
}

// async/await
async function loadDashboard(id: number) {
  try {
    const user = await fetchUser(id);
    const posts = await fetchPosts(user.id);
    return processPosts(posts);
  } catch (error) {
    return fallback(error);
  }
}
```

---

## Promise Combinators

### Q16: When would you use Promise.any over Promise.race?

**Answer:** When you want the first successful result and don't care about intermediate failures. `Promise.race` rejects on the first settled rejection, while `Promise.any` ignores rejections until all fail.

```typescript
// Race: first settled wins (resolve OR reject)
const fastest = await Promise.race([
  fetch("https://api1.com"), // Might reject
  fetch("https://api2.com"),
]);

// Any: first fulfilled wins (ignores rejections)
const firstSuccess = await Promise.any([
  fetch("https://api1.com"), // If this rejects, tries next
  fetch("https://api2.com"),
]);
```

### Q17: What is the AggregateError in Promise.any?

**Answer:** When all promises in `Promise.any` reject, it throws an `AggregateError` containing all rejection reasons in the `.errors` property.

```typescript
try {
  await Promise.any([
    Promise.reject(new Error("fail1")),
    Promise.reject(new Error("fail2")),
  ]);
} catch (error) {
  if (error instanceof AggregateError) {
    console.log(error.errors); // [Error: fail1, Error: fail2]
  }
}
```

### Q18: How do you implement a timeout with Promise.race?

**Answer:**
```typescript
function withTimeout<T>(promise: Promise<T>, ms: number): Promise<T> {
  const timeout = new Promise<never>((_, reject) => {
    setTimeout(() => reject(new Error(`Timeout after ${ms}ms`)), ms);
  });
  return Promise.race([promise, timeout]);
}

// Usage
const user = await withTimeout(fetchUser(1), 5000);
```

### Q19: What happens to unresolved promises when Promise.race settles?

**Answer:** They continue executing in the background. JavaScript doesn't cancel promises. You need `AbortController` for actual cancellation.

```typescript
function fetchWithTimeout(url: string, ms: number): Promise<Response> {
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), ms);

  return Promise.race([
    fetch(url, { signal: controller.signal }),
    new Promise<never>((_, reject) =>
      setTimeout(() => reject(new Error("timeout")), ms)
    ),
  ]).finally(() => clearTimeout(timeoutId));
}
```

### Q20: How do you implement a promise concurrency limiter?

**Answer:**
```typescript
async function parallel<T>(
  tasks: Array<() => Promise<T>>,
  concurrency: number
): Promise<T[]> {
  const results: T[] = [];
  const executing = new Set<Promise<void>>();

  for (const task of tasks) {
    const p = task()
      .then((result) => results.push(result))
      .then(() => executing.delete(p));

    executing.add(p);

    if (executing.size >= concurrency) {
      await Promise.race(executing);
    }
  }

  await Promise.all(executing);
  return results;
}
```

---

## Generators & Iterators

### Q21: What is the difference between yield and yield*?

**Answer:** `yield` produces a single value. `yield*` delegates to another iterable (generator, array, string, etc.), forwarding all its yields.

```typescript
function* inner() {
  yield 1;
  yield 2;
}

function* outer() {
  yield 0;
  yield* inner(); // Delegates - yields 1, 2
  yield 3;
}

[...outer()]; // [0, 1, 2, 3]
```

### Q22: How do generators implement lazy evaluation?

**Answer:** Code after `yield` only executes when `.next()` is called. Values are computed on-demand, not pre-computed. This is memory-efficient for large or infinite sequences.

```typescript
function* fibonacci(): Generator<number> {
  let a = 0, b = 1;
  while (true) {
    yield a;
    [a, b] = [b, a + b];
  }
}

// Only computes values when consumed
const first10 = [...take(fibonacci(), 10)];
```

### Q23: How do you make a custom class iterable?

**Answer:** Implement the `[Symbol.iterator]()` method that returns an iterator with a `next()` method.

```typescript
class Range implements Iterable<number> {
  constructor(private start: number, private end: number) {}

  [Symbol.iterator](): Iterator<number> {
    let current = this.start;
    return {
      next: () =>
        current <= this.end
          ? { value: current++, done: false }
          : { value: undefined, done: true },
    };
  }
}

for (const num of new Range(1, 5)) console.log(num);
```

### Q24: What is the difference between for...in and for...of?

**Answer:** `for...in` iterates over enumerable property keys (objects). `for...of` iterates over the values of an iterable (arrays, strings, maps, sets, generators).

```typescript
const obj = { a: 1, b: 2 };
for (const key in obj) console.log(key); // "a", "b"

const arr = [1, 2, 3];
for (const val of arr) console.log(val); // 1, 2, 3
```

---

## Async Generators

### Q25: What is an async generator?

**Answer:** A function that combines async functions and generators - can `await` promises and `yield` values lazily.

```typescript
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

for await (const page of fetchPages("/api/posts")) {
  console.log(page);
}
```

### Q26: How does `for await...of` differ from `for...of`?

**Answer:** `for await...of` handles async iterables, awaiting each value. `for...of` handles synchronous iterables only.

```typescript
// Sync
for (const value of syncIterable) { /* ... */ }

// Async
for await (const value of asyncIterable) { /* ... */ }
```

### Q27: What is `Symbol.asyncIterator`?

**Answer:** The async equivalent of `Symbol.iterator`. Objects implement this to be async iterable and work with `for await...of`.

---

## Observables

### Q28: What is the difference between Subject, BehaviorSubject, and ReplaySubject?

**Answer:**
- **Subject**: No initial value, only emits to current subscribers
- **BehaviorSubject**: Has a current value, emits it immediately to new subscribers
- **ReplaySubject**: Replays previous N values to new subscribers

### Q29: When would you use an Observable over a Promise?

**Answer:** When you need multiple values over time, cancellation, complex transformation chains, or real-time data streams. For simple request-response, use promises.

### Q30: What is multicasting?

**Answer:** Sharing a single subscription among multiple subscribers. Subjects enable multicasting. Without it, each subscription creates a new execution.

```typescript
// Unicast (each subscriber gets new execution)
const cold = new Observable<number>((subscriber) => {
  console.log("New execution");
  subscriber.next(Math.random());
});

cold.subscribe(console.log); // "New execution", random
cold.subscribe(console.log); // "New execution", different random

// Multicast (shared execution)
const subject = new Subject<number>();
subject.subscribe(console.log);
subject.subscribe(console.log);
subject.next(Math.random()); // Same value to both subscribers
```

---

## Code Challenges

### Q31: Implement a promise retry function

```typescript
function retry<T>(
  fn: () => Promise<T>,
  retries: number,
  delay: number
): Promise<T> {
  return fn().catch((err) => {
    if (retries <= 0) throw err;
    return new Promise((resolve) => setTimeout(resolve, delay))
      .then(() => retry(fn, retries - 1, delay));
  });
}

// Usage
const data = await retry(() => fetch("/api"), 3, 1000);
```

### Q32: Implement Promise.all from scratch

```typescript
function promiseAll<T>(promises: Promise<T>[]): Promise<T[]> {
  return new Promise((resolve, reject) => {
    const results: T[] = [];
    let completed = 0;

    if (promises.length === 0) {
      resolve([]);
      return;
    }

    promises.forEach((promise, index) => {
      promise
        .then((value) => {
          results[index] = value;
          completed++;
          if (completed === promises.length) resolve(results);
        })
        .catch(reject);
    });
  });
}
```

### Q33: Implement an observable from scratch

```typescript
class Observable<T> {
  constructor(private subscribeFn: (observer: { next: (v: T) => void; error: (e: unknown) => void; complete: () => void }) => () => void) {}

  subscribe(observer: { next: (v: T) => void; error?: (e: unknown) => void; complete?: () => void }) {
    return this.subscribeFn({
      next: observer.next,
      error: observer.error ?? (() => {}),
      complete: observer.complete ?? (() => {}),
    });
  }
}

// Usage
const interval$ = new Observable<number>((observer) => {
  let count = 0;
  const id = setInterval(() => observer.next(count++), 1000);
  return () => clearInterval(id);
});

const sub = interval$.subscribe({ next: (v) => console.log(v) });
setTimeout(() => sub.unsubscribe(), 5000);
```

### Q34: Implement a debounce with promises

```typescript
function debounce<T>(fn: (...args: unknown[]) => Promise<T>, ms: number) {
  let timeoutId: ReturnType<typeof setTimeout>;
  let latestResolve: ((value: T) => void) | null = null;

  return (...args: unknown[]): Promise<T> => {
    return new Promise<T>((resolve) => {
      if (latestResolve) latestResolve = null;
      latestResolve = resolve;

      clearTimeout(timeoutId);
      timeoutId = setTimeout(async () => {
        const result = await fn(...args);
        if (latestResolve === resolve) {
          resolve(result);
        }
      }, ms);
    });
  };
}
```

### Q35: What is the output of this code?

```typescript
async function async1() {
  console.log("async1 start");
  await async2();
  console.log("async1 end");
}

async function async2() {
  console.log("async2");
}

console.log("script start");

setTimeout(() => {
  console.log("setTimeout");
}, 0);

async1();

new Promise((resolve) => {
  console.log("promise1");
  resolve(undefined);
}).then(() => {
  console.log("promise2");
});

console.log("script end");
```

**Answer:**
```
script start
async1 start
async2
promise1
script end
async1 end
promise2
setTimeout
```

Explanation: Microtasks (promises) execute before macrotasks (setTimeout). `await` yields back to the event loop.

---

## System Design

### Q36: How would you design a typed event emitter?

```typescript
type EventMap = {
  "user:login": { userId: string; timestamp: number };
  "user:logout": { userId: string };
  "data:received": { data: unknown };
};

class TypedEventEmitter<Events extends Record<string, unknown>> {
  private listeners = new Map<keyof Events, Set<(data: any) => void>>();

  on<K extends keyof Events>(event: K, listener: (data: Events[K]) => void): () => void {
    if (!this.listeners.has(event)) {
      this.listeners.set(event, new Set());
    }
    this.listeners.get(event)!.add(listener);
    return () => this.listeners.get(event)?.delete(listener);
  }

  emit<K extends keyof Events>(event: K, data: Events[K]): void {
    this.listeners.get(event)?.forEach((listener) => listener(data));
  }
}

// Usage - fully typed
const emitter = new TypedEventEmitter<EventMap>();
emitter.on("user:login", (data) => {
  console.log(data.userId);  // ✅ TypeScript knows userId exists
  console.log(data.foo);     // ❌ Error: foo doesn't exist
});
```

### Q37: How would you implement retry logic with exponential backoff?

```typescript
async function retryWithBackoff<T>(
  fn: () => Promise<T>,
  maxRetries: number = 5,
  baseDelay: number = 1000,
  maxDelay: number = 30000
): Promise<T> {
  let lastError: unknown;

  for (let attempt = 0; attempt <= maxRetries; attempt++) {
    try {
      return await fn();
    } catch (error) {
      lastError = error;

      if (attempt < maxRetries) {
        const delay = Math.min(
          baseDelay * Math.pow(2, attempt) + Math.random() * 1000,
          maxDelay
        );
        await new Promise((resolve) => setTimeout(resolve, delay));
      }
    }
  }

  throw lastError;
}
```
