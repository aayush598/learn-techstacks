# Function Types in TypeScript

## Table of Contents

1. [Function Type Syntax](#function-type-syntax)
2. [Call Signatures](#call-signatures)
3. [Construct Signatures](#construct-signatures)
4. [Readonly Functions](#readonly-functions)
5. [Optional This Parameter](#optional-this-parameter)
6. [Void-Returning Functions](#void-returning-functions)
7. [Generator Function Types](#generator-function-types)
8. [Async Function Types](#async-function-types)
9. [Generic Function Types](#generic-function-types)
10. [Complex Function Type Examples](#complex-function-type-examples)
11. [Best Practices](#best-practices)
12. [Interview Questions](#interview-questions)

---

## Function Type Syntax

TypeScript provides multiple ways to define function types.

```typescript
// Type alias for a function
type MathOp = (a: number, b: number) => number;

const add: MathOp = (a, b) => a + b;
const subtract: MathOp = (a, b) => a - b;

// Interface with call signature
interface Formatter {
  (value: string, options?: FormatOptions): string;
}

const format: Formatter = (value, options) => {
  return options?.uppercase ? value.toUpperCase() : value;
};

// Inline function type
function process(
  callback: (data: string, index: number) => boolean
): void {
  // ...
}

// Function type with no parameters
type InitFn = () => void;
type AsyncInitFn = () => Promise<void>;

// Function type with rest parameters
type LogFn = (...args: unknown[]) => void;

// Function type with generic
type Mapper<T, U> = (item: T, index: number) => U;
type Predicate<T> = (item: T) => boolean;
type AsyncFn<T> = () => Promise<T>;
```

### Comparison of Syntaxes

```typescript
// Type alias (most common)
type Callback = (data: string) => void;

// Interface call signature
interface Callback {
  (data: string): void;
}

// Key difference: interface can be extended, type alias can be intersected
interface HasCallback {
  (data: string): void;
}

interface ExtendedCallback extends HasCallback {
  (data: string, options: Options): void;
}

// Type alias intersection
type BaseCallback = (data: string) => void;
type ExtendedCallback2 = BaseCallback & ((data: string, options: Options) => void);
```

---

## Call Signatures

Call signatures define the shape of callable types using interface syntax.

```typescript
// Basic call signature
interface SearchFunc {
  (source: string, subString: string): boolean;
}

const mySearch: SearchFunc = (source, subString) => {
  return source.search(subString) > -1;
};

// Call signature with property
interface Counter {
  (start: number): void;
  interval: number;
  reset(): void;
}

function createCounter(): Counter {
  const counter = function (start: number) {
    counter.interval = start;
  } as Counter;

  counter.interval = 0;
  counter.reset = function () {
    counter.interval = 0;
  };

  return counter;
}

// Call signature with overloaded methods
interface Calculator {
  (value: number): number;
  add(a: number, b: number): number;
  subtract(a: number, b: number): number;
  multiply(a: number, b: number): number;
}

function createCalculator(): Calculator {
  const calc = function (value: number): number {
    return value;
  } as Calculator;

  calc.add = (a, b) => a + b;
  calc.subtract = (a, b) => a - b;
  calc.multiply = (a, b) => a * b;

  return calc;
}

const calc = createCalculator();
calc(5);            // 5
calc.add(2, 3);     // 5
calc.multiply(4, 5); // 20
```

### Advanced Call Signatures

```typescript
// Call signature with generic
interface Repository<T> {
  findById(id: string): Promise<T | null>;
  findAll(): Promise<T[]>;
  save(entity: T): Promise<T>;
  delete(id: string): Promise<boolean>;
}

// Call signature with multiple overloads
interface EventDispatcher {
  (event: string): void;
  (event: string, data: unknown): void;
  (event: string, data: unknown, options: DispatchOptions): void;
}

// Call signature with this type
interface Validator {
  (this: ValidationContext, value: string): boolean;
}

interface ValidationContext {
  field: string;
  form: Record<string, unknown>;
}

// Call signature with conditional return
interface Fetcher {
  (url: string): Promise<unknown>;
  <T>(url: string, schema: Schema<T>): Promise<T>;
}
```

---

## Construct Signatures

Construct signatures define types for functions used with `new`.

```typescript
// Basic construct signature
interface ClockConstructor {
  new (hour: number, minute: number): Clock;
}

interface Clock {
  tick(): void;
}

function createClock(ctor: ClockConstructor, hour: number, minute: number): Clock {
  return new ctor(hour, minute);
}

class DigitalClock implements Clock {
  constructor(private h: number, private m: number) {}

  tick(): void {
    console.log(`Digital: ${this.h}:${this.m}`);
  }
}

class AnalogClock implements Clock {
  constructor(private h: number, private m: number) {}

  tick(): void {
    console.log(`Analog: ${this.h}:${this.m}`);
  }
}

const digital = createClock(DigitalClock, 12, 17);
const analog = createClock(AnalogClock, 10, 30);

// Construct signature with generic
interface Factory<T> {
  new (...args: unknown[]): T;
}

function createInstance<T>(factory: Factory<T>, ...args: unknown[]): T {
  return new factory(...args);
}

// Construct signature with properties
interface Car {
  make: string;
  model: string;
  year: number;
}

interface CarConstructor {
  new (make: string, model: string, year: number): Car;
  readonly MAX_YEAR: number;
}

// Combined call and construct signature
interface Buffer {
  new (size: number): Buffer;
  (size: number): Buffer;
  isBuffer(obj: unknown): obj is Buffer;
}
```

---

## Readonly Functions

Making function types and properties readonly.

```typescript
// Readonly function properties
interface ReadonlyConfig {
  readonly apiUrl: string;
  readonly timeout: number;
  readonly headers: Readonly<Record<string, string>>;
}

function getConfig(): ReadonlyConfig {
  return {
    apiUrl: "https://api.example.com",
    timeout: 5000,
    headers: { "Content-Type": "application/json" },
  };
}

const config = getConfig();
// config.apiUrl = "other"; // Error: Cannot assign to 'apiUrl'

// Readonly this parameter
class ImmutableBuilder {
  private readonly value: number;

  constructor(value: number) {
    this.value = value;
  }

  add(n: number): ImmutableBuilder {
    return new ImmutableBuilder(this.value + n);
  }

  multiply(n: number): ImmutableBuilder {
    return new ImmutableBuilder(this.value * n);
  }

  build(): number {
    return this.value;
  }
}

const result = new ImmutableBuilder(5)
  .add(3)
  .multiply(2)
  .build(); // 16

// Readonly function types
type ReadonlyFn<T extends (...args: any[]) => any> = T;

// Readonly arrays in function parameters
function sum(...numbers: readonly number[]): number {
  return numbers.reduce((a, b) => a + b, 0);
}

const nums: readonly number[] = [1, 2, 3];
sum(...nums); // Works

// Readonly tuples
function pair<T, U>(a: T, b: U): readonly [T, U] {
  return [a, b];
}
```

---

## Optional This Parameter

TypeScript allows an optional `this` parameter for type-checking how functions are called.

```typescript
// Function with optional this parameter
interface EventEmitter {
  on(event: string, listener: (this: EventEmitter) => void): void;
}

// this parameter in function types
type Handler<T> = (this: T, event: Event) => void;

class Button {
  private listeners: Array<() => void> = [];

  onClick(handler: (this: HTMLButtonElement, event: Event) => void): void {
    // The 'this' parameter is erased at runtime
    // It only affects TypeScript's type checking
  }
}

// void this parameter - prevents accessing this
function standalone(this: void, value: number): number {
  // this is explicitly void - cannot access any properties
  return value * 2;
}

// this parameter in methods
interface Calculator2 {
  value: number;
  add(this: Calculator2, n: number): Calculator2;
  getValue(this: Calculator2): number;
}

// Generic this type
class Chainable<T extends Chainable<T>> {
  private items: unknown[] = [];

  add(item: unknown): T {
    this.items.push(item);
    return this as unknown as T;
  }

  getItems(): unknown[] {
    return [...this.items];
  }
}

class StringChain extends Chainable<StringChain> {
  join(separator: string): string {
    return this.getItems().join(separator);
  }
}

class NumberChain extends Chainable<NumberChain> {
  sum(): number {
    return this.getItems().reduce((a, b) => (a as number) + (b as number), 0);
  }
}

// Chaining works correctly
const strResult = new StringChain()
  .add("hello")
  .add("world")
  .join(" "); // "hello world"

const numResult = new NumberChain()
  .add(1)
  .add(2)
  .add(3)
  .sum(); // 6
```

---

## Void-Returning Functions

Understanding void-returning function types and their implications.

```typescript
// Void-returning function type
type VoidFn = () => void;
type VoidCallback<T> = (item: T) => void;

// Important: void-returning functions CAN return values
// but the return value is ignored
const fn: VoidFn = () => 42; // No error!

// This is why forEach works with callbacks that return values
const numbers = [1, 2, 3];
numbers.forEach((n) => n * 2); // Return value ignored, no error

// vs. map which requires non-void return
const doubled = numbers.map((n) => n * 2); // Must return a value

// void vs undefined in function types
type ReturnsVoid = () => void;
type ReturnsUndefined = () => undefined;

const voidFn: ReturnsVoid = () => {
  return 42; // Allowed! Return value is ignored
};

// const undefinedFn: ReturnsUndefined = () => {
//   return 42; // Error! Must return undefined
// };

// Strict function types with never
type StrictVoid = () => never;
// const strictFn: StrictVoid = () => 42; // Error!

// When to use void vs never vs undefined
// void: Function has no meaningful return value
// never: Function never returns (throws, infinite loop)
// undefined: Function explicitly returns undefined

// Practical example
function processArray<T>(arr: T[], callback: (item: T) => void): void {
  for (const item of arr) {
    callback(item);
  }
}

// This is fine even though callback returns a value
processArray([1, 2, 3], (n) => n * 2); // No error

// If you want to prevent returning, use a stricter type
type Processor<T> = (item: T) => undefined;
// processArray([1, 2, 3], (n) => n * 2); // Error: number is not undefined
```

---

## Generator Function Types

Typing generator functions and their iterators.

```typescript
// Generator function type
type GeneratorFn<T> = () => Generator<T, void, unknown>;

// Typed generator function
function* range(start: number, end: number): Generator<number, void, unknown> {
  for (let i = start; i < end; i++) {
    yield i;
  }
}

const gen = range(0, 5);
console.log(gen.next()); // { value: 0, done: false }
console.log(gen.next()); // { value: 1, done: false }

// Generator with return value
function* fibonacci(): Generator<number, number, unknown> {
  let a = 0;
  let b = 1;

  while (true) {
    yield a;
    [a, b] = [b, a + b];
  }
}

// Take first N from generator
function* take<T>(gen: Generator<T>, count: number): Generator<T, void, unknown> {
  let i = 0;
  while (i < count) {
    const next = gen.next();
    if (next.done) return;
    yield next.value;
    i++;
  }
}

// Async generator
async function* fetchPages(
  url: string
): AsyncGenerator<PageData, void, unknown> {
  let page = 1;
  let hasMore = true;

  while (hasMore) {
    const response = await fetch(`${url}?page=${page}`);
    const data = await response.json();
    yield data;
    hasMore = data.hasMore;
    page++;
  }
}

// Using async generator
async function processPages() {
  for await (const page of fetchPages("https://api.com/pages")) {
    console.log(page);
  }
}

// Generator with typed next/send/return
function* stateMachine<S, A>(
  initialState: S,
  reducer: (state: S, action: A) => S
): Generator<S, void, A> {
  let state = initialState;
  while (true) {
    const action = yield state;
    state = reducer(state, action);
  }
}
```

---

## Async Function Types

Typing async functions and their return types.

```typescript
// Basic async function type
type AsyncFn<T> = () => Promise<T>;
type AsyncFnWithArgs<A extends unknown[], T> = (...args: A) => Promise<T>;

// Async function declaration
async function fetchUser(id: string): Promise<User> {
  const response = await fetch(`/api/users/${id}`);
  return response.json();
}

// Async arrow function
const fetchPost = async (id: string): Promise<Post> => {
  const response = await fetch(`/api/posts/${id}`);
  return response.json();
};

// Async function with error handling
type Result<T> = { ok: true; data: T } | { ok: false; error: Error };

async function safeFetch<T>(url: string): Promise<Result<T>> {
  try {
    const response = await fetch(url);
    if (!response.ok) {
      return { ok: false, error: new Error(`HTTP ${response.status}`) };
    }
    const data = await response.json();
    return { ok: true, data };
  } catch (error) {
    return { ok: false, error: error as Error };
  }
}

// Async higher-order functions
async function mapAsync<T, U>(
  items: T[],
  fn: (item: T) => Promise<U>
): Promise<U[]> {
  return Promise.all(items.map(fn));
}

async function filterAsync<T>(
  items: T[],
  predicate: (item: T) => Promise<boolean>
): Promise<T[]> {
  const results = await Promise.all(items.map(predicate));
  return items.filter((_, i) => results[i]);
}

// Async function types in interfaces
interface ApiService {
  getUser(id: string): Promise<User>;
  createUser(data: CreateUserDto): Promise<User>;
  updateUser(id: string, data: UpdateUserDto): Promise<User>;
  deleteUser(id: string): Promise<void>;
}

// Async generator type
type AsyncGeneratorFn<T> = () => AsyncGenerator<T, void, unknown>;

// Awaited type utility
type Awaited<T> = T extends Promise<infer U> ? Awaited<U> : T;

type UserPromise = Promise<User>;
type UserType = Awaited<UserPromise>; // User
```

---

## Generic Function Types

Generic types for reusable function signatures.

```typescript
// Generic function type
type IdentityFn = <T>(x: T) => T;
type MapperFn = <T, U>(item: T, index: number) => U;
type PredicateFn = <T>(item: T) => boolean;

// Generic function with constraints
type Lengthwise = <T extends { length: number }>(arg: T) => T;

function logLength<T extends { length: number }>(arg: T): T {
  console.log(arg.length);
  return arg;
}

// Generic function types in interfaces
interface Container<T> {
  get(): T;
  set(value: T): void;
  map<U>(fn: (value: T) => U): Container<U>;
}

// Generic function with multiple type parameters
type Curry<A extends unknown[], R> = {
  (...args: A): R;
};

// Generic conditional function type
type NarrowFn<T> = T extends string
  ? (s: string) => string
  : T extends number
  ? (n: number) => number
  : (x: unknown) => unknown;

// Generic overload type
type OverloadedFn = {
  (x: string): string;
  (x: number): number;
  (x: boolean): boolean;
};

// Practical generic function types
type AsyncMapper<T, U> = (item: T) => Promise<U>;
type AsyncFilter<T> = (item: T) => Promise<boolean>;
type AsyncReducer<T, U> = (acc: U, item: T) => Promise<U>;

type EventMap = Record<string, unknown>;

type EventHandler<TEvent> = (event: TEvent) => void | Promise<void>;

type TypedEventEmitter<Events extends EventMap> = {
  on<K extends keyof Events>(
    event: K,
    handler: EventHandler<Events[K]>
  ): void;
  off<K extends keyof Events>(
    event: K,
    handler: EventHandler<Events[K]>
  ): void;
  emit<K extends keyof Events>(event: K, data: Events[K]): void;
};
```

---

## Complex Function Type Examples

Real-world complex function type patterns.

```typescript
// Middleware pattern
type Middleware<TContext> = (
  context: TContext,
  next: () => Promise<void>
) => Promise<void>;

// Pipeline
type Pipeline<TInput, TOutput> = (
  input: TInput
) => TOutput | Promise<TOutput>;

// Schema validation
type Schema<T> = {
  validate: (value: unknown) => value is T;
  parse: (value: unknown) => T;
  transform: <U>(fn: (value: T) => U) => Schema<U>;
};

// Builder pattern
type Builder<T> = {
  [K in keyof T as `set${Capitalize<string & K>}`]: (
    value: T[K]
  ) => Builder<T>;
} & {
  build: () => T;
};

// Reactive stream
type Observable<T> = {
  subscribe: (observer: Observer<T>) => Subscription;
  pipe: <U>(...operators: Array<(source: Observable<T>) => Observable<U>>) => Observable<U>;
};

type Observer<T> = {
  next: (value: T) => void;
  error: (error: Error) => void;
  complete: () => void;
};

type Subscription = {
  unsubscribe: () => void;
};

// Router
type Route = {
  path: string;
  method: "GET" | "POST" | "PUT" | "DELETE";
  handler: (req: Request, res: Response) => Promise<void>;
  middleware?: Middleware<Request>[];
};

// Decorator type
type ClassDecorator = <T extends new (...args: any[]) => any>(
  target: T
) => T;

type MethodDecorator = <T>(
  target: any,
  propertyKey: string,
  descriptor: TypedPropertyDescriptor<T>
) => TypedPropertyDescriptor<T>;

// Plugin system
type Plugin<TConfig> = {
  name: string;
  version: string;
  setup: (config: TConfig) => Promise<void>;
  teardown: () => Promise<void>;
};

// Command pattern
type Command<TState> = {
  execute: (state: TState) => TState;
  undo: (state: TState) => TState;
  description: string;
};

// State machine
type StateMachineConfig<TState extends string, TEvent extends string> = {
  initial: TState;
  states: Record<
    TState,
    {
      on?: Partial<Record<TEvent, TState>>;
      entry?: () => void;
      exit?: () => void;
    }
  >;
};
```

---

## Best Practices

```typescript
// 1. Use type aliases for reusable function types
type Callback<T> = (data: T) => void;
type AsyncCallback<T> = (data: T) => Promise<void>;

// 2. Use interface call signatures for extensible types
interface EventEmitter {
  (event: string): void;
  listeners: Map<string, Function[]>;
}

// 3. Prefer specific types over Function
// BAD
function process(fn: Function): void { /* ... */ }

// GOOD
function process(fn: (x: number) => number): void { /* ... */ }

// 4. Use readonly for immutable function parameters
function sort(items: readonly number[]): number[] {
  return [...items].sort((a, b) => a - b);
}

// 5. Document complex function types
/** A middleware function that processes requests in sequence */
type Middleware<Ctx> = (
  context: Ctx,
  next: () => Promise<void>
) => Promise<void>;

// 6. Use generic constraints for flexible yet type-safe functions
function pluck<T, K extends keyof T>(items: T[], key: K): T[K][] {
  return items.map((item) => item[key]);
}
```

---

## Interview Questions

### Q1: What is the difference between `type Func = () => void` and `type Func = () => undefined`?

**Answer:** `void` means the return value is ignored - the function can return anything. `undefined` means the function must explicitly return `undefined`. Use `void` when you don't care about the return value.

### Q2: What are call signatures and when would you use them?

**Answer:** Call signatures define the type of callable values using interface syntax. They're useful when you need to add properties to a function type or create overloaded function types that can be extended.

### Q3: How do you type a function that returns a function?

**Answer:** Use nested arrow syntax or type aliases:
```typescript
type FnReturningFn = (x: number) => (y: string) => boolean;
// or
type FnReturningFn = (x: number) => (y: string) => boolean;
```

### Q4: What is the `this` parameter in TypeScript?

**Answer:** The `this` parameter is a special TypeScript-only parameter that defines the type of `this` inside the function. It's erased at runtime and only used for compile-time checking.
