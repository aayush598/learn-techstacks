## Global Scope Pollution

**Global scope pollution** occurs when too many variables or functions are defined in the **global scope**, making them accessible everywhere in the program. This increases the risk of **name conflicts, accidental overwrites, and hard-to-debug errors**.

This is a commonly asked interview concept related to **scope management and best practices**.

---

# 1. What is Global Scope?

A variable is in **global scope** if it is declared **outside any function or block**, or if it is **implicitly created without declaration**.

Example:

```js
let a = 10;
const b = 20;
var c = 30;
```

These variables are accessible anywhere in the program.

---

# 2. What is Global Scope Pollution?

Global scope pollution happens when:

* Too many variables exist globally
* Variables accidentally become global
* Different scripts use the same variable names
* Global variables get overwritten

Example:

```js
var userName = "John";
var total = 100;
var count = 5;
var data = {};
```

If many scripts do this, conflicts occur.

---

# 3. Accidental Global Variables (Very Important)

One of the biggest causes of global pollution is **missing declarations**.

### Example

```js
function test() {
   x = 10;
}

test();

console.log(x);
```

Output:

```
10
```

Because:

```js
x = 10;
```

creates a global variable automatically.

---

## Why This Happens

Without `let`, `const`, or `var`, JavaScript assigns the variable to the global object.

In browsers:

```js
x = 10;

console.log(window.x); // 10
```

---

# 4. var Creates Global Object Properties

When declared globally with `var`, variables become properties of `window`.

```js
var a = 10;

console.log(window.a); // 10
```

But:

```js
let b = 20;
const c = 30;

console.log(window.b); // undefined
console.log(window.c); // undefined
```

So `var` contributes more to global pollution.

---

# 5. Problems Caused by Global Scope Pollution

## 1️⃣ Name Conflicts

Two scripts using same variable:

```js
var user = "John";
```

Another script:

```js
var user = "Admin";
```

Now original value is lost.

---

## 2️⃣ Accidental Overrides

Example:

```js
var count = 10;

function update() {
   count = 5;
}
```

Function modifies global variable unintentionally.

---

## 3️⃣ Hard Debugging

When many functions modify global variables:

```js
total = 100;

function add() {
 total += 10;
}

function subtract() {
 total -= 5;
}
```

Tracking value becomes difficult.

---

## 4️⃣ Security Risks

Global variables can be modified by any script loaded on the page.

---

## 5️⃣ Memory Issues

Global variables stay in memory until the page closes.

Local variables get garbage collected.

---

# 6. How to Prevent Global Scope Pollution

## 1️⃣ Always Use let or const

Bad:

```js
x = 10;
```

Good:

```js
let x = 10;
```

---

## 2️⃣ Use Strict Mode

Strict mode prevents accidental globals.

```js
"use strict";

x = 10;
```

Error:

```
ReferenceError
```

---

## 3️⃣ Use Functions to Encapsulate Variables

Bad:

```js
var total = 100;
```

Better:

```js
function calculate() {
   let total = 100;
}
```

---

## 4️⃣ Use IIFE (Immediately Invoked Function Expression)

Very common interview topic.

```js
(function() {
   let privateVar = 10;
})();
```

Variable stays private.

---

## 5️⃣ Use ES Modules (Modern Best Practice)

Each module has its own scope.

Example:

```js
export const a = 10;
```

Imported only where needed.

Modules automatically avoid global pollution.

---

# 7. Example of Global Pollution Problem

### File 1

```js
var config = {
  theme: "dark"
};
```

### File 2

```js
var config = {
  language: "en"
};
```

Second file overwrites first.

---

# 8. Global vs Local Variables

## Global Variable

```js
let a = 10;
```

Accessible everywhere.

---

## Local Variable

```js
function test() {
   let a = 10;
}
```

Accessible only inside function.

---

# 9. Interview Trap Question

### Example

```js
function test() {
   var a = b = 10;
}

test();

console.log(a);
console.log(b);
```

Result:

```
ReferenceError
10
```

Explanation:

```js
var a = 10;
b = 10;
```

* `a` → function scope
* `b` → global scope

Very common interview question.

---

# 10. Real-World Example

Bad:

```js
var user;
var cart;
var total;
var isLoggedIn;
```

Good:

```js
function app() {
 let user;
 let cart;
 let total;
 let isLoggedIn;
}
```

Better isolation.

---

# 11. Perfect Interview Answer

> Global scope pollution happens when too many variables are declared in the global scope or variables are accidentally created globally. This can cause naming conflicts, unexpected overrides, and debugging difficulties. It can be prevented by using let and const, strict mode, functions, and ES modules.

---

Next topic:

**Best Practices for Variable Declaration**

After that we move to:

**Data Types (Primitive vs Reference)** — another very high-frequency interview topic.
