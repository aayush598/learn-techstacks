Below is a **deep, interview-grade explanation** of **Variables & Scope**, broken into **clear sub-parts**, with **internal behavior, edge cases, and interview traps**. This is one of the **highest-ROI JavaScript topics**, so read it carefully.

---

# 2. Variables & Scope

---

## 2.1 `var` vs `let` vs `const`

### 1️⃣ `var`

#### Characteristics

* **Function-scoped**
* **Hoisted** and initialized as `undefined`
* Allows **re-declaration**
* Allows **re-assignment**

```js
var x = 10;
var x = 20; // allowed
x = 30;     // allowed
```

#### Problems with `var`

* No block scope
* Causes unexpected bugs
* Leaks outside blocks (`if`, `for`)

```js
if (true) {
  var a = 5;
}
console.log(a); // 5 ❌
```

---

### 2️⃣ `let`

#### Characteristics

* **Block-scoped**
* Hoisted but **not initialized**
* No re-declaration in same scope
* Allows re-assignment

```js
let x = 10;
x = 20;     // allowed
let x = 30; // ❌ error
```

```js
if (true) {
  let b = 5;
}
console.log(b); // ❌ ReferenceError
```

---

### 3️⃣ `const`

#### Characteristics

* **Block-scoped**
* Hoisted but **not initialized**
* No re-declaration
* No re-assignment
* Must be initialized at declaration

```js
const x = 10;
x = 20; // ❌ error
```

#### Important Interview Trap

`const` does **not** make objects immutable.

```js
const obj = { a: 1 };
obj.a = 2; // allowed
```

Only the **reference** is constant.

---

### Comparison Table

| Feature    | var             | let       | const     |
| ---------- | --------------- | --------- | --------- |
| Scope      | Function        | Block     | Block     |
| Hoisting   | Yes (undefined) | Yes (TDZ) | Yes (TDZ) |
| Re-declare | Yes             | No        | No        |
| Re-assign  | Yes             | Yes       | No        |

---

## 2.2 Block Scope vs Function Scope

### Block Scope

A variable is accessible **only within `{}`**.

* `let`
* `const`

```js
{
  let x = 10;
}
console.log(x); // ❌
```

---

### Function Scope

A variable is accessible **inside the entire function**.

* `var`

```js
function test() {
  var y = 20;
}
console.log(y); // ❌
```

---

### Interview Insight

> `var` ignores block scope, which causes accidental variable leaks.

---

## 2.3 Temporal Dead Zone (TDZ)

### Definition

TDZ is the time between:

* Variable hoisting
* Variable initialization

Accessing a variable in this phase throws a **ReferenceError**.

---

### Example

```js
console.log(a); // ❌ ReferenceError
let a = 10;
```

Behind the scenes:

* `a` is hoisted
* Not initialized
* Exists in TDZ until declaration is reached

---

### Why TDZ Exists

* Prevents unsafe access
* Encourages clean code
* Eliminates unpredictable behavior of `var`

---

### Interview Framing

> `let` and `const` are hoisted but inaccessible until initialized.

---

## 2.4 Variable Shadowing

### Definition

When a variable in an inner scope has the **same name** as one in the outer scope.

---

### Example

```js
let x = 10;

function test() {
  let x = 20;
  console.log(x); // 20
}

console.log(x); // 10
```

---

### Illegal Shadowing (Trick Question)

```js
let a = 10;
{
  var a = 20; // ❌ SyntaxError
}
```

* `var` cannot shadow `let` in the same or nested scope

---

### Interview Tip

> Shadowing is allowed with `let`/`const`, but mixing `var` with block-scoped variables causes errors.

---

## 2.5 Global Scope Pollution

### Definition

Unintentionally creating variables in the global scope.

---

### How It Happens

```js
function test() {
  x = 10; // ❌ no declaration
}
```

* `x` becomes a global variable

---

### Problems

* Name collisions
* Hard-to-track bugs
* Security issues
* Poor performance

---

### How to Avoid

* Always use `let` / `const`
* Use strict mode
* Use modules

```js
"use strict";
x = 10; // ❌ error
```

---

## 2.6 Best Practices for Variable Declaration

### ✅ Prefer `const` by default

```js
const PI = 3.14;
```

### ✅ Use `let` only when re-assignment is needed

```js
let count = 0;
count++;
```

### ❌ Avoid `var`

Only for legacy code.

---

### ✅ Declare variables at top of scope

Improves readability.

---

### ✅ Avoid global variables

Use modules and closures.

---

### ✅ Use meaningful names

```js
let userAge; // good
let x;       // bad
```

---

## Final Interview Summary (Memorize This)

> `var` is function-scoped and hoisted with undefined, while `let` and `const` are block-scoped and exist in the temporal dead zone until initialized. JavaScript scope rules help prevent global pollution and enable predictable behavior when variables are declared correctly.

---

Next logical topic to continue:
➡ **Data Types (Primitive vs Reference)**
➡ **Hoisting in depth**
➡ **Execution Context**

Tell me which one to answer next, and I’ll continue in the same depth.
