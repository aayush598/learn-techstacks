## `string` Primitive Type in JavaScript (Detailed Interview Explanation)

### Definition

A **string** is a primitive data type used to represent **textual data** in JavaScript.

```js
let name = "John";
let city = 'Delhi';
let message = `Hello`;
```

Strings are:

* Primitive values
* Immutable
* Stored by value
* Indexed sequences of characters

---

# 1. Ways to Create Strings

## 1. Double Quotes

```js
let name = "John";
```

## 2. Single Quotes

```js
let name = 'John';
```

There is **no functional difference** between single and double quotes.

---

## 3. Template Literals (Backticks)

Introduced in ES6.

```js
let name = "John";
let msg = `Hello ${name}`;
```

### Advantages

#### 1. Variable Interpolation

```js
let age = 25;
let text = `Age is ${age}`;
```

---

#### 2. Multiline Strings

```js
let text = `Hello
World`;
```

Without template literals:

```js
let text = "Hello\nWorld";
```

---

#### 3. Expressions Inside Strings

```js
let result = `Sum is ${5 + 5}`;
```

---

# 2. String Immutability

Strings **cannot be modified after creation**.

```js
let str = "hello";

str[0] = "H";

console.log(str);
```

Output:

```
hello
```

The original string remains unchanged.

---

## Why Strings Are Immutable

Instead of modifying:

```js
str[0] = "H";
```

JavaScript creates a **new string**:

```js
str = "Hello";
```

---

## Interview Explanation

> Strings are immutable, meaning operations on strings create new strings instead of modifying the original one.

---

# 3. String Indexing

Strings behave like arrays of characters.

```js
let text = "JavaScript";

console.log(text[0]); // J
console.log(text[4]); // S
```

---

## String Length

```js
let text = "Hello";

console.log(text.length);
```

Output:

```
5
```

---

# 4. String Methods (Important Interview Section)

String methods **do not modify the original string**.

---

## 1. toUpperCase()

```js
let text = "hello";

text.toUpperCase();
```

Result:

```
HELLO
```

---

## 2. toLowerCase()

```js
"text".toLowerCase()
```

---

## 3. trim()

Removes spaces.

```js
let text = " hello ";

text.trim();
```

Result:

```
"hello"
```

---

## 4. slice()

Extracts part of string.

```js
let text = "JavaScript";

text.slice(0,4);
```

Result:

```
Java
```

---

## 5. substring()

```js
text.substring(0,4);
```

Similar to slice.

---

### Difference Between slice and substring

| slice                 | substring         |
| --------------------- | ----------------- |
| Allows negative index | No negative index |

Example:

```js
"hello".slice(-2) // "lo"
```

---

## 6. includes()

```js
"javascript".includes("script")
```

Result:

```
true
```

---

## 7. indexOf()

```js
"hello".indexOf("l")
```

Result:

```
2
```

---

## 8. replace()

```js
"hello".replace("h","H")
```

Result:

```
Hello
```

---

## 9. split()

Converts string → array.

```js
"a,b,c".split(",")
```

Result:

```
["a","b","c"]
```

---

## 10. concat()

```js
"Hello".concat(" World")
```

---

# 5. String vs String Object (Interview Trap)

Primitive string:

```js
let a = "hello";
```

String object:

```js
let b = new String("hello");
```

### Difference

```js
typeof a // string
typeof b // object
```

### Comparison Problem

```js
"a" === new String("a")
// false
```

### Interview Rule

> Never use `new String()`.

---

# 6. String Comparison

Strings compare lexicographically.

```js
"apple" < "banana"
// true
```

Based on Unicode values.

---

# 7. Escape Characters

Used to include special characters.

| Escape | Meaning      |
| ------ | ------------ |
| \n     | New line     |
| \t     | Tab          |
| '      | Single quote |
| "      | Double quote |
| \      | Backslash    |

Example:

```js
let text = "Hello\nWorld";
```

---

# 8. String Coercion (Very Common)

JavaScript converts values into strings automatically.

```js
"5" + 5
```

Result:

```
"55"
```

Because `+` with string triggers concatenation.

---

### Conversion to String

```js
String(10)
```

or

```js
10 + ""
```

---

# 9. Memory Behavior

Strings are **stored by value**.

```js
let a = "hello";
let b = a;

b = "world";
```

Result:

```
a = "hello"
b = "world"
```

Separate copies.

---

# 10. Performance Interview Question

### Why Many String Concatenations Are Slow

```js
let result = "";

for(let i=0;i<1000;i++){
 result += "a";
}
```

Each iteration creates a new string.

Better approach:

```js
let arr = [];

for(let i=0;i<1000;i++){
 arr.push("a");
}

arr.join("");
```

---

# 11. Important Interview Edge Cases

### Case 1

```js
typeof "hello"
```

Result:

```
"string"
```

---

### Case 2

```js
"hello" instanceof String
```

Result:

```
false
```

Because primitive.

---

### Case 3

```js
new String("hello") instanceof String
```

Result:

```
true
```

---

### Case 4

```js
"abc"[1]
```

Result:

```
"b"
```

---

# 12. Common Interview Questions About Strings

### Q1: Are strings mutable?

Answer:

> No. Strings are immutable. Any modification creates a new string.

---

### Q2: Where are strings stored?

Answer:

> Strings are primitive values stored directly in memory.

---

### Q3: Difference between slice and substring?

Answer:

> slice supports negative indices while substring does not.

---

### Q4: Difference between String and string?

Answer:

> string is a primitive type while String is an object wrapper.

---

# Final Interview Summary (Strong Answer)

> Strings are immutable primitive values used to store text in JavaScript. They are indexed, stored by value, and operations on strings create new strings instead of modifying the original one. Template literals allow interpolation and multiline strings.

---

Next recommended primitive types:

* **number** (very important)
* **boolean**
* **undefined vs null (very common interview question)**
