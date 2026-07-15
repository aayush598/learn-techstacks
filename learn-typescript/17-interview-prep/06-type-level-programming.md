# Type-Level Programming in TypeScript

## The Ultimate Interview Prep Guide

---

## What is Type-Level Programming

TypeScript's type system is **Turing-complete** — meaning you can perform arbitrary computation entirely within the type system, without any runtime code. Type-level programming is the practice of writing types that compute new types from input types, using conditional types, mapped types, template literals, recursive types, and inference.

### Compile-Time vs Runtime

```typescript
// Runtime programming — code executes when you run the program
function add(a: number, b: number): number {
  return a + b; // runs at runtime
}

// Type-level programming — TypeScript compiler resolves this
type Sum<A extends number, B extends number> = /* ... */;
type Result = Sum<2, 3>; // resolved to 5 at compile time only
// Sum<2, 3> has ZERO runtime cost — it only exists during type checking
```

### Why It Matters

- Catch bugs before code runs — impossible states become unrepresentable
- Eliminate runtime validation — types serve as documentation and contract
- Build self-documenting APIs — generic constraints describe exactly what's allowed
- Required for advanced library design — React, Prisma, tRPC all use this heavily
- Common in senior/staff-level interviews

---

## Type-Level Primitives

### Conditional Types = if/else

```typescript
type IsString<T> = T extends string ? true : false;

type A = IsString<"hello">; // true
type B = IsString<42>;      // false

// Distributed conditional types — when T is a union, the conditional distributes
type ToUpper<T> = T extends string ? Uppercase<T> : never;
type C = ToUpper<"a" | "b" | "c">; // "A" | "B" | "C"
// Equivalent to: ToUpper<"a"> | ToUpper<"b"> | ToUpper<"c">

// Non-distributive conditional — wrap in tuple to prevent distribution
type ToUpperNonDist<T> = [T] extends [string] ? Uppercase<T> : never;
type D = ToUpperNonDist<"a" | "b">; // never (because ["a"|"b"] is not assignable to [string])
```

### Mapped Types = loops

```typescript
// A mapped type iterates over every key in a type — like a for..of loop
type Stringify<T> = {
  [K in keyof T]: string;
};

interface User { name: string; age: number; }
type UserStrings = Stringify<User>; // { name: string; age: string; }

// Adding/removing modifiers with +/- prefixes
type Mutable<T> = {
  -readonly [K in keyof T]: T[K];
};

type Optional<T> = {
  [K in keyof T]?: T[K];
};
```

### Template Literals = string manipulation

```typescript
type Greet<Name extends string> = `Hello, ${Name}!`;
type Msg = Greet<"Alice">; // "Hello, Alice!"

// Pattern matching with template literals
type ExtractId<Route extends string> =
  Route extends `/api/users/${infer Id}` ? Id : never;

type Id = ExtractId<"/api/users/42">; // "42"
```

### Indexed Access = object property access

```typescript
interface Config {
  db: { host: string; port: number };
  api: { url: string; timeout: number };
}

type DbHost = Config["db"]["host"]; // string
type AllUrls = Config["api" | "db"]; // { host: string; port: number; url: string; timeout: number }
```

### Recursive Types = recursion

```typescript
// Build tuple of length N recursively
type BuildTuple<N extends number, T extends any[] = []> =
  T["length"] extends N ? T : BuildTuple<N, [...T, unknown]>;

type Tuple5 = BuildTuple<5>; // [unknown, unknown, unknown, unknown, unknown]
```

### Union Types = iteration

```typescript
type Colors = "red" | "green" | "blue";
// Union distributes over conditional types — effectively iterating each member
type IsWarm<T> = T extends "red" | "orange" ? "warm" : "cool";
type Result = IsWarm<Colors>; // "warm" | "cool" | "cool"
```

### never = empty state / impossible

```typescript
// never is the bottom type — no value can inhabit it
type Impossible = never;

// Used as identity element in unions
type UnionWithNever<T> = T | never; // T (never is identity for union)
type IntersectionWithNever<T> = T & never; // never (never is annihilator for intersection)
```

---

## Built-in Utility Types — Implementations from Scratch

### 1. Partial\<T\>

```typescript
type MyPartial<T> = {
  [K in keyof T]?: T[K];
};

// Usage
interface User { name: string; age: number; email: string; }
type PartialUser = MyPartial<User>;
// { name?: string; age?: number; email?: string; }
```

### 2. Required\<T\>

```typescript
type MyRequired<T> = {
  [K in keyof T]-?: T[K];
};

type FullUser = MyRequired<PartialUser>;
// { name: string; age: number; email: string; }
```

### 3. Readonly\<T\>

```typescript
type MyReadonly<T> = {
  readonly [K in keyof T]: T[K];
};

const user: MyReadonly<User> = { name: "Alice", age: 30, email: "a@b.com" };
// user.name = "Bob"; // Error: Cannot assign to 'name' because it is a read-only property
```

### 4. Pick\<T, K\>

```typescript
type MyPick<T, K extends keyof T> = {
  [P in K]: T[P];
};

type NameAndAge = MyPick<User, "name" | "age">;
// { name: string; age: number; }
```

### 5. Omit\<T, K\>

