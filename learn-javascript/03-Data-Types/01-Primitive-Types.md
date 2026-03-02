Below is a **deep, interview-focused explanation of Primitive Types only**, covering **definition, memory behavior, edge cases, and interview traps**. This is structured so you can **explain confidently in interviews**.

---

# Primitive Types in JavaScript

## Definition

Primitive types are **basic data types that store actual values directly in memory** and are **immutable**.

JavaScript has **7 primitive types**:

1. `string`
2. `number`
3. `boolean`
4. `undefined`
5. `null`
6. `symbol`
7. `bigint`

---

# 1. String

## Definition

A string represents **textual data**.

```js
let name = "John";
let city = 'London';
let message = `Hello ${name}`;
```

Strings can be defined using:

* Double quotes `" "`
* Single quotes `' '`
* Backticks `` ` ` `` (Template literals)

---

## Template Literals

Backticks allow:

### 1. Variable Interpolation

```js
let name = "John";
let text = `Hello ${name}`;
```

### 2. Multiline Strings

```js
let msg = `Hello
World`;
```

---

## String Immutability

Strings cannot be changed after creation.

```js
let str = "hello";
str[0] = "H";

console.log(str); // "hello"
```

Instead, a **new string is created**:

```js
str = "Hello";
```

---

## String Methods Create New Strings

```js
let text = "hello";

let upper = text.toUpperCase();

console.log(text);  // "hello"
console.log(upper); // "HELLO"
```

---

## Interview Points

* Strings are immutable
* Stored by value
* Indexed

```js
let s = "abc";
console.log(s[1]); // b
```

---

# 2. Number

## Definition

Represents numeric values.

```js
let age = 25;
let price = 99.5;
```

JavaScript uses **one numeric type**:

* 64-bit floating point (IEEE 754)

No separate:

* int
* float
* double

---

## Special Numeric Values

### NaN (Not a Number)

```js
let x = 0 / 0;
console.log(x); // NaN
```

Important behavior:

```js
NaN === NaN // false
```

Correct check:

```js
Number.isNaN(NaN) // true
```

---

### Infinity

```js
console.log(1 / 0); // Infinity
```

---

### Floating Point Precision Problem

```js
0.1 + 0.2
// 0.30000000000000004
```

Interview explanation:

> JavaScript uses binary floating-point representation.

---

## Safe Integers

Maximum safe integer:

```js
Number.MAX_SAFE_INTEGER
```

Value:

```
9007199254740991
```

Beyond this, precision is lost.

---

## typeof Number

```js
typeof 10 // "number"
typeof NaN // "number"
typeof Infinity // "number"
```

---

# 3. Boolean

## Definition

Represents logical values:

```js
true
false
```

Example:

```js
let isAdmin = true;
```

---

## Boolean Conversion

Falsy values:

```
false
0
""
null
undefined
NaN
```

Example:

```js
Boolean(0) // false
Boolean(1) // true
```

---

## Common Interview Example

```js
if ("hello") {
 console.log("runs");
}
```

Because `"hello"` is truthy.

---

# 4. Undefined

## Definition

Represents a variable that **exists but has no assigned value**.

```js
let x;
console.log(x); // undefined
```

---

## When Undefined Occurs

### 1. Uninitialized Variable

```js
let a;
```

---

### 2. Missing Function Argument

```js
function test(x) {
 console.log(x);
}

test(); // undefined
```

---

### 3. Missing Object Property

```js
let obj = {};
console.log(obj.name); // undefined
```

---

### 4. Function Without Return

```js
function test() {}
console.log(test()); // undefined
```

---

## typeof Undefined

```js
typeof undefined
// "undefined"
```

---

# 5. Null

## Definition

Represents **intentional absence of value**.

```js
let user = null;
```

Meaning:

> "Value exists but currently empty."

---

## Null vs Undefined

| null                    | undefined     |
| ----------------------- | ------------- |
| Intentional empty value | Not assigned  |
| Assigned manually       | Default value |

Example:

```js
let x = null;
let y;

console.log(x); // null
console.log(y); // undefined
```

---

## Historical Bug

```js
typeof null
// "object"
```

Reason:

Early JavaScript implementation error.

Still exists for backward compatibility.

---

## Proper Null Check

```js
value === null
```

---

# 6. Symbol

## Definition

Represents a **unique identifier**.

```js
const id = Symbol();
```

Each symbol is unique:

```js
Symbol() === Symbol()
// false
```

---

## Symbol with Description

```js
const id = Symbol("userId");
```

Description is only for debugging.

---

## Symbol as Object Keys

```js
const id = Symbol();

const user = {
 [id]: 123
};
```

Prevents property collisions.

---

## Interview Use Cases

Used in:

* Internal object properties
* Libraries
* Framework internals

---

# 7. BigInt

## Definition

Represents very large integers.

```js
const big = 12345678901234567890n;
```

Notice the **n** at end.

---

## When BigInt Is Needed

When numbers exceed:

```
Number.MAX_SAFE_INTEGER
```

Example:

```js
9007199254740991 + 1 === 9007199254740991 + 2
// true ❌ precision lost
```

BigInt fixes this:

```js
9007199254740991n + 1n
```

---

## BigInt Restrictions

Cannot mix with number:

```js
10n + 5
// Error
```

Must convert:

```js
Number(10n) + 5
```

---

# Memory Representation (Interview-Level Detail)

### Primitive

Stored directly:

```
a → 10
```

### Copy Creates New Value

```js
let a = 10;
let b = a;
```

Memory:

```
a → 10
b → 10
```

Independent copies.

---

# Primitive Type Summary Table

| Type      | Example  | typeof    |
| --------- | -------- | --------- |
| string    | "hello"  | string    |
| number    | 10       | number    |
| boolean   | true     | boolean   |
| undefined | let x;   | undefined |
| null      | null     | object ❌  |
| symbol    | Symbol() | symbol    |
| bigint    | 10n      | bigint    |

---

# Final Interview Summary

> JavaScript has seven primitive types: string, number, boolean, undefined, null, symbol, and bigint. Primitive values are immutable and stored directly in memory. When assigned, primitives create independent copies rather than shared references.

---

Next important topic:

**Reference Types (Object, Array, Function, Map, Set)**

This is the **second half of Data Types** and is equally important.
