# 11 — Generics Interview Questions

## Table of Contents

1. [Fundamentals](#fundamentals)
2. [Generic Functions](#generic-functions)
3. [Generic Interfaces and Classes](#generic-interfaces-and-classes)
4. [Constraints](#constraints)
5. [Utility Types](#utility-types)
6. [Conditional Types](#conditional-types)
7. [Mapped Types](#mapped-types)
8. [Template Literal Types](#template-literal-types)
9. [Coding Challenges](#coding-challenges)
10. [Advanced Concepts](#advanced-concepts)

---

## Fundamentals

### Q1: What are generics in TypeScript?

**Answer:** Generics provide a way to create reusable, type-safe components that work
with a variety of types while preserving type information. They are type-level
parameters — similar to how functions accept value parameters, generics accept type
parameters.

```typescript
function identity<T>(value: T): T {
  return value;
}

identity("hello"); // TypeScript infers T = string
identity(42);      // TypeScript infers T = number
```

Generics are erased at runtime — they have zero performance cost and exist only at
compile time.

---

### Q2: Why use generics instead of `any`?

**Answer:** `any` disables all type checking. Generics preserve type safety while
maintaining flexibility:

```typescript
// any: no type safety
function processAny(value: any): any {
  return value.foo; // no error at compile time, possible runtime crash
}

// generic: full type safety
function processGeneric<T extends { foo: string }>(value: T): string {
  return value.foo; // TypeScript guarantees .foo exists
}
```

Generics also enable autocomplete, refactoring safety, and compile-time error
detection.

---

### Q3: What are the conventional type parameter names?

**Answer:**

| Name | Meaning |
|---|---|
| `T` | Primary **T**ype |
| `U` | Second type (follows T) |
| `V` | **V**alue |
| `K` | **K**ey |
| `R` | **R**eturn type |
| `E` | **E**lement |
| `P` | **P**roperty |
| `N` | **N**umber |

Any valid identifier works. Use meaningful names in complex signatures.

---

### Q4: Can TypeScript infer generic types automatically?

**Answer:** Yes. TypeScript infers type parameters from function arguments, callback
parameters, and contextual positions:

```typescript
function wrap<T>(value: T): { value: T } {
  return { value };
}

const result = wrap(42); // T inferred as number
```

Only provide explicit type arguments when inference gives the wrong type.

---

## Generic Functions

### Q5: Write a generic function that returns the first element of an array.

**Answer:**

```typescript
function first<T>(items: T[]): T | undefined {
  return items[0];
}

const num = first([1, 2, 3]);    // number
const str = first(["a", "b"]);  // string
const empty = first([]);         // undefined
```

---

### Q6: How do you write a generic arrow function?

**Answer:**

```typescript
const identity = <T>(value: T): T => value;

// In .tsx files, add a trailing comma:
const identity = <T,>(value: T): T => value;
```

---

### Q7: Write a generic `map` function with proper typing.

**Answer:**

```typescript
function map<TInput, TOutput>(
  items: TInput[],
  transform: (item: TInput) => TOutput
): TOutput[] {
  return items.map(transform);
}

const lengths = map(["hello", "world"], (s) => s.length);
// lengths: number[]
```

---

### Q8: How do generic async functions work?

**Answer:**

```typescript
async function fetchData<T>(url: string): Promise<T> {
  const response = await fetch(url);
  return response.json() as Promise<T>;
}

const users = await fetchData<User[]>("/api/users");
// users: User[]
```

---

## Generic Interfaces and Classes

### Q9: What is the difference between a generic interface and a generic type alias?

**Answer:**

| Feature | Interface | Type Alias |
|---|---|---|
| Declaration merging | Yes | No |
| Extends/implements | Yes | Intersection only |
| Union types | No | Yes |
| Mapped types | No | Yes |
| Conditional types | No | Yes |

Use interfaces for object shapes and class implementations. Use type aliases for
unions, intersections, mapped types, and conditional types.

---

### Q10: Can a generic class implement a generic interface?

**Answer:** Yes, either binding the type or leaving it open:

```typescript
interface Repository<T> {
  findById(id: string): Promise<T | null>;
  findAll(): Promise<T[]>;
}

// Open — defers type to callers
class InMemoryRepo<T> implements Repository<T> {
  private items = new Map<string, T>();
  async findById(id: string) { return this.items.get(id) ?? null; }
  async findAll() { return Array.from(this.items.values()); }
}

// Bound — locks type to User
class UserRepo implements Repository<User> {
  async findById(id: string) { /* ... */ }
  async findAll() { /* ... */ }
}
```

---

### Q11: Can static members use the class's type parameter?

**Answer:** No. Static members belong to the constructor, not instances. They cannot
access instance-level type parameters. Make the static method separately generic:

```typescript
class Factory<T> {
  // ❌ static create(value: T): Factory<T> { ... }

  // ✅
  static create<T>(value: T): Factory<T> {
    return new Factory(value);
  }
}
```

---

## Constraints

### Q12: What does `extends` mean in a generic context?

**Answer:** `extends` means `T` must be assignable to the constraint type. It does
NOT mean class inheritance.

```typescript
// T must have a .length property
function logLength<T extends { length: number }>(value: T): void {
  console.log(value.length);
}

logLength("hello");    // ✅
logLength([1, 2, 3]);  // ✅
// logLength(42);      // ❌ number has no .length
```

---

### Q13: How do you constrain a type parameter to be a key of another type?

**Answer:**

```typescript
function getProperty<T, K extends keyof T>(obj: T, key: K): T[K] {
  return obj[key];
}

const user = { name: "Alice", age: 30 };
getProperty(user, "name");  // ✅ string
// getProperty(user, "email"); // ❌ "email" not in keyof typeof user
```

---

### Q14: How do you add multiple constraints?

**Answer:** Use intersection (`&`):

```typescript
function process<T extends HasLength & Printable>(value: T): void {
  console.log(value.length, value.toString());
}

interface HasLength { length: number; }
interface Printable { toString(): string; }
```

---

### Q15: What is the difference between `<T>` and `<T extends unknown>`?

**Answer:** They are functionally identical. `<T>` is shorthand for `<T extends unknown>`.
The explicit form is sometimes used in `.tsx` files to avoid JSX parsing conflicts.

---

## Utility Types

### Q16: Implement `Partial<T>` from scratch.

**Answer:**

```typescript
type MyPartial<T> = {
  [K in keyof T]?: T[K];
};
```

---

### Q17: Implement `Pick<T, K>` from scratch.

**Answer:**

```typescript
type MyPick<T, K extends keyof T> = {
  [P in K]: T[P];
};
```

---

### Q18: Implement `Omit<T, K>` from scratch.

**Answer:**

```typescript
type MyOmit<T, K extends keyof T> = {
  [P in keyof T as P extends K ? never : P]: T[P];
};
```

---

### Q19: Implement `Exclude<T, U>` from scratch.

**Answer:**

```typescript
type MyExclude<T, U> = T extends U ? never : T;
```

---

### Q20: Implement `ReturnType<T>` from scratch.

**Answer:**

```typescript
type MyReturnType<T extends (...args: any[]) => any> =
  T extends (...args: any[]) => infer R ? R : never;
```

---

### Q21: What does `NonNullable<T>` do and how is it implemented?

**Answer:** It removes `null` and `undefined` from a type:

```typescript
type MyNonNullable<T> = T & {};
// Or equivalently: T extends null | undefined ? never : T
```

---

## Conditional Types

### Q22: How do conditional types work?

**Answer:** They follow the pattern `T extends U ? X : Y`:

```typescript
type IsString<T> = T extends string ? true : false;

type A = IsString<"hello">; // true
type B = IsString<42>;      // false
```

---

### Q23: What is the `infer` keyword?

**Answer:** `infer` declares a type variable that TypeScript infers from the matched
type:

```typescript
type ElementType<T> = T extends Array<infer E> ? E : never;

type A = ElementType<string[]>;  // string
type B = ElementType<number[]>;  // number
```

---

### Q24: What are distributive conditional types?

**Answer:** When `T` is a naked type parameter, the conditional distributes over
unions:

```typescript
type ToArray<T> = T extends any ? T[] : never;
type A = ToArray<string | number>; // string[] | number[]

// Non-distributive: wrap in tuple
type ToArrayNonDist<T> = [T] extends [any] ? T[] : never;
type B = ToArrayNonDist<string | number>; // (string | number)[]
```

---

### Q25: How does `Extract<T, U>` work?

**Answer:** It keeps only members of `T` assignable to `U`:

```typescript
type Extract<T, U> = T extends U ? T : never;

type A = Extract<"a" | "b" | "c", "a" | "f">; // "a"
```

---

## Mapped Types

### Q26: What are mapped types?

**Answer:** Mapped types iterate over the keys of an existing type to produce a new
type:

```typescript
type Readonly<T> = {
  readonly [K in keyof T]: T[K];
};

type Optional<T> = {
  [K in keyof T]?: T[K];
};
```

---

### Q27: How do you make all properties required?

**Answer:** Use `-?` to remove optionality:

```typescript
type Required<T> = {
  [K in keyof T]-?: T[K];
};
```

---

### Q28: What is key remapping and how does it work?

**Answer:** Key remapping (TypeScript 4.1+) uses the `as` clause to transform keys:

```typescript
type Getters<T> = {
  [K in keyof T as `get${Capitalize<string & K>}`]: () => T[K];
};

interface User { name: string; }
type UserGetters = Getters<User>; // { getName: () => string }
```

---

### Q29: How do you filter keys in a mapped type?

**Answer:**

```typescript
// Keep only string-valued keys
type StringKeys<T> = {
  [K in keyof T as T[K] extends string ? K : never]: T[K];
};

interface Mixed { name: string; age: number; email: string; }
type OnlyStrings = StringKeys<Mixed>; // { name: string; email: string }
```

---

## Template Literal Types

### Q30: What are template literal types?

**Answer:** Types that construct string literal types using backtick syntax:

```typescript
type Greeting = `Hello, ${string}`;
type Name = "Alice";
type Age = 30;
type Info = `${Name} is ${Age}`; // "Alice is 30"
```

---

### Q31: What happens when you use a union in a template literal?

**Answer:** TypeScript produces the cartesian product:

```typescript
type Color = "red" | "blue";
type Size = "sm" | "lg";
type Result = `${Color}-${Size}`;
// "red-sm" | "red-lg" | "blue-sm" | "blue-lg"
```

---

### Q32: How do you extract route parameters from a string?

**Answer:**

```typescript
type ExtractParams<T extends string> =
  T extends `${string}:${infer Param}/${infer Rest}`
    ? Param | ExtractParams<Rest>
    : T extends `${string}:${infer Param}`
      ? Param
      : never;

type Params = ExtractParams<"/users/:id/posts/:postId">;
// "id" | "postId"
```

---

## Coding Challenges

### Q33: Implement a `DeepReadonly<T>` type.

**Answer:**

```typescript
type DeepReadonly<T> = T extends (infer U)[]
  ? ReadonlyArray<DeepReadonly<U>>
  : T extends object
    ? { readonly [K in keyof T]: DeepReadonly<T[K]> }
    : T;

interface Nested {
  a: { b: { c: string } };
  d: number[];
}

type Frozen = DeepReadonly<Nested>;
// { readonly a: { readonly b: { readonly c: string } }; readonly d: readonly number[] }
```

---

### Q34: Implement a type-safe `EventEmitter` types.

**Answer:**

```typescript
type EventMap = {
  login: { userId: string };
  logout: { userId: string };
  error: { code: string; message: string };
};

type EventHandlers<T> = {
  [K in keyof T]: (payload: T[K]) => void;
};

type Handlers = EventHandlers<EventMap>;
// {
//   login: (payload: { userId: string }) => void;
//   logout: (payload: { userId: string }) => void;
//   error: (payload: { code: string; message: string }) => void;
// }
```

---

### Q35: Implement a `Merge<A, B>` type that gives B priority.

**Answer:**

```typescript
type Merge<A, B> = Omit<A, keyof B> & B;

interface Base { id: string; name: string; }
interface Override { name: number; age: number; }

type Result = Merge<Base, Override>;
// { id: string; name: number; age: number }
```

---

### Q36: Implement a type-safe `pluck` function.

**Answer:**

```typescript
function pluck<T, K extends keyof T>(items: T[], key: K): T[K][] {
  return items.map((item) => item[key]);
}

const users = [
  { name: "Alice", age: 30 },
  { name: "Bob", age: 25 },
];

pluck(users, "name"); // ["Alice", "Bob"]
pluck(users, "age");  // [30, 25]
```

---

### Q37: Implement a `DeepPartial<T>` type.

**Answer:**

```typescript
type DeepPartial<T> = T extends object
  ? { [K in keyof T]?: DeepPartial<T[K]> }
  : T;

interface Config {
  server: {
    host: string;
    port: number;
    ssl: { cert: string; key: string };
  };
}

type PartialConfig = DeepPartial<Config>;
// All properties deeply optional
```

---

### Q38: Implement `Parameters<T>` from scratch.

**Answer:**

```typescript
type MyParameters<T extends (...args: any[]) => any> =
  T extends (...args: infer P) => any ? P : never;

type A = MyParameters<(a: string, b: number) => void>; // [a: string, b: number]
```

---

## Advanced Concepts

### Q39: What are recursive conditional types?

**Answer:** Types that call themselves in the conditional branch:

```typescript
type Flatten<T extends any[]> = T extends [infer First, ...infer Rest]
  ? First extends any[]
    ? [...Flatten<First>, ...Flatten<Rest>]
    : [First, ...Flatten<Rest>]
  : T;

type Result = Flatten<[1, [2, 3], [4, [5]]]>; // [1, 2, 3, 4, 5]
```

---

### Q40: How do you prevent distributive conditional types?

**Answer:** Wrap the checked type in a tuple:

```typescript
// Distributive — checks each union member separately
type Bad<T> = T extends string ? "yes" : "no";
type R1 = Bad<string | number>; // "yes" | "no"

// Non-distributive — checks the union as a whole
type Good<T> = [T] extends [string] ? "yes" : "no";
type R2 = Good<string | number>; // "no"
```

---

### Q41: What is the relationship between `infer` and conditional types?

**Answer:** `infer` can only be used within the `extends` clause of a conditional
type. It declares a type variable that TypeScript infers from the type being matched:

```typescript
// infer captures the return type
type ReturnOf<T> = T extends (...args: any[]) => infer R ? R : never;

// infer captures function parameters
type ArgsOf<T> = T extends (...args: infer P) => any ? P : never;
```

---

### Q42: How do you type a curried function?

**Answer:**

```typescript
type Curried<T> =
  T extends (first: infer First, ...rest: infer Rest) => infer Return
    ? Rest extends [never]
      ? (first: First) => Return
      : (first: First) => Curried<(...args: Rest) => Return>
    : T;

function curry<T extends (...args: any[]) => any>(
  fn: T
): Curried<T> {
  const arity = fn.length;
  function curried(...args: any[]): any {
    if (args.length >= arity) {
      return fn(...args);
    }
    return (...moreArgs: any[]) => curried(...args, ...moreArgs);
  }
  return curried as Curried<T>;
}

const add = curry((a: number, b: number, c: number) => a + b + c);
add(1)(2)(3); // 6
add(1, 2)(3); // 6
add(1)(2, 3); // 6
```

---

### Q43: Explain the difference between `unknown` and `any` in generics.

**Answer:**

- `any` disables type checking — you can do anything with it, no safety.
- `unknown` requires narrowing before use — type safe but requires explicit checks.

```typescript
function processAny(value: any) {
  value.foo.bar; // no error, possible crash
}

function processUnknown(value: unknown) {
  // value.foo.bar; // ❌ Error
  if (typeof value === "object" && value !== null && "foo" in value) {
    (value as { foo: { bar: string } }).foo.bar; // ✅ after narrowing
  }
}
```

Use `unknown` when the type is not yet known. Use `any` only as a last resort.

---

### Q44: What are phantom types and how do generics enable them?

**Answer:** Phantom types are types that exist only at compile time to enforce
invariants:

```typescript
type Brand<T, B extends string> = T & { readonly __brand: B };

type USD = Brand<number, "USD">;
type EUR = Brand<number, "EUR">;

function addUSD(a: USD, b: USD): USD {
  return (a + b) as USD;
}

const price: USD = 10 as USD;
const tax: USD = 2 as USD;
const total = addUSD(price, tax); // ✅

// const wrong: EUR = 5 as EUR;
// addUSD(price, wrong); // ❌ Cannot mix USD and EUR
```
