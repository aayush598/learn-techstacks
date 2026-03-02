## Block Scope vs Function Scope

Understanding **block scope vs function scope** is essential because it explains **how variables are accessible in different parts of code** and why `var` behaves differently from `let` and `const`.

---

# 1. What is Scope?

**Scope** determines **where a variable can be accessed** in a program.

In JavaScript, the main scope types relevant here are:

* **Global Scope**
* **Function Scope**
* **Block Scope**

This section focuses on:

* Function scope (`var`)
* Block scope (`let`, `const`)

---

# 2. Function Scope

## Definition

A variable declared inside a function is accessible **everywhere inside that function**, but **not outside the function**.

Variables declared with **`var` are function-scoped**.

---

## Example

```js
function test() {
    var x = 10;
    console.log(x); // 10
}

console.log(x); // ReferenceError
```

Here:

* `x` exists only inside `test()`

---

## Important Behavior

### `var` ignores block scope

```js
function example() {

    if (true) {
        var a = 5;
    }

    console.log(a); // 5
}
```

Even though `a` was declared inside `{}`, it is still accessible in the function.

Because:

**`var` is function-scoped, not block-scoped.**

---

## Loop Example

```js
for (var i = 0; i < 3; i++) {}

console.log(i); // 3
```

The variable still exists outside the loop.

This is a major source of bugs.

---

# 3. Block Scope

## Definition

A variable declared inside `{}` is accessible **only inside that block**.

Variables declared with:

* `let`
* `const`

are block-scoped.

---

## Example

```js
if (true) {
    let x = 10;
}

console.log(x); // ReferenceError
```

The variable exists only inside the block.

---

## Example with `const`

```js
{
   const y = 20;
}

console.log(y); // ReferenceError
```

Same behavior as `let`.

---

# 4. Blocks in JavaScript

Blocks are created by `{}` in:

* `if` statements
* `for` loops
* `while` loops
* `switch`
* try/catch
* standalone `{}` blocks

Example:

```js
{
   let a = 10;
}
```

---

# 5. Function Scope vs Block Scope Example

## Example 1

```js
if (true) {

   var a = 10;
   let b = 20;
   const c = 30;

}

console.log(a); // 10
console.log(b); // ReferenceError
console.log(c); // ReferenceError
```

Explanation:

* `a` → function/global scope
* `b` → block scope
* `c` → block scope

---

# 6. Nested Scope Behavior

### Example

```js
let x = 10;

function test() {

   let y = 20;

   if (true) {
      let z = 30;
      console.log(x); // 10
      console.log(y); // 20
      console.log(z); // 30
   }

}
```

Rules:

* Inner scope can access outer scope
* Outer scope cannot access inner scope

---

# 7. Real Interview Example

### Example

```js
function test() {

   if (true) {
      var a = 10;
      let b = 20;
   }

   console.log(a); // 10
   console.log(b); // ReferenceError
}

test();
```

Why?

Because:

* `var` → function scoped
* `let` → block scoped

---

# 8. Loop + Closure Interview Trap

### Using `var`

```js
for (var i = 0; i < 3; i++) {
   setTimeout(() => console.log(i), 1000);
}
```

Output:

```
3
3
3
```

Because:

* Only one `i`
* Function scope
* Final value is 3

---

### Using `let`

```js
for (let i = 0; i < 3; i++) {
   setTimeout(() => console.log(i), 1000);
}
```

Output:

```
0
1
2
```

Because:

* Each iteration creates a new block scope

---

# 9. Visual Scope Model

Example:

```js
let a = 1;

function test() {

   let b = 2;

   if (true) {

      let c = 3;

   }

}
```

Scope access:

```
Global Scope:
   a

Function Scope:
   b

Block Scope:
   c
```

Accessible:

| Variable | Accessible Where  |
| -------- | ----------------- |
| a        | Everywhere inside |
| b        | Inside function   |
| c        | Inside block only |

---

# 10. Why Block Scope Was Introduced

Before ES6, only `var` existed.

Problems:

* Variables leaking outside blocks
* Hard-to-find bugs
* Unexpected values

Example:

```js
if (true) {
   var user = "John";
}

console.log(user); // exists unexpectedly
```

Block scope fixed this.

---

# 11. Practical Use Cases

## Function Scope Use Case

```js
function calculate() {
   var total = 0;
}
```

`total` belongs to function logic.

---

## Block Scope Use Case

```js
if (userLoggedIn) {
   let token = "abc";
}
```

Token should exist only inside condition.

---

# 12. Perfect Interview Answer

> Function scope means variables declared with `var` are accessible throughout the entire function. Block scope means variables declared with `let` and `const` are accessible only inside the block `{}` where they are declared. Block scope prevents variables from leaking and avoids bugs.

---

Next best topic (commonly asked right after this):

**Temporal Dead Zone (TDZ)**

This is asked in almost every JavaScript interview.
