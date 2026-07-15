# Async Generators in TypeScript

## Table of Contents

- [Async Generator Syntax](#async-generator-syntax)
- [AsyncGenerator Type](#asyncgenerator-type)
- [Async Iterator Protocol](#async-iterator-protocol)
- [Async Iterable Protocol](#async-iterable-protocol)
- [for await...of](#for-awaitof)
- [Streaming Data Patterns](#streaming-data-patterns)
- [Async Generators for Pagination](#async-generators-for-pagination)
- [Real-World Examples](#real-world-examples)
- [Interview Questions](#interview-questions)

---

## Async Generator Syntax

An async generator function combines async functions and generator functions.

```typescript
// Basic async generator
async function* count(): AsyncGenerator<number> {
  for (let i = 0; i < 5; i++) {
    await delay(100);
    yield i;
  }
}

// Async generator with multiple types
async function* mixedTypes(): AsyncGenerator<number | string> {
  yield 1;
  await delay(100);
  yield "hello";
  await delay(100);
  yield 2;
}

// Async generator returning a value
async function* withReturn(): AsyncGenerator<number, string> {
  yield 1;
  yield 2;
  return "done";
}

// Usage
const gen = count();
console.log(await gen.next()); // { value: 0, done: false }
console.log(await gen.next()); // { value: 1, done: false }
// ... until done

// Async generator arrow function (limited use)
const asyncArrowGen = async function* (): AsyncGenerator<number> {
  yield 1;
  yield 2;
};
```

---

## AsyncGenerator Type

```typescript
// AsyncGenerator<TYield, TReturn, TNext>
// TYield: type of values yielded
// TReturn: type of the return value
// TNext: type of values passed into .next()

// Basic async generator type
async function* basic(): AsyncGenerator<number> {
  yield 1;
}

// With return type
async function* withReturn(): AsyncGenerator<number, string> {
  yield 1;
  return "finished";
}

// With next type (bidirectional)
async function* bidirectional(): AsyncGenerator<string, void, { action: string; data: number }> {
  while (true) {
    const input = yield "waiting";
    // input is typed as { action: string; data: number }
    console.log(input.action, input.data);
  }
}

// Complex type example
interface StreamEvent<T> {
  type: "data" | "error" | "end";
  payload: T;
  timestamp: number;
}

async function* eventStream<T>(): AsyncGenerator<StreamEvent<T>> {
  let connected = true;

  while (connected) {
    await delay(1000);
    yield {
      type: "data",
      payload: await fetchData(),
      timestamp: Date.now(),
    };
  }

  yield { type: "end", payload: null as unknown as T, timestamp: Date.now() };
}
```

---

## Async Iterator Protocol

```typescript
// Async iterator interface
interface AsyncIterator<T, TReturn = any, TNext = unknown> {
  next(...args: [] | [TNext]): Promise<IteratorResult<T, TReturn>>;
  return?(value?: TReturn): Promise<IteratorResult<T, TReturn>>;
  throw?(e?: any): Promise<IteratorResult<T, TReturn>>;
}

// Manual async iterator implementation
class AsyncRangeIterator implements AsyncIterator<number> {
  private current: number;
  private readonly end: number;
  private readonly delayMs: number;

  constructor(start: number, end: number, delayMs: number = 100) {
    this.current = start;
    this.end = end;
    this.delayMs = delayMs;
  }

  async next(): Promise<IteratorResult<number>> {
    if (this.current <= this.end) {
      await new Promise((resolve) => setTimeout(resolve, this.delayMs));
      return { value: this.current++, done: false };
    }
    return { value: undefined, done: true };
  }

  async return(value?: number): Promise<IteratorResult<number>> {
    console.log("Async iterator returning:", value);
    return { value, done: true };
  }

  async throw(error?: unknown): Promise<IteratorResult<number>> {
    throw error;
  }
}

// Async generator as iterator
async function* createIterator(): AsyncGenerator<number> {
  for (let i = 0; i < 5; i++) {
    await delay(100);
    yield i;
  }
}

// Both implement the same protocol
const manualIterator = new AsyncRangeIterator(0, 4);
const generatorIterator = createIterator();
```

---

## Async Iterable Protocol

```typescript
// Async iterable interface
interface AsyncIterable<T> {
  [Symbol.asyncIterator](): AsyncIterator<T>;
}

// Async iterable class
class AsyncRange implements AsyncIterable<number> {
  constructor(
    private start: number,
    private end: number,
    private delayMs: number = 100
  ) {}

  [Symbol.asyncIterator](): AsyncIterator<number> {
    let current = this.start;
    const end = this.end;
    const delayMs = this.delayMs;

    return {
      async next(): Promise<IteratorResult<number>> {
        if (current <= end) {
          await new Promise((resolve) => setTimeout(resolve, delayMs));
          return { value: current++, done: false };
        }
        return { value: undefined, done: true };
      },
    };
  }
}

// Consume with for await...of
async function consumeAsync() {
  for await (const num of new AsyncRange(1, 5)) {
    console.log(num);
  }
}

// Async generator functions automatically implement async iterable
async function* autoAsyncIterable(): AsyncGenerator<number> {
  for (let i = 0; i < 5; i++) {
    await delay(100);
    yield i;
  }
}

// Both are async iterables
const asyncRange = new AsyncRange(1, 5);
const asyncGen = autoAsyncIterable();

// Both can be used with for await...of
for await (const num of asyncRange) console.log(num);
for await (const num of asyncGen) console.log(num);
```

---

## for await...of

```typescript
// for await...of iterates over async iterables
async function processStream() {
  for await (const chunk of readableStream) {
    console.log(chunk);
  }
}

// Error handling with for await...of
async function safeProcessStream() {
  try {
    for await (const chunk of readableStream) {
      await processChunk(chunk);
    }
  } catch (error) {
    console.error("Stream processing failed:", error);
  }
}

// Early termination
async function findFirst() {
  for await (const item of asyncGenerator()) {
    if (item符合条件) return item;
  }
  return null;
}

// Destructuring in for await...of
async function* entries(): AsyncGenerator<[string, number]> {
  yield ["a", 1];
  yield ["b", 2];
}

async function processEntries() {
  for await (const [key, value] of entries()) {
    console.log(`${key}: ${value}`);
  }
}

// Combining sync and async iterables
async function* combined(): AsyncGenerator<string | number> {
  // Yield sync values
  yield* [1, 2, 3];

  // Yield async values
  for await (const val of asyncGenerator()) {
    yield val;
  }
}
```

---

## Streaming Data Patterns

```typescript
// Streaming API responses
async function* streamResponse(url: string): AsyncGenerator<string> {
  const response = await fetch(url);
  const reader = response.body!.getReader();
  const decoder = new TextDecoder();

  try {
    while (true) {
      const { done, value } = await reader.read();
      if (done) break;
      yield decoder.decode(value, { stream: true });
    }
  } finally {
    reader.releaseLock();
  }
}

// Usage
for await (const chunk of streamResponse("https://api.example.com/stream")) {
  process.stdout.write(chunk);
}

// Transform stream with async generator
async function* transformStream<TInput, TOutput>(
  source: AsyncIterable<TInput>,
  transformer: (input: TInput) => Promise<TOutput>
): AsyncGenerator<TOutput> {
  for await (const input of source) {
    yield await transformer(input);
  }
}

// Filter stream
async function* filterStream<T>(
  source: AsyncIterable<T>,
  predicate: (item: T) => Promise<boolean>
): AsyncGenerator<T> {
  for await (const item of source) {
    if (await predicate(item)) yield item;
  }
}

// Buffer stream (collect N items)
async function* bufferStream<T>(
  source: AsyncIterable<T>,
  size: number
): AsyncGenerator<T[]> {
  let buffer: T[] = [];

  for await (const item of source) {
    buffer.push(item);
    if (buffer.length >= size) {
      yield [...buffer];
      buffer = [];
    }
  }

  if (buffer.length > 0) yield buffer;
}

// Throttle stream
async function* throttleStream<T>(
  source: AsyncIterable<T>,
  intervalMs: number
): AsyncGenerator<T> {
  let lastYield = 0;

  for await (const item of source) {
    const now = Date.now();
    if (now - lastYield >= intervalMs) {
      yield item;
      lastYield = now;
    }
  }
}
```

---

## Async Generators for Pagination

```typescript
interface PaginatedResponse<T> {
  data: T[];
  pagination: {
    page: number;
    totalPages: number;
    hasNext: boolean;
  };
}

async function* paginate<T>(
  fetchPage: (page: number) => Promise<PaginatedResponse<T>>
): AsyncGenerator<T> {
  let page = 1;

  while (true) {
    const response = await fetchPage(page);

    for (const item of response.data) {
      yield item;
    }

    if (!response.pagination.hasNext) break;
    page++;
  }
}

// Usage
async function fetchUsers(page: number): Promise<PaginatedResponse<User>> {
  const response = await fetch(`/api/users?page=${page}`);
  return response.json();
}

async function processAllUsers() {
  for await (const user of paginate(fetchUsers)) {
    console.log(user.name);
  }
}

// Paginated with limit
async function* paginateWithLimit<T>(
  fetchPage: (page: number) => Promise<PaginatedResponse<T>>,
  limit: number
): AsyncGenerator<T> {
  let page = 1;
  let totalYielded = 0;

  while (totalYielded < limit) {
    const response = await fetchPage(page);

    for (const item of response.data) {
      if (totalYielded >= limit) return;
      yield item;
      totalYielded++;
    }

    if (!response.pagination.hasNext) break;
    page++;
  }
}

// Paginated with error handling
async function* safePaginate<T>(
  fetchPage: (page: number) => Promise<PaginatedResponse<T>>,
  maxRetries: number = 3
): AsyncGenerator<T> {
  let page = 1;

  while (true) {
    let retries = 0;

    while (retries < maxRetries) {
      try {
        const response = await fetchPage(page);

        for (const item of response.data) {
          yield item;
        }

        if (!response.pagination.hasNext) return;
        page++;
        break;
      } catch (error) {
        retries++;
        if (retries >= maxRetries) throw error;
        await delay(1000 * retries); // Exponential backoff
      }
    }
  }
}
```

---

## Real-World Examples

```typescript
// Real-time log streaming
async function* streamLogs(
  websocket: WebSocket
): AsyncGenerator<LogEntry> {
  const buffer: LogEntry[] = [];
  let resolve: ((value: IteratorResult<LogEntry>) => void) | null = null;

  websocket.onmessage = (event) => {
    const entry = JSON.parse(event.data) as LogEntry;
    if (resolve) {
      resolve({ value: entry, done: false });
      resolve = null;
    } else {
      buffer.push(entry);
    }
  };

  while (true) {
    if (buffer.length > 0) {
      yield buffer.shift()!;
    } else {
      const result = await new Promise<IteratorResult<LogEntry>>((r) => {
        resolve = r;
      });
      yield result.value;
    }
  }
}

// File watcher
async function* watchFiles(
  dir: string
): AsyncGenerator<{ type: string; path: string }> {
  const chokidar = await import("chokidar");
  const watcher = chokidar.watch(dir);

  const events: Array<{ type: string; path: string }> = [];
  let resolve: (() => void) | null = null;

  watcher.on("all", (type, path) => {
    events.push({ type, path });
    resolve?.();
    resolve = null;
  });

  while (true) {
    if (events.length > 0) {
      yield events.shift()!;
    } else {
      await new Promise<void>((r) => { resolve = r; });
    }
  }
}

// Database cursor
async function* queryCursor<T>(
  db: Database,
  query: string,
  batchSize: number = 100
): AsyncGenerator<T> {
  let offset = 0;

  while (true) {
    const results = await db.all<T>(
      `${query} LIMIT ? OFFSET ?`,
      [batchSize, offset]
    );

    if (results.length === 0) break;

    for (const row of results) {
      yield row;
    }

    offset += batchSize;

    if (results.length < batchSize) break;
  }
}

// GraphQL subscription
async function* subscribe<T>(
  client: GraphQLClient,
  query: string,
  variables?: Record<string, unknown>
): AsyncGenerator<T> {
  const observable = client.subscribe({ query, variables });
  const iterator = observable[Symbol.asyncIterator]();

  while (true) {
    const { value, done } = await iterator.next();
    if (done) break;
    yield value.data as T;
  }
}
```

---

## Interview Questions

1. **What is an async generator?**
   A function that is both async (can await promises) and a generator (can yield values lazily).

2. **What is the type signature of an async generator?**
   `AsyncGenerator<TYield, TReturn, TNext>` - similar to `Generator` but all methods return Promises.

3. **What is `for await...of`?**
   A loop that iterates over async iterables, awaiting each value before proceeding.

4. **How do async generators differ from regular generators?**
   Async generators can `await` promises inside and yield values asynchronously. Regular generators are synchronous.

5. **What is `Symbol.asyncIterator`?**
   The async equivalent of `Symbol.iterator`. Objects implement this to be async iterable.

6. **When would you use async generators over regular async functions?**
   For streaming data, paginated APIs, or when you need lazy evaluation of async operations.

7. **How do you handle errors in async generators?**
   Use try/catch inside the generator, or handle errors in the `for await...of` consumer.

8. **Can you use async generators with Node.js streams?**
   Yes, via `stream.pipeline()` or by implementing `Symbol.asyncIterator` on readable streams.

9. **What is the difference between `AsyncGenerator` and `AsyncIterableIterator`?**
   They're the same thing. `AsyncGenerator` is the more specific type.

10. **How do you implement backpressure with async generators?**
    Use `yield` - the generator pauses until the consumer calls `next()`, naturally applying backpressure.

11. **Can you convert a sync generator to an async generator?**
    Wrap yields in `yield await Promise.resolve(value)` or use `yield*` with async iterables.

12. **What happens when you call `return()` on an async generator?**
    The generator completes, returning the provided value. Cleanup code in `finally` blocks runs.

13. **How do async generators handle cleanup?**
    Use `finally` blocks inside the generator for cleanup (closing connections, releasing resources).

14. **What is the difference between `for await...of` and `Promise.all` with async generators?**
    `for await...of` processes values sequentially. `Promise.all` runs all promises concurrently.

15. **Can async generators be used with WebSockets?**
    Yes, they're excellent for modeling real-time data streams from WebSocket connections.