```typescript
type MyOmit<T, K extends keyof any> = Pick<T, Exclude<keyof T, K>>;

type WithoutEmail = MyOmit<User, "email">;
// { name: string; age: number; }
```

### 6. Record\<K, V\>

```typescript
type MyRecord<K extends keyof any, V> = {
  [P in K]: V;
};

type ColorMap = MyRecord<"red" | "green" | "blue", string>;
// { red: string; green: string; blue: string; }
```

### 7. Exclude\<T, U\>

```typescript
type MyExclude<T, U> = T extends U ? never : T;

type T1 = MyExclude<"a" | "b" | "c", "a">; // "b" | "c"
type T2 = MyExclude<string | number | boolean, string>; // number | boolean
```

### 8. Extract\<T, U\>

```typescript
type MyExtract<T, U> = T extends U ? T : never;

type T1 = MyExtract<"a" | "b" | "c", "a" | "b">; // "a" | "b"
type T2 = MyExtract<string | number | boolean, string>; // string
```

### 9. NonNullable\<T\>

```typescript
type MyNonNullable<T> = T extends null | undefined ? never : T;

type T1 = MyNonNullable<string | null | undefined>; // string
type T2 = MyNonNullable<0 | "" | false | null | undefined>; // 0 | "" | false
```

### 10. ReturnType\<T\>

```typescript
type MyReturnType<T extends (...args: any[]) => any> =
  T extends (...args: any[]) => infer R ? R : never;

function greet(name: string): string { return `Hello, ${name}`; }
function getNumber(): number { return 42; }

type T1 = MyReturnType<typeof greet>; // string
type T2 = MyReturnType<typeof getNumber>; // number
```

### 11. Parameters\<T\>

```typescript
type MyParameters<T extends (...args: any[]) => any> =
  T extends (...args: infer P) => any ? P : never;

type T1 = MyParameters<(a: string, b: number) => void>; // [a: string, b: number]
type T2 = MyParameters<() => void>; // []
```

### 12. ConstructorParameters\<T\>

```typescript
type MyConstructorParameters<T extends abstract new (...args: any) => any> =
  T extends abstract new (...args: infer P) => any ? P : never;

class HttpClient {
  constructor(public baseUrl: string, public timeout: number) {}
}

type T1 = MyConstructorParameters<typeof HttpClient>; // [baseUrl: string, timeout: number]
```

### 13. InstanceType\<T\>

```typescript
type MyInstanceType<T extends abstract new (...args: any) => any> =
  T extends abstract new (...args: any) => infer R ? R : any;

type T1 = MyInstanceType<typeof HttpClient>; // HttpClient
```

### 14. Awaited\<T\>

```typescript
type MyAwaited<T> =
  T extends Promise<infer U> ? MyAwaited<U> : T;

type T1 = MyAwaited<Promise<string>>; // string
type T2 = MyAwaited<Promise<Promise<number>>>; // number
type T3 = MyAwaited<boolean>; // boolean
```

### 15. ReadonlyArray\<T\>

```typescript
type MyReadonlyArray<T> = readonly T[];

const arr: MyReadonlyArray<number> = [1, 2, 3];
// arr.push(4); // Error: Property 'push' does not exist on type 'readonly number[]'
```

### 16. Parameters with Labeled Tuples

```typescript
type LabeledParameters<T extends (...args: any[]) => any> =
  T extends (...args: infer P) => any
    ? { [K in keyof P as K extends `${number}` ? never : K]: P[K] } extends infer L
      ? [keyof L extends never ? never : L, ...any[]] extends infer _
        ? never
        : never
      : never
    : never;
// Labeled tuples preserve parameter names in the type
type Fn = (name: string, age: number, email: string) => void;
type Params = Parameters<Fn>; // [name: string, age: number, email: string]
```

---

## Advanced Type-Level Utilities — Implement from Scratch

### 1. UnionToIntersection\<U\>

```typescript
type UnionToIntersection<U> =
  (U extends any ? (x: U) => void : never) extends (x: infer I) => void
    ? I
    : never;

type T1 = UnionToIntersection<{ a: string } | { b: number }>;
// { a: string } & { b: number }

// How it works:
// 1. Distributes U into a union of functions: ((x: {a: string}) => void) | ((x: {b: number}) => void)
// 2. The outer extends catches both: (x: {a: string} & {b: number}) => void
// 3. Infer extracts the intersection
```

### 2. DeepPartial\<T\>

```typescript
type DeepPartial<T> = {
  [K in keyof T]?: T[K] extends object ? DeepPartial<T[K]> : T[K];
};

interface Config {
  db: { host: string; port: number; credentials: { user: string; pass: string } };
  api: { url: string; };
}

type PartialConfig = DeepPartial<Config>;
// { db?: { host?: string; port?: number; credentials?: { user?: string; pass?: string } }; api?: { url?: string } }
```

### 3. DeepReadonly\<T\>

```typescript
type DeepReadonly<T> = {
  readonly [K in keyof T]: T[K] extends object ? DeepReadonly<T[K]> : T[K];
};

const config: DeepReadonly<Config> = { /* ... */ };
// config.db.host = "new"; // Error: readonly
// config.db.credentials.user = "admin"; // Error: readonly
```

### 4. DeepRequired\<T\>

