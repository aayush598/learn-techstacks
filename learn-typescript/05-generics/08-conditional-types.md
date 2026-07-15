# 08 — Conditional Types

## Table of Contents

1. [Conditional Type Syntax](#conditional-type-syntax)
2. [The `infer` Keyword](#infer-keyword)
3. [Distributive Conditional Types](#distributive-conditional-types)
4. [Nested Conditional Types](#nested-conditional-types)
5. [Conditional Types with Unions](#conditional-types-with-unions)
6. [Conditional Type Inference](#conditional-type-inference)
7. [Exclude and Extract Explained](#exclude-and-extract)
8. [Real-World Conditional Types](#real-world-examples)
9. [Best Practices](#best-practices)
10. [Interview Questions](#interview-questions)

---

## Conditional Type Syntax

Conditional types follow the pattern `T extends U ? X : Y`. They check if type `T`
is assignable to `U` and return `X` if true, `Y` if false.

```typescript
type IsString<T> = T extends string ? "yes" : "no";

type A = IsString<"hello">;  // "yes"
type B = IsString<42>;       // "no"
type C = IsString<string>;   // "yes"
```

### Basic Usage

```typescript
type TypeName<T> =
  T extends string ? "string" :
  T extends number ? "number" :
  T extends boolean ? "boolean" :
  T extends undefined ? "undefined" :
  T extends Function ? "function" :
  "object";

type T1 = TypeName<"hello">;   // "string"
type T2 = TypeName<42>;        // "number"
type T3 = TypeName<() => void>; // "function"
type T4 = TypeName<string[]>;  // "object"
```

### Conditional Types in Interfaces

```typescript
interface ApiResponse<T> {
  data: T extends (infer U)[] ? U[] : T;
  status: number;
  isPaginated: T extends Array<unknown> ? true : false;
}

type UserResponse = ApiResponse<User[]>;
// { data: User[]; status: number; isPaginated: true }

type SingleUserResponse = ApiResponse<User>;
// { data: User; status: number; isPaginated: false }
```

---

## The `infer` Keyword

The `infer` keyword declares a **type variable** within a conditional type that
TypeScript infers from the type being checked.

### Basic infer

```typescript
type ReturnType<T> = T extends (...args: any[]) => infer R ? R : never;

type A = ReturnType<() => string>;        // string
type B = ReturnType<(x: number) => void>; // void
type C = ReturnType<string>;              // never (not a function)
```

### Infer Function Parameters

```typescript
type FirstParam<T> = T extends (first: infer P, ...rest: any[]) => any
  ? P
  : never;

type A = FirstParam<(name: string, age: number) => void>; // string
type B = FirstParam<() => void>;                           // never
```

### Infer Promise Resolution

```typescript
type ResolvedPromise<T> = T extends Promise<infer U>
  ? ResolvedPromise<U>  // recursive — unwraps nested promises
  : T;

type A = ResolvedPromise<Promise<string>>;                    // string
type B = ResolvedPromise<Promise<Promise<number>>>;           // number
type C = ResolvedPromise<Promise<Promise<Promise<boolean>>>>; // boolean
```

### Infer Array Element Type

```typescript
type ElementType<T> = T extends Array<infer E> ? E : never;

type A = ElementType<string[]>;   // string
type B = ElementType<number[]>;   // number
type C = ElementType<(string | number)[]>; // string | number
type D = ElementType<string>;     // never
```

### Infer Object Property Types

```typescript
type PropertyType<T, K extends keyof T> = T extends { [P in K]: infer V }
  ? V
  : never;

interface User {
  name: string;
  age: number;
}

type NameType = PropertyType<User, "name">; // string
```

### Infer from Tuples

```typescript
type Head<T extends any[]> = T extends [infer First, ...any[]] ? First : never;
type Tail<T extends any[]> = T extends [any, ...infer Rest] ? Rest : [];
type Last<T extends any[]> = T extends [...any[], infer L] ? L : never;

type A = Head<[1, 2, 3]>;    // 1
type B = Tail<[1, 2, 3]>;    // [2, 3]
type C = Last<[1, 2, 3]>;    // 3
```

### Infer in Template Literals

```typescript
type ExtractRouteParams<T extends string> =
  T extends `${string}:${infer Param}/${infer Rest}`
    ? Param | ExtractRouteParams<Rest>
    : T extends `${string}:${infer Param}`
      ? Param
      : never;

type Params = ExtractRouteParams<"/users/:userId/posts/:postId">;
// "userId" | "postId"
```

### Infer with Multiple Candidates

```typescript
type ReturnTypes<T> = T extends {
  [key: string]: (...args: any[]) => infer R;
} ? R : never;

interface Services {
  getUser: () => User;
  getPost: (id: string) => Post;
  deleteUser: (id: string) => Promise<void>;
}

type AllReturns = ReturnTypes<Services>;
// User | Post | Promise<void>
```

---

## Distributive Conditional Types

When `T` is a naked type parameter, the conditional type **distributes** over the
union — it evaluates the condition for each member independently.

### Basic Distribution

```typescript
type ToArray<T> = T extends any ? T[] : never;

type A = ToArray<string | number>;
// string[] | number[] (distributed)

// NOT: (string | number)[] (non-distributed)
```

### Non-Distributive: Wrap in Tuple

```typescript
type ToArrayNonDist<T> = [T] extends [any] ? T[] : never;

type B = ToArrayNonDist<string | number>;
// (string | number)[] (non-distributed)
```

### Exclude as Distribution

```typescript
type Exclude<T, U> = T extends U ? never : T;

type Result = Exclude<"a" | "b" | "c", "a">;
// Step 1: "a" extends "a" → never
// Step 2: "b" extends "a" → "b"
// Step 3: "c" extends "a" → "c"
// Result: never | "b" | "c" = "b" | "c"
```

### When Distribution is Unwanted

```typescript
// ❌ Distributes — may give unexpected results
type BadIsString<T> = T extends string ? true : false;
type R1 = BadIsString<string | number>; // true | false

// ✅ Non-distributive — checks the whole union
type GoodIsString<T> = [T] extends [string] ? true : false;
type R2 = GoodIsString<string | number>; // false (union is not a string)
```

### Distribution Control with `never`

```typescript
type DistributionControl<T> = [T] extends [never]
  ? "empty"
  : T extends any
    ? "has-value"
    : never;

type A = DistributionControl<never>;        // "empty"
type B = DistributionControl<string>;        // "has-value"
type C = DistributionControl<string | number>; // "has-value"
```

---

## Nested Conditional Types

Conditional types can be nested for complex type-level logic.

```typescript
type TypeKind<T> =
  T extends string
    ? T extends `${number}`
      ? "numeric-string"
      : "string"
    : T extends number
      ? T extends 0
        ? "zero"
        : "positive-number"
      : "other";

type A = TypeKind<"hello">;    // "string"
type B = TypeKind<"42">;       // "numeric-string"
type C = TypeKind<0>;          // "zero"
type D = TypeKind<42>;         // "positive-number"
type E = TypeKind<true>;       // "other"
```

### Nested Conditions for Complex Validation

```typescript
type ValidateInput<T> =
  T extends string
    ? T extends ""
      ? { valid: false; error: "Empty string" }
      : { valid: true; value: T }
    : T extends number
      ? T extends 0
        ? { valid: false; error: "Zero is not allowed" }
        : T > 0
          ? { valid: true; value: T }
          : { valid: false; error: "Negative numbers not allowed" }
      : { valid: false; error: "Unsupported type" };
```

---

## Conditional Types with Unions

When a conditional type distributes over a union, each member is checked independently.

```typescript
type NonNullable<T> = T extends null | undefined ? never : T;

type A = NonNullable<string | null | undefined>; // string
type B = NonNullable<null | undefined>;          // never
```

### Union Results

```typescript
type MessageOf<T> = T extends { message: string } ? T["message"] : never;

interface Email {
  message: string;
  subject: string;
}

interface SMS {
  message: string;
  phone: string;
}

interface PhoneCall {
  phoneNumber: string;
}

type Messages = MessageOf<Email | SMS | PhoneCall>;
// string | string | never = string
```

### Conditional Union Members

```typescript
type Flatten<T> = T extends Array<infer U> ? U : T;

type A = Flatten<string[]>;          // string
type B = Flatten<number[]>;          // number
type C = Flatten<(string | number)[]>; // string | number
type D = Flatten<boolean>;           // boolean
```

---

## Conditional Type Inference

Using `infer` within conditional types to extract and compose types.

### Infer Function Overloads

```typescript
type LastReturnType<T extends (...args: any[]) => any> =
  T extends {
    (...args: any[]): infer R;
    (...args: any[]): infer R;
  }
    ? R
    : never;
```

### Infer Constructor

```typescript
type InstanceOf<T> = T extends new (...args: any[]) => infer I ? I : never;

class MyClass {
  name = "instance";
}

type A = InstanceOf<typeof MyClass>; // MyClass
```

### Infer in Context

```typescript
type PromiseValue<T> = T extends Promise<infer V>
  ? V extends Promise<infer V2>
    ? V2
    : V
  : never;

type A = PromiseValue<Promise<string>>;              // string
type B = PromiseValue<Promise<Promise<number>>>;     // number
type C = PromiseValue<string>;                       // never
```

---

## Exclude and Extract Explained

### Exclude

```typescript
// Implementation
type Exclude<T, U> = T extends U ? never : T;

// Step-by-step for Exclude<"a" | "b" | "c", "a" | "b">
// 1. "a" extends "a" | "b" → never
// 2. "b" extends "a" | "b" → never
// 3. "c" extends "a" | "b" → "c"
// Result: never | never | "c" = "c"
```

### Extract

```typescript
// Implementation
type Extract<T, U> = T extends U ? T : never;

// Step-by-step for Extract<"a" | "b" | "c", "a" | "b">
// 1. "a" extends "a" | "b" → "a"
// 2. "b" extends "a" | "b" → "b"
// 3. "c" extends "a" | "b" → never
// Result: "a" | "b" | never = "a" | "b"
```

### Practical Usage

```typescript
type AllEvents = "click" | "hover" | "focus" | "blur" | "scroll";
type MouseEvents = Extract<AllEvents, "click" | "hover">;
type FocusEvents = Extract<AllEvents, "focus" | "blur">;
type NonMouseEvents = Exclude<AllEvents, MouseEvents>;
// "focus" | "blur" | "scroll"
```

---

## Real-World Examples

### Type-Safe API Router

```typescript
type ExtractParams<T extends string> =
  T extends `${string}:${infer Param}/${infer Rest}`
    ? { [K in Param]: string } & ExtractParams<Rest>
    : T extends `${string}:${infer Param}`
      ? { [K in Param]: string }
      : {};

type Params1 = ExtractParams<"/users/:id">;
// { id: string }

type Params2 = ExtractParams<"/users/:userId/posts/:postId">;
// { userId: string } & { postId: string }
// = { userId: string; postId: string }
```

### Event Handler Types

```typescript
type EventHandlerMap = {
  click: MouseEvent;
  keydown: KeyboardEvent;
  focus: FocusEvent;
  scroll: Event;
};

type EventHandler<T extends keyof EventHandlerMap> =
  (event: EventHandlerMap[T]) => void;

const onClick: EventHandler<"click"> = (event) => {
  console.log(event.clientX, event.clientY); // ✅ MouseEvent properties
};

const onKeyDown: EventHandler<"keydown"> = (event) => {
  console.log(event.key); // ✅ KeyboardEvent properties
};
```

### Deep Readonly with Conditional

```typescript
type DeepReadonly<T> = T extends (infer U)[]
  ? ReadonlyArray<DeepReadonly<U>>
  : T extends object
    ? { readonly [K in keyof T]: DeepReadonly<T[K]> }
    : T;

interface NestedData {
  items: Array<{
    name: string;
    tags: string[];
  }>;
  config: {
    nested: {
      value: string;
    };
  };
}

type FrozenData = DeepReadonly<NestedData>;
// All deeply readonly
```

### String Manipulation with Conditionals

```typescript
type IsEmptyString<T extends string> = T extends "" ? true : false;

type Split<T extends string, D extends string> =
  T extends `${infer Head}${D}${infer Tail}`
    ? [Head, ...Split<Tail, D>]
    : [T];

type Parts = Split<"a.b.c.d", ".">;
// ["a", "b", "c", "d"]

type Join<T extends string[], D extends string> =
  T extends [infer First extends string, ...infer Rest extends string[]]
    ? Rest extends []
      ? First
      : `${First}${D}${Join<Rest, D>}`
    : never;

type Joined = Join<["a", "b", "c"], "-">;
// "a-b-c"
```

### Type-Level Validators

```typescript
type IsValidEmail<T extends string> =
  T extends `${string}@${string}.${string}` ? true : false;

type A = IsValidEmail<"alice@example.com">; // true
type B = IsValidEmail<"not-an-email">;      // false

type IsNumericString<T extends string> =
  T extends `${number}` ? true : false;

type C = IsNumericString<"42">;    // true
type D = IsNumericString<"abc">;   // false
```

### Prisma-like Query Types

```typescript
type WhereClause<T> = {
  [K in keyof T]?: T[K] extends string
    ? { equals?: string; contains?: string; startsWith?: string }
    : T[K] extends number
      ? { equals?: number; gt?: number; lt?: number; gte?: number; lte?: number }
      : { equals?: T[K] };
};

interface Product {
  id: string;
  name: string;
  price: number;
  inStock: boolean;
}

type ProductWhere = WhereClause<Product>;
// {
//   id?: { equals?: string; contains?: string; startsWith?: string };
//   name?: { equals?: string; contains?: string; startsWith?: string };
//   price?: { equals?: number; gt?: number; lt?: number; gte?: number; lte?: number };
//   inStock?: { equals?: boolean };
// }
```

---

## Best Practices

1. **Distribute carefully** — use `[T] extends [U]` when you want to check the
   union as a whole.
2. **Prefer `infer`** for extracting types from complex structures.
3. **Limit nesting depth** — more than 3-4 levels makes types unreadable.
4. **Use conditional types with care** — they can produce cryptic error messages.
5. **Document complex conditionals** with comments explaining the logic.
6. **Test edge cases** — `never`, `unknown`, `any`, and unions can produce surprising results.

---

## Interview Questions

**Q1: What is a conditional type?**

A type that uses `T extends U ? X : Y` syntax to choose between types based on type
relationships. It evaluates at compile time, not runtime.

**Q2: What does `infer` do?**

`infer` declares a type variable within a conditional type that TypeScript infers from
the matched type. For example, `T extends Promise<infer U> ? U : never` extracts the
Promise resolution type.

**Q3: What are distributive conditional types?**

When `T` is a naked type parameter, the conditional distributes over unions — each
member is checked independently. Wrap in `[T]` to prevent distribution.

**Q4: How does `Exclude<T, U>` work?**

`Exclude<"a" | "b" | "c", "a">` distributes: "a" extends "a" → never, "b" → "b",
"c" → "c". Result: `"b" | "c"`.

**Q5: Can you use conditional types in interfaces?**

Yes, but they cannot use `infer` in interface declarations — only in type aliases.
Interfaces can reference conditional types via type aliases.
