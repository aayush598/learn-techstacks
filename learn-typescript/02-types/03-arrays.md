# Arrays in TypeScript

## Table of Contents

1. [Overview](#overview)
2. [Array<T> vs T[] Syntax](#arrayt-vs-t-syntax)
3. [Readonly Arrays](#readonly-arrays)
4. [Typed Arrays](#typed-arrays)
5. [Array Methods with Types](#array-methods-with-types)
6. [Type Narrowing in Callbacks](#type-narrowing-in-callbacks)
7. [flat and flatMap](#flat-and-flatmap)
8. [Array Destructuring with Types](#array-destructuring-with-types)
9. [Multi-dimensional Arrays](#multi-dimensional-arrays)
10. [Best Practices](#best-practices)
11. [Interview Questions](#interview-questions)

---

## Overview

Arrays in TypeScript are collections of elements of the same type. TypeScript supports two equivalent syntaxes for typed arrays, readonly variants, and type-safe array operations.

---

## Array\<T\> vs T[] Syntax

Both syntaxes are identical in behavior — use whichever you prefer (T[] is more common).

```typescript
// Generic syntax: Array<T>
const numbers: Array<number> = [1, 2, 3];
const names: Array<string> = ["Alice", "Bob"];
const mixed: Array<string | number> = [1, "two", 3];

// Shorthand syntax: T[]
const numbers2: number[] = [1, 2, 3];
const names2: string[] = ["Alice", "Bob"];
const mixed2: (string | number)[] = [1, "two", 3];

// Nested arrays
const matrix: number[][] = [
  [1, 2, 3],
  [4, 5, 6],
  [7, 8, 9],
];
// Equivalent to: Array<Array<number>>

const matrixGeneric: Array<Array<number>> = [
  [1, 2, 3],
  [4, 5, 6],
];

// Empty arrays (must annotate when empty)
const empty: string[] = [];
const emptyGeneric: Array<string> = [];

// Array of objects
interface User {
  name: string;
  age: number;
}

const users: User[] = [
  { name: "Alice", age: 30 },
  { name: "Bob", age: 25 },
];

const usersGeneric: Array<User> = [
  { name: "Alice", age: 30 },
  { name: "Bob", age: 25 },
];

// Array of functions
const callbacks: Array<(x: number) => number> = [
  (x) => x * 2,
  (x) => x + 1,
  (x) => x ** 2,
];

// Array of arrays of strings
const grid: string[][] = [
  ["a", "b", "c"],
  ["d", "e", "f"],
];

// Type inference in arrays
const inferred = [1, 2, 3]; // number[]
const mixedInferred = [1, "two"]; // (string | number)[]
```

**Recommendation:** Most TypeScript codebases use `T[]` syntax for simple types and `Array<T>` for complex generics. Both are valid.

```typescript
// ✅ Common convention
const ids: number[] = [1, 2, 3];
const items: User[] = [];
const matrix: number[][] = [];

// Also fine
const ids2: Array<number> = [1, 2, 3];
```

---

## Readonly Arrays

Readonly arrays prevent modification after creation.

```typescript
// readonly keyword
const frozen: readonly number[] = [1, 2, 3];
// frozen.push(4);     // Error: Property 'push' does not exist
// frozen[0] = 10;     // Error: Index signature in type 'readonly number[]'
// frozen.length = 0;  // Error

// ReadonlyArray<T> type
const immutable: ReadonlyArray<string> = ["a", "b", "c"];
// Same restrictions as readonly number[]

// Read-only with objects
interface ReadonlyUser {
  readonly name: string;
  readonly age: number;
}

const readonlyUsers: readonly ReadonlyUser[] = [
  { name: "Alice", age: 30 },
];
// readonlyUsers.push(...); // Error
// readonlyUsers[0].name = "Bob"; // Error (because ReadonlyUser has readonly name)

// as const for truly frozen arrays
const constantArray = [1, 2, 3] as const;
// Type: readonly [1, 2, 3] (tuple, not array!)
// This is more restrictive than readonly number[]

// readonly vs ReadonlyArray
const a: readonly number[] = [1, 2, 3];
const b: ReadonlyArray<number> = [1, 2, 3];
// These are equivalent

// Converting mutable to readonly
const mutable = [1, 2, 3];
const readonlyVersion: readonly number[] = mutable; // OK
const readonlyVersion2: ReadonlyArray<number> = mutable; // OK

// Converting readonly to mutable (requires explicit cast)
const readonlyArr: readonly number[] = [1, 2, 3];
const mutableArr: number[] = [...readonlyArr]; // Spread creates new mutable array
const mutableArr2: number[] = readonlyArr as number[]; // Unsafe assertion

// Readonly in type positions
type ImmutableConfig = {
  readonly settings: readonly string[];
};

const config: ImmutableConfig = {
  settings: ["a", "b", "c"],
};
// config.settings.push("d"); // Error
// config.settings = ["x"];    // Error (readonly property)

// Methods available on readonly arrays (non-mutating only)
const nums: readonly number[] = [1, 2, 3, 4, 5];

nums.map((n) => n * 2);     // OK — returns new array
nums.filter((n) => n > 2);   // OK — returns new array
nums.reduce((acc, n) => acc + n, 0); // OK
nums.find((n) => n > 3);     // OK
nums.includes(3);             // OK
nums.indexOf(3);              // OK
nums.slice(1, 3);             // OK

// These are NOT available on readonly arrays:
// nums.push(6);     // Error
// nums.pop();        // Error
// nums.splice(0, 1); // Error
// nums.sort();       // Error
// nums.reverse();    // Error
// nums.fill(0);      // Error
```

---

## Typed Arrays

TypeScript has built-in types for binary data (JavaScript TypedArrays).

```typescript
// Signed integers
const int8: Int8Array = new Int8Array([1, -2, 3]);
const int16: Int16Array = new Int16Array([1000, -2000]);
const int32: Int32Array = new Int32Array([100000, -200000]);

// Unsigned integers
const uint8: Uint8Array = new Uint8Array([0, 128, 255]);
const uint8clamped: Uint8ClampedArray = new Uint8ClampedArray([0, 256, -10]);
const uint16: Uint16Array = new Uint16Array([0, 65535]);
const uint32: Uint32Array = new Uint32Array([0, 4294967295]);

// Floating point
const float32: Float32Array = new Float32Array([1.5, 2.7, 3.14]);
const float64: Float64Array = new Float64Array([1.5, 2.7, 3.14]);

// BigInt typed arrays
const bigInt64: BigInt64Array = new BigInt64Array([1n, -2n, 3n]);
const bigUint64: BigUint64Array = new BigUint64Array([0n, 18446744073709551615n]);

// Common typed array operations
const buffer = new ArrayBuffer(16); // 16 bytes
const view = new DataView(buffer);
const int32View = new Int32Array(buffer);

int32View[0] = 42;
int32View[1] = 100;
console.log(int32View.length); // 4 (16 bytes / 4 bytes per int32)

// Typed arrays in function signatures
function processBytes(data: Uint8Array): number {
  let sum = 0;
  for (const byte of data) {
    sum += byte;
  }
  return sum;
}

// Creating typed arrays from other iterables
const fromArray = new Uint8Array([1, 2, 3, 4]);
const fromTyped = new Uint16Array(new Uint8Array([1, 2, 3, 4]));
const fromBuffer = new Float32Array(new ArrayBuffer(8), 0, 2);

// Typed arrays are NOT regular arrays
function handleData(data: Uint8Array | number[]): void {
  // Can't use regular array methods directly on typed arrays without checking
  if (Array.isArray(data)) {
    data.map((n) => n * 2); // Regular array — OK
  } else {
    data.map((n) => n * 2); // TypedArray also has map — OK
    // But push/pop/splice are not available on typed arrays
  }
}

// Blob and File API usage
async function readFile(file: File): Promise<Uint8Array> {
  return new Uint8Array(await file.arrayBuffer());
}
```

---

## Array Methods with Types

TypeScript provides full type information for all array methods.

### map

```typescript
const numbers: number[] = [1, 2, 3, 4, 5];

// Return type is inferred from callback
const doubled: number[] = numbers.map((n) => n * 2);
// Callback: (n: number) => number
// Return type: number[]

const strings: string[] = numbers.map((n) => n.toString());
// Callback: (n: number) => string
// Return type: string[]

// Explicit return type
const formatted: string[] = numbers.map((n): string => `$${n.toFixed(2)}`);

// Map with index
const indexed: string[] = numbers.map((n, i) => `${i}: ${n}`);

// Map with complex transformations
interface User {
  name: string;
  age: number;
}

const users: User[] = [
  { name: "Alice", age: 30 },
  { name: "Bob", age: 25 },
];

const names: string[] = users.map((u) => u.name);
const greetings: string[] = users.map((u) => `Hello, ${u.name}!`);
```

### filter

```typescript
const numbers: number[] = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];

// Basic filter (type predicate not needed for simple cases)
const evens: number[] = numbers.filter((n) => n % 2 === 0);

// Type predicate (is keyword) for complex filtering
interface Animal {
  type: "dog" | "cat" | "bird";
  name: string;
}

const animals: Animal[] = [
  { type: "dog", name: "Rex" },
  { type: "cat", name: "Whiskers" },
  { type: "bird", name: "Tweety" },
  { type: "dog", name: "Buddy" },
];

function isDog(animal: Animal): animal is Animal & { type: "dog" } {
  return animal.type === "dog";
}

const dogs: (Animal & { type: "dog" })[] = animals.filter(isDog);
// dogs: [{ type: "dog", name: "Rex" }, { type: "dog", name: "Buddy" }]

// Without type predicate, the type would be Animal[] (not narrowed)
const dogsUnsafe = animals.filter((a) => a.type === "dog"); // Animal[]

// Filter with union types
const mixed: (string | number | boolean)[] = [1, "hello", true, 42, "world"];
const stringsOnly: string[] = mixed.filter((x): x is string => typeof x === "string");
```

### reduce

```typescript
const numbers: number[] = [1, 2, 3, 4, 5];

// With initial value (type of accumulator is inferred from initial value)
const sum: number = numbers.reduce((acc, n) => acc + n, 0);

// Without initial value (accumulator type is first element type)
const sum2: number = numbers.reduce((acc, n) => acc + n);

// Complex reduction
interface Vote {
  candidate: string;
  count: number;
}

const votes: Vote[] = [
  { candidate: "Alice", count: 10 },
  { candidate: "Bob", count: 15 },
  { candidate: "Alice", count: 5 },
  { candidate: "Charlie", count: 8 },
  { candidate: "Bob", count: 3 },
];

// Group by candidate
const grouped: Record<string, number> = votes.reduce((acc, vote) => {
  acc[vote.candidate] = (acc[vote.candidate] || 0) + vote.count;
  return acc;
}, {} as Record<string, number>);

// Result: { Alice: 15, Bob: 18, Charlie: 8 }

// Building an object from an array
const nameToAge: Record<string, number> = users.reduce((acc, user) => {
  acc[user.name] = user.age;
  return acc;
}, {});
```

### find and findIndex

```typescript
const users: User[] = [
  { name: "Alice", age: 30 },
  { name: "Bob", age: 25 },
  { name: "Charlie", age: 35 },
];

// find returns T | undefined
const bob: User | undefined = users.find((u) => u.name === "Bob");

if (bob) {
  console.log(bob.age); // 25 — narrowed to User
}

// findIndex returns number (-1 if not found)
const charlieIndex: number = users.findIndex((u) => u.name === "Charlie");

// findLast and findLastIndex (ES2023)
const lastUnder30: User | undefined = users.findLast((u) => u.age < 30);
const lastUnder30Index: number = users.findLastIndex((u) => u.age < 30);
```

### some and every

```typescript
const numbers: number[] = [2, 4, 6, 8, 10];

// some returns boolean
const hasEven: boolean = numbers.some((n) => n % 2 === 0); // true
const hasNegative: boolean = numbers.some((n) => n < 0);    // false

// every returns boolean
const allEven: boolean = numbers.every((n) => n % 2 === 0); // true
const allPositive: boolean = numbers.every((n) => n > 0);    // true

// Type narrowing with some
const mixed: (string | number)[] = [1, "hello", 2, "world"];
const hasString: boolean = mixed.some((x) => typeof x === "string"); // true
// Note: some doesn't narrow the array type — it only returns boolean
```

### sort

```typescript
const numbers: number[] = [3, 1, 4, 1, 5, 9, 2, 6];

// sort mutates the original array!
const sorted = numbers.sort((a, b) => a - b); // [1, 1, 2, 3, 4, 5, 6, 9]
console.log(numbers); // Also sorted! (mutated)

// To avoid mutation:
const original: number[] = [3, 1, 4, 1, 5, 9, 2, 6];
const sortedCopy: number[] = [...original].sort((a, b) => a - b);
console.log(original); // Unchanged

// toSorted (ES2023) — returns new array, doesn't mutate
const sorted2: number[] = numbers.toSorted((a, b) => a - b);

// Generic sort comparator
function sortBy<T, K extends keyof T>(array: T[], key: K, order: "asc" | "desc" = "asc"): T[] {
  return [...array].sort((a, b) => {
    const aVal = a[key];
    const bVal = b[key];
    if (aVal < bVal) return order === "asc" ? -1 : 1;
    if (aVal > bVal) return order === "asc" ? 1 : -1;
    return 0;
  });
}

const sortedUsers = sortBy(users, "age", "desc");
```

---

## Type Narrowing in Callbacks

TypeScript provides special support for type narrowing within array method callbacks.

```typescript
// Type predicate with filter (is keyword)
function isString(value: unknown): value is string {
  return typeof value === "string";
}

const mixed: (string | number | boolean)[] = [1, "hello", true, "world"];
const strings: string[] = mixed.filter(isString); // ["hello", "world"]

// Assertion function for filtering
function assertNumber(value: unknown): asserts value is number {
  if (typeof value !== "number") {
    throw new Error("Expected number");
  }
}

// Custom type guard in filter
interface Success {
  status: "success";
  data: string;
}

interface Error {
  status: "error";
  message: string;
}

type Response = Success | Error;

const responses: Response[] = [
  { status: "success", data: "ok" },
  { status: "error", message: "fail" },
  { status: "success", data: "done" },
];

function isSuccess(response: Response): response is Success {
  return response.status === "success";
}

const successResponses: Success[] = responses.filter(isSuccess);
// [{ status: "success", data: "ok" }, { status: "success", data: "done" }]

// The "never" trick for exhaustive checking in callbacks
function processItem(item: "a" | "b" | "c"): string {
  const handlers: Record<string, (x: string) => string> = {
    a: (x) => x.toUpperCase(),
    b: (x) => x.toLowerCase(),
    c: (x) => x.trim(),
  };
  return handlers[item](item);
}
```

---

## flat and flatMap

```typescript
// flat — flattens nested arrays
const nested: number[][] = [[1, 2], [3, 4], [5, 6]];
const flattened: number[] = nested.flat(); // [1, 2, 3, 4, 5, 6]

// flat with depth
const deepNested: number[][][] = [[[1, 2]], [[3, 4]], [[5, 6]]];
const flat1: (number | number[])[] = deepNested.flat(1); // [[1,2], [3,4], [5,6]]
const flat2: number[] = deepNested.flat(2); // [1, 2, 3, 4, 5, 6]
const flatAll: number[] = deepNested.flat(Infinity); // [1, 2, 3, 4, 5, 6]

// flatMap — map + flat(1) in one step
const sentences: string[] = ["hello world", "foo bar baz"];
const words: string[] = sentences.flatMap((s) => s.split(" "));
// ["hello", "world", "foo", "bar", "baz"]

// flatMap for conditional mapping
const numbers: number[] = [1, 2, 3, 4, 5, 6];
const evensOnly: number[] = numbers.flatMap((n) => (n % 2 === 0 ? [n] : []));
// [2, 4, 6]

// flatMap for one-to-many transformation
interface Department {
  name: string;
  employees: string[];
}

const departments: Department[] = [
  { name: "Engineering", employees: ["Alice", "Bob"] },
  { name: "Marketing", employees: ["Charlie"] },
  { name: "Sales", employees: ["Dave", "Eve", "Frank"] },
];

const allEmployees: string[] = departments.flatMap((d) => d.employees);
// ["Alice", "Bob", "Charlie", "Dave", "Eve", "Frank"]

// flatMap with type narrowing
const mixed: (string | number[])[] = ["hello", [1, 2], "world", [3]];
const flattened2: (string | number)[] = mixed.flatMap((x) =>
  typeof x === "string" ? [x] : x
);
// ["hello", 1, 2, "world", 3]
```

---

## Array Destructuring with Types

```typescript
// Basic destructuring with type annotation
const numbers: number[] = [1, 2, 3, 4, 5];
const [first, second, ...rest]: number[] = numbers;
// first: number, second: number, rest: number[]

// Destructuring in function parameters
function processHead([head, ...tail]: number[]): string {
  return `Head: ${head}, Tail: ${tail.join(", ")}`;
}

processHead([1, 2, 3, 4]); // "Head: 1, Tail: 2, 3, 4"

// Destructuring with defaults
const [a = 0, b = 0, c = 0]: number[] = [1, 2];
// a: 1, b: 2, c: 0

// Destructuring with type assertions
const [x, y] = [1, 2] as const;
// x: 1, y: 2 (literal types!)

// Destructuring in loops
const pairs: [string, number][] = [["a", 1], ["b", 2]];
for (const [letter, num] of pairs) {
  console.log(`${letter}: ${num}`);
}

// Destructuring typed arrays
function getCoordinates(): [number, number, number] {
  return [1.0, 2.0, 3.0];
}

const [lat, lng, alt] = getCoordinates();

// Skipping elements
const [first2, , third]: number[] = [1, 2, 3];
// first2: 1, third: 3
```

---

## Multi-dimensional Arrays

```typescript
// 2D array (matrix)
const matrix: number[][] = [
  [1, 2, 3],
  [4, 5, 6],
  [7, 8, 9],
];

// Accessing elements
const element: number = matrix[1][2]; // 6

// 3D array
const cube: number[][][] = [
  [[1, 2], [3, 4]],
  [[5, 6], [7, 8]],
];

// Matrix operations
function multiplyMatrices(a: number[][], b: number[][]): number[][] {
  const result: number[][] = [];
  for (let i = 0; i < a.length; i++) {
    result[i] = [];
    for (let j = 0; j < b[0].length; j++) {
      let sum = 0;
      for (let k = 0; k < b.length; k++) {
        sum += a[i][k] * b[k][j];
      }
      result[i][j] = sum;
    }
  }
  return result;
}

// Typed multi-dimensional arrays
const typedMatrix = new Int32Array(3 * 3); // 3x3 matrix as flat typed array
typedMatrix[0 * 3 + 1] = 5; // Access row 0, col 1
```

---

## Best Practices

1. **Prefer `T[]` syntax** for simple types; use `Array<T>` for complex generic types
2. **Use `readonly` arrays** when the array should not be modified
3. **Use `as const`** for arrays that should be treated as tuples with literal types
4. **Use type predicates** (`is` keyword) with `filter` to narrow array element types
5. **Use `flatMap`** instead of `map().flat()` for better performance and readability
6. **Prefer `[...spread]`** over `slice()` for creating shallow copies
7. **Use `Array.isArray()`** to narrow union types containing arrays
8. **Annotate empty arrays** since TypeScript can't infer the element type
9. **Use typed arrays** (`Uint8Array`, etc.) for binary data operations
10. **Avoid mutating arrays** — prefer pure functions (`map`, `filter`, `reduce`)

---

## Interview Questions

### Q1: What is the difference between `Array<T>` and `T[]`?

**Answer:** They are completely equivalent. `T[]` is syntactic sugar for `Array<T>`. Most codebases prefer `T[]` for its brevity.

### Q2: How do you make an array readonly in TypeScript?

**Answer:** Three ways:
```typescript
const a: readonly number[] = [1, 2, 3];
const b: ReadonlyArray<number> = [1, 2, 3];
const c = [1, 2, 3] as const; // readonly [1, 2, 3] (tuple)
```
The `readonly` modifier prevents mutation methods (`push`, `pop`, `splice`, etc.) from being called.

### Q3: How does `filter` narrow array types?

**Answer:** By default, `filter` doesn't narrow element types. Use a type predicate function with the `is` keyword:
```typescript
function isString(x: unknown): x is string {
  return typeof x === "string";
}
const strings = mixed.filter(isString); // string[]
```

### Q4: What is the difference between `flat()` and `flatMap()`?

**Answer:** `flat(depth)` flattens nested arrays by the specified depth. `flatMap(fn)` is equivalent to `map(fn).flat(1)` — it maps each element to an array and then flattens one level. `flatMap` is more efficient since it doesn't create an intermediate array.

### Q5: When would you use a typed array like `Uint8Array`?

**Answer:** Typed arrays are used for working with binary data: file I/O, network protocols, image processing, WebGL, cryptography, and `ArrayBuffer` operations. They provide fixed-size, typed storage with better performance for numeric computations.