```typescript
type DeepRequired<T> = {
  [K in keyof T]-?: T[K] extends object ? DeepRequired<T[K]> : T[K];
};

type FullConfig = DeepRequired<DeepPartial<Config>>;
// All nested properties are required again
```

### 5. Mutable\<T\>

```typescript
type Mutable<T> = {
  -readonly [K in keyof T]: T[K];
};

interface Frozen {
  readonly x: number;
  readonly y: number;
}

type MutableFrozen = Mutable<Frozen>; // { x: number; y: number; }
```

### 6. Prettify\<T\>

```typescript
type Prettify<T> = { [K in keyof T]: T[K] } & {};

// Intersections like { a: string } & { b: number } display as an intersection in tooltips
// Prettify flattens them into a single object type for readability
type Pretty = Prettify<{ a: string } & { b: number }>;
// Hover shows: { a: string; b: number }
```

### 7. NoInfer\<T\>

```typescript
type NoInfer<T> = [T][T extends any ? 0 : never];

// Prevents TypeScript from using context to infer T
function createFSM<S extends string>(transition: S, initial: NoInfer<S>): S {
  return transition;
}

// createFSM("running", "idle"); // Error: "idle" is not assignable to "running"
// Without NoInfer, TypeScript would infer S = "running" | "idle"
```

### 8. IsNever\<T\>

```typescript
type IsNever<T> = [T] extends [never] ? true : false;

type T1 = IsNever<never>; // true
type T2 = IsNever<string>; // false
type T3 = IsNever<undefined>; // false

// Why not just `T extends never`?
// Because `never extends never` distributes and produces never (the empty union),
// which is falsy in a conditional. Wrapping in tuple prevents distribution.
```

### 9. IsAny\<T\>

```typescript
type IsAny<T> = 0 extends (1 & T) ? true : false;

type T1 = IsAny<any>;    // true
type T2 = IsAny<unknown>; // false
type T3 = IsAny<string>;  // false
// Only `any` satisfies `0 extends (1 & T)` because `1 & any` = `any`, and `0 extends any` = true
```

### 10. IsUnknown\<T\>

```typescript
type IsUnknown<T> =
  IsAny<T> extends true ? false :
  unknown extends T ? true : false;

type T1 = IsUnknown<unknown>; // true
type T2 = IsUnknown<any>;     // false
type T3 = IsNever<unknown>;   // false (note: unknown extends unknown = true)
// Actually this gives: IsNever is a separate check; this returns false for unknown itself
```

### 11. Equals\<A, B\>

```typescript
type Equals<A, B> =
  (<T>() => T extends A ? 1 : 2) extends
  (<T>() => T extends B ? 1 : 2) ? true : false;

type T1 = Equals<string, string>; // true
type T2 = Equals<string, number>; // false
type T3 = Equals<any, unknown>;   // false
type T4 = Equals<[1, 2], [1, 2]>; // true
// This trick exploits TypeScript's internal function type comparison
```

### 12. Not\<T\>

```typescript
type Not<T extends boolean> = T extends true ? false : true;

type T1 = Not<true>;  // false
type T2 = Not<false>; // true
```

### 13. And\<A, B\>

```typescript
type And<A extends boolean, B extends boolean> =
  A extends true ? B extends true ? true : false : false;

type T1 = And<true, true>;   // true
type T2 = And<true, false>;  // false
type T3 = And<false, true>;  // false
type T4 = And<false, false>; // false
```

### 14. Or\<A, B\>

```typescript
type Or<A extends boolean, B extends boolean> =
  A extends true ? true : B extends true ? true : false;

type T1 = Or<true, false>;  // true
type T2 = Or<false, false>; // false
```

### 15. If\<C, T, F\>

```typescript
type If<C extends boolean, T, F> = C extends true ? T : F;

type T1 = If<true, "yes", "no">;  // "yes"
type T2 = If<false, "yes", "no">; // "no"
```

### 16. Head\<T\>

```typescript
type Head<T extends any[]> = T extends [infer H, ...any[]] ? H : never;

type T1 = Head<[1, 2, 3]>; // 1
type T2 = Head<["a", "b"]>; // "a"
type T3 = Head<[]>;          // never
```

### 17. Tail\<T\>

```typescript
type Tail<T extends any[]> = T extends [any, ...infer Rest] ? Rest : [];

type T1 = Tail<[1, 2, 3]>; // [2, 3]
type T2 = Tail<[1]>;        // []
type T3 = Tail<[]>;          // []
```

### 18. Last\<T\>

```typescript
type Last<T extends any[]> = T extends [...any[], infer L] ? L : never;

type T1 = Last<[1, 2, 3]>; // 3
type T2 = Last<["a"]>;      // "a"
type T3 = Last<[]>;          // never
```

### 19. Length\<T\>

```typescript
type Length<T extends any[]> = T["length"];

type T1 = Length<[1, 2, 3]>; // 3
type T2 = Length<[]>;          // 0
```

### 20. Push\<T, V\>

```typescript
type Push<T extends any[], V> = [...T, V];

type T1 = Push<[1, 2], 3>; // [1, 2, 3]
type T2 = Push<[], "a">;    // ["a"]
```

### 21. Unshift\<T, V\>

```typescript
type Unshift<T extends any[], V> = [V, ...T];

type T1 = Unshift<[2, 3], 1>; // [1, 2, 3]
type T2 = Unshift<[], "a">;    // ["a"]
```

