## Reference Types in JavaScript (Detailed Interview Explanation)

### Definition

**Reference types (non-primitive types)** are data types that store **references (memory addresses)** instead of actual values.

When you assign or copy a reference type, you copy the **reference**, not the value.

Main reference types:

* Object
* Array
* Function
* Date
* Map
* Set

---

# 1. How Reference Types Work Internally

### Primitive Example

```js
let a = 10;
let b = a;

b = 20;
```

Memory:

```
a → 10
b → 20
```

Separate copies.

---

### Reference Example

```js
let obj1 = { x: 10 };
let obj2 = obj1;

obj2.x = 20;
```

Memory:

```
obj1 → memory location A
obj2 → memory location A
```

Result:

```
obj1.x = 20
obj2.x = 20
```

Both point to same object.

---

### Interview Explanation

> Reference types store memory addresses, so copying them copies the reference rather than the value.

---

# 2. Object

## Definition

An **object** is a collection of key-value pairs.

```js
const user = {
 name: "John",
 age: 25
};
```

---

## Characteristics

* Mutable
* Stored by reference
* Dynamic structure
* Keys are usually strings or symbols

---

## Accessing Properties

### Dot Notation

```js
user.name
```

---

### Bracket Notation

```js
user["age"]
```

Useful when keys are dynamic.

---

## Modifying Objects

```js
user.age = 30;
```

Allowed even with const:

```js
const user = { age: 20 };

user.age = 25;
```

Works because reference is constant, not content.

---

## Object Copy Problem (Interview Favorite)

```js
const a = { x: 1 };
const b = a;

b.x = 2;
```

Result:

```
a.x = 2
```

Because same reference.

---

## Creating Copies

### Shallow Copy

```js
const copy = {...a};
```

or

```js
Object.assign({}, a);
```

---

## Deep Copy

```js
JSON.parse(JSON.stringify(a))
```

Limitations:

* No functions
* No Date objects
* No undefined
* No Symbol

---

# 3. Array

## Definition

An array is an ordered list of values.

```js
const arr = [1,2,3];
```

---

## Characteristics

* Mutable
* Stored by reference
* Dynamic size

---

## Reference Behavior

```js
const a = [1,2];
const b = a;

b.push(3);

console.log(a);
```

Result:

```
[1,2,3]
```

Same reference.

---

## Copying Arrays

### Shallow Copy

```js
const copy = [...arr];
```

or

```js
const copy = arr.slice();
```

---

## Deep Copy

```js
JSON.parse(JSON.stringify(arr))
```

---

# 4. Function

## Definition

Functions are **objects that can be executed**.

```js
function greet() {}
```

---

## Functions Are Objects

```js
function test(){}

test.x = 10;

console.log(test.x);
```

Output:

```
10
```

---

## First-Class Functions

Functions can:

* Be assigned

```js
const f = function() {};
```

* Passed

```js
setTimeout(f,1000);
```

* Returned

```js
function outer(){
 return function(){}
}
```

---

## typeof Function

```js
typeof function(){}
```

Result:

```
"function"
```

Special case.

Actually functions are objects.

---

# 5. Date

## Definition

Represents date and time.

```js
const now = new Date();
```

---

## Stored as Timestamp

Internally:

```
Milliseconds since Jan 1 1970
```

---

## Mutable Object

```js
const d = new Date();

d.setFullYear(2030);
```

Allowed.

---

## Reference Behavior

```js
const d1 = new Date();
const d2 = d1;

d2.setFullYear(2030);
```

Both change.

---

# 6. Map

## Definition

Map stores key-value pairs where keys can be **any type**.

```js
const map = new Map();

map.set("name","John");
```

---

## Object vs Map

| Object              | Map               |
| ------------------- | ----------------- |
| Keys mostly strings | Any type keys     |
| Slower operations   | Faster operations |
| Not ordered         | Ordered           |

---

## Example

```js
const map = new Map();

map.set(1,"one");
map.set(true,"yes");
```

Valid.

---

## Reference Behavior

```js
const m1 = new Map();
const m2 = m1;

m2.set("a",1);
```

Both affected.

---

# 7. Set

## Definition

Set stores **unique values**.

```js
const set = new Set([1,2,2,3]);
```

Result:

```
{1,2,3}
```

---

## Characteristics

* Unique values
* Mutable
* Stored by reference

---

## Example

```js
set.add(5);
set.has(5);
set.delete(5);
```

---

## Reference Behavior

```js
const s1 = new Set([1]);
const s2 = s1;

s2.add(2);
```

Both change.

---

# 8. typeof Reference Types

| Value        | typeof   |
| ------------ | -------- |
| {}           | object   |
| []           | object   |
| null         | object ❌ |
| function(){} | function |
| new Date()   | object   |
| new Map()    | object   |
| new Set()    | object   |

---

# 9. Mutability (Important Interview Topic)

Reference types are mutable.

Example:

```js
const obj = { a:1 };

obj.a = 2;
```

Allowed.

---

Primitive:

```js
let s = "hi";

s[0] = "H";
```

Not allowed.

---

# 10. Equality Behavior (Interview Favorite)

---

## Primitive Comparison

```js
10 === 10
```

Result:

```
true
```

---

## Object Comparison

```js
{} === {}
```

Result:

```
false
```

Because different references.

---

## Array Comparison

```js
[] === []
```

Result:

```
false
```

---

## Same Reference

```js
const a = {};
const b = a;

a === b
```

Result:

```
true
```

---

# 11. Important Interview Traps

---

## Trap 1

```js
const a = {x:1};
const b = {x:1};

a === b
```

Result:

```
false
```

---

## Trap 2

```js
const arr1 = [1];
const arr2 = [1];

arr1 === arr2
```

Result:

```
false
```

---

## Trap 3

```js
const obj = {a:1};

const copy = obj;

copy.a = 5;
```

Result:

```
obj.a = 5
```

---

# 12. Memory Model (Interview-Level)

Reference types:

```
Stack:
obj → Address 0x123

Heap:
0x123 → {x:10}
```

Assignment:

```
obj2 → Address 0x123
```

Same object.

---

# Final Interview Summary (Strong Answer)

> Reference types store memory addresses instead of actual values. Objects, arrays, functions, maps, and sets are reference types. When assigned or copied, they share the same memory reference, which is why modifying one variable affects the other.

---

Next **VERY IMPORTANT interview topic:**

**Primitive vs Reference Types (Deep Comparison)**

This question is asked in almost every JavaScript interview.
