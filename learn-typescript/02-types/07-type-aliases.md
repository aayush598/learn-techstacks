# Type Aliases in TypeScript

## Table of Contents

1. [Overview](#overview)
2. [Type Alias Syntax](#type-alias-syntax)
3. [Aliasing Primitives](#aliasing-primitives)
4. [Aliasing Objects](#aliasing-objects)
5. [Aliasing Functions](#aliasing-functions)
6. [Aliasing Unions](#aliasing-unions)
7. [Aliasing Tuples](#aliasing-tuples)
8. [Recursive Type Aliases](#recursive-type-aliases)
9. [Type Alias vs Variable](#type-alias-vs-variable)
10. [Type Hoisting Behavior](#type-hoisting-behavior)
11. [Best Practices](#best-practices)
12. [Interview Questions](#interview-questions)

---

## Overview

Type aliases create a new name for an existing type using the `type` keyword. They don't create a new type — they create a new **name** for an existing one.

```typescript
// Without type alias
function greet(name: string): string {
  return `Hello, ${name}!`;
}

// With type alias
type Name = string;
function greet2(name: Name): string {
  return `Hello, ${name}!`;
}
```

---

## Type Alias Syntax

```typescript
// Basic syntax
type Identifier = Type;

// Multiple type aliases
type UserID = string | number;
type Callback = (data: string) => void;
type Point = { x: number; y: number };

// Type aliases can reference other type aliases
type Coordinate = Point;
type NamedCoordinate = Coordinate & { name: string };

// Intersection in type aliases
type Timestamped = { createdAt: Date; updatedAt: Date };
type User = { name: string; age: number };
type UserWithTimestamps = User & Timestamped;
// Equivalent to: { name: string; age: number; createdAt: Date; updatedAt: Date }
```

---

## Aliasing Primitives

```typescript
// Create descriptive names for primitives
type UserID = string;
type Email = string;
type Age = number;
type IsActive = boolean;
type Timestamp = number;

// These are all still the underlying primitive types
const userId: UserID = "abc-123";
const email: Email = "alice@example.com";
const age: Age = 30;
const active: IsActive = true;
const ts: Timestamp = Date.now();

// They don't prevent mixing (type aliases are transparent)
const id: UserID = age; // No error! Both are number/string underneath

// But they add documentation value
function createUser(id: UserID, email: Email, age: Age): void {
  // The parameter names make the API clear
}

// Template literal type aliases
type HTTPMethod = "GET" | "POST" | "PUT" | "DELETE";
type APIPath = `/${string}`;
type Route = `${HTTPMethod} ${APIPath}`;

// Literal type aliases
type DiceRoll = 1 | 2 | 3 | 4 | 5 | 6;
type Month = 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12;
```

---

## Aliasing Objects

```typescript
// Object type alias
interface User {
  id: number;
  name: string;
  email: string;
  isActive: boolean;
}

// Type alias for object (using type keyword)
type Product = {
  id: number;
  name: string;
  price: number;
  description?: string;
};

// Intersection of object types
type Timestamped = { createdAt: Date; updatedAt: Date };
type SoftDeletable = { deletedAt: Date | null };
type Entity = { id: number } & Timestamped & SoftDeletable;
// { id: number; createdAt: Date; updatedAt: Date; deletedAt: Date | null }

// Generic object type alias
type ApiResponse<T> = {
  data: T;
  status: number;
  message: string;
};

type UserResponse = ApiResponse<User>;
type ProductResponse = ApiResponse<Product>;

// Mapped types
type Optional<T> = {
  [K in keyof T]?: T[K];
};

type Readonly2<T> = {
  readonly [K in keyof T]: T[K];
};

// Conditional mapped types
type NullableStrings<T> = {
  [K in keyof T]: T[K] extends string ? T[K] | null : T[K];
};

type UserWithNullables = NullableStrings<User>;
// { id: number; name: string | null; email: string | null; isActive: boolean }
```

---

## Aliasing Functions

```typescript
// Function type alias
type Callback = (data: string) => void;
type Predicate = (value: unknown) => boolean;
type Mapper<T, U> = (value: T) => U;
type Reducer<T, U> = (acc: U, value: T) => U;
type AsyncOperation = () => Promise<void>;

// Using function type aliases
function processData(data: string, callback: Callback): void {
  callback(data);
}

function filterArray<T>(arr: T[], predicate: Predicate): T[] {
  return arr.filter(predicate);
}

function mapArray<T, U>(arr: T[], mapper: Mapper<T, U>): U[] {
  return arr.map(mapper);
}

// Function type alias with overloads
type FormatFn = {
  (value: number): string;
  (value: Date): string;
  (value: number, locale: string): string;
};

// Function type alias with this parameter
type ClickHandler = (this: HTMLElement, event: MouseEvent) => void;

// Higher-order function types
type Middleware<T> = (next: T) => T;
type Plugin<T> = (config: T) => T;

// Function type alias in objects
type EventHandlers = {
  onClick: (event: MouseEvent) => void;
  onHover: (event: MouseEvent) => void;
  onFocus: (event: FocusEvent) => void;
};

// Callable type alias
type CallMe = {
  (name: string): string;
  (name: string, greeting: string): string;
};
```

---

## Aliasing Unions

```typescript
// Union type aliases
type StringOrNumber = string | number;
type Nullable<T> = T | null;
type Maybe<T> = T | null | undefined;

// Discriminated unions
type Shape =
  | { kind: "circle"; radius: number }
  | { kind: "rectangle"; width: number; height: number }
  | { kind: "triangle"; base: number; height: number };

// API response union
type APIResult<T> =
  | { success: true; data: T }
  | { success: false; error: string };

// State union (common in React)
type RequestState<T> =
  | { status: "idle" }
  | { status: "loading" }
  | { status: "success"; data: T }
  | { status: "error"; error: Error };

// Using discriminated union
function handleResult(result: APIResult<User>): void {
  if (result.success) {
    console.log(result.data); // narrowed to { success: true; data: T }
  } else {
    console.error(result.error); // narrowed to { success: false; error: string }
  }
}

// Exhaustive union
type DayOfWeek = "monday" | "tuesday" | "wednesday" | "thursday" | "friday" | "saturday" | "sunday";
type Weekend = Extract<DayOfWeek, "saturday" | "sunday">;
type Weekday = Exclude<DayOfWeek, Weekend>;
```

---

## Aliasing Tuples

```typescript
// Tuple type aliases
type Pair = [string, number];
type Triple = [string, number, boolean];
type Point3D = [x: number, y: number, z: number];
type Response = [data: string, status: number, error?: string];

// Labeled tuple aliases
type UserTuple = [name: string, age: number, email: string];
type HTTPResult = [statusCode: number, statusText: string, body?: string];

// Rest elements in tuple aliases
type HeadAndTail = [head: string, ...tail: number[]];
type MixedRest = [string, ...Array<string | number>, boolean];

// Generic tuple aliases
type PairOf<T> = [T, T];
type TripleOf<T> = [T, T, T];
type Result<T> = [error: null, data: T] | [error: Error, data: null];

// Using tuple aliases
function createPair<T>(a: T, b: T): PairOf<T> {
  return [a, b];
}

function safeParse<T>(json: string): Result<T> {
  try {
    return [null, JSON.parse(json)];
  } catch (e) {
    return [e as Error, null];
  }
}

const [err, data] = safeParse<User>('{"name": "Alice"}');
if (!err) {
  console.log(data.name);
}
```

---

## Recursive Type Aliases

TypeScript supports recursive type aliases for representing tree-like structures.

```typescript
// Linked list
type LinkedList<T> = {
  value: T;
  next: LinkedList<T> | null;
};

const list: LinkedList<number> = {
  value: 1,
  next: {
    value: 2,
    next: {
      value: 3,
      next: null,
    },
  },
};

// Binary tree
type BinaryTree<T> = {
  value: T;
  left: BinaryTree<T> | null;
  right: BinaryTree<T> | null;
};

// JSON value (recursive union)
type JSONValue =
  | string
  | number
  | boolean
  | null
  | JSONValue[]
  | { [key: string]: JSONValue };

const data: JSONValue = {
  name: "Alice",
  age: 30,
  hobbies: ["reading", "coding"],
  address: {
    city: "San Francisco",
    zip: "94102",
  },
};

// Nested object type
type NestedObject = {
  [key: string]: string | NestedObject;
};

// Recursive array type (for deeply nested arrays)
type DeepArray<T> = T | DeepArray<T>[];

// Tree with depth limit (to prevent infinite recursion in type checking)
type LimitedTree<T, Depth extends number = 0> = {
  value: T;
  children: Depth extends 5 ? [] : LimitedTree<T, [...any[], 0]>[];
};

// Recursive conditional type
type Flatten<T extends any[]> = T extends [infer Head, ...infer Rest]
  ? Head extends any[]
    ? [...Flatten<Head>, ...Flatten<Rest>]
    : [Head, ...Flatten<Rest>]
  : [];

type Flat = Flatten<[[1, 2], [3, [4, 5]]]>; // [1, 2, 3, 4, 5]
```

---

## Type Alias vs Variable

Type aliases create **type-level** names; variables create **value-level** names.

```typescript
// Type alias (compile-time only)
type StringAlias = string;
// Does NOT exist at runtime

// Variable (runtime value)
const StringVar = String;
// Exists at runtime

// Type alias cannot be used as a value
type MyString = string;
// const x: MyString = "hello"; // OK (type annotation)
// MyString("hello"); // Error: not a value

// Variable cannot be used as a type
const MyType = { name: string };
// const x: MyType = { name: "Alice" }; // Error: not a type
// Use: type MyType = typeof MyType;

// const assertion creates both!
const Status = {
  Active: "active",
  Inactive: "inactive",
} as const;
type Status = (typeof Status)[keyof typeof Status]; // "active" | "inactive"
// Status exists as both a value (the object) and a type (the union)

// Type alias vs interface for variables
type TypeUser = { name: string; age: number };
interface InterfaceUser { name: string; age: number; }

// Both can be used in type positions
const a: TypeUser = { name: "Alice", age: 30 };
const b: InterfaceUser = { name: "Bob", age: 25 };

// Neither can be used as a value
// const c = new TypeUser(); // Error
// const d = new InterfaceUser(); // Error
```

---

## Type Hoisting Behavior

Type aliases are **NOT hoisted** — they must be declared before use.

```typescript
// ❌ Error: 'StringAlias' was used before it was declared
// const x: StringAlias = "hello";
// type StringAlias = string;

// ✅ Correct: declare first, then use
type StringAlias = string;
const x: StringAlias = "hello";

// This differs from function declarations (which are hoisted)
greet(); // OK — function declarations are hoisted
function greet() {
  console.log("hello");
}

// But type aliases are like let/const — they exist in the "temporal dead zone"
// before their declaration

// Forward references work with interfaces (which ARE hoisted)
// const a: InterfaceUser = { name: "Alice", age: 30 }; // Works!
// interface InterfaceUser { name: string; age: number; } // OK

// Recursive type aliases can reference themselves
type Node = {
  value: number;
  children: Node[]; // References itself — OK
};

// Circular type aliases
type A = {
  b: B;
};
type B = {
  a: A;
};
```

---

## Best Practices

1. **Use `type` for unions, intersections, tuples, and mapped types**
2. **Use `type` when you need computed/mapped properties**
3. **Name type aliases descriptively** — they serve as documentation
4. **Use generic type aliases** for reusable type patterns
5. **Use type aliases for complex inline types** to improve readability
6. **Don't use type aliases for simple object shapes** — prefer interfaces
7. **Use `as const` + type alias** for enum-like patterns
8. **Be aware** that type aliases are not hoisted — declare before use
9. **Use recursive type aliases** for tree structures and JSON-like data
10. **Combine type aliases with utility types** for advanced transformations

---

## Interview Questions

### Q1: What is a type alias in TypeScript?

**Answer:** A type alias creates a new name for an existing type using the `type` keyword. It doesn't create a new type — just a new name. Type aliases can represent primitives, objects, unions, tuples, functions, and more.

### Q2: Are type aliases hoisted?

**Answer:** No. Type aliases must be declared before they are used. This differs from interface declarations, which are hoisted.

### Q3: Can you use a type alias as a value?

**Answer:** No. Type aliases exist only at compile time. To create both a value and a type, use `as const` objects with `typeof`:
```typescript
const Status = { Active: "active" } as const;
type Status = (typeof Status)[keyof typeof Status];
```

### Q4: What are recursive type aliases?

**Answer:** Type aliases that reference themselves, used for representing tree-like structures like linked lists, binary trees, and JSON values. TypeScript supports them with constraints to prevent infinite recursion.

### Q5: When would you use a type alias over an interface?

**Answer:** Use type aliases for unions, intersections, tuples, mapped types, conditional types, and computed properties. Use interfaces for object shapes that might be extended or implemented by classes.