### 22. Concat\<A, B\>

```typescript
type Concat<A extends any[], B extends any[]> = [...A, ...B];

type T1 = Concat<[1, 2], [3, 4]>; // [1, 2, 3, 4]
type T2 = Concat<[], [1]>;         // [1]
```

### 23. Flatten\<T\>

```typescript
type Flatten<T extends any[]> =
  T extends [infer H, ...infer Rest]
    ? H extends any[]
      ? [...Flatten<H>, ...Flatten<Rest>]
      : [H, ...Flatten<Rest>]
    : T;

type T1 = Flatten<[1, [2, 3], [4, [5]]]>; // [1, 2, 3, 4, 5]
type T2 = Flatten<[[1, 2], [3, 4]]>;       // [1, 2, 3, 4]
```

### 24. Reverse\<T\>

```typescript
type Reverse<T extends any[]> =
  T extends [infer H, ...infer Rest]
    ? [...Reverse<Rest>, H]
    : T;

type T1 = Reverse<[1, 2, 3]>; // [3, 2, 1]
type T2 = Reverse<["a", "b"]>; // ["b", "a"]
```

### 25. Zip\<A, B\>

```typescript
type Zip<A extends any[], B extends any[]> =
  A extends [infer AH, ...infer AR]
    ? B extends [infer BH, ...infer BR]
      ? [[AH, BH], ...Zip<AR, BR>]
      : []
    : [];

type T1 = Zip<[1, 2, 3], ["a", "b", "c"]>; // [[1, "a"], [2, "b"], [3, "c"]]
type T2 = Zip<[1, 2], ["a"]>;                // [[1, "a"]]
```

### 26. Includes\<T, V\>

```typescript
type Includes<T extends any[], V> =
  T extends [infer H, ...infer Rest]
    ? Equal<H, V> extends true
      ? true
      : Includes<Rest, V>
    : false;

type Equal<A, B> =
  (<T>() => T extends A ? 1 : 2) extends (<T>() => T extends B ? 1 : 2) ? true : false;

type T1 = Includes<[1, 2, 3], 2>; // true
type T2 = Includes<["a", "b"], "c">; // false
type T3 = Includes<[true, false], true>; // true
```

### 27. Filter\<T, F\>

```typescript
type Filter<T extends any[], F> =
  T extends [infer H, ...infer Rest]
    ? H extends F
      ? [H, ...Filter<Rest, F>]
      : Filter<Rest, F>
    : [];

type T1 = Filter<[1, "hello", 2, "world", 3], string>; // ["hello", "world"]
type T2 = Filter<[1, 2, 3], number>;                     // [1, 2, 3]
```

### 28. Map\<T, F\>

```typescript
type MapTuple<T extends any[], F extends (arg: any) => any> =
  T extends [infer H, ...infer Rest]
    ? [F extends (arg: H) => infer R ? R : never, ...MapTuple<Rest, F>]
    : [];

type Double = (x: number) => number;
type ToString = (x: any) => string;

type T1 = MapTuple<[1, 2, 3], typeof Double>; // [number, number, number]
// More useful with mapped transforms:
type MapToNumber<T extends any[]> = { [K in keyof T]: number };
type T2 = MapToNumber<[1, "a", true]>; // [number, number, number]
```

### 29. Join\<T, S\>

```typescript
type Join<T extends string[], D extends string> =
  T extends [infer H extends string, ...infer Rest extends string[]]
    ? Rest extends []
      ? H
      : `${H}${D}${Join<Rest, D>}`
    : "";

type T1 = Join<["hello", "world"], " ">;  // "hello world"
type T2 = Join<["a", "b", "c"], "-">;     // "a-b-c"
type T3 = Join<["only"], "x">;              // "only"
type T4 = Join<[], "-">;                    // ""
```

### 30. Split\<S, D\>

```typescript
type Split<S extends string, D extends string> =
  S extends `${infer H}${D}${infer Rest}`
    ? [H, ...Split<Rest, D>]
    : [S];

type T1 = Split<"hello world", " ">;     // ["hello", "world"]
type T2 = Split<"a-b-c", "-">;           // ["a", "b", "c"]
type T3 = Split<"no-separator", "x">;     // ["no-separator"]
```

### 31. Replace\<S, F, T\>

```typescript
type Replace<S extends string, F extends string, T extends string> =
  S extends `${infer Before}${F}${infer After}`
    ? `${Before}${T}${After}`
    : S;

type T1 = Replace<"Hello World", "World", "TS">; // "Hello TS"
type T2 = Replace<"aaa", "a", "b">;               // "baa" (only first occurrence)
```

### 32. Trim\<S\>

```typescript
type Trim<S extends string> =
  S extends ` ${infer Rest}` ? Trim<Rest> :
  S extends `${infer Rest} ` ? Trim<Rest> :
  S;

type T1 = Trim<"  hello  ">; // "hello"
type T2 = Trim<" no spaces ">; // "no spaces"
```

### 33. ParseInt\<S\>

```typescript
type ParseInt<S extends string> =
  S extends `${infer N extends number}` ? N : never;

type T1 = ParseInt<"42">; // 42
type T2 = ParseInt<"abc">; // never
type T3 = ParseInt<"3.14">; // 3.14 (partial)
```

