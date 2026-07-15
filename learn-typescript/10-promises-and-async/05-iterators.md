# Iterators in TypeScript

## Table of Contents

- [Iterator Protocol](#iterator-protocol)
- [Iterable Protocol](#iterable-protocol)
- [Iterator Type Definitions](#iterator-type-definitions)
- [Custom Iterables](#custom-iterables)
- [for...of with Custom Iterators](#forof-with-custom-iterators)
- [Iterator Utilities](#iterator-utilities)
- [Async Iterators](#async-iterators)
- [Built-in Iterables](#built-in-iterables)
- [Interview Questions](#interview-questions)

---

## Iterator Protocol

The iterator protocol defines a standard way to produce a sequence of values.

```typescript
// Iterator interface
interface Iterator<T, TReturn = any, TNext = unknown> {
  next(...args: [] | [TNext]): IteratorResult<T, TReturn>;
  return?(value?: TReturn): IteratorResult<T, TReturn>;
  throw?(e?: any): IteratorResult<T, TReturn>;
}

// IteratorResult
interface IteratorResult<T, TReturn = any> {
  done: boolean;
  value: T;
}

// When done is true, value is the return value (TReturn)
interface IteratorYieldResult<TYield> {
  done: false;
  value: TYield;
}

interface IteratorReturnResult<TReturn> {
  done: true;
  value: TReturn;
}

// Basic iterator example
class Counter implements Iterator<number> {
  private count = 0;

  next(): IteratorResult<number> {
    if (this.count < 5) {
      return { value: this.count++, done: false };
    }
    return { value: undefined, done: true };
  }

  return(value?: number): IteratorResult<number> {
    console.log("Iterator returned with:", value);
    return { value, done: true };
  }
}

const counter = new Counter();
console.log(counter.next()); // { value: 0, done: false }
console.log(counter.next()); // { value: 1, done: false }
console.log(counter.next()); // { value: 2, done: false }
console.log(counter.return(100)); // { value: 100, done: true }
```

---

## Iterable Protocol

The iterable protocol defines how to create an iterator.

```typescript
// Iterable interface
interface Iterable<T> {
  [Symbol.iterator](): Iterator<T>;
}

// IterableIterator combines both protocols
interface IterableIterator<T> extends Iterator<T> {
  [Symbol.iterator](): IterableIterator<T>;
}

// Simple iterable class
class Range implements Iterable<number> {
  constructor(
    private start: number,
    private end: number
  ) {}

  [Symbol.iterator](): Iterator<number> {
    let current = this.start;
    const end = this.end;

    return {
      next(): IteratorResult<number> {
        if (current <= end) {
          return { value: current++, done: false };
        }
        return { value: undefined, done: true };
      },
    };
  }
}

// Usage
const range = new Range(1, 5);
for (const num of range) {
  console.log(num); // 1, 2, 3, 4, 5
}

// Spread operator works with iterables
const array = [...new Range(1, 5)]; // [1, 2, 3, 4, 5]

// Destructuring works with iterables
const [first, second, ...rest] = new Range(1, 10);
// first = 1, second = 2, rest = [3, 4, 5, 6, 7, 8, 9, 10]

// Array.from works with iterables
const fromIterable = Array.from(new Range(1, 5)); // [1, 2, 3, 4, 5]
```

---

## Iterator Type Definitions

```typescript
// TypeScript provides several built-in iterator types

// Iterable<T>
interface Iterable<T> {
  [Symbol.iterator](): Iterator<T>;
}

// IterableIterator<T>
interface IterableIterator<T> extends Iterator<T> {
  [Symbol.iterator](): IterableIterator<T>;
}

// Iterator<T, TReturn, TNext>
interface Iterator<T, TReturn = any, TNext = unknown> {
  next(...args: [] | [TNext]): IteratorResult<T, TReturn>;
  return?(value?: TReturn): IteratorResult<T, TReturn>;
  throw?(e?: any): IteratorResult<T, TReturn>;
}

// ReadableStream specific
interface ReadableStreamIterator<T> {
  [Symbol.asyncIterator](): AsyncIterableIterator<T>;
}

// Map entries, keys, values
declare global {
  interface Map<K, V> {
    entries(): IterableIterator<[K, V]>;
    keys(): IterableIterator<K>;
    values(): IterableIterator<V>;
  }

  interface Set<T> {
    entries(): IterableIterator<[T, T]>;
    keys(): IterableIterator<T>;
    values(): IterableIterator<T>;
  }
}

// Custom iterator with complex type
interface Employee {
  id: number;
  name: string;
  department: string;
}

class EmployeeDirectory implements Iterable<Employee> {
  private employees: Employee[] = [];

  add(employee: Employee): void {
    this.employees.push(employee);
  }

  [Symbol.iterator](): Iterator<Employee> {
    let index = 0;
    const employees = this.employees;

    return {
      next(): IteratorResult<Employee> {
        if (index < employees.length) {
          return { value: employees[index++], done: false };
        }
        return { value: undefined as unknown as Employee, done: true };
      },
    };
  }
}
```

---

## Custom Iterables

```typescript
// Fibonacci iterable
class Fibonacci implements Iterable<number> {
  constructor(private limit: number) {}

  [Symbol.iterator](): Iterator<number> {
    let a = 0;
    let b = 1;
    let count = 0;
    const limit = this.limit;

    return {
      next(): IteratorResult<number> {
        if (count >= limit) {
          return { value: undefined, done: true };
        }
        const value = a;
        [a, b] = [b, a + b];
        count++;
        return { value, done: false };
      },
    };
  }
}

const fibs = [...new Fibonacci(10)]; // [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]

// Binary tree with in-order traversal
class TreeNode<T> {
  left?: TreeNode<T>;
  right?: TreeNode<T>;

  constructor(public value: T) {}
}

class BinaryTree<T> implements Iterable<T> {
  constructor(private root?: TreeNode<T>) {}

  [Symbol.iterator](): Iterator<T> {
    const stack: TreeNode<T>[] = [];
    let current = this.root;

    return {
      next(): IteratorResult<T> {
        while (current || stack.length > 0) {
          while (current) {
            stack.push(current);
            current = current.left;
          }
          current = stack.pop()!;
          const value = current.value;
          current = current.right;
          return { value, done: false };
        }
        return { value: undefined as unknown as T, done: true };
      },
    };
  }
}

// Linked list iterable
class LinkedListNode<T> {
  constructor(
    public value: T,
    public next?: LinkedListNode<T>
  ) {}
}

class LinkedList<T> implements Iterable<T> {
  head?: LinkedListNode<T>;

  append(value: T): void {
    const node = new LinkedListNode(value);
    if (!this.head) {
      this.head = node;
      return;
    }
    let current = this.head;
    while (current.next) current = current.next;
    current.next = node;
  }

  [Symbol.iterator](): Iterator<T> {
    let current = this.head;

    return {
      next(): IteratorResult<T> {
        if (current) {
          const value = current.value;
          current = current.next;
          return { value, done: false };
        }
        return { value: undefined as unknown as T, done: true };
      },
    };
  }
}

const list = new LinkedList<number>();
list.append(1);
list.append(2);
list.append(3);
console.log([...list]); // [1, 2, 3]

// Map-like with custom iteration
class SortedMap<K, V> implements Iterable<[K, V]> {
  private entries: [K, V][] = [];
  private sortFn: (a: K, b: K) => number;

  constructor(sortFn: (a: K, b: K) => number) {
    this.sortFn = sortFn;
  }

  set(key: K, value: V): void {
    this.entries.push([key, value]);
    this.entries.sort((a, b) => this.sortFn(a[0], b[0]));
  }

  [Symbol.iterator](): Iterator<[K, V]> {
    let index = 0;
    const entries = this.entries;

    return {
      next(): IteratorResult<[K, V]> {
        if (index < entries.length) {
          return { value: entries[index++], done: false };
        }
        return { value: undefined, done: true };
      },
    };
  }
}
```

---

## for...of with Custom Iterators

```typescript
// for...of automatically calls [Symbol.iterator]()
class Countdown implements Iterable<string> {
  constructor(private start: number) {}

  [Symbol.iterator](): Iterator<string> {
    let current = this.start;

    return {
      next(): IteratorResult<string> {
        if (current <= 0) {
          return { value: "Go!", done: false };
        }
        return { value: String(current--), done: false };
      },
    };
  }
}

for (const msg of new Countdown(3)) {
  console.log(msg); // "3", "2", "1", "Go!"
}

// Destructuring with custom iterators
class Coordinate {
  constructor(public x: number, public y: number) {}

  [Symbol.iterator](): Iterator<number> {
    let index = 0;
    const values = [this.x, this.y];

    return {
      next(): IteratorResult<number> {
        if (index < values.length) {
          return { value: values[index++], done: false };
        }
        return { value: undefined, done: true };
      },
    };
  }
}

const [x, y] = new Coordinate(10, 20); // x = 10, y = 20

// Spread operator
const coords = [...new Coordinate(1, 2)]; // [1, 2]

// Array.from
const asArray = Array.from(new Coordinate(3, 4)); // [3, 4]

// Array destructuring with rest
const [first, ...remaining] = new Coordinate(10, 20); // first = 10, remaining = [20]
```

---

## Iterator Utilities

```typescript
// Map iterator
function* map<T, R>(
  iterable: Iterable<T>,
  fn: (item: T) => R
): IterableIterator<R> {
  for (const item of iterable) {
    yield fn(item);
  }
}

// Filter iterator
function* filter<T>(
  iterable: Iterable<T>,
  predicate: (item: T) => boolean
): IterableIterator<T> {
  for (const item of iterable) {
    if (predicate(item)) yield item;
  }
}

// Take iterator
function* take<T>(
  iterable: Iterable<T>,
  count: number
): IterableIterator<T> {
  let taken = 0;
  for (const item of iterable) {
    if (taken >= count) return;
    yield item;
    taken++;
  }
}

// Skip iterator
function* skip<T>(
  iterable: Iterable<T>,
  count: number
): IterableIterator<T> {
  let skipped = 0;
  for (const item of iterable) {
    if (skipped >= count) yield item;
    else skipped++;
  }
}

// Chain utility
function chain<T>(...iterables: Iterable<T>[]): IterableIterator<T> {
  return (function* () {
    for (const iterable of iterables) {
      yield* iterable;
    }
  })();
}

// Enumerate
function* enumerate<T>(
  iterable: Iterable<T>,
  start: number = 0
): IterableIterator<[number, T]> {
  let index = start;
  for (const item of iterable) {
    yield [index++, item];
  }
}

// Zip
function* zip<A, B>(
  iterableA: Iterable<A>,
  iterableB: Iterable<B>
): IterableIterator<[A, B]> {
  const iterA = iterableA[Symbol.iterator]();
  const iterB = iterableB[Symbol.iterator]();

  while (true) {
    const a = iterA.next();
    const b = iterB.next();
    if (a.done || b.done) return;
    yield [a.value, b.value];
  }
}

// Usage of utilities
const result = take(
  filter(
    map(new Range(1, 100), (x) => x * 2),
    (x) => x % 3 === 0
  ),
  5
);
console.log([...result]); // [6, 12, 18, 24, 30]
```

---

## Async Iterators

```typescript
// Async iterable and async iterator interfaces
interface AsyncIterable<T> {
  [Symbol.asyncIterator](): AsyncIterator<T>;
}

interface AsyncIterator<T, TReturn = any, TNext = unknown> {
  next(...args: [] | [TNext]): Promise<IteratorResult<T, TReturn>>;
  return?(value?: TReturn): Promise<IteratorResult<T, TReturn>>;
  throw?(e?: any): Promise<IteratorResult<T, TReturn>>;
}

// Async generator function (most common way to create async iterables)
async function* fetchPages(url: string): AsyncIterableIterator<Response> {
  let page = 1;
  while (true) {
    const response = await fetch(`${url}?page=${page}`);
    if (!response.ok) break;
    yield response;
    const data = await response.json();
    if (!data.nextPage) break;
    page++;
  }
}

// for await...of loop
async function processPages() {
  for await (const page of fetchPages("https://api.example.com/posts")) {
    const data = await page.json();
    console.log(data);
  }
}

// Manual async iterator
class AsyncRange implements AsyncIterable<number> {
  constructor(
    private start: number,
    private end: number,
    private delay: number
  ) {}

  [Symbol.asyncIterator](): AsyncIterator<number> {
    let current = this.start;
    const end = this.end;
    const delay = this.delay;

    return {
      async next(): Promise<IteratorResult<number>> {
        if (current <= end) {
          await new Promise((resolve) => setTimeout(resolve, delay));
          return { value: current++, done: false };
        }
        return { value: undefined, done: true };
      },
    };
  }
}

// Consume async iterable
async function consumeAsync() {
  const asyncRange = new AsyncRange(1, 5, 100);
  for await (const num of asyncRange) {
    console.log(num); // 1, 2, 3, 4, 5 (with 100ms delay between each)
  }
}
```

---

## Built-in Iterables

```typescript
// String is iterable
for (const char of "hello") {
  console.log(char); // 'h', 'e', 'l', 'l', 'o'
}

// Array is iterable
for (const item of [1, 2, 3]) {
  console.log(item);
}

// Map is iterable
const map = new Map([["a", 1], ["b", 2]]);
for (const [key, value] of map) {
  console.log(key, value);
}

// Set is iterable
const set = new Set([1, 2, 3]);
for (const item of set) {
  console.log(item);
}

// TypedArray is iterable
const typedArray = new Uint8Array([1, 2, 3]);
for (const item of typedArray) {
  console.log(item);
}

// NodeList is iterable
const elements = document.querySelectorAll("div");
for (const el of elements) {
  console.log(el.textContent);
}

// Arguments object is iterable
function example() {
  for (const arg of arguments) {
    console.log(arg);
  }
}

// Generator is iterable
function* gen() {
  yield 1;
  yield 2;
}
for (const val of gen()) {
  console.log(val);
}

// Plain objects are NOT iterable
// for (const [key, value] of {}) {} // Error!
// Use Object.entries() instead
for (const [key, value] of Object.entries({ a: 1, b: 2 })) {
  console.log(key, value);
}
```

---

## Interview Questions

1. **What is the difference between Iterator and Iterable?**
   An iterator has a `next()` method. An iterable has `[Symbol.iterator]()` that returns an iterator.

2. **How does `for...of` work with custom iterables?**
   It calls `[Symbol.iterator]()` to get an iterator, then repeatedly calls `next()` until `done` is true.

3. **What is `Symbol.iterator`?**
   A well-known symbol that objects implement to be iterable. It's the key that connects an object to the `for...of` loop.

4. **Can you make a plain object iterable?**
   Yes, by implementing `[Symbol.iterator]()` method.

5. **What is the difference between `for...in` and `for...of`?**
   `for...in` iterates over enumerable property keys. `for...of` iterates over the values of an iterable.

6. **How do you implement a bidirectional iterator?**
   Use `TNext` type parameter and pass values to `generator.next(value)`.

7. **What are the three methods of the Iterator protocol?**
   `next()`, `return()`, and `throw()`.

8. **What is the difference between synchronous and asynchronous iterators?**
   Sync iterators have `next()` returning `IteratorResult<T>`. Async iterators have `next()` returning `Promise<IteratorResult<T>>`.

9. **How do you create a custom iterable class?**
   Implement `[Symbol.iterator]()` that returns an iterator with `next()` method.

10. **What is the purpose of the `return()` method on iterators?**
    It's called when iteration is early-terminated (e.g., `break` in `for...of`), allowing cleanup.

11. **How do generators relate to iterators?**
    Generator functions return objects that implement both the Iterator and Iterable protocols.

12. **What is the `done` property used for?**
    When `done: true`, the iteration stops. The `value` property contains the return value if any.

13. **How do you iterate over a Map's entries?**
    Use `for (const [key, value] of map)` or `for (const [key, value] of map.entries())`.

14. **Can you spread an iterable into an array?**
    Yes, using `[...iterable]` or `Array.from(iterable)`.

15. **What is the `TNext` type parameter in `Iterator<T, TReturn, TNext>`?**
    It specifies the type of values that can be passed to `next()` for bidirectional communication.
