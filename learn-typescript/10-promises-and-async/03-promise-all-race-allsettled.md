# Promise.all, Promise.race, Promise.allSettled, Promise.any

## Table of Contents

- [Promise.all](#promiseall)
- [Promise.race](#promiserace)
- [Promise.allSettled](#promiseallsettled)
- [Promise.any](#promiseany)
- [Comparison Matrix](#comparison-matrix)
- [When to Use Which](#when-to-use-which)
- [Performance Considerations](#performance-considerations)
- [Error Handling Patterns](#error-handling-patterns)
- [Interview Questions](#interview-questions)

---

## Promise.all

`Promise.all` takes an iterable of promises and returns a single promise that resolves when all input promises resolve, or rejects if any input promise rejects.

### Type Signature

```typescript
interface PromiseConstructor {
  all<T extends readonly unknown[] | []>(
    values: T
  ): Promise<{ -readonly [P in keyof T]: Awaited<T[P]> }>;

  all<T>(values: Iterable<T | PromiseLike<T>>): Promise<Awaited<T>[]>;
}
```

### Basic Usage with Types

```typescript
// Tuple inference - preserves individual types
const results = await Promise.all([
  Promise.resolve(1),         // number
  Promise.resolve("hello"),   // string
  Promise.resolve(true),      // boolean
]);
// Type: [number, string, boolean]

// Explicit tuple type
const tuple = await Promise.all<[
  Promise<User>,
  Promise<Post[]>,
  Promise<Comment[]>
]>([
  fetchUser(1),
  fetchPosts(1),
  fetchComments(1),
]);
// Type: [User, Post[], Comment[]]

// Array of same type
const users = await Promise.all<number>(
  [1, 2, 3].map((id) => fetchUser(id).then((u) => u.id))
);
// Type: number[]
```

### Real-World Example: Parallel API Calls

```typescript
interface DashboardData {
  user: User;
  posts: Post[];
  notifications: Notification[];
  stats: Stats;
}

async function loadDashboard(userId: number): Promise<DashboardData> {
  const [user, posts, notifications, stats] = await Promise.all([
    fetchUser(userId),
    fetchPosts(userId),
    fetchNotifications(userId),
    fetchStats(userId),
  ]);

  return { user, posts, notifications, stats };
}

// With typed error handling
async function loadDashboardSafe(userId: number): Promise<DashboardData | null> {
  try {
    const [user, posts, notifications, stats] = await Promise.all([
      fetchUser(userId),
      fetchPosts(userId),
      fetchNotifications(userId),
      fetchStats(userId),
    ]);
    return { user, posts, notifications, stats };
  } catch (error) {
    console.error("Failed to load dashboard:", error);
    return null;
  }
}
```

### Promise.all with Empty Arrays

```typescript
const empty = await Promise.all([]);           // never[]
const emptyTyped = await Promise.all<never>([]); // never[]

// Safe handling of dynamic arrays
async function fetchItems(ids: number[]): Promise<Item[]> {
  if (ids.length === 0) return [];
  return Promise.all(ids.map(fetchItem));
}
```

### Error Behavior

```typescript
// Promise.all rejects IMMEDIATELY with the first rejection
// Other promises continue executing but their results are ignored

const p1 = new Promise((resolve) => setTimeout(() => resolve(1), 100));
const p2 = new Promise((_, reject) => setTimeout(() => reject(new Error("fail")), 50));
const p3 = new Promise((resolve) => setTimeout(() => resolve(3), 200));

try {
  await Promise.all([p1, p2, p3]);
} catch (error) {
  // Catches the rejection from p2 after ~50ms
  // p1 and p3 still resolve but their results are lost
}
```

### Transforming Promise.all Results

```typescript
// Map results to a different shape
const userNames = await Promise.all(
  ids.map(async (id) => {
    const user = await fetchUser(id);
    return user.name;
  })
);

// Create a map from results
const userMap = new Map(
  await Promise.all(
    ids.map(async (id) => {
      const user = await fetchUser(id);
      return [id, user] as const;
    })
  )
);
```

---

## Promise.race

`Promise.race` returns a promise that resolves or rejects with the first settled promise's result.

### Type Signature

```typescript
interface PromiseConstructor {
  race<T>(
    values: Iterable<T | PromiseLike<T>>
  ): Promise<Awaited<T>>;
}
```

### Basic Usage

```typescript
// First to settle wins
const first = await Promise.race([
  fetch("/api/source1"),
  fetch("/api/source2"),
  fetch("/api/source3"),
]);

// Race with different types (note: TypeScript may infer union type)
const result = await Promise.race([
  Promise.resolve(42),       // number
  Promise.resolve("hello"),  // string
]);
// Type: number | string
```

### Timeout Pattern

```typescript
function withTimeout<T>(promise: Promise<T>, ms: number): Promise<T> {
  return Promise.race([
    promise,
    new Promise<never>((_, reject) =>
      setTimeout(() => reject(new Error(`Timeout after ${ms}ms`)), ms)
    ),
  ]);
}

// Usage
const user = await withTimeout(fetchUser(1), 5000);
```

### AbortController with Race

```typescript
function fetchWithTimeout(url: string, timeoutMs: number): Promise<Response> {
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), timeoutMs);

  return Promise.race([
    fetch(url, { signal: controller.signal }),
    new Promise<never>((_, reject) => {
      setTimeout(() => reject(new Error("Timeout")), timeoutMs);
    }),
  ]).finally(() => clearTimeout(timeoutId));
}
```

### First Successful Response

```typescript
async function firstSuccess<T>(
  operations: Array<() => Promise<T>>
): Promise<T> {
  return Promise.race(operations.map((op) => op()));
}

// ⚠️ Warning: If the first settled promise is a rejection,
// Promise.race rejects immediately, even if others would succeed
```

### Error Behavior

```typescript
// Promise.race settles with the FIRST settled promise
// If the first settled promise rejects, race rejects

const fastReject = new Promise((_, reject) =>
  setTimeout(() => reject(new Error("fast fail")), 10)
);
const slowResolve = new Promise((resolve) =>
  setTimeout(() => resolve("slow success"), 100)
);

try {
  await Promise.race([fastReject, slowResolve]);
} catch (error) {
  // Catches the rejection from fastReject
  // slowResolve is ignored
}
```

---

## Promise.allSettled

`Promise.allSettled` waits for all promises to settle (fulfill or reject) and returns an array of results.

### Type Signature

```typescript
interface PromiseConstructor {
  allSettled<T extends readonly unknown[] | []>(
    values: T
  ): Promise<{
    -readonly [P in keyof T]:
      | { readonly status: "fulfilled"; readonly value: Awaited<T[P]> }
      | { readonly status: "rejected"; readonly reason: unknown };
  }>;

  allSettled<T>(
    values: Iterable<T | PromiseLike<T>>
  ): Promise<
    Array<
      | { status: "fulfilled"; value: Awaited<T> }
      | { status: "rejected"; reason: unknown }
    >
  >;
}
```

### Basic Usage

```typescript
const results = await Promise.allSettled([
  Promise.resolve(1),
  Promise.reject(new Error("fail")),
  Promise.resolve(3),
]);

// results type:
// Array<
//   | { status: "fulfilled"; value: number }
//   | { status: "rejected"; reason: Error }
// >

results.forEach((result) => {
  if (result.status === "fulfilled") {
    console.log("Value:", result.value); // TypeScript knows value is number
  } else {
    console.log("Error:", result.reason);
  }
});
```

### Type Narrowing Helpers

```typescript
function isFulfilled<T>(
  result: PromiseSettledResult<T>
): result is PromiseFulfilledResult<T> {
  return result.status === "fulfilled";
}

function isRejected(
  result: PromiseSettledResult<unknown>
): result is PromiseRejectedResult {
  return result.status === "rejected";
}

// Usage
const results = await Promise.allSettled([
  fetchUser(1),
  fetchUser(2),
  fetchUser(3),
]);

const successfulUsers = results.filter(isFulfilled).map((r) => r.value);
const failedIds = results
  .filter(isRejected)
  .map((r, i) => ({ index: i, error: r.reason }));
```

### Real-World Example: Batch Processing

```typescript
interface BatchResult<T> {
  successful: T[];
  failed: Array<{ item: unknown; error: unknown }>;
}

async function batchProcess<TInput, TOutput>(
  items: TInput[],
  processor: (item: TInput) => Promise<TOutput>,
  concurrency: number = 5
): Promise<BatchResult<TOutput>> {
  const results = await Promise.allSettled(
    chunk(items, concurrency).flat().map(processor)
  );

  const successful: TOutput[] = [];
  const failed: Array<{ item: unknown; error: unknown }> = [];

  results.forEach((result, index) => {
    if (isFulfilled(result)) {
      successful.push(result.value);
    } else {
      failed.push({ item: items[index], error: result.reason });
    }
  });

  return { successful, failed };
}
```

### Error Behavior

```typescript
// Promise.allSettled NEVER rejects
// It always resolves with an array of settled results

const results = await Promise.allSettled([
  Promise.reject(new Error("fail1")),
  Promise.reject(new Error("fail2")),
  Promise.reject(new Error("fail3")),
]);

// All three rejections are captured in results
// No rejection propagates
console.log(results.every((r) => r.status === "rejected")); // true
```

---

## Promise.any

`Promise.any` takes an iterable of promises and returns a promise that resolves with the first fulfilled promise. If all promises reject, it rejects with an `AggregateError`.

### Type Signature

```typescript
interface PromiseConstructor {
  any<T extends readonly unknown[] | []>(
    values: T
  ): Promise<Awaited<T[number]>>;

  any<T>(values: Iterable<T | PromiseLike<T>>): Promise<Awaited<T>>;
}
```

### Basic Usage

```typescript
// First to fulfill wins
const result = await Promise.any([
  Promise.reject(new Error("fail")),
  Promise.resolve("success"),
  Promise.reject(new Error("fail2")),
]);
// result: "success"

// All fail
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

### Fallback Data Sources

```typescript
interface DataSource {
  fetch: () => Promise<Data>;
  name: string;
}

async function fetchWithFallback(sources: DataSource[]): Promise<Data> {
  return Promise.any(
    sources.map((source) =>
      source.fetch().catch((error) => {
        console.warn(`${source.name} failed:`, error.message);
        throw error;
      })
    )
  );
}

// Usage
const data = await fetchWithFallback([
  { name: "Primary API", fetch: () => fetchFromPrimary() },
  { name: "Secondary API", fetch: () => fetchFromSecondary() },
  { name: "Cache", fetch: () => fetchFromCache() },
]);
```

### Geographic Fallback

```typescript
async function fetchFromNearestRegion<T>(
  regions: Array<{ url: string; region: string }>
): Promise<T> {
  return Promise.any(
    regions.map(async ({ url, region }) => {
      const response = await fetch(url);
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      return response.json() as Promise<T>;
    })
  );
}

const data = await fetchFromNearestRegion([
  { url: "https://us.api.example.com", region: "us" },
  { url: "https://eu.api.example.com", region: "eu" },
  { url: "https://ap.api.example.com", region: "ap" },
]);
```

### Error Behavior

```typescript
// Promise.any rejects with AggregateError if ALL promises reject
// It IGNORES rejections until all fail

const result = await Promise.any([
  Promise.reject(new Error("first")),
  Promise.resolve("winner"),
  Promise.reject(new Error("third")),
]);
// result: "winner" - the rejection from "first" is ignored

// All rejections are collected in AggregateError
try {
  await Promise.any([
    Promise.reject(new Error("error1")),
    Promise.reject(new Error("error2")),
  ]);
} catch (error) {
  console.log(error instanceof AggregateError); // true
  console.log(error.errors.length); // 2
}
```

---

## Comparison Matrix

| Feature | Promise.all | Promise.race | Promise.allSettled | Promise.any |
|---|---|---|---|---|
| **Resolves when** | All fulfill | First settles | All settle | First fulfills |
| **Rejects when** | Any rejects | First rejects | Never | All reject |
| **Result type** | Array of values | Single value | Array of results | Single value |
| **Error handling** | Stops on first error | Uses first settled | Captures all errors | Collects in AggregateError |
| **Empty input** | Resolves `[]` | Rejects | Resolves `[]` | Rejects |
| **Best for** | Parallel independent ops | Timeout/competition | Reporting all results | Fallback sources |

```typescript
// Side-by-side type comparison
const allResult = await Promise.all([
  Promise.resolve(1),
  Promise.resolve("a"),
]);
// Type: [number, string]

const raceResult = await Promise.race([
  Promise.resolve(1),
  Promise.resolve("a"),
]);
// Type: number | string

const settledResult = await Promise.allSettled([
  Promise.resolve(1),
  Promise.resolve("a"),
]);
// Type: Array<
//   | { status: "fulfilled"; value: number }
//   | { status: "fulfilled"; value: string }
//   | { status: "rejected"; reason: unknown }
// >

const anyResult = await Promise.any([
  Promise.resolve(1),
  Promise.resolve("a"),
]);
// Type: number | string
```

---

## When to Use Which

### Promise.all - Parallel Independent Operations

```typescript
// When you need ALL results and operations are independent
const [user, settings, notifications] = await Promise.all([
  fetchUser(id),
  fetchSettings(id),
  fetchNotifications(id),
]);
```

### Promise.race - Timeout or Competition

```typescript
// When you need the fastest response
const fastest = await Promise.race([
  fetchFromPrimary(),
  fetchFromCache(),
]);

// When you need timeout protection
const result = await Promise.race([
  longRunningOperation(),
  new Promise((_, reject) => setTimeout(() => reject(new Error("timeout")), 5000)),
]);
```

### Promise.allSettled - Batch Operations with Error Reporting

```typescript
// When you want to know which succeeded and which failed
const results = await Promise.allSettled(
  userIds.map((id) => updateUserProfile(id, data))
);

const summary = {
  succeeded: results.filter((r) => r.status === "fulfilled").length,
  failed: results.filter((r) => r.status === "rejected").length,
};
```

### Promise.any - Fallback Strategy

```typescript
// When you have multiple sources and any one will do
const data = await Promise.any([
  fetchFromPrimaryDB(),
  fetchFromReplicaDB(),
  fetchFromCache(),
]);
```

---

## Performance Considerations

```typescript
// ❌ Creating many promises eagerly
const promises = Array.from({ length: 1000 }, (_, i) => fetchItem(i));
const results = await Promise.all(promises);

// ✅ Limit concurrency to avoid overwhelming the system
async function parallelLimited<T>(
  items: number[],
  limit: number,
  fn: (id: number) => Promise<T>
): Promise<T[]> {
  const results: T[] = [];
  const executing = new Set<Promise<void>>();

  for (const item of items) {
    const p = fn(item).then((result) => {
      results.push(result);
    }).then(() => {
      executing.delete(p);
    });
    executing.add(p);

    if (executing.size >= limit) {
      await Promise.race(executing);
    }
  }

  await Promise.all(executing);
  return results;
}

// Memory consideration: Promise.allSettled keeps all results
// even if most failed. For very large arrays, consider streaming.
```

---

## Error Handling Patterns

```typescript
// Pattern 1: Partial failure tolerance
async function resilientAll<T>(
  promises: Promise<T>[]
): Promise<Array<{ status: "fulfilled"; value: T } | { status: "rejected"; error: unknown }>> {
  const results = await Promise.allSettled(promises);
  return results.map((r) =>
    r.status === "fulfilled"
      ? { status: "fulfilled", value: r.value }
      : { status: "rejected", error: r.reason }
  );
}

// Pattern 2: Fail-fast with context
async function failFast<T>(
  operations: Array<{ name: string; execute: () => Promise<T> }>
): Promise<T[]> {
  return Promise.all(
    operations.map(async ({ name, execute }) => {
      try {
        return await execute();
      } catch (error) {
        throw new Error(`Operation "${name}" failed: ${error}`);
      }
    })
  );
}

// Pattern 3: Retry with race
async function withRetry<T>(
  fn: () => Promise<T>,
  retries: number = 3,
  delay: number = 1000
): Promise<T> {
  return Promise.any(
    Array.from({ length: retries }, (_, i) =>
      new Promise<T>((resolve, reject) => {
        setTimeout(async () => {
          try {
            resolve(await fn());
          } catch (error) {
            reject(error);
          }
        }, i * delay);
      })
    )
  );
}
```

---

## Interview Questions

1. **What happens when one promise in `Promise.all` rejects?**
   `Promise.all` immediately rejects with that error. Other promises continue executing but their results are ignored.

2. **How does `Promise.allSettled` differ from `Promise.all`?**
   `Promise.allSettled` never rejects. It waits for all promises to settle and returns their statuses and results, regardless of success or failure.

3. **When would you use `Promise.any` over `Promise.race`?**
   When you want the first successful result and don't care about intermediate failures. `Promise.race` rejects on the first settled rejection, while `Promise.any` ignores rejections until all fail.

4. **What is `AggregateError`?**
   A special error type that wraps multiple errors. Used by `Promise.any` when all promises reject, providing access to all individual rejection reasons via the `.errors` property.

5. **How do you type `Promise.allSettled` results?**
   Each element is `PromiseSettledResult<T>` - a discriminated union with `status: "fulfilled"` or `status: "rejected"`.

6. **What is the performance implication of using `Promise.all` with many promises?**
   All promises start executing immediately. If you have thousands of async operations, this can overwhelm the system. Use a concurrency limiter.

7. **Can `Promise.all` accept an empty array?**
   Yes, it resolves immediately with an empty array `[]`.

8. **Can `Promise.any` accept an empty array?**
   No, it rejects immediately with an `AggregateError` containing zero errors.

9. **How do you implement a timeout with `Promise.race`?**
   Race the actual promise against a promise that rejects after a delay using `setTimeout`.

10. **What happens to unresolved promises when `Promise.race` settles?**
    They continue executing in the background. JavaScript doesn't cancel promises. You'd need `AbortController` for cancellation.

11. **How do you get partial results from `Promise.all`?**
    You can't - it either gives all results or throws. Use `Promise.allSettled` instead for partial results.

12. **What is the difference between `Promise.all` and `Promise.allSettled` for error handling?**
    `Promise.all` fails fast on first error. `Promise.allSettled` collects all results including errors, allowing you to handle failures individually.

13. **How do you handle different promise types in `Promise.all`?**
    TypeScript infers a tuple type. Use explicit type annotations or `as const` for precise typing.

14. **What is the "Promise.all anti-pattern"?**
    Using `Promise.all` when promises depend on each other (sequential execution needed), or not using `Promise.all` when operations are independent.

15. **How does `Promise.any` handle duplicate fulfillments?**
    It resolves with the first fulfilled promise and ignores subsequent fulfillments, similar to how `Promise.race` handles the first settled promise.