### 34. TupleToUnion\<T\>

```typescript
type TupleToUnion<T extends any[]> = T[number];

type T1 = TupleToUnion<[1, 2, 3]>; // 1 | 2 | 3
type T2 = TupleToUnion<["a", "b"]>; // "a" | "b"
```

### 35. UnionToTuple\<U\> (Advanced)

```typescript
type UnionToTuple<U, T extends any[] = []> =
  U extends U ? UnionToTuple<Exclude<U, U>, [U, ...T]> : T;
// Note: This is a simplified version. True UnionToTuple is notoriously difficult
// and requires workarounds. The above loses order in practice.
// In production, use libraries like ts-toolbelt or type-fest.
```

---

## Type-Level Algorithms

### Type-Level Arithmetic

```typescript
// Helper: build tuple of length N
type BuildTuple<N extends number, T extends any[] = []> =
  T["length"] extends N ? T : BuildTuple<N, [...T, unknown]>;

// Add two numbers
type Add<A extends number, B extends number> =
  [...BuildTuple<A>, ...BuildTuple<B>]["length"] & number;

type T1 = Add<3, 4>; // 7

// Subtract: build B-length tuple from A-length tuple
type Subtract<A extends number, B extends number> =
  BuildTuple<A> extends [...BuildTuple<B>, ...infer Rest]
    ? Rest["length"]
    : never;

type T2 = Subtract<7, 3>; // 4

// Multiply: add A to itself B times
type Multiply<A extends number, B extends number, R extends any[] = []> =
  R["length"] extends B
    ? R["length"]
    : Multiply<A, B, [...R, ...BuildTuple<A>]>;

type T3 = Multiply<3, 4>; // 12

// Divide: how many times does B fit into A?
type Divide<A extends number, B extends number, R extends any[] = []> =
  A extends 0 ? R["length"] :
  R["length"] extends A ? never :
  Divide<Subtract<A, B> extends number ? Subtract<A, B> : never, B, [...R, unknown]>;

type T4 = Divide<12, 3>; // 4
```

### Type-Level Fibonacci

```typescript
type Fib<N extends number, A extends any[] = [1], B extends any[] = [1], I extends any[] = []> =
  I["length"] extends N
    ? A["length"]
    : Fib<N, [...A, ...B], A, [...I, unknown]>;

type F0 = Fib<0>;  // 1
type F5 = Fib<5>;  // 8
type F10 = Fib<10>; // 89
```

### Type-Level Factorial

```typescript
type Factorial<N extends number, R extends number = 1> =
  N extends 0 ? R :
  Factorial<Subtract<N, 1> extends number ? Subtract<N, 1> : never, Multiply<R, N> extends number ? Multiply<R, N> : never>;

type F5 = Factorial<5>; // 120
type F0 = Factorial<0>; // 1
```

### Type-Level Sorting (Bubble Sort)

```typescript
type Swap<T extends any[], I extends number, J extends number> =
  T extends [...infer Before extends any[], infer AtI, ...infer Middle extends any[], infer AtJ, ...infer After extends any[]]
    ? [number, ...Before, AtJ, ...Middle, AtI, ...After]
    : T;

type BubbleSort<T extends number[]> =
  T extends [infer A extends number, infer B extends number, ...infer Rest extends number[]]
    ? A extends number
      ? B extends number
        ? number extends B
          ? T
          : `${A}` extends `${infer _AN extends number}`
            ? `${B}` extends `${infer _BN extends number}`
              ? _AN extends number
                ? _BN extends number
                  ? [...BuildTuple<_BN>, ...any[]] extends [...BuildTuple<_AN>, ...any[]]
                    ? [B, ...BubbleSort<[A, ...Rest]>]
                    : [A, ...BubbleSort<[B, ...Rest]>]
                  : T
                : T
              : T
            : T
          : T
        : T
      : T
    : T;
```

### Type-Level Permutation

```typescript
type Permutation<T, U = T> =
  [T] extends [never]
    ? []
    : T extends U
      ? [T, ...Permutation<Exclude<U, T>>]
      : [];

type T1 = Permutation<"A" | "B" | "C">;
// ["A","B","C"] | ["A","C","B"] | ["B","A","C"] | ["B","C","A"] | ["C","A","B"] | ["C","B","A"]
```

---

## Real-World Type-Level Programming

### Type-Safe Route Parameters

```typescript
type ExtractParams<S extends string> =
  S extends `${string}:${infer Param}/${infer Rest}`
    ? { [K in Param | keyof ExtractParams<Rest>]: string }
    : S extends `${string}:${infer Param}`
      ? { [K in Param]: string }
      : {};

type Params = ExtractParams<"/users/:userId/posts/:postId">;
// { userId: string; postId: string }

function navigate<R extends string>(route: R, params: ExtractParams<R>): void {
  // type-safe route navigation
}

navigate("/users/:userId/posts/:postId", { userId: "1", postId: "42" }); // OK
// navigate("/users/:userId", { postId: "42" }); // Error
```

### Type-Safe i18n Key Extraction

