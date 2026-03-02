# Mutability vs Immutability in JavaScript (Detailed Interview Explanation)

This is a **very important topic**, especially for **React interviews**, because React relies heavily on **immutability for state updates**.

---

# 1. Definition

## Mutable

A value is **mutable** if it can be **changed after creation** without creating a new value.

Example:

```js
const obj = { a: 1 };

obj.a = 2;
```

The object itself changed.

---

## Immutable

A value is **immutable** if it **cannot be changed after creation**. Any modification creates a **new value**.

Example:

```js
let str = "hello";

str = "world";
```

Original string not modified — new string created.

---

# 2. Primitive Types Are Immutable

All primitive types are immutable:

* string
* number
* boolean
* null
* undefined
* symbol
* bigint

---

## String Example

```js
let str = "hello";

str[0] = "H";

console.log(str);
```

Output:

```
hello
```

String unchanged.

---

## New Value Created

```js
str = "Hello";
```

Now:

```
Hello
```

New string created.

---

## Number Example

```js
let x = 10;

x = 20;
```

New value assigned.

---

# 3. Reference Types Are Mutable

Reference types are mutable:

* Object
* Array
* Function
* Map
* Set
* Date

---

## Object Example

```js
const obj = { a: 1 };

obj.a = 2;
```

Object changed.

---

## Array Example

```js
const arr = [1,2,3];

arr.push(4);
```

Array changed.

---

# 4. const Does NOT Mean Immutable (Interview Trap)

```js
const obj = { a: 1 };

obj.a = 2;
```

Works.

Because:

> const prevents reassignment, not mutation.

---

## Reassignment Error

```js
const obj = { a: 1 };

obj = { a: 2 };
```

Error.

---

# 5. Immutable Operations (Important for React)

Instead of mutating:

### Bad (Mutable)

```js
arr.push(4);
```

---

### Good (Immutable)

```js
const newArr = [...arr, 4];
```

Creates new array.

---

## Object Example

Mutable:

```js
user.name = "John";
```

Immutable:

```js
const newUser = {
 ...user,
 name: "John"
};
```

---

# 6. Why Immutability Matters

## 1. Predictable Code

Avoids side effects.

---

## 2. Easier Debugging

Old values preserved.

---

## 3. React Performance

React uses reference comparison.

Example:

```js
oldState === newState
```

If equal → no re-render.

---

# 7. Mutable Methods vs Immutable Methods

## Mutable Array Methods

Modify original array:

* push
* pop
* shift
* unshift
* splice
* sort
* reverse

Example:

```js
arr.push(5);
```

Original changed.

---

## Immutable Array Methods

Return new array:

* map
* filter
* slice
* concat

Example:

```js
const newArr = arr.map(x => x*2);
```

Original unchanged.

---

# 8. Object.freeze() (Interview Topic)

Makes object immutable.

```js
const obj = { a:1 };

Object.freeze(obj);

obj.a = 2;
```

Still:

```
1
```

Change ignored.

---

## Limitation (Important)

Freeze is shallow.

```js
const obj = {
 address: {
   city:"Delhi"
 }
};

Object.freeze(obj);

obj.address.city = "Mumbai";
```

Still changes.

---

# 9. Deep Immutability

Use:

* Recursive freeze
* structuredClone + freeze
* Libraries (Immer)

---

# 10. Memory Behavior

## Mutable Example

```js
const a = {x:1};
const b = a;

b.x = 2;
```

Result:

```
a.x = 2
```

Same object.

---

## Immutable Example

```js
const a = {x:1};

const b = {...a};

b.x = 2;
```

Result:

```
a.x = 1
b.x = 2
```

Different objects.

---

# 11. Equality Behavior

Mutable:

```js
const a = {x:1};
const b = a;

a === b
```

Result:

```
true
```

---

Immutable copy:

```js
const a = {x:1};
const b = {...a};

a === b
```

Result:

```
false
```

---

# 12. Common Interview Traps

---

## Trap 1

```js
const arr = [1,2];

const newArr = arr;

newArr.push(3);
```

arr becomes `[1,2,3]`.

---

## Trap 2

```js
const arr = [1,2];

const newArr = [...arr];

newArr.push(3);
```

arr stays `[1,2]`.

---

## Trap 3

```js
let str = "hello";

str.toUpperCase();
```

Result:

```
hello
```

Because new string returned.

Correct:

```js
str = str.toUpperCase();
```

---

# 13. Interview-Level Comparison

| Feature           | Mutable | Immutable          |
| ----------------- | ------- | ------------------ |
| Can change value  | Yes     | No                 |
| Creates new value | No      | Yes                |
| Primitives        | No      | Yes                |
| Objects           | Yes     | No (unless frozen) |

---

# 14. Perfect Interview Answer

> Primitive types in JavaScript are immutable, meaning their values cannot be changed after creation. Reference types like objects and arrays are mutable, meaning their properties or elements can be modified. Immutability is important in React because state updates rely on creating new objects instead of modifying existing ones.

---

## Next Major Interview Section

You have now completed **Data Types completely.**

Next high-value section:

**Functions Deep Dive**

or

**Hoisting (Extremely Important Interview Topic)**

The best next topic is **Hoisting** because it is asked in almost every interview.
