## Temporal Dead Zone (TDZ)

The **Temporal Dead Zone (TDZ)** is a fundamental concept related to **`let` and `const` hoisting**. It is frequently asked in interviews because it demonstrates understanding of **JavaScript execution phases and hoisting behavior**.

---

# 1. Definition

The **Temporal Dead Zone** is the period between:

* When a variable is **hoisted**
* And when it is **initialized**

During this period, the variable **exists in memory but cannot be accessed**.

If accessed, JavaScript throws a:

```
ReferenceError
```

---

# 2. Basic Example

```js
console.log(a);
let a = 10;
```

Output:

```
ReferenceError: Cannot access 'a' before initialization
```

---

# 3. Why This Happens

JavaScript runs code in two phases:

## Phase 1 — Memory Creation Phase

Variables are stored in memory:

```
a → uninitialized (TDZ)
```

For comparison:

```
var a → undefined
let a → TDZ
const a → TDZ
```

---

## Phase 2 — Execution Phase

```js
let a = 10;
```

Now:

```
a → 10
```

Before this line executes, `a` is inside TDZ.

---

# 4. TDZ vs var Hoisting

## Example with `var`

```js
console.log(a);
var a = 10;
```

Output:

```
undefined
```

Because:

```
var a = undefined;
console.log(a);
a = 10;
```

---

## Example with `let`

```js
console.log(a);
let a = 10;
```

Output:

```
ReferenceError
```

Because:

```
a exists but is uninitialized
```

---

# 5. TDZ with const

Same behavior as `let`.

```js
console.log(x);
const x = 5;
```

Output:

```
ReferenceError
```

---

# 6. TDZ Inside Block Scope

TDZ also applies inside blocks.

```js
{
   console.log(a);
   let a = 10;
}
```

Output:

```
ReferenceError
```

Because TDZ starts at the **beginning of the block**.

---

# 7. TDZ Timeline

Example:

```js
{
   let x = 5;
}
```

Timeline:

```
Block Starts → TDZ begins
let x = 5 → TDZ ends
Block Ends → x destroyed
```

---

# 8. TDZ With Functions

Example:

```js
function test() {

   console.log(a);

   let a = 10;

}

test();
```

Output:

```
ReferenceError
```

Because TDZ exists inside function scope too.

---

# 9. TDZ with Default Parameters (Advanced Interview Question)

Example:

```js
let a = 5;

function test(a = a) {
   console.log(a);
}

test();
```

Output:

```
ReferenceError
```

Reason:

Parameter `a` creates a new scope.

Inside function:

```
a → TDZ
```

So default value tries to use `a` before initialization.

---

# 10. TDZ with typeof (Very Common Interview Trap)

Normally:

```js
typeof x;
```

Output:

```
undefined
```

But:

```js
typeof a;
let a = 10;
```

Output:

```
ReferenceError
```

Because:

`a` exists but is in TDZ.

---

# 11. Why Temporal Dead Zone Exists

Before ES6:

```js
console.log(a);
var a = 10;
```

Produced:

```
undefined
```

This caused bugs because:

* Variables could be used before assignment
* Hard to detect mistakes

TDZ was introduced to:

* Make behavior predictable
* Prevent unsafe access
* Improve code quality

---

# 12. Important Rules

### Rule 1

TDZ applies to:

* `let`
* `const`
* `class`

---

### Rule 2

TDZ starts:

```
Beginning of scope
```

Example:

```js
{
   // TDZ starts here

   let x = 10;

   // TDZ ends here
}
```

---

### Rule 3

TDZ ends when variable is initialized.

---

# 13. Classic Interview Examples

## Example 1

```js
let a = 10;

function test() {
   console.log(a);
   let a = 20;
}

test();
```

Output:

```
ReferenceError
```

Why:

Inside function:

```
let a → TDZ
```

Local variable hides global variable.

---

## Example 2

```js
let a = 10;

{
   console.log(a);
   let a = 20;
}
```

Output:

```
ReferenceError
```

Block variable shadows outer variable.

---

# 14. Visual Explanation

Example:

```js
console.log(a);
let a = 10;
```

Memory Phase:

```
a → TDZ
```

Execution Phase:

```
console.log(a) ❌
a = 10
```

---

# 15. Perfect Interview Answer

> The Temporal Dead Zone is the time between when a variable declared with `let` or `const` is hoisted and when it is initialized. During this period the variable cannot be accessed and will throw a ReferenceError. It starts at the beginning of the scope and ends when the variable is assigned a value.

---

Next recommended topic:

**Variable Shadowing**

or

**Hoisting (Deep Dive)**

Hoisting is one of the **most important JavaScript interview topics**.