```typescript
type Messages = {
  greeting: { en: string; es: string };
  farewell: { en: string; es: string };
  nested: { deep: { message: { en: string; es: string } } };
};

type DeepKeys<T, Prefix extends string = ""> =
  T extends object
    ? { [K in keyof T & string]: DeepKeys<T[K], `${Prefix}${K}.`> }[keyof T & string]
    : `${Prefix extends `${infer P}.` ? P : Prefix}`;

type I18nKey = DeepKeys<Messages>;
// "greeting" | "farewell" | "nested" | "nested.deep" | "nested.deep.message"

function t(key: I18nKey): string { return key; }
t("greeting"); // OK
// t("invalid"); // Error
```

### Type-Safe Event Emitter

```typescript
type EventMap = {
  click: { x: number; y: number };
  change: { value: string };
  submit: { data: FormData };
};

class TypedEmitter<Events extends Record<string, any>> {
  private handlers: { [K in keyof Events]?: Array<(payload: Events[K]) => void> } = {};

  on<K extends keyof Events>(event: K, handler: (payload: Events[K]) => void): void {
    (this.handlers[event] ??= []).push(handler);
  }

  emit<K extends keyof Events>(event: K, payload: Events[K]): void {
    this.handlers[event]?.forEach(h => h(payload));
  }
}

const emitter = new TypedEmitter<EventMap>();
emitter.on("click", (payload) => {
  console.log(payload.x, payload.y); // payload is { x: number; y: number }
});
emitter.emit("click", { x: 1, y: 2 }); // OK
// emitter.emit("click", { value: "test" }); // Error: missing 'x' and 'y'
```

### Type-Safe Deep Get/Set

```typescript
type DeepGet<T, Path extends string> =
  Path extends `${infer Head}.${infer Rest}`
    ? Head extends keyof T
      ? DeepGet<T[Head], Rest>
      : never
    : Path extends keyof T
      ? T[Path]
      : never;

interface Store {
  user: {
    profile: {
      name: string;
      address: { city: string; zip: string };
    };
    settings: { theme: "light" | "dark" };
  };
}

type UserName = DeepGet<Store, "user.profile.name">; // string
type City = DeepGet<Store, "user.profile.address.city">; // string
type Theme = DeepGet<Store, "user.settings.theme">; // "light" | "dark"
```

### Type-Safe SQL Query Builder

```typescript
type QueryResult<T extends string> =
  T extends `SELECT ${infer Cols} FROM ${infer Table}`
    ? Cols extends "*"
      ? any // would be Table mapped to a schema
      : Cols extends `${infer Col}, ${infer Rest}`
        ? { [K in Col]: any } & QueryResult<`SELECT ${Rest} FROM ${Table}`>
        : { [K in Cols]: any }
    : never;

type Q1 = QueryResult<"SELECT name, age FROM users">;
// { name: any } & { age: any }
```

### Type-Safe CSS Properties

```typescript
type CSSValue = `${number}${"px" | "em" | "rem" | "%" | "vh" | "vw"}`;

type CSSProperties = {
  width?: CSSValue;
  height?: CSSValue;
  margin?: CSSValue;
  padding?: CSSValue;
  color?: `#${string}`;
  display?: "block" | "inline" | "flex" | "grid" | "none";
};

function css(props: CSSProperties): string {
  return Object.entries(props).map(([k, v]) => `${k}: ${v}`).join("; ");
}

css({ width: "100px", color: "#ff0000", display: "flex" }); // OK
// css({ width: "100" }); // Error: missing unit
// css({ color: "red" }); // Error: must be hex
```

---

## Interview Questions (25+)

### Q1: Implement Pick\<T, K\> from scratch

```typescript
type MyPick<T, K extends keyof T> = {
  [P in K]: T[P];
};
// Tests:
type A = MyPick<{ a: string; b: number; c: boolean }, "a" | "c">;
// { a: string; c: boolean }
```

### Q2: Implement Omit\<T, K\> from scratch

```typescript
type MyOmit<T, K extends keyof any> = Pick<T, Exclude<keyof T, K>>;
// Or equivalently:
type MyOmit2<T, K extends keyof any> = {
  [P in keyof T as P extends K ? never : P]: T[P];
};
type B = MyOmit<{ a: string; b: number; c: boolean }, "b">;
// { a: string; c: boolean }
```

### Q3: Implement DeepPartial\<T\>

```typescript
type DeepPartial<T> = {
  [K in keyof T]?: T[K] extends object ? DeepPartial<T[K]> : T[K];
};
```

### Q4: Implement UnionToIntersection\<U\>

```typescript
type UnionToIntersection<U> =
  (U extends any ? (x: U) => void : never) extends (x: infer I) => void ? I : never;
```

### Q5: Implement a type-safe Head\<T\> for tuples

```typescript
type Head<T extends any[]> = T extends [infer H, ...any[]] ? H : never;
```

### Q6: Implement Split\<S, D\> that splits a string type

```typescript
type Split<S extends string, D extends string> =
  S extends `${infer H}${D}${infer Rest}`
    ? [H, ...Split<Rest, D>]
    : [S];
```

### Q7: Implement Join\<T, S\> that joins a tuple type

```typescript
type Join<T extends string[], D extends string> =
  T extends [infer H extends string, ...infer Rest extends string[]]
    ? Rest extends []
      ? H
      : `${H}${D}${Join<Rest, D>}`
    : "";
