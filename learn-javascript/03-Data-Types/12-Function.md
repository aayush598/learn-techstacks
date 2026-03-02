# Function in JavaScript (Detailed Interview Explanation)

## Definition

A **function** is a reusable block of code that performs a task and can be executed when called.

```js
function greet() {
  console.log("Hello");
}
```

Functions in JavaScript are:

* Reference types
* Objects
* First-class citizens
* Callable objects
* Stored by reference

---

# 1. Functions Are Objects (Very Important)

Functions behave like objects.

```js
function test() {}

test.x = 10;

console.log(test.x);
```

Output:

```
10
```

This works because functions are objects internally.

---

## typeof Function

```js
typeof function(){}
```

Output:

```
"function"
```

Special case.

Technically:

```js
function(){} instanceof Object
```

Output:

```
true
```

---

### Interview Explanation

> Functions are special objects that can be executed.

---

# 2. Creating Functions

## 1️⃣ Function Declaration

```js
function greet() {
  console.log("Hello");
}
```

Characteristics:

* Hoisted
* Can be called before declaration

```js
greet();

function greet() {}
```

Works.

---

## 2️⃣ Function Expression

```js
const greet = function() {
  console.log("Hello");
};
```

Characteristics:

* Not hoisted
* Stored in variable

```js
greet();
```

Works only after declaration.

---

## 3️⃣ Arrow Functions

```js
const greet = () => {
  console.log("Hello");
};
```

Introduced in ES6.

---

# 3. Differences Between Function Types

| Feature      | Declaration | Expression | Arrow   |
| ------------ | ----------- | ---------- | ------- |
| Hoisted      | Yes         | No         | No      |
| this binding | Dynamic     | Dynamic    | Lexical |
| Constructor  | Yes         | Yes        | No      |

---

# 4. First-Class Functions (Very Important)

JavaScript functions are **first-class citizens**.

Meaning functions can:

---

## Assigned to Variables

```js
const f = function(){};
```

---

## Passed as Arguments

```js
setTimeout(function(){
 console.log("Hi");
},1000);
```

---

## Returned from Functions

```js
function outer(){
 return function(){
   console.log("Inner");
 };
}
```

---

### Interview Explanation

> Functions are first-class citizens because they can be assigned, passed, and returned.

---

# 5. Parameters vs Arguments

### Parameters

Defined in function:

```js
function add(a,b){}
```

---

### Arguments

Passed during call:

```js
add(1,2);
```

---

# 6. Default Parameters

```js
function greet(name="Guest"){
 console.log(name);
}
```

```js
greet();
```

Output:

```
Guest
```

---

# 7. Rest Parameters

Collect multiple arguments.

```js
function sum(...nums){
 return nums.reduce((a,b)=>a+b);
}
```

---

# 8. arguments Object

Available in normal functions.

```js
function test(){
 console.log(arguments);
}
```

Not available in arrow functions.

---

# 9. Return Values

```js
function add(a,b){
 return a+b;
}
```

If no return:

```js
function test(){}

test();
```

Result:

```
undefined
```

---

# 10. Arrow Functions (Very Important)

---

## Basic Arrow Function

```js
const add = (a,b)=>a+b;
```

---

## Single Parameter

```js
const square = x=>x*x;
```

---

## Multiple Lines

```js
const add = (a,b)=>{
 return a+b;
};
```

---

# 11. Arrow Function vs Normal Function

### 1️⃣ this Behavior

Normal:

```js
const obj = {
 name:"John",
 greet(){
  console.log(this.name);
 }
};
```

Works.

Arrow:

```js
const obj = {
 name:"John",
 greet:()=>{
  console.log(this.name);
 }
};
```

Does NOT work.

Because arrow functions don't have their own `this`.

---

### 2️⃣ Constructor

Normal functions:

```js
function User(){}
new User();
```

Works.

Arrow:

```js
const User = ()=>{};
new User();
```

Error.

---

### 3️⃣ arguments Object

Normal:

```js
function test(){
 console.log(arguments);
}
```

Arrow:

```js
const test=()=>{
 console.log(arguments);
}
```

Error.

---

# 12. Higher Order Functions (Very Important)

Functions that:

* Take functions as arguments
* Return functions

---

## Example

```js
function operate(fn,x){
 return fn(x);
}
```

Example:

```js
operate(x=>x*2,5);
```

Result:

```
10
```

---

Examples in JS:

* map
* filter
* reduce

---

# 13. Callback Functions

Function passed to another function.

```js
setTimeout(()=>{
 console.log("Done");
},1000);
```

Arrow function is callback.

---

# 14. Pure vs Impure Functions

---

## Pure Function

Same input → same output.

```js
function add(a,b){
 return a+b;
}
```

---

## Impure Function

Depends on external state.

```js
let x=10;

function add(a){
 return a+x;
}
```

---

# 15. Immediately Invoked Function Expression (IIFE)

Runs immediately.

```js
(function(){
 console.log("run");
})();
```

---

## Arrow IIFE

```js
(()=>{
 console.log("run");
})();
```

---

# 16. Function Scope

Variables inside functions are private.

```js
function test(){
 let x=10;
}
```

x not accessible outside.

---

# 17. Closures Preview

Functions remember outer variables.

```js
function outer(){
 let x=10;

 return function(){
   console.log(x);
 };
}
```

This is closure.

Major interview topic later.

---

# 18. Function Reference Behavior

Functions copied by reference.

```js
function a(){}

const b=a;

b===a
```

Result:

```
true
```

---

# 19. Important Interview Edge Cases

---

## Case 1

```js
typeof function(){}
```

Result:

```
"function"
```

---

## Case 2

```js
function test(){}
test instanceof Object
```

Result:

```
true
```

---

## Case 3

```js
(() => {})()
```

Immediately executes.

---

## Case 4

```js
function test(a,b){
 return;
 a+b;
}
```

Result:

```
undefined
```

Because newline after return.

---

## Case 5

```js
function test(a,b){
 return a+b;
}

test(1)
```

Result:

```
NaN
```

Because:

```
1 + undefined
```

---

# 20. Memory Model

Functions stored in heap.

Variable stores reference.

```id="mnjyot"
Stack:
f → 0x456

Heap:
0x456 → function code
```

---

# 21. Common Interview Questions

### Q1: Are functions objects?

Yes.

---

### Q2: What are first-class functions?

Functions that can be assigned, passed, and returned.

---

### Q3: Difference between arrow and normal functions?

Main difference is `this`.

---

### Q4: Are functions reference types?

Yes.

---

# Final Interview Summary (Strong Answer)

> Functions in JavaScript are first-class objects that can be assigned to variables, passed as arguments, and returned from other functions. They are stored by reference and support multiple forms such as function declarations, expressions, and arrow functions. Arrow functions differ mainly in their lexical this binding.

---

Next reference types:

* Date
* Map
* Set

Then we move to **Primitive vs Reference Types (one of the most important interview questions).**
