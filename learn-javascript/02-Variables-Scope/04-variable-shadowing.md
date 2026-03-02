## Variable Shadowing

**Variable shadowing** occurs when a variable declared in an **inner scope** has the **same name** as a variable in an **outer scope**, causing the inner variable to temporarily override access to the outer variable within that scope.

This is a **common interview topic** because it tests understanding of **scope rules and variable resolution**.

---

# 1. Basic Definition

When JavaScript tries to access a variable, it searches:

1. Current scope
2. Parent scope
3. Global scope

If a variable exists in the current scope with the same name, it **shadows (hides)** the outer variable.

---

# 2. Basic Example

```js
let x = 10;

function test() {
    let x = 20;
    console.log(x);
}

test();
console.log(x);
```

Output:

```
20
10
```

Explanation:

* Inner `x` shadows outer `x`
* Inside function → `x = 20`
* Outside → `x = 10`

---

# 3. Scope Resolution (How JavaScript Finds Variables)

Example:

```js
let a = 1;

function outer() {
    let a = 2;

    function inner() {
        let a = 3;
        console.log(a);
    }

    inner();
}

outer();
```

Output:

```
3
```

JavaScript looks:

```
inner() scope → found a = 3
outer() scope → ignored
global scope → ignored
```

Nearest variable wins.

---

# 4. Shadowing with Block Scope

Shadowing commonly occurs with `let` and `const`.

```js
let count = 5;

if (true) {
    let count = 10;
    console.log(count);
}

console.log(count);
```

Output:

```
10
5
```

Inner variable exists only inside block.

---

# 5. Shadowing with Functions

```js
let user = "John";

function login() {
    let user = "Admin";
    console.log(user);
}

login();
console.log(user);
```

Output:

```
Admin
John
```

Function variable shadows global variable.

---

# 6. Shadowing vs Reassignment (Important Difference)

## Shadowing

Creates a **new variable**

```js
let x = 10;

{
   let x = 20;
}
```

Two separate variables exist.

---

## Reassignment

Changes the **same variable**

```js
let x = 10;

{
   x = 20;
}
```

Only one variable exists.

---

# 7. Legal Shadowing

Allowed cases:

### Example 1

```js
let a = 10;

{
   let a = 20;
}
```

Valid.

---

### Example 2

```js
const x = 5;

function test() {
   const x = 10;
}
```

Valid.

---

# 8. Illegal Shadowing (Very Important Interview Question)

Illegal shadowing happens when `var` conflicts with block-scoped variables.

### Example

```js
let a = 10;

{
   var a = 20;
}
```

Error:

```
SyntaxError: Identifier 'a' has already been declared
```

Reason:

* `var` is function/global scoped
* `let` is block scoped
* `var` tries to redeclare same variable

---

## Another Illegal Example

```js
const x = 5;

{
   var x = 10;
}
```

Error.

---

# 9. Legal Mixed Shadowing

This is allowed:

```js
var a = 10;

{
   let a = 20;
}
```

Why?

* `var a` → global/function scope
* `let a` → block scope

Different scopes.

---

# 10. Shadowing with Functions vs Blocks

### Example

```js
var a = 10;

function test() {
   var a = 20;
}

test();
```

Valid shadowing.

Function scope is separate.

---

# 11. Shadowing + Temporal Dead Zone (Advanced)

Example:

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

Explanation:

Inside function:

```
let a → TDZ
```

Local variable shadows global variable even before initialization.

---

# 12. Nested Shadowing

Example:

```js
let x = 1;

function a() {
   let x = 2;

   function b() {
      let x = 3;
      console.log(x);
   }

   b();
}

a();
```

Output:

```
3
```

Closest scope is used.

---

# 13. Why Variable Shadowing Can Be Dangerous

Problems:

### 1️⃣ Confusing Code

```js
let total = 100;

function calculate() {
   let total = 50;
}
```

Hard to track values.

---

### 2️⃣ Bugs

Developer might think outer variable is changing.

---

### 3️⃣ Hidden Variables

Shadowing hides outer variables unintentionally.

---

# 14. Best Practices

### Use Different Names

Good:

```js
let totalPrice = 100;

function calculate() {
   let discountPrice = 50;
}
```

---

### Avoid Deep Shadowing

Avoid:

```js
let x = 1;

function a() {
 let x = 2;

 if(true){
  let x = 3;
 }
}
```

---

### Keep Scope Small

Use block scope carefully.

---

# 15. Perfect Interview Answer

> Variable shadowing occurs when a variable declared in an inner scope has the same name as a variable in an outer scope, hiding the outer variable within that scope. JavaScript always resolves variables by searching from the nearest scope outward. Shadowing is allowed with `let` and `const`, but illegal shadowing can occur when `var` conflicts with block-scoped variables.

---

Next logical topic:

**Global Scope Pollution**

This is often asked with:

* var vs let
* window object
* strict mode
