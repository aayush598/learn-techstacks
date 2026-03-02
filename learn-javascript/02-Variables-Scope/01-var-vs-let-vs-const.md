Here is a **deep, interview-quality explanation of `var` vs `let` vs `const`**, including **internal behavior, hoisting, scope, edge cases, and interview traps**. This topic is **almost guaranteed in interviews**, often with tricky examples.

---

# var vs let vs const

These three keywords are used to **declare variables in JavaScript**, but they behave differently in **scope, hoisting, reassignment, and redeclaration**.

---

# 1. `var`

## Definition

`var` is the **old way** to declare variables in JavaScript (before ES6).

```js
var x = 10;
```

---

## Characteristics

### 1️⃣ Function Scope

`var` is scoped to the **function**, not the block.

```js
if (true) {
    var a = 5;
}

console.log(a); // 5
```

The variable escapes the block.

---

### 2️⃣ Hoisting with Initialization

`var` is hoisted and initialized with `undefined`.

```js
console.log(a);
var a = 10;
```

Behind the scenes:

```js
var a;
console.log(a); // undefined
a = 10;
```

---

### 3️⃣ Re-declaration Allowed

```js
var x = 10;
var x = 20;

console.log(x); // 20
```

This is allowed and often causes bugs.

---

### 4️⃣ Re-assignment Allowed

```js
var x = 10;
x = 50;
```

---

### 5️⃣ Global Object Binding

When declared globally, `var` becomes a property of `window`.

```js
var a = 10;
console.log(window.a); // 10
```

`let` and `const` do not behave this way.

---

# 2. `let`

## Definition

`let` was introduced in **ES6** to fix problems with `var`.

```js
let x = 10;
```

---

## Characteristics

### 1️⃣ Block Scope

`let` is limited to `{}` blocks.

```js
if (true) {
    let a = 5;
}

console.log(a); // ReferenceError
```

---

### 2️⃣ Hoisting Without Initialization

`let` is hoisted but not initialized.

```js
console.log(a);
let a = 10;
```

Result:

```
ReferenceError
```

Because of the **Temporal Dead Zone**.

---

### 3️⃣ No Re-declaration

```js
let x = 10;
let x = 20;
```

Error:

```
Identifier already declared
```

---

### 4️⃣ Re-assignment Allowed

```js
let x = 10;
x = 15;
```

---

### 5️⃣ Not Attached to Window

```js
let a = 10;

console.log(window.a); // undefined
```

---

# 3. `const`

## Definition

`const` declares a variable that **cannot be reassigned**.

```js
const x = 10;
```

---

## Characteristics

### 1️⃣ Block Scope

Same as `let`.

```js
{
  const a = 5;
}

console.log(a); // ReferenceError
```

---

### 2️⃣ Hoisting Without Initialization

```js
console.log(a);
const a = 10;
```

Error:

```
ReferenceError
```

---

### 3️⃣ Must Be Initialized

```js
const x;
```

Error:

```
Missing initializer
```

---

### 4️⃣ No Re-assignment

```js
const x = 10;

x = 20;
```

Error:

```
Assignment to constant variable
```

---

### 5️⃣ Objects and Arrays Can Change (Important)

`const` protects the **reference**, not the value.

```js
const user = {
  name: "John"
};

user.name = "Mike"; // allowed
```

But:

```js
user = {}; // error
```

---

# 4. Internal Behavior Comparison

## Example

```js
var a = 10;
let b = 20;
const c = 30;
```

### Memory Creation Phase

Engine stores:

```
a → undefined
b → TDZ
c → TDZ
```

### Execution Phase

```
a = 10
b = 20
c = 30
```

---

# 5. Key Differences

| Feature                 | var             | let       | const     |
| ----------------------- | --------------- | --------- | --------- |
| Scope                   | Function        | Block     | Block     |
| Hoisting                | Yes (undefined) | Yes (TDZ) | Yes (TDZ) |
| Re-declaration          | Yes             | No        | No        |
| Re-assignment           | Yes             | Yes       | No        |
| Initialization Required | No              | No        | Yes       |
| Window Object           | Yes             | No        | No        |

---

# 6. Classic Interview Examples

## Example 1

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

Because `var` is function-scoped.

---

## Example 2

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

Because `let` creates a new block scope per iteration.

---

## Example 3

```js
var a = 10;

function test() {
 console.log(a);
 var a = 20;
}

test();
```

Output:

```
undefined
```

Because:

```
var a;
console.log(a);
a = 20;
```

---

# 7. When to Use Each

### Use `const` (Default Choice)

```js
const API_URL = "example.com";
```

Best for:

* Constants
* Objects
* Arrays
* Functions

---

### Use `let` (When Value Changes)

```js
let counter = 0;
counter++;
```

Best for:

* Counters
* Loops
* Mutable values

---

### Avoid `var`

Only used in:

* Old codebases
* Legacy projects

---

# 8. Perfect Interview Answer (Concise)

> `var` is function-scoped and hoisted with undefined. `let` and `const` are block-scoped and exist in the temporal dead zone until initialized. `let` allows reassignment while `const` does not. Modern JavaScript prefers `const` and `let` because they prevent scope-related bugs.

---

Next most important subtopic:

**Block Scope vs Function Scope**

or

**Temporal Dead Zone (very important interview topic)**

Both are commonly asked immediately after `var let const`.
