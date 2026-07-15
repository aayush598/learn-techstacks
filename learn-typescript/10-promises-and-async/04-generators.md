# Generators in TypeScript

## Table of Contents

- [Generator Function Basics](#generator-function-basics)
- [Generator Types](#generator-types)
- [Yield Expression](#yield-expression)
- [Iterator Protocol](#iterator-protocol)
- [Generators with Types](#generators-with-types)
- [Lazy Evaluation](#lazy-evaluation)
- [Infinite Sequences](#infinite-sequences)
- [State Machines](#state-machines)
- [Bidirectional Generators](#bidirectional-generators)
- [Generator Utilities](#generator-utilities)
- [Interview Questions](#interview-questions)

---

## Generator Function Basics

A generator function is a special function that can be paused and resumed, yielding values lazily.

```typescript
// Basic generator function
function* count(): Generator<number> {
  console.log("Starting");
  yield 1;
  console.log("After first yield");
  yield 2;
  console.log("After second yield");
  yield 3;
  console.log("Done");
}

// Calling a generator function returns an iterator
const counter = count();
console.log(counter); // Generator { }

// Each call to .next() runs until the next yield
console.log(counter.next()); // { value: 1, done: false }
console.log(counter.next()); // { value: 2, done: false }
console.log(counter.next()); // { value: 3, done: false }
console.log(counter.next()); // { value: undefined, done: true }
```

### Generator vs Regular Function

```typescript
// Regular function: runs to completion
function regular(): number[] {
  return [1, 2, 3];
}

// Generator function: can be paused
function* generator(): Generator<number> {
  yield 1;
  yield 2;
  yield 3;
}

// Generator function with * (asterisk) can be placed:
function* a() {}   // Before function name
function* b() {}   // After function keyword
function *c() {}   // Both (valid but unusual)
function * d() {}  // With space (valid)
```

---

## Generator Types

```typescript
// Generator<TYield, TReturn, TNext>
// TYield: type of values yielded
// TReturn: type of the return value
// TNext: type of values passed into .next()

// Simple generator yielding numbers
function* numbers(): Generator<number> {
  yield 1;
  yield 2;
  yield 3;
}

// Generator with return value
function* withReturn(): Generator<number, string> {
  yield 1;
  yield 2;
  return "done";
}

const gen = withReturn();
gen.next(); // { value: 1, done: false }
gen.next(); // { value: 2, done: false }
gen.next(); // { value: "done", done: true }

// Generator with bidirectional communication
function* echo(): Generator<string, string, string> {
  const input1 = yield "ready";
  const input2 = yield `got: ${input1}`;
  const input3 = yield `got: ${input2}`;
  return `final: ${input3}`;
}

const echoGen = echo();
echoGen.next();          // { value: "ready", done: false }
echoGen.next("hello");   // input1 = "hello", { value: "got: hello", done: false }
echoGen.next("world");   // input2 = "world", { value: "got: world", done: false }
echoGen.next("foo");     // input3 = "foo", { value: "final: foo", done: true }

// IterableGenerator (most common - infinite generators)
function* infinite(): IterableGenerator<number> {
  let i = 0;
  while (true) {
    yield i++;
  }
}

// Async generator (covered in separate section)
async function* asyncGen(): AsyncGenerator<number> {
  yield await Promise.resolve(1);
}
```

---

## Yield Expression

```typescript
// yield produces a value to the caller
function* simpleYield(): Generator<number> {
  yield 1; // Produces 1
  yield 2; // Produces 2
}

// yield* delegates to another generator
function* delegate(): Generator<number> {
  yield* [1, 2, 3]; // Delegates to array iterator
  yield* anotherGen();
  yield* "hello"; // Delegates to string iterator (yields 'h', 'e', 'l', 'l', 'o')
}

function* anotherGen(): Generator<number> {
  yield 10;
  yield 20;
}

// yield* with generator function
function* outer(): Generator<string> {
  yield "a";
  yield* inner();
  yield "b";
}

function* inner(): Generator<string> {
  yield "x";
  yield "y";
}

// [...outer()] === ["a", "x", "y", "b"]

// yield* captures the return value
function* innerWithReturn(): Generator<number, string> {
  yield 1;
  return "inner done";
}

function* outerCapturing(): Generator<number, string> {
  const result = yield* innerWithReturn();
  console.log(result); // "inner done"
  return "outer done";
}

// yield* with different types
function* mixed(): Generator<string | number> {
  yield* [1, 2, 3];       // number
  yield* ["a", "b", "c"]; // string
}
```

---

## Iterator Protocol

Generators implement both the Iterator and Iterable protocols.

```typescript
// Iterator protocol: { next(), return(), throw() }
function* generator(): Generator<number> {
  yield 1;
  yield 2;
}

const gen = generator();

// next(): returns { value, done }
console.log(gen.next()); // { value: 1, done: false }

// return(): completes the generator
console.log(gen.return(100)); // { value: 100, done: true }

// throw(): throws an error into the generator
function* throwing(): Generator<number> {
  try {
    yield 1;
    yield 2;
  } catch (error) {
    console.log("Caught:", error);
  }
  yield 3;
}

const throwGen = throwing();
throwGen.next();             // { value: 1, done: false }
throwGen.next();             // { value: 2, done: false }
throwGen.throw(new Error("boom")); // "Caught: Error: boom" → { value: 3, done: false }

// Manual generator implementation
class NumberGenerator implements Iterator<number> {
  private current = 0;

  next(): IteratorResult<number> {
    if (this.current < 3) {
      return { value: this.current++, done: false };
    }
    return { value: undefined, done: true };
  }

  return(value?: number): IteratorResult<number> {
    console.log("Generator returned with:", value);
    return { value, done: true };
  }

  throw(error: unknown): IteratorResult<number> {
    console.log("Generator thrown into with:", error);
    throw error;
  }
}

// Iterable protocol: { [Symbol.iterator] }
class NumberRange implements Iterable<number> {
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

const range = new NumberRange(1, 5);
for (const num of range) {
  console.log(num); // 1, 2, 3, 4, 5
}
```

---

## Generators with Types

```typescript
// Typed generator for tree traversal
interface TreeNode<T> {
  value: T;
  children: TreeNode<T>[];
}

function* traverseTree<T>(node: TreeNode<T>): Generator<T> {
  yield node.value;
  for (const child of node.children) {
    yield* traverseTree(child);
  }
}

const tree: TreeNode<string> = {
  value: "root",
  children: [
    { value: "child1", children: [] },
    {
      value: "child2",
      children: [
        { value: "grandchild1", children: [] },
        { value: "grandchild2", children: [] },
      ],
    },
  ],
};

console.log([...traverseTree(tree)]); // ["root", "child1", "child2", "grandchild1", "grandchild2"]

// Typed generator for paginated API
interface PaginatedResponse<T> {
  data: T[];
  nextPage: number | null;
}

async function* paginate<T>(
  fetchPage: (page: number) => Promise<PaginatedResponse<T>>
): AsyncGenerator<T> {
  let page = 1;
  while (true) {
    const response = await fetchPage(page);
    yield* response.data;
    if (response.nextPage === null) break;
    page = response.nextPage;
  }
}

// Generator with complex yield types
function* commandProcessor(): Generator<
  string,              // yield type
  string,              // return type
  { command: string; args: string[] } // next() parameter type
> {
  let input = yield "Ready for commands";
  while (input.command !== "quit") {
    if (input.command === "echo") {
      input = yield input.args.join(" ");
    } else if (input.command === "upper") {
      input = yield input.args.map((a) => a.toUpperCase()).join(" ");
    } else {
      input = yield `Unknown command: ${input.command}`;
    }
  }
  return "Goodbye";
}
```

---

## Lazy Evaluation

Generators compute values on-demand, making them memory-efficient.

```typescript
// ❌ Eager evaluation - creates all values upfront
function* eagerRange(start: number, end: number): Generator<number> {
  const values: number[] = [];
  for (let i = start; i <= end; i++) {
    values.push(i);
  }
  yield* values; // Yields all at once
}

// ✅ Lazy evaluation - creates values on demand
function* lazyRange(start: number, end: number): Generator<number> {
  for (let i = start; i <= end; i++) {
    yield i; // Yields one at a time
  }
}

// Lazy evaluation with expensive computation
function* expensiveValues(): Generator<{ index: number; value: number }> {
  for (let i = 0; i < 1_000_000; i++) {
    // This computation only happens when someone calls .next()
    console.log(`Computing value ${i}...`);
    yield { index: i, value: Math.sqrt(i) };
  }
}

// Only computes the first 5 values
const gen = expensiveValues();
for (let i = 0; i < 5; i++) {
  const { value } = gen.next().value as { index: number; value: number };
  console.log(value);
}

// Pipeline of lazy operations
function* map<T, R>(iterable: Iterable<T>, fn: (item: T) => R): Generator<R> {
  for (const item of iterable) {
    yield fn(item);
  }
}

function* filter<T>(iterable: Iterable<T>, fn: (item: T) => boolean): Generator<T> {
  for (const item of iterable) {
    if (fn(item)) yield item;
  }
}

function* take<T>(iterable: Iterable<T>, count: number): Generator<T> {
  let taken = 0;
  for (const item of iterable) {
    if (taken >= count) return;
    yield item;
    taken++;
  }
}

// Lazy pipeline - no intermediate arrays created
const result = take(
  filter(
    map(lazyRange(0, 1_000_000), (x) => x * 2),
    (x) => x % 3 === 0
  ),
  10
);

console.log([...result]); // First 10 even numbers divisible by 3
```

---

## Infinite Sequences

```typescript
// Fibonacci sequence
function* fibonacci(): Generator<number> {
  let a = 0;
  let b = 1;
  while (true) {
    yield a;
    [a, b] = [b, a + b];
  }
}

// Take first 10 Fibonacci numbers
const fibs = [...take(fibonacci(), 10)];
console.log(fibs); // [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]

// Prime numbers
function* primes(): Generator<number> {
  yield 2;
  let candidate = 3;
  const knownPrimes: number[] = [2];

  while (true) {
    const isPrime = knownPrimes.every((p) => candidate % p !== 0);
    if (isPrime) {
      yield candidate;
      knownPrimes.push(candidate);
    }
    candidate += 2;
  }
}

// Natural numbers
function* naturals(start: number = 1): Generator<number> {
  let i = start;
  while (true) {
    yield i++;
  }
}

// Powers of 2
function* powersOfTwo(): Generator<number> {
  let power = 1;
  while (true) {
    yield power;
    power *= 2;
  }
}

// Cycle through a sequence
function* cycle<T>(items: T[]): Generator<T> {
  while (true) {
    yield* items;
  }
}

const colors = cycle(["red", "green", "blue"]);
const firstTen = [...take(colors, 10)]; // ["red", "green", "blue", "red", "green", "blue", "red", "green", "blue", "red"]

// Interleave two generators
function* interleave<T>(
  gen1: Generator<T>,
  gen2: Generator<T>
): Generator<T> {
  while (true) {
    const v1 = gen1.next();
    const v2 = gen2.next();
    if (v1.done && v2.done) return;
    if (!v1.done) yield v1.value;
    if (!v2.done) yield v2.value;
  }
}
```

---

## State Machines

Generators can model state machines elegantly.

```typescript
type TrafficLightState = "green" | "yellow" | "red";
type TrafficLightAction = "tick";

function* trafficLight(): Generator<{
  state: TrafficLightState;
  duration: number;
}> {
  while (true) {
    yield { state: "green", duration: 30 };
    yield { state: "yellow", duration: 5 };
    yield { state: "red", duration: 20 };
  }
}

// State machine with transitions
interface StateTransition<S extends string, E extends string> {
  from: S;
  event: E;
  to: S;
  action?: () => void;
}

function* stateMachine<S extends string, E extends string>(
  initialState: S,
  transitions: StateTransition<S, E>[]
): Generator<{ state: S; event: E | null }> {
  let currentState = initialState;
  let lastEvent: E | null = null;

  yield { state: currentState, event: null };

  while (true) {
    const event: E = yield { state: currentState, event: lastEvent };
    const transition = transitions.find(
      (t) => t.from === currentState && t.event === event
    );

    if (transition) {
      transition.action?.();
      currentState = transition.to;
      lastEvent = event;
    }
  }
}

// Usage
const light = stateMachine<TrafficLightState, TrafficLightAction>(
  "green",
  [
    { from: "green", event: "tick", to: "yellow" },
    { from: "yellow", event: "tick", to: "red" },
    { from: "red", event: "tick", to: "green" },
  ]
);

light.next();                    // { state: "green", event: null }
light.next("tick");             // { state: "yellow", event: "tick" }
light.next("tick");             // { state: "red", event: "tick" }
light.next("tick");             // { state: "green", event: "tick" }

// Vending machine state machine
type VendingState = "idle" | "hasMoney" | "dispensing" | "done";
type VendingEvent = "insert" | "select" | "dispense" | "return";

function* vendingMachine(): Generator<
  { state: VendingState; message: string },
  void,
  VendingEvent
> {
  let balance = 0;

  yield { state: "idle", message: "Insert coins" };

  while (true) {
    const event = yield { state: "idle", message: `Balance: $${balance}` };

    if (event === "insert") {
      balance += 1;
      yield { state: "hasMoney", message: `Added $1. Balance: $${balance}` };
    } else if (event === "select") {
      if (balance >= 2) {
        balance -= 2;
        yield { state: "dispensing", message: "Dispensing..." };
        yield { state: "idle", message: "Done!" };
      } else {
        yield { state: "hasMoney", message: "Insufficient funds" };
      }
    } else if (event === "return") {
      yield { state: "done", message: `Returning $${balance}` };
      return;
    }
  }
}
```

---

## Bidirectional Generators

```typescript
// Generators that receive values via .next()
function* dialog(): Generator<string, string, string> {
  const name = yield "What is your name?";
  const age = yield `Hello ${name}! How old are you?`;
  return `${name} is ${age} years old`;
}

const d = dialog();
console.log(d.next());                    // "What is your name?"
console.log(d.next("Alice"));             // "Hello Alice! How old are you?"
console.log(d.next("30"));                // "Alice is 30 years old"

// Coroutine pattern
function* coroutine<TInput, TOutput>(): Generator<TOutput, void, TInput> {
  while (true) {
    const input: TInput = yield undefined as unknown as TOutput;
    console.log("Received:", input);
  }
}

// Reducer generator
function* reducer<S, A>(
  initialState: S,
  reducer: (state: S, action: A) => S
): Generator<S, void, A> {
  let state = initialState;
  while (true) {
    const action: A = yield state;
    state = reducer(state, action);
  }
}

const counter = reducer(0, (state: number, action: string) => {
  if (action === "increment") return state + 1;
  if (action === "decrement") return state - 1;
  return state;
});

counter.next();                // 0
counter.next("increment");    // 1
counter.next("increment");    // 2
counter.next("decrement");    // 1
```

---

## Generator Utilities

```typescript
// Compose multiple generators
function* compose<T>(
  ...generators: Array<() => Generator<T>>
): Generator<T> {
  for (const gen of generators) {
    yield* gen();
  }
}

// Memoize generator results
function* memoized<T>(gen: () => Generator<T>): Generator<T> {
  const cache: T[] = [];
  let computed = false;

  function* compute(): Generator<T> {
    if (!computed) {
      yield* gen();
      computed = true;
    }
  }

  yield* compute();
}

// Chunk generator
function* chunk<T>(iterable: Iterable<T>, size: number): Generator<T[]> {
  let chunk: T[] = [];
  for (const item of iterable) {
    chunk.push(item);
    if (chunk.length === size) {
      yield chunk;
      chunk = [];
    }
  }
  if (chunk.length > 0) yield chunk;
}

// Flatten generator
function* flatten<T>(nested: Iterable<Iterable<T>>): Generator<T> {
  for (const iterable of nested) {
    yield* iterable;
  }
}

// Scan (running accumulator)
function* scan<T, R>(
  iterable: Iterable<T>,
  fn: (acc: R, item: T) => R,
  initial: R
): Generator<R> {
  let accumulator = initial;
  yield accumulator;
  for (const item of iterable) {
    accumulator = fn(accumulator, item);
    yield accumulator;
  }
}

// Running sum
const runningSum = [...scan([1, 2, 3, 4], (acc, item) => acc + item, 0)];
// [0, 1, 3, 6, 10]

// Pairwise iteration
function* pairwise<T>(iterable: Iterable<T>): Generator<[T, T]> {
  const iterator = iterable[Symbol.iterator]();
  let prev = iterator.next();
  let curr = iterator.next();

  while (!curr.done) {
    yield [prev.value, curr.value];
    prev = curr;
    curr = iterator.next();
  }
}

// Window (sliding window)
function* window<T>(iterable: Iterable<T>, size: number): Generator<T[]> {
  const buffer: T[] = [];
  for (const item of iterable) {
    buffer.push(item);
    if (buffer.length > size) buffer.shift();
    if (buffer.length === size) yield [...buffer];
  }
}
```

---

## Interview Questions

1. **What is a generator function?**
   A function that can be paused and resumed using `yield` expressions, producing a sequence of values lazily.

2. **What is the difference between `yield` and `yield*`?**
   `yield` produces a single value. `yield*` delegates to another iterable (generator, array, string, etc.).

3. **What are the three type parameters of `Generator<TYield, TReturn, TNext>`?**
   `TYield` is the type yielded, `TReturn` is the type returned, and `TNext` is the type passed into `.next()`.

4. **How do generators implement lazy evaluation?**
   Code after `yield` only executes when `.next()` is called, computing values on-demand.

5. **What is the iterator protocol?**
   An object with a `next()` method returning `{ value, done }`, and optionally `return()` and `throw()` methods.

6. **How do you create an infinite sequence with generators?**
   Use `while (true)` with `yield` inside the loop.

7. **What is `yield*` used for?**
   Delegation to another generator or iterable, forwarding all yields and receiving the return value.

8. **Can generators receive values?**
   Yes, via `generator.next(value)` - the value is returned by the `yield` expression inside the generator.

9. **How do generators relate to async/await?**
   `async/await` is syntactic sugar over generators + promises. An async function is essentially a generator that yields promises.

10. **What is the difference between `Generator` and `IterableIterator`?**
    `Generator` includes all three type parameters and `TReturn`. `IterableIterator` is simpler with just `TYield`.

11. **How do you convert a generator to an array?**
    Use the spread operator: `[...generator()]` or `Array.from(generator())`.

12. **What happens when you call `.return()` on a generator?**
    The generator completes immediately, returning the provided value and setting `done: true`.

13. **What is the coroutine pattern with generators?**
    Using bidirectional communication where the generator both yields values and receives inputs, modeling coroutines or state machines.

14. **When should you use generators over async/await?**
    For lazy sequences, infinite streams, custom iteration, state machines, or when you need fine-grained control over iteration.

15. **What are the performance benefits of generators?**
    Memory efficiency (no intermediate arrays), lazy evaluation (compute only what's needed), and O(1) space for infinite sequences.
