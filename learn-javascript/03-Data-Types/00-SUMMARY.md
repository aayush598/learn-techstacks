Below is a **deep, interview-grade explanation** of **JavaScript Data Types**, structured so you can **explain clearly, handle edge cases, and answer follow-ups**. This topic is **guaranteed** in interviews.

---

# 3. Data Types in JavaScript

---

## 3.1 Classification of Data Types

JavaScript data types are broadly divided into:

1. **Primitive (Value Types)**
2. **Reference (Non-Primitive Types)**

---

# 3.2 Primitive Types

Primitive types store **actual values directly** in memory and are **immutable**.

---

## 1️⃣ `string`

### Definition

Represents textual data enclosed in quotes.

```js
let name = "John";
let city = 'Delhi';
let msg = `Hello ${name}`;
```

### Key Points

* Immutable
* Indexed
* Template literals support interpolation

```js
name[0] = "A"; // ❌ no effect
```

---

## 2️⃣ `number`

### Definition

Represents both integers and floating-point numbers.

```js
let age = 25;
let price = 99.99;
```

### Special Values

* `NaN`
* `Infinity`
* `-Infinity`

```js
typeof NaN; // "number"
```

### Interview Trap

```js
0.1 + 0.2 !== 0.3 // true (floating-point precision issue)
```

---

## 3️⃣ `boolean`

### Definition

Logical values: `true` or `false`.

```js
let isLoggedIn = true;
```

### Truthy / Falsy

Falsy values:

* `false`
* `0`
* `""`
* `null`
* `undefined`
* `NaN`

---

## 4️⃣ `undefined`

### Definition

A variable declared but **not assigned a value**.

```js
let x;
console.log(x); // undefined
```

### Interview Note

* Default value for uninitialized variables
* Returned when accessing non-existing object properties

---

## 5️⃣ `null`

### Definition

Represents **intentional absence of value**.

```js
let data = null;
```

### Interview Trap

```js
typeof null; // "object" ❌
```

This is a **historical bug** in JavaScript.

---

## 6️⃣ `symbol` (ES6)

### Definition

Creates **unique and immutable identifiers**.

```js
const id = Symbol("id");
```

### Use Case

* Prevent property name collisions
* Internal object properties

```js
const obj = {
  [id]: 123
};
```

---

## 7️⃣ `bigint` (ES2020)

### Definition

Handles integers larger than `Number.MAX_SAFE_INTEGER`.

```js
const big = 123456789012345678901234567890n;
```

### Interview Note

* Cannot mix with `number` directly
* Ends with `n`

---

# 3.3 Reference (Non-Primitive) Types

Reference types store **memory addresses**, not actual values.

---

## 1️⃣ Object

### Definition

Key-value pair collection.

```js
const user = {
  name: "Alice",
  age: 30
};
```

### Characteristics

* Mutable
* Stored by reference
* Can hold any type of value

---

## 2️⃣ Array

### Definition

Ordered list of values.

```js
const arr = [1, 2, 3];
```

### Characteristics

* Zero-indexed
* Dynamic size
* Mutable

---

## 3️⃣ Function

### Definition

Callable object.

```js
function greet() {}
```

### Interview Insight

> Functions are **first-class objects** in JavaScript.

They can be:

* Passed as arguments
* Returned from functions
* Assigned to variables

---

## 4️⃣ Date

### Definition

Represents date and time.

```js
const now = new Date();
```

### Interview Note

* Internally stores timestamp (milliseconds)
* Mutable

---

## 5️⃣ Map

### Definition

Key-value collection with **any type of key**.

```js
const map = new Map();
map.set("a", 1);
```

### Advantages Over Object

* Preserves insertion order
* Better performance for frequent additions/removals

---

## 6️⃣ Set

### Definition

Stores **unique values only**.

```js
const set = new Set([1, 2, 2, 3]);
```

Result: `{1, 2, 3}`

---

# 3.4 Primitive vs Non-Primitive Types

| Feature    | Primitive      | Non-Primitive |
| ---------- | -------------- | ------------- |
| Stored as  | Value          | Reference     |
| Mutability | Immutable      | Mutable       |
| Size       | Fixed          | Dynamic       |
| Comparison | By value       | By reference  |
| Examples   | string, number | object, array |

---

## 3.5 Pass by Value vs Pass by Reference

### Pass by Value (Primitives)

```js
let a = 10;
let b = a;
b = 20;

console.log(a); // 10
```

A copy of value is passed.

---

### Pass by Reference (Objects)

```js
let obj1 = { x: 10 };
let obj2 = obj1;
obj2.x = 20;

console.log(obj1.x); // 20
```

Both point to the same memory location.

---

### Interview Clarification

> JavaScript is technically **pass-by-value**, but for objects, the value is a reference.

---

## 3.6 `typeof` Quirks

| Expression          | Result      |
| ------------------- | ----------- |
| typeof 10           | "number"    |
| typeof "hi"         | "string"    |
| typeof undefined    | "undefined" |
| typeof null         | "object" ❌  |
| typeof []           | "object"    |
| typeof function(){} | "function"  |

### Correct Null Check

```js
value === null
```

---

## 3.7 Mutability vs Immutability

### Immutable (Primitives)

```js
let str = "abc";
str[0] = "x";
console.log(str); // "abc"
```

---

### Mutable (Objects)

```js
const obj = { a: 1 };
obj.a = 2;
```

---

### Why Immutability Matters

* Predictable state
* Better debugging
* Essential for React & Redux

---

## Final Interview Summary (Memorize This)

> Primitive types are immutable and stored by value, while reference types are mutable and stored by reference. JavaScript compares primitives by value and objects by reference, which leads to common pitfalls such as `typeof null` returning `"object"` and unexpected mutations.

---

Next recommended topic:
➡ **Type Conversion & Coercion**
➡ **Execution Context & Call Stack**
➡ **Hoisting (Deep Dive)**

Tell me which one to continue with.
