# Tuples in TypeScript

## Table of Contents

1. [Overview](#overview)
2. [Tuple Types](#tuple-types)
3. [Readonly Tuples](#readonly-tuples)
4. [Optional Tuple Elements](#optional-tuple-elements)
5. [Rest Elements in Tuples](#rest-elements-in-tuples)
6. [Labeled Tuples](#labeled-tuples)
7. [Tuple Types vs Array Types](#tuple-types-vs-array-types)
8. [Destructuring Tuples](#destructuring-tuples)
9. [Returning Tuples from Functions](#returning-tuples-from-functions)
10. [Tuple Assignability](#tuple-assignability)
11. [Variadic Tuple Types](#variadic-tuple-types)
12. [Best Practices](#best-practices)
13. [Interview Questions](#interview-questions)

---

## Overview

Tuples are **fixed-length arrays** where each element has a **specific type** at a specific index. They combine the benefits of arrays (ordered collections) with the type safety of interfaces (known structure).

```typescript
// Regular array — any number of elements of the same type
const arr: number[] = [1, 2, 3, 4, 5]; // OK

// Tuple — fixed length, specific types at each position
const tuple: [string, number] = ["Alice", 30]; // OK
const bad: [string, number] = [30, "Alice"];   // Error: wrong order
const bad2: [string, number] = ["Alice"];      // Error: missing element
const bad3: [string, number] = ["Alice", 30, true]; // Error: too many
```

---

## Tuple Types

```typescript
// Basic tuple: [type1, type2, ...]
const pair: [string, number] = ["age", 30];
const triple: [boolean, string, number] = [true, "hello", 42];

// Accessing tuple elements (type is known per index)
const name: string = pair[0]; // string
const age: number = pair[1];  // number

// TypeScript knows the exact type at each index
pair[0].toUpperCase(); // OK
pair[1].toFixed(2);    // OK

// Empty tuple
const empty: [] = [];

// Tuple as a type annotation
let coordinates: [number, number, number];
coordinates = [1.0, 2.0, 3.0]; // OK

// Tuples in interfaces
interface ApiResponse {
  data: [string, number, boolean]; // [data, statusCode, success]
}

// Tuples in type aliases
type Point3D = [x: number, y: number, z: number];

// Tuples in arrays
const points: Point3D[] = [
  [1, 2, 3],
  [4, 5, 6],
];

// Heterogeneous tuples
const mixed: [string, number, boolean, null] = ["hello", 42, true, null];

// Tuple with union types at specific positions
const flexible: [string | number, boolean] = [42, true];
```

---

## Readonly Tuples

```typescript
// readonly tuples cannot be modified after creation
const immutable: readonly [string, number] = ["Alice", 30];
// immutable[0] = "Bob";  // Error: read-only property
// immutable.push("test"); // Error: push does not exist

// as const creates the most specific tuple type
const literal = [1, "hello", true] as const;
// Type: readonly [1, "hello", true]

// Converting readonly tuple to mutable
const readonlyTuple: readonly [string, number] = ["Alice", 30];
const mutableTuple: [string, number] = [...readonlyTuple];

// Readonly tuples vs readonly arrays
const readonlyArr: readonly number[] = [1, 2, 3]; // Variable length
const readonlyTuple2: readonly [number, number, number] = [1, 2, 3]; // Fixed
```

---

## Optional Tuple Elements

```typescript
// Optional elements use ? syntax
const userTuple: [string, number, boolean?] = ["Alice", 30];
const userTuple2: [string, number, boolean?] = ["Alice", 30, true];

// Accessing optional elements
const [name, age, isActive] = userTuple;
// name: string, age: number, isActive: boolean | undefined

// Optional elements must be at the end
// const bad: [string?, number, boolean]; // Error

// Multiple optional elements
const config: [string, number?, boolean?, string?] = ["localhost"];

// Optional elements with defaults in destructuring
const [n, a, active = false] = userTuple;

// Optional tuple in type positions
type Result = [data: string, error?: Error];
const success: Result = ["ok"];
const failure: Result = ["fail", new Error("something went wrong")];
```

---

## Rest Elements in Tuples

```typescript
// Rest elements capture remaining elements
const restTuple: [string, ...number[]] = ["Alice", 1, 2, 3, 4, 5];

// Rest element in the middle
const withRest: [boolean, ...string[], number] = [true, "a", "b", "c", 42];

// Rest elements with constraints
function logFirstAndRest<T extends [string, ...unknown[]]>(tuple: T): void {
  const [first, ...rest] = tuple;
  console.log(`First: ${first}, Rest: ${rest}`);
}

logFirstAndRest(["hello", 1, 2, 3]);

// Rest elements in tuple types
type NamedArgs = [name: string, ...args: number[]];
function callWithName(...tuple: NamedArgs): void {
  const [name, ...args] = tuple;
  console.log(`Name: ${name}, Args: ${args}`);
}

callWithName("test", 1, 2, 3);
```

---

## Labeled Tuples

Labels add documentation to tuple positions without changing the type.

```typescript
// Labeled tuple syntax
type UserTuple = [name: string, age: number, email: string];

const user: UserTuple = ["Alice", 30, "alice@example.com"];

// Labels show up in error messages (much more readable!)
// Error: Type 'number' is not assignable to type 'string'.
//   The expected type comes from property 'name' which is declared here.

// Labels in function signatures
function createUser(name: string, age: number, email: string): UserTuple {
  return [name, age, email];
}

// Labels with optional elements
type HttpResult = [
  statusCode: number,
  statusText: string,
  body?: string,
];

const ok: HttpResult = [200, "OK", '{"data": true}'];
const notFound: HttpResult = [404, "Not Found"];

// Labels with rest elements
type EventTuple = [
  eventName: string,
  ...args: (string | number | boolean)[]
];

const clickEvent: EventTuple = ["click", "button", 100, true];
const hoverEvent: EventTuple = ["hover", "div"];

// Labels in destructuring
function processHttpResult([code, text, body]: HttpResult): string {
  return `${code} ${text}: ${body ?? "no body"}`;
}
```

---

## Tuple Types vs Array Types

| Feature | Tuple | Array |
|---------|-------|-------|
| Length | Fixed | Variable |
| Element types | Specific per index | All same type |
| Access | Type known per index | Union of all types |
| Assignment | Must match exactly | Any compatible array |
| Use case | Fixed structure | Variable-length data |

```typescript
// Array: all elements same type, variable length
const arr: number[] = [1, 2, 3, 4, 5]; // OK
const arr2: number[] = [1];             // Also OK
const arr3: number[] = [];              // Also OK

// Tuple: fixed length, specific types per position
const tuple: [string, number] = ["Alice", 30];
// const tuple2: [string, number] = ["Alice"]; // Error: too short

// Array access returns union of all element types (if any)
const arrEl: number = arr[0]; // number

// Tuple access returns specific type per index
const tupleEl0: string = tuple[0]; // string
const tupleEl1: number = tuple[1]; // number

// Array .length is number
console.log(arr.length); // number

// Tuple .length is a literal type!
console.log(tuple.length); // 2 (literal type, not number)
```

---

## Destructuring Tuples

```typescript
// Basic destructuring
const pair: [string, number] = ["Alice", 30];
const [name, age] = pair;

// Skipping elements
const triple: [string, number, boolean] = ["Alice", 30, true];
const [first, , third] = triple; // third = true

// Rest elements
const [head, ...tail]: [string, ...number[]] = ["Alice", 1, 2, 3];
// head: "Alice", tail: [1, 2, 3]

// Default values
const optional: [string, number, boolean?] = ["Alice", 30];
const [n, a, active = false] = optional; // active: false

// Nested destructuring
const nested: [[string, number], boolean] = [["Alice", 30], true];
const [[userName, userAge], isAdmin] = nested;

// In function parameters
function process([name, age, active = false]: [string, number, boolean?]): string {
  return `${name} (${age}) - ${active ? "active" : "inactive"}`;
}

process(["Alice", 30]);     // "Alice (30) - inactive"
process(["Bob", 25, true]); // "Bob (25) - active"
```

---

## Returning Tuples from Functions

```typescript
// Functions can return tuples for multiple return values
function useState<T>(initial: T): [T, (value: T) => void] {
  let state = initial;
  const setState = (value: T) => { state = value; };
  return [state, setState];
}

const [count, setCount] = useState(0);
// count: number, setState: (value: number) => void
setCount(5);

// Generic tuple return
function swap<T, U>(pair: [T, U]): [U, T] {
  return [pair[1], pair[0]];
}

const swapped = swap(["hello", 42]); // [42, "hello"]

// Tuple with error handling
function parseJSON<T>(json: string): [T, null] | [null, Error] {
  try {
    return [JSON.parse(json), null];
  } catch (e) {
    return [null, e as Error];
  }
}

const [data, error] = parseJSON<{ name: string }>('{"name": "Alice"}');
if (data) {
  console.log(data.name); // "Alice"
} else {
  console.error(error!.message);
}

// React-style hooks pattern
function useReducer<S, A>(
  reducer: (state: S, action: A) => S,
  initial: S
): [S, (action: A) => void] {
  let state = initial;
  const dispatch = (action: A) => { state = reducer(state, action); };
  return [state, dispatch];
}
```

---

## Tuple Assignability

```typescript
// Tuples are assignable to arrays
const tuple: [string, number] = ["Alice", 30];
const arr: (string | number)[] = tuple; // OK — tuple is assignable to array

// But arrays are NOT assignable to tuples
const arr2: string[] = ["a", "b", "c"];
// const tuple2: [string, string, string] = arr2; // Error!

// Tuples with fewer elements can be assigned to longer tuples with optional elements
const short: [string] = ["hello"];
const long: [string, number?] = short; // OK

// Excess property checking for tuples
const pair: [string, number] = ["Alice", 30];
// TypeScript checks exact length for literal tuple assignments
const literal: [string, number] = ["Alice", 30]; // OK

// Tuple to union conversion
type TupleToUnion<T extends any[]> = T[number];
type Result = TupleToUnion<[string, number, boolean]>; // string | number | boolean

// Array to tuple (with as const or explicit typing)
const arr3 = [1, "hello", true] as const; // readonly [1, "hello", true]
const tuple3: [number, string, boolean] = [...arr3]; // Spread works
```

---

## Variadic Tuple Types

TypeScript 4.0+ introduced variadic tuple types — tuples that can spread and concat.

```typescript
// Basic variadic tuple type
type Concat<A extends any[], B extends any[]> = [...A, ...B];

type AB = Concat<[1, 2], [3, 4]>; // [1, 2, 3, 4]

// Reverse a tuple
type Reverse<T extends any[]> = T extends [infer Head, ...infer Tail]
  ? [...Reverse<Tail>, Head]
  : [];

type Reversed = Reverse<[1, 2, 3]>; // [3, 2, 1]

// Flatten nested tuples
type Flatten<T extends any[]> = T extends [infer Head, ...infer Tail]
  ? Head extends any[]
    ? [...Flatten<Head>, ...Flatten<Tail>]
    : [Head, ...Flatten<Tail>]
  : [];

type Flat = Flatten<[[1, 2], [3, [4, 5]]]>; // [1, 2, 3, 4, 5]

// Length of a tuple
type Length<T extends any[]> = T["length"];
type L = Length<[1, 2, 3]>; // 3

// First element
type Head<T extends any[]> = T extends [infer First, ...any[]] ? First : never;
type H = Head<[1, 2, 3]>; // 1

// Last element
type Last<T extends any[]> = T extends [...any[], infer Tail] ? Tail : never;
type L2 = Last<[1, 2, 3]>; // 3

// Prepend
type Prepend<E, T extends any[]> = [E, ...T];
type P = Prepend<0, [1, 2, 3]>; // [0, 1, 2, 3]

// Real-world: typed function composition
type ComposeArgs<Fns extends ((...args: any[]) => any)[]> =
  Fns extends [(...args: infer A) => any, ...infer Rest]
    ? Rest extends [(arg: any) => any, ...any[]]
      ? ComposeArgs<Rest> extends [...any[]]
        ? A
        : never
      : A
    : never;

// Variadic tuples with generics
function concat<A extends any[], B extends any[]>(a: A, b: B): [...A, ...B] {
  return [...a, ...b];
}

const result = concat([1, 2], ["a", "b"]); // [1, 2, "a", "b"]

// Mapped types over tuples
type MapTuple<T extends any[], F extends (arg: any) => any> =
  T extends [infer Head, ...infer Rest]
    ? [F extends (arg: Head) => infer R ? R : never, ...MapTuple<Rest, F>]
    : [];

type Doubled = MapTuple<[1, 2, 3], (n: number) => number>; // [number, number, number]
```

---

## Best Practices

1. **Use tuples for fixed-structure data** where position has meaning (key-value pairs, coordinate data)
2. **Prefer objects over tuples** when the structure has many fields — tuples become unreadable with 4+ elements
3. **Use labeled tuples** for better error messages and documentation
4. **Use `as const`** for tuple literals to get the most specific types
5. **Return tuples from functions** that need multiple return values (like `useState`)
6. **Use readonly tuples** for data that should not be modified
7. **Use variadic tuples** for advanced generic types and type-level programming

---

## Interview Questions

### Q1: What is the difference between a tuple and an array in TypeScript?

**Answer:** A tuple has a fixed length with specific types at each position. An array has a variable length with all elements of the same type. Tuple access returns the exact type at that index, while array access returns the union of all element types.

### Q2: How do you create a readonly tuple?

**Answer:** Use `readonly` keyword or `as const`:
```typescript
const a: readonly [string, number] = ["Alice", 30];
const b = ["hello", 42] as const; // readonly ["hello", 42]
```

### Q3: What are labeled tuples?

**Answer:** Tuples with named labels for each position. They don't change the type but improve error messages and documentation: `[name: string, age: number]`.

### Q4: Can you spread a tuple in a function call?

**Answer:** Yes, using rest parameters and variadic tuple types:
```typescript
function log(...args: [string, number, boolean]) { /* ... */ }
const tuple: [string, number, boolean] = ["test", 1, true];
log(...tuple); // OK
```

### Q5: What are variadic tuple types?

**Answer:** A TypeScript 4.0+ feature that allows tuple types to use rest elements and spread other tuple types, enabling powerful type-level manipulation like concatenation, reversal, and mapping over tuples.