```

### Q8: Implement Includes\<T, V\> for tuples

```typescript
type Includes<T extends any[], V> =
  T extends [infer H, ...infer Rest]
    ? (<X>() => X extends H ? 1 : 2) extends (<X>() => X extends V ? 1 : 2)
      ? true
      : Includes<Rest, V>
    : false;
```

### Q9: Implement Filter\<T, F\> for tuples

```typescript
type Filter<T extends any[], F> =
  T extends [infer H, ...infer Rest]
    ? H extends F ? [H, ...Filter<Rest, F>] : Filter<Rest, F>
    : [];
```

### Q10: Implement a type-safe IsNever\<T\>

```typescript
type IsNever<T> = [T] extends [never] ? true : false;
```

### Q11: Implement a type-safe Equals\<A, B\>

```typescript
type Equals<A, B> =
  (<T>() => T extends A ? 1 : 2) extends (<T>() => T extends B ? 1 : 2) ? true : false;
```

### Q12: What makes TypeScript's type system Turing-complete?

TypeScript's type system is Turing-complete because it has:
1. **Conditional types** — branching (if/else)
2. **Recursive types** — loops/recursion (with tail-call optimization in TS 4.5+)
3. **Template literals** — string manipulation
4. **Indexed access / mapped types** — data access and iteration
5. **Union types** — nondeterminism / set operations
6. **Infinite type depth** (with caveats) — recursion can continue until the compiler's depth limit

You can encode arbitrary computation: addition, multiplication, Fibonacci, even a full interpreter — all at the type level.

### Q13: Explain how mapped types work as loops

```typescript
// Mapped types iterate over every key K in keyof T
// { [K in keyof T]: NewType }
// Additional modifiers: readonly, optional (+/-)
// Key remapping (TS 4.1+): [K in keyof T as NewKey]
type Getters<T> = {
  [K in keyof T as `get${Capitalize<string & K>}`]: () => T[K];
};
// For { name: string } => { getName: () => string }
```

### Q14: Explain how conditional types work as if/else

```typescript
// T extends U ? X : Y
// If T is assignable to U, resolve to X; otherwise Y
// Distributes over unions automatically when T is a naked type parameter
// Wrap in [T] to prevent distribution
```

### Q15: How do recursive types work in TypeScript?

Recursive types call themselves. TypeScript (since 4.1) supports tail-call optimization for certain recursive patterns. Without optimization, recursion depth is limited (~50 levels for some patterns, ~1000 for tail-recursive ones).

```typescript
type Flatten<T extends any[]> =
  T extends [infer H, ...infer Rest]
    ? H extends any[]
      ? [...Flatten<H>, ...Flatten<Rest>]
      : [H, ...Flatten<Rest>]
    : T;
```

### Q16: What are the limitations of TypeScript's type system?

- **Recursion depth limit** — ~50-1000 levels depending on pattern
- **No true tail-call optimization** for all recursive types (only specific patterns)
- **Cannot compute across file boundaries** easily
- **Instantiation depth exceeded** errors with very deep recursion
- **No mutation** — type-level computation is purely functional
- **Performance** — very complex types slow down the compiler significantly
- **Cannot dynamically generate type names** — all types must be statically analyzable

### Q17: Implement type-safe deep property access

```typescript
type DeepGet<T, Path extends string> =
  Path extends `${infer Head}.${infer Rest}`
    ? Head extends keyof T ? DeepGet<T[Head], Rest> : never
    : Path extends keyof T ? T[Path] : never;

function deepGet<T, P extends string>(obj: T, path: P): DeepGet<T, P> {
  return path.split(".").reduce((acc: any, key) => acc?.[key], obj);
}
```

### Q18: Implement a type-safe PathJoin utility

```typescript
type CleanPath<S extends string> =
  S extends `/${infer Rest}` ? CleanPath<Rest> :
  S extends `${infer Rest}/` ? CleanPath<Rest> :
  S extends `${infer A}//${infer B}` ? CleanPath<`${A}/${B}`> :
  S;

type PathJoin<A extends string, B extends string> =
  CleanPath<`${A}/${B}`> extends infer R extends string ? R : never;

type P1 = PathJoin<"/users", "posts">; // "users/posts"
type P2 = PathJoin<"/a//", "/b/">;      // "a/b"
```

### Q19: Implement a type that extracts all event names and their payload types

```typescript
type EventMap = {
  click: { x: number; y: number };
  focus: void;
  input: { value: string };
};

type EventPayloads = {
  [K in keyof EventMap]: { event: K; payload: EventMap[K] };
}[keyof EventMap];

// = { event: "click"; payload: { x: number; y: number } }
// | { event: "focus"; payload: void }
// | { event: "input"; payload: { value: string } }
```

### Q20: How do you prevent circular type references?

- Use interfaces (declaration merging) instead of type aliases for circular structures
- Break cycles with intermediary types
- Use lazy evaluation: `type Lazy<T> = T extends () => infer U ? U : T`
- Use class-based approaches where forward declarations help
- Avoid mutual recursion between type aliases when possible

### Q21: What is tail-call optimization in recursive types?

Tail-call optimization (TCO) in TypeScript (4.5+) means that recursive types where the recursive call is the last operation (in tail position) don't blow the stack. The compiler transforms them into iterative loops internally:

```typescript
// Tail-recursive — optimized:
type Tail<T extends any[]> =
  T extends [any, ...infer Rest] ? Rest : [];

