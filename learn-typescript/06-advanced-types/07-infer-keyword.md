# The `infer` Keyword in TypeScript

The `infer` keyword is used within **conditional types** to extract and name a type that TypeScript would otherwise infer. It allows you to "capture" types from within complex type expressions, making conditional types significantly more powerful.

---

## Table of Contents

1. [What Does `infer` Do?](#what-does-infer-do)
2. [infer in Conditional Types](#infer-in-conditional-types)
3. [infer in Function Return Types](#infer-in-function-return-types)
4. [infer in Function Parameters](#infer-in-function-parameters)
5. [infer in Promise Types](#infer-in-promise-types)
6. [infer in Array Types](#infer-in-array-types)
7. [infer in Template Literals](#infer-in-template-literals)
8. [Multiple infer](#multiple-infer)
9. [infer Constraints](#infer-constraints)
10. [Real-World infer Patterns](#real-world-infer-patterns)
11. [Best Practices](#best-practices)
12. [Interview Questions](#interview-questions)

---

## What Does `infer` Do?

`infer` declares a **type variable** within a conditional type. It tells TypeScript to "figure out" and capture a type from a specific position.

```typescript
// Without infer — we can only check, not capture
type IsString<T> = T extends string ? true : false;

// With infer — we capture a type
type ReturnType<T> = T extends (...args: any[]) => infer R ? R : never;
```

### Basic example

```typescript
// Extract the return type of a function
type GetReturnType<T> = T extends (...args: any[]) => infer R ? R : never;

type A = GetReturnType<() => string>;           // string
type B = GetReturnType<(x: number) => boolean>; // boolean
type C = GetReturnType<string>;                 // never (not a function)
```

### How it works

1. `T extends (...args: any[]) => infer R` — checks if `T` is a function type
2. `infer R` — captures the return type and names it `R`
3. `? R : never` — if `T` is a function, return the captured `R`; otherwise return `never`

---

## infer in Conditional Types

`infer` only works inside the `extends` clause of conditional types.

```typescript
// Extract element type from an array
type ElementOf<T> = T extends (infer E)[] ? E : never;

type A = ElementOf<string[]>;     // string
type B = ElementOf<number[]>;     // number
type C = ElementOf<(string | number)[]>; // string | number
type D = ElementOf<string>;       // never (not an array)
```

### Extract first element of a tuple

```typescript
type First<T extends any[]> = T extends [infer First, ...any[]] ? First : never;

type A = First<[string, number, boolean]>; // string
type B = First<[number]>;                  // number
type C = First<[]>;                        // never
```

### Extract last element of a tuple

```typescript
type Last<T extends any[]> = T extends [...any[], infer Last] ? Last : never;

type A = Last<[string, number, boolean]>; // boolean
type B = Last<[number, string]>;          // string
type C = Last<[number]>;                  // number
```

---

## infer in Function Return Types

Extracting function return types is the most common use of `infer`.

### Basic ReturnType

```typescript
type ReturnType<T> = T extends (...args: any[]) => infer R ? R : never;

type A = ReturnType<() => string>;             // string
type B = ReturnType<(x: number, y: number) => boolean>; // boolean
type C = ReturnType<() => void>;               // void
type D = ReturnType<() => Promise<string>>;    // Promise<string>
type E = ReturnType<string>;                   // never
```

### Extract return type from async functions

```typescript
type AsyncReturnType<T> = T extends (...args: any[]) => Promise<infer R> ? R : never;

async function getUser() {
  return { id: 1, name: "Alice" };
}

type User = AsyncReturnType<typeof getUser>; // { id: 1; name: string }
```

### Extract return type with inference chain

```typescript
// First extract the Promise, then extract the resolved type
type UnwrapPromise<T> = T extends Promise<infer U> ? U : T;

type AsyncFn = () => Promise<string>;
type ReturnOfAsyncFn = ReturnType<AsyncFn>; // Promise<string>
type Unwrapped = UnwrapPromise<ReturnOfAsyncFn>; // string
```

---

## infer in Function Parameters

You can use `infer` to extract function parameter types.

### Extract first parameter type

```typescript
type FirstParam<T> = T extends (first: infer P, ...args: any[]) => any ? P : never;

type A = FirstParam<(name: string, age: number) => void>; // string
type B = FirstParam<(x: number) => void>;                 // number
type C = FirstParam<() => void>;                          // never
```

### Extract all parameter types as a tuple

```typescript
type Params<T> = T extends (...args: infer P) => any ? P : never;

type A = Params<(name: string, age: number) => void>; // [name: string, age: number]
type B = Params<(x: number) => void>;                 // [x: number]
type C = Params<() => void>;                          // []
```

### Extract specific parameter

```typescript
type SecondParam<T> = T extends (first: any, second: infer P, ...args: any[]) => any
  ? P
  : never;

type A = SecondParam<(a: string, b: number, c: boolean) => void>; // number
```

### Extract constructor parameter types

```typescript
type ConstructorParams<T> = T extends new (...args: infer P) => any ? P : never;

class User {
  constructor(public name: string, public age: number) {}
}

type Params = ConstructorParams<typeof User>; // [name: string, age: number]
```

---

## infer in Promise Types

Extracting types from `Promise` is a common pattern.

### Unwrap a Promise

```typescript
type UnwrapPromise<T> = T extends Promise<infer U> ? U : T;

type A = UnwrapPromise<Promise<string>>;  // string
type B = UnwrapPromise<Promise<number>>;  // number
type C = UnwrapPromise<string>;           // string (not a Promise)
```

### Deeply unwrap Promises

```typescript
type DeepUnwrap<T> = T extends Promise<infer U> ? DeepUnwrap<U> : T;

type A = DeepUnwrap<Promise<Promise<string>>>;  // string
type B = DeepUnwrap<Promise<Promise<number>>>;  // number
type C = DeepUnwrap<Promise<string>>;           // string
```

### Unwrap Promise with fallback

```typescript
type Awaited<T> = T extends Promise<infer U> ? Awaited<U> : T;

type A = Awaited<Promise<string>>;                  // string
type B = Awaited<Promise<Promise<number>>>;         // number
type C = Awaited<string>;                           // string
```

### Extract Promise result type

```typescript
type PromiseResult<T> = T extends Promise<infer R> ? R : never;

async function fetchData(): Promise<{ data: string[] }> {
  return { data: [] };
}

type Result = PromiseResult<ReturnType<typeof fetchData>>; // { data: string[] }
```

---

## infer in Array Types

Extract types from arrays and tuples.

### Element type

```typescript
type ElementType<T> = T extends (infer E)[] ? E : never;

type A = ElementType<string[]>;     // string
type B = ElementType<number[]>;     // number
type C = ElementType<(string | boolean)[]>; // string | boolean
type D = ElementType<string>;       // never
```

### First and rest

```typescript
type Head<T> = T extends [infer H, ...any[]] ? H : never;
type Tail<T> = T extends [any, ...infer T] ? T : never;

type A = Head<[string, number, boolean]>; // string
type B = Tail<[string, number, boolean]>; // [number, boolean]

type C = Head<[string]>;  // string
type D = Tail<[string]>;  // []
```

### Reverse a tuple

```typescript
type Reverse<T extends any[]> = T extends [infer H, ...infer T]
  ? [...Reverse<T>, H]
  : [];

type A = Reverse<[1, 2, 3]>; // [3, 2, 1]
type B = Reverse<[string]>;  // [string]
type C = Reverse<[]>;        // []
```

### Flatten an array

```typescript
type Flatten<T extends any[]> = T extends [infer H, ...infer T]
  ? H extends any[]
    ? [...Flatten<H>, ...Flatten<T>]
    : [H, ...Flatten<T>]
  : [];

type A = Flatten<[1, [2, 3], [4, [5]]]>; // [1, 2, 3, 4, 5]
```

---

## infer in Template Literals

Extract parts of template literal types.

### Extract before and after

```typescript
type BeforeSlash<T> = T extends `${infer B}/${string}` ? B : never;
type AfterSlash<T> = T extends `${string}/${infer A}` ? A : never;

type A = BeforeSlash<"hello/world">;  // "hello"
type B = AfterSlash<"hello/world">;   // "world"
```

### Extract segments

```typescript
type Split<T extends string, D extends string> = T extends `${infer H}${D}${infer T}`
  ? [H, ...Split<T, D>]
  : [T];

type A = Split<"a/b/c", "/">;  // ["a", "b", "c"]
type B = Split<"hello", "/">;  // ["hello"]
```

### Parse route params

```typescript
type ExtractParam<T extends string> = T extends `:${infer P}` ? P : never;

type A = ExtractParam<":id">;    // "id"
type B = ExtractParam<":name">;  // "name"
type C = ExtractParam<"static">; // never
```

### Extract all params from a route

```typescript
type ExtractParams<T extends string> = T extends `${string}:${infer Param}/${infer Rest}`
  ? Param | ExtractParams<`/${Rest}`>
  : T extends `${string}:${infer Param}`
  ? Param
  : never;

type Route = "/users/:id/posts/:postId/comments/:commentId";
type Params = ExtractParams<Route>; // "id" | "postId" | "commentId"
```

---

## Multiple infer

You can use multiple `infer` declarations in a single conditional type.

```typescript
// Extract both parameter and return types
type FunctionInfo<T> = T extends (first: infer P1, second: infer P2) => infer R
  ? { params: [P1, P2]; return: R }
  : never;

type Info = FunctionInfo<(name: string, age: number) => boolean>;
// { params: [string, number]; return: boolean }
```

### Extract from a pair type

```typescript
type Pair<A = any, B = any> = { first: A; second: B };

type UnpackPair<T> = T extends Pair<infer A, infer B>
  ? { first: A; second: B }
  : never;

type Result = UnpackPair<Pair<string, number>>;
// { first: string; second: number }
```

### Extract from conditional

```typescript
type ExtractBoth<T> = T extends { a: infer A; b: infer B }
  ? { a: A; b: B }
  : never;

type Result = ExtractBoth<{ a: string; b: number }>;
// { a: string; b: number }
```

### Multiple infer in template literals

```typescript
type ParseRoute<T extends string> = T extends `/${infer Segment}/${infer Rest}`
  ? { segment: Segment; rest: Rest }
  : T extends `/${infer Segment}`
  ? { segment: Segment; rest: never }
  : never;

type A = ParseRoute<"/users/posts">;
// { segment: "users"; rest: "posts" }

type B = ParseRoute<"/users">;
// { segment: "users"; rest: never }
```

---

## infer Constraints

You can constrain inferred types using additional extends clauses.

### Constrained infer

```typescript
type ArrayOfNumbers<T> = T extends (infer E extends number)[] ? E[] : never;

type A = ArrayOfNumbers<number[]>;     // number[]
type B = ArrayOfNumbers<(number | string)[]>; // number[]
type C = ArrayOfNumbers<string[]>;     // never (string doesn't extend number)
```

### Constrained infer in function types

```typescript
type StringFunction<T> = T extends (x: infer P extends string) => any ? P : never;

type A = StringFunction<(x: string) => void>;   // string
type B = StringFunction<(x: number) => void>;   // never
type C = StringFunction<(x: string | number) => void>; // string (only string part)
```

### Constrained infer with interface

```typescript
interface Animal {
  name: string;
  age: number;
}

type ExtractAnimal<T> = T extends { type: infer A extends Animal } ? A : never;

type A = ExtractAnimal<{ type: Animal }>; // Animal
type B = ExtractAnimal<{ type: string }>; // never
```

---

## Real-World infer Patterns

### 1. Deep Partial

```typescript
type DeepPartial<T> = T extends object
  ? { [K in keyof T]?: DeepPartial<T[K]> }
  : T;

type Config = {
  db: {
    host: string;
    port: number;
    ssl: boolean;
  };
  cache: {
    host: string;
    ttl: number;
  };
};

type PartialConfig = DeepPartial<Config>;
// {
//   db?: { host?: string; port?: number; ssl?: boolean };
//   cache?: { host?: string; ttl?: number };
// }
```

### 2. Unwrap any type

```typescript
type Unwrap<T> = T extends Promise<infer U>
  ? Unwrap<U>
  : T extends { unwrap(): infer U }
  ? U
  : T;

type A = Unwrap<Promise<string>>;           // string
type B = Unwrap<Promise<Promise<number>>>;  // number
```

### 3. Extract event handler types

```typescript
type EventHandlers = {
  click: (event: MouseEvent) => void;
  keydown: (event: KeyboardEvent) => void;
  focus: (event: FocusEvent) => void;
};

type HandlerParam<T extends keyof EventHandlers> = EventHandlers[T] extends (
  event: infer E
) => any
  ? E
  : never;

type ClickEvent = HandlerParam<"click">; // MouseEvent
type KeyEvent = HandlerParam<"keydown">;  // KeyboardEvent
```

### 4. Type-safe React component props

```typescript
type PropsOf<C> = C extends React.ComponentType<infer P> ? P : never;

type ButtonProps = PropsOf<typeof Button>; // props of Button component
```

### 5. Extract from Redux action

```typescript
type ActionType =
  | { type: "INCREMENT"; amount: number }
  | { type: "DECREMENT"; amount: number }
  | { type: "SET"; value: number };

type ActionPayload<T extends ActionType["type"]> = Extract<ActionType, { type: T }>;

type IncrementPayload = ActionPayload<"INCREMENT">; // { type: "INCREMENT"; amount: number }
```

### 6. Builder pattern

```typescript
type Builder<T> = {
  [K in keyof T as `set${Capitalize<string & K>}`]: (value: T[K]) => Builder<T>;
} & { build: () => T };

function builder<T>(initial: T): Builder<T> {
  const state = { ...initial };
  const result: any = {};

  for (const key in state) {
    result[`set${key.charAt(0).toUpperCase()}${key.slice(1)}`] = (value: any) => {
      state[key] = value;
      return result;
    };
  }

  result.build = () => ({ ...state });
  return result;
}

const userBuilder = builder({ name: "", age: 0, email: "" });
const user = userBuilder.setName("Alice").setAge(30).setEmail("alice@example.com").build();
// { name: string; age: number; email: string }
```

---

## Best Practices

1. **Use `infer` to extract types from complex expressions** — avoid manual type definitions
2. **Use `infer` in conditional types** — it only works in the `extends` clause
3. **Name inferred types clearly** — use meaningful names like `R` for return, `P` for param, `E` for element
4. **Use constraints** — `infer E extends string` to narrow inferred types
5. **Chain inference** — combine multiple conditional types for deep extraction
6. **Don't over-infer** — sometimes explicit types are clearer

---

## Interview Questions

### Q1: What does the `infer` keyword do?

**Answer:** `infer` declares a type variable within a conditional type. It tells TypeScript to infer and capture a type from a specific position. For example, `T extends (...args: any[]) => infer R ? R : never` captures the return type of a function type `T` and names it `R`.

### Q2: Where can `infer` be used?

**Answer:** `infer` can only be used in the `extends` clause of a conditional type. It declares a type variable that is only accessible in the true branch of the conditional type.

### Q3: How do you extract a function's return type using `infer`?

**Answer:** Use `type ReturnType<T> = T extends (...args: any[]) => infer R ? R : never`. The `infer R` captures the return type of the function, and the conditional type returns `R` if `T` is a function or `never` otherwise.

### Q4: Can you use multiple `infer` in one conditional type?

**Answer:** Yes. You can declare multiple inferred type variables, like `T extends (a: infer P, b: infer Q) => infer R ? [P, Q, R] : never`. Each `infer` captures a different type from the expression.

### Q5: How do you constrain an inferred type?

**Answer:** Use `infer E extends SomeType` to constrain the inferred type. For example, `T extends (infer E extends string)[] ? E[] : never` ensures `E` must extend `string`.

### Q6: What is the difference between `infer` and a type parameter?

**Answer:** A type parameter (`<T>`) is declared on a function, class, or type alias and is provided by the caller. `infer` is declared inside a conditional type and captures a type from the expression itself. Type parameters are external; `infer` is internal to the conditional type.
