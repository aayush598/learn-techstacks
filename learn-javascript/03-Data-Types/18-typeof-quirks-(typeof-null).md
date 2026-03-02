# `typeof` Quirks in JavaScript (Especially `typeof null`)

The `typeof` operator returns a **string representing the type of a value**.

```js
typeof value
```

Example:

```js
typeof 10
```

Output:

```
"number"
```

However, `typeof` has several **quirks and inconsistencies** that are commonly asked in interviews.

---

# 1. The Famous Quirk: `typeof null`

```js
typeof null
```

Output:

```
"object"
```

This is **incorrect logically**, because:

> `null` is a primitive type, not an object.

---

## Why Does This Happen?

This is a **historical bug in JavaScript**.

In early JavaScript implementations:

* Values were stored with type tags
* Objects had type tag `0`
* `null` was represented as `0`

So JavaScript mistakenly identified `null` as an object.

This behavior remains for **backward compatibility**.

---

## Correct Interview Explanation

> typeof null returns "object" because of a historical bug in JavaScript, even though null is actually a primitive type.

---

# 2. Complete typeof Results Table

| Value          | typeof Result |
| -------------- | ------------- |
| `"hello"`      | `"string"`    |
| `10`           | `"number"`    |
| `true`         | `"boolean"`   |
| `undefined`    | `"undefined"` |
| `Symbol()`     | `"symbol"`    |
| `10n`          | `"bigint"`    |
| `null`         | `"object"` ❌  |
| `{}`           | `"object"`    |
| `[]`           | `"object"`    |
| `new Date()`   | `"object"`    |
| `new Map()`    | `"object"`    |
| `new Set()`    | `"object"`    |
| `function(){}` | `"function"`  |

---

# 3. Array Quirk

```js
typeof []
```

Output:

```
"object"
```

Arrays are objects.

Correct way to check arrays:

```js
Array.isArray([])
```

Result:

```
true
```

---

# 4. Function Special Case

```js
typeof function(){}
```

Output:

```
"function"
```

Functions are actually objects.

```js
function test(){}

test instanceof Object
```

Result:

```
true
```

---

# 5. NaN Quirk

```js
typeof NaN
```

Output:

```
"number"
```

Even though NaN means "Not a Number".

---

# 6. Checking Undefined Safely (Important)

```js
typeof x
```

If x is not declared:

```
"undefined"
```

No error.

---

But:

```js
x === undefined
```

Error:

```
ReferenceError
```

---

## Why typeof is Used

```js
if(typeof x === "undefined"){
}
```

Safe check.

---

# 7. typeof vs instanceof

Important distinction.

```js
typeof []
```

Result:

```
"object"
```

But:

```js
[] instanceof Array
```

Result:

```
true
```

---

# 8. Important Interview Edge Cases

---

## Case 1

```js
typeof null
```

Result:

```
"object"
```

---

## Case 2

```js
typeof undefined
```

Result:

```
"undefined"
```

---

## Case 3

```js
typeof []
```

Result:

```
"object"
```

---

## Case 4

```js
typeof {}
```

Result:

```
"object"
```

---

## Case 5

```js
typeof function(){}
```

Result:

```
"function"
```

---

## Case 6

```js
typeof NaN
```

Result:

```
"number"
```

---

## Case 7

```js
typeof 10n
```

Result:

```
"bigint"
```

---

# 9. Reliable Type Checking (Interview-Level)

## For Array

```js
Array.isArray(value)
```

---

## For Null

```js
value === null
```

---

## For Object

```js
typeof value === "object" && value !== null
```

---

## Universal Method

```js
Object.prototype.toString.call(value)
```

Examples:

```
[object Array]
[object Object]
[object Date]
```

---

# 10. Common Interview Questions

### Q1: Why typeof null is object?

Answer:

> It is a legacy bug in JavaScript caused by early type-tagging implementation and kept for backward compatibility.

---

### Q2: How to check null correctly?

Answer:

```js
value === null
```

---

### Q3: How to detect array?

Answer:

```js
Array.isArray(value)
```

---

# 11. Perfect Interview Answer

> typeof null returns "object" due to a historical bug in JavaScript. typeof also returns "object" for arrays and other objects, and "function" for functions even though they are objects. Therefore typeof should be used carefully for type checking.

---

## Next Important Topic

Next topic in your list:

**Mutability vs Immutability**

This is **very important for React interviews.**