// Non-tail-recursive — NOT optimized (calls Flatten inside a spread):
type Flatten<T extends any[]> =
  T extends [infer H, ...infer Rest]
    ? H extends any[] ? [...Flatten<H>, ...Flatten<Rest>] : [H, ...Flatten<Rest>]
    : T;
```

### Q22: How would you implement a type-safe SQL SELECT type?

```typescript
type Select<T extends string, Columns extends string[]> =
  T extends `FROM ${infer Table}`
    ? { table: Table; columns: Columns; result: Columns[number] }
    : never;

// Or more elaborately with a schema:
type Schema = {
  users: { id: number; name: string; email: string };
  posts: { id: number; title: string; userId: number };
};

type Query<Col extends string, Table extends keyof Schema> =
  Col extends "*"
    ? Schema[Table]
    : Col extends keyof Schema[Table]
      ? Pick<Schema[Table], Col>
      : never;

type R = Query<"name" | "email", "users">;
// { name: string; email: string }
```

### Q23: Implement a type-safe validator that infers output types

```typescript
type Validator<T> = {
  parse: (input: unknown) => T;
  _type: T;
};

function string(): Validator<string> {
  return {
    _type: "" as string,
    parse: (input) => {
      if (typeof input !== "string") throw new Error("Expected string");
      return input;
    },
  };
}

function object<T extends Record<string, Validator<any>>>(
  shape: T
): Validator<{ [K in keyof T]: T[K]["_type"] }> {
  const keys = Object.keys(shape) as (keyof T)[];
  return {
    _type: {} as any,
    parse: (input) => {
      const obj = input as Record<string, unknown>;
      const result = {} as any;
      for (const key of keys) {
        result[key] = shape[key].parse(obj[key as string]);
      }
      return result;
    },
  };
}

const schema = object({
  name: string(),
  age: string(), // in real life: number()
});

type Inferred = ReturnType<typeof schema.parse>;
// { name: string; age: string }
```

### Q24: What are phantom types and how are they useful?

Phantom types carry type information that has no runtime representation — they're used to encode state machines or constraints at the type level:

```typescript
type Valid = { readonly _brand: "valid" };
type Invalid = { readonly _brand: "invalid" };

type Email<State = Invalid> = string & { readonly _state: State };

function createEmail(input: string): Email<Invalid> {
  return input as Email<Invalid>;
}

function validateEmail(email: Email<Invalid>): Email<Valid> {
  if (!email.includes("@")) throw new Error("Invalid");
  return email as Email<Valid>;
}

function sendEmail(email: Email<Valid>): void {
  // only accepts validated emails
  console.log("Sending to", email);
}

const raw = createEmail("test@example.com");
// sendEmail(raw); // Error: Email<Invalid> not assignable to Email<Valid>
const valid = validateEmail(raw);
sendEmail(valid); // OK
```

### Q25: Implement a type-safe builder pattern

```typescript
type BuilderShape = { [key: string]: any };

type Builder<T extends BuilderShape, Built extends Partial<T> = {}> = {
  set<K extends Exclude<keyof T, keyof Built>>(
    key: K,
    value: T[K]
  ): Builder<T, Built & { [P in K]: T[K] }>;

  build(): keyof T extends keyof Built ? T : never;
};

function builder<T extends BuilderShape>(): Builder<T> {
  const data = {} as any;
  const self: any = {
    set(key: string, value: any) {
      data[key] = value;
      return self;
    },
    build() {
      return data;
    },
  };
  return self;
}

interface User {
  name: string;
  age: number;
  email: string;
}

const user = builder<User>()
  .set("name", "Alice")
  .set("age", 30)
  .set("email", "a@b.com")
  .build();
// user is type User

// const bad = builder<User>().set("name", "Alice").build();
// Error: build() returns `never` because not all required keys are set
```

### Q26: What is the difference between `extends` and `infer`?

`extends` checks assignability (like `instanceof` for types). `infer` extracts a type from within another type within a conditional branch:

```typescript
// extends: checks if T is assignable to string
type IsString<T> = T extends string ? true : false;

// infer: extracts the return type from a function type
type Ret<T> = T extends (...args: any[]) => infer R ? R : never;

// Combined: infer inside extends for pattern matching
type UnpackPromise<T> = T extends Promise<infer U> ? U : T;
```

---

## Best Practices

1. **Wrap naked types in tuples** to prevent unwanted distribution: `[T] extends [U]` instead of `T extends U`
2. **Use `never` for impossible states** — it naturally disappears from unions
3. **Prefer interfaces for public APIs** — they produce better error messages
4. **Keep recursive types tail-recursive** when possible for better performance
5. **Use `[keyof T]` constraint patterns** to ensure key safety: `K extends keyof T`
6. **Use key remapping** (`as`) to transform mapped type keys: `[K in keyof T as NewKey]`
7. **Use distributive conditional types** intentionally — sometimes you want distribution, sometimes you don't
8. **Test your types** with `type Assert<T, Expected> = T extends Expected ? Expected extends T ? true : false : false;`
9. **Name intermediate types** — deeply nested inline types are unreadable
10. **Avoid `any` in utility types** — use `unknown` and narrow: `T extends (...args: unknown[]) => any`
