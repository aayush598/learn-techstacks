# 10 - Loops

## Table of Contents

- [for Loop](#for-loop)
- [while Loop](#while-loop)
- [do...while Loop](#do-while-loop)
- [for...in Loop](#forin-loop)
- [for...of Loop](#forof-loop)
- [forEach with Typed Arrays](#foreach-with-typed-arrays)
- [Iteration Protocols in TypeScript](#iteration-protocols-in-typescript)
- [Loop Performance Considerations](#loop-performance-considerations)
- [Summary](#summary)

---

## for Loop

The classic `for` loop provides full control over iteration with initialization, condition, and update expressions.

### Basic Syntax

```typescript
// for (initialization; condition; update)
for (let i = 0; i < 5; i++) {
  console.log(i); // 0, 1, 2, 3, 4
}
```

### Iterating Arrays

```typescript
const fruits: string[] = ["apple", "banana", "cherry"];

for (let i = 0; i < fruits.length; i++) {
  console.log(fruits[i]);
}

// Reverse iteration
for (let i = fruits.length - 1; i >= 0; i--) {
  console.log(fruits[i]); // cherry, banana, apple
}
```

### Multiple Variables

```typescript
// Multiple initialization and update expressions
for (let i = 0, j = 10; i < j; i++, j--) {
  console.log(i, j);
  // 0 10, 1 9, 2 8, 3 7, 4 6
}
```

### Step Size

```typescript
// Skip elements
for (let i = 0; i < 20; i += 3) {
  console.log(i); // 0, 3, 6, 9, 12, 15, 18
}
```

### for Loop with Type Annotations

```typescript
// Typed loop variables
const numbers: number[] = [10, 20, 30, 40, 50];

for (let i: number = 0; i < numbers.length; i++) {
  const value: number = numbers[i];
  console.log(`Index ${i}: ${value}`);
}

// TypeScript infers types automatically
for (let i = 0; i < numbers.length; i++) {
  // i: number (inferred)
  // numbers[i]: number (inferred)
}
```

### break and continue

```typescript
// break — exit the loop early
for (let i = 0; i < 100; i++) {
  if (i === 5) break;
  console.log(i); // 0, 1, 2, 3, 4
}

// continue — skip current iteration
for (let i = 0; i < 10; i++) {
  if (i % 2 === 0) continue;
  console.log(i); // 1, 3, 5, 7, 9
}

// Labeled breaks for nested loops
outer: for (let i = 0; i < 5; i++) {
  for (let j = 0; j < 5; j++) {
    if (i === 2 && j === 3) break outer;
    console.log(i, j);
  }
}
```

### Infinite Loops

```typescript
// Infinite loop with break
while (true) {
  const input = getUserInput();
  if (input === "quit") break;
  processInput(input);
}

// Infinite for loop
for (;;) {
  const result = await fetchData();
  if (result.done) break;
}
```

---

## while Loop

The `while` loop continues as long as its condition is truthy.

### Basic Syntax

```typescript
let count: number = 0;
while (count < 5) {
  console.log(count);
  count++;
}
// 0, 1, 2, 3, 4
```

### while with Type Narrowing

```typescript
// Processing a queue
interface Task {
  id: number;
  name: string;
  status: "pending" | "processing" | "done";
}

function processTasks(tasks: Task[]): void {
  while (tasks.length > 0) {
    const task = tasks.shift();
    if (task) {
      // task: Task (not null — shift() returns T | undefined)
      task.status = "processing";
      console.log(`Processing: ${task.name}`);
      task.status = "done";
    }
  }
}
```

### while with Complex Conditions

```typescript
//等待 until condition is met
async function waitForValue(): Promise<string> {
  let result: string | null = null;

  while (result === null) {
    result = await fetchValue();
    if (result === null) {
      await sleep(1000);
    }
  }

  return result; // result: string (narrowed from string | null)
}
```

### while(true) Pattern

```typescript
// Event loop pattern
function startServer(): void {
  while (true) {
    const request = acceptConnection();
    handleRequest(request);
  }
}

// Polling pattern
async function pollForUpdates(): Promise<void> {
  while (true) {
    const updates = await checkForUpdates();
    if (updates.length > 0) {
      processUpdates(updates);
    }
    await sleep(5000);
  }
}
```

---

## do...while Loop

The `do...while` loop executes the body **at least once** before checking the condition.

### Basic Syntax

```typescript
let count: number = 0;
do {
  console.log(count);
  count++;
} while (count < 5);
// 0, 1, 2, 3, 4
```

### do...while vs while

```typescript
// while — may not execute at all
let x = 10;
while (x < 5) {
  console.log(x); // Never executes
}

// do...while — executes at least once
let y = 10;
do {
  console.log(y); // Executes once: 10
} while (y < 5);
```

### do...while for User Input

```typescript
// Menu-driven program
function showMenu(): string {
  let choice: string;

  do {
    console.log("1. New Game");
    console.log("2. Load Game");
    console.log("3. Quit");
    choice = prompt("Enter choice:") ?? "";
  } while (!["1", "2", "3"].includes(choice));

  return choice;
}
```

### do...while with Type Assertions

```typescript
// Parsing with retry
function parseInput(input: string): { valid: boolean; data?: unknown } {
  let result: { valid: boolean; data?: unknown };

  do {
    result = tryParse(input);
    if (!result.valid) {
      input = await getNewInput();
    }
  } while (!result.valid);

  return result; // result.data is definitely defined
}
```

---

## for...in Loop

The `for...in` loop iterates over **enumerable property keys** of an object.

### Basic Usage

```typescript
const user = { name: "Alice", age: 30, email: "alice@example.com" };

for (const key in user) {
  console.log(`${key}: ${user[key as keyof typeof user]}`);
}

// Output:
// name: Alice
// age: 30
// email: alice@example.com
```

### for...in with Type Safety

```typescript
// TypeScript requires type assertion with for...in
const obj = { a: 1, b: 2, c: 3 };

for (const key in obj) {
  // key: string (not "a" | "b" | "c")
  console.log(`${key}: ${obj[key as keyof typeof obj]}`);
}

// Safer approach using Object.keys
for (const key of Object.keys(obj)) {
  console.log(`${key}: ${obj[key as keyof typeof obj]}`);
}
```

### for...in with Inherited Properties

```typescript
// for...in iterates over inherited properties too
class Animal {
  name: string = "Animal";
}

class Dog extends Animal {
  breed: string = "Labrador";
}

const dog = new Dog();

for (const key in dog) {
  console.log(key); // "name", "breed" — both own and inherited
}

// Use hasOwnProperty to filter
for (const key in dog) {
  if (Object.prototype.hasOwnProperty.call(dog, key)) {
    console.log(key); // "name", "breed" (only own properties)
  }
}
```

### for...in Best Practices

```typescript
// BEST PRACTICE: Don't use for...in for arrays
const arr = ["a", "b", "c"];

// BAD — for...in on arrays
for (const index in arr) {
  console.log(index); // "0", "1", "2" (strings, not numbers!)
  console.log(arr[index as number]); // Need type assertion
}

// GOOD — use for...of for arrays
for (const value of arr) {
  console.log(value); // "a", "b", "c"
}

// GOOD — use Object.keys/values/entries for objects
for (const [key, value] of Object.entries(obj)) {
  console.log(`${key}: ${value}`);
}
```

---

## for...of Loop

The `for...of` loop iterates over **iterable objects** — arrays, strings, maps, sets, and custom iterables.

### Basic Usage

```typescript
// Arrays
const fruits: string[] = ["apple", "banana", "cherry"];
for (const fruit of fruits) {
  console.log(fruit); // "apple", "banana", "cherry"
}

// Strings
const greeting: string = "Hello";
for (const char of greeting) {
  console.log(char); // "H", "e", "l", "l", "o"
}

// Maps
const map = new Map<string, number>([
  ["a", 1],
  ["b", 2],
]);
for (const [key, value] of map) {
  console.log(`${key}: ${value}`);
}

// Sets
const set = new Set<number>([1, 2, 3]);
for (const value of set) {
  console.log(value); // 1, 2, 3
}
```

### for...of with Typed Iterables

```typescript
// Typed arrays
const numbers: number[] = [1, 2, 3, 4, 5];
for (const num of numbers) {
  // num: number (automatically typed)
  console.log(num * 2);
}

// Readonly arrays
const readonlyArr: readonly string[] = ["a", "b", "c"];
for (const item of readonlyArr) {
  // item: string
  console.log(item);
}

// Tuples
const tuple: [string, number] = ["hello", 42];
for (const item of tuple) {
  // item: string | number
  console.log(item);
}

// Maps with typed entries
const scores = new Map<string, number>([
  ["Alice", 95],
  ["Bob", 87],
]);

for (const [name, score] of scores) {
  // name: string, score: number
  console.log(`${name}: ${score}`);
}
```

### for...of vs for...in

```typescript
const arr = ["a", "b", "c"];
const obj = { x: 1, y: 2, z: 3 };

// for...of iterates over VALUES (for iterables)
for (const value of arr) {
  console.log(value); // "a", "b", "c"
}

// for...in iterates over KEYS (for enumerable properties)
for (const key in obj) {
  console.log(key); // "x", "y", "z"
}

// for...in on arrays iterates over indices (strings!)
for (const index in arr) {
  console.log(index); // "0", "1", "2" (strings)
}

// for...of on arrays iterates over values
for (const value of arr) {
  console.log(value); // "a", "b", "c"
}
```

### Destructuring with for...of

```typescript
// Object destructuring
const users = [
  { name: "Alice", age: 30 },
  { name: "Bob", age: 25 },
];

for (const { name, age } of users) {
  console.log(`${name} is ${age} years old`);
}

// Nested destructuring
const data = [
  { user: { name: "Alice" }, score: 95 },
  { user: { name: "Bob" }, score: 87 },
];

for (const { user: { name }, score } of data) {
  console.log(`${name}: ${score}`);
}
```

### for...of with Entries

```typescript
// Using Object.entries for indexed iteration
const fruits = ["apple", "banana", "cherry"];

for (const [index, fruit] of fruits.entries()) {
  console.log(`${index + 1}. ${fruit}`);
}
// 1. apple
// 2. banana
// 3. cherry
```

---

## forEach with Typed Arrays

The `forEach` method executes a function for each array element.

### Basic Usage

```typescript
const numbers: number[] = [1, 2, 3, 4, 5];

numbers.forEach((num) => {
  console.log(num); // 1, 2, 3, 4, 5
});

// With index
numbers.forEach((num, index) => {
  console.log(`${index}: ${num}`);
});

// With full array reference
numbers.forEach((num, index, arr) => {
  console.log(`${num} at index ${index} of [${arr}]`);
});
```

### forEach Type Parameters

```typescript
// TypeScript infers parameter types from array type
const users: User[] = [{ name: "Alice", age: 30 }];

users.forEach((user) => {
  // user: User (inferred)
  console.log(user.name);
});

// With explicit types (usually unnecessary)
users.forEach((user: User, index: number): void => {
  console.log(`${index}: ${user.name}`);
});
```

### forEach Return Value

```typescript
// forEach always returns undefined — it cannot be used to build arrays
const numbers: number[] = [1, 2, 3, 4, 5];

// This doesn't work for building arrays
const results: number[] = [];
numbers.forEach((num) => {
  results.push(num * 2); // Can't return a value
});

// Use map instead
const results = numbers.map((num) => num * 2);
```

### forEach vs for...of

```typescript
const items = ["a", "b", "c"];

// forEach — can't break out early
items.forEach((item) => {
  if (item === "b") return; // continues to next iteration
  console.log(item); // "a", "c"
});

// for...of — can use break and continue
for (const item of items) {
  if (item === "b") break; // exits the loop
  console.log(item); // "a"
}

// forEach — can't use async/await properly
const asyncProcess = async (items: Item[]) => {
  // BAD: forEach doesn't await promises
  items.forEach(async (item) => {
    await processItem(item); // These run concurrently, not sequentially
  });

  // GOOD: for...of with await
  for (const item of items) {
    await processItem(item); // These run sequentially
  }
};
```

### forEach with Type Guards

```typescript
// Filtering within forEach (less idiomatic)
const mixed: (string | number)[] = [1, "hello", 2, "world"];
const strings: string[] = [];

mixed.forEach((item) => {
  if (typeof item === "string") {
    strings.push(item); // item narrowed to string
  }
});

// Better: use filter
const strings = mixed.filter((item): item is string => typeof item === "string");
```

---

## Iteration Protocols in TypeScript

TypeScript supports JavaScript's iteration protocols for custom iterables.

### The Iterable Protocol

```typescript
// An object is iterable if it has a [Symbol.iterator] method
interface Iterable<T> {
  [Symbol.iterator](): Iterator<T>;
}

// An iterator has a next() method
interface Iterator<T> {
  next(): IteratorResult<T>;
}

interface IteratorResult<T> {
  value: T;
  done: boolean;
}
```

### Custom Iterable

```typescript
class NumberRange {
  constructor(private start: number, private end: number) {}

  [Symbol.iterator](): Iterator<number> {
    let current = this.start;
    const end = this.end;

    return {
      next(): IteratorResult<number> {
        if (current <= end) {
          return { value: current++, done: false };
        }
        return { value: undefined as unknown as number, done: true };
      },
    };
  }
}

const range = new NumberRange(1, 5);

// Works with for...of
for (const num of range) {
  console.log(num); // 1, 2, 3, 4, 5
}

// Works with spread
const numbers = [...range]; // [1, 2, 3, 4, 5]

// Works with destructuring
const [first, second, ...rest] = range;
// first: 1, second: 2, rest: [3, 4, 5]
```

### Async Iteration

```typescript
// Async iterable — has [Symbol.asyncIterator] method
interface AsyncIterable<T> {
  [Symbol.asyncIterator](): AsyncIterator<T>;
}

interface AsyncIterator<T> {
  next(): Promise<IteratorResult<T>>;
}

// Async for...of
async function* generateNumbers(): AsyncGenerator<number> {
  for (let i = 0; i < 5; i++) {
    await new Promise((resolve) => setTimeout(resolve, 100));
    yield i;
  }
}

async function processNumbers(): Promise<void> {
  for await (const num of generateNumbers()) {
    console.log(num); // 0, 1, 2, 3, 4 (with delays)
  }
}
```

### Generator Functions

```typescript
// Generators are both iterators and iterables
function* fibonacci(): Generator<number> {
  let a = 0;
  let b = 1;

  while (true) {
    yield a;
    [a, b] = [b, a + b];
  }
}

// Use with for...of (limit iterations)
let count = 0;
for (const num of fibonacci()) {
  console.log(num);
  if (++count >= 10) break;
}

// Typed generators
function* typedGenerator(): Generator<string, void, unknown> {
  yield "hello";
  yield "world";
}
```

### Generators as Iterables

```typescript
class EventBus {
  private listeners: Map<string, Function[]> = new Map();

  on(event: string, callback: Function): void {
    const existing = this.listeners.get(event) ?? [];
    this.listeners.set(event, [...existing, callback]);
  }

  *getEvents(): Generator<string> {
    yield* this.listeners.keys();
  }
}

const bus = new EventBus();
bus.on("click", () => {});
bus.on("focus", () => {});

for (const event of bus.getEvents()) {
  console.log(event); // "click", "focus"
}
```

---

## Loop Performance Considerations

### for vs forEach vs for...of

```typescript
const largeArray = Array.from({ length: 1_000_000 }, (_, i) => i);

// for loop — fastest (no function call overhead)
console.time("for");
for (let i = 0; i < largeArray.length; i++) {
  const x = largeArray[i];
}
console.timeEnd("for");

// for...of — slightly slower (iterator protocol overhead)
console.time("for...of");
for (const x of largeArray) {
  // ...
}
console.timeEnd("for...of");

// forEach — slowest (function call overhead for each element)
console.time("forEach");
largeArray.forEach((x) => {
  // ...
});
console.timeEnd("forEach");
```

### Optimization Tips

```typescript
// Cache array length
const arr = getLargeArray();
for (let i = 0, len = arr.length; i < len; i++) {
  // Use arr[i]
}

// Use early exit
for (const item of items) {
  if (found) break;
  if (matches(item)) {
    found = item;
  }
}

// Use appropriate data structure
// Set for lookups
const set = new Set(largeArray);
if (set.has(value)) { /* ... */ }

// Map for key-value lookups
const map = new Map(largeArray.map((item) => [item.id, item]));
```

---

## Summary

| Loop Type | Best For | Supports break | Supports await | Typed |
|-----------|----------|---------------|----------------|-------|
| `for` | Counted iteration | Yes | Yes | Yes |
| `while` | Condition-based | Yes | Yes | Yes |
| `do...while` | At-least-once | Yes | Yes | Yes |
| `for...in` | Object keys | Yes | Yes | Needs assertion |
| `for...of` | Iterable values | Yes | Yes | Yes |
| `forEach` | Array elements | No (return only) | No | Yes |

> **Best Practices:**
> 1. Use `for...of` for arrays (cleaner syntax, supports break/continue/await)
> 2. Use `Object.entries`/`Object.keys`/`Object.values` for objects
> 3. Avoid `for...in` for arrays (iterates indices as strings)
> 4. Use `for` when you need the index and performance matters
> 5. Avoid `forEach` with async/await (doesn't await promises)
> 6. Use generators for lazy iteration and infinite sequences
