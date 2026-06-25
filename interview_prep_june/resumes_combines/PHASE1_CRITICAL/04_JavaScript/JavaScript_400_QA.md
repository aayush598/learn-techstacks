# JavaScript (ES6+) - 400+ Interview Q&A

## For YC Startups & Top Tech Companies

---

# PHASE 1: FUNDAMENTALS (Q1–Q70)

---

### Q1: What is the difference between var, let, and const?

**Answer:**

`var` is function-scoped, hoisted to the top of its function, and can be redeclared and reassigned. `let` and `const` are block-scoped and are hoisted but not initialized (Temporal Dead Zone). `const` cannot be reassigned, though its properties can be mutated.

```js
// var - function scoped
function test() {
  var x = 1;
  if (true) {
    var x = 2; // same variable
    console.log(x); // 2
  }
  console.log(x); // 2
}

// let - block scoped
function test2() {
  let y = 1;
  if (true) {
    let y = 2; // different variable
    console.log(y); // 2
  }
  console.log(y); // 1
}

// const - block scoped, cannot reassign
const z = { name: 'Alice' };
z.name = 'Bob'; // allowed
// z = {}; // TypeError
```

---

### Q2: What is hoisting? Provide examples.

**Answer:**

Hoisting is JavaScript's behavior of moving declarations to the top of their scope during compilation. `var` declarations are hoisted and initialized with `undefined`. `let` and `const` are hoisted but not initialized (TDZ). Function declarations are hoisted entirely.

```js
// var hoisting
console.log(a); // undefined (not ReferenceError)
var a = 5;

// let/const hoisting (TDZ)
// console.log(b); // ReferenceError: Cannot access before initialization
let b = 10;

// Function declaration hoisting
foo(); // "hello"
function foo() {
  console.log('hello');
}

// Function expression - not hoisted
// bar(); // TypeError: bar is not a function
var bar = function() {
  console.log('world');
};
```

---

### Q3: What is the Temporal Dead Zone (TDZ)?

**Answer:**

The TDZ is the period between entering scope and the actual declaration of a `let` or `const` variable. Accessing the variable in this zone throws a `ReferenceError`. This prevents usage before initialization.

```js
{
  // TDZ starts here for x
  // console.log(x); // ReferenceError
  let x = 5; // TDZ ends here
  console.log(x); // 5
}

// TDZ also applies to default parameters
function test(y = x, x = 1) {
  // undefined reference: x is in TDZ when evaluating default for y
}
// test(); // ReferenceError
```

---

### Q4: What are the data types in JavaScript?

**Answer:**

JavaScript has 8 data types: 7 primitive (string, number, boolean, undefined, null, symbol, bigint) and 1 non-primitive (object).

```js
// Primitives
typeof 'hello';    // 'string'
typeof 42;         // 'number'
typeof true;       // 'boolean'
typeof undefined;  // 'undefined'
typeof null;       // 'object' (historical bug)
typeof Symbol();   // 'symbol'
typeof 10n;        // 'bigint'

// Non-primitive
typeof {};         // 'object'
typeof [];         // 'object'
typeof function(){}; // 'function'
```

---

### Q5: How does typeof differ from instanceof?

**Answer:**

`typeof` returns a string indicating the primitive type. `instanceof` checks whether an object is an instance of a constructor in its prototype chain.

```js
typeof 'hello';         // 'string'
typeof [];              // 'object'

[] instanceof Array;    // true
[] instanceof Object;   // true (Array inherits from Object)
'' instanceof String;   // false (primitive)

// instanceof with custom constructors
class Car {}
const myCar = new Car();
myCar instanceof Car;   // true
```

---

### Q6: What is type coercion? Give examples of implicit coercion.

**Answer:**

Type coercion is JavaScript's automatic conversion of values between types. It happens in operations involving mixed types.

```js
// String coercion
'5' + 3;      // '53'
'5' + null;   // '5null'

// Numeric coercion
'5' - 3;      // 2
'5' * '2';    // 10
'hello' - 1;  // NaN (string can't parse to number)
true + 1;     // 2
false + 1;    // 1
null + 1;     // 1
undefined + 1; // NaN

// Boolean coercion
if ('hello') {}  // truthy
if (0) {}        // falsy
!!'hello';       // true
!!0;             // false
```

---

### Q7: What is the difference between == and ===?

**Answer:**

`==` checks for value equality with type coercion. `===` checks for strict equality without coercion (type + value must match).

```js
// == coerces types
5 == '5';       // true
0 == false;     // true
null == undefined; // true
[] == false;    // true
'' == 0;        // true

// === no coercion
5 === '5';      // false
0 === false;    // false
null === undefined; // false

// Special cases
NaN == NaN;     // false
NaN === NaN;    // false
Object.is(NaN, NaN); // true
```

---

### Q8: What values are truthy and falsy in JavaScript?

**Answer:**

Falsy values: `false`, `0`, `''` (empty string), `null`, `undefined`, `NaN`. Everything else is truthy, including `'0'`, `'false'`, `[]`, `{}`, `-1`, `Infinity`.

```js
if (false) {}      // falsy
if (0) {}          // falsy
if ('') {}         // falsy
if (null) {}       // falsy
if (undefined) {}  // falsy
if (NaN) {}        // falsy

if ('0') {}        // truthy - non-empty string
if ('false') {}    // truthy - non-empty string
if ([]) {}         // truthy
if ({}) {}         // truthy
if (-1) {}         // truthy
```

---

### Q9: Explain null vs undefined vs NaN.

**Answer:**

`null` is an intentional absence of value (assigned). `undefined` means a variable has been declared but not assigned. `NaN` (Not a Number) is a numeric value resulting from an invalid math operation.

```js
let a;
console.log(a); // undefined

let b = null;
console.log(b); // null

console.log(parseInt('hello')); // NaN
console.log(Math.sqrt(-1));     // NaN

typeof null;       // 'object' (historical bug)
typeof undefined;  // 'undefined'
typeof NaN;        // 'number'

null == undefined;  // true
null === undefined; // false
NaN === NaN;        // false
isNaN(NaN);         // true
Number.isNaN(NaN);  // true
```

---

### Q10: What is a closure? Give a practical example.

**Answer:**

A closure is a function that retains access to its outer (enclosing) function's variables even after the outer function has returned. Closures are created every time a function is created.

```js
// Basic closure
function outer(x) {
  return function inner(y) {
    return x + y; // inner remembers x
  };
}
const add5 = outer(5);
console.log(add5(3)); // 8

// Practical: counter with encapsulation
function createCounter() {
  let count = 0;
  return {
    increment: () => ++count,
    decrement: () => --count,
    getCount: () => count,
  };
}
const counter = createCounter();
counter.increment(); // 1
counter.increment(); // 2
counter.decrement(); // 1

// Practical: memoization
function memoize(fn) {
  const cache = {};
  return function(...args) {
    const key = JSON.stringify(args);
    if (cache[key] !== undefined) return cache[key];
    return (cache[key] = fn(...args));
  };
}
```

---

### Q11: How can closures cause memory leaks?

**Answer:**

Closures prevent garbage collection of outer variables that are still referenced. If a closure outlives its intended scope, it keeps references alive unnecessarily, causing memory leaks.

```js
// Memory leak: closure retains large data
function leaky() {
  const largeArray = new Array(1000000).fill('data');
  return function() {
    console.log('hello');
    // largeArray is never used but kept alive
  };
}
const fn = leaky(); // largeArray cannot be GC'd

// Solution: nullify references
function fixed() {
  const largeArray = new Array(1000000).fill('data');
  const result = function() {
    console.log('hello');
  };
  largeArray = null; // allow GC
  return result;
}

// Classic leak: DOM references in closures
function addHandler() {
  const el = document.getElementById('btn');
  el.addEventListener('click', function handler() {
    console.log(el.id); // el referenced in closure
  });
  // Even after element removal, handler holds reference
}
```

---

### Q12: What is lexical scope?

**Answer:**

Lexical scope means that a variable's scope is determined by its position in the source code at compile time. Inner functions can access variables from their outer scopes based on where they are physically written.

```js
const global = 'global';

function outer() {
  const outerVar = 'outer';

  function inner() {
    const innerVar = 'inner';
    console.log(global);  // 'global'
    console.log(outerVar); // 'outer'
    console.log(innerVar); // 'inner'
  }

  inner();
}

outer();
// inner has access to all three scopes

// Scope chain: inner -> outer -> global
```

---

### Q13: What is an execution context and the call stack?

**Answer:**

An execution context is the environment where JavaScript code runs. It contains the variable environment, scope chain, and `this` binding. The call stack is a LIFO structure tracking execution contexts.

```js
function a() {
  console.log('a calls b');
  b();
  console.log('a done');
}

function b() {
  console.log('b calls c');
  c();
  console.log('b done');
}

function c() {
  console.log('c running');
  throw new Error('stack trace shows call stack');
}

a();

// Call stack visualization:
// 1. Global Execution Context
// 2. a() pushed
// 3.   b() pushed
// 4.     c() pushed
// 5.     c() popped
// 6.   b() popped
// 7. a() popped
```

---

### Q14: Explain the JavaScript event loop in detail.

**Answer:**

The event loop coordinates synchronous execution, microtasks (Promises, MutationObserver), and macrotasks (setTimeout, setInterval, I/O). It continuously checks the call stack: if empty, it processes all microtasks, then picks one macrotask.

```js
console.log('1'); // sync

setTimeout(() => {
  console.log('2'); // macrotask
}, 0);

Promise.resolve().then(() => {
  console.log('3'); // microtask
});

console.log('4'); // sync

// Output: 1, 4, 3, 2
// Explanation:
// 1. Sync code: 1, 4
// 2. Microtasks (Promise callbacks): 3
// 3. Macrotask (setTimeout): 2
```

---

### Q15: What are microtasks and macrotasks? How do they differ?

**Answer:**

Microtasks (Promise `.then`/`.catch`/`.finally`, MutationObserver, queueMicrotask) run immediately after the current script and before macrotasks. Macrotasks (setTimeout, setInterval, I/O, UI rendering, setImmediate) run in the next iteration of the event loop.

```js
console.log('start');

setTimeout(() => console.log('timeout'), 0); // macrotask

Promise.resolve().then(() => console.log('promise')); // microtask

queueMicrotask(() => console.log('microtask')); // microtask

console.log('end');

// Output: start, end, promise, microtask, timeout
// Order: sync -> microtasks (all) -> macrotask (one per iteration)
```

---

### Q16: Why does setTimeout(fn, 0) not execute immediately?

**Answer:**

`setTimeout(fn, 0)` is a macrotask. It is added to the task queue and runs only after the current call stack is empty **and** all microtasks are completed. Even with a 0ms delay, it must wait for the event loop to reach it.

```js
console.log('A');
setTimeout(() => console.log('B'), 0);
console.log('C');
// A, C, B

// More complex
setTimeout(() => console.log('B'), 0);
Promise.resolve().then(() => console.log('M1'));
Promise.resolve().then(() => {
  console.log('M2');
  Promise.resolve().then(() => console.log('M3'));
});
console.log('A');
// A, M1, M2, M3, B
```

---

### Q17: Explain the 4 rules for determining `this` in JavaScript.

**Answer:**

1. **Default binding**: In non-strict mode, `this` is the global object (`window`/`global`). In strict mode, `this` is `undefined`.
2. **Implicit binding**: When a function is called as a method of an object, `this` points to that object.
3. **Explicit binding**: `call`, `apply`, and `bind` explicitly set `this`.
4. **New binding**: When a function is used as a constructor with `new`, `this` points to the newly created instance.

```js
// 1. Default binding
function show() {
  console.log(this); // window (non-strict) / undefined (strict)
}
show();

// 2. Implicit binding
const obj = {
  name: 'Alice',
  greet() { console.log(this.name); }
};
obj.greet(); // 'Alice'

// 3. Explicit binding
function sayHi() { console.log(this.name); }
sayHi.call({ name: 'Bob' }); // 'Bob'
sayHi.apply({ name: 'Bob' }); // 'Bob'
const bound = sayHi.bind({ name: 'Bob' });
bound(); // 'Bob'

// 4. New binding
function Person(name) {
  this.name = name;
  console.log(this); // Person instance
}
new Person('Alice');
```

---

### Q18: How does `this` behave in arrow functions?

**Answer:**

Arrow functions do not have their own `this`. They capture the `this` from the enclosing lexical scope at definition time. They cannot be used as constructors, and `call`/`apply`/`bind` cannot override their `this`.

```js
const obj = {
  name: 'Alice',
  regular: function() {
    console.log(this.name); // 'Alice'
    const inner = function() {
      console.log(this.name); // undefined/global
    };
    inner();
  },
  arrow: function() {
    console.log(this.name); // 'Alice'
    const inner = () => {
      console.log(this.name); // 'Alice' (captured from arrow's scope)
    };
    inner();
  }
};

// Event handlers
button.addEventListener('click', function() {
  console.log(this); // button element
  setTimeout(() => {
    console.log(this); // button element (arrow captures this)
  }, 100);
});
```

---

### Q19: What is the difference between call, apply, and bind?

**Answer:**

`call` invokes a function with a given `this` and comma-separated arguments. `apply` is similar but takes arguments as an array. `bind` returns a new function with `this` bound (does not invoke).

```js
function greet(greeting, punctuation) {
  return `${greeting}, ${this.name}${punctuation}`;
}

const person = { name: 'Alice' };

// call
greet.call(person, 'Hello', '!'); // 'Hello, Alice!'

// apply
greet.apply(person, ['Hello', '!']); // 'Hello, Alice!'

// bind
const boundGreet = greet.bind(person);
boundGreet('Hi', '!'); // 'Hi, Alice!'
boundGreet('Hey', '.'); // 'Hey, Alice.'

// Partial application with bind
const greetHello = greet.bind(person, 'Hello');
greetHello('!'); // 'Hello, Alice!'

// Array min/max with apply
const nums = [5, 2, 8, 1];
Math.max.apply(null, nums); // 8
Math.max(...nums); // 8 (ES6 spread)
```

---

### Q20: What are the differences between arrow functions and regular functions?

**Answer:**

Arrow functions: no own `this` (lexical), no `arguments` object, cannot be used as constructors (no `new`), no `super`, no `prototype` property, cannot be generators. Arrow functions also cannot have duplicate named parameters.

```js
// this binding
const obj = {
  name: 'Alice',
  regular() { return this.name; },
  arrow: () => this.name // this is outer scope (global/undefined)
};

obj.regular(); // 'Alice'
obj.arrow();   // undefined (or '' in window)

// arguments object
function regular() { console.log(arguments); }
regular(1, 2, 3); // [1, 2, 3]

const arrow = () => { console.log(arguments); };
// ReferenceError: arguments is not defined

// Constructor
function Car(make) { this.make = make; }
new Car('Toyota'); // works

const Bike = () => {};
// new Bike(); // TypeError: Bike is not a constructor

// prototype
console.log(Car.prototype); // {constructor: f}
console.log(Bike.prototype); // undefined
```

---

### Q21: What is an IIFE (Immediately Invoked Function Expression)?

**Answer:**

An IIFE is a function expression that is defined and executed immediately. It creates a new scope to encapsulate variables and avoid polluting the global namespace.

```js
// Basic IIFE
(function() {
  const msg = 'Hello from IIFE';
  console.log(msg);
})();

// Arrow function IIFE
(() => {
  console.log('Arrow IIFE');
})();

// With parameters
((name) => {
  console.log(`Hello, ${name}`);
})('Alice');

// Module pattern with IIFE
const counter = (() => {
  let count = 0;
  return {
    increment() { return ++count; },
    decrement() { return --count; },
    getCount() { return count; }
  };
})();

// Classic: avoid global variable pollution
(function($) {
  // jQuery plugin code
  // $ is safe here
})(jQuery);
```

---

### Q22: What are first-class functions and higher-order functions?

**Answer:**

First-class functions means functions are treated as values — they can be assigned to variables, passed as arguments, and returned from other functions. Higher-order functions are functions that take other functions as arguments or return functions.

```js
// First-class: functions as values
const greet = function(name) { return `Hi ${name}`; };
const fn = greet; // assigned to variable

// Higher-order: function takes function as argument
function repeat(fn, n) {
  for (let i = 0; i < n; i++) fn();
}
repeat(() => console.log('Hello'), 3);

// Higher-order: function returns function
function multiplyBy(factor) {
  return function(num) {
    return num * factor;
  };
}
const double = multiplyBy(2);
const triple = multiplyBy(3);
console.log(double(5));  // 10
console.log(triple(5));  // 15

// Common HOFs
[1, 2, 3].map(x => x * 2);
[1, 2, 3].filter(x => x > 1);
[1, 2, 3].reduce((acc, x) => acc + x, 0);
```

---

### Q23: What is a pure function?

**Answer:**

A pure function always returns the same output for the same input and has no side effects (does not modify external state, file I/O, network requests, DOM manipulation, etc.).

```js
// Pure
function add(a, b) {
  return a + b;
}
add(2, 3); // always 5

// Pure - no mutation
function updateAge(person, newAge) {
  return { ...person, age: newAge };
}

// Impure - relies on external state
let taxRate = 0.1;
function calcPrice(price) {
  return price + price * taxRate; // depends on external variable
}

// Impure - side effect
function appendToLog(item) {
  log.push(item); // mutates external array
  return item;
}

// Impure - modifies input
function addProperty(obj) {
  obj.newProp = 'value'; // mutates original object
  return obj;
}
```

---

### Q24: Explain variable scoping with var, let, and const in loops.

**Answer:**

`var` in a loop creates a single function-scoped variable. `let` creates a new binding for each iteration, which is why closures work correctly with `let`.

```js
// var - single variable, shared
for (var i = 0; i < 3; i++) {
  setTimeout(() => console.log(i), 100);
}
// Output: 3, 3, 3

// let - new binding per iteration
for (let i = 0; i < 3; i++) {
  setTimeout(() => console.log(i), 100);
}
// Output: 0, 1, 2

// const in for...of (new binding per iteration)
const arr = ['a', 'b', 'c'];
for (const el of arr) {
  console.log(el); // a, b, c
}
```

---

### Q25: How do you handle default parameters in functions?

**Answer:**

ES6 introduced default parameter values. They are evaluated at call time and can reference previous parameters.

```js
// Basic defaults
function greet(name = 'Guest') {
  return `Hello, ${name}`;
}
greet();         // 'Hello, Guest'
greet('Alice');  // 'Hello, Alice'

// Multiple parameters
function createUser(name = 'User', role = 'viewer') {
  return { name, role };
}

// Default with destructuring
function fetchData({ url, method = 'GET', timeout = 3000 } = {}) {
  return { url, method, timeout };
}

// Only undefined triggers default
function test(x = 5) { return x; }
test(undefined); // 5
test(null);      // null (null is not undefined)
test(0);         // 0
test('');        // ''
```

---

### Q26: What is the difference between rest parameters and the arguments object?

**Answer:**

Rest parameters (`...args`) are a real array containing only the excess parameters. `arguments` is an array-like object (not a real array) containing all arguments, including named ones.

```js
function oldWay() {
  console.log(arguments); // array-like, not real array
  return Array.from(arguments).reduce((a, b) => a + b);
}

function newWay(...args) {
  console.log(args); // real array
  return args.reduce((a, b) => a + b);
}

console.log(oldWay(1, 2, 3)); // 6
console.log(newWay(1, 2, 3)); // 6

// Rest with named parameters
function log(level, ...messages) {
  console.log(`[${level}]`, ...messages);
}
log('INFO', 'User', 'logged', 'in'); // [INFO] User logged in
```

---

### Q27: How does the spread operator work? Give examples.

**Answer:**

The spread operator (`...`) expands iterables (arrays, strings, objects) into individual elements. It's used for copying, merging, and passing elements as arguments.

```js
// Array spread
const arr1 = [1, 2, 3];
const arr2 = [...arr1, 4, 5]; // [1, 2, 3, 4, 5]
const copy = [...arr1]; // shallow copy

// Combine arrays
const combined = [...arr1, ...arr2];

// Spread as function arguments
const nums = [4, 7, 1, 9];
Math.max(...nums); // 9

// String to array
const chars = [...'hello']; // ['h', 'e', 'l', 'l', 'o']

// Object spread (ES2018)
const obj1 = { a: 1, b: 2 };
const obj2 = { ...obj1, c: 3 }; // { a: 1, b: 2, c: 3 }
```

---

### Q28: What is destructuring? Show examples with objects and arrays.

**Answer:**

Destructuring is unpacking values from arrays or properties from objects into distinct variables.

```js
// Array destructuring
const [a, b] = [1, 2];
console.log(a, b); // 1, 2

// Skip elements
const [first, , third] = [10, 20, 30];
console.log(first, third); // 10, 30

// Default values
const [x = 1, y = 2] = [5];
console.log(x, y); // 5, 2

// Rest in destructuring
const [head, ...tail] = [1, 2, 3, 4];
console.log(head, tail); // 1, [2, 3, 4]

// Swapping variables
let p = 1, q = 2;
[p, q] = [q, p]; // swap

// Object destructuring
const user = { name: 'Alice', age: 30, city: 'NYC' };
const { name, age } = user;

// Renaming
const { name: userName, city: location } = user;

// Nested destructuring
const data = { user: { id: 1, address: { city: 'NYC' } } };
const { user: { address: { city } } } = data;

// Function parameter destructuring
function printUser({ name, age }) {
  console.log(`${name} is ${age} years old`);
}
```

---

### Q29: What is optional chaining (?.)?

**Answer:**

Optional chaining (`?.`) allows accessing nested properties safely without checking each level. If a reference is `null` or `undefined`, the expression short-circuits and returns `undefined`.

```js
const user = {
  name: 'Alice',
  address: null,
};

// Without optional chaining
const email = user && user.contact && user.contact.email;
// With optional chaining
const email2 = user?.contact?.email;

console.log(email);  // undefined
console.log(email2); // undefined

// Optional chaining with function calls
const result = user.getProfile?.();

// Dynamic properties
const key = 'name';
const value = user?.[key];
```

---

### Q30: What is nullish coalescing (??)?

**Answer:**

The nullish coalescing operator (`??`) returns the right operand only when the left operand is `null` or `undefined`. Unlike `||`, it does not treat `0`, `''`, or `false` as falsy.

```js
const a = 0;
const b = '';

const withOr = a || 'default';      // 'default' (0 is falsy)
const withNullish = a ?? 'default';  // 0 (0 is not null/undefined)

const withOr2 = b ?? 'default';     // ''
const withNullish2 = b ?? 'default'; // ''

// Use cases
function config(options = {}) {
  const timeout = options.timeout ?? 3000;
  const retries = options.retries ?? 3;
  const logLevel = options.logLevel ?? 'info';
  return { timeout, retries, logLevel };
}

config({ timeout: 0, retries: false });
// { timeout: 0, retries: false, logLevel: 'info' }
```

---

### Q31: What is the difference between shallow copy and deep copy?

**Answer:**

Shallow copy duplicates top-level properties; nested objects are still referenced. Deep copy creates completely independent copies of all nested structures.

```js
// Shallow copy methods
const original = { a: 1, b: { c: 2 } };
const shallow1 = { ...original };
const shallow2 = Object.assign({}, original);
shallow1.b.c = 99;
console.log(original.b.c); // 99 (shared reference)

// Deep copy methods
const deep1 = JSON.parse(JSON.stringify(original));
const deep2 = structuredClone(original);

// Recursive deep clone
function deepClone(obj) {
  if (obj === null || typeof obj !== 'object') return obj;
  if (obj instanceof Date) return new Date(obj);
  if (obj instanceof RegExp) return new RegExp(obj);
  if (obj instanceof Map) return new Map(deepClone([...obj]));
  if (obj instanceof Set) return new Set(deepClone([...obj]));
  if (Array.isArray(obj)) return obj.map(deepClone);
  return Object.fromEntries(
    Object.entries(obj).map(([k, v]) => [k, deepClone(v)])
  );
}
```

---

### Q32: What is the difference between for...in and for...of?

**Answer:**

`for...in` iterates over enumerable property keys (including inherited) of an object. `for...of` iterates over values of iterable objects (arrays, strings, maps, sets).

```js
const arr = ['a', 'b', 'c'];
arr.customProp = 'custom';

// for...in (keys, includes inherited)
for (const key in arr) {
  console.log(key); // '0', '1', '2', 'customProp'
}

// for...of (values, only iterables)
for (const val of arr) {
  console.log(val); // 'a', 'b', 'c'
}

// for...in on objects
const obj = { name: 'Alice', age: 30 };
for (const key in obj) {
  console.log(key, obj[key]); // name Alice, age 30
}

// for...of with Object methods
for (const [k, v] of Object.entries(obj)) {
  console.log(k, v);
}
```

---

### Q33: Explain strict mode vs non-strict mode.

**Answer:**

Strict mode (`'use strict'`) enforces stricter parsing and error handling: silent errors become throws, prevents accidental globals, prohibits `this` being the global object in functions, disallows duplicate parameters, and more.

```js
// Non-strict mode
function sloppy() {
  undeclaredVar = 42; // creates global variable
  console.log(this); // global object
}
sloppy();

// Strict mode
'use strict';
function strict() {
  console.log(this); // undefined
}
strict();

// Key differences:
// 1. No accidental globals
// 2. this is undefined in functions
// 3. No duplicate parameter names
// 4. No octal literals (use 0o prefix)
// 5. No 'with' statement
// 6. eval() creates own scope
// 7. delete of undeletable throws
```

---

### Q34: How does JavaScript handle garbage collection?

**Answer:**

JavaScript uses automatic garbage collection, primarily mark-and-sweep. The GC marks objects reachable from roots (global object, current execution context) and sweeps unmarked objects. V8 also uses generational GC with young/old generations.

```js
// Objects become eligible for GC when no references exist
let obj = { data: 'large' };
obj = null; // now eligible for GC

// Closures can prevent GC
function createHandler() {
  const element = document.getElementById('btn');
  const largeData = new Array(1000000);
  return function() {
    console.log('clicked');
    // largeData is kept alive by closure
  };
}

// WeakMap/WeakSet allow GC of keys
let key = { id: 1 };
const cache = new WeakMap();
cache.set(key, 'expensive data');
key = null; // key object can be GC'd
```

---

### Q35: What is the difference between synchronous and asynchronous code?

**Answer:**

Synchronous code executes sequentially, blocking until each operation completes. Asynchronous code allows non-blocking execution using callbacks, Promises, and async/await.

```js
// Synchronous
console.log('Start');
const result = heavyComputation(); // blocks
console.log('End');

// Asynchronous (Promise)
console.log('Start');
fetch('/api/data')
  .then(res => res.json())
  .then(data => console.log('Data:', data));
console.log('End');
// Output: Start, End, Data: ... (when fetch completes)

// Asynchronous (async/await)
async function load() {
  console.log('Start');
  const data = await fetch('/api/data');
  console.log('Data:', data);
  console.log('End');
}
```

---

### Q36: Explain tagged template literals.

**Answer:**

Tagged templates allow calling a function with a template literal. The function receives the string parts array and interpolated values.

```js
// Basic tagged template
function highlight(strings, ...values) {
  return strings.reduce((result, str, i) => {
    const val = values[i] ? `<strong>${values[i]}</strong>` : '';
    return result + str + val;
  }, '');
}

const name = 'Alice';
const role = 'developer';
const result = highlight`${name} is a ${role}`;
// '<strong>Alice</strong> is a <strong>developer</strong>'

// SQL escaping
function sql(strings, ...values) {
  const escaped = values.map(v =>
    typeof v === 'string' ? v.replace(/'/g, "''") : v
  );
  return strings.reduce((r, s, i) => r + s + (escaped[i] || ''), '');
}
```

---

### Q37: What are getters and setters in JavaScript?

**Answer:**

Getters and setters are special methods that allow computed properties with function behavior on access/assignment.

```js
// Class syntax
class Circle {
  constructor(radius) {
    this._radius = radius;
  }

  get area() {
    return Math.PI * this._radius ** 2;
  }

  set radius(value) {
    if (value <= 0) throw new Error('Radius must be positive');
    this._radius = value;
  }

  get radius() {
    return this._radius;
  }
}

const c = new Circle(5);
console.log(c.area); // 78.54
c.radius = 10;
console.log(c.area); // 314.16

// Object literal syntax
const person = {
  firstName: 'John',
  lastName: 'Doe',
  get fullName() {
    return `${this.firstName} ${this.lastName}`;
  },
  set fullName(name) {
    [this.firstName, this.lastName] = name.split(' ');
  }
};
```

---

### Q38: What are property descriptors?

**Answer:**

Property descriptors define the behavior of object properties: `value`, `writable`, `configurable`, `enumerable`, and `get`/`set` for accessor properties.

```js
const obj = {};

// Data descriptor
Object.defineProperty(obj, 'name', {
  value: 'Alice',
  writable: true,
  enumerable: true,
  configurable: true
});

// Accessor descriptor
Object.defineProperty(obj, 'greeting', {
  get() { return `Hello, ${this.name}`; },
  set(v) { this.name = v; },
  enumerable: true,
  configurable: false
});

// Describe properties
console.log(Object.getOwnPropertyDescriptor(obj, 'name'));

// Non-writable
Object.defineProperty(obj, 'constant', {
  value: 42,
  writable: false
});
obj.constant = 100; // fails silently / TypeError in strict
```

---

### Q39: What is the difference between shallow and deep comparison?

**Answer:**

Shallow comparison (=== for objects) checks if two references point to the same object. Deep comparison checks if all nested property values are equal.

```js
const a = { name: 'Alice' };
const b = { name: 'Alice' };
const c = a;

a === b; // false (different references)
a === c; // true (same reference)

// Deep equality
function deepEqual(a, b) {
  if (a === b) return true;
  if (a == null || b == null) return false;
  if (typeof a !== 'object' && typeof b !== 'object') return a === b;
  if (typeof a !== typeof b) return false;

  if (a instanceof Date) return a.getTime() === b.getTime();

  if (Array.isArray(a) && Array.isArray(b)) {
    if (a.length !== b.length) return false;
    return a.every((item, i) => deepEqual(item, b[i]));
  }

  if (Array.isArray(a) !== Array.isArray(b)) return false;
  const keysA = Object.keys(a);
  const keysB = Object.keys(b);
  if (keysA.length !== keysB.length) return false;
  return keysA.every(key => deepEqual(a[key], b[key]));
}
```

---

### Q40: Explain the concept of memoization.

**Answer:**

Memoization is an optimization technique that caches function results based on arguments, avoiding repeated computation for the same inputs.

```js
function memoize(fn) {
  const cache = new Map();
  return function(...args) {
    const key = JSON.stringify(args);
    if (cache.has(key)) {
      return cache.get(key);
    }
    const result = fn.apply(this, args);
    cache.set(key, result);
    return result;
  };
}

const expensiveCalc = memoize(function(n) {
  let total = 0;
  for (let i = 0; i < n; i++) total += i;
  return total;
});

expensiveCalc(10000000); // computes
expensiveCalc(10000000); // cache hit

// Memoized Fibonacci
const fib = memoize(function(n) {
  if (n <= 1) return n;
  return fib(n - 1) + fib(n - 2);
});
```

---

### Q41: What is NaN and how do you check for it?

**Answer:**

`NaN` (Not a Number) is a numeric value representing an invalid number. It's the only value not equal to itself. Use `Number.isNaN()` for robust checking.

```js
// Ways to get NaN
parseInt('hello');  // NaN
Math.sqrt(-1);      // NaN
undefined + 1;      // NaN
0 / 0;              // NaN

// NaN is not equal to itself
NaN === NaN;  // false

// Checking for NaN
isNaN(NaN);           // true - but coerces
isNaN('hello');       // true - coerces to NaN

Number.isNaN(NaN);    // true - no coercion
Number.isNaN('hello'); // false

// Object.is
Object.is(NaN, NaN);  // true

// Array methods
[NaN].includes(NaN);  // true (uses SameValueZero)
[NaN].indexOf(NaN);   // -1 (uses ===)
```

---

### Q42: How does Short-circuit evaluation work?

**Answer:**

Short-circuit evaluation stops evaluating logical expressions as soon as the result is determined. `&&` returns the first falsy value (or last truthy). `||` returns the first truthy value (or last falsy).

```js
// && - returns first falsy, else last
0 && 'hello';       // 0 (first falsy)
3 && 4;             // 4 (both truthy, returns last)

// || - returns first truthy, else last
0 || 'hello';       // 'hello'
false || true;      // true
'first' || 'second'; // 'first'

// ?? - nullish coalescing
0 ?? 'default';     // 0 (not null/undefined)
null ?? 'default';  // 'default'

// Practical
user && user.logout(); // conditional execution
const name = userInput || 'Guest'; // default
```

---

### Q43: What is the difference between function declaration and function expression?

**Answer:**

Function declarations are hoisted (can be called before definition). Function expressions are not hoisted. Declarations must have a name; expressions can be anonymous.

```js
// Function declaration - hoisted
hello(); // 'Hello!'
function hello() {
  console.log('Hello!');
}

// Function expression - not hoisted
// world(); // TypeError
var world = function() {
  console.log('World!');
};

// Named function expression
const factorial = function fac(n) {
  return n <= 1 ? 1 : n * fac(n);
};
```

---

### Q44: What is recursion and what are its use cases?

**Answer:**

Recursion is when a function calls itself. It must have a base case to terminate. Use cases: tree traversal, factorial, Fibonacci, directory walking, divide-and-conquer.

```js
// Factorial
function factorial(n) {
  if (n <= 1) return 1;
  return n * factorial(n - 1);
}

// Tree traversal
const tree = {
  value: 1,
  children: [
    { value: 2, children: [{ value: 4, children: [] }] },
    { value: 3, children: [{ value: 5, children: [] }] }
  ]
};

function traverseDFS(node) {
  console.log(node.value);
  node.children.forEach(traverseDFS);
}

// Deep flatten
function deepFlatten(arr) {
  return arr.reduce((acc, item) =>
    acc.concat(Array.isArray(item) ? deepFlatten(item) : item), []);
}

// Recursion with memoization
const fibMemo = (function() {
  const cache = { 0: 0, 1: 1 };
  return function fib(n) {
    if (cache[n] !== undefined) return cache[n];
    cache[n] = fib(n - 1) + fib(n - 2);
    return cache[n];
  };
})();
```

---

### Q45: What are the different ways to create objects in JavaScript?

**Answer:**

Objects can be created using object literals, constructors, `Object.create()`, ES6 classes, and factory functions.

```js
// 1. Object literal
const obj1 = { name: 'Alice' };

// 2. Constructor function
function Person(name) {
  this.name = name;
}
const obj2 = new Person('Bob');

// 3. ES6 Class
class Animal {
  constructor(type) { this.type = type; }
  speak() { console.log(`I'm a ${this.type}`); }
}
const obj3 = new Animal('Dog');

// 4. Object.create
const proto = { greet() { console.log('Hello'); } };
const obj4 = Object.create(proto);

// 5. Factory function
function createCar(make, model) {
  return { make, model, drive() { console.log('Driving...'); } };
}
const obj5 = createCar('Toyota', 'Camry');

// 6. Object.create(null) - no prototype
const obj6 = Object.create(null);
```

---

### Q46: How do you check if a property exists on an object?

**Answer:**

Use `in` operator (own and inherited), `hasOwnProperty` (own only), or `Object.hasOwn()` (modern).

```js
const obj = { name: 'Alice', age: undefined };
const proto = { inherited: true };
Object.setPrototypeOf(obj, proto);

// in operator
'name' in obj;        // true
'inherited' in obj;   // true (inherited)
'toString' in obj;    // true (from Object.prototype)

// hasOwnProperty - own only
obj.hasOwnProperty('name');       // true
obj.hasOwnProperty('inherited');  // false

// Object.hasOwn() - modern (ES2022)
Object.hasOwn(obj, 'name');       // true

// Direct access is ambiguous for undefined values
obj.nonexistent === undefined; // true
obj.age === undefined;         // true (but property exists!)
'age' in obj;                  // true (correct)
```

---

### Q47: What is the `delete` operator?

**Answer:**

`delete` removes a property from an object. Returns `true` if successful. Does not affect variables declared with `var`/`let`/`const`.

```js
const obj = { a: 1, b: 2, c: 3 };
delete obj.a;           // true
console.log(obj);       // { b: 2, c: 3 }

// Non-configurable properties
const obj2 = {};
Object.defineProperty(obj2, 'fixed', {
  value: 42,
  configurable: false
});
delete obj2.fixed; // false (non-strict) / TypeError (strict)

// Can't delete var/let/const
var x = 10;
delete x; // false

// Array delete leaves holes
const arr = [1, 2, 3];
delete arr[1]; // true
console.log(arr); // [1, empty, 3]
console.log(arr.length); // 3

// Use splice for arrays
arr.splice(1, 1); // [1, 3]
```

---

### Q48: How does `typeof` work and what are its limitations?

**Answer:**

`typeof` returns a string indicating the type. Main limitation: `typeof null === 'object'` (historical bug). Cannot distinguish between object types (arrays, dates all return `'object'`).

```js
typeof undefined;    // 'undefined'
typeof true;         // 'boolean'
typeof 42;           // 'number'
typeof 'hello';      // 'string'
typeof Symbol();     // 'symbol'
typeof 10n;          // 'bigint'
typeof function(){}; // 'function'

typeof null;         // 'object' (BUG!)
typeof [];           // 'object'
typeof {};           // 'object'
typeof new Date();   // 'object'

// Better type checks
Array.isArray([]);                                 // true
Object.prototype.toString.call([]);                // '[object Array]'
Object.prototype.toString.call(null);              // '[object Null]'

// typeof is safe for undeclared variables
typeof undeclaredVar; // 'undefined' (no ReferenceError)
```

---

### Q49: What is the difference between value and reference assignment?

**Answer:**

Primitives are assigned/passed by value (copy). Objects are assigned/passed by reference (both point to the same object).

```js
// Primitives: by value
let a = 5;
let b = a;
b = 10;
console.log(a); // 5 (unchanged)

// Objects: by reference
const obj1 = { value: 1 };
const obj2 = obj1;
obj2.value = 2;
console.log(obj1.value); // 2 (changed!)

// Function parameters
function mutate(x) {
  x.value = 99;
  x = null; // reassigning parameter doesn't affect original
}
const obj = { value: 1 };
mutate(obj);
console.log(obj.value); // 99
console.log(obj); // { value: 99 } (not null!)
```

---

### Q50: How does `Object.freeze()` differ from `Object.seal()`?

**Answer:**

`Object.freeze()` makes an object completely immutable (no add/remove/change). `Object.seal()` prevents adding/removing but allows changing existing writable properties.

```js
const frozen = Object.freeze({ name: 'Alice', age: 30 });
frozen.name = 'Bob';    // fails silently (strict: TypeError)
frozen.city = 'NYC';    // fails
delete frozen.age;       // fails

const sealed = Object.seal({ name: 'Alice', age: 30 });
sealed.name = 'Bob';    // works!
sealed.city = 'NYC';    // fails
delete sealed.age;       // fails

// Check
Object.isFrozen(frozen); // true
Object.isSealed(sealed); // true
```

---

### Q51: What is the comma operator?

**Answer:**

The comma operator evaluates both operands and returns the value of the second operand.

```js
const result = (1, 2, 3);
console.log(result); // 3

// In for loops
for (let i = 0, j = 10; i < j; i++, j--) {
  console.log(i, j);
}

// Side effects
let a = 1;
const b = (a++, a + 1);
console.log(a); // 2
console.log(b); // 3
```

---

### Q52: What are the ways to convert string to number?

**Answer:**

Options: `Number()`, `parseInt()`, `parseFloat()`, unary `+`, bitwise tricks.

```js
const str = '42';
const floatStr = '3.14';
const invalid = '42abc';

Number(str);          // 42
+str;                 // 42
parseInt(str, 10);    // 42
parseFloat(floatStr); // 3.14

// Edge cases
Number('');           // 0
parseInt('', 10);     // NaN
parseInt(invalid, 10); // 42 (stops at non-digit)
Number(invalid);      // NaN

// Radix
parseInt('0xFF', 16); // 255
parseInt('101', 2);   // 5

const n = +'42'; // 42
```

---

### Q53: What is the difference between `Number()` and `parseInt()`?

**Answer:**

`Number()` converts the entire string to a number, returning `NaN` for invalid strings. `parseInt()` parses from left to right and stops at the first non-digit.

```js
Number('42px');      // NaN
parseInt('42px', 10); // 42

Number('');          // 0
parseInt('', 10);    // NaN

Number(true);        // 1
parseInt(true, 10);  // NaN

Number(null);        // 0
parseInt(null, 10);  // NaN

Number('0xFF');      // 255
parseInt('0xFF', 16); // 255
```

---

### Q54: What is the difference between `substring`, `substr`, and `slice` for strings?

**Answer:**

`substring(start, end)` swaps if start > end, negative treated as 0. `substr(start, length)` deprecated. `slice(start, end)` supports negative indices, no swap.

```js
const str = 'Hello World';

// slice - supports negative indices
str.slice(0, 5);    // 'Hello'
str.slice(-5);      // 'World'
str.slice(-5, -2);  // 'Wor'

// substring - swaps if start > end
str.substring(0, 5);  // 'Hello'
str.substring(5, 0);  // 'Hello' (swapped)
str.substring(-3);    // 'Hello World' (negative becomes 0)

// substr (deprecated) - length parameter
str.substr(0, 5);   // 'Hello'
str.substr(-5);     // 'World'

// Use slice for consistency
```

---

### Q55: What is the difference between callback, Promise, and async/await?

**Answer:**

Callbacks are functions passed as arguments. Promises provide `.then()` chaining. `async/await` is syntactic sugar over Promises with synchronous-looking code.

```js
// Callback - callback hell
getUser(1, (user) => {
  getPosts(user.id, (posts) => {
    getComments(posts[0].id, (comments) => {
      console.log(comments);
    });
  });
});

// Promise - chaining
getUser(1)
  .then(user => getPosts(user.id))
  .then(posts => getComments(posts[0].id))
  .then(comments => console.log(comments))
  .catch(err => console.error(err));

// async/await - clean
async function displayComments() {
  try {
    const user = await getUser(1);
    const posts = await getPosts(user.id);
    const comments = await getComments(posts[0].id);
    console.log(comments);
  } catch (err) {
    console.error(err);
  }
}
```

---

### Q56: What is the purpose of `Symbol` in JavaScript?

**Answer:**

`Symbol` creates unique, immutable identifiers useful as object property keys to avoid name collisions. Used for constants, well-known symbols (Symbol.iterator, Symbol.hasInstance, etc.).

```js
// Unique values
const sym1 = Symbol('debug');
const sym2 = Symbol('debug');
sym1 === sym2; // false

// Symbol as property key
const id = Symbol('id');
const user = { name: 'Alice', [id]: 123 };
user[id]; // 123
Object.keys(user); // ['name'] - symbols hidden

// Symbol.iterator - make objects iterable
const range = {
  start: 1, end: 5,
  [Symbol.iterator]() {
    let current = this.start;
    return {
      next: () => ({
        value: current,
        done: current++ > this.end
      })
    };
  }
};
console.log([...range]); // [1, 2, 3, 4, 5]

// Symbol.for - global registry
const globalSym1 = Symbol.for('shared');
const globalSym2 = Symbol.for('shared');
globalSym1 === globalSym2; // true
```

---

### Q57: What is the difference between `Map` and `Object`?

**Answer:**

Map preserves insertion order, accepts any key type (objects, functions, primitives), has `size` property, and better performance for frequent add/delete. Objects have string/Symbol keys only.

```js
// Map - any key type
const map = new Map();
const objKey = { id: 1 };
map.set(objKey, 'value');
map.set(42, 'number');
map.set(true, 'boolean');
map.size; // 3

// Object - string/Symbol keys
const obj = { 42: 'number', true: 'boolean' };

// Map iteration preserves order
const orderedMap = new Map();
orderedMap.set('a', 1);
orderedMap.set('b', 2);
for (const [k, v] of orderedMap) console.log(k, v); // a, b

// Map performance: O(1) for add/delete/has
// Object has prototype chain issues
const obj2 = { toString: 'test' };
console.log(obj2.toString); // 'test' (shadowed)
```

---

### Q58: What is the difference between `Set`, `WeakSet`, `Map`, and `WeakMap`?

**Answer:**

`Set`: unique values, any type, iterable, has `size`. `WeakSet`: objects only, weak refs, no iteration. `Map`: key-value any types, iterable, has `size`. `WeakMap`: object keys only, weak refs, no iteration.

```js
// Set
const set = new Set([1, 2, 2, 3, 3]);
console.log([...set]); // [1, 2, 3]
set.has(1); // true
set.size; // 3

// WeakSet - objects only, weak references
let obj = { id: 1 };
const weakSet = new WeakSet();
weakSet.add(obj);
obj = null; // obj can be GC'd, entry auto-removed

// Map
const map = new Map();
map.set('key', 'value');
map.set({}, 'object key');
map.size; // 2

// WeakMap - object keys only, weak references
let key = { data: 'sensitive' };
const weakMap = new WeakMap();
weakMap.set(key, 'private data');
key = null; // entry auto-removed by GC
```

---

### Q59: What is the difference between enumerable and non-enumerable properties?

**Answer:**

Enumerable properties appear in `for...in` and `Object.keys()`. Non-enumerable are hidden from enumeration but still accessible.

```js
const obj = {};
Object.defineProperty(obj, 'visible', {
  value: 'yes', enumerable: true
});
Object.defineProperty(obj, 'hidden', {
  value: 'secret', enumerable: false
});

Object.keys(obj); // ['visible']
for (const key in obj) console.log(key); // 'visible'

// Both accessible
console.log(obj.visible); // 'yes'
console.log(obj.hidden);  // 'secret'

// Get ALL own properties
Object.getOwnPropertyNames(obj); // ['visible', 'hidden']
```

---

### Q60: What are the different ways to create strings in JavaScript?

**Answer:**

Strings can be created using single quotes, double quotes, template literals (backticks), and the `String` constructor.

```js
const single = 'Hello';
const double = "Hello";
const template = `Hello`;

// Template literals - interpolation
const name = 'Alice';
const greeting = `Hello, ${name}!`; // 'Hello, Alice!'

// Multiline
const multiline = `
  Line 1
  Line 2
`;

// String constructor
const strObj = new String('Hello');
typeof strObj; // 'object'

// String.fromCharCode
String.fromCharCode(65, 66, 67); // 'ABC'
```

---

### Q61: How do template literals work?

**Answer:**

Template literals (backticks) support string interpolation with `${expression}`, multiline strings, and tagged templates.

```js
// Interpolation
const name = 'Alice';
const age = 30;
const msg = `Name: ${name}, Age: ${age}`;

// Expressions
const price = 10;
const tax = 0.08;
`Total: $${(price * (1 + tax)).toFixed(2)}`;

// Multiline
const html = `
  <div>
    <h1>Title</h1>
  </div>
`;

// Function calls inside
const greet = () => 'Hello';
`${greet()} World`; // 'Hello World'

// Nested templates
const items = ['apple', 'banana'];
const list = `
  <ul>
    ${items.map(item => `<li>${item}</li>`).join('')}
  </ul>
`;
```

---

### Q62: What is the difference between `null` and `undefined`?

**Answer:**

`null` is an intentional absence of value. `undefined` means declared but not assigned. They are loosely equal but strictly different.

```js
// undefined
let a;
console.log(a); // undefined
function test() { }
console.log(test()); // undefined
const obj = {};
console.log(obj.nonExistent); // undefined

// null - intentional empty value
const b = null;

// Comparisons
null == undefined;  // true
null === undefined; // false

typeof null;       // 'object' (bug)
typeof undefined;  // 'undefined'

// Defaults
function greet(name) {
  name = name ?? 'Guest'; // treat null/undefined same
  return `Hello, ${name}`;
}
```

---

### Q63: What is the difference between `Object.freeze()` and `const`?

**Answer:**

`const` prevents reassignment of the variable binding. `Object.freeze()` makes the object itself immutable (properties cannot be changed). A `const` object's properties can still be mutated unless frozen.

```js
const obj = { name: 'Alice' };
obj = { name: 'Bob' }; // TypeError: reassignment

obj.name = 'Bob'; // works! (mutation)
console.log(obj.name); // 'Bob'

// Frozen
const frozen = Object.freeze({ name: 'Alice' });
frozen.name = 'Bob'; // fails silently/strict TypeError

// Combining
const frozenObj = Object.freeze({ name: 'Alice' });
// frozenObj reassignment: TypeError
// frozenObj.name mutation: fails
```

---

### Q64: What is the difference between assignment (`=`), `==`, and `===`?

**Answer:**

`=` assigns a value. `==` compares values with type coercion. `===` compares values without coercion (strict equality).

```js
// = assignment
let x = 5;

// == comparison (with coercion)
5 == '5';       // true
0 == false;     // true
null == undefined; // true

// === comparison (no coercion)
5 === '5';      // false
0 === false;    // false
null === undefined; // false

// Best practice: use === almost always
// Use == only when you explicitly want coercion (rare)
```

---

### Q65: How do you handle default values in different scenarios?

**Answer:**

Use default parameters (functions), `||` (falsy default), `??` (nullish default), destructuring defaults.

```js
// Function default parameters
function greet(name = 'Guest') {
  return `Hello, ${name}`;
}

// || - all falsy trigger default
const name = userInput || 'Guest';
// Problem: '', 0, false all trigger default

// ?? - only null/undefined trigger default
const name2 = userInput ?? 'Guest';
// '' stays '', 0 stays 0

// Destructuring defaults
function config({ timeout = 3000, retries = 3 } = {}) {
  return { timeout, retries };
}

// Logical assignment (ES2021)
let count = null;
count ??= 0; // nullish assignment

let retries = 5;
retries ||= 3; // falsy assignment
```

---

### Q66: What are the different patterns to avoid callback hell?

**Answer:**

Use Promises, async/await, modularization, and control flow libraries.

```js
// Callback hell
getUser(1, (err, user) => {
  if (err) handleError(err);
  getPosts(user.id, (err, posts) => {
    if (err) handleError(err);
    getComments(posts[0].id, (err, comments) => {
      if (err) handleError(err);
      console.log(comments);
    });
  });
});

// Promise chain
getUser(1)
  .then(user => getPosts(user.id))
  .then(posts => getComments(posts[0].id))
  .then(comments => console.log(comments))
  .catch(err => handleError(err));

// async/await
async function getData() {
  try {
    const user = await getUser(1);
    const posts = await getPosts(user.id);
    const comments = await getComments(posts[0].id);
    console.log(comments);
  } catch (err) {
    handleError(err);
  }
}

// Modularization - break into named functions
function handleError(err) { console.error(err); }

function onUser(user) {
  return getPosts(user.id).then(onPosts);
}

function onPosts(posts) {
  return getComments(posts[0].id).then(console.log);
}

getUser(1).then(onUser).catch(handleError);
```

---

### Q67: How does the event loop work with the call stack?

**Answer:**

The event loop continuously checks if the call stack is empty. If empty, it processes all microtasks (Promise callbacks, queueMicrotask), then picks one macrotask (setTimeout, I/O) and executes it.

```js
console.log('1: Sync');

setTimeout(() => {
  console.log('2: Macrotask');
}, 0);

Promise.resolve().then(() => {
  console.log('3: Microtask');
});

queueMicrotask(() => {
  console.log('4: Microtask 2');
});

// 1: Sync
// 3: Microtask
// 4: Microtask 2
// 2: Macrotask

// Microtasks can starve macrotasks
function loop() {
  Promise.resolve().then(loop); // infinite microtasks
}
```

---

### Q68: What is the difference between `Object.preventExtensions()`, `Object.seal()`, and `Object.freeze()`?

**Answer:**

| Method | Add | Delete | Change | Config |
|--------|-----|--------|--------|--------|
| `preventExtensions` | No | Yes | Yes | Yes |
| `seal` | No | No | Yes | No |
| `freeze` | No | No | No | No |

```js
const p = Object.preventExtensions({ a: 1 });
p.b = 2; // fails
p.a = 2; // works

const s = Object.seal({ a: 1 });
s.a = 2; // works (writable still true)
delete s.a; // fails

const f = Object.freeze({ a: 1 });
f.a = 2; // fails
delete f.a; // fails

// Check
Object.isExtensible(p); // false
Object.isSealed(s);     // true
Object.isFrozen(f);     // true
```

---

### Q69: What is the difference between `for...in` and `Object.keys()`?

**Answer:**

`for...in` iterates over enumerable keys including inherited properties. `Object.keys()` returns own enumerable keys only.

```js
const parent = { inherited: true };
const child = Object.create(parent);
child.own = 'yes';

for (const key in child) {
  console.log(key); // 'own', 'inherited'
}

Object.keys(child); // ['own'] (own only)

// Safe for...in with hasOwnProperty
for (const key in child) {
  if (child.hasOwnProperty(key)) {
    console.log(key); // 'own'
  }
}
```

---

### Q70: How do you handle errors in JavaScript?

**Answer:**

Use `try/catch/finally` for synchronous code, `.catch()` for Promises, `try/catch` with async/await, and global error handlers.

```js
// try/catch
try {
  const result = riskyOperation();
  console.log(result);
} catch (error) {
  console.error('Error:', error.message);
} finally {
  console.log('Always runs');
}

// Promise .catch
fetch('/api/data')
  .then(res => res.json())
  .catch(err => console.error('Fetch error:', err));

// async/await
async function getData() {
  try {
    const res = await fetch('/api/data');
    const data = await res.json();
    return data;
  } catch (err) {
    console.error('Failed:', err);
    throw err; // re-throw if needed
  }
}

// Global handler
window.onerror = function(msg, url, line) {
  console.error('Global error:', msg);
  return true; // prevent default browser handling
};

// Unhandled promise rejection
window.onunhandledrejection = function(event) {
  console.error('Unhandled rejection:', event.reason);
};
```

---

# PHASE 2: OBJECTS & PROTOTYPES (Q71–Q130)

---

### Q71: What is prototypal inheritance?

**Answer:**

Prototypal inheritance is JavaScript's mechanism where objects inherit properties from other objects through the prototype chain.

```js
const animal = {
  eat() { console.log('Eating...'); },
  sleep() { console.log('Sleeping...'); }
};

const dog = Object.create(animal);
dog.bark = function() { console.log('Woof!'); };

dog.bark();  // 'Woof!' (own)
dog.eat();   // 'Eating...' (inherited from animal)
dog.sleep(); // 'Sleeping...' (inherited)

// Prototype chain
Object.getPrototypeOf(dog) === animal; // true
Object.getPrototypeOf(animal) === Object.prototype; // true
Object.getPrototypeOf(Object.prototype); // null

// Property shadowing
dog.eat = function() { console.log('Dog eating...'); };
dog.eat(); // 'Dog eating...' (own shadows inherited)
```

---

### Q72: What is the difference between `__proto__` and `prototype`?

**Answer:**

`__proto__` is the actual prototype of an instance (the `[[Prototype]]`). `prototype` is a property on constructor functions that becomes the `__proto__` of instances.

```js
function Person(name) {
  this.name = name;
}
Person.prototype.greet = function() {
  console.log(`Hi, I'm ${this.name}`);
};

const alice = new Person('Alice');

// __proto__ (instance's prototype)
alice.__proto__ === Person.prototype; // true
alice.__proto__ === Object.getPrototypeOf(alice); // true

// prototype (constructor's property)
Person.prototype === alice.__proto__; // true
Person.prototype.constructor === Person; // true

// Object.create
const proto = { method() {} };
const obj = Object.create(proto);
obj.__proto__ === proto; // true

// Classes
class Animal {}
class Dog extends Animal {}
Dog.__proto__ === Animal; // true (extends)
Dog.prototype.__proto__ === Animal.prototype; // true

// Arrow functions have no prototype
const arrow = () => {};
console.log(arrow.prototype); // undefined
```

---

### Q73: How does the prototype chain work?

**Answer:**

When accessing a property, JS first checks own properties. If not found, it traverses the `[[Prototype]]` chain until found or until `null`.

```js
const grandparent = { a: 1 };
const parent = Object.create(grandparent);
parent.b = 2;
const child = Object.create(parent);
child.c = 3;

console.log(child.c); // 3 (own)
console.log(child.b); // 2 (from parent)
console.log(child.a); // 1 (from grandparent)
console.log(child.toString); // function (from Object.prototype)
console.log(child.nonexistent); // undefined (chain ends at null)

// Chain: child -> parent -> grandparent -> Object.prototype -> null

// Shadowing
parent.a = 99;
console.log(child.a); // 99 (found on parent before grandparent)

// hasOwnProperty
child.hasOwnProperty('c'); // true
child.hasOwnProperty('b'); // false (inherited)
```

---

### Q74: How do ES6 classes work under the hood?

**Answer:**

ES6 classes are syntactic sugar over constructor functions + prototype. Methods are added to `ClassName.prototype`. Static methods are on the constructor itself.

```js
// ES6 class
class Person {
  constructor(name) {
    this.name = name;
  }
  greet() {
    console.log(`Hi, I'm ${this.name}`);
  }
  static create(name) {
    return new Person(name);
  }
}

// Desugared (approximately)
function Person(name) {
  this.name = name;
}
Person.prototype.greet = function() {
  console.log(`Hi, I'm ${this.name}`);
};
Person.create = function(name) {
  return new Person(name);
};

const alice = new Person('Alice');
alice.greet(); // 'Hi, I'm Alice'
alice.__proto__ === Person.prototype; // true

// Class methods are non-enumerable
Object.keys(Person.prototype); // []
```

---

### Q75: How does `extends` and `super` work?

**Answer:**

`extends` sets up prototype inheritance between classes. `super()` calls the parent constructor. `super.method()` calls parent methods.

```js
class Animal {
  constructor(name) {
    this.name = name;
  }
  speak() {
    console.log(`${this.name} makes a sound`);
  }
  static classify() {
    return 'Animal';
  }
}

class Dog extends Animal {
  constructor(name, breed) {
    super(name); // must call super before using this
    this.breed = breed;
  }
  speak() {
    super.speak(); // call parent method
    console.log(`${this.name} barks`);
  }
  static classify() {
    return `${super.classify()} > Dog`;
  }
}

const dog = new Dog('Rex', 'Lab');
dog.speak();
// 'Rex makes a sound'
// 'Rex barks'
console.log(Dog.classify()); // 'Animal > Dog'

// Inherited statics
Dog.__proto__ === Animal; // true (static inheritance)
```

---

### Q76: How does the `new` keyword work?

**Answer:**

`new` creates a new object, links its prototype, executes the constructor with `this` bound, and returns the object.

```js
function Person(name) {
  // 1. Creates {} (empty object)
  // 2. Links __proto__ to Person.prototype
  // 3. this = new object
  // 4. Executes body: this.name = name
  // 5. Returns this (implicitly)
  this.name = name;
}

// Manual implementation
function _new(constructor, ...args) {
  const obj = Object.create(constructor.prototype);
  const result = constructor.apply(obj, args);
  return (typeof result === 'object' && result !== null) ? result : obj;
}

const alice = _new(Person, 'Alice');
alice instanceof Person; // true
alice.name; // 'Alice'

// If constructor returns object, that's used instead
function ReturnsObject() {
  return { custom: 'object' };
}
const r = new ReturnsObject();
r instanceof ReturnsObject; // false
r.custom; // 'object'
```

---

### Q77: Factory vs Constructor vs Class?

**Answer:**

Factory functions return an object without `new`. Constructor functions use `new`. Classes are syntactic sugar over constructors.

```js
// Factory function
function createPerson(name, age) {
  const _private = 'secret'; // truly private
  return {
    name,
    age,
    greet() { console.log(`Hi, I'm ${this.name}`); }
  };
}
const p1 = createPerson('Alice', 30);

// Constructor function
function Person(name, age) {
  this.name = name;
  this.age = age;
}
Person.prototype.greet = function() {
  console.log(`Hi, I'm ${this.name}`);
};
const p2 = new Person('Bob', 25);

// Class
class PersonClass {
  constructor(name, age) {
    this.name = name;
    this.age = age;
  }
  greet() { console.log(`Hi, I'm ${this.name}`); }
}
const p3 = new PersonClass('Charlie', 35);

// Factory advantages: private variables via closure, no 'new' needed
function createCounter(initial = 0) {
  let count = initial;
  return {
    increment() { return ++count; },
    decrement() { return --count; },
    getCount() { return count; }
  };
}
```

---

### Q78: How does `Object.create()` work?

**Answer:**

`Object.create(proto, propertiesObject)` creates a new object with the specified prototype and optional property descriptors.

```js
const animal = { eat() { console.log('Eating'); } };

const dog = Object.create(animal);
dog.bark = function() { console.log('Woof'); };
dog.eat(); // 'Eating' (inherited)

// With property descriptors
const obj = Object.create(animal, {
  name: {
    value: 'Rex',
    writable: true,
    enumerable: true,
    configurable: true
  }
});

// Object with no prototype
const pure = Object.create(null);
pure.key = 'value';
// pure.toString(); // TypeError

// Polyfill
function objectCreate(proto) {
  function F() {}
  F.prototype = proto;
  return new F();
}
```

---

### Q79: What is the difference between `Object.assign()` and spread operator?

**Answer:**

Both do shallow copy. `Object.assign` triggers setters on target; spread doesn't. Both copy own enumerable properties.

```js
const obj1 = { a: 1, b: { c: 2 } };

// Object.assign
const merged1 = Object.assign({}, obj1, { d: 3 });

// Spread (ES2018)
const merged2 = { ...obj1, d: 3 };

// Difference: setters
const target = {};
Object.defineProperty(target, 'a', {
  set(v) { console.log('Setter:', v); }
});
Object.assign(target, { a: 5 }); // logs setter
const spreadResult = { ...target }; // no setters

// Object.assign returns target
let t = {};
const r = Object.assign(t, { a: 1 });
r === t; // true

// assign copies getter values
const source = { get a() { return 1; } };
Object.assign({}, source); // { a: 1 }
```

---

### Q80: How do you make an object immutable?

**Answer:**

`Object.freeze()` for shallow immutability. Deep freeze for nested. Proxy for full control.

```js
// Shallow freeze
const obj = { a: 1, b: { c: 2 } };
Object.freeze(obj);
obj.a = 42; // fails silently (TypeError in strict)
obj.b.c = 42; // works! (nested not frozen)

// Deep freeze
function deepFreeze(obj) {
  Object.values(obj).forEach(v => {
    if (v && typeof v === 'object') deepFreeze(v);
  });
  return Object.freeze(obj);
}

// Proxy for true immutability
const immutable = new Proxy(obj, {
  set() { throw new Error('Immutable'); },
  deleteProperty() { throw new Error('Immutable'); },
  defineProperty() { throw new Error('Immutable'); }
});
```

---

### Q81: What are property descriptors and how do you use them?

**Answer:**

Property descriptors define metadata: `value`, `writable`, `enumerable`, `configurable` (data) or `get`/`set` (accessor).

```js
const obj = {};

// Data descriptor
Object.defineProperty(obj, 'name', {
  value: 'Alice',
  writable: true,
  enumerable: true,
  configurable: true
});

// Accessor descriptor
Object.defineProperty(obj, 'greeting', {
  get() { return `Hello, ${this.name}`; },
  set(v) { this.name = v; },
  enumerable: true,
  configurable: false
});

// Multiple properties
Object.defineProperties(obj, {
  _age: { value: 30, writable: true },
  age: {
    get() { return this._age; },
    set(v) { if (v > 0) this._age = v; },
    enumerable: true
  }
});

// Reading descriptors
Object.getOwnPropertyDescriptor(obj, 'name');

// Clone with descriptors
const clone = Object.defineProperties({},
  Object.getOwnPropertyDescriptors(obj)
);
```

---

### Q82: How do you implement getters and setters?

**Answer:**

Getters/setters can be in classes, object literals, or via `Object.defineProperty`. They allow computed properties and validation.

```js
// Object literal
const person = {
  _name: 'Alice',
  get name() { return this._name; },
  set name(v) {
    if (!v) throw new Error('Name required');
    this._name = v;
  }
};

// Class
class Circle {
  #radius;
  constructor(radius) { this.#radius = radius; }
  get radius() { return this.#radius; }
  set radius(v) {
    if (v <= 0) throw new Error('Invalid radius');
    this.#radius = v;
  }
  get area() { return Math.PI * this.#radius ** 2; }
}

// Object.defineProperty
const obj = {};
Object.defineProperty(obj, 'computed', {
  get() { return this._value * 2; },
  set(v) { this._value = v; }
});

// Lazy initialization via getter
class LazyLoader {
  get data() {
    delete this.data;
    this.data = this.loadData();
    return this.data;
  }
  loadData() {
    console.log('Loading...');
    return { important: 'data' };
  }
}
```

---

### Q83: What is the difference between data and accessor properties?

**Answer:**

Data properties store a value directly (using `value` descriptor). Accessor properties define `get`/`set` functions. A property can be one or the other, not both.

```js
// Data property
const data = {};
Object.defineProperty(data, 'prop', {
  value: 42,
  writable: true,
  enumerable: true,
  configurable: true
});

// Accessor property
const accessor = {};
Object.defineProperty(accessor, 'prop', {
  get() { return this._value; },
  set(v) { this._value = v; },
  enumerable: true,
  configurable: true
});

// Cannot mix
// Object.defineProperty({}, 'bad', {
//   value: 1,
//   get() {} // TypeError
// });

// Object literal syntax
const mix = {
  dataProp: 42,
  get accessorProp() { return this._value; },
  set accessorProp(v) { this._value = v; }
};
```

---

### Q84: How do you iterate over an object's properties?

**Answer:**

Options: `for...in`, `Object.keys()`, `Object.getOwnPropertyNames()`, `Reflect.ownKeys()`, `Object.values()`, `Object.entries()`.

```js
const symbolKey = Symbol('secret');
const obj = { a: 1, b: 2 };
Object.defineProperty(obj, 'c', { value: 3, enumerable: false });
obj[symbolKey] = 'hidden';

// for...in - own + inherited enumerable
for (const key in obj) {
  if (obj.hasOwnProperty(key)) console.log(key); // 'a', 'b'
}

// Object.keys - own enumerable
Object.keys(obj); // ['a', 'b']

// Object.getOwnPropertyNames - all own (non-enumerable too)
Object.getOwnPropertyNames(obj); // ['a', 'b', 'c']

// Reflect.ownKeys - all own including Symbol
Reflect.ownKeys(obj); // ['a', 'b', 'c', Symbol(secret)]

// Object.values
Object.values(obj); // [1, 2]

// Object.entries
Object.entries(obj); // [['a', 1], ['b', 2]]
```

---

### Q85: What is the difference between `in` and `hasOwnProperty`?

**Answer:**

`in` checks prototype chain. `hasOwnProperty` checks own only. `Object.hasOwn()` is the modern safe version.

```js
const parent = { inherited: true };
const child = Object.create(parent);
child.own = 'yes';

'inherited' in child; // true (inherited)
child.hasOwnProperty('inherited'); // false
Object.hasOwn(child, 'inherited'); // false

'own' in child; // true
child.hasOwnProperty('own'); // true

'toString' in child; // true (from Object.prototype)
child.hasOwnProperty('toString'); // false

// hasOwnProperty safety issue
const noProto = Object.create(null);
noProto.prop = 'value';
// noProto.hasOwnProperty('prop'); // TypeError
Object.hasOwn(noProto, 'prop'); // true (safe)
Object.prototype.hasOwnProperty.call(noProto, 'prop'); // true
```

---

### Q86: What are `Object.keys()`, `values()`, and `entries()`?

**Answer:**

`keys()` returns property names. `values()` returns values. `entries()` returns `[key, value]` pairs. All return own enumerable properties only.

```js
const obj = { a: 1, b: 2, c: 3 };

Object.keys(obj);    // ['a', 'b', 'c']
Object.values(obj);  // [1, 2, 3]
Object.entries(obj); // [['a', 1], ['b', 2], ['c', 3]]

// Create Map from object
const map = new Map(Object.entries(obj));

// Transform
Object.fromEntries(
  Object.entries(obj).map(([k, v]) => [k, v * 2])
); // { a: 2, b: 4, c: 6 }

// Filter
Object.fromEntries(
  Object.entries(obj).filter(([k]) => k !== 'a')
); // { b: 2, c: 3 }

// Sum values
Object.values(obj).reduce((acc, v) => acc + v, 0); // 6
```

---

### Q87: How does `Object.fromEntries()` work?

**Answer:**

`Object.fromEntries()` transforms `[key, value]` pairs into an object. It's the inverse of `Object.entries()`.

```js
// Basic
const entries = [['a', 1], ['b', 2], ['c', 3]];
const obj = Object.fromEntries(entries);
// { a: 1, b: 2, c: 3 }

// Reverse Object.entries
const original = { x: 10, y: 20 };
const back = Object.fromEntries(Object.entries(original));

// From Map
const map = new Map([['name', 'Alice'], ['age', 30]]);
Object.fromEntries(map); // { name: 'Alice', age: 30 }

// Filter/transform
const prices = { apple: 1.5, banana: 0.5 };
const discounted = Object.fromEntries(
  Object.entries(prices).map(([item, price]) => [item, price * 0.9])
);

// From any iterable
function* pairs() {
  yield ['a', 1];
  yield ['b', 2];
}
Object.fromEntries(pairs()); // { a: 1, b: 2 }
```

---

### Q88: `Object.assign()` vs `Object.create()`?

**Answer:**

`Object.assign` copies properties from sources to target (mutates). `Object.create` creates a new object with a specified prototype.

```js
const proto = { greet() { console.log('Hi'); } };
const source = { a: 1, b: 2 };

// Object.create - sets prototype
const obj1 = Object.create(proto, {
  a: { value: 1, enumerable: true },
  b: { value: 2, enumerable: true }
});
obj1.greet(); // 'Hi' (inherited)

// Object.assign - copies properties
const obj2 = Object.assign({}, source);
obj2.greet(); // TypeError (no greet)

// Object.create for inheritance
const child = Object.create(parent);

// Object.assign for merging
const merged = Object.assign({}, defaults, overrides);
```

---

### Q89: How do you implement Mixins?

**Answer:**

Mixins combine properties from multiple sources using `Object.assign` or class composition with extends.

```js
// Object mixin
const canEat = {
  eat() { console.log(`${this.name} eating`); }
};
const canSleep = {
  sleep() { console.log(`${this.name} sleeping`); }
};

const duck = Object.assign({ name: 'Duck' }, canEat, canSleep);
duck.eat();  // 'Duck eating'

// Class mixin pattern
const FlyMixin = (Base) => class extends Base {
  fly() { console.log(`${this.name} flying`); }
};

class Bird {
  constructor(name) { this.name = name; }
}

class SuperDuck extends FlyMixin(Bird) {}
const superDuck = new SuperDuck('Super Duck');
superDuck.fly(); // 'Super Duck flying'

// Composition over inheritance
function createPerson(name) {
  return { name };
}
function withGreeting(person) {
  person.greet = () => console.log(`Hi, I'm ${person.name}`);
  return person;
}
```

---

### Q90: How does JavaScript property lookup work?

**Answer:**

JavaScript checks own properties first, then walks the prototype chain. It returns the first found or `undefined` if chain ends.

```js
const grandparent = { a: 1 };
const parent = Object.create(grandparent);
parent.b = 2;
const child = Object.create(parent);
child.c = 3;

// Lookup for child.a:
// 1. child own -> not found
// 2. parent own -> not found
// 3. grandparent own -> found! returns 1

// Setting always goes to own properties
child.a = 99;
console.log(child.a); // 99 (own)
console.log(grandparent.a); // 1 (unchanged)

// Accessor properties on prototype
const proto = {
  _name: 'Proto',
  get name() { return this._name; },
  set name(v) { this._name = v; }
};
const instance = Object.create(proto);
instance.name = 'Instance'; // Uses prototype setter
console.log(instance.name); // 'Instance' (uses getter)
```

---

### Q91: How do you create private properties?

**Answer:**

Use `#` private fields (ES2021), closures, WeakMap, or Symbol convention.

```js
// Class private fields (ES2021+)
class Person {
  #name;
  #age;

  constructor(name, age) {
    this.#name = name;
    this.#age = age;
  }

  #privateMethod() { return 'Private'; }

  greet() { return `Hi, I'm ${this.#name}`; }
}
const p = new Person('Alice', 30);
// p.#name; // SyntaxError

// WeakMap approach
const _private = new WeakMap();
class Person2 {
  constructor(name) {
    _private.set(this, { name });
  }
  getName() { return _private.get(this).name; }
}

// Closure approach
function createPerson(name) {
  const _name = name;
  return {
    greet() { console.log(`Hi, I'm ${_name}`); }
  };
}

// Symbol approach (discoverable)
const _name = Symbol('name');
class Person3 {
  constructor(name) { this[_name] = name; }
}
```

---

### Q92: What is the difference between `Map` and `WeakMap`?

**Answer:**

`WeakMap` keys must be objects, hold weak references (don't prevent GC). Not iterable, no `size`, no `clear()`. Map has all features.

```js
// WeakMap - private data, caching
let obj = { id: 1 };
const wm = new WeakMap();
wm.set(obj, 'private data');
obj = null; // entry auto-removed when obj is GC'd

// Map - iteration, any keys, size
const m = new Map([['key', 'value'], [42, 'number']]);
m.size; // 2
for (const [k, v] of m) console.log(k, v);

// Memory leak with Map
const mapCache = new Map();
function processElement(el) {
  const result = { data: 'expensive' };
  mapCache.set(el, result); // prevents GC of el!
  return result;
}

// Safe with WeakMap
const weakCache = new WeakMap();
function processElement(el) {
  const result = { data: 'expensive' };
  weakCache.set(el, result); // GC can collect when el goes away
  return result;
}
```

---

### Q93: What is the difference between `Set` and `WeakSet`?

**Answer:**

`Set` stores unique values (any type), iterable, has `size`. `WeakSet` stores only objects, weak references, no iteration, no `size`.

```js
// Set
const set = new Set([1, 2, 3, 'text']);
set.size; // 4
set.has(1); // true
for (const val of set) console.log(val);
set.clear();

// WeakSet - objects only
let obj1 = { a: 1 };
const ws = new WeakSet([obj1]);
ws.has(obj1); // true
obj1 = null; // can be GC'd, entry removed

// Use case: mark objects processed
const processed = new WeakSet();
function process(obj) {
  if (processed.has(obj)) return;
  processed.add(obj);
  // do work...
}
```

---

### Q94: How does optional chaining differ from `&&` chaining?

**Answer:**

`?.` only checks for null/undefined (not other falsy values). Works with function calls and dynamic properties. `&&` checks truthiness.

```js
const user = {
  name: 'Alice',
  address: null,
  getProfile() { return { role: 'admin' }; }
};

user?.address?.city; // undefined
user?.profile?.name; // undefined
user?.getProfile?.(); // { role: 'admin' }

// vs && chaining
user && user.address && user.address.city; // undefined

// Difference with falsy
const data = { count: 0, name: '' };
data?.count; // 0 (correct)
data && data.count; // 0 (correct here too)

// Function call existence
obj.method?.();

// Dynamic property
user?.[key];

// Delete
delete user?.address?.city;
```

---

### Q95: What is the nullish coalescing assignment (`??=`)?

**Answer:**

`??=` assigns a value only if the variable is null or undefined. Part of ES2021 logical assignment operators.

```js
let a = null;
let b = 0;
let c = '';

a ??= 'default'; // a = 'default' (null)
b ??= 'default'; // b = 0 (not null/undefined)
c ??= 'default'; // c = '' (not null/undefined)

// vs ||=
let x = 0;
x ||= 42; // x = 42 (0 is falsy)
x ??= 99; // x = 42 (not null/undefined)

// Use cases
function config(options) {
  options.timeout ??= 3000;
  options.retries ??= 3;
  return options;
}

const obj = {};
obj.name ??= 'Guest';
```

---

### Q96: What is `||=` (logical OR assignment)?

**Answer:**

`||=` assigns a value only if the current value is falsy. Shorthand for `x = x || value`.

```js
let a = 0;
let b = 'hello';

a ||= 42; // a = 42 (0 is falsy)
b ||= 'world'; // b stays 'hello' (truthy)

// Practical defaults
const settings = { theme: '', fontSize: 0 };
settings.theme ||= 'dark'; // theme = 'dark'
settings.fontSize ||= 16; // fontSize = 16

// Note: replaces 0 and '' - use ??= to keep them

// Chaining
let count = 0;
count ||= 1; // count = 1
```

---

### Q97: What is `&&=` (logical AND assignment)?

**Answer:**

`&&=` assigns a value only if the current value is truthy. Shorthand for `x = x && value`.

```js
let a = true;
let b = false;

a &&= 'assigned'; // a = 'assigned' (truthy)
b &&= 'assigned'; // b stays false (falsy)

// Practical: update only if truthy
let user = { name: 'Alice', isAdmin: true };
user.isAdmin &&= false; // set to false

// Safe mutation
let config = { debug: true };
config.debug &&= false; // debug = false (was truthy)
```

---

### Q98: How do you merge objects in JavaScript?

**Answer:**

Use spread, `Object.assign()` for shallow merge. Implement deep merge for nested objects.

```js
// Shallow merge
const a = { x: 1, y: 2 };
const b = { y: 3, z: 4 };

// Spread
const merged1 = { ...a, ...b }; // { x: 1, y: 3, z: 4 }

// Object.assign
const merged2 = Object.assign({}, a, b); // { x: 1, y: 3, z: 4 }

// Deep merge
function deepMerge(target, ...sources) {
  if (!sources.length) return target;
  const source = sources.shift();
  if (isPlainObject(target) && isPlainObject(source)) {
    for (const key of Object.keys(source)) {
      if (isPlainObject(source[key])) {
        if (!target[key]) Object.assign(target, { [key]: {} });
        deepMerge(target[key], source[key]);
      } else {
        Object.assign(target, { [key]: source[key] });
      }
    }
  }
  return deepMerge(target, ...sources);
}

function isPlainObject(obj) {
  return obj && typeof obj === 'object' && !Array.isArray(obj);
}
```

---

### Q99: What is the difference between `Object.is()` and `===`?

**Answer:**

`Object.is()` behaves like `===` except for `-0` vs `+0` and `NaN` vs `NaN`.

```js
NaN === NaN;         // false
Object.is(NaN, NaN); // true

-0 === 0;            // true
Object.is(-0, 0);    // false

// Other cases same as ===
Object.is('hello', 'hello'); // true
Object.is({}, {}); // false

// Polyfill
function objectIs(x, y) {
  if (x === y) {
    return x !== 0 || 1 / x === 1 / y;
  }
  return x !== x && y !== y;
}

// Array methods use SameValueZero (Object.is but -0/+0 same)
[NaN].includes(NaN); // true
```

---

### Q100: What is the `Reflect` API?

**Answer:**

`Reflect` provides methods for interceptable JavaScript operations that mirror Proxy traps.

```js
const obj = { a: 1, b: 2 };

// Reflect.get
Reflect.get(obj, 'a'); // 1

// Reflect.set
Reflect.set(obj, 'c', 3);

// Reflect.has
Reflect.has(obj, 'a'); // true

// Reflect.ownKeys
Reflect.ownKeys(obj); // ['a', 'b', 'c']

// Reflect.defineProperty
Reflect.defineProperty(obj, 'd', { value: 4 });

// Reflect.deleteProperty
Reflect.deleteProperty(obj, 'a');

// Better than try-catch
if (Reflect.defineProperty(obj, 'x', { value: 1 })) {
  // success
}

// Proxy forwarding
const handler = {
  get(target, prop, receiver) {
    return Reflect.get(target, prop, receiver);
  }
};
```

---

### Q101: How does the `Proxy` object work?

**Answer:**

`Proxy` wraps an object and intercepts operations via handler traps. Used for validation, logging, reactivity, and virtualization.

```js
const target = { name: 'Alice', age: 30 };
const handler = {
  get(obj, prop) {
    if (prop === 'age') return obj[prop] + ' years';
    return obj[prop];
  },
  set(obj, prop, value) {
    if (prop === 'age' && (typeof value !== 'number' || value < 0)) {
      throw new Error('Invalid age');
    }
    obj[prop] = value;
    return true;
  }
};
const proxy = new Proxy(target, handler);
console.log(proxy.age); // '30 years'

// Validation proxy
function createValidator(obj, schema) {
  return new Proxy(obj, {
    set(target, prop, value) {
      if (schema[prop] && !schema[prop](value)) {
        throw new Error(`Invalid ${prop}: ${value}`);
      }
      target[prop] = value;
      return true;
    }
  });
}

// Revocable proxy
const { proxy: rev, revoke } = Proxy.revocable(target, {});
rev.name; // 'Alice'
revoke();
// rev.name; // TypeError
```

---

### Q102: Proxy vs `Object.defineProperty`?

**Answer:**

`Proxy` intercepts entire object operations via traps (including non-existent properties). `Object.defineProperty` only intercepts specific defined properties.

```js
// Object.defineProperty - one at a time
const obj = {};
Object.defineProperty(obj, 'name', {
  get() { return this._name; },
  set(v) { this._name = v; console.log('set'); }
});
obj.name = 'Alice'; // logs
obj.other = 'test'; // no interception

// Proxy - all properties
const handler = {
  get(target, prop) {
    console.log(`Get ${String(prop)}`);
    return target[prop];
  },
  set(target, prop, value) {
    console.log(`Set ${String(prop)} = ${value}`);
    target[prop] = value;
    return true;
  }
};
const proxy = new Proxy(obj, handler);
proxy.x = 10;   // logs
proxy.x;        // logs

// Proxy additional traps:
// deleteProperty, has, ownKeys, construct, apply
// getPrototypeOf, setPrototypeOf
// preventExtensions, isExtensible
```

---

### Q103: What are well-known symbols?

**Answer:**

Built-in Symbol values for customizing behavior: `Symbol.iterator`, `Symbol.hasInstance`, `Symbol.toStringTag`, `Symbol.species`, `Symbol.toPrimitive`, `Symbol.match`, etc.

```js
// Symbol.iterator
const range = {
  start: 1, end: 5,
  [Symbol.iterator]() {
    let current = this.start;
    return {
      next: () => ({
        value: current,
        done: current++ > this.end
      })
    };
  }
};
[...range]; // [1, 2, 3, 4, 5]

// Symbol.toStringTag
class Custom {
  get [Symbol.toStringTag]() { return 'Custom'; }
}
Object.prototype.toString.call(new Custom()); // '[object Custom]'

// Symbol.hasInstance
class Zero {
  static [Symbol.hasInstance](num) { return num === 0; }
}
0 instanceof Zero; // true

// Symbol.toPrimitive
const obj = {
  [Symbol.toPrimitive](hint) {
    if (hint === 'string') return 'custom';
    if (hint === 'number') return 42;
    return 'default';
  }
};
String(obj); // 'custom'
Number(obj); // 42
```

---

### Q104: How do you make objects iterable with `Symbol.iterator`?

**Answer:**

Implement `[Symbol.iterator]` returning an iterator with `next()` returning `{ value, done }`.

```js
const fibonacci = {
  [Symbol.iterator]() {
    let a = 0, b = 1;
    return {
      next() {
        const value = a;
        [a, b] = [b, a + b];
        return { value, done: value > 100 };
      }
    };
  }
};

for (const n of fibonacci) {
  console.log(n); // 0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89
}

// Generator approach (easier)
const range = {
  *[Symbol.iterator](start = 0, end = 10) {
    for (let i = start; i <= end; i++) yield i;
  }
};
```

---

### Q105: `structuredClone` vs `Object.assign` vs JSON clone?

**Answer:**

`structuredClone` deep clones, handles circular refs, Dates, Maps, Sets. `Object.assign` shallow clones. JSON method loses functions, undefined, Symbols, circular refs.

```js
const obj = {
  name: 'Alice',
  date: new Date(),
  map: new Map([['key', 'value']]),
  nested: { a: 1 },
  fn: () => console.log('test')
};
obj.self = obj; // circular

// Object.assign - shallow, no circular
const shallow = Object.assign({}, obj);
shallow.nested.a = 99;
console.log(obj.nested.a); // 99 (shared!)

// JSON - loses functions, Date, Map, undefined, circular
// JSON.parse(JSON.stringify(obj)) // throws on circular

// structuredClone - deep clone, handles all
const deep = structuredClone(obj);
deep.nested.a = 99;
console.log(obj.nested.a); // 1 (independent)
deep.date instanceof Date; // true
deep.map instanceof Map;   // true
```

---

### Q106: `for...in` vs `for...of` with objects?

**Answer:**

`for...in` works on objects (enumerable keys including inherited). `for...of` doesn't work on plain objects (not iterable). Use `Object.keys()`/`values()`/`entries()` with `for...of`.

```js
const obj = { a: 1, b: 2, c: 3 };

// for...in
for (const key in obj) {
  if (obj.hasOwnProperty(key)) {
    console.log(key, obj[key]);
  }
}

// for...of on plain object -> TypeError
// for (const val of obj) {} // TypeError

// for...of with Object methods
for (const key of Object.keys(obj)) console.log(key);
for (const val of Object.values(obj)) console.log(val);
for (const [k, v] of Object.entries(obj)) console.log(k, v);

// Custom iterable object
const iterableObj = {
  a: 1, b: 2, c: 3,
  *[Symbol.iterator]() {
    for (const key of Object.keys(this)) yield this[key];
  }
};
for (const val of iterableObj) console.log(val);
```

---

### Q107: What is `Object.hasOwn()`?

**Answer:**

`Object.hasOwn()` (ES2022) safely checks own properties. Unlike `hasOwnProperty`, it works on `Object.create(null)` and isn't shadowable.

```js
const obj1 = { name: 'Alice' };
const obj2 = Object.create(null);
obj2.name = 'Bob';
const obj3 = { hasOwnProperty: () => 'hacked', name: 'Charlie' };

// obj.hasOwnProperty() can fail
obj1.hasOwnProperty('name'); // true
// obj2.hasOwnProperty('name'); // TypeError
obj3.hasOwnProperty('name'); // 'hacked' (shadowed!)

// Object.hasOwn() - safe
Object.hasOwn(obj1, 'name'); // true
Object.hasOwn(obj2, 'name'); // true
Object.hasOwn(obj3, 'name'); // true
Object.hasOwn(obj1, 'toString'); // false (inherited)
```

---

### Q108: `Object.keys()` vs `getOwnPropertyNames()`?

**Answer:**

`Object.keys()` returns enumerable own properties only. `getOwnPropertyNames()` returns all own properties including non-enumerable.

```js
const obj = {};
Object.defineProperties(obj, {
  a: { value: 1, enumerable: true },
  b: { value: 2, enumerable: false },
  [Symbol('c')]: { value: 3, enumerable: true }
});

Object.keys(obj); // ['a']
Object.getOwnPropertyNames(obj); // ['a', 'b']

// Both exclude Symbols
Object.getOwnPropertySymbols(obj); // [Symbol(c)]
Reflect.ownKeys(obj); // ['a', 'b', Symbol(c)]

// Non-enumerable still accessible
console.log(obj.b); // 2
```

---

### Q109: How does `super` work in prototypes?

**Answer:**

`super` references the prototype of the current object. Works in class methods and object literal method shorthand.

```js
// In classes
class Parent {
  constructor(x) { this.x = x; }
  greet() { return `Parent: ${this.x}`; }
}

class Child extends Parent {
  constructor(x, y) {
    super(x);
    this.y = y;
  }
  greet() {
    return `${super.greet()}, Child: ${this.y}`;
  }
}

// In object literals
const parent = {
  name: 'Parent',
  greet() { return `Hello from ${this.name}`; }
};

const child = {
  name: 'Child',
  greet() {
    return `${super.greet()} (overridden)`;
  }
};
Object.setPrototypeOf(child, parent);
child.greet(); // 'Hello from Child (overridden)'

// super.prop only works in method shorthand
// Regular/anonymous functions don't work with super
```

---

### Q110: Static vs Instance methods?

**Answer:**

Static methods are on the class itself. Instance methods are on the prototype (available on instances). Statics are inherited by subclasses.

```js
class MathUtils {
  static add(a, b) { return a + b; }
  constructor(value) { this.value = value; }
  getValue() { return this.value; }
  square() { return this.value ** 2; }
}

// Static
MathUtils.add(2, 3); // 5

// Instance
const m = new MathUtils(5);
m.getValue(); // 5
m.square(); // 25

// Static cannot be called on instances
// m.add(2, 3); // TypeError

// Static inheritance
class AdvancedMath extends MathUtils {
  static multiply(a, b) { return a * b; }
}
AdvancedMath.add(2, 3); // 5 (inherited static)
```

---

### Q111: How does `this` work in different contexts?

**Answer:**

`this` depends on execution context: global, function (default/implicit/explicit/new), arrow (lexical), event handler, constructor.

```js
// Global
console.log(this); // window (browser)

// Regular function
function showThis() { console.log(this); }
showThis(); // window (non-strict) / undefined (strict)

// Method call
const obj = { name: 'Alice', greet() { console.log(this.name); } };
obj.greet(); // 'Alice'

// Method detached
const detached = obj.greet;
detached(); // undefined/global

// Arrow - lexical
const arrow = () => console.log(this);
arrow(); // outer this

// Event handler
button.addEventListener('click', function() {
  console.log(this); // button element
});

// Constructor
function Car(make) { this.make = make; }
new Car('Toyota');
```

---

### Q112: How do you copy properties without overwriting existing?

**Answer:**

Use iteration with `in` check, or Proxy for virtual defaults.

```js
function assignDefaults(target, ...sources) {
  for (const source of sources) {
    for (const key of Object.keys(source)) {
      if (!(key in target)) {
        target[key] = source[key];
      }
    }
  }
  return target;
}

const defaults = { name: 'Guest', role: 'viewer', theme: 'dark' };
const user = { name: 'Alice' };
assignDefaults(user, defaults);
// { name: 'Alice', role: 'viewer', theme: 'dark' }

// Spread approach (reverse)
const result = Object.fromEntries(
  Object.entries(defaults).filter(([k]) => !(k in user))
);
const merged = { ...user, ...result };

// Proxy approach
function withDefaults(target, defaults) {
  return new Proxy(target, {
    get(obj, prop) {
      return prop in obj ? obj[prop] : defaults[prop];
    }
  });
}
```

---

### Q113: `Object.create()` vs `new Object()`?

**Answer:**

`new Object()` creates with `Object.prototype`. `Object.create(proto)` uses any prototype (including `null`).

```js
const obj1 = new Object();
obj1.__proto__ === Object.prototype; // true

const obj2 = Object.create(Object.prototype); // same as obj1

// Object.create(null) - no prototype
const nullProto = Object.create(null);
nullProto.__proto__; // undefined
nullProto.toString; // undefined

// Custom prototype
const customProto = { greet() { console.log('Hi'); } };
const obj3 = Object.create(customProto);
obj3.greet(); // 'Hi'

// new Object({a:1}) wraps
const wrapped = new Object({ a: 1 });
console.log(wrapped); // { a: 1 }

// Object.create with descriptors
const obj4 = Object.create(Object.prototype, {
  name: { value: 'Alice', writable: true }
});
```

---

### Q114: `Object.assign()` vs `Object.defineProperties()`?

**Answer:**

`Object.assign` copies values. `Object.defineProperties` defines full descriptors (value, get/set, writable, etc.).

```js
// Object.assign - copies values
const source = { a: 1, b: 2 };
const target1 = Object.assign({}, source);
// Properties are default descriptors (writable:true, enumerable:true, configurable:true)

// Object.defineProperties - full control
const target2 = {};
Object.defineProperties(target2, {
  a: { value: 1, writable: false, enumerable: false },
  b: {
    get() { return this._b; },
    set(v) { this._b = v * 2; },
    enumerable: true
  }
});

target2.a = 99; // fails (writable: false)
target2.b = 5;
target2.b; // 10 (setter doubled)

// Object.assign copies getter results (not getters)
const getterSource = { get x() { return 1; } };
Object.assign({}, getterSource); // { x: 1 }
```

---

### Q115: What is the property enumeration order?

**Answer:**

Integer-like keys first (ascending), string keys in insertion order, Symbol keys in insertion order.

```js
const obj = {};
obj['b'] = 1;
obj['2'] = 2;
obj['a'] = 3;
obj[Symbol('c')] = 4;
obj['1'] = 5;
obj[Symbol('d')] = 6;

Object.keys(obj); // ['1', '2', 'b', 'a']
// Number-like keys first: '1', '2'
// Then string keys in insertion order: 'b', 'a'
// Symbols not included in keys/values/entries

Reflect.ownKeys(obj);
// ['1', '2', 'b', 'a', Symbol(c), Symbol(d)]

// for...in follows same order (plus inherited)
// Object.values, Object.entries follow same order
```

---

### Q116: What is the `with` statement and why avoid it?

**Answer:**

`with` extends scope chain but is disallowed in strict mode, causes performance issues and ambiguity.

```js
// Avoid with statement
const obj = { a: 1, b: 2 };

with (obj) {
  console.log(a, b); // 1, 2
  a = 5; // modifies obj.a
}

// Problem: ambiguous
function test(obj) {
  with (obj) {
    x = 10; // Is x a property or global? Unknown at compile time
  }
}

// Better alternative: destructuring
const { a, b } = obj;
console.log(a, b);

// Strict mode forbids with
'use strict';
// with (obj) {} // SyntaxError
```

---

### Q117: What is the `__proto__` gotcha with object literals?

**Answer:**

`__proto__` in object literal sets the prototype (special behavior). It's a getter/setter on `Object.prototype`.

```js
// Special - sets prototype
const obj1 = { __proto__: { method() {} } };
obj1.method(); // works, inherited

// Unlike regular property
const obj2 = {};
obj2.__proto__ = { method() {} }; // works but uses setter

// Object literal with __proto__ as regular property
const obj3 = {};
Object.defineProperty(obj3, '__proto__', {
  value: 'doesnt change proto',
  writable: true,
  enumerable: true
});
// Now obj3.__proto__ is a regular property, not prototype

// Object.create is clearer
const obj4 = Object.create({ method() {} });
```

---

### Q118: How do you detect if an object has a property from prototype vs own?

**Answer:**

Use `hasOwnProperty`/`Object.hasOwn` for own. Use `in` or check prototype chain manually.

```js
function getPropertyOrigin(obj, prop) {
  if (Object.hasOwn(obj, prop)) {
    return { source: 'own', value: obj[prop] };
  }
  if (prop in obj) {
    const proto = Object.getPrototypeOf(obj);
    while (proto) {
      if (Object.hasOwn(proto, prop)) {
        return { source: 'prototype', value: obj[prop] };
      }
      proto = Object.getPrototypeOf(proto);
    }
  }
  return { source: 'not found' };
}

const parent = { inherited: 'yes' };
const child = Object.create(parent);
child.own = 'yes';

getPropertyOrigin(child, 'own'); // { source: 'own', value: 'yes' }
getPropertyOrigin(child, 'inherited'); // { source: 'prototype', value: 'yes' }
getPropertyOrigin(child, 'toString'); // { source: 'prototype', value: [Function] }
getPropertyOrigin(child, 'nonexistent'); // { source: 'not found' }
```

---

### Q119: How do you implement inheritance without classes?

**Answer:**

Use `Object.create()` to set up prototype chains, or manually assign prototypes.

```js
// Parent
function Animal(name) {
  this.name = name;
}
Animal.prototype.eat = function() {
  console.log(`${this.name} eats`);
};

// Child
function Dog(name, breed) {
  Animal.call(this, name); // call parent constructor
  this.breed = breed;
}

// Set up inheritance
Dog.prototype = Object.create(Animal.prototype);
Dog.prototype.constructor = Dog; // fix constructor

// Add child methods
Dog.prototype.bark = function() {
  console.log(`${this.name} barks`);
};

// Override
Dog.prototype.eat = function() {
  Animal.prototype.eat.call(this);
  console.log(`${this.name} wolfs down food`);
};

const dog = new Dog('Rex', 'Lab');
dog.eat(); // 'Rex eats', 'Rex wolfs down food'
dog.bark(); // 'Rex barks'
dog instanceof Dog; // true
dog instanceof Animal; // true
```

---

### Q120: What is `instanceof` with primitive wrappers?

**Answer:**

Primitives are not `instanceof` their wrapper constructors. Only object-wrapped versions are.

```js
'hello' instanceof String;  // false (primitive)
new String('hello') instanceof String; // true

42 instanceof Number;      // false
new Number(42) instanceof Number; // true

// But primitives have access to wrapper methods
'hello'.toUpperCase(); // 'HELLO' (auto-boxing)

// instanceof across realms (iframes) breaks
// Use Object.prototype.toString instead
Object.prototype.toString.call('hello'); // '[object String]'
Object.prototype.toString.call(42); // '[object Number]'
```

---

### Q121: How do you implement `new` keyword manually?

**Answer:**

`new` creates object, links prototype, binds `this`, returns object (or constructor return if object).

```js
function myNew(Constructor, ...args) {
  // 1. Create new object with prototype linked
  const obj = Object.create(Constructor.prototype);

  // 2. Execute constructor with obj as this
  const result = Constructor.apply(obj, args);

  // 3. Return object if result is object, else new object
  return (result !== null && typeof result === 'object')
    ? result
    : obj;
}

function Person(name) {
  this.name = name;
}

const p = myNew(Person, 'Alice');
console.log(p.name); // 'Alice'
console.log(p instanceof Person); // true

// Constructor that returns object
function ReturnsObj() {
  return { custom: true };
}
const r = myNew(ReturnsObj);
console.log(r instanceof ReturnsObj); // false
console.log(r.custom); // true
```

---

### Q122: What is the difference between `.constructor` and `instanceof`?

**Answer:**

`.constructor` is a regular property that can be modified. `instanceof` checks the prototype chain and cannot be easily spoofed.

```js
function Person(name) { this.name = name; }
const p = new Person('Alice');

p.constructor === Person; // true
p instanceof Person; // true

// constructor can be changed
p.constructor = function Fake() {};
p instanceof Person; // true (prototype unchanged)
p.constructor === Person; // false

// .constructor can be missing
const obj = Object.create(null);
obj.constructor; // undefined

// instanceof uses prototype chain
const child = Object.create(p);
child instanceof Person; // true (inherits through prototype)

// instanceof can be customized via Symbol.hasInstance
class Custom {
  static [Symbol.hasInstance](v) { return v.custom === true; }
}
{ custom: true } instanceof Custom; // true
```

---

### Q123: What is the prototype chain for native types?

**Answer:**

All objects ultimately inherit from `Object.prototype`. Arrays, Dates, RegExps, and functions all have their own prototype that extends `Object.prototype`.

```js
// Array
const arr = [];
arr.__proto__ === Array.prototype; // true
Array.prototype.__proto__ === Object.prototype; // true

// Function
function fn() {}
fn.__proto__ === Function.prototype; // true
Function.prototype.__proto__ === Object.prototype; // true

// Number (primitive, but wrapper)
const num = 42;
num.__proto__; // undefined (primitive)
(42).__proto__; // Number.prototype (auto-boxed)

// Chain example for arrays:
// arr -> Array.prototype -> Object.prototype -> null

// Methods added at each level
Array.prototype.push; // exists
Object.prototype.toString; // exists
// Array inherits toString but has its own version
Array.prototype.toString !== Object.prototype.toString; // true
```

---

### Q124: How do you extend built-in objects?

**Answer:**

Extend built-ins via subclassing (class extends Array/Date/etc.) or by modifying prototypes (not recommended).

```js
// Extend Array via subclass
class MyArray extends Array {
  first() { return this[0]; }
  last() { return this[this.length - 1]; }
  average() { return this.reduce((a, b) => a + b, 0) / this.length; }
}

const myArr = new MyArray(1, 2, 3, 4, 5);
console.log(myArr.first()); // 1
console.log(myArr.last());  // 5
console.log(myArr.average()); // 3
console.log(myArr.length); // 5

// Methods that return new arrays use Symbol.species
const mapped = myArr.map(x => x * 2);
mapped instanceof MyArray; // true (uses Symbol.species)

// Modify prototype (not recommended)
Array.prototype.sum = function() {
  return this.reduce((a, b) => a + b, 0);
};
[1, 2, 3].sum(); // 6

// Caution: avoid modifying built-in prototypes (collisions, future issues)
```

---

### Q125: How does `Object.assign()` handle getters/setters?

**Answer:**

`Object.assign` reads getter values and copies them as data properties (getters are not preserved).

```js
const source = {
  get name() {
    return this._name || 'Default';
  },
  set name(v) {
    console.log('Setter called');
    this._name = v;
  }
};

source.name = 'Alice'; // 'Setter called'

const target = Object.assign({}, source);
// target.name is 'Alice' (the VALUE, not a getter)
// The getter/setter is NOT copied

// To copy getters, use property descriptors
const fullCopy = Object.defineProperties({},
  Object.getOwnPropertyDescriptors(source)
);
// Now fullCopy has the getter/setter

// Object.assign's source getter is called once per assignment
const spySource = { get x() { console.log('getter'); return 42; } };
Object.assign({}, spySource); // logs 'getter'
```

---

### Q126: How do you clone an object with getters/setters preserved?

**Answer:**

Use `Object.getOwnPropertyDescriptors()` with `Object.defineProperties()`.

```js
const obj = {
  _name: 'Alice',
  get name() { return this._name.toUpperCase(); },
  set name(v) { this._name = v; }
};

// Shallow copy loses getter (copies value)
const shallow = { ...obj };
console.log(shallow.name); // 'ALICE' (value, not getter)
shallow.name = 'Bob'; // sets data property, not setter
console.log(shallow._name); // undefined

// Proper clone with descriptors
const clone = Object.defineProperties({},
  Object.getOwnPropertyDescriptors(obj)
);
console.log(clone.name); // 'ALICE' (getter works)
clone.name = 'Bob'; // setter works
console.log(clone._name); // 'Bob'

// structuredClone also loses getters
const structClone = structuredClone(obj);
// structClone.name is 'ALICE' (plain value)
```

---

### Q127: How do you implement multiple inheritance?

**Answer:**

JavaScript doesn't support multiple inheritance. Use composition, mixins, or trait patterns instead.

```js
// Composition approach
function createWalker(state) {
  return {
    walk() { console.log(`${state.name} walking`); }
  };
}
function createSwimmer(state) {
  return {
    swim() { console.log(`${state.name} swimming`); }
  };
}

function createDuck(name) {
  const state = { name };
  return Object.assign(state, createWalker(state), createSwimmer(state));
}

const duck = createDuck('Duck');
duck.walk(); // 'Duck walking'
duck.swim(); // 'Duck swimming'

// Mixin classes
const WalkerMixin = (Base) => class extends Base {
  walk() { console.log(`${this.name} walking`); }
};
const SwimmerMixin = (Base) => class extends Base {
  swim() { console.log(`${this.name} swimming`); }
};

class Animal {
  constructor(name) { this.name = name; }
}

class Duck extends SwimmerMixin(WalkerMixin(Animal)) {
  quack() { console.log(`${this.name} quacking`); }
}

const duck2 = new Duck('Donald');
duck2.walk();
duck2.swim();
duck2.quack();
```

---

### Q128: How does the prototype chain affect `hasOwnProperty`?

**Answer:**

`hasOwnProperty` is inherited from `Object.prototype`. It can be shadowed, removed, or unavailable on objects without `Object.prototype` in chain.

```js
// Inherited from Object.prototype
const obj = { a: 1 };
obj.hasOwnProperty('a'); // true

// Objects without Object.prototype
const noProto = Object.create(null);
noProto.a = 1;
// noProto.hasOwnProperty('a'); // TypeError

// Use safe call
Object.prototype.hasOwnProperty.call(noProto, 'a'); // true
// Or modern:
Object.hasOwn(noProto, 'a'); // true

// Shadowed hasOwnProperty
const shadowed = { hasOwnProperty: () => 'hacked', a: 1 };
shadowed.hasOwnProperty('a'); // 'hacked' (shadowed!)
Object.hasOwn(shadowed, 'a'); // true (safe)

// Prototype chain with hasOwnProperty
const parent = { a: 1 };
const child = Object.create(parent);
child.b = 2;
child.hasOwnProperty('a'); // false (inherited, not own)
child.hasOwnProperty('b'); // true
'toString' in child; // true (from Object.prototype)
child.hasOwnProperty('toString'); // false
```

---

### Q129: What is the difference between `Object.setPrototypeOf` and `Object.create`?

**Answer:**

`Object.create` creates a new object with specified prototype. `Object.setPrototypeOf` mutates an existing object's prototype.

```js
// Object.create - creates new object
const proto = { greet() { console.log('Hi'); } };
const obj = Object.create(proto);

// Object.setPrototypeOf - mutates existing
const existing = { name: 'Alice' };
Object.setPrototypeOf(existing, proto);
existing.greet(); // 'Hi'

// Performance warning
// Object.setPrototypeOf is slow - avoid in hot paths
// Use Object.create for new objects

// Changing prototype of existing object
function changeProto() {
  const obj = { a: 1 };
  const proto1 = { b: 2 };
  const proto2 = { c: 3 };
  Object.setPrototypeOf(obj, proto1);
  obj.b; // 2
  Object.setPrototypeOf(obj, proto2);
  obj.c; // 3
  obj.b; // undefined
}

// __proto__ setter same as setPrototypeOf
const another = {};
another.__proto__ = proto; // same as setPrototypeOf
```

---

### Q130: How do you create a truly empty object?

**Answer:**

`Object.create(null)` creates an object with no prototype — no `toString`, `hasOwnProperty`, `constructor`, etc.

```js
// Regular object - has prototype
const regular = {};
regular.toString; // function from Object.prototype
'toString' in regular; // true

// Truly empty
const empty = Object.create(null);
empty.toString; // undefined
'toString' in empty; // false
empty.__proto__; // undefined

// Use cases:
// 1. Safe dictionary (no prototype pollution)
const dict = Object.create(null);
dict.key = 'value';
// No chance of key collision with prototype properties

// 2. JSON-like data structures
const data = Object.create(null);
data.user = { name: 'Alice' };

// 3. Avoid prototype pollution attacks
function safeGet(key, obj) {
  return Object.create(null)[key]; // safer

  // But recommended: Object.hasOwn + direct access
}

// Warning: no toString means console.log shows "[Object: null prototype] { key: 'value' }"
```

---

# PHASE 3: ARRAYS (Q131–Q180)

---

### Q131: How does `map()` work? Give examples.

**Answer:**

`map()` creates a new array by calling a function on every element. It does not mutate the original array.

```js
const numbers = [1, 2, 3, 4, 5];

const doubled = numbers.map(n => n * 2);
// [2, 4, 6, 8, 10]

// With index
const withIndex = numbers.map((n, i) => `${i}: ${n}`);
// ['0: 1', '1: 2', '2: 3', '3: 4', '4: 5']

// Array of objects
const users = [{ name: 'Alice' }, { name: 'Bob' }];
const names = users.map(u => u.name);
// ['Alice', 'Bob']

// Parsing strings
const strings = ['1', '2', '3'];
const nums = strings.map(Number);
// [1, 2, 3]

// map on array-like objects
const divs = document.querySelectorAll('div');
const texts = Array.from(divs).map(el => el.textContent);

// Chaining
const result = [1, 2, 3, 4]
  .map(n => n * 2)
  .filter(n => n > 5);
// [6, 8]
```

---

### Q132: How does `filter()` work?

**Answer:**

`filter()` creates a new array with elements that pass a test function. Returns empty array if no elements pass.

```js
const numbers = [1, 2, 3, 4, 5, 6];

const evens = numbers.filter(n => n % 2 === 0);
// [2, 4, 6]

const greaterThan3 = numbers.filter(n => n > 3);
// [4, 5, 6]

// Filter objects
const users = [
  { name: 'Alice', age: 30 },
  { name: 'Bob', age: 17 },
  { name: 'Charlie', age: 25 }
];
const adults = users.filter(u => u.age >= 18);
// [{ name: 'Alice', age: 30 }, { name: 'Charlie', age: 25 }]

// Removing falsy values
const mixed = [0, 'hello', false, '', 42, null];
const truthy = mixed.filter(Boolean);
// ['hello', 42]

// Using index
const removeEveryOther = numbers.filter((_, i) => i % 2 === 0);
// [1, 3, 5]
```

---

### Q133: How does `reduce()` work? Give advanced examples.

**Answer:**

`reduce()` executes a reducer function on each element, accumulating a result. It can do anything map/filter can do, plus more complex operations.

```js
const numbers = [1, 2, 3, 4, 5];

// Sum
const sum = numbers.reduce((acc, n) => acc + n, 0);
// 15

// Product
const product = numbers.reduce((acc, n) => acc * n, 1);
// 120

// Max
const max = numbers.reduce((acc, n) => (n > acc ? n : acc), -Infinity);
// 5

// Grouping
const items = ['apple', 'banana', 'apple', 'orange', 'banana', 'apple'];
const grouped = items.reduce((acc, item) => {
  acc[item] = (acc[item] || 0) + 1;
  return acc;
}, {});
// { apple: 3, banana: 2, orange: 1 }

// Flatten
const nested = [[1, 2], [3, 4], [5, 6]];
const flat = nested.reduce((acc, arr) => acc.concat(arr), []);
// [1, 2, 3, 4, 5, 6]

// Compose functions
const compose = (...fns) => x => fns.reduceRight((acc, fn) => fn(acc), x);
const add1 = x => x + 1;
const double = x => x * 2;
const add1ThenDouble = compose(double, add1);
add1ThenDouble(5); // 12 ((5+1)*2)

// Pipe (left to right)
const pipe = (...fns) => x => fns.reduce((acc, fn) => fn(acc), x);
const doubleThenAdd1 = pipe(double, add1);
doubleThenAdd1(5); // 11 (5*2+1)
```

---

### Q134: How does `forEach()` differ from `map()`?

**Answer:**

`forEach()` executes a function for each element but returns `undefined`. It's used for side effects. `map()` returns a new array and is used for transformation.

```js
const numbers = [1, 2, 3];

// forEach - for side effects, returns undefined
const forEachResult = numbers.forEach(n => console.log(n));
// 1, 2, 3
console.log(forEachResult); // undefined

// map - for transformation, returns new array
const mapResult = numbers.map(n => n * 2);
console.log(mapResult); // [2, 4, 6]

// forEach cannot be chained
// numbers.forEach(n => n*2).filter(n => n > 2); // TypeError

// map can be chained
numbers.map(n => n*2).filter(n => n > 2); // [4, 6]

// forEach does not work with async/await as expected
// (forEach doesn't wait for promises)
async function badAsync() {
  [1, 2, 3].forEach(async n => {
    await delay(1000);
    console.log(n);
  });
  console.log('Done'); // runs BEFORE the numbers
}

// Use for...of or Promise.all instead
async function goodAsync() {
  for (const n of [1, 2, 3]) {
    await delay(1000);
    console.log(n);
  }
  console.log('Done'); // runs AFTER
}
```

---

### Q135: How does `find()` differ from `filter()`?

**Answer:**

`find()` returns the first matching element (or `undefined`). `filter()` returns all matching elements (always an array).

```js
const users = [
  { id: 1, name: 'Alice' },
  { id: 2, name: 'Bob' },
  { id: 3, name: 'Charlie' },
  { id: 4, name: 'Bob' }
];

const bob = users.find(u => u.name === 'Bob');
console.log(bob); // { id: 2, name: 'Bob' }

const allBobs = users.filter(u => u.name === 'Bob');
console.log(allBobs); // [{ id: 2, name: 'Bob' }, { id: 4, name: 'Bob' }]

// find returns undefined
const unknown = users.find(u => u.id === 999);
console.log(unknown); // undefined

// filter returns empty array
const none = users.filter(u => u.id === 999);
console.log(none); // []

// findIndex - like find but returns index
const index = users.findIndex(u => u.name === 'Bob');
console.log(index); // 1
```

---

### Q136: How do `some()` and `every()` work?

**Answer:**

`some()` returns `true` if any element passes the test. `every()` returns `true` only if all elements pass. Both short-circuit.

```js
const numbers = [1, 2, 3, 4, 5];

// some
const hasEven = numbers.some(n => n % 2 === 0); // true
const hasNegative = numbers.some(n => n < 0); // false

// every
const allPositive = numbers.every(n => n > 0); // true
const allEven = numbers.every(n => n % 2 === 0); // false

// Short-circuit behavior
const bigArray = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];
bigArray.some(n => {
  console.log('Checking', n);
  return n > 5;
});
// Logs: 1, 2, 3, 4, 5, 6 (stops at 6)

bigArray.every(n => {
  console.log('Checking', n);
  return n < 5;
});
// Logs: 1, 2, 3, 4, 5 (stops at 5)

// Empty arrays
[].some(() => true);  // false (vacuous truth)
[].every(() => false); // true (vacuous truth)
```

---

### Q137: How does `sort()` work and what are its pitfalls?

**Answer:**

`sort()` converts elements to strings by default. Use a compare function for numeric sort. It mutates the original array.

```js
// Default: string sort
const numbers = [1, 10, 2, 21];
numbers.sort();
console.log(numbers); // [1, 10, 2, 21] (string sort!)

// Numeric sort (ascending)
numbers.sort((a, b) => a - b);
console.log(numbers); // [1, 2, 10, 21]

// Numeric sort (descending)
numbers.sort((a, b) => b - a);
console.log(numbers); // [21, 10, 2, 1]

// Sort objects by property
const users = [
  { name: 'Charlie', age: 35 },
  { name: 'Alice', age: 30 },
  { name: 'Bob', age: 25 }
];
users.sort((a, b) => a.age - b.age);
// [{ name: 'Bob', age: 25 }, { name: 'Alice', age: 30 }, { name: 'Charlie', age: 35 }]

// Sort by string property
users.sort((a, b) => a.name.localeCompare(b.name));
// [{ name: 'Alice', age: 30 }, { name: 'Bob', age: 25 }, { name: 'Charlie', age: 35 }]

// Stable sort (ES2019+)
// Equal elements maintain original order
const items = [{ n: 1, order: 0 }, { n: 2, order: 1 }, { n: 1, order: 2 }];
items.sort((a, b) => a.n - b.n);
// [{ n: 1, order: 0 }, { n: 1, order: 2 }, { n: 2, order: 1 }] (order preserved)

// Pitfall: sort mutates
const original = [3, 1, 2];
const sorted = original.sort();
console.log(original === sorted); // true (same reference)
```

---

### Q138: What is the difference between `reverse()` and `toReversed()`?

**Answer:**

`reverse()` mutates the original array. `toReversed()` (ES2023) returns a reversed copy without mutating.

```js
const arr = [1, 2, 3, 4, 5];

// Mutating
const reversed = arr.reverse();
console.log(arr); // [5, 4, 3, 2, 1] (mutated)
console.log(reversed === arr); // true

// Non-mutating (ES2023)
const arr2 = [1, 2, 3, 4, 5];
const copyReversed = arr2.toReversed();
console.log(arr2); // [1, 2, 3, 4, 5] (unchanged)
console.log(copyReversed); // [5, 4, 3, 2, 1]

// Other new non-mutating methods:
// toSorted() - like sort() but returns copy
// toSpliced() - like splice() but returns copy
// with(index, value) - returns copy with element replaced

const sorted = arr2.toSorted((a, b) => b - a);
console.log(arr2); // unchanged
console.log(sorted); // [5, 4, 3, 2, 1]
```

---

### Q139: What is the difference between `splice()` and `slice()`?

**Answer:**

`splice()` mutates the array (add/remove elements). `slice()` returns a shallow copy (non-mutating).

```js
const arr = [1, 2, 3, 4, 5];

// slice - returns new array
const sliced = arr.slice(1, 3); // [2, 3]
console.log(arr); // [1, 2, 3, 4, 5] (unchanged)

// slice with negative
arr.slice(-2); // [4, 5]
arr.slice(); // full shallow copy

// splice - mutates
const removed = arr.splice(1, 2); // remove 2 elements from index 1
console.log(arr); // [1, 4, 5] (mutated)
console.log(removed); // [2, 3] (removed elements)

// splice to insert
arr.splice(1, 0, 2, 3); // remove 0, insert 2,3
console.log(arr); // [1, 2, 3, 4, 5]

// splice to replace
arr.splice(0, 2, 'a', 'b'); // remove first 2, insert a,b
console.log(arr); // ['a', 'b', 3, 4, 5]

// Use slice + spread for immutable operations
const immutable = [1, 2, 3, 4, 5];
const newArr = [...immutable.slice(0, 2), ...immutable.slice(3)];
// [1, 2, 4, 5]
```

---

### Q140: How do `flat()` and `flatMap()` work?

**Answer:**

`flat(depth)` flattens nested arrays to specified depth (default 1). `flatMap()` maps then flattens by 1 level.

```js
const nested = [1, [2, [3, [4]]]];

// flat - default depth 1
nested.flat(); // [1, 2, [3, [4]]]

// flat with depth
nested.flat(2); // [1, 2, 3, [4]]
nested.flat(Infinity); // [1, 2, 3, 4]

// flatMap - map then flatten by 1
const sentences = ['Hello world', 'Foo bar'];
const words = sentences.flatMap(s => s.split(' '));
// ['Hello', 'world', 'Foo', 'bar']

// flatMap instead of map+filter
const numbers = [1, 2, 3, 4, 5];
const result = numbers.flatMap(n => n % 2 === 0 ? [n, n * 2] : []);
// [2, 4, 4, 8] (even numbers doubled)

// Without flatMap, you'd need:
const result2 = numbers
  .filter(n => n % 2 === 0)
  .map(n => [n, n * 2])
  .flat();
// [2, 4, 4, 8]

// flatMap removal
const removeNegatives = [1, -2, 3, -4].flatMap(n => n > 0 ? [n] : []);
// [1, 3]
```

---

### Q141: How do `Array.from()` and `Array.of()` work?

**Answer:**

`Array.from()` creates arrays from iterables or array-likes. `Array.of()` creates arrays from arguments (unlike `Array()` constructor).

```js
// Array.from - from iterables
Array.from('hello'); // ['h', 'e', 'l', 'l', 'o']
Array.from(new Set([1, 2, 2, 3])); // [1, 2, 3]
Array.from(new Map([['a', 1], ['b', 2]])); // [['a', 1], ['b', 2]]

// Array.from - from array-like
const divs = document.querySelectorAll('div');
const divArray = Array.from(divs);

// Array.from - with map function
Array.from('hello', c => c.toUpperCase()); // ['H', 'E', 'L', 'L', 'O']

// Create range
Array.from({ length: 5 }, (_, i) => i + 1); // [1, 2, 3, 4, 5]
Array.from({ length: 26 }, (_, i) => String.fromCharCode(97 + i));
// ['a', 'b', ..., 'z']

// Array.of - unlike Array()
Array.of(5); // [5]
Array(5); // [empty x 5] (length-5 empty array)

Array.of(1, 2, 3); // [1, 2, 3]
Array(1, 2, 3); // [1, 2, 3] (same here)

// Array.from with thisArg
const doubler = { factor: 2 };
Array.from([1, 2, 3], function(n) { return n * this.factor; }, doubler);
// [2, 4, 6]
```

---

### Q142: What is `Array.isArray()` and why use it?

**Answer:**

`Array.isArray()` reliably checks if a value is an array. Better than `typeof` (returns 'object') and `instanceof` (fails across iframes).

```js
Array.isArray([]); // true
Array.isArray([1, 2, 3]); // true
Array.isArray(new Array(5)); // true
Array.isArray({}); // false
Array.isArray('hello'); // false

// typeof fails
typeof []; // 'object' (not helpful)

// instanceof fails across iframes/realms
const iframe = document.createElement('iframe');
document.body.appendChild(iframe);
const iframeArray = new iframe.contentWindow.Array(1, 2, 3);
iframeArray instanceof Array; // false (different realm!)
Array.isArray(iframeArray); // true (works!)

// Older polyfill
Array.isArray = Array.isArray || function(arg) {
  return Object.prototype.toString.call(arg) === '[object Array]';
};
```

---

### Q143: How do generator functions work with `yield`?

**Answer:**

Generator functions (`function*`) return an iterator that can be paused/resumed with `yield`. Each `next()` call executes until next `yield`.

```js
// Basic generator
function* countToThree() {
  yield 1;
  yield 2;
  yield 3;
}

const gen = countToThree();
console.log(gen.next()); // { value: 1, done: false }
console.log(gen.next()); // { value: 2, done: false }
console.log(gen.next()); // { value: 3, done: false }
console.log(gen.next()); // { value: undefined, done: true }

// Generator as iterable
for (const n of countToThree()) {
  console.log(n); // 1, 2, 3
}

// Infinite generator
function* fibonacci() {
  let a = 0, b = 1;
  while (true) {
    yield a;
    [a, b] = [b, a + b];
  }
}

const fib = fibonacci();
for (let i = 0; i < 10; i++) {
  console.log(fib.next().value); // 0, 1, 1, 2, 3, 5, 8, 13, 21, 34
}

// Generator with next() argument
function* twoWay() {
  const a = yield 'First';
  console.log('Received:', a);
  const b = yield 'Second';
  console.log('Received:', b);
  return 'Done';
}

const gen2 = twoWay();
console.log(gen2.next()); // { value: 'First', done: false }
console.log(gen2.next('A')); // logs 'Received: A', then { value: 'Second', done: false }
console.log(gen2.next('B')); // logs 'Received: B', then { value: 'Done', done: true }
```

---

### Q144: How do you find the last element matching a condition?

**Answer:**

Use `findLast()` (ES2023) or reverse and find.

```js
const numbers = [1, 2, 3, 4, 5, 4, 3, 2, 1];

// findLast (ES2023)
const lastEven = numbers.findLast(n => n % 2 === 0); // 2
const lastGreaterThan3 = numbers.findLast(n => n > 3); // 4

// findLastIndex (ES2023)
const lastIndex = numbers.findLastIndex(n => n % 2 === 0); // 7

// Before ES2023
const last = [...numbers].reverse().find(n => n % 2 === 0); // 2
// Careful: reverse() mutates

// Manual approach
function findLast(arr, predicate) {
  for (let i = arr.length - 1; i >= 0; i--) {
    if (predicate(arr[i], i, arr)) return arr[i];
  }
  return undefined;
}
```

---

### Q145: How do you remove duplicates from an array?

**Answer:**

Multiple approaches: Set, filter with indexOf, reduce.

```js
const arr = [1, 2, 2, 3, 4, 4, 5];

// Using Set (simplest)
const unique1 = [...new Set(arr)];
// [1, 2, 3, 4, 5]

// Using filter
const unique2 = arr.filter((n, i) => arr.indexOf(n) === i);

// Using reduce
const unique3 = arr.reduce((acc, n) => {
  if (!acc.includes(n)) acc.push(n);
  return acc;
}, []);

// For objects by property
const users = [
  { id: 1, name: 'Alice' },
  { id: 2, name: 'Bob' },
  { id: 1, name: 'Alice' }
];

const uniqueUsers = [...new Map(users.map(u => [u.id, u])).values()];
// [{ id: 1, name: 'Alice' }, { id: 2, name: 'Bob' }]

// Multiple property uniqueness
const byNameAndAge = [...new Map(
  users.map(u => [`${u.name}-${u.age}`, u])
).values()];
```

---

### Q146: How do you flatten a nested array (deep flatten)?

**Answer:**

Use `flat(Infinity)` or recursive reduce.

```js
const deeplyNested = [1, [2, [3, [4, [5]]]]];

// ES2019 - flat with Infinity
const flat1 = deeplyNested.flat(Infinity);
// [1, 2, 3, 4, 5]

// Recursive reduce
function deepFlatten(arr) {
  return arr.reduce((acc, item) =>
    acc.concat(Array.isArray(item) ? deepFlatten(item) : item), []);
}

// Generator approach
function* flattenGenerator(arr) {
  for (const item of arr) {
    if (Array.isArray(item)) yield* flattenGenerator(item);
    else yield item;
  }
}
const flat3 = [...flattenGenerator(deeplyNested)];

// Stack-based (no recursion)
function flattenStack(arr) {
  const stack = [...arr];
  const result = [];
  while (stack.length) {
    const item = stack.pop();
    if (Array.isArray(item)) stack.push(...item);
    else result.unshift(item);
  }
  return result;
}
```

---

### Q147: How do you group array elements by a property?

**Answer:**

Use `Object.groupBy()` (ES2024), or manual reduce.

```js
const users = [
  { name: 'Alice', role: 'admin' },
  { name: 'Bob', role: 'user' },
  { name: 'Charlie', role: 'admin' },
  { name: 'Dave', role: 'user' }
];

// Object.groupBy (ES2024)
const groupedByRole = Object.groupBy(users, user => user.role);
// {
//   admin: [{ name: 'Alice', role: 'admin' }, { name: 'Charlie', role: 'admin' }],
//   user: [{ name: 'Bob', role: 'user' }, { name: 'Dave', role: 'user' }]
// }

// Map.groupBy (ES2024) - returns Map
const groupedMap = Map.groupBy(users, user => user.role);

// Pre-ES2024: manual reduce
const grouped = users.reduce((acc, user) => {
  (acc[user.role] = acc[user.role] || []).push(user);
  return acc;
}, {});
// Same result

// Group by multiple properties
const groupedByName = users.reduce((acc, user) => {
  const key = `${user.role}-${user.name[0]}`;
  (acc[key] = acc[key] || []).push(user);
  return acc;
}, {});
```

---

### Q148: How does `reduceRight()` differ from `reduce()`?

**Answer:**

`reduceRight()` processes elements from right to left instead of left to right.

```js
const numbers = [1, 2, 3, 4, 5];

// reduce: left to right
const sum = numbers.reduce((acc, n) => acc + n, 0); // 15

// reduceRight: right to left
const subtractLeft = numbers.reduce((acc, n) => acc - n, 0);
// (((((0 - 1) - 2) - 3) - 4) - 5) = -15

const subtractRight = numbers.reduceRight((acc, n) => acc - n, 0);
// (((((0 - 5) - 4) - 3) - 2) - 1) = -15 (same result)

// Practical: reverse string
const str = 'hello';
const reversed = [...str].reduceRight((acc, c) => acc + c, '');
// 'olleh'

// Practical: nested structure traversal
const tree = [
  { value: 1, children: [{ value: 2 }] },
  { value: 3 }
];
// Process leaves right-to-left
```

---

### Q149: What is the difference between `fill()` and `copyWithin()`?

**Answer:**

`fill()` sets array elements to a static value. `copyWithin()` copies a portion of the array to another position within the same array. Both mutate.

```js
// fill - all elements to value
const arr1 = [1, 2, 3, 4, 5];
arr1.fill(0); // [0, 0, 0, 0, 0]

// fill with start/end
const arr2 = [1, 2, 3, 4, 5];
arr2.fill(0, 2, 4); // [1, 2, 0, 0, 5]

// Create array with same value
Array.from({ length: 5 }, () => 0); // [0, 0, 0, 0, 0]
new Array(5).fill(0); // [0, 0, 0, 0, 0]

// copyWithin - copies within same array
const arr3 = [1, 2, 3, 4, 5, 6];
arr3.copyWithin(0, 3, 5); // copy elements at index 3,4 to index 0,1
// [4, 5, 3, 4, 5, 6]

// copyWithin parameters: target, start, end
// default end = arr.length
const arr4 = [1, 2, 3, 4, 5];
arr4.copyWithin(0, 3); // [4, 5, 3, 4, 5]

// Negative indices
arr4.copyWithin(-2, -3, -1);
```

---

### Q150: How do you create an array from scratch with values?

**Answer:**

Several approaches: `Array()` constructor, `Array.from()`, `Array.of()`, literal, spread.

```js
// Array literal
const arr1 = [1, 2, 3, 4, 5];

// Array constructor (length)
const arr2 = new Array(5); // [empty x 5]
arr2.fill(0); // [0, 0, 0, 0, 0]

// Array.of (no length confusion)
const arr3 = Array.of(5); // [5]
const arr4 = Array.of(1, 2, 3); // [1, 2, 3]

// Array.from with map
const arr5 = Array.from({ length: 5 }, (_, i) => i); // [0, 1, 2, 3, 4]
const arr6 = Array.from({ length: 5 }, () => Math.random());

// Spread with array methods
const arr7 = [...Array(10).keys()]; // [0, 1, 2, ..., 9]
const arr8 = [...Array(10)].map((_, i) => i * 2); // [0, 2, 4, ..., 18]

// Loop-based
function range(start, end) {
  return Array.from({ length: end - start + 1 }, (_, i) => start + i);
}
range(3, 7); // [3, 4, 5, 6, 7]
```

---

### Q151: How do you check if two arrays are equal?

**Answer:**

Reference equality (`===`) checks if same array. Value equality requires comparing elements recursively.

```js
const a = [1, 2, 3];
const b = [1, 2, 3];
const c = a;

a === b; // false (different references)
a === c; // true (same reference)

// Shallow array equality
function shallowArrayEqual(a, b) {
  if (a.length !== b.length) return false;
  return a.every((val, i) => val === b[i]);
}

// Deep array equality
function deepArrayEqual(a, b) {
  if (a === b) return true;
  if (a.length !== b.length) return false;
  return a.every((val, i) => {
    if (Array.isArray(val) && Array.isArray(b[i])) {
      return deepArrayEqual(val, b[i]);
    }
    return val === b[i];
  });
}

// JSON.stringify (ordered keys, no circular refs)
JSON.stringify(a) === JSON.stringify(b); // true

// Lodash isEqual handles edge cases
```

---

### Q152: How do you convert between arrays and objects?

**Answer:**

Use `Object.entries()`/`Object.fromEntries()` for object-to-array, or manual iteration.

```js
// Object to array of key-value pairs
const obj = { a: 1, b: 2, c: 3 };

const entries = Object.entries(obj);
// [['a', 1], ['b', 2], ['c', 3]]

const keys = Object.keys(obj);
// ['a', 'b', 'c']

const values = Object.values(obj);
// [1, 2, 3]

// Array of pairs back to object
const pairs = [['name', 'Alice'], ['age', 30]];
const backToObj = Object.fromEntries(pairs);
// { name: 'Alice', age: 30 }

// Array to object with index as key
const arr = ['a', 'b', 'c'];
const indexed = { ...arr };
// { '0': 'a', '1': 'b', '2': 'c' }

// Array to object with custom mapping
const users = ['Alice', 'Bob', 'Charlie'];
const usersObj = Object.fromEntries(users.map((name, i) => [i, name]));
// { '0': 'Alice', '1': 'Bob', '2': 'Charlie' }

// Array of objects to object keyed by property
const items = [{ id: 1, val: 'a' }, { id: 2, val: 'b' }];
const byId = Object.fromEntries(items.map(item => [item.id, item]));
// { '1': { id: 1, val: 'a' }, '2': { id: 2, val: 'b' } }
```

---

### Q153: What is the difference between `push`/`pop` and `unshift`/`shift`?

**Answer:**

`push`/`pop` operate at the end (O(1)). `unshift`/`shift` operate at the beginning (O(n) - all elements must shift).

```js
const arr = [1, 2, 3];

// push - add to end
arr.push(4); // [1, 2, 3, 4], returns 4 (new length)

// pop - remove from end
const last = arr.pop(); // last = 4, arr = [1, 2, 3]

// unshift - add to beginning
arr.unshift(0); // [0, 1, 2, 3], returns 4 (new length)

// shift - remove from beginning
const first = arr.shift(); // first = 0, arr = [1, 2, 3]

// Performance comparison (unshift/shift are slower)
const big = [];
console.time('push');
for (let i = 0; i < 100000; i++) big.push(i);
console.timeEnd('push'); // fast

console.time('unshift');
for (let i = 0; i < 100000; i++) big.unshift(i);
console.timeEnd('unshift'); // MUCH slower

// If you need to prepend often, use a Deque or reverse the array
```

---

### Q154: How do you merge two arrays?

**Answer:**

Use spread, `concat()`, or push with spread.

```js
const arr1 = [1, 2, 3];
const arr2 = [4, 5, 6];

// Spread
const merged = [...arr1, ...arr2]; // [1, 2, 3, 4, 5, 6]

// concat
const merged2 = arr1.concat(arr2);
// [1, 2, 3, 4, 5, 6]

// concat multiple
const merged3 = arr1.concat(arr2, [7, 8]);

// push with spread (mutates arr1)
arr1.push(...arr2); // arr1 = [1, 2, 3, 4, 5, 6]

// Without duplicates
const a = [1, 2, 3];
const b = [3, 4, 5];
const unique = [...new Set([...a, ...b])];
// [1, 2, 3, 4, 5]

// Merge array-like objects
const nodes1 = document.querySelectorAll('.a');
const nodes2 = document.querySelectorAll('.b');
const all = [...nodes1, ...nodes2];
```

---

### Q155: How do you split/chunk an array?

**Answer:**

Use `slice` in a loop or `splice` (destructive).

```js
function chunk(arr, size) {
  const result = [];
  for (let i = 0; i < arr.length; i += size) {
    result.push(arr.slice(i, i + size));
  }
  return result;
}

chunk([1, 2, 3, 4, 5, 6, 7], 3);
// [[1, 2, 3], [4, 5, 6], [7]]

// Generator version
function* chunkGen(arr, size) {
  for (let i = 0; i < arr.length; i += size) {
    yield arr.slice(i, i + size);
  }
}

// Using from
const chunked = Array.from(
  { length: Math.ceil(arr.length / size) },
  (_, i) => arr.slice(i * size, (i + 1) * size)
);

// Pairwise
function pairwise(arr) {
  return arr.slice(0, -1).map((item, i) => [item, arr[i + 1]]);
}
pairwise([1, 2, 3, 4]); // [[1, 2], [2, 3], [3, 4]]
```

---

### Q156: How do you find the intersection/difference/union of arrays?

**Answer:**

Use Set operations with filter.

```js
const arr1 = [1, 2, 3, 4, 5];
const arr2 = [4, 5, 6, 7, 8];

// Intersection
const intersection = arr1.filter(x => arr2.includes(x));
// [4, 5]

// Difference (in arr1 but not arr2)
const difference = arr1.filter(x => !arr2.includes(x));
// [1, 2, 3]

// Symmetric difference
const symmetricDiff = [
  ...arr1.filter(x => !arr2.includes(x)),
  ...arr2.filter(x => !arr1.includes(x))
];
// [1, 2, 3, 6, 7, 8]

// Union
const union = [...new Set([...arr1, ...arr2])];
// [1, 2, 3, 4, 5, 6, 7, 8]

// For large arrays, use Set for O(1) lookup
const set2 = new Set(arr2);
const intersectionFast = arr1.filter(x => set2.has(x));
// [4, 5]
```

---

### Q157: How does `at()` work for arrays?

**Answer:**

`at()` (ES2022) accepts positive and negative indices. Negative indices count from the end. Unlike bracket notation, negative indexing works.

```js
const arr = ['a', 'b', 'c', 'd', 'e'];

// Positive index
arr.at(0); // 'a'
arr.at(2); // 'c'

// Negative index (from the end)
arr.at(-1); // 'e'
arr.at(-2); // 'd'

// Equivalent bracket notation
arr[0]; // 'a'
arr[arr.length - 1]; // 'e'
arr[arr.length - 2]; // 'd'

// at() is cleaner for negative indexing
// Also works on strings: 'hello'.at(-1) // 'o'

// Use case: last element
arr.at(-1); // cleaner than arr[arr.length - 1]
```

---

### Q158: How do you implement a custom `forEach` for arrays?

**Answer:**

```js
Array.prototype.myForEach = function(callback, thisArg) {
  for (let i = 0; i < this.length; i++) {
    if (i in this) { // skip holes
      callback.call(thisArg, this[i], i, this);
    }
  }
};

// Implementation with edge cases
Array.prototype.myForEach = function(callback, thisArg) {
  if (typeof callback !== 'function') {
    throw new TypeError(callback + ' is not a function');
  }
  const arr = Object(this);
  const len = arr.length >>> 0; // ensure positive integer
  for (let i = 0; i < len; i++) {
    if (i in arr) {
      callback.call(thisArg, arr[i], i, arr);
    }
  }
};

[1, 2, 3].myForEach(n => console.log(n * 2)); // 2, 4, 6
```

---

### Q159: How do you implement a custom `map`?

**Answer:**

```js
Array.prototype.myMap = function(callback, thisArg) {
  const result = new Array(this.length);
  for (let i = 0; i < this.length; i++) {
    if (i in this) {
      result[i] = callback.call(thisArg, this[i], i, this);
    }
  }
  return result;
};

// With error handling
Array.prototype.myMap = function(callback, thisArg) {
  if (typeof callback !== 'function') {
    throw new TypeError(callback + ' is not a function');
  }
  const arr = Object(this);
  const len = arr.length >>> 0;
  const result = new Array(len);
  for (let i = 0; i < len; i++) {
    if (i in arr) {
      result[i] = callback.call(thisArg, arr[i], i, arr);
    }
  }
  return result;
};

[1, 2, 3].myMap(n => n * 2); // [2, 4, 6]
```

---

### Q160: How do you implement a custom `filter`?

**Answer:**

```js
Array.prototype.myFilter = function(callback, thisArg) {
  const result = [];
  for (let i = 0; i < this.length; i++) {
    if (i in this) {
      if (callback.call(thisArg, this[i], i, this)) {
        result.push(this[i]);
      }
    }
  }
  return result;
};

// Example
[1, 2, 3, 4, 5].myFilter(n => n > 2); // [3, 4, 5]

// Close over sparse arrays
const sparse = [1, , 3]; // has hole
sparse.myFilter(n => n !== undefined); // [1, 3] (skips hole)
```

---

### Q161: How do you implement a custom `reduce`?

**Answer:**

```js
Array.prototype.myReduce = function(callback, initialValue) {
  if (typeof callback !== 'function') {
    throw new TypeError(callback + ' is not a function');
  }
  const arr = Object(this);
  const len = arr.length >>> 0;
  let accumulator = initialValue;
  let startIndex = 0;

  if (arguments.length < 2) {
    // Find first non-hole index
    while (startIndex < len && !(startIndex in arr)) {
      startIndex++;
    }
    if (startIndex >= len) {
      throw new TypeError('Reduce of empty array with no initial value');
    }
    accumulator = arr[startIndex++];
  }

  for (let i = startIndex; i < len; i++) {
    if (i in arr) {
      accumulator = callback(accumulator, arr[i], i, arr);
    }
  }
  return accumulator;
};

[1, 2, 3].myReduce((a, b) => a + b); // 6
[]; // TypeError without initial value
``` 
```
---

# PHASE 4: DOM & BROWSER (Q162–Q220)

---

### Q162: What is the DOM?

**Answer:**

The Document Object Model (DOM) is a programming interface for HTML/XML documents. It represents the document as a tree of nodes.

```js
document.getElementById('myId');
document.querySelector('.myClass');
document.querySelectorAll('div');

const el = document.querySelector('div');
el.parentNode;
el.childNodes;
el.children;
el.firstChild;
el.lastChild;
el.nextElementSibling;
el.previousElementSibling;
```

---

### Q163: What is event bubbling?

**Answer:**

Event bubbling means an event triggered on a nested element propagates upward through ancestors.

```html
<div id="outer">
  <div id="inner">
    <button id="btn">Click</button>
  </div>
</div>
```

```js
document.getElementById('outer').addEventListener('click', () => console.log('Outer'));
document.getElementById('inner').addEventListener('click', () => console.log('Inner'));
document.getElementById('btn').addEventListener('click', () => console.log('Button'));

// Clicking button: 'Button', 'Inner', 'Outer' (bubbles up)
```

---

### Q164: What is event capturing?

**Answer:**

Event capturing propagates from root down to target. Use `true` or `{ capture: true }` as third argument.

```js
document.getElementById('outer').addEventListener('click', () => {
  console.log('Outer capture');
}, true);

document.getElementById('inner').addEventListener('click', () => {
  console.log('Inner capture');
}, true);

document.getElementById('btn').addEventListener('click', () => {
  console.log('Target');
}, true);

// Clicking button: 'Outer capture', 'Inner capture', 'Target'
// Then bubbling phase runs
```

---

### Q165: What is event delegation?

**Answer:**

Event delegation uses bubbling to handle events for many elements by attaching a single listener to a parent.

```js
// Without delegation
document.querySelectorAll('.item').forEach(item => {
  item.addEventListener('click', () => console.log('Item clicked'));
});

// With delegation
document.querySelector('#list').addEventListener('click', (e) => {
  const item = e.target.closest('.item');
  if (item) {
    console.log('Item clicked:', item.textContent);
  }
});

// Dynamic items work automatically
const newItem = document.createElement('li');
newItem.className = 'item';
newItem.textContent = 'New';
list.appendChild(newItem);
// No need to add listener
```

---

### Q166: What are `preventDefault()` and `stopPropagation()`?

**Answer:**

`preventDefault()` prevents default browser action. `stopPropagation()` stops event from bubbling/capturing further.

```js
// preventDefault
document.querySelector('a').addEventListener('click', (e) => {
  e.preventDefault(); // link won't navigate
});

document.querySelector('form').addEventListener('submit', (e) => {
  e.preventDefault(); // form won't submit
});

// stopPropagation
document.querySelector('#inner').addEventListener('click', (e) => {
  e.stopPropagation(); // stops bubbling
});

document.querySelector('#outer').addEventListener('click', () => {
  console.log('This never runs for inner clicks');
});

// stopImmediatePropagation - stops other listeners on same element
btn.addEventListener('click', (e) => {
  e.stopImmediatePropagation();
});
btn.addEventListener('click', () => console.log('Never runs'));
```

---

### Q167: What is the difference between `e.target` and `e.currentTarget`?

**Answer:**

`e.target` is the element that triggered the event. `e.currentTarget` is the element the listener was attached to.

```js
document.getElementById('list').addEventListener('click', (e) => {
  console.log('target:', e.target.tagName);   // LI (what was clicked)
  console.log('currentTarget:', e.currentTarget.id); // 'list' (listener element)
});
```

---

### Q168: How do `localStorage` and `sessionStorage` differ?

**Answer:**

`localStorage` persists until deleted. `sessionStorage` clears when tab closes. Both per-origin, store strings.

```js
// localStorage - persists
localStorage.setItem('key', 'value');
localStorage.getItem('key');
localStorage.removeItem('key');
localStorage.clear();

// sessionStorage - cleared on tab close
sessionStorage.setItem('temp', 'data');
sessionStorage.getItem('temp');

// Both only store strings
localStorage.setItem('obj', JSON.stringify({ a: 1 }));
const obj = JSON.parse(localStorage.getItem('obj'));

// Storage event (other tabs)
window.addEventListener('storage', (e) => {
  console.log('Changed:', e.key, e.oldValue, e.newValue);
});
```

---

### Q169: How do cookies differ from localStorage?

**Answer:**

Cookies are sent with every request (~4KB). localStorage is client-only (~5MB+). Cookies have expiration, HttpOnly, Secure, SameSite flags.

```js
// Set cookie
document.cookie = 'theme=dark; path=/; max-age=' + 60*60*24*7;

// Read all cookies
console.log(document.cookie);

// Parse cookies
function getCookie(name) {
  const match = document.cookie.match(new RegExp('(^| )' + name + '=([^;]+)'));
  return match ? match[2] : null;
}

// Delete cookie
document.cookie = 'theme=; max-age=0; path=/';
```

---

### Q170: How does the Fetch API work?

**Answer:**

`fetch()` returns a Promise resolving to Response. Supports methods, headers, body.

```js
// GET
fetch('https://api.example.com/users')
  .then(res => {
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    return res.json();
  })
  .then(data => console.log(data))
  .catch(err => console.error(err));

// POST
fetch('https://api.example.com/users', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ name: 'Alice' })
});

// Different response types
const text = await fetch(url).then(r => r.text());
const json = await fetch(url).then(r => r.json());
const blob = await fetch(url).then(r => r.blob());

// Upload file
const formData = new FormData();
formData.append('file', fileInput.files[0]);
fetch('/upload', { method: 'POST', body: formData });
```

---

### Q171: How does `AbortController` work?

**Answer:**

`AbortController` allows aborting fetch requests. Useful for timeouts and cancellation.

```js
async function fetchWithTimeout(url, timeoutMs = 5000) {
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), timeoutMs);

  try {
    const response = await fetch(url, { signal: controller.signal });
    clearTimeout(timeoutId);
    return response.json();
  } catch (err) {
    clearTimeout(timeoutId);
    if (err.name === 'AbortError') {
      throw new Error(`Request timed out after ${timeoutMs}ms`);
    }
    throw err;
  }
}

// Cancel stale requests
let currentController;
function search(query) {
  if (currentController) currentController.abort();
  currentController = new AbortController();
  return fetch(`/api/search?q=${query}`, { signal: currentController.signal });
}
```

---

### Q172: What is CORS?

**Answer:**

CORS (Cross-Origin Resource Sharing) is a browser security mechanism controlling cross-origin requests via HTTP headers.

```js
// Server headers needed:
// Access-Control-Allow-Origin: https://example.com
// Access-Control-Allow-Methods: GET, POST, PUT
// Access-Control-Allow-Headers: Content-Type, Authorization
// Access-Control-Allow-Credentials: true

// Preflight (OPTIONS) for non-simple requests
// Client-side: CORS is browser-enforced

fetch('https://api.other-domain.com/data', {
  mode: 'cors',
  credentials: 'include'
});

// Solutions for CORS:
// 1. Server adds CORS headers
// 2. Proxy server
// 3. JSONP (legacy)
```

---

### Q173: What is SOP (Same-Origin Policy)?

**Answer:**

SOP prevents scripts from accessing resources from different origins (protocol + host + port).

```js
// Same origin: https://example.com/page1 and https://example.com/page2

// Different origins:
// https vs http (different protocol)
// example.com vs api.example.com (different host)
// :80 vs :8080 (different port)

// Bypassing SOP:
// 1. CORS
// 2. Proxy
// 3. postMessage (iframe/window)
// 4. JSONP (legacy)

// postMessage example
iframe.contentWindow.postMessage('hello', 'https://other.com');

window.addEventListener('message', (e) => {
  if (e.origin !== 'https://parent.com') return;
  console.log(e.data);
});
```

---

### Q174: What is the difference between `async` and `defer`?

**Answer:**

`async` executes as soon as downloaded (no order guarantee). `defer` executes after parsing (in order). Both load async.

```html
<!-- Normal - blocks parsing -->
<script src="script.js"></script>

<!-- async - downloads async, executes ASAP -->
<script async src="analytics.js"></script>

<!-- defer - downloads async, executes after parsing, in order -->
<script defer src="app.js"></script>
```

```js
// DOMContentLoaded:
// - async: fires before async scripts complete
// - defer: fires after all defer scripts execute

// Use async for: analytics, ads (independent)
// Use defer for: scripts needing DOM (main app)
```

---

### Q175: What is `requestAnimationFrame`?

**Answer:**

`requestAnimationFrame` schedules a function before the next repaint (~60fps). Pauses in background tabs, more efficient than setTimeout for animations.

```js
function animate(time) {
  element.style.transform = `translateX(${position}px)`;
  position += 2;
  if (position < 500) {
    requestAnimationFrame(animate);
  }
}
requestAnimationFrame(animate);

// FPS-independent animation
let lastTime = 0;
function animate(time) {
  const delta = time - lastTime;
  lastTime = time;
  position += delta * 0.1; // 100px/sec
  element.style.transform = `translateX(${position}px)`;
  if (position < 500) requestAnimationFrame(animate);
}
requestAnimationFrame(animate);

// Cancel
const id = requestAnimationFrame(animate);
cancelAnimationFrame(id);
```

---

### Q176: What are Web Workers?

**Answer:**

Web Workers run JavaScript in a separate thread. No DOM access. Communication via `postMessage`.

```js
// main.js
const worker = new Worker('worker.js');
worker.postMessage({ type: 'compute', data: [1, 2, 3] });
worker.onmessage = (e) => console.log('Result:', e.data);
worker.terminate();

// worker.js
self.onmessage = (e) => {
  const result = e.data.data.reduce((a, b) => a + b, 0);
  self.postMessage({ type: 'result', data: result });
};

// Transferable objects (zero-copy)
worker.postMessage(largeBuffer, [largeBuffer]);

// SharedWorker (shared across tabs)
const sharedWorker = new SharedWorker('shared.js');
sharedWorker.port.postMessage('hello');
```

---

### Q177: What are Service Workers?

**Answer:**

Service Workers act as a programmable network proxy enabling offline support, caching, and push notifications.

```js
// Register
if ('serviceWorker' in navigator) {
  navigator.serviceWorker.register('/sw.js');
}

// sw.js
self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open('v1').then(cache => cache.addAll([
      '/', '/index.html', '/styles.css', '/app.js'
    ]))
  );
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then(keys =>
      Promise.all(keys.filter(k => k !== 'v1').map(caches.delete))
    )
  );
});

self.addEventListener('fetch', (event) => {
  event.respondWith(
    caches.match(event.request)
      .then(cached => cached || fetch(event.request))
      .catch(() => caches.match('/offline.html'))
  );
});

// Push notifications
self.addEventListener('push', (event) => {
  const data = event.data.json();
  event.waitUntil(
    self.registration.showNotification(data.title, { body: data.body })
  );
});
```

---

### Q178: What is IntersectionObserver?

**Answer:**

IntersectionObserver detects when an element enters/leaves the viewport. Used for lazy loading, infinite scroll, animations.

```js
const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.src = entry.target.dataset.src; // lazy load
      observer.unobserve(entry.target);
    }
  });
}, {
  root: null,
  rootMargin: '200px',
  threshold: 0.1
});

document.querySelectorAll('.lazy').forEach(img => observer.observe(img));

// Infinite scroll
const sentinel = document.querySelector('#sentinel');
const listObserver = new IntersectionObserver((entries) => {
  if (entries[0].isIntersecting) loadMoreItems();
});
listObserver.observe(sentinel);

// Track visibility ratios
const adObserver = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    console.log('Visibility ratio:', entry.intersectionRatio);
  });
}, { threshold: [0, 0.25, 0.5, 0.75, 1] });
```

---

### Q179: What is MutationObserver?

**Answer:**

MutationObserver watches for DOM changes (child nodes, attributes, text). More efficient than polling.

```js
const observer = new MutationObserver((mutations) => {
  mutations.forEach(mutation => {
    if (mutation.type === 'childList') {
      console.log('Added:', mutation.addedNodes);
      console.log('Removed:', mutation.removedNodes);
    }
    if (mutation.type === 'attributes') {
      console.log(`Attribute ${mutation.attributeName} changed`);
    }
  });
});

observer.observe(target, {
  childList: true,
  attributes: true,
  attributeFilter: ['class', 'style'],
  characterData: true,
  subtree: true
});

// Disconnect
observer.disconnect();

// Use cases: detect third-party changes, react to dynamic content
```

---

### Q180: How do you create and dispatch custom events?

**Answer:**

Use `CustomEvent` with `dispatchEvent()`.

```js
const event = new CustomEvent('userLogin', {
  detail: { userId: 123, name: 'Alice' },
  bubbles: true,
  cancelable: true
});

document.dispatchEvent(event);

document.addEventListener('userLogin', (e) => {
  console.log('User logged in:', e.detail);
});

// From elements
el.dispatchEvent(new CustomEvent('itemSelected', {
  detail: { id: 5 },
  bubbles: true
}));

el.parentElement.addEventListener('itemSelected', (e) => {
  console.log('Item selected:', e.detail.id);
});
```

---

### Q181: What is `innerHTML` vs `textContent` vs `innerText`?

**Answer:**

`innerHTML` parses HTML. `textContent` returns all text (includes hidden). `innerText` respects CSS (no hidden text, triggers reflow).

```js
const div = document.querySelector('div');
div.innerHTML = '<span style="display:none">Hidden</span>Visible';
console.log(div.textContent); // 'HiddenVisible'
console.log(div.innerText); // 'Visible' (respects display:none)

// Security: never innerHTML with user input (XSS risk)
div.textContent = userInput; // safe

// Creating elements safely
const span = document.createElement('span');
span.textContent = userInput;
div.appendChild(span);
```

---

### Q182: What is `appendChild` vs `append`?

**Answer:**

`appendChild` returns node, accepts only Node. `append` returns undefined, accepts multiple Nodes and strings.

```js
const parent = document.querySelector('#parent');
const child = document.createElement('div');

// appendChild
const returned = parent.appendChild(child);
console.log(returned === child); // true

// append - multiple, strings
parent.append('Some text', child, anotherChild);

// prepend - like append but at beginning
parent.prepend(child);

// before, after, replaceWith, remove (modern)
child.before(sibling);
child.after(sibling);
child.replaceWith(newChild);
child.remove(); // no parent needed
```

---

### Q183: How do you handle forms with JavaScript?

**Answer:**

Use `FormData` and `e.preventDefault()`.

```js
const form = document.querySelector('#myForm');

form.addEventListener('submit', (e) => {
  e.preventDefault();

  const formData = new FormData(form);
  const data = Object.fromEntries(formData.entries());
  console.log(data);

  // Multiple values (checkboxes)
  const hobbies = formData.getAll('hobbies');

  // Validation
  const email = form.elements.email;
  if (!email.validity.valid) {
    console.log(email.validationMessage);
    return;
  }

  fetch('/api/submit', {
    method: 'POST',
    body: formData, // multipart
  });
});
```

---

### Q184: What are data attributes (`data-*`)?

**Answer:**

Store custom data on HTML elements. Access via `dataset` (camelCase).

```html
<div id="user" data-id="123" data-role="admin">User Card</div>
```

```js
const user = document.querySelector('#user');
console.log(user.dataset.id); // '123'
console.log(user.dataset.role); // 'admin'

user.dataset.status = 'active';

// CSS select
document.querySelector('[data-role="admin"]');
```

---

### Q185: What is `requestIdleCallback`?

**Answer:**

Schedules a function to run during browser idle periods. Used for non-critical tasks.

```js
requestIdleCallback((deadline) => {
  while (deadline.timeRemaining() > 0 && tasks.length > 0) {
    processTask(tasks.shift());
  }
  if (tasks.length > 0) {
    requestIdleCallback(processTasks, { timeout: 2000 });
  }
});

// Use cases: analytics, logging, prefetching
requestIdleCallback(() => {
  sendAnalyticsData();
});
```

---

### Q186: How do you detect element visibility?

**Answer:**

Use IntersectionObserver or `getBoundingClientRect()`.

```js
// IntersectionObserver (recommended)
const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) console.log('Visible');
  });
});
observer.observe(element);

// getBoundingClientRect
function isInViewport(el) {
  const rect = el.getBoundingClientRect();
  return (
    rect.top >= 0 && rect.left >= 0 &&
    rect.bottom <= window.innerHeight &&
    rect.right <= window.innerWidth
  );
}

// Partially visible
function isPartiallyVisible(el) {
  const rect = el.getBoundingClientRect();
  return rect.bottom > 0 && rect.top < window.innerHeight &&
         rect.right > 0 && rect.width < window.innerWidth;
}
```

---

### Q187: How does debouncing work?

**Answer:**

Debouncing delays a function until after a period of inactivity.

```js
function debounce(fn, delay = 300) {
  let timeoutId;
  return function(...args) {
    clearTimeout(timeoutId);
    timeoutId = setTimeout(() => fn.apply(this, args), delay);
  };
}

// Usage
const searchInput = document.querySelector('#search');
const debouncedSearch = debounce(async (query) => {
  const results = await fetch(`/api/search?q=${query}`);
  console.log('Results:', await results.json());
}, 500);

searchInput.addEventListener('input', (e) => {
  debouncedSearch(e.target.value);
});
```

---

### Q188: How does throttling work?

**Answer:**

Throttling ensures a function is called at most once per interval.

```js
function throttle(fn, limit = 300) {
  let inThrottle = false;
  return function(...args) {
    if (!inThrottle) {
      fn.apply(this, args);
      inThrottle = true;
      setTimeout(() => { inThrottle = false; }, limit);
    }
  };
}

// Usage
const throttledScroll = throttle(() => {
  console.log('Scroll position:', window.scrollY);
}, 200);

window.addEventListener('scroll', throttledScroll, { passive: true });
```

---

### Q189: How do you implement drag and drop?

**Answer:**

Use HTML5 Drag and Drop API or mouse events.

```js
// HTML5 DnD
const draggable = document.querySelector('#draggable');
const dropzone = document.querySelector('#dropzone');

draggable.addEventListener('dragstart', (e) => {
  e.dataTransfer.setData('text/plain', draggable.id);
  e.dataTransfer.effectAllowed = 'move';
});

dropzone.addEventListener('dragover', (e) => {
  e.preventDefault();
  e.dataTransfer.dropEffect = 'move';
});

dropzone.addEventListener('drop', (e) => {
  e.preventDefault();
  const id = e.dataTransfer.getData('text/plain');
  dropzone.appendChild(document.getElementById(id));
});

// Mouse-based drag
let isDragging = false, offsetX, offsetY;
element.addEventListener('mousedown', (e) => {
  isDragging = true;
  const rect = element.getBoundingClientRect();
  offsetX = e.clientX - rect.left;
  offsetY = e.clientY - rect.top;
});

document.addEventListener('mousemove', (e) => {
  if (!isDragging) return;
  element.style.left = (e.clientX - offsetX) + 'px';
  element.style.top = (e.clientY - offsetY) + 'px';
});

document.addEventListener('mouseup', () => { isDragging = false; });
```

---

### Q190: What is ResizeObserver?

**Answer:**

ResizeObserver watches for element size changes.

```js
const observer = new ResizeObserver((entries) => {
  entries.forEach(entry => {
    const { width, height } = entry.contentRect;
    console.log(`${entry.target.id}: ${width}x${height}`);
  });
});

observer.observe(document.querySelector('#resizable'));

// Responsive adjustments
const widgetObserver = new ResizeObserver((entries) => {
  entries.forEach(entry => {
    entry.target.classList.toggle('compact', entry.contentRect.width < 300);
  });
});
```

---

### Q191: What is the History API?

**Answer:**

The History API (`pushState`, `popstate`) manages browser history without page reload. Used for SPA routing.

```js
// Push new entry
history.pushState({ page: 1 }, 'Title', '/page1');

// Replace current
history.replaceState({ page: 2 }, 'Title', '/page2');

// Listen for navigation
window.addEventListener('popstate', (e) => {
  console.log('State:', e.state);
  updatePage(e.state ? e.state.page : 0);
});

history.back();
history.forward();
history.go(-2);
```

---

### Q192: What is the `beforeunload` event?

**Answer:**

Fires when page is about to be unloaded. Used to warn about unsaved changes.

```js
let hasUnsavedChanges = false;

window.addEventListener('beforeunload', (e) => {
  if (hasUnsavedChanges) {
    e.preventDefault();
    e.returnValue = '';
  }
});

// Track changes
document.querySelector('#editor').addEventListener('input', () => {
  hasUnsavedChanges = true;
});

document.querySelector('#save').addEventListener('click', () => {
  saveData();
  hasUnsavedChanges = false;
});
```

---

### Q193: What is the `visibilitychange` event?

**Answer:**

Fires when tab visibility changes. Better than blur/focus for pausing activity.

```js
document.addEventListener('visibilitychange', () => {
  if (document.hidden) {
    console.log('Tab hidden - pause');
    video.pause();
    clearInterval(pollingInterval);
  } else {
    console.log('Tab visible - resume');
    video.play();
    pollingInterval = setInterval(pollServer, 5000);
  }
});

// Also useful
document.visibilityState; // 'visible' | 'hidden'
```

---

### Q194: What is Clipboard API?

**Answer:**

Async read/write access to clipboard. Requires user interaction for reading.

```js
// Write
async function copyToClipboard(text) {
  try {
    await navigator.clipboard.writeText(text);
  } catch (err) {
    console.error('Copy failed:', err);
  }
}

// Read
async function pasteFromClipboard() {
  try {
    return await navigator.clipboard.readText();
  } catch (err) {
    console.error('Paste failed:', err);
  }
}

// Fallback
function fallbackCopy(text) {
  const textarea = document.createElement('textarea');
  textarea.value = text;
  textarea.style.position = 'fixed';
  textarea.style.opacity = '0';
  document.body.appendChild(textarea);
  textarea.select();
  document.execCommand('copy');
  document.body.removeChild(textarea);
}
```

---

### Q195: What is `window.matchMedia`?

**Answer:**

Evaluates CSS media queries in JavaScript. Supports `matches` and `change` events.

```js
const isMobile = window.matchMedia('(max-width: 768px)');
console.log('Is mobile:', isMobile.matches);

const darkMode = window.matchMedia('(prefers-color-scheme: dark)');

function handleThemeChange(e) {
  document.documentElement.dataset.theme = e.matches ? 'dark' : 'light';
}
darkMode.addEventListener('change', handleThemeChange);

// Device capabilities
const hover = window.matchMedia('(hover: hover)');
const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
```

---

### Q196: What is the Notification API?

**Answer:**

Displays system notifications. Requires permission.

```js
async function requestNotificationPermission() {
  if (!('Notification' in window)) return false;
  const permission = await Notification.requestPermission();
  return permission === 'granted';
}

function showNotification(title, options = {}) {
  if (Notification.permission === 'granted') {
    const notification = new Notification(title, {
      body: options.body,
      icon: options.icon || '/icon.png',
      tag: options.tag,
      data: options.data
    });

    notification.addEventListener('click', () => {
      window.focus();
      notification.close();
    });

    return notification;
  }
}
```

---

### Q197: What is `beforeinstallprompt`?

**Answer:**

Event for triggering PWA install banner programmatically.

```js
let deferredPrompt;

window.addEventListener('beforeinstallprompt', (e) => {
  e.preventDefault();
  deferredPrompt = e;
  document.querySelector('#install-btn').style.display = 'block';
});

document.querySelector('#install-btn').addEventListener('click', async () => {
  if (!deferredPrompt) return;
  deferredPrompt.prompt();
  const { outcome } = await deferredPrompt.userChoice;
  console.log(outcome === 'accepted' ? 'Installed' : 'Declined');
  deferredPrompt = null;
});

window.addEventListener('appinstalled', () => {
  console.log('PWA installed');
});
```

---

### Q198: What is the Fullscreen API?

**Answer:**

Allows elements to display fullscreen. Requires user gesture.

```js
async function enterFullscreen(element = document.documentElement) {
  try {
    await element.requestFullscreen();
  } catch (err) {
    console.error('Fullscreen failed:', err);
  }
}

async function exitFullscreen() {
  await document.exitFullscreen();
}

// Check state
document.fullscreenElement;
document.fullscreenEnabled;

document.addEventListener('fullscreenchange', () => {
  console.log('Fullscreen:', !!document.fullscreenElement);
});
```

---

### Q199: What is the Geolocation API?

**Answer:**

Access device location. Requires user permission.

```js
navigator.geolocation.getCurrentPosition(
  (position) => {
    console.log('Lat:', position.coords.latitude);
    console.log('Lng:', position.coords.longitude);
    console.log('Accuracy:', position.coords.accuracy);
  },
  (error) => {
    switch (error.code) {
      case error.PERMISSION_DENIED: console.error('Denied'); break;
      case error.POSITION_UNAVAILABLE: console.error('Unavailable'); break;
      case error.TIMEOUT: console.error('Timeout'); break;
    }
  },
  { enableHighAccuracy: true, timeout: 10000, maximumAge: 60000 }
);

// Watch position
const watchId = navigator.geolocation.watchPosition(updatePosition);
navigator.geolocation.clearWatch(watchId);
```

---

### Q200: How do you implement lazy loading images?

**Answer:**

Use native `loading="lazy"` or IntersectionObserver.

```js
// Native (modern browsers)
// <img src="placeholder.jpg" data-src="real.jpg" loading="lazy">

// IntersectionObserver
const imageObserver = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      const img = entry.target;
      img.src = img.dataset.src;
      img.removeAttribute('data-src');
      img.classList.add('loaded');
      imageObserver.unobserve(img);
    }
  });
}, { rootMargin: '200px' });

document.querySelectorAll('img[data-src]').forEach(img => imageObserver.observe(img));
```

---

### Q201: What are browser storage options?

**Answer:**

Cookies (~4KB), localStorage (~5MB), sessionStorage (~5MB), IndexedDB (unlimited), Cache API.

```js
// IndexedDB - async, structured, large
const db = await indexedDB.open('MyDB', 1);
const store = db.createObjectStore('items', { keyPath: 'id' });
await store.put({ id: 1, name: 'Alice' });

// Cache API (Service Workers)
const cache = await caches.open('v1');
await cache.put('/data.json', new Response(JSON.stringify(data)));
const cached = await cache.match('/data.json');

// Which to use:
// Key-value small: localStorage
// Server comm: Cookies
// Large structured: IndexedDB
// Offline: Cache API
```

---

### Q202: What is the Shadow DOM?

**Answer:**

Shadow DOM encapsulates DOM subtrees and styles, creating a scoped boundary.

```js
const host = document.querySelector('#host');
const shadow = host.attachShadow({ mode: 'open' });

shadow.innerHTML = `
  <style>h2 { color: blue; }</style>
  <h2>Shadow Title</h2>
  <slot></slot>
`;

// Custom element with Shadow DOM
class MyWidget extends HTMLElement {
  constructor() {
    super();
    this.attachShadow({ mode: 'open' });
  }
  connectedCallback() {
    this.shadowRoot.innerHTML = `<p>Hello from shadow</p>`;
  }
}
customElements.define('my-widget', MyWidget);
```

---

### Q203: What are Web Components?

**Answer:**

Web Components = Custom Elements + Shadow DOM + HTML Templates.

```js
class UserCard extends HTMLElement {
  static get observedAttributes() { return ['name']; }

  constructor() {
    super();
    this.attachShadow({ mode: 'open' });
    this.shadowRoot.innerHTML = `
      <style>.card { border: 1px solid; padding: 8px; }</style>
      <div class="card"><span class="name"></span></div>
    `;
  }

  connectedCallback() { this.render(); }
  attributeChangedCallback() { this.render(); }

  render() {
    this.shadowRoot.querySelector('.name').textContent =
      this.getAttribute('name') || 'Guest';
  }
}
customElements.define('user-card', UserCard);
```

---

### Q204: What is `window.postMessage`?

**Answer:**

`postMessage` enables cross-origin communication between windows/iframes.

```js
// In parent
const iframe = document.querySelector('iframe');
iframe.contentWindow.postMessage(
  { type: 'update', data: { theme: 'dark' } },
  'https://trusted-origin.com'
);

window.addEventListener('message', (e) => {
  if (e.origin !== 'https://trusted-origin.com') return;
  console.log('Received:', e.data);
});

// In iframe
window.addEventListener('message', (e) => {
  if (e.origin !== 'https://parent.com') return;
  e.source.postMessage({ type: 'response' }, e.origin);
});
```

---

### Q205: How do you implement virtual scrolling?

**Answer:**

Render only visible items, recycle DOM elements for large lists.

```js
class VirtualScroller {
  constructor(container, { itemHeight, totalItems, renderItem }) {
    this.container = container;
    this.itemHeight = itemHeight;
    this.totalItems = totalItems;
    this.renderItem = renderItem;
    this.container.style.overflowY = 'auto';
    this.container.style.position = 'relative';

    const totalHeight = itemHeight * totalItems;
    this.spacer = document.createElement('div');
    this.spacer.style.height = `${totalHeight}px`;
    this.container.appendChild(this.spacer);

    this.viewport = document.createElement('div');
    this.viewport.style.position = 'absolute';
    this.viewport.style.width = '100%';
    this.container.appendChild(this.viewport);

    this.container.addEventListener('scroll', () => this.update());
    this.update();
  }

  update() {
    const scrollTop = this.container.scrollTop;
    const height = this.container.clientHeight;
    const start = Math.floor(scrollTop / this.itemHeight);
    const end = Math.min(start + Math.ceil(height / this.itemHeight) + 1, this.totalItems);

    this.viewport.style.transform = `translateY(${start * this.itemHeight}px)`;
    this.viewport.innerHTML = '';
    for (let i = start; i < end; i++) {
      const item = this.renderItem(i);
      item.style.height = `${this.itemHeight}px`;
      this.viewport.appendChild(item);
    }
  }
}

// Usage
new VirtualScroller(document.querySelector('#list'), {
  itemHeight: 50,
  totalItems: 100000,
  renderItem: (i) => {
    const div = document.createElement('div');
    div.textContent = `Item ${i}`;
    return div;
  }
});
```

---

### Q206: What are Pointer Events?

**Answer:**

Unify mouse, touch, and pen input. Use `pointerType` to distinguish.

```js
element.addEventListener('pointerdown', (e) => {
  console.log('Pointer type:', e.pointerType); // 'mouse'|'touch'|'pen'
  console.log('Pressure:', e.pressure);
});

// Pointer capture for drag
element.addEventListener('pointerdown', (e) => {
  e.target.setPointerCapture(e.pointerId);
});

element.addEventListener('pointermove', (e) => {
  if (e.target.hasPointerCapture(e.pointerId)) {
    // Handle drag
  }
});

// CSS touch-action
// .no-touch { touch-action: none; }
// .pan-x { touch-action: pan-x; }
```

---

### Q207: What is the Screen Capture API?

**Answer:**

`getDisplayMedia` captures screen/window content.

```js
async function startScreenCapture() {
  const stream = await navigator.mediaDevices.getDisplayMedia({
    video: { cursor: 'always' },
    audio: false
  });

  const video = document.querySelector('#preview');
  video.srcObject = stream;

  stream.getVideoTracks()[0].addEventListener('ended', () => {
    console.log('Sharing stopped');
  });

  return stream;
}

// Record screen
async function recordScreen() {
  const stream = await navigator.mediaDevices.getDisplayMedia({ video: true });
  const recorder = new MediaRecorder(stream);
  const chunks = [];

  recorder.ondataavailable = (e) => chunks.push(e.data);
  recorder.onstop = () => {
    const blob = new Blob(chunks, { type: 'video/webm' });
    const a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = 'recording.webm';
    a.click();
  };

  recorder.start();
  return recorder;
}
```

---

### Q208: How does `contenteditable` work?

**Answer:**

Makes HTML elements editable. `document.execCommand` (deprecated) handles formatting.

```html
<div contenteditable="true" id="editor">Edit this</div>
```

```js
const editor = document.querySelector('#editor');
editor.addEventListener('input', () => {
  console.log('Updated:', editor.innerHTML);
});

// Formatting (deprecated but used)
document.execCommand('bold');
document.execCommand('italic');

// Sanitize output
function sanitizeHTML(html) {
  const template = document.createElement('template');
  template.innerHTML = html;
  template.content.querySelectorAll('script, style, iframe')
    .forEach(el => el.remove());
  return template.innerHTML;
}
```

---

### Q209: How do you implement infinite scrolling?

**Answer:**

Use IntersectionObserver on a sentinel element.

```js
class InfiniteScroller {
  constructor({ container, fetchMore }) {
    this.container = container;
    this.fetchMore = fetchMore;
    this.page = 1;
    this.loading = false;
    this.hasMore = true;

    this.sentinel = document.createElement('div');
    this.sentinel.style.height = '1px';
    this.container.appendChild(this.sentinel);

    this.observer = new IntersectionObserver((entries) => {
      if (entries[0].isIntersecting && !this.loading && this.hasMore) {
        this.load();
      }
    }, { rootMargin: '200px' });

    this.observer.observe(this.sentinel);
  }

  async load() {
    this.loading = true;
    try {
      const items = await this.fetchMore(this.page);
      if (items.length === 0) {
        this.hasMore = false;
        return;
      }
      items.forEach(item => this.container.appendChild(this.createItem(item)));
      this.page++;
    } finally {
      this.loading = false;
    }
  }
}
```

---

### Q210: How do you implement a simple reactive binding?

**Answer:**

Use Proxy to detect changes and update DOM.

```js
function reactive(obj, onChange) {
  return new Proxy(obj, {
    set(target, prop, value) {
      const old = target[prop];
      target[prop] = value;
      if (old !== value) onChange(prop, value, old);
      return true;
    }
  });
}

function bindState(initialState) {
  const state = reactive(initialState, (prop, value) => {
    document.querySelectorAll(`[data-bind="${prop}"]`).forEach(el => {
      if (el.tagName === 'INPUT') {
        el.value = value;
      } else {
        el.textContent = value;
      }
    });
  });

  document.querySelectorAll('[data-bind]').forEach(el => {
    const prop = el.dataset.bind;
    if (el.tagName === 'INPUT') {
      el.addEventListener('input', () => state[prop] = el.value);
      el.value = state[prop];
    } else {
      el.textContent = state[prop];
    }
  });

  return state;
}

// Usage
const state = bindState({ name: 'Alice' });
// <input data-bind="name"> <span data-bind="name"></span>
```

---

# PHASE 5: PROMISES & ASYNC (Q211–Q270)

---

### Q211: What are the states of a Promise?

**Answer:**

A Promise has three states: `pending`, `fulfilled`, `rejected`. Once settled (fulfilled/rejected), it's immutable.

```js
const promise = new Promise((resolve, reject) => {
  // PENDING
  setTimeout(() => {
    resolve('Success!');
    // or reject(new Error('Failed'));
  }, 1000);
});

promise
  .then(value => console.log('FULFILLED:', value))
  .catch(error => console.log('REJECTED:', error))
  .finally(() => console.log('Settled'));

// Can only settle once
const single = new Promise((resolve, reject) => {
  resolve('First');
  resolve('Second'); // ignored
  reject('Error'); // ignored
});
single.then(v => console.log(v)); // 'First'
```

---

### Q212: How does Promise chaining work?

**Answer:**

Each `.then()` returns a new Promise. Return value becomes next `.then()`'s input. Errors propagate until caught.

```js
Promise.resolve(1)
  .then(n => {
    console.log(n); // 1
    return n * 2;
  })
  .then(n => {
    console.log(n); // 2
    return n * 3;
  })
  .then(n => console.log(n)); // 6

// Returning a Promise unrolls it
Promise.resolve(1)
  .then(n => new Promise(resolve => setTimeout(() => resolve(n * 2), 1000)))
  .then(n => console.log(n)); // 2 (after 1s)

// Error propagation
Promise.resolve(1)
  .then(n => { throw new Error('Oops'); })
  .then(n => console.log('Skipped')) // skipped
  .catch(err => console.log(err.message)) // 'Oops'
  .then(() => console.log('After catch')); // runs
```

---

### Q213: What is Promise.all?

**Answer:**

`Promise.all` resolves when ALL fulfill, or rejects when ANY rejects. Returns results array in order.

```js
const p1 = Promise.resolve(1);
const p2 = new Promise(resolve => setTimeout(() => resolve(2), 100));
const p3 = Promise.resolve(3);

Promise.all([p1, p2, p3])
  .then(results => console.log(results)); // [1, 2, 3]

// Rejection: fails fast
const pFail = Promise.reject(new Error('Fail'));
Promise.all([p1, pFail])
  .catch(err => console.log(err.message)); // 'Fail'

// Parallel API calls
async function fetchAll() {
  const [users, posts] = await Promise.all([
    fetch('/api/users').then(r => r.json()),
    fetch('/api/posts').then(r => r.json())
  ]);
  return { users, posts };
}

// Non-promise values wrapped
Promise.all([1, Promise.resolve(2), 3])
  .then(v => console.log(v)); // [1, 2, 3]
```

---

### Q214: What is Promise.race?

**Answer:**

`Promise.race` resolves/rejects with the first settled promise.

```js
const slow = new Promise(resolve => setTimeout(() => resolve('Slow'), 2000));
const fast = new Promise(resolve => setTimeout(() => resolve('Fast'), 500));

Promise.race([slow, fast])
  .then(result => console.log(result)); // 'Fast'

// Timeout pattern
function fetchWithTimeout(url, ms = 5000) {
  return Promise.race([
    fetch(url).then(r => r.json()),
    new Promise((_, reject) => setTimeout(() => reject(new Error('Timeout')), ms))
  ]);
}
```

---

### Q215: What is Promise.allSettled?

**Answer:**

`Promise.allSettled` waits for ALL to settle. Returns `{status, value/reason}`. Never rejects.

```js
const p1 = Promise.resolve(1);
const p2 = Promise.reject(new Error('Fail'));
const p3 = new Promise(resolve => setTimeout(resolve, 100, 3));

Promise.allSettled([p1, p2, p3]).then(results => {
  console.log(results);
  // [
  //   { status: 'fulfilled', value: 1 },
  //   { status: 'rejected', reason: Error('Fail') },
  //   { status: 'fulfilled', value: 3 }
  // ]
});

// Practical: report successes and failures
async function fetchAllData() {
  const results = await Promise.allSettled(urls.map(url =>
    fetch(url).then(r => r.json())
  ));

  const successes = results.filter(r => r.status === 'fulfilled').map(r => r.value);
  const failures = results.filter(r => r.status === 'rejected').map(r => r.reason);
  return { successes, failures };
}
```

---

### Q216: What is Promise.any?

**Answer:**

`Promise.any` resolves with first FULFILLED. All reject => `AggregateError`.

```js
const p1 = Promise.reject(new Error('E1'));
const p2 = new Promise(resolve => setTimeout(resolve, 100, 'Fast'));
const p3 = Promise.reject(new Error('E3'));

Promise.any([p1, p2, p3])
  .then(result => console.log(result)); // 'Fast'

// All reject
Promise.any([Promise.reject('E1'), Promise.reject('E2')])
  .catch(err => {
    console.log(err instanceof AggregateError); // true
    console.log(err.errors); // ['E1', 'E2']
  });
```

---

### Q217: How does async/await work?

**Answer:**

`async` functions return a Promise. `await` pauses execution (non-blocking) until the Promise settles.

```js
async function fetchUser(id) {
  const response = await fetch(`/api/users/${id}`);
  const data = await response.json();
  return data;
}

// Returns a Promise
fetchUser(1).then(user => console.log(user));

// Error handling
async function getData() {
  try {
    const user = await fetchUser(1);
    const posts = await fetch(`/api/users/${user.id}/posts`).then(r => r.json());
    return { user, posts };
  } catch (err) {
    console.error('Failed:', err);
    throw err;
  }
}

// Sequential vs Parallel
// BAD: slow
const a = await fetchA();
const b = await fetchB(); // waits for A first

// GOOD: fast
const [a, b] = await Promise.all([fetchA(), fetchB()]);
```

---

### Q218: What is callback hell and how to avoid it?

**Answer:**

Deeply nested callbacks that are hard to read. Solved by Promises, async/await, modularization.

```js
// Callback hell
getUser(1, (err, user) => {
  if (err) return handleError(err);
  getPosts(user.id, (err, posts) => {
    if (err) return handleError(err);
    getComments(posts[0].id, (err, comments) => {
      if (err) return handleError(err);
      console.log(comments);
    });
  });
});

// Promise chain
getUser(1)
  .then(user => getPosts(user.id))
  .then(posts => getComments(posts[0].id))
  .then(comments => console.log(comments))
  .catch(handleError);

// async/await
async function load() {
  try {
    const user = await getUser(1);
    const posts = await getPosts(user.id);
    const comments = await getComments(posts[0].id);
    console.log(comments);
  } catch (err) {
    handleError(err);
  }
}
```

---

### Q219: How do you promisify a callback function?

**Answer:**

Wrap in `new Promise` and call resolve/reject in callback.

```js
// Promisify fs.readFile
function readFilePromise(path) {
  return new Promise((resolve, reject) => {
    fs.readFile(path, 'utf8', (err, data) => {
      if (err) reject(err);
      else resolve(data);
    });
  });
}

// Generic promisify
function promisify(fn) {
  return function(...args) {
    return new Promise((resolve, reject) => {
      fn(...args, (err, result) => {
        if (err) reject(err);
        else resolve(result);
      });
    });
  };
}

// setTimeout to Promise
function delay(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}
await delay(1000);
```

---

### Q220: How does `queueMicrotask` work?

**Answer:**

Schedules a microtask (before macrotasks like setTimeout).

```js
console.log('1: sync');
queueMicrotask(() => console.log('2: microtask'));
Promise.resolve().then(() => console.log('3: promise microtask'));
setTimeout(() => console.log('4: macrotask'), 0);
console.log('5: sync');
// Output: 1, 5, 2, 3, 4

// Microtask queue drains completely before next macrotask
queueMicrotask(() => {
  console.log('A');
  queueMicrotask(() => console.log('B')); // also processed
});
setTimeout(() => console.log('C'), 0);
// A, B, C
```

---

### Q221: What is the event loop ordering with async/await?

**Answer:**

`await` suspends execution; the rest runs as microtask. Sync code before first await runs immediately.

```js
async function foo() {
  console.log('2: async start');
  await null;
  console.log('4: after first await');
}

console.log('1: sync start');
foo();
console.log('3: sync end');
// Output: 1, 2, 3, 4

// With Promise
async function test() {
  console.log('A');
  const result = await Promise.resolve('B');
  console.log(result);
  console.log('C');
}
console.log('1');
test();
console.log('2');
// Output: 1, A, 2, B, C
```

---

### Q222: How do you implement retry logic with Promises?

**Answer:**

Recursive retry with exponential backoff.

```js
async function fetchWithRetry(url, options = {}) {
  const maxRetries = options.retries || 3;
  const baseDelay = options.baseDelay || 1000;

  for (let attempt = 1; attempt <= maxRetries; attempt++) {
    try {
      const response = await fetch(url);
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      return await response.json();
    } catch (err) {
      if (attempt === maxRetries) throw err;
      const delay = baseDelay * Math.pow(2, attempt - 1) + Math.random() * 500;
      await new Promise(resolve => setTimeout(resolve, delay));
    }
  }
}

// Generic retry wrapper
function withRetry(fn, options = {}) {
  const maxRetries = options.retries || 3;
  return async (...args) => {
    let lastError;
    for (let i = 0; i < maxRetries; i++) {
      try { return await fn(...args); }
      catch (err) {
        lastError = err;
        if (i < maxRetries - 1) await new Promise(r => setTimeout(r, 1000 * 2 ** i));
      }
    }
    throw lastError;
  };
}
```

---

### Q223: What is the `finally` block in Promises?

**Answer:**

`.finally()` runs regardless of fulfill/reject. Used for cleanup. Doesn't receive value/error. Its return value is ignored.

```js
function fetchUsers() {
  showLoading();
  return fetch('/api/users')
    .then(r => r.json())
    .then(users => { console.log(users); return users; })
    .catch(err => { console.error(err); throw err; })
    .finally(() => hideLoading()); // always runs
}

// finally doesn't transform result
Promise.resolve(1)
  .finally(() => 'ignored')
  .then(v => console.log(v)); // 1

// finally can override rejection
Promise.reject(new Error('original'))
  .finally(() => { throw new Error('new'); })
  .catch(err => console.log(err.message)); // 'new'
```

---

### Q224: What is `Promise.resolve()` vs `new Promise(r => r())`?

**Answer:**

Both create fulfilled promises. `Promise.resolve()` handles thenables and returns same promise for promises.

```js
Promise.resolve(42).then(v => console.log(v)); // 42
new Promise(r => r(42)).then(v => console.log(v)); // 42

// Thenable unrolling
const thenable = { then(resolve) { resolve('thenable'); } };
Promise.resolve(thenable).then(v => console.log(v)); // 'thenable'

// Returns same promise for promises
const p = Promise.resolve(1);
console.log(Promise.resolve(p) === p); // true
```

---

### Q225: What is the difference between microtask and macrotask priorities?

**Answer:**

Microtasks run before macrotasks in each event loop iteration. After each macrotask, all microtasks are drained.

```js
setTimeout(() => {
  console.log('Macro 1');
  Promise.resolve().then(() => console.log('Micro in macro'));
}, 0);

setTimeout(() => console.log('Macro 2'), 0);

Promise.resolve().then(() => console.log('Micro 1'));

// Output:
// Micro 1
// Macro 1
// Micro in macro
// Macro 2
```

---

### Q226: How do you convert callback-based APIs to async/await?

**Answer:**

Wrap in Promise, then use await.

```js
// Node.js util.promisify
const { promisify } = require('util');
const readFile = promisify(fs.readFile);
const data = await readFile('file.txt', 'utf8');

// Custom promisify
function delay(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

// Event to Promise
function once(el, event) {
  return new Promise(resolve => el.addEventListener(event, resolve, { once: true }));
}
await once(button, 'click');
console.log('Button clicked');
```

---

### Q227: How do you handle async errors without try/catch?

**Answer:**

Use `.catch()` on Promises, or return `[error, result]` tuples (Go-style).

```js
// Using .catch()
fetch('/api/data')
  .then(r => r.json())
  .catch(err => ({ error: err }))
  .then(result => {
    if (result.error) {
      console.error('Failed:', result.error);
      return;
    }
    console.log('Data:', result);
  });

// Go-style error handling
async function safe(fn) {
  try {
    const result = await fn();
    return [null, result];
  } catch (err) {
    return [err, null];
  }
}

const [err, data] = await safe(() => fetch('/api/data').then(r => r.json()));
if (err) {
  console.error('Error:', err);
} else {
  console.log('Data:', data);
}
```

---

### Q228: What is the Promise constructor anti-pattern?

**Answer:**

Wrapping an existing promise in `new Promise` instead of returning it directly.

```js
// BAD: unnecessary wrapping
function bad() {
  return new Promise((resolve, reject) => {
    fetch('/api/data')
      .then(r => r.json())
      .then(resolve)
      .catch(reject);
  });
}

// GOOD: return the promise directly
function good() {
  return fetch('/api/data').then(r => r.json());
}

// GOOD for callback APIs (non-promise)
function goodPromisify() {
  return new Promise((resolve, reject) => {
    fs.readFile('file.txt', (err, data) => {
      if (err) reject(err);
      else resolve(data);
    });
  });
}
```

---

### Q229: How do you implement sequential async operations?

**Answer:**

Use `for...of`, `reduce`, or recursion.

```js
// for...of
async function sequential(urls) {
  const results = [];
  for (const url of urls) {
    const data = await fetch(url).then(r => r.json());
    results.push(data);
  }
  return results;
}

// reduce
function sequentialReduce(urls) {
  return urls.reduce((promise, url) =>
    promise.then(results =>
      fetch(url).then(r => r.json()).then(data => [...results, data])
    ), Promise.resolve([]));
}

// With concurrency limit
async function parallelLimit(tasks, limit, fn) {
  const results = [];
  const executing = [];
  for (const task of tasks) {
    const p = fn(task).then(r => results.push(r));
    executing.push(p);
    if (executing.length >= limit) {
      await Promise.race(executing);
      executing.splice(0, executing.findIndex(e => e === p) + 1);
    }
  }
  await Promise.all(executing);
  return results;
}
```

---

### Q230: How do you cancel a Promise?

**Answer:**

Promises aren't cancellable natively. Use AbortController or custom wrappers.

```js
// AbortController with fetch
const controller = new AbortController();
fetch('/api/data', { signal: controller.signal })
  .catch(err => {
    if (err.name === 'AbortError') console.log('Cancelled');
  });
controller.abort();

// Custom cancellable promise
function cancellablePromise(executor) {
  let cancel;
  const promise = new Promise((resolve, reject) => {
    cancel = () => reject(new DOMException('Cancelled', 'AbortError'));
    executor(resolve, reject);
  });
  promise.cancel = cancel;
  return promise;
}

const p = cancellablePromise((resolve) => {
  const id = setTimeout(() => resolve('Done'), 5000);
});
p.cancel();
p.catch(err => console.log(err.name)); // 'AbortError'
```

---

### Q231: How do you implement `Promise.all` manually?

**Answer:**

```js
function myPromiseAll(promises) {
  return new Promise((resolve, reject) => {
    const results = [];
    let completed = 0;
    const len = promises.length;

    if (len === 0) { resolve([]); return; }

    for (let i = 0; i < len; i++) {
      Promise.resolve(promises[i])
        .then(value => {
          results[i] = value;
          completed++;
          if (completed === len) resolve(results);
        })
        .catch(reject);
    }
  });
}

myPromiseAll([1, Promise.resolve(2), Promise.resolve(3)])
  .then(v => console.log(v)); // [1, 2, 3]
```

---

### Q232: How do you implement `Promise.race` manually?

**Answer:**

```js
function myPromiseRace(promises) {
  return new Promise((resolve, reject) => {
    for (const item of promises) {
      Promise.resolve(item).then(resolve, reject);
    }
  });
}

const slow = new Promise(resolve => setTimeout(resolve, 100, 'Slow'));
const fast = new Promise(resolve => setTimeout(resolve, 50, 'Fast'));
myPromiseRace([slow, fast]).then(v => console.log(v)); // 'Fast'
```

---

### Q233: How do you implement `Promise.allSettled` manually?

**Answer:**

```js
function myPromiseAllSettled(promises) {
  return new Promise(resolve => {
    const results = [];
    let completed = 0;
    const len = promises.length;

    if (len === 0) { resolve([]); return; }

    for (let i = 0; i < len; i++) {
      Promise.resolve(promises[i])
        .then(value => { results[i] = { status: 'fulfilled', value }; })
        .catch(reason => { results[i] = { status: 'rejected', reason }; })
        .finally(() => {
          completed++;
          if (completed === len) resolve(results);
        });
    }
  });
}
```

---

### Q234: How do you implement `Promise.any` manually?

**Answer:**

```js
function myPromiseAny(promises) {
  return new Promise((resolve, reject) => {
    let rejections = [];
    let rejected = 0;
    const len = promises.length;

    if (len === 0) {
      reject(new AggregateError([], 'All promises were rejected'));
      return;
    }

    for (let i = 0; i < len; i++) {
      Promise.resolve(promises[i])
        .then(resolve)
        .catch(reason => {
          rejections[i] = reason;
          rejected++;
          if (rejected === len) {
            reject(new AggregateError(rejections, 'All promises were rejected'));
          }
        });
    }
  });
}
```

---

### Q235: What happens when you `await` a non-Promise value?

**Answer:**

`await` wraps it with `Promise.resolve()`.

```js
async function test() {
  const a = await 42; // Promise.resolve(42)
  console.log(a); // 42

  const b = await 'hello';
  console.log(b); // 'hello'

  const c = await { key: 'value' };
  console.log(c); // { key: 'value' }
}

// await with thenable
const thenable = { then(resolve) { resolve('thenable'); } };
async function testThenable() {
  const result = await thenable;
  console.log(result); // 'thenable'
}
```

---

### Q236: What is the difference between `throw` in sync and `reject` in Promises?

**Answer:**

`throw` stops execution immediately. `reject` returns a rejected Promise; code after reject still runs.

```js
// Sync: throw stops execution
function sync() {
  throw new Error('Fail');
  console.log('Never'); // unreachable
}

// Promise: reject doesn't stop
function promise() {
  return new Promise((resolve, reject) => {
    reject(new Error('Fail'));
    console.log('After reject'); // STILL runs!
    resolve('Will be ignored'); // ignored
  });
}

// async/await: throw works like sync
async function asyncFn() {
  throw new Error('Fail');
  console.log('Never'); // unreachable
}

// Unhandled rejections
Promise.reject(new Error('Unhandled'));
// Node: unhandledRejection / browser: unhandledrejection
```

---

### Q237: How do you handle multiple sequential async operations?

**Answer:**

Use `for...of`, `reduce`, or recursion.

```js
// for...of
async function sequential(urls) {
  const results = [];
  for (const url of urls) {
    const data = await fetch(url).then(r => r.json());
    results.push(data);
  }
  return results;
}

// reduce
function sequentialReduce(urls) {
  return urls.reduce((promise, url) =>
    promise.then(results =>
      fetch(url).then(r => r.json()).then(data => [...results, data])
    ), Promise.resolve([]));
}
```

---

### Q238: How do you implement a timeout for async operations?

**Answer:**

Use `Promise.race` or AbortController.

```js
// General timeout
function timeout(ms) {
  return new Promise((_, reject) =>
    setTimeout(() => reject(new Error(`Timed out after ${ms}ms`)), ms)
  );
}

async function withTimeout(promise, ms) {
  return Promise.race([promise, timeout(ms)]);
}

// AbortController for fetch
function fetchWithTimeout(url, ms = 5000) {
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), ms);

  return fetch(url, { signal: controller.signal })
    .then(response => { clearTimeout(timeoutId); return response; })
    .catch(err => {
      clearTimeout(timeoutId);
      if (err.name === 'AbortError') throw new Error('Timeout');
      throw err;
    });
}
```

---

### Q239: What is top-level await?

**Answer:**

Allows `await` outside `async` in ES modules. Blocks module execution until promise settles.

```js
// In ES module (.mjs or "type": "module")
const response = await fetch('/api/config');
const config = await response.json();

export default config;

// Dynamic module loading
const { default: _ } = await import('lodash');

// Resource initialization
const db = await connectToDatabase();
export { db };

// Fallback pattern
let locale;
try {
  const data = await fetch('/api/locale');
  locale = await data.json();
} catch {
  locale = await import('./default-locale.js');
}
```

---

### Q240: How do you implement async/await with generators?

**Answer:**

```js
function asyncToGenerator(generatorFn) {
  return function(...args) {
    const gen = generatorFn.apply(this, args);
    return new Promise((resolve, reject) => {
      function step(key, arg) {
        try {
          const { value, done } = gen[key](arg);
          if (done) {
            resolve(value);
          } else {
            Promise.resolve(value).then(
              v => step('next', v),
              e => step('throw', e)
            );
          }
        } catch (err) {
          reject(err);
        }
      }
      step('next');
    });
  };
}

// Usage
const asyncFunction = asyncToGenerator(function* () {
  const data = yield fetch('/api/data').then(r => r.json());
  const more = yield fetch(`/api/more/${data.id}`).then(r => r.json());
  return more;
});

asyncFunction().then(result => console.log(result));
```

---

### Q241: How does Promise.prototype.catch work?

**Answer:**

`.catch()` is syntactic sugar for `.then(null, rejectionHandler)`. Catches errors from previous `.then()`.

```js
Promise.resolve(1)
  .then(v => { throw new Error('Error in then'); })
  .catch(err => {
    console.log('Caught:', err.message);
    return 'recovery';
  })
  .then(v => console.log(v)); // 'recovery'

// catch doesn't catch errors in its own handler
Promise.reject('err')
  .catch(err => { throw new Error('Another'); })
  .catch(err => console.log('Caught too:', err.message));

// catch on different branches (each handles rejection)
const p = Promise.reject('err');
p.then(v => console.log('A:', v)); // rejected
p.catch(e => console.log('B:', e)); // handles
```

---

### Q242: What is the difference between `Promise.resolve().then(fn)` and `queueMicrotask(fn)`?

**Answer:**

Both schedule microtasks. `.then()` returns a Promise (supports chaining). `queueMicrotask()` returns nothing.

```js
// Both schedule microtasks
Promise.resolve().then(() => console.log('Promise.then'));
queueMicrotask(() => console.log('queueMicrotask'));

// Chaining
Promise.resolve()
  .then(() => 'value')
  .then(v => console.log(v)); // 'value'

// queueMicrotask can't chain but supports nesting
queueMicrotask(() => {
  console.log('first');
  queueMicrotask(() => console.log('nested'));
});

// Error handling
Promise.resolve().then(() => { throw new Error('caught'); })
  .catch(e => console.log(e.message));

queueMicrotask(() => { throw new Error('uncaught'); });
// queueMicrotask errors need try/catch
```

---

### Q243: How does the event loop handle microtask starvation?

**Answer:**

Infinite microtask scheduling prevents macrotasks from running (e.g., recursive promise resolution).

```js
// Microtask starvation
function starve() {
  Promise.resolve().then(starve);
}
starve();
// setTimeout(() => console.log('Never runs'), 0);

// Macrotask starvation (less common)
function starveMacro() {
  setTimeout(starveMacro, 0);
}
// Microtasks still run between macrotasks

// Solutions:
// 1. Batching
// 2. Use setTimeout to break the microtask loop
function safeAsync() {
  setTimeout(() => {
    // Heavy work here
    Promise.resolve().then(safeAsync);
  }, 0);
}
```

---

### Q244: What is the async/await vs Promise performance difference?

**Answer:**

async/await is syntactic sugar — similar performance. Both create microtasks. The overhead is negligible for I/O operations.

```js
// Promise chain
function promiseStyle() {
  return fetch('/api/data')
    .then(r => r.json())
    .then(data => process(data));
}

// async/await (desugared to same)
async function asyncStyle() {
  const r = await fetch('/api/data');
  const data = await r.json();
  return process(data);
}

// Both return Promises. Await adds 2 extra microtasks per await
// For I/O-bound code, difference is negligible (< 1μs)
// For hot-path sync code, prefer sync operations
```

---

### Q245: How do you handle errors in async iterators?

**Answer:**

Use try/catch inside async generators, or handle rejection in for-await-of.

```js
// Async generator
async function* fetchPages(url) {
  let page = 1;
  while (true) {
    try {
      const response = await fetch(`${url}?page=${page}`);
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      const data = await response.json();
      if (data.length === 0) return;
      yield data;
      page++;
    } catch (err) {
      console.error('Error fetching page:', page, err);
      throw err; // or break/continue
    }
  }
}

// Consuming
try {
  for await (const page of fetchPages('/api/items')) {
    console.log('Page:', page);
  }
} catch (err) {
  console.error('Failed:', err);
}

// Async iteration error handling
const asyncIterable = {
  async *[Symbol.asyncIterator]() {
    yield 1;
    throw new Error('Oops');
  }
};

try {
  for await (const val of asyncIterable) {
    console.log(val);
  }
} catch (err) {
  console.log('Caught:', err.message);
}
```

---

### Q246: What is `Promise.prototype.finally`?

**Answer:**

`.finally()` runs regardless of settlement. It doesn't transform the promise value. Used for cleanup.

```js
let loading = true;

fetch('/api/data')
  .then(r => r.json())
  .then(data => console.log(data))
  .catch(err => console.error(err))
  .finally(() => {
    loading = false;
    hideSpinner();
  });

// finally doesn't change the result
Promise.resolve(42)
  .finally(() => {}) // runs
  .then(v => console.log(v)); // 42

// finally can throw (overrides)
Promise.resolve(42)
  .finally(() => { throw new Error('override'); })
  .catch(err => console.log(err.message)); // 'override'
```

---

### Q247: What is async generator and `for await...of`?

**Answer:**

Async generators (`async function*`) yield promises. `for await...of` consumes async iterables.

```js
// Async generator
async function* getItems() {
  let i = 0;
  while (i < 3) {
    await delay(1000);
    yield i++;
  }
}

// Consume
(async () => {
  for await (const item of getItems()) {
    console.log(item); // 0, 1, 2 (with 1s delay each)
  }
})();

// Async iterable
const asyncRange = {
  from: 0,
  to: 5,
  [Symbol.asyncIterator]() {
    return {
      current: this.from,
      last: this.to,
      async next() {
        await delay(200);
        if (this.current <= this.last) {
          return { value: this.current++, done: false };
        }
        return { value: undefined, done: true };
      }
    };
  }
};

for await (const n of asyncRange) {
  console.log(n); // 0, 1, 2, 3, 4, 5
}
```

---

### Q248: How do you implement a simple async queue?

**Answer:**

```js
class AsyncQueue {
  constructor() {
    this.queue = [];
    this.resolvers = [];
  }

  enqueue(value) {
    if (this.resolvers.length > 0) {
      const resolve = this.resolvers.shift();
      resolve(value);
    } else {
      this.queue.push(value);
    }
  }

  async dequeue() {
    if (this.queue.length > 0) {
      return this.queue.shift();
    }
    return new Promise(resolve => this.resolvers.push(resolve));
  }

  get length() { return this.queue.length; }
}

// Usage
const q = new AsyncQueue();
q.enqueue('hello');
q.enqueue('world');

console.log(await q.dequeue()); // 'hello'
console.log(await q.dequeue()); // 'world'

// Async producer-consumer
async function producer() {
  for (let i = 0; i < 5; i++) {
    await delay(100);
    q.enqueue(i);
  }
}

async function consumer() {
  while (true) {
    const item = await q.dequeue();
    console.log('Consumed:', item);
  }
}
```

---

### Q249: What is the difference between `Promise.all` and `Promise.allSettled`?

**Answer:**

`Promise.all` rejects fast (on first rejection). `Promise.allSettled` waits for all to settle, never rejects.

```js
const failing = Promise.reject(new Error('Fail'));
const slow = new Promise(resolve => setTimeout(resolve, 100, 'Slow'));

// Promise.all - fails fast
Promise.all([failing, slow])
  .catch(err => console.log(err.message)); // 'Fail' (immediate)

// Promise.allSettled - waits for all
Promise.allSettled([failing, slow])
  .then(results => {
    console.log(results[0]); // { status: 'rejected', reason: Error }
    console.log(results[1]); // { status: 'fulfilled', value: 'Slow' }
  });

// When to use:
// - all: need all to succeed, fail fast
// - allSettled: need results of all, handle failures individually
```

---

### Q250: What is the difference between `finally` in try/catch and Promise.finally?

**Answer:**

Both run regardless of outcome. `try/catch finally` catches synchronous errors. `Promise.finally` handles async.

```js
// try/catch/finally - synchronous
try {
  riskyOperation();
} catch (err) {
  console.error(err);
} finally {
  cleanup(); // always runs
}

// Promise.finally - asynchronous
fetch('/api/data')
  .then(r => r.json())
  .catch(err => console.error(err))
  .finally(() => cleanup());

// try/finally in async function covers both
async function combined() {
  try {
    return await fetch('/api/data').then(r => r.json());
  } catch (err) {
    console.error(err);
    throw err;
  } finally {
    cleanup(); // always runs
  }
}
```

---

# PHASE 6: ES6+ FEATURES (Q251–Q290)

---

### Q251: What are ES Modules (ESM)?

**Answer:**

ES Modules are the official JS module system using `import`/`export`. Static analysis, tree-shaking, strict mode.

```js
// math.js
export const PI = 3.14159;
export function add(a, b) { return a + b; }
export default function multiply(a, b) { return a * b; }

// app.js
import multiply, { PI, add } from './math.js';

// Renaming imports
import { add as sum } from './math.js';

// Re-export
export { PI } from './math.js';

// Namespace import
import * as math from './math.js';
math.add(1, 2);

// Import for side effects
import './polyfills.js';
```

---

### Q252: ESM vs CommonJS?

**Answer:**

ESM: static, tree-shakable, async, strict mode. CJS: dynamic, sync, not strict by default.

```js
// CommonJS
const math = require('./math');
module.exports = { add, multiply };

// ESM
import { add } from './math.js';
export { add };
export default add;

// Key differences:
// 1. ESM: static imports hoisted; CJS: dynamic require
// 2. ESM: top-level await; CJS: no
// 3. ESM: import.meta.url; CJS: __dirname
// 4. ESM: tree-shakable; CJS: not

// Dynamic import (both work)
const m = await import(`./${moduleName}.js`); // ESM dynamic
const m = require(`./${moduleName}`); // CJS dynamic
```

---

### Q253: How does dynamic `import()` work?

**Answer:**

Returns a Promise for the module namespace. Enables code splitting and lazy loading.

```js
async function loadModule() {
  const module = await import('./module.js');
  return module.default();
}

// Code splitting (React)
const AdminPanel = React.lazy(() => import('./AdminPanel'));

// Conditional loading
if (condition) {
  const { heavyFunction } = await import('./heavy.js');
  heavyFunction();
}

// Event-triggered loading
button.addEventListener('click', async () => {
  const { showChart } = await import('./chart.js');
  showChart(data);
});

// Module namespace
const module = await import('./utils.js');
console.log(Object.keys(module)); // ['export1', 'export2']
```

---

### Q254: What are `Proxy` and `Reflect`?

**Answer:**

`Proxy` wraps objects to intercept operations. `Reflect` provides methods mirroring Proxy traps.

```js
const target = { name: 'Alice', age: 30 };

const proxy = new Proxy(target, {
  get(target, prop, receiver) {
    if (prop === 'age') return target[prop] + ' years';
    return Reflect.get(target, prop, receiver);
  },
  set(target, prop, value) {
    if (prop === 'age' && typeof value !== 'number') {
      throw new TypeError('Age must be a number');
    }
    return Reflect.set(target, prop, value);
  }
});

// Reflect utility methods
Reflect.ownKeys({ a: 1, b: 2 }); // ['a', 'b']
Reflect.get({ a: 1 }, 'a'); // 1
Reflect.set({ a: 1 }, 'a', 2); // true
Reflect.has({ a: 1 }, 'a'); // true
Reflect.deleteProperty({ a: 1 }, 'a'); // true
```

---

### Q255: What is `BigInt`?

**Answer:**

`BigInt` represents integers beyond `2^53 - 1`. Use `n` suffix.

```js
const big = 9007199254740991n;
const fromNum = BigInt(42);
const fromStr = BigInt('9007199254740992');

// Operations
10n + 20n; // 30n
10n * 20n; // 200n
5n / 2n; // 2n (truncates)

// Can't mix with regular numbers
// 10n + 5; // TypeError
Number(10n) + 5; // 15

// Comparisons
10n == 10; // true
10n === 10; // false

// Use cases: large IDs, crypto, financial precision
```

---

### Q256: What is `globalThis`?

**Answer:**

Standard way to access global object across environments.

```js
// Browser
window === globalThis; // true

// Node.js
global === globalThis; // true

// Web Worker
self === globalThis; // true

// Usage
globalThis.setTimeout(() => {}, 1000);
globalThis.console.log('Hello');
globalThis.myApp = { version: '1.0' };
```

---

### Q257: What are enhanced object literals?

**Answer:**

Shorthand properties, methods, computed keys, spread.

```js
const name = 'Alice';
const age = 30;

// Property shorthand
const user = { name, age };

// Method shorthand
const obj = {
  greet() { console.log('Hello'); },
  ['say' + 'Hi']() { console.log('Hi'); }
};

// Computed property names
const key = 'dynamic';
const computed = {
  [key]: 'value',
  [`${key}Prop`]: true
};

// Spread
const settings = { ...defaults, ...userSettings };

// Getters/setters
const person = {
  _name: 'Alice',
  get name() { return this._name; },
  set name(v) { this._name = v; }
};
```

---

### Q258: What are new string methods?

**Answer:**

`includes`, `startsWith`, `endsWith`, `repeat`, `padStart`, `padEnd`, `trimStart`, `trimEnd`, `replaceAll`, `at`.

```js
const str = 'Hello World';

str.includes('World'); // true
str.startsWith('Hello'); // true
str.endsWith('World'); // true
'ha'.repeat(3); // 'hahaha'
'5'.padStart(3, '0'); // '005'
'hello'.padEnd(8, '-'); // 'hello---'
'  hi  '.trimStart(); // 'hi  '
'  hi  '.trimEnd(); // '  hi'
'foo bar foo'.replaceAll('foo', 'baz'); // 'baz bar baz'
'hello'.at(-1); // 'o'
```

---

### Q259: What are new number/ Math methods?

**Answer:**

`Number.isFinite`, `Number.isNaN`, `Number.isInteger`, `Number.isSafeInteger`, `Math.trunc`, `Math.sign`, `Math.cbrt`, `Math.hypot`, exponent operator `**`.

```js
Number.isFinite(42); // true
Number.isFinite('42'); // false (no coercion)
Number.isNaN(NaN); // true
Number.isNaN('NaN'); // false
Number.isInteger(42); // true
Number.isInteger(42.5); // false
Number.isSafeInteger(9007199254740991); // true

Math.trunc(42.7); // 42
Math.sign(-5); // -1
Math.cbrt(27); // 3
Math.hypot(3, 4); // 5

2 ** 3; // 8 (exponent operator)
```

---

### Q260: What are new Array static/instance methods?

**Answer:**

`Array.from`, `Array.of`, `Array.isArray`, `at`, `findLast`, `findLastIndex`, `toSorted`, `toReversed`, `toSpliced`, `with`, `groupBy`.

```js
Array.from('hello'); // ['h','e','l','l','o']
Array.from({ length: 3 }, (_, i) => i); // [0, 1, 2]
Array.of(5); // [5]

[1, 2, 3].at(-1); // 3
[1, 2, 3, 4].findLast(n => n > 2); // 4
[1, 2, 3, 4].findLastIndex(n => n > 2); // 3

const arr = [3, 1, 2];
arr.toSorted(); // [1, 2, 3] (copy)
arr.toReversed(); // [2, 1, 3] (copy)
arr.with(0, 99); // [99, 1, 2]
arr; // [3, 1, 2] (unchanged)

Object.groupBy([1, 2, 3, 4, 5], n => n % 2 ? 'odd' : 'even');
// { odd: [1, 3, 5], even: [2, 4] }
```

---

### Q261: What is `Object.hasOwn()`?

**Answer:**

`Object.hasOwn(obj, prop)` (ES2022) safely checks own properties. Works on Object.create(null), can't be shadowed.

```js
const obj = Object.create(null);
obj.name = 'Alice';

// obj.hasOwnProperty('name'); // TypeError
Object.hasOwn(obj, 'name'); // true (works!)
Object.hasOwn(obj, 'toString'); // false

// Can't be shadowed
const hacked = { hasOwnProperty: () => true };
Object.hasOwn(hacked, 'toString'); // false (correct)

// Use instead of:
// obj.hasOwnProperty(key) // can be shadowed
// Object.prototype.hasOwnProperty.call(obj, key) // verbose
```

---

### Q262: What are Error cause and AggregateError?

**Answer:**

`cause` (ES2022) for error chaining. `AggregateError` for multiple errors.

```js
// Error cause
try {
  await fetch('/api/data');
} catch (err) {
  throw new Error('Failed to load data', { cause: err });
}

// Later
try {
  await process();
} catch (err) {
  console.log(err.message); // 'Failed to load data'
  console.log(err.cause); // original fetch error
}

// AggregateError
try {
  await Promise.any([
    Promise.reject(new Error('E1')),
    Promise.reject(new Error('E2'))
  ]);
} catch (err) {
  if (err instanceof AggregateError) {
    console.log(err.errors); // [Error: E1, Error: E2]
  }
}
```

---

### Q263: What is `structuredClone()`?

**Answer:**

Deeply clones JS values, handling Maps, Sets, Dates, RegExps, ArrayBuffers, circular references.

```js
const original = {
  name: 'Alice',
  date: new Date(),
  map: new Map([['key', 'value']]),
  set: new Set([1, 2, 3]),
  nested: { arr: [1, 2] }
};

original.self = original; // circular

const clone = structuredClone(original);

clone !== original; // true
clone.date instanceof Date; // true
clone.map instanceof Map; // true
clone.self === clone; // true (circular preserved!)

// CANNOT clone: functions, DOM elements, WeakMap, Promise, Symbols
```

---

### Q264: What are WeakRef and FinalizationRegistry?

**Answer:**

`WeakRef` holds a weak reference. `FinalizationRegistry` runs callback when object is GC'd.

```js
// WeakRef
let obj = { data: 'important' };
const ref = new WeakRef(obj);

const deref = ref.deref();
if (deref) console.log('Still alive:', deref.data);

obj = null; // can be GC'd

// FinalizationRegistry
const registry = new FinalizationRegistry((heldValue) => {
  console.log('Cleaned up:', heldValue);
});

function trackObject(obj, id) {
  registry.register(obj, id);
}

let tracked = { data: 'large' };
trackObject(tracked, 'tracked-1');
tracked = null; // callback runs when GC'd

// Use cases: cache with expiration, memory leak detection
```

---

### Q265: What is `ArrayBuffer` and typed arrays?

**Answer:**

`ArrayBuffer` is fixed-length binary data. Typed arrays (Uint8Array, Int32Array) provide views.

```js
const buffer = new ArrayBuffer(16);
const uint8 = new Uint8Array(buffer);
uint8[0] = 255;
uint8[1] = 128;

const int32 = new Int32Array(buffer);
int32[0]; // reads first 4 bytes as 32-bit int

// DataView - flexible endianness
const view = new DataView(buffer);
view.setUint8(0, 42);
view.setInt16(2, 1024, true); // little-endian
view.setFloat32(4, 3.14);

console.log(view.getUint8(0)); // 42

// Text encoding
const encoder = new TextEncoder();
const encoded = encoder.encode('Hello'); // Uint8Array
const decoder = new TextDecoder();
decoder.decode(encoded); // 'Hello'
```

---

### Q266: What are `Atomics` and `SharedArrayBuffer`?

**Answer:**

`SharedArrayBuffer` shares memory between threads. `Atomics` provides safe concurrent operations. Requires cross-origin isolation headers.

```js
// Main thread
const sab = new SharedArrayBuffer(4);
const view = new Int32Array(sab);
view[0] = 0;

const worker = new Worker('worker.js');
worker.postMessage(sab);

// Atomic operations
Atomics.add(view, 0, 1); // atomic increment
Atomics.load(view, 0); // atomic read
Atomics.store(view, 0, 42); // atomic write

// Worker
self.onmessage = (e) => {
  const sab = e.data;
  const view = new Int32Array(sab);
  Atomics.add(view, 0, 1);
  Atomics.notify(view, 0, 1); // wake up waiting threads
};
```

---

### Q267: What is `import.meta`?

**Answer:**

`import.meta` provides metadata about the current module (url, resolve function).

```js
// Current module URL
console.log(import.meta.url); // 'file:///path/to/module.js'

// Dynamic resolution (import.meta.resolve)
const url = import.meta.resolve('./other.js');
// Returns resolved URL string: 'file:///path/to/other.js'

// For Node.js
import { fileURLToPath } from 'url';
const __filename = fileURLToPath(import.meta.url);
const __dirname = fileURLToPath(new URL('.', import.meta.url));
```

---

### Q268: What is the `??` (nullish coalescing) operator?

**Answer:**

Returns right operand only if left is `null` or `undefined`. Unlike `||`, doesn't treat `0`, `''`, `false` as falsy.

```js
const a = 0;
const b = '';

a || 'default'; // 'default' (0 is falsy)
a ?? 'default'; // 0 (not null/undefined)

b || 'default'; // 'default'
b ?? 'default'; // ''

// Use cases
function config(options) {
  const timeout = options.timeout ?? 3000;
  const retries = options.retries ?? 3;
  return { timeout, retries };
}

config({ timeout: 0, retries: false });
// { timeout: 0, retries: false }

// Can't chain with && or || without parens
// const x = a && b ?? c; // SyntaxError
const x = (a && b) ?? c; // OK
```

---

### Q269: What is `?.` (optional chaining) operator?

**Answer:**

Safe property access. Returns `undefined` if intermediate value is `null`/`undefined`. Short-circuits.

```js
const user = { name: 'Alice', address: null };

// Without
const city = user && user.address && user.address.city;

// With optional chaining
const city = user?.address?.city; // undefined

// Function calls
const result = user.getProfile?.();

// Dynamic properties
const key = 'name';
const value = user?.[key];

// Optional chaining with delete
delete user?.address?.city;

// Array
const first = arr?.[0];
```

---

### Q270: What are logical assignment operators (`??=`, `||=`, `&&=`)?

**Answer:**

ES2021 operators combining logical operators with assignment.

```js
// ??= (nullish assignment)
let a = null;
a ??= 'default'; // 'default' (only null/undefined)
let b = 0;
b ??= 'default'; // 0 (not null/undefined)

// ||= (falsy assignment)
let c = 0;
c ||= 42; // 42 (0 is falsy)
let d = 'hello';
d ||= 'world'; // 'hello' (truthy)

// &&= (truthy assignment)
let e = true;
e &&= 'set'; // 'set' (was truthy)
let f = false;
f &&= 'set'; // false (was falsy)

// Use cases
function config(options) {
  options.timeout ??= 3000;
  options.name ||= 'Guest';
  options.debug &&= false;
  return options;
}
```

---

# PHASE 7: NODE.JS (Q271–Q310)

---

### Q271: What is the EventEmitter in Node.js?

**Answer:**

EventEmitter is a core Node.js class for event-driven architecture. Used extensively in Node APIs (streams, HTTP, etc.).

```js
const EventEmitter = require('events');

class MyEmitter extends EventEmitter {
  doSomething() {
    console.log('Doing something...');
    this.emit('done', { result: 'success' });
  }
}

const emitter = new MyEmitter();

// Listen
emitter.on('done', (data) => {
  console.log('Event received:', data);
});

// One-time listener
emitter.once('once', () => console.log('This runs only once'));

// Error handling
emitter.on('error', (err) => {
  console.error('Error:', err.message);
});

// Emit events
emitter.doSomething();

// Remove listeners
emitter.off('done', handler);
emitter.removeAllListeners('done');

// Listener count
console.log(emitter.listenerCount('done'));
```

---

### Q272: What are Streams in Node.js?

**Answer:**

Streams process data chunk by chunk without loading everything into memory. Four types: Readable, Writable, Duplex, Transform.

```js
const fs = require('fs');
const zlib = require('zlib');

// Readable stream
const readStream = fs.createReadStream('input.txt', { encoding: 'utf8', highWaterMark: 1024 });

// Writable stream
const writeStream = fs.createWriteStream('output.txt');

// Pipe - readable to writable
readStream.pipe(writeStream);

// Transform stream (compression)
const gzip = zlib.createGzip();
fs.createReadStream('input.txt')
  .pipe(gzip)
  .pipe(fs.createWriteStream('input.txt.gz'));

// Custom stream
const { Transform } = require('stream');
const upperCase = new Transform({
  transform(chunk, encoding, callback) {
    this.push(chunk.toString().toUpperCase());
    callback();
  }
});

fs.createReadStream('input.txt')
  .pipe(upperCase)
  .pipe(process.stdout);

// Events
readStream.on('data', (chunk) => console.log('Received', chunk.length, 'bytes'));
readStream.on('end', () => console.log('Finished'));
readStream.on('error', (err) => console.error(err));
```

---

### Q273: What is Buffer in Node.js?

**Answer:**

Buffer handles binary data in Node.js. Global, no need to require.

```js
// Create buffer
const buf1 = Buffer.alloc(10); // zero-filled
const buf2 = Buffer.alloc(10, 0xFF); // filled with 0xFF
const buf3 = Buffer.from('Hello');
const buf4 = Buffer.from([0x48, 0x65, 0x6C, 0x6C, 0x6F]);
const buf5 = Buffer.from('Hello', 'base64');

// Read/write
buf3[0]; // 72 (0x48)
buf3.write('World', 0);
buf3.toString(); // 'World'
buf3.toString('hex'); // '576f726c64'
buf3.toString('base64'); // 'V29ybGQ='

// Slice (no copy, shares memory)
const slice = buf3.slice(0, 3);

// Copy
const copy = Buffer.alloc(5);
buf3.copy(copy);

// Compare
Buffer.compare(buf3, buf4);
buf3.equals(buf4);

// Encoding conversions
Buffer.from('€uro', 'utf8'); // UTF-8 bytes
Buffer.from('€uro', 'utf16le'); // UTF-16 LE bytes
```

---

### Q274: What is `process.nextTick` vs `setImmediate` vs `setTimeout`?

**Answer:**

`process.nextTick` runs before microtasks and macrotasks (highest priority). `setImmediate` runs after I/O callbacks. `setTimeout(fn, 0)` runs after setImmediate.

```js
console.log('1: sync');

process.nextTick(() => console.log('2: nextTick'));

Promise.resolve().then(() => console.log('3: microtask'));

setImmediate(() => console.log('4: setImmediate'));

setTimeout(() => console.log('5: setTimeout(0)'), 0);

// Output: 1, 2, 3, 4, 5
// Note: nextTick runs before microtasks!

// Order within event loop phases:
// 1. nextTick queue (drained completely)
// 2. Microtasks (Promise callbacks)
// 3. Timers (setTimeout, setInterval)
// 4. I/O callbacks
// 5. setImmediate
// 6. Close callbacks

// nextTick recursion can starve I/O
function recursiveNextTick() {
  process.nextTick(recursiveNextTick);
}
// setTimeout callbacks never run
```

---

### Q275: What is the difference between `spawn`, `exec`, and `fork`?

**Answer:**

`spawn` streams I/O, suitable for large data. `exec` buffers output (up to maxBuffer). `fork` creates a child process (Node.js) with IPC channel.

```js
const { spawn, exec, fork } = require('child_process');

// spawn - streams output
const ls = spawn('ls', ['-lh', '/usr']);
ls.stdout.on('data', (data) => console.log(`stdout: ${data}`));
ls.stderr.on('data', (data) => console.error(`stderr: ${data}`));
ls.on('close', (code) => console.log(`Exit code: ${code}`));

// exec - buffers output
exec('ls -lh /usr', (error, stdout, stderr) => {
  if (error) console.error(error);
  console.log(stdout);
});

// fork - IPC communication
const child = fork('child.js');
child.send({ hello: 'world' });
child.on('message', (msg) => console.log('From child:', msg));

// child.js
process.on('message', (msg) => {
  console.log('From parent:', msg);
  process.send({ response: 'ok' });
});

// Differences:
// spawn: stream, no shell by default, large output
// exec: buffer, uses shell, limited output (200KB default)
// fork: Node only, IPC built-in
```

---

### Q276: What is the Cluster module?

**Answer:**

Cluster allows a Node.js application to fork across multiple CPU cores. Master distributes connections to workers.

```js
const cluster = require('cluster');
const http = require('http');
const os = require('os');

if (cluster.isMaster) {
  const numCPUs = os.cpus().length;
  console.log(`Master ${process.pid} forking ${numCPUs} workers`);

  for (let i = 0; i < numCPUs; i++) {
    cluster.fork();
  }

  cluster.on('exit', (worker, code, signal) => {
    console.log(`Worker ${worker.process.pid} died`);
    // Replace dead worker
    cluster.fork();
  });
} else {
  // Worker - handles requests
  http.createServer((req, res) => {
    res.writeHead(200);
    res.end(`Handled by ${process.pid}\n`);
  }).listen(8000);

  console.log(`Worker ${process.pid} started`);
}

// Note: Not ideal for stateful apps (each worker has own memory)
// Use shared storage (Redis, DB) for sessions
```

---

### Q277: CommonJS vs ESM in Node.js?

**Answer:**

CommonJS uses `require`/`module.exports` (sync). ESM uses `import`/`export` (async, static). Node.js supports both.

```js
// CommonJS (.cjs or "type": "commonjs")
const fs = require('fs');
const path = require('path');
module.exports = { myFunction };
exports.myFunction = myFunction;

// __dirname, __filename available
console.log(__dirname, __filename);

// require is synchronous, can be conditional
const lib = condition ? require('lib-a') : require('lib-b');

// ESM (.mjs or "type": "module")
import fs from 'fs/promises';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

export default myFunction;
export { myFunction };

// Dynamic import
const mod = await import('./module.js');

// Interop: ESM can import CJS (default export = module.exports)
import cjsModule from './cjs-module.cjs';

// CJS cannot require ESM (must use dynamic import)
async function loadESM() {
  const esm = await import('./esm-module.mjs');
}
```

---

### Q278: How does Node.js handle uncaught exceptions?

**Answer:**

`process.on('uncaughtException')` catches unhandled sync errors (use for cleanup only). `process.on('unhandledRejection')` catches unhandled Promise rejections.

```js
// Uncaught sync exceptions
process.on('uncaughtException', (err, origin) => {
  console.error('Uncaught exception:', err);
  // Perform cleanup, then exit
  process.exit(1);
});

// Async errors in callback APIs
process.on('uncaughtExceptionMonitor', (err, origin) => {
  console.log('Exception captured:', err);
});

// Unhandled Promise rejections
process.on('unhandledRejection', (reason, promise) => {
  console.error('Unhandled Rejection at:', promise, 'reason:', reason);
  // In Node 15+, unhandled rejections crash the process
});

// Rejection Handled (late catch)
process.on('rejectionHandled', (promise) => {
  console.log('Rejection was handled late:', promise);
});

// Best practice: catch all errors explicitly
async function safeMain() {
  try {
    await runApp();
  } catch (err) {
    console.error('Application error:', err);
    process.exitCode = 1;
  }
}

// Domain module (deprecated) - avoid
```

---

### Q279: What are the main Node.js File System APIs?

**Answer:**

`fs` module offers sync, callback, and promise-based APIs.

```js
const fs = require('fs');
const fsPromises = require('fs/promises');

// Callback style
fs.readFile('file.txt', 'utf8', (err, data) => {
  if (err) console.error(err);
  else console.log(data);
});

// Promise style (modern)
async function readFile() {
  try {
    const data = await fsPromises.readFile('file.txt', 'utf8');
    console.log(data);
  } catch (err) {
    console.error(err);
  }
}

// Sync style (blocking)
const data = fs.readFileSync('file.txt', 'utf8');

// Write
await fsPromises.writeFile('output.txt', 'Hello World', 'utf8');
fs.appendFileSync('log.txt', 'new line\n');

// File info
const stat = await fsPromises.stat('file.txt');
console.log(stat.isFile(), stat.size, stat.mtime);

// Directory operations
await fsPromises.mkdir('new-dir', { recursive: true });
const files = await fsPromises.readdir('.');
await fsPromises.unlink('file.txt'); // delete
await fsPromises.rmdir('dir'); // remove dir

// Watch for changes
fs.watch('file.txt', (eventType, filename) => {
  console.log(`${filename}: ${eventType}`);
});
```

---

### Q280: What is `path` module?

**Answer:**

The `path` module handles file path manipulation across platforms.

```js
const path = require('path');

// Normalize
path.normalize('/foo/bar//baz/asdf/..'); // '/foo/bar/baz'

// Join
path.join('/foo', 'bar', 'baz/asdf', 'quux', '..');
// '/foo/bar/baz/asdf'

// Resolve (absolute path)
path.resolve('foo/bar'); // '/current/working/dir/foo/bar'
path.resolve('/foo', 'bar', 'baz'); // '/foo/bar/baz'

// Parse
const parsed = path.parse('/home/user/file.txt');
// { root: '/', dir: '/home/user', base: 'file.txt', ext: '.txt', name: 'file' }

// Format
path.format({ dir: '/home/user', base: 'file.txt' });
// '/home/user/file.txt'

// Components
path.basename('/foo/bar/baz.txt'); // 'baz.txt'
path.dirname('/foo/bar/baz.txt'); // '/foo/bar'
path.extname('file.txt'); // '.txt'

// Platform-specific
path.sep; // '/' on POSIX, '\\' on Windows
path.delimiter; // ':' on POSIX, ';' on Windows

// Relative path
path.relative('/data/orandea/test/aaa', '/data/orandea/impl/bbb');
// '../../impl/bbb'
```

---

### Q281: What is `process.env` and how do you use environment variables?

**Answer:**

`process.env` contains environment variables. Use for configuration, secrets management.

```js
// Access
console.log(process.env.NODE_ENV); // 'development', 'production'
console.log(process.env.PATH);
console.log(process.env.HOME);

// Set (only affects current process)
process.env.MY_VAR = 'value';
console.log(process.env.MY_VAR);

// .env file (using dotenv)
// require('dotenv').config();
// console.log(process.env.DB_URL);

// Default values with fallback
const port = process.env.PORT || 3000;
const dbUrl = process.env.DB_URL ?? 'localhost:5432';

// List all
console.log(Object.keys(process.env));

// Sanitize sensitive output
function safeEnv() {
  const sensitive = ['PASSWORD', 'SECRET', 'TOKEN'];
  const safe = { ...process.env };
  sensitive.forEach(key => { if (safe[key]) safe[key] = '***'; });
  return safe;
}
```

---

### Q282: What is `http` module in Node.js?

**Answer:**

The `http` module creates HTTP servers and clients.

```js
const http = require('http');

// Create server
const server = http.createServer((req, res) => {
  console.log(`${req.method} ${req.url}`);

  // Request headers
  console.log(req.headers);

  // Request body
  let body = '';
  req.on('data', chunk => body += chunk);
  req.on('end', () => {
    console.log('Body:', body);

    // Response
    res.writeHead(200, {
      'Content-Type': 'application/json',
      'X-Custom-Header': 'value'
    });
    res.end(JSON.stringify({ message: 'Hello', method: req.method }));
  });
});

server.listen(3000, () => {
  console.log('Server running on port 3000');
});

// HTTP client (make requests)
const options = {
  hostname: 'api.example.com',
  port: 443,
  path: '/data',
  method: 'GET',
  headers: { 'Content-Type': 'application/json' }
};

const req = http.request(options, (res) => {
  let data = '';
  res.on('data', chunk => data += chunk);
  res.on('end', () => console.log(JSON.parse(data)));
});

req.on('error', (err) => console.error(err));
req.end();

// https module (same API, SSL/TLS)
const https = require('https');
```

---

### Q283: What is `os` module?

**Answer:**

The `os` module provides operating system utility methods.

```js
const os = require('os');

// CPU info
console.log('CPUs:', os.cpus().length);
console.log('CPU model:', os.cpus()[0].model);

// Memory
console.log('Total memory:', os.totalmem());
console.log('Free memory:', os.freemem());
console.log('Used memory:', os.totalmem() - os.freemem());

// Network
console.log('Network interfaces:', os.networkInterfaces());

// System info
console.log('Hostname:', os.hostname());
console.log('Platform:', os.platform()); // 'linux', 'darwin', 'win32'
console.log('Arch:', os.arch()); // 'x64', 'arm64'
console.log('Release:', os.release());
console.log('Uptime:', os.uptime(), 'seconds');

// User
console.log('Home dir:', os.homedir());
console.log('Temp dir:', os.tmpdir());
console.log('User:', os.userInfo());

// EOL (End of line)
console.log(JSON.stringify(os.EOL)); // '\n' on POSIX, '\r\n' on Windows

// Load average
console.log('Load avg (1, 5, 15 min):', os.loadavg());
```

---

### Q284: What is `path.resolve` vs `path.join`?

**Answer:**

`path.join` joins path segments. `path.resolve` resolves to an absolute path.

```js
const path = require('path');

// join - concatenates with platform separator
path.join('/foo', 'bar', 'baz'); // '/foo/bar/baz'
path.join('foo', 'bar', '..'); // 'foo'

// resolve - returns absolute path
path.resolve('foo/bar'); // '/current/working/dir/foo/bar'
path.resolve('/foo', 'bar'); // '/foo/bar'
path.resolve('/foo', '..', 'bar'); // '/bar'

// If no absolute segment, uses cwd
path.resolve('a', 'b'); // '/cwd/a/b'
path.resolve('/a', '/b'); // '/b' (last absolute wins)

// If rightmost is absolute, returns it
path.resolve('/a', '/b', 'c'); // '/b/c'

// Practical
const fullPath = path.resolve(__dirname, '..', 'config', 'app.js');
```

---

### Q285: What are Node.js global objects?

**Answer:**

Globals available without require: `process`, `Buffer`, `__dirname`, `__filename`, `console`, `exports`, `module`, `require`, `setTimeout`, `setInterval`, `setImmediate`, `queueMicrotask`, `URL`, `URLSearchParams`, `TextEncoder`, `TextDecoder`, `performance`, `structuredClone`, `AbortController`.

```js
// Process
process.argv;
process.cwd();
process.exit(0);

// Buffer
Buffer.from('hello');

// Global timer functions
setTimeout(() => {}, 1000);
setInterval(() => {}, 2000);
setImmediate(() => {});
queueMicrotask(() => {});

// URL
const url = new URL('https://example.com/path?query=value');
console.log(url.hostname);

// performance (for timing)
console.log(performance.now());
performance.mark('start');

// structuredClone
const clone = structuredClone({ a: 1, b: { c: 2 } });

// AbortController (since Node 15)
const ac = new AbortController();
```

---

### Q286: What are the differences between `require` and `import`?

**Answer:**

`require` is synchronous, loads at runtime, can be conditional, caches modules. `import` is async (static), hoisted, analyzed at compile time.

```js
// require
const fs = require('fs'); // cached
const myModule = require('./module');

// Can be conditional
const lib = process.env.DEBUG ? require('debug') : require('production-lib');

// Runtime resolution
const module = require(`./locales/${lang}`);

// JSON
const config = require('./config.json');

// import
import fs from 'fs'; // hoisted
import { myFunc } from './module.js';

// No conditional static imports (use dynamic import)
if (condition) {
  const { lib } = await import('./lib.js');
}

// import assertions
import data from './data.json' assert { type: 'json' };

// Caching behavior similar, but import is async
// Both cache modules: subsequent require/import return same instance
```

---

### Q287: What is `require.resolve`?

**Answer:**

`require.resolve` resolves a module path without loading it. Returns the absolute file path.

```js
const path = require('path');

// Resolve module path
const modulePath = require.resolve('lodash');
console.log(modulePath); // '/path/to/node_modules/lodash/lodash.js'

// Resolve relative path
const configPath = require.resolve('./config');
console.log(configPath); // '/current/dir/config.js'

// With paths option
const customPath = require.resolve('my-module', {
  paths: ['/some/path', '/other/path']
});

// Not found: throws MODULE_NOT_FOUND
try {
  require.resolve('non-existent');
} catch (err) {
  console.log(err.code); // 'MODULE_NOT_FOUND'
}

// Check if module exists without loading
function moduleExists(name) {
  try {
    require.resolve(name);
    return true;
  } catch {
    return false;
  }
}
```

---

### Q288: What are `module.exports` and `exports`?

**Answer:**

`module.exports` is the actual object returned by `require`. `exports` is an alias for `module.exports`. Assignment to `exports` breaks the reference.

```js
// This works:
exports.add = (a, b) => a + b;
exports.subtract = (a, b) => a - b;

// Equivalent to:
module.exports = { add: ..., subtract: ... };

// This DOES NOT work:
exports = { add: (a, b) => a + b }; // breaks reference
// module.exports is still the original empty object

// This works:
module.exports = { add: (a, b) => a + b };

// Replacing module.exports entirely:
module.exports = class MyClass {};

// Shorthand:
exports.myFunc = () => {};

// Export class:
class Person {}
module.exports = Person;

// Export instance (singleton):
module.exports = new Person();
```

---

### Q289: What is the Node.js module resolution algorithm?

**Answer:**

Node.js resolves `require('x')` by looking for `x` in `node_modules`, then `node_modules` of parent directories, up to root. For relative paths, resolves from the requiring file's directory.

```js
// require('./module')
// 1. ./module.js
// 2. ./module.json
// 3. ./module/index.js
// 4. ./module/index.node
// 5. ./module/package.json (main field)

// require('package-name')
// 1. <cwd>/node_modules/package-name
// 2. <parent>/node_modules/package-name
// 3. ... up to root

// require('package-name/sub/path')
// 1. <cwd>/node_modules/package-name/sub/path.js

// package.json main field
// {
//   "main": "dist/index.js",
//   "exports": { ".": "./dist/index.js" } // ESM
// }

// NODE_PATH environment variable
// NODE_PATH=/shared/modules

// __dirname resolution
// require.resolve.paths('module') shows search paths
```

---

### Q290: How does Node.js handle module caching?

**Answer:**

Modules are cached after first load. Subsequent `require` calls return the same instance. `require.cache` stores all cached modules.

```js
// Modules cached by resolved filename
const modA = require('./module'); // loaded and cached
const modB = require('./module'); // returns cached version
console.log(modA === modB); // true

// Inspect cache
console.log(require.cache); // { '/path/to/module.js': Module {...} }

// Delete from cache (force reload)
delete require.cache[require.resolve('./module')];
const modNew = require('./module'); // reloaded

// Clear all cache
Object.keys(require.cache).forEach(key => {
  delete require.cache[key];
});

// Module._cache is the same as require.cache

// Module _resolveFilename
console.log(require.resolve('./module'));

// Each module is an instance of Module class
const Module = require('module');
const m = new Module('filename.js');
```

---

### Q291: What are the `setTimeout` vs `setInterval` vs `setImmediate` differences?

**Answer:**

`setTimeout` runs once after delay. `setInterval` runs repeatedly every delay. `setImmediate` runs after I/O callbacks (check phase). All return timer objects.

```js
// setTimeout - runs once
const timeout = setTimeout(() => {
  console.log('Delayed');
}, 1000);
clearTimeout(timeout); // cancel

// setInterval - runs repeatedly
const interval = setInterval(() => {
  console.log('Every 1s');
}, 1000);
clearInterval(interval); // stop

// setImmediate - runs after I/O
const immediate = setImmediate(() => {
  console.log('After I/O callbacks');
});
clearImmediate(immediate);

// Recursive setTimeout (vs setInterval)
function recursiveTimeout() {
  console.log('Runs, then waits 1s');
  setTimeout(recursiveTimeout, 1000);
}
// Unlike setInterval, setTimeout waits for operation + delay

// Order in event loop
setTimeout(() => console.log('timeout'), 0);
setImmediate(() => console.log('immediate'));
// Order varies based on phase in event loop
// In top-level (not in I/O): order is non-deterministic
// In I/O callback: immediate always runs before timer

// In I/O callback
fs.readFile('file.txt', () => {
  setTimeout(() => console.log('timeout'), 0);
  setImmediate(() => console.log('immediate'));
});
// Output: immediate, timeout
```

---

### Q292: What is the `util` module in Node.js?

**Answer:**

The `util` module provides utility functions: `promisify`, `callbackify`, `types`, `debuglog`, `format`, `inherits`, `inspect`.

```js
const util = require('util');

// promisify - callback to promise
const readFile = util.promisify(fs.readFile);
const data = await readFile('file.txt', 'utf8');

// callbackify - promise to callback
const cbFn = util.callbackify(async () => 'result');
cbFn((err, result) => console.log(result));

// format - printf-like
console.log(util.format('%s %d', 'hello', 42)); // 'hello 42'
console.log(util.formatWithOptions({ colors: true }, 'Message: %o', obj));

// inspect - object inspection
console.log(util.inspect({ a: 1, b: { c: 2 } }, { depth: 2, colors: true }));

// types
util.types.isDate(new Date()); // true
util.types.isPromise(Promise.resolve()); // true

// debuglog - namespaced debugging
const debug = util.debuglog('myapp');
debug('this is a debug message');
// NODE_DEBUG=myapp node script.js

// inherits (legacy, use class extends)
function Base() {}
function Child() {}
util.inherits(Child, Base);
```

---

### Q293: What is `npm` and `package.json`?

**Answer:**

`npm` is Node.js package manager. `package.json` defines project metadata, dependencies, scripts.

```json
{
  "name": "my-app",
  "version": "1.0.0",
  "description": "My application",
  "main": "index.js",
  "type": "module",
  "scripts": {
    "start": "node index.js",
    "dev": "node --watch index.js",
    "test": "jest",
    "build": "webpack"
  },
  "dependencies": {
    "express": "^4.18.0"
  },
  "devDependencies": {
    "jest": "^29.0.0"
  },
  "peerDependencies": {
    "react": "^18.0.0"
  },
  "engines": {
    "node": ">=18.0.0"
  },
  "exports": {
    ".": "./index.js",
    "./utils": "./utils.js"
  }
}
```

```bash
npm install express        # install package
npm install --save-dev jest # dev dependency
npm ci                     # clean install from lockfile
npm outdated               # check for outdated packages
npm audit                  # security audit
npm update                 # update packages
npx create-react-app my-app # run package without installing
```

---

### Q294: What is the `crypto` module?

**Answer:**

The `crypto` module provides cryptographic functionality.

```js
const crypto = require('crypto');

// Hash
const hash = crypto.createHash('sha256');
hash.update('Hello World');
console.log(hash.digest('hex'));

// HMAC (hash with key)
const hmac = crypto.createHmac('sha256', 'secret-key');
hmac.update('message');
console.log(hmac.digest('hex'));

// Random bytes
const buf = crypto.randomBytes(32);
console.log(buf.toString('hex'));

// UUID v4
const uuid = crypto.randomUUID();
console.log(uuid); // '550e8400-e29b-41d4-a716-446655440000'

// PBKDF2 (password hashing)
crypto.pbkdf2('password', 'salt', 100000, 64, 'sha512', (err, derivedKey) => {
  if (err) throw err;
  console.log(derivedKey.toString('hex'));
});

// Cipher/Decipher
const algorithm = 'aes-256-cbc';
const key = crypto.randomBytes(32);
const iv = crypto.randomBytes(16);

const cipher = crypto.createCipheriv(algorithm, key, iv);
let encrypted = cipher.update('Hello', 'utf8', 'hex');
encrypted += cipher.final('hex');

const decipher = crypto.createDecipheriv(algorithm, key, iv);
let decrypted = decipher.update(encrypted, 'hex', 'utf8');
decrypted += decipher.final('utf8');
console.log(decrypted); // 'Hello'
```

---

### Q295: What is `zlib` module?

**Answer:**

The `zlib` module provides compression/decompression (gzip, deflate, brotli).

```js
const zlib = require('zlib');
const fs = require('fs');
const { promisify } = require('util');

const gzip = promisify(zlib.gzip);
const gunzip = promisify(zlib.gunzip);

async function compress(input) {
  const compressed = await gzip(input);
  return compressed;
}

async function decompress(compressed) {
  const output = await gunzip(compressed);
  return output.toString();
}

// Stream compression
fs.createReadStream('input.txt')
  .pipe(zlib.createGzip())
  .pipe(fs.createWriteStream('input.txt.gz'));

fs.createReadStream('input.txt.gz')
  .pipe(zlib.createGunzip())
  .pipe(fs.createWriteStream('output.txt'));

// Brotli (better compression)
const brotliCompress = promisify(zlib.brotliCompress);
const brotliDecompress = promisify(zlib.brotliDecompress);

// Zlib constants
zlib.constants.Z_BEST_COMPRESSION; // 9
zlib.constants.Z_BEST_SPEED; // 1
zlib.constants.Z_DEFAULT_COMPRESSION; // -1
```

---

### Q296: What are `URL` and `URLSearchParams`?

**Answer:**

`URL` parses/constructs URLs. `URLSearchParams` handles query parameters.

```js
const url = new URL('https://user:pass@example.com:8080/path?q=hello#section');

console.log(url.protocol); // 'https:'
console.log(url.hostname); // 'example.com'
console.log(url.port); // '8080'
console.log(url.pathname); // '/path'
console.log(url.search); // '?q=hello'
console.log(url.hash); // '#section'
console.log(url.username); // 'user'
console.log(url.password); // 'pass'
console.log(url.origin); // 'https://example.com:8080'
console.log(url.href); // full URL

// Modify
url.pathname = '/new-path';
url.searchParams.set('q', 'world');
url.searchParams.append('page', '2');
console.log(url.href);

// URLSearchParams
const params = new URLSearchParams('q=hello&page=1&page=2');
params.get('q'); // 'hello'
params.get('page'); // '1' (first)
params.getAll('page'); // ['1', '2']
params.has('q'); // true
params.append('sort', 'asc');
params.delete('page');
params.toString(); // 'q=hello&sort=asc'

// From object
const obj = { q: 'search', limit: '10' };
const sp = new URLSearchParams(obj);
sp.toString(); // 'q=search&limit=10'
```

---

### Q297: What is `readline` module?

**Answer:**

The `readline` module provides interface for reading from readable streams (e.g., stdin).

```js
const readline = require('readline');

// CLI prompt
const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});

rl.question('What is your name? ', (answer) => {
  console.log(`Hello, ${answer}!`);
  rl.close();
});

rl.on('close', () => {
  console.log('Goodbye!');
  process.exit(0);
});

// Async/await version
function ask(question) {
  return new Promise((resolve) => {
    const rl = readline.createInterface({
      input: process.stdin,
      output: process.stdout
    });
    rl.question(question, (answer) => {
      rl.close();
      resolve(answer);
    });
  });
}

const name = await ask('Name: ');
const age = await ask('Age: ');
console.log(`${name} is ${age} years old`);
```

---

### Q298: What are `assertion` testing in Node.js?

**Answer:**

The `assert` module provides testing assertions. Use the `strict` version for strict equality.

```js
const assert = require('assert/strict');

// Strict comparisons
assert.strictEqual(1, 1); // passes
assert.strictEqual(1, '1'); // AssertionError (different types)
assert.notStrictEqual(1, '1'); // passes

// Deep equality
assert.deepStrictEqual({ a: 1 }, { a: 1 }); // passes
assert.deepStrictEqual({ a: 1 }, { a: '1' }); // fails (types differ)

// Throws
assert.throws(() => { throw new Error('fail'); });
assert.throws(() => { throw new Error('fail'); }, /fail/);
assert.rejects(Promise.reject(new Error('fail')), /fail/);

// Does not throw
assert.doesNotThrow(() => {});

// If, fail
assert.ok(true);
assert.ok(value !== null, 'Value should not be null');
assert.fail('Should not reach here');

// Custom messages
assert.strictEqual(a, b, `Expected ${a} to equal ${b}`);

// Difference between regular and strict assert:
// assert (legacy): uses == for comparisons
// assert/strict: uses === for comparisons
```

---

### Q299: What are the console methods in Node.js?

**Answer:**

`console` provides debugging output. Extended in Node.js with `console.table`, `console.time`, etc.

```js
// Basic
console.log('Basic log');
console.error('Error output'); // stderr
console.warn('Warning'); // stderr

// Format
console.log('Hello %s, you have %d messages', 'Alice', 5);
console.log('Object: %o', { a: 1, b: 2 });
console.log('JSON: %j', { a: 1, b: 2 });

// Timing
console.time('operation');
heavyOperation();
console.timeEnd('operation'); // 'operation: 123ms'

// Table
const users = [
  { name: 'Alice', age: 30 },
  { name: 'Bob', age: 25 }
];
console.table(users);

// Count
console.count('counter'); // 1
console.count('counter'); // 2
console.countReset('counter');

// Trace
console.trace('Stack trace');

// Group
console.group('User Details');
console.log('Name: Alice');
console.log('Age: 30');
console.groupEnd();

// Assert
console.assert(value === 42, 'Value is not 42');
```

---

### Q300: What is the `vm` module?

**Answer:**

The `vm` module runs JavaScript code in a sandboxed context. Useful for executing untrusted code or custom DSLs.

```js
const vm = require('vm');

// Run code in current context
vm.runInThisContext('console.log("hello")');

// Run in new context (sandbox)
const sandbox = { x: 1, console };
vm.createContext(sandbox);
vm.runInContext('console.log(x + 1)', sandbox); // 2

// Script object (compile once, run multiple times)
const code = 'y = x * 2';
const script = new vm.Script(code);
const context = vm.createContext({ x: 5, y: 0, console });
script.runInContext(context);
console.log(context.y); // 10

// Timeout for untrusted code
try {
  vm.runInNewContext('while(true) {}', {}, { timeout: 100 });
} catch (err) {
  console.log('Script timed out');
}

// Error handling
try {
  vm.runInNewContext('throw new Error("custom")');
} catch (err) {
  console.log(err.message); // 'custom'
}

// WARNING: vm is NOT a security sandbox
// Untrusted code can still escape with proper techniques
```

---

## Phase 7: Node.js (Continued) — Q301–Q380

---

### Q301: What is the `os` module?

**Answer:**

The `os` module provides operating system-related utility methods and properties.

```js
const os = require('os');

console.log('Platform:', os.platform());
console.log('Architecture:', os.arch());
console.log('Type:', os.type());
console.log('Release:', os.release());
console.log('Hostname:', os.hostname());
console.log('Uptime:', os.uptime(), 'seconds');
console.log('Load Average:', os.loadavg());

console.log('Total Memory:', os.totalmem());
console.log('Free Memory:', os.freemem());

console.log('CPU Count:', os.cpus().length);
console.log('CPU Info:', os.cpus()[0]);

console.log('Network:', os.networkInterfaces());
console.log('Home Dir:', os.homedir());
console.log('Temp Dir:', os.tmpdir());
console.log('User:', os.userInfo());
console.log('Endianness:', os.endianness());
console.log('EOL:', JSON.stringify(os.EOL));
```

---

### Q302: What is the `path` module?

**Answer:**

The `path` module provides utilities for working with file and directory paths.

```js
const path = require('path');

console.log(path.join('/foo', 'bar', 'baz/asdf'));
console.log(path.join('a', 'b', '..', 'c'));

console.log(path.resolve('foo/bar'));
console.log(path.resolve('/foo', 'bar'));

const parsed = path.parse('/home/user/file.txt');
console.log(parsed);
console.log(path.format(parsed));

console.log(path.basename('/foo/bar/file.txt'));
console.log(path.dirname('/foo/bar/file.txt'));
console.log(path.extname('/foo/bar/file.txt'));

console.log(path.relative('/data/a', '/data/b/file.txt'));
console.log(path.normalize('/foo/bar//baz/../asd'));

console.log(path.sep);
console.log(path.delimiter);

console.log(path.isAbsolute('/foo/bar'));
console.log(path.isAbsolute('./foo'));
```

---

### Q303: How does Node.js handle DNS lookups?

**Answer:**

Node.js provides the `dns` module for DNS resolution with two approaches: `lookup` (OS facilities) and `resolve*` (actual DNS queries).

```js
const dns = require('dns');

dns.lookup('google.com', (err, address, family) => {
  console.log('address:', address, 'family:', family);
});

dns.lookup('google.com', { all: true }, (err, addresses) => {
  console.log('all addresses:', addresses);
});

dns.resolve4('google.com', (err, addresses) => {
  console.log('IPv4 addresses:', addresses);
});

dns.resolve6('google.com', (err, addresses) => {
  console.log('IPv6 addresses:', addresses);
});

dns.resolve('google.com', 'MX', (err, records) => {
  console.log('MX records:', records);
});

dns.reverse('8.8.8.8', (err, hostnames) => {
  console.log('hostnames:', hostnames);
});

async function dnsLookup() {
  const addresses = await dns.promises.resolve4('google.com');
  console.log(addresses);
}
dnsLookup();
```

---

### Q304: What is the `net` module?

**Answer:**

The `net` module provides an asynchronous network API for creating TCP servers and clients.

```js
const net = require('net');

const server = net.createServer((socket) => {
  console.log('Client connected');

  socket.on('data', (data) => {
    console.log('Received:', data.toString());
    socket.write('Echo: ' + data.toString());
  });

  socket.on('end', () => {
    console.log('Client disconnected');
  });

  socket.on('error', (err) => {
    console.log('Socket error:', err.message);
  });
});

server.listen(8080, () => {
  console.log('Server listening on port 8080');
});

const client = new net.Socket();
client.connect(8080, 'localhost', () => {
  console.log('Connected to server');
  client.write('Hello from client');
});

client.on('data', (data) => {
  console.log('Server response:', data.toString());
  client.destroy();
});

client.on('close', () => {
  console.log('Connection closed');
});
```

---

### Q305: What is the `dgram` module for UDP?

**Answer:**

The `dgram` module provides UDP datagram socket implementation for connectionless communication.

```js
const dgram = require('dgram');

const server = dgram.createSocket('udp4');

server.on('message', (msg, rinfo) => {
  console.log('Server got: ' + msg + ' from ' + rinfo.address + ':' + rinfo.port);
  server.send('ACK', rinfo.port, rinfo.address);
});

server.on('listening', () => {
  const addr = server.address();
  console.log('Server listening ' + addr.address + ':' + addr.port);
});

server.bind(41234);

const client = dgram.createSocket('udp4');
const message = Buffer.from('Hello UDP');

client.send(message, 41234, 'localhost', (err) => {
  if (err) console.log(err);
  client.close();
});

client.on('message', (msg) => {
  console.log('Client received:', msg.toString());
  client.close();
});
```

---

### Q306: What are Node.js timers and their differences?

**Answer:**

Node.js provides `setTimeout`, `setInterval`, `setImmediate`, and `process.nextTick`, each with different execution order within the event loop.

```js
setTimeout(() => {
  console.log('timeout');
}, 0);

const interval = setInterval(() => {
  console.log('interval');
  clearInterval(interval);
}, 1000);

setImmediate(() => {
  console.log('immediate');
});

process.nextTick(() => {
  console.log('nextTick');
});

const timer = setTimeout(() => {}, 100000);
timer.unref();
timer.ref();

setTimeout((a, b) => {
  console.log(a + b);
}, 100, 1, 2);
```

---

### Q307: What is `process.nextTick` vs `setImmediate`?

**Answer:**

`process.nextTick` fires before the next event loop iteration (microtask), while `setImmediate` fires after the current poll phase. `nextTick` has higher priority.

```js
process.nextTick(() => console.log('nextTick 1'));
setImmediate(() => console.log('setImmediate 1'));
setTimeout(() => console.log('setTimeout 1'), 0);

const fs = require('fs');
fs.readFile(__filename, () => {
  setImmediate(() => console.log('setImmediate after I/O'));
  setTimeout(() => console.log('setTimeout after I/O'), 0);
  process.nextTick(() => console.log('nextTick after I/O'));
});
```

---

### Q308: How to handle uncaught exceptions and unhandled rejections?

**Answer:**

Node.js provides process-level events for catching unhandled errors and promise rejections.

```js
process.on('uncaughtException', (err, origin) => {
  console.error('Uncaught Exception:', err);
  process.exit(1);
});

process.on('unhandledRejection', (reason, promise) => {
  console.error('Unhandled Rejection at:', promise);
  console.error('Reason:', reason);
});

process.on('warning', (warning) => {
  console.warn(warning.name);
  console.warn(warning.message);
});

async function riskyOperation() {
  try {
    await someAsyncFunction();
  } catch (err) {
    console.error('Caught error:', err);
  }
}
```

---

### Q309: What is the readline module?

**Answer:**

The `readline` module provides an interface for reading data from a readable stream one line at a time.

```js
const readline = require('readline');

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout,
  prompt: '> '
});

rl.prompt();

rl.on('line', (line) => {
  switch (line.trim()) {
    case 'hello':
      console.log('world!');
      break;
    case 'exit':
      rl.close();
      break;
    default:
      console.log('Echo: ' + line);
  }
  rl.prompt();
});

rl.on('close', () => {
  console.log('Goodbye!');
  process.exit(0);
});

const rl2 = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});

rl2.question('What is your name? ', (name) => {
  console.log('Hello, ' + name + '!');
  rl2.close();
});
```

---

### Q310: What is the `util` module?

**Answer:**

The `util` module provides utility functions for debugging, formatting, inheritance, and type checking.

```js
const util = require('util');
const fs = require('fs');

const readFile = util.promisify(fs.readFile);

async function read() {
  const data = await readFile('file.txt', 'utf8');
  console.log(data);
}

console.log(util.format('%s:%s', 'foo', 'bar'));
console.log(util.format(1, 2, 3));

console.log(util.types.isDate(new Date()));
console.log(util.types.isPromise(Promise.resolve()));
console.log(util.types.isRegExp(/test/));
console.log(util.types.isMap(new Map()));

const obj = { a: 1, b: { c: 2 }, d: [1, 2, 3] };
console.log(util.inspect(obj, { showHidden: false, depth: 2, colors: true }));
```

---

### Q311: How does Node.js handle HTTP2?

**Answer:**

Node.js supports HTTP/2 via the `http2` module with server push, multiplexing, header compression, and stream prioritization.

```js
const http2 = require('http2');

const server = http2.createSecureServer({
  key: fs.readFileSync('server-key.pem'),
  cert: fs.readFileSync('server-cert.pem')
});

server.on('error', (err) => console.error(err));

server.on('stream', (stream, headers) => {
  stream.respond({
    'content-type': 'text/plain',
    ':status': 200
  });
  stream.end('Hello from HTTP/2');
});

server.listen(8443);

const client = http2.connect('https://localhost:8443', {
  ca: fs.readFileSync('server-cert.pem')
});

const req = client.request({ ':path': '/' });

req.on('response', (headers, flags) => {
  console.log('Response headers:', headers);
});

let data = '';
req.setEncoding('utf8');
req.on('data', (chunk) => data += chunk);
req.on('end', () => {
  console.log('Body:', data);
  client.close();
});

req.end();
```

---

### Q312: What is the `https` module?

**Answer:**

The `https` module is the TLS/SSL version of `http` for creating secure servers and making secure requests.

```js
const https = require('https');
const fs = require('fs');

const options = {
  key: fs.readFileSync('private-key.pem'),
  cert: fs.readFileSync('certificate.pem'),
  ca: fs.readFileSync('ca-cert.pem'),
  passphrase: 'secret',
  requestCert: true,
  rejectUnauthorized: true
};

const server = https.createServer(options, (req, res) => {
  res.writeHead(200, { 'Content-Type': 'text/plain' });
  res.end('Secure Hello\n');
});

server.listen(443, () => {
  console.log('HTTPS server on port 443');
});

const req = https.get('https://api.github.com/users/octocat', {
  headers: { 'User-Agent': 'Node.js' }
}, (res) => {
  let data = '';
  res.on('data', (chunk) => data += chunk);
  res.on('end', () => {
    console.log(JSON.parse(data));
  });
});

req.on('error', (e) => console.error(e));
```

---

### Q313: What is the `crypto` module for hashing and encryption?

**Answer:**

The `crypto` module provides cryptographic functionality including hashing, HMAC, encryption, decryption, and digital signatures.

```js
const crypto = require('crypto');

const hash = crypto.createHash('sha256');
hash.update('Hello, world!');
console.log(hash.digest('hex'));

const hmac = crypto.createHmac('sha256', 'secret-key');
hmac.update('message');
console.log(hmac.digest('hex'));

const buf = crypto.randomBytes(16);
console.log(buf.toString('hex'));

const uuid = crypto.randomUUID();
console.log(uuid);

const algorithm = 'aes-256-cbc';
const key = crypto.randomBytes(32);
const iv = crypto.randomBytes(16);

function encrypt(text) {
  const cipher = crypto.createCipheriv(algorithm, key, iv);
  let encrypted = cipher.update(text, 'utf8', 'hex');
  encrypted += cipher.final('hex');
  return { iv: iv.toString('hex'), encryptedData: encrypted };
}

function decrypt(encrypted) {
  const decipher = crypto.createDecipheriv(
    algorithm,
    key,
    Buffer.from(encrypted.iv, 'hex')
  );
  let decrypted = decipher.update(encrypted.encryptedData, 'hex', 'utf8');
  decrypted += decipher.final('utf8');
  return decrypted;
}

const encrypted = encrypt('Secret message');
console.log('Encrypted:', encrypted);
console.log('Decrypted:', decrypt(encrypted));
```

---

### Q314: What is the `zlib` module?

**Answer:**

The `zlib` module provides compression/decompression using Gzip, Deflate/Inflate, and Brotli.

```js
const zlib = require('zlib');
const fs = require('fs');

const gzip = zlib.createGzip();
const input = fs.createReadStream('input.txt');
const output = fs.createWriteStream('input.txt.gz');
input.pipe(gzip).pipe(output);

const gunzip = zlib.createGunzip();
const compressed = fs.createReadStream('input.txt.gz');
const decompressed = fs.createWriteStream('output.txt');
compressed.pipe(gunzip).pipe(decompressed);

async function compressData(data) {
  const buffer = Buffer.from(data, 'utf8');
  const compressed = await zlib.gzip(buffer);
  console.log('Compressed: ' + buffer.length + ' -> ' + compressed.length + ' bytes');
  const decompressed = await zlib.gunzip(compressed);
  return decompressed.toString();
}

compressData('Hello, world!').then(console.log);
```

---

### Q315: What are HTTP methods and status codes in Node.js?

**Answer:**

HTTP methods define the action to perform, and status codes indicate the result. Node.js handles them via `http.ServerResponse`.

```js
const http = require('http');

const server = http.createServer((req, res) => {
  console.log('Method:', req.method);
  console.log('URL:', req.url);

  if (req.method === 'GET' && req.url === '/api/users') {
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify([{ id: 1, name: 'Alice' }]));
  } else if (req.method === 'POST' && req.url === '/api/users') {
    let body = '';
    req.on('data', (chunk) => body += chunk);
    req.on('end', () => {
      const user = JSON.parse(body);
      res.writeHead(201, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({ id: 2, ...user }));
    });
  } else {
    res.writeHead(404, { 'Content-Type': 'text/plain' });
    res.end('Not Found');
  }
});
```

---

### Q316: What is Express.js and how does it work?

**Answer:**

Express.js is a minimal web framework for Node.js that provides routing, middleware, and HTTP utilities.

```js
const express = require('express');
const app = express();

app.use(express.json());
app.use(express.urlencoded({ extended: true }));

app.use((req, res, next) => {
  console.log(req.method + ' ' + req.url);
  next();
});

function authenticate(req, res, next) {
  const token = req.headers.authorization;
  if (token === 'Bearer valid-token') {
    req.user = { id: 1, name: 'Alice' };
    next();
  } else {
    res.status(401).json({ error: 'Unauthorized' });
  }
}

app.get('/', (req, res) => {
  res.send('Hello World');
});

app.get('/api/users', authenticate, (req, res) => {
  res.json([{ id: 1, name: 'Alice' }]);
});

app.get('/api/users/:id', (req, res) => {
  res.json({ id: req.params.id });
});

app.get('/search', (req, res) => {
  const q = req.query.q;
  res.json({ query: q });
});

app.post('/api/users', (req, res) => {
  const user = req.body;
  res.status(201).json(user);
});

app.use((err, req, res, next) => {
  console.error(err.stack);
  res.status(500).json({ error: 'Something broke!' });
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log('Server on port ' + PORT);
});
```

---

### Q317: What are Express middleware types?

**Answer:**

Express has application-level, router-level, error-handling, built-in, and third-party middleware.

```js
const express = require('express');
const app = express();

app.use((req, res, next) => {
  console.log('Request Time:', Date.now());
  next();
});

app.use('/api', (req, res, next) => {
  console.log('API request');
  next();
});

const router = express.Router();
router.use((req, res, next) => {
  console.log('Router middleware');
  next();
});
router.get('/users', (req, res) => res.send('Users'));
app.use('/admin', router);

app.use((err, req, res, next) => {
  console.error(err.stack);
  res.status(err.status || 500).json({
    error: err.message || 'Internal Error'
  });
});

app.use(express.json());
app.use(express.urlencoded({ extended: false }));
app.use(express.static('public'));

function requireRole(role) {
  return (req, res, next) => {
    if (req.user && req.user.role === role) {
      next();
    } else {
      res.status(403).json({ error: 'Forbidden' });
    }
  };
}
```

---

### Q318: What are WebSockets and how to use them in Node.js?

**Answer:**

WebSockets provide full-duplex communication over a single TCP connection. The `ws` library is commonly used.

```js
const WebSocket = require('ws');

const wss = new WebSocket.Server({ port: 8080 });

wss.on('connection', (ws, req) => {
  console.log('Client connected');
  ws.send(JSON.stringify({ type: 'welcome', message: 'Connected!' }));

  ws.on('message', (data) => {
    const message = JSON.parse(data.toString());
    console.log('Received:', message);
    ws.send(JSON.stringify({ type: 'echo', data: message }));
  });

  ws.on('close', () => {
    console.log('Client disconnected');
  });

  ws.on('error', (err) => {
    console.error('WebSocket error:', err);
  });
});

const ws = new WebSocket('ws://localhost:8080');

ws.on('open', () => {
  console.log('Connected to server');
  ws.send(JSON.stringify({ type: 'chat', text: 'Hello!' }));
});

ws.on('message', (data) => {
  console.log('Server:', JSON.parse(data));
});
```

---

### Q319: What is Socket.IO and how is it different from raw WebSockets?

**Answer:**

Socket.IO provides auto-reconnection, fallback transports, rooms, namespaces, and event-based messaging on top of WebSockets.

```js
const io = require('socket.io')(3000, {
  cors: { origin: '*' },
  transports: ['websocket', 'polling']
});

io.use((socket, next) => {
  const token = socket.handshake.auth.token;
  if (token === 'valid') {
    next();
  } else {
    next(new Error('Authentication error'));
  }
});

io.on('connection', (socket) => {
  console.log('Client connected:', socket.id);
  socket.join('room1');

  socket.on('chat message', (msg) => {
    io.to('room1').emit('chat message', msg);
    socket.broadcast.emit('chat message', msg);
  });

  socket.on('disconnect', (reason) => {
    console.log('Disconnected:', reason);
  });
});

const adminNamespace = io.of('/admin');
adminNamespace.on('connection', (socket) => {
  console.log('Admin connected:', socket.id);
});
```

---

### Q320: How do you handle environment variables in Node.js?

**Answer:**

Environment variables are accessed via `process.env` and commonly managed with `.env` files and the `dotenv` package.

```js
const nodeEnv = process.env.NODE_ENV || 'development';
const port = process.env.PORT || 3000;
const dbUrl = process.env.DATABASE_URL;

const config = {
  nodeEnv: process.env.NODE_ENV || 'development',
  port: parseInt(process.env.PORT || '3000', 10),
  dbUrl: process.env.DATABASE_URL,
  isDev: process.env.NODE_ENV !== 'production',
  isProd: process.env.NODE_ENV === 'production',
  logLevel: process.env.LOG_LEVEL || 'info',
};

function validateEnv() {
  const required = ['DATABASE_URL', 'SECRET_KEY'];
  const missing = required.filter(key => !process.env[key]);
  if (missing.length > 0) {
    throw new Error('Missing env vars: ' + missing.join(', '));
  }
}
```

---

### Q321: What are environment-specific configurations in Node.js?

**Answer:**

Configurations vary by environment (development, testing, staging, production) using env vars and config files.

```js
const config = {
  development: {
    port: 3000,
    db: { host: 'localhost', port: 5432, database: 'app_dev', logging: true },
    logLevel: 'debug',
    cors: { origin: '*' }
  },
  test: {
    port: 3001,
    db: { host: 'localhost', port: 5432, database: 'app_test', logging: false },
    logLevel: 'silent'
  },
  production: {
    port: parseInt(process.env.PORT || '8080', 10),
    db: {
      host: process.env.DB_HOST,
      port: parseInt(process.env.DB_PORT || '5432', 10),
      database: process.env.DB_NAME,
      logging: false
    },
    logLevel: 'info',
    cors: { origin: process.env.CORS_ORIGIN ? process.env.CORS_ORIGIN.split(',') : [] }
  }
};

module.exports = config[process.env.NODE_ENV || 'development'];

const isDev = process.env.NODE_ENV === 'development';
const isProd = process.env.NODE_ENV === 'production';
const isTest = process.env.NODE_ENV === 'test';
```

---

### Q322: What is the `perf_hooks` module?

**Answer:**

The `perf_hooks` module provides performance measurement APIs including high-resolution timestamps and performance measurements.

```js
const { performance, PerformanceObserver, monitorEventLoopDelay } = require('perf_hooks');

const start = performance.now();
const duration = performance.now() - start;
console.log('Duration: ' + duration + 'ms');

performance.mark('start');
performance.mark('end');
performance.measure('task1', 'start', 'end');

const measures = performance.getEntriesByName('task1');
console.log(measures[0].duration);

const observer = new PerformanceObserver((list) => {
  const entries = list.getEntries();
  entries.forEach((entry) => {
    console.log(entry.name + ': ' + entry.duration + 'ms');
  });
});
observer.observe({ entryTypes: ['measure'] });

const h = monitorEventLoopDelay({ resolution: 20 });
h.enable();
setTimeout(() => {
  h.disable();
  console.log('Min delay: ' + h.min + 'ms');
  console.log('Max delay: ' + h.max + 'ms');
}, 10000);
```

---

### Q323: What is the `async_hooks` module?

**Answer:**

The `async_hooks` module tracks the lifetime of asynchronous resources in Node.js for debugging and diagnostics.

```js
const async_hooks = require('async_hooks');

const hook = async_hooks.createHook({
  init(asyncId, type, triggerAsyncId, resource) {
    console.log('Init: ' + type + '(' + asyncId + '), trigger: ' + triggerAsyncId);
  },
  before(asyncId) {
    console.log('Before: ' + asyncId);
  },
  after(asyncId) {
    console.log('After: ' + asyncId);
  },
  destroy(asyncId) {
    console.log('Destroy: ' + asyncId);
  }
});

hook.enable();

const { AsyncLocalStorage } = require('async_hooks');
const asyncLocalStorage = new AsyncLocalStorage();

function middleware(req, res, next) {
  asyncLocalStorage.run({ userId: req.headers['x-user-id'] }, () => {
    next();
  });
}

function getCurrentUser() {
  return asyncLocalStorage.getStore();
}
```

---

### Q324: How does Node.js handle internationalization (i18n)?

**Answer:**

Node.js provides the `Intl` object (built into V8) for locale-aware formatting of dates, numbers, and strings.

```js
const date = new Date();

const usFormatter = new Intl.DateTimeFormat('en-US');
console.log(usFormatter.format(date));

const deFormatter = new Intl.DateTimeFormat('de-DE');
console.log(deFormatter.format(date));

const customFormatter = new Intl.DateTimeFormat('en-US', {
  weekday: 'long',
  year: 'numeric',
  month: 'long',
  day: 'numeric',
  timeZone: 'UTC'
});
console.log(customFormatter.format(date));

const num = 1234567.89;
console.log(new Intl.NumberFormat('en-US').format(num));
console.log(new Intl.NumberFormat('de-DE').format(num));

console.log(new Intl.NumberFormat('en-US', {
  style: 'currency',
  currency: 'USD'
}).format(num));

const rtf = new Intl.RelativeTimeFormat('en', { numeric: 'auto' });
console.log(rtf.format(-1, 'day'));
console.log(rtf.format(1, 'hour'));
```

---

### Q325: What are CommonJS vs ES Modules in Node.js?

**Answer:**

Node.js supports both CommonJS (CJS) with `require`/`module.exports` and ES Modules (ESM) with `import`/`export`.

```js
// CommonJS
const add = (a, b) => a + b;
const subtract = (a, b) => a - b;
module.exports = { add, subtract };

// ES Modules
// export const add = (a, b) => a + b;
// export default function subtract(a, b) { return a - b; }

// CJS Dynamic require
const moduleName = 'fs';
const fs = require(moduleName);

// ESM Dynamic import
async function loadModule() {
  const lodash = await import('lodash');
  console.log(lodash.default);
}
```

---

### Q326: How do you create a CLI tool in Node.js?

**Answer:**

CLI tools use `#!/usr/bin/env node`, `process.argv`, and often the `commander` or `yargs` library.

```js
#!/usr/bin/env node

const args = process.argv.slice(2);
const command = args[0];

if (command === 'greet') {
  const name = args[1] || 'World';
  console.log('Hello, ' + name + '!');
} else if (command === 'add') {
  const sum = args.slice(1).reduce((a, b) => a + parseFloat(b), 0);
  console.log('Sum: ' + sum);
} else {
  console.log('Usage: my-cli [greet|add] [args...]');
}

process.on('SIGINT', () => {
  console.log('\nGoodbye!');
  process.exit(0);
});
```

---

### Q327: How do you create a REST API in Node.js?

**Answer:**

A REST API exposes CRUD operations via HTTP methods on resource endpoints.

```js
const http = require('http');

let users = [
  { id: '1', name: 'Alice', email: 'alice@example.com' },
  { id: '2', name: 'Bob', email: 'bob@example.com' }
];

const server = http.createServer((req, res) => {
  const method = req.method;
  const url = req.url;
  res.setHeader('Content-Type', 'application/json');

  if (method === 'GET' && url === '/users') {
    res.writeHead(200);
    res.end(JSON.stringify(users));
  } else if (method === 'GET' && url.startsWith('/users/')) {
    const id = url.split('/')[2];
    const user = users.find(u => u.id === id);
    if (user) {
      res.writeHead(200);
      res.end(JSON.stringify(user));
    } else {
      res.writeHead(404);
      res.end(JSON.stringify({ error: 'Not found' }));
    }
  } else if (method === 'POST' && url === '/users') {
    let body = '';
    req.on('data', chunk => body += chunk);
    req.on('end', () => {
      const { name, email } = JSON.parse(body);
      const newUser = { id: Date.now().toString(), name, email };
      users.push(newUser);
      res.writeHead(201);
      res.end(JSON.stringify(newUser));
    });
  } else {
    res.writeHead(404);
    res.end(JSON.stringify({ error: 'Route not found' }));
  }
});

server.listen(3000, () => {
  console.log('REST API on port 3000');
});
```

---

### Q328: What is GraphQL and how to use it in Node.js?

**Answer:**

GraphQL is a query language for APIs that lets clients request exactly the data they need. Used with `apollo-server`.

```js
const { ApolloServer, gql } = require('apollo-server');

const typeDefs = gql`
  type User {
    id: ID!
    name: String!
    email: String!
  }

  type Query {
    users: [User!]!
    user(id: ID!): User
  }

  type Mutation {
    createUser(name: String!, email: String!): User!
  }
`;

const users = [
  { id: '1', name: 'Alice', email: 'alice@test.com' },
  { id: '2', name: 'Bob', email: 'bob@test.com' }
];

const resolvers = {
  Query: {
    users: () => users,
    user: (_, { id }) => users.find(u => u.id === id)
  },
  Mutation: {
    createUser: (_, { name, email }) => {
      const user = { id: String(users.length + 1), name, email };
      users.push(user);
      return user;
    }
  }
};

const server = new ApolloServer({ typeDefs, resolvers });
server.listen(4000).then(({ url }) => {
  console.log('GraphQL server at ' + url);
});
```

---

### Q329: What is middleware architecture in Express?

**Answer:**

Middleware are functions with access to `req`, `res`, and `next` that execute code, modify req/res, end requests, or call the next middleware.

```js
const express = require('express');
const app = express();

app.use((req, res, next) => {
  console.log('[' + new Date().toISOString() + '] ' + req.method + ' ' + req.url);
  next();
});

app.use('/api', (req, res, next) => {
  const ip = req.ip;
  req.requestTime = Date.now();
  next();
});

const validateUser = (req, res, next) => {
  const name = req.body.name;
  const email = req.body.email;
  if (!name || !email) {
    return res.status(400).json({ error: 'Missing fields' });
  }
  if (!email.includes('@')) {
    return res.status(400).json({ error: 'Invalid email' });
  }
  next();
};

app.post('/api/users', validateUser, (req, res) => {
  const user = { id: Date.now(), ...req.body };
  res.status(201).json(user);
});

app.use((err, req, res, next) => {
  console.error('Unhandled error:', err);
  res.status(500).json({ error: 'Internal Server Error' });
});

const asyncHandler = (fn) => (req, res, next) => {
  Promise.resolve(fn(req, res, next)).catch(next);
};

app.get('/async', asyncHandler(async (req, res) => {
  const data = await fetchData();
  res.json(data);
}));
```

---

### Q330: What is a reverse proxy and how does it work with Node.js?

**Answer:**

A reverse proxy (like Nginx) sits in front of Node.js, handling TLS, load balancing, caching, and static file serving.

```nginx
upstream node_app {
    least_conn;
    server 127.0.0.1:3000 weight=5;
    server 127.0.0.1:3001 weight=3;
    keepalive 64;
}

server {
    listen 80;
    server_name example.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name example.com;

    location / {
        proxy_pass http://node_app;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

```js
const app = express();
app.set('trust proxy', true);

app.get('/', (req, res) => {
  console.log('Client IP:', req.ip);
  console.log('Protocol:', req.protocol);
  res.send('Hello');
});
```

---

### Q331: What is pm2 and how is it used for process management?

**Answer:**

PM2 is a production process manager for Node.js with clustering, monitoring, and auto-restart capabilities.

```bash
pm2 start app.js
pm2 start app.js --name "my-app"
pm2 start app.js -i max
pm2 start app.js -i 2

pm2 list
pm2 logs
pm2 monit
pm2 status
pm2 show my-app
pm2 stop my-app
pm2 restart my-app
pm2 delete my-app
pm2 reload all
pm2 scale my-app +2
pm2 startup
pm2 save
```

```js
// ecosystem.config.js
module.exports = {
  apps: [{
    name: 'my-app',
    script: './dist/index.js',
    instances: 'max',
    exec_mode: 'cluster',
    env: { NODE_ENV: 'development' },
    env_production: { NODE_ENV: 'production' },
    max_memory_restart: '1G',
    autorestart: true,
    max_restarts: 10,
    restart_delay: 4000
  }]
};
```

---

### Q332: What is the cluster module for scaling?

**Answer:**

The `cluster` module creates child processes that share server ports for load balancing across CPU cores.

```js
const cluster = require('cluster');
const http = require('http');
const os = require('os');

if (cluster.isMaster) {
  const numCPUs = os.cpus().length;
  console.log('Master ' + process.pid + ' is running');

  for (let i = 0; i < numCPUs; i++) {
    cluster.fork();
  }

  cluster.on('exit', (worker, code, signal) => {
    console.log('Worker ' + worker.process.pid + ' died');
    cluster.fork();
  });

} else {
  http.createServer((req, res) => {
    res.writeHead(200);
    res.end('Handled by worker ' + process.pid + '\n');
  }).listen(8000, () => {
    console.log('Worker ' + process.pid + ' started');
  });
}
```

---

### Q333: What is the repository pattern in Node.js?

**Answer:**

The repository pattern abstracts data access behind a consistent interface for easy swapping of databases or mocking.

```js
class UserRepository {
  async findAll() { throw new Error('Not implemented'); }
  async findById(id) { throw new Error('Not implemented'); }
  async create(data) { throw new Error('Not implemented'); }
  async update(id, data) { throw new Error('Not implemented'); }
  async delete(id) { throw new Error('Not implemented'); }
}

class InMemoryUserRepository extends UserRepository {
  constructor() {
    super();
    this.users = new Map();
  }

  async findAll() {
    return Array.from(this.users.values());
  }

  async findById(id) {
    return this.users.get(id) || null;
  }

  async create(data) {
    const id = Date.now().toString();
    const user = { id, ...data, createdAt: new Date() };
    this.users.set(id, user);
    return user;
  }

  async update(id, data) {
    const user = this.users.get(id);
    if (!user) return null;
    const updated = { ...user, ...data, updatedAt: new Date() };
    this.users.set(id, updated);
    return updated;
  }

  async delete(id) {
    return this.users.delete(id);
  }
}

class UserService {
  constructor(repository) {
    this.repository = repository;
  }

  async getAllUsers() {
    return this.repository.findAll();
  }

  async createUser(data) {
    if (!data.email || !data.email.includes('@')) {
      throw new Error('Invalid email');
    }
    return this.repository.create(data);
  }
}

const repo = process.env.NODE_ENV === 'test'
  ? new InMemoryUserRepository()
  : new PostgresUserRepository(db);
const service = new UserService(repo);
```

---

### Q334: What is the Strategy pattern in Node.js?

**Answer:**

The Strategy pattern allows selecting an algorithm at runtime, commonly used in authentication and payment processing.

```js
class AuthStrategy {
  async authenticate(credentials) {
    throw new Error('Not implemented');
  }
}

class LocalAuthStrategy extends AuthStrategy {
  async authenticate({ username, password }) {
    const user = await db.users.findByUsername(username);
    if (!user || !(await bcrypt.compare(password, user.password))) {
      throw new Error('Invalid credentials');
    }
    return user;
  }
}

class JWTStrategy extends AuthStrategy {
  async authenticate({ token }) {
    try {
      const decoded = jwt.verify(token, process.env.JWT_SECRET);
      const user = await db.users.findById(decoded.userId);
      if (!user) throw new Error('User not found');
      return user;
    } catch (err) {
      throw new Error('Invalid token');
    }
  }
}

class Authenticator {
  constructor() {
    this.strategies = new Map();
  }

  register(name, strategy) {
    this.strategies.set(name, strategy);
  }

  async authenticate(method, credentials) {
    const strategy = this.strategies.get(method);
    if (!strategy) {
      throw new Error('Unknown auth method: ' + method);
    }
    return strategy.authenticate(credentials);
  }
}

const authenticator = new Authenticator();
authenticator.register('local', new LocalAuthStrategy());
authenticator.register('jwt', new JWTStrategy());
```

---

### Q335: What is the Observer pattern in Node.js?

**Answer:**

Node.js EventEmitter is a built-in implementation of the Observer pattern where objects emit events and listeners observe them.

```js
const EventEmitter = require('events');

class OrderService extends EventEmitter {
  async createOrder(orderData) {
    const order = { id: Date.now(), ...orderData, status: 'created' };
    this.emit('order:created', order);
    return order;
  }
}

const orderService = new OrderService();

orderService.on('order:created', (order) => {
  console.log('[LOG] Order ' + order.id + ' created');
});

orderService.on('order:created', (order) => {
  console.log('[EMAIL] Sending confirmation for order ' + order.id);
});

orderService.once('order:created', (order) => {
  console.log('[AUDIT] First order: ' + order.id);
});

orderService.createOrder({ userId: 1, items: ['item1'] });

console.log(orderService.listenerCount('order:created'));
orderService.setMaxListeners(20);
```

---

### Q336: What are microservices patterns in Node.js?

**Answer:**

Microservices split an application into small, independent services communicating via HTTP, message queues, or gRPC.

```js
const express = require('express');
const app = express();

// Service registry
class ServiceRegistry {
  constructor() {
    this.services = new Map();
  }

  register(name, url) {
    this.services.set(name, url);
  }

  get(name) {
    return this.services.get(name);
  }
}

const registry = new ServiceRegistry();
registry.register('users', 'http://localhost:3001');
registry.register('orders', 'http://localhost:3002');

// Circuit breaker
class CircuitBreaker {
  constructor(fn, options = {}) {
    this.fn = fn;
    this.failureThreshold = options.failureThreshold || 5;
    this.resetTimeout = options.resetTimeout || 30000;
    this.failures = 0;
    this.state = 'CLOSED';
    this.lastFailureTime = null;
  }

  async call(...args) {
    if (this.state === 'OPEN') {
      if (Date.now() - this.lastFailureTime >= this.resetTimeout) {
        this.state = 'HALF_OPEN';
      } else {
        throw new Error('Circuit breaker is OPEN');
      }
    }
    try {
      const result = await this.fn(...args);
      this.failures = 0;
      this.state = 'CLOSED';
      return result;
    } catch (err) {
      this.failures++;
      this.lastFailureTime = Date.now();
      if (this.failures >= this.failureThreshold) {
        this.state = 'OPEN';
      }
      throw err;
    }
  }
}
```

---

### Q337: How do you implement caching in Node.js?

**Answer:**

Caching strategies include in-memory cache, LRU cache, Redis, and HTTP caching headers.

```js
class MemoryCache {
  constructor(ttl = 60000) {
    this.cache = new Map();
    this.ttl = ttl;
  }

  get(key) {
    const item = this.cache.get(key);
    if (!item) return null;
    if (Date.now() > item.expiry) {
      this.cache.delete(key);
      return null;
    }
    return item.value;
  }

  set(key, value, ttl = this.ttl) {
    this.cache.set(key, { value, expiry: Date.now() + ttl });
  }

  delete(key) { this.cache.delete(key); }
  clear() { this.cache.clear(); }
}

class LRUCache {
  constructor(capacity = 100) {
    this.capacity = capacity;
    this.cache = new Map();
  }

  get(key) {
    if (!this.cache.has(key)) return -1;
    const value = this.cache.get(key);
    this.cache.delete(key);
    this.cache.set(key, value);
    return value;
  }

  set(key, value) {
    if (this.cache.has(key)) {
      this.cache.delete(key);
    } else if (this.cache.size >= this.capacity) {
      this.cache.delete(this.cache.keys().next().value);
    }
    this.cache.set(key, value);
  }
}

function cacheMiddleware(duration) {
  const cache = new Map();
  return (req, res, next) => {
    const key = req.originalUrl;
    const cached = cache.get(key);
    if (cached && Date.now() < cached.expiry) {
      return res.json(cached.data);
    }
    const originalJson = res.json.bind(res);
    res.json = (data) => {
      cache.set(key, { data, expiry: Date.now() + duration });
      originalJson(data);
    };
    next();
  };
}
```

---

### Q338: What are batch operations and bulk processing in Node.js?

**Answer:**

Batch operations process multiple items in a single operation to reduce overhead in database operations, API calls, and file processing.

```js
async function batchInsertUsers(users, batchSize = 100) {
  const results = [];
  for (let i = 0; i < users.length; i += batchSize) {
    const batch = users.slice(i, i + batchSize);
    results.push(batch.length);
  }
  return results;
}

async function batchApiCalls(urls, concurrency = 5) {
  const results = [];
  const queue = [...urls];

  async function worker() {
    while (queue.length > 0) {
      const url = queue.shift();
      try {
        const response = await fetch(url);
        const data = await response.json();
        results.push({ url, data, status: 'success' });
      } catch (err) {
        results.push({ url, error: err.message, status: 'failed' });
      }
    }
  }

  const workers = Array(concurrency).fill(null).map(() => worker());
  await Promise.all(workers);
  return results;
}

async function batchWithPartialSuccess(items, processFn) {
  const results = await Promise.allSettled(items.map(item => processFn(item)));
  const succeeded = [];
  const failed = [];
  results.forEach((result, index) => {
    if (result.status === 'fulfilled') {
      succeeded.push({ index, value: result.value });
    } else {
      failed.push({ index, reason: result.reason });
    }
  });
  return { succeeded, failed, total: items.length };
}
```

---

### Q339: How do you handle database operations in Node.js?

**Answer:**

Database operations use drivers (pg, mysql2) or ORMs (Sequelize, Prisma, Mongoose) for PostgreSQL, MongoDB, and other databases.

```js
const { Pool } = require('pg');
const pool = new Pool({
  host: 'localhost',
  port: 5432,
  database: 'myapp',
  user: 'user',
  password: 'password',
  max: 20,
  idleTimeoutMillis: 30000
});

async function getUsers() {
  const { rows } = await pool.query('SELECT * FROM users WHERE active = $1', [true]);
  return rows;
}

async function createUserWithProfile(userData, profileData) {
  const client = await pool.connect();
  try {
    await client.query('BEGIN');
    const { rows } = await client.query(
      'INSERT INTO users (name, email) VALUES ($1, $2) RETURNING id',
      [userData.name, userData.email]
    );
    await client.query('COMMIT');
    return rows[0].id;
  } catch (err) {
    await client.query('ROLLBACK');
    throw err;
  } finally {
    client.release();
  }
}
```

---

### Q340: How do you implement authentication and authorization in Node.js?

**Answer:**

Authentication verifies identity using JWT, sessions, or OAuth. Authorization controls access via RBAC or middleware.

```js
const jwt = require('jsonwebtoken');
const bcrypt = require('bcrypt');
const express = require('express');
const app = express();

app.use(express.json());

const users = [];

app.post('/api/register', async (req, res) => {
  const { username, password } = req.body;
  const hashedPassword = await bcrypt.hash(password, 10);
  users.push({ id: users.length + 1, username, password: hashedPassword });
  res.status(201).json({ message: 'User created' });
});

app.post('/api/login', async (req, res) => {
  const { username, password } = req.body;
  const user = users.find(u => u.username === username);
  if (!user || !(await bcrypt.compare(password, user.password))) {
    return res.status(401).json({ error: 'Invalid credentials' });
  }
  const token = jwt.sign(
    { userId: user.id, username: user.username, role: 'user' },
    process.env.JWT_SECRET,
    { expiresIn: '1h' }
  );
  res.json({ token });
});

function authenticate(req, res, next) {
  const authHeader = req.headers.authorization;
  if (!authHeader || !authHeader.startsWith('Bearer ')) {
    return res.status(401).json({ error: 'No token provided' });
  }
  try {
    req.user = jwt.verify(authHeader.split(' ')[1], process.env.JWT_SECRET);
    next();
  } catch (err) {
    res.status(401).json({ error: 'Invalid token' });
  }
}

function authorize(...roles) {
  return (req, res, next) => {
    if (!roles.includes(req.user.role)) {
      return res.status(403).json({ error: 'Insufficient permissions' });
    }
    next();
  };
}

app.get('/api/profile', authenticate, (req, res) => {
  res.json({ user: req.user });
});

app.get('/api/admin', authenticate, authorize('admin'), (req, res) => {
  res.json({ message: 'Admin access granted' });
});
```

---

### Q341: What are WebSockets used for real-time applications?

**Answer:**

WebSockets enable real-time bidirectional communication for chat, live updates, gaming, and streaming data.

```js
const WebSocket = require('ws');
const wss = new WebSocket.Server({ port: 8080 });

const clients = new Map();

wss.on('connection', (ws) => {
  const id = Date.now();
  clients.set(id, ws);
  ws.send(JSON.stringify({ type: 'system', message: 'Welcome!', id }));

  ws.on('message', (data) => {
    const msg = JSON.parse(data.toString());
    wss.clients.forEach((client) => {
      if (client.readyState === WebSocket.OPEN) {
        client.send(JSON.stringify({
          type: 'chat',
          user: msg.user,
          message: msg.message,
          timestamp: Date.now()
        }));
      }
    });
  });

  ws.on('close', () => {
    clients.delete(id);
  });
});
```

---

### Q342: What is rate limiting and how to implement it?

**Answer:**

Rate limiting controls request frequency using token bucket, sliding window, or fixed window algorithms.

```js
class SlidingWindowRateLimiter {
  constructor(windowMs, maxRequests) {
    this.windowMs = windowMs;
    this.maxRequests = maxRequests;
    this.requests = new Map();
  }

  isAllowed(key) {
    const now = Date.now();
    const windowStart = now - this.windowMs;

    if (!this.requests.has(key)) {
      this.requests.set(key, []);
    }

    const timestamps = this.requests.get(key);
    while (timestamps.length > 0 && timestamps[0] < windowStart) {
      timestamps.shift();
    }

    if (timestamps.length >= this.maxRequests) {
      return false;
    }

    timestamps.push(now);
    return true;
  }
}

const rateLimiter = new SlidingWindowRateLimiter(60000, 10);

function rateLimitMiddleware(req, res, next) {
  const key = req.ip;
  if (!rateLimiter.isAllowed(key)) {
    return res.status(429).json({ error: 'Too many requests' });
  }
  next();
}

app.use('/api', rateLimitMiddleware);
```

---

### Q343: What is the CQRS pattern?

**Answer:**

CQRS (Command Query Responsibility Segregation) separates read and write operations into different models or services.

```js
class UserCommandService {
  constructor(writeRepository) {
    this.repository = writeRepository;
  }

  async createUser(command) {
    const user = {
      id: Date.now().toString(),
      name: command.name,
      email: command.email,
      createdAt: new Date()
    };
    await this.repository.save(user);
    return user;
  }
}

class UserQueryService {
  constructor(readRepository) {
    this.readRepository = readRepository;
  }

  async getUser(id) {
    return this.readRepository.findById(id);
  }

  async getUsers(filters) {
    return this.readRepository.find(filters);
  }
}

class EventBus {
  constructor() {
    this.subscribers = new Map();
  }

  subscribe(eventType, handler) {
    if (!this.subscribers.has(eventType)) {
      this.subscribers.set(eventType, []);
    }
    this.subscribers.get(eventType).push(handler);
  }

  publish(eventType, data) {
    const handlers = this.subscribers.get(eventType) || [];
    handlers.forEach(handler => handler({ type: eventType, data }));
  }
}
```

---

### Q344: How do you implement logging in Node.js?

**Answer:**

Logging involves structured output for debugging and monitoring. Use libraries like `winston` or `pino`.

```js
const { AsyncLocalStorage } = require('async_hooks');
const asyncLocalStorage = new AsyncLocalStorage();

function correlationMiddleware(req, res, next) {
  const correlationId = req.headers['x-correlation-id'] || Date.now().toString();
  asyncLocalStorage.run({ correlationId }, () => {
    res.setHeader('x-correlation-id', correlationId);
    next();
  });
}

function log(level, message, data = {}) {
  const context = asyncLocalStorage.getStore() || {};
  const entry = {
    level,
    message,
    ...data,
    correlationId: context.correlationId,
    timestamp: new Date().toISOString(),
    pid: process.pid
  };
  console.log(JSON.stringify(entry));
}

const logger = {
  info: (msg, data) => log('info', msg, data),
  error: (msg, err) => log('error', msg, { error: err?.message, stack: err?.stack }),
  warn: (msg, data) => log('warn', msg, data),
  debug: (msg, data) => log('debug', msg, data)
};
```

---

### Q345: What is the difference between SQL and NoSQL databases in Node.js?

**Answer:**

SQL databases (PostgreSQL, MySQL) use structured schemas and relations. NoSQL databases (MongoDB, Redis) offer flexible schemas.

```js
// SQL with fixed schema, relations, ACID
// CREATE TABLE users (
//   id SERIAL PRIMARY KEY,
//   name VARCHAR(255) NOT NULL,
//   email VARCHAR(255) UNIQUE NOT NULL
// );

// NoSQL with flexible schema, embedded documents
// {
//   _id: ObjectId(),
//   name: 'Alice',
//   email: 'alice@test.com',
//   tags: ['javascript', 'node'],
//   profile: { bio: 'Developer' }
// }

// When to use SQL: complex relationships, ACID transactions, fixed schema
// When to use NoSQL: flexible schema, hierarchical data, horizontal scaling

class UserService {
  constructor() {
    this.sqlDb = new SQLDatabase();
    this.cache = new RedisCache();
  }

  async getUser(id) {
    let user = await this.cache.get('user:' + id);
    if (user) return user;
    user = await this.sqlDb.query('SELECT * FROM users WHERE id = $1', [id]);
    await this.cache.set('user:' + id, user, 300);
    return user;
  }
}
```

---

### Q346: What is the Prisma ORM?

**Answer:**

Prisma is a modern ORM with type-safe database access, auto-generated queries, and migrations.

```js
const { PrismaClient } = require('@prisma/client');
const prisma = new PrismaClient();

async function createUser(data) {
  return prisma.user.create({ data });
}

async function getUsers() {
  return prisma.user.findMany({
    include: { posts: true },
    orderBy: { createdAt: 'desc' },
    take: 10
  });
}

async function getUser(id) {
  return prisma.user.findUnique({
    where: { id },
    include: { posts: { where: { published: true } } }
  });
}

async function updateUser(id, data) {
  return prisma.user.update({ where: { id }, data });
}

async function deleteUser(id) {
  return prisma.user.delete({ where: { id } });
}

async function searchUsers(searchTerm) {
  return prisma.user.findMany({
    where: {
      OR: [
        { name: { contains: searchTerm, mode: 'insensitive' } },
        { email: { contains: searchTerm, mode: 'insensitive' } }
      ]
    }
  });
}

async function getPaginatedUsers(page = 1, perPage = 10) {
  const skip = (page - 1) * perPage;
  const [users, total] = await Promise.all([
    prisma.user.findMany({ skip, take: perPage, orderBy: { createdAt: 'desc' } }),
    prisma.user.count()
  ]);
  return { users, total, page, perPage, totalPages: Math.ceil(total / perPage) };
}
```

---

### Q347: What is the Mongoose ODM?

**Answer:**

Mongoose is an ODM for MongoDB with schema validation, middleware, and query building.

```js
const mongoose = require('mongoose');
const { Schema } = mongoose;

mongoose.connect('mongodb://localhost:27017/myapp');

const userSchema = new Schema({
  name: { type: String, required: true, trim: true },
  email: { type: String, required: true, unique: true, lowercase: true },
  age: { type: Number, min: 0, max: 150 },
  role: { type: String, enum: ['user', 'admin'], default: 'user' },
  tags: [String],
  createdAt: { type: Date, default: Date.now },
  updatedAt: { type: Date, default: Date.now }
});

userSchema.virtual('isAdult').get(function() {
  return this.age >= 18;
});

userSchema.pre('save', function(next) {
  this.updatedAt = Date.now();
  next();
});

userSchema.statics.findByEmail = function(email) {
  return this.findOne({ email: email.toLowerCase() });
};

const User = mongoose.model('User', userSchema);

async function crudExample() {
  const user = new User({ name: 'Alice', email: 'alice@test.com', age: 30 });
  await user.save();

  const found = await User.findById(user._id);
  const foundByEmail = await User.findByEmail('alice@test.com');

  await User.findByIdAndUpdate(user._id, { age: 31 });
  await User.findByIdAndDelete(user._id);
}
```

---

### Q348: What is Redis and how is it used in Node.js?

**Answer:**

Redis is an in-memory data store used for caching, sessions, rate limiting, pub/sub, and queues.

```js
const redis = require('redis');

const client = redis.createClient({ url: 'redis://localhost:6379' });

client.on('error', (err) => console.error('Redis error:', err));

await client.connect();

await client.set('key', 'value');
await client.setEx('cached', 3600, 'data');
const value = await client.get('key');

await client.hSet('user:1', 'name', 'Alice');
await client.hSet('user:1', 'email', 'alice@test.com');
const user = await client.hGetAll('user:1');

await client.lPush('queue', 'job1');
const job = await client.rPop('queue');

await client.expire('key', 300);
const ttl = await client.ttl('key');

const pipeline = client.multi();
pipeline.set('a', '1');
pipeline.set('b', '2');
const results = await pipeline.exec();

const subscriber = client.duplicate();
await subscriber.connect();
await subscriber.subscribe('channel', (message) => {
  console.log('Received:', message);
});
await client.publish('channel', 'Hello!');
```

---

### Q349: What are worker threads in Node.js?

**Answer:**

Worker threads allow running JavaScript in parallel with separate V8 instances, ideal for CPU-intensive tasks.

```js
// worker.js
const { parentPort, workerData } = require('worker_threads');

function fibonacci(n) {
  if (n <= 1) return n;
  return fibonacci(n - 1) + fibonacci(n - 2);
}

const result = fibonacci(workerData.num);
parentPort.postMessage({ result });

// main.js
const { Worker } = require('worker_threads');
const path = require('path');

function runWorker(workerData) {
  return new Promise((resolve, reject) => {
    const worker = new Worker(path.join(__dirname, 'worker.js'), { workerData });
    worker.on('message', resolve);
    worker.on('error', reject);
    worker.on('exit', (code) => {
      if (code !== 0) reject(new Error('Worker exited with code ' + code));
    });
  });
}

async function parallelFib() {
  const numbers = [40, 41, 42, 43, 44];
  const results = await Promise.all(numbers.map(n => runWorker({ num: n })));
  console.log('Results:', results);
}
```

---

### Q350: What is the difference between cluster and worker_threads?

**Answer:**

Cluster forks processes (separate memory, share ports), while worker_threads spawns threads in the same process (shared memory via SharedArrayBuffer).

```js
const { Worker } = require('worker_threads');

// Worker threads share memory
const sharedBuffer = new SharedArrayBuffer(4);
const sharedArray = new Int32Array(sharedBuffer);

// Cluster forks processes (separate memory)
const cluster = require('cluster');
if (cluster.isMaster) {
  for (let i = 0; i < 4; i++) cluster.fork();
  cluster.on('exit', (worker) => cluster.fork());
} else {
  // Worker processes share ports
  http.createServer((req, res) => {
    res.end('Worker ' + process.pid);
  }).listen(3000);
}

// Use worker_threads for CPU-intensive tasks
// Use cluster for high availability and port sharing
```

---

### Q351: How do you handle file uploads in Node.js?

**Answer:**

File uploads use `multer` for multipart/form-data processing with storage configuration and file validation.

```js
const express = require('express');
const multer = require('multer');
const path = require('path');
const { randomUUID } = require('crypto');

const app = express();

const storage = multer.diskStorage({
  destination: (req, file, cb) => cb(null, 'uploads/'),
  filename: (req, file, cb) => {
    const ext = path.extname(file.originalname);
    cb(null, randomUUID() + ext);
  }
});

const fileFilter = (req, file, cb) => {
  const allowedTypes = ['image/jpeg', 'image/png', 'image/gif'];
  if (allowedTypes.includes(file.mimetype)) {
    cb(null, true);
  } else {
    cb(new Error('Invalid file type'), false);
  }
};

const upload = multer({
  storage,
  limits: { fileSize: 5 * 1024 * 1024, files: 3 },
  fileFilter
});

app.post('/upload', upload.single('file'), (req, res) => {
  res.json({
    message: 'File uploaded',
    file: {
      originalName: req.file.originalname,
      filename: req.file.filename,
      size: req.file.size,
      mimetype: req.file.mimetype
    }
  });
});

app.post('/upload-multiple', upload.array('files', 5), (req, res) => {
  res.json({
    message: 'Files uploaded',
    files: req.files.map(f => ({
      originalName: f.originalname,
      filename: f.filename,
      size: f.size
    }))
  });
});

app.use((err, req, res, next) => {
  if (err instanceof multer.MulterError) {
    return res.status(400).json({ error: err.message });
  }
  next(err);
});
```

---

### Q352: How do you implement search functionality in Node.js?

**Answer:**

Search can use SQL LIKE, full-text search, MongoDB text indexes, or Elasticsearch.

```js
// SQL LIKE search
async function searchPosts(query) {
  const result = await pool.query(
    'SELECT * FROM posts WHERE title ILIKE $1 OR content ILIKE $1 ORDER BY created_at DESC LIMIT 20',
    ['%' + query + '%']
  );
  return result.rows;
}

// PostgreSQL full-text search
async function fullTextSearch(query) {
  const result = await pool.query(
    `SELECT *, ts_rank(to_tsvector('english', title || ' ' || content),
            plainto_tsquery('english', $1)) AS rank
     FROM posts
     WHERE to_tsvector('english', title || ' ' || content) @@
           plainto_tsquery('english', $1)
     ORDER BY rank DESC LIMIT 20`,
    [query]
  );
  return result.rows;
}

// Search service abstraction
class SearchService {
  constructor() {
    this.engine = process.env.SEARCH_ENGINE || 'basic';
  }

  async search(query, options = {}) {
    switch (this.engine) {
      case 'elasticsearch': return this.esSearch(query, options);
      case 'postgres': return this.pgSearch(query, options);
      default: return this.basicSearch(query, options);
    }
  }
}
```

---

### Q353: What are health checks and readiness probes?

**Answer:**

Health checks monitor application availability. Readiness probes indicate when the app is ready to serve traffic.

```js
const express = require('express');
const app = express();

app.get('/health', (req, res) => {
  res.json({
    status: 'ok',
    timestamp: new Date().toISOString(),
    uptime: process.uptime()
  });
});

app.get('/health/detailed', async (req, res) => {
  const checks = {
    server: { status: 'ok' },
    database: { status: 'unknown' },
    memory: { status: 'ok' }
  };

  try {
    await db.query('SELECT 1');
    checks.database = { status: 'ok' };
  } catch (err) {
    checks.database = { status: 'error', message: err.message };
  }

  const memoryUsage = process.memoryUsage();
  const heapUsedMB = memoryUsage.heapUsed / 1024 / 1024;
  if (heapUsedMB > 500) {
    checks.memory = { status: 'warning', heapUsedMB };
  }

  const allOk = Object.values(checks).every(c => c.status === 'ok');
  res.status(allOk ? 200 : 503).json({
    status: allOk ? 'healthy' : 'unhealthy',
    checks,
    timestamp: new Date().toISOString()
  });
});

let isReady = false;

app.get('/ready', (req, res) => {
  res.status(isReady ? 200 : 503).json({ status: isReady ? 'ready' : 'not ready' });
});

async function initializeApp() {
  await db.connect();
  isReady = true;
}

initializeApp();
app.listen(3000);
```

---

### Q354: What is APM and how to monitor Node.js applications?

**Answer:**

APM (Application Performance Monitoring) tools track performance metrics like CPU, memory, event loop lag, and request latency.

```js
const os = require('os');

function getMetrics() {
  return {
    cpuLoad: os.loadavg(),
    cpuCount: os.cpus().length,
    memory: {
      total: os.totalmem(),
      free: os.freemem(),
      usagePercent: ((os.totalmem() - os.freemem()) / os.totalmem() * 100).toFixed(2)
    },
    pid: process.pid,
    uptime: process.uptime(),
    memoryUsage: process.memoryUsage()
  };
}

function monitoringMiddleware(req, res, next) {
  const start = process.hrtime.bigint();
  res.on('finish', () => {
    const duration = Number(process.hrtime.bigint() - start) / 1e6;
    console.log(JSON.stringify({
      type: 'request',
      method: req.method,
      path: req.path,
      status: res.statusCode,
      duration: duration.toFixed(2) + 'ms',
      timestamp: new Date().toISOString()
    }));
  });
  next();
}
```

---

### Q355: How do you handle database migrations in Node.js?

**Answer:**

Database migrations version-control schema changes using tools like Knex, Sequelize, TypeORM, or custom runners.

```js
class MigrationRunner {
  constructor(db) {
    this.db = db;
    this.migrations = new Map();
  }

  register(name, up, down) {
    this.migrations.set(name, { up, down });
  }

  async runMigrations() {
    await this.ensureMigrationsTable();
    const executed = await this.getExecutedMigrations();
    const pending = Array.from(this.migrations.keys())
      .filter(m => !executed.includes(m))
      .sort();

    for (const name of pending) {
      console.log('Running migration: ' + name);
      await this.migrations.get(name).up(this.db);
      await this.recordMigration(name);
    }
  }

  async ensureMigrationsTable() {
    await this.db.query(
      'CREATE TABLE IF NOT EXISTS migrations (name VARCHAR(255) PRIMARY KEY, executed_at TIMESTAMP DEFAULT NOW())'
    );
  }

  async getExecutedMigrations() {
    const { rows } = await this.db.query('SELECT name FROM migrations ORDER BY name ASC');
    return rows.map(r => r.name);
  }

  async recordMigration(name) {
    await this.db.query('INSERT INTO migrations (name) VALUES ($1)', [name]);
  }
}

const runner = new MigrationRunner(pool);
runner.register('001_create_users', async (db) => {
  await db.query('CREATE TABLE users (id SERIAL PRIMARY KEY, name VARCHAR(255) NOT NULL, email VARCHAR(255) UNIQUE NOT NULL, created_at TIMESTAMP DEFAULT NOW())');
}, async (db) => {
  await db.query('DROP TABLE IF EXISTS users');
});
```

---

### Q356: What is a child process in Node.js?

**Answer:**

Child processes allow executing system commands and running other programs from Node.js using `child_process` module.

```js
const { spawn, exec, execFile, fork } = require('child_process');

// spawn - streams output
const ls = spawn('ls', ['-la']);
ls.stdout.on('data', (data) => console.log('Output: ' + data));
ls.stderr.on('data', (data) => console.error('Error: ' + data));
ls.on('close', (code) => console.log('Exited with code ' + code));

// exec - buffers output
exec('find . -type f | wc -l', (error, stdout, stderr) => {
  if (error) console.error(error);
  console.log('File count: ' + stdout.trim());
});

// execFile - direct binary execution
execFile('node', ['--version'], (error, stdout) => {
  if (error) throw error;
  console.log('Node version: ' + stdout);
});

// fork - new Node.js process for IPC
const child = fork('worker.js');
child.send({ task: 'compute', data: 42 });
child.on('message', (result) => {
  console.log('Result:', result);
});
```

---

### Q357: What is the stream pipeline and why use it?

**Answer:**

Stream pipeline handles backpressure and error propagation automatically, preventing data loss and memory issues.

```js
const { pipeline } = require('stream');
const fs = require('fs');
const zlib = require('zlib');

pipeline(
  fs.createReadStream('input.txt'),
  zlib.createGzip(),
  fs.createWriteStream('input.txt.gz'),
  (err) => {
    if (err) {
      console.error('Pipeline failed:', err);
    } else {
      console.log('Pipeline succeeded');
    }
  }
);

// Without pipeline (error-prone)
const readStream = fs.createReadStream('input.txt');
const writeStream = fs.createWriteStream('output.txt');
readStream.pipe(writeStream);
// Missing error handling, no backpressure management

// With pipeline (proper)
pipeline(
  readStream,
  writeStream,
  (err) => {
    if (err) console.error('Pipeline failed:', err);
    else console.log('Done');
  }
);
```

---

### Q358: How do you manage application configuration?

**Answer:**

Configuration management uses env vars, config files, hierarchical configs, and validation for different environments.

```js
const convict = require('convict');

const config = convict({
  env: {
    format: ['production', 'development', 'test'],
    default: 'development',
    env: 'NODE_ENV'
  },
  port: {
    format: 'port',
    default: 3000,
    env: 'PORT'
  },
  db: {
    host: { format: String, default: 'localhost', env: 'DB_HOST' },
    port: { format: 'port', default: 5432, env: 'DB_PORT' },
    name: { format: String, default: 'myapp', env: 'DB_NAME' }
  },
  redis: {
    host: { format: String, default: 'localhost', env: 'REDIS_HOST' },
    port: { format: 'port', default: 6379, env: 'REDIS_PORT' }
  }
});

config.validate({ allowed: 'strict' });
module.exports = config;
```

---

### Q359: How do you implement error handling middleware?

**Answer:**

Error handling middleware with 4 parameters catches errors and provides consistent error responses.

```js
class AppError extends Error {
  constructor(message, statusCode) {
    super(message);
    this.statusCode = statusCode;
    this.isOperational = true;
    Error.captureStackTrace(this, this.constructor);
  }
}

class NotFoundError extends AppError {
  constructor(resource) {
    super(resource + ' not found', 404);
  }
}

class ValidationError extends AppError {
  constructor(message) {
    super(message, 400);
  }
}

function errorHandler(err, req, res, next) {
  err.statusCode = err.statusCode || 500;
  err.status = err.status || 'error';

  if (process.env.NODE_ENV === 'development') {
    res.status(err.statusCode).json({
      error: err.message,
      stack: err.stack,
      status: err.status
    });
  } else {
    if (err.isOperational) {
      res.status(err.statusCode).json({
        error: err.message
      });
    } else {
      console.error('Unexpected error:', err);
      res.status(500).json({
        error: 'Internal server error'
      });
    }
  }
}

app.use(errorHandler);

// Usage
app.get('/users/:id', async (req, res, next) => {
  try {
    const user = await db.findUser(req.params.id);
    if (!user) throw new NotFoundError('User');
    res.json(user);
  } catch (err) {
    next(err);
  }
});
```

---

### Q360: How do you test Node.js applications?

**Answer:**

Testing uses Jest, Mocha, or Vitest with unit tests, integration tests, and end-to-end tests.

```js
const jest = require('jest');

// Unit test
describe('UserService', () => {
  let userService;
  let mockRepository;

  beforeEach(() => {
    mockRepository = {
      findAll: jest.fn(),
      findById: jest.fn(),
      create: jest.fn()
    };
    userService = new UserService(mockRepository);
  });

  test('should return all users', async () => {
    const users = [{ id: '1', name: 'Alice' }];
    mockRepository.findAll.mockResolvedValue(users);

    const result = await userService.getAllUsers();

    expect(result).toEqual(users);
    expect(mockRepository.findAll).toHaveBeenCalledTimes(1);
  });

  test('should throw error for invalid email', async () => {
    await expect(userService.createUser({ name: 'Bob', email: 'invalid' }))
      .rejects.toThrow('Invalid email');
  });
});

// Integration test
const supertest = require('supertest');
const app = require('../app');

describe('API Integration Tests', () => {
  test('GET /api/users returns 200', async () => {
    const response = await supertest(app)
      .get('/api/users')
      .expect(200);

    expect(Array.isArray(response.body)).toBe(true);
  });

  test('POST /api/users creates user', async () => {
    const response = await supertest(app)
      .post('/api/users')
      .send({ name: 'Alice', email: 'alice@test.com' })
      .expect(201);

    expect(response.body).toHaveProperty('id');
  });
});
```

---

### Q361: What is Docker and how is it used with Node.js?

**Answer:**

Docker containers package Node.js applications with dependencies for consistent deployment across environments.

```dockerfile
# Dockerfile
FROM node:18-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

FROM node:18-alpine
WORKDIR /app
RUN addgroup -g 1001 -S appgroup && adduser -S appuser -u 1001
COPY --from=builder /app/node_modules ./node_modules
COPY . .
USER appuser
EXPOSE 3000
CMD ["node", "dist/index.js"]

# docker-compose.yml
version: '3.8'
services:
  app:
    build: .
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=production
      - DB_HOST=postgres
    depends_on:
      - postgres
    healthcheck:
      test: ["CMD", "wget", "--spider", "http://localhost:3000/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  postgres:
    image: postgres:15
    environment:
      POSTGRES_DB: myapp
      POSTGRES_PASSWORD: secret
    volumes:
      - pgdata:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine

volumes:
  pgdata:
```

---

### Q362: How do you deploy Node.js applications?

**Answer:**

Deployment involves CI/CD pipelines, process managers, reverse proxies, and cloud platforms like AWS, GCP, or Vercel.

```bash
# CI/CD Pipeline (GitHub Actions)
# .github/workflows/deploy.yml
name: Deploy
on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: 18
      - run: npm ci
      - run: npm test
      - run: npm run build

      - name: Deploy to AWS
        run: |
          aws ecs update-service --cluster my-cluster \
            --service my-service \
            --force-new-deployment

# Deploy steps
# 1. Build: npm run build
# 2. Test: npm test
# 3. Build Docker image: docker build -t myapp .
# 4. Push to registry: docker push registry/myapp:tag
# 5. Deploy: kubectl apply -f k8s/deployment.yaml
# 6. Health check: curl https://app.com/health
```

```js
// Graceful shutdown for deployments
process.on('SIGTERM', async () => {
  console.log('SIGTERM received. Shutting down...');
  server.close(() => {
    console.log('Server closed');
    process.exit(0);
  });
  setTimeout(() => process.exit(1), 10000);
});
```

---

### Q363: What is Kubernetes and how does it orchestrate Node.js containers?

**Answer:**

Kubernetes manages container deployment, scaling, and service discovery for Node.js applications.

```yaml
# k8s/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: node-app
  labels:
    app: node-app
spec:
  replicas: 3
  selector:
    matchLabels:
      app: node-app
  template:
    metadata:
      labels:
        app: node-app
    spec:
      containers:
      - name: app
        image: myapp:latest
        ports:
        - containerPort: 3000
        env:
        - name: NODE_ENV
          value: "production"
        - name: DB_HOST
          valueFrom:
            configMapKeyRef:
              name: app-config
              key: db_host
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /live
            port: 3000
          initialDelaySeconds: 10
          periodSeconds: 5
        readinessProbe:
          httpGet:
            path: /ready
            port: 3000
          initialDelaySeconds: 5
          periodSeconds: 5
---
# k8s/service.yaml
apiVersion: v1
kind: Service
metadata:
  name: node-app-service
spec:
  selector:
    app: node-app
  ports:
  - port: 80
    targetPort: 3000
  type: LoadBalancer
---
# k8s/hpa.yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: node-app-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: node-app
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
```

---

### Q364: How do you implement serverless functions in Node.js?

**Answer:**

Serverless functions (AWS Lambda, Vercel Functions, Netlify Functions) run stateless, event-driven code without managing servers.

```js
// AWS Lambda handler
exports.handler = async (event, context) => {
  console.log('Event:', JSON.stringify(event, null, 2));

  try {
    const { userId } = event.pathParameters;
    const user = await db.getUser(userId);

    return {
      statusCode: 200,
      headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*'
      },
      body: JSON.stringify(user)
    };
  } catch (err) {
    return {
      statusCode: 500,
      body: JSON.stringify({ error: err.message })
    };
  }
};

// Vercel serverless function
// api/users.js
export default async function handler(req, res) {
  if (req.method === 'GET') {
    const users = await db.getUsers();
    res.json(users);
  } else if (req.method === 'POST') {
    const user = await db.createUser(req.body);
    res.status(201).json(user);
  } else {
    res.status(405).json({ error: 'Method not allowed' });
  }
}

// Netlify function
// netlify/functions/hello.js
exports.handler = async (event) => {
  return {
    statusCode: 200,
    body: JSON.stringify({ message: 'Hello from Netlify!' })
  };
};
```

---

### Q365: How do you handle database connection pooling?

**Answer:**

Connection pooling reuses database connections to reduce overhead and manage concurrent access.

```js
const { Pool } = require('pg');

const pool = new Pool({
  host: 'localhost',
  port: 5432,
  database: 'myapp',
  user: 'user',
  password: 'password',
  max: 20,
  idleTimeoutMillis: 30000,
  connectionTimeoutMillis: 2000,
  maxUses: 7500,
  allowExitOnIdle: false
});

pool.on('error', (err, client) => {
  console.error('Unexpected error on idle client', err);
});

pool.on('acquire', (client) => {
  console.log('Client acquired. Pool total: ' + pool.totalCount + ', idle: ' + pool.idleCount);
});

async function query(text, params) {
  const start = Date.now();
  const result = await pool.query(text, params);
  const duration = Date.now() - start;
  console.log('Executed query - duration: ' + duration + 'ms, rows: ' + result.rowCount);
  return result;
}

async function getTotalConnections() {
  return {
    total: pool.totalCount,
    idle: pool.idleCount,
    waiting: pool.waitingCount
  };
}

process.on('SIGTERM', async () => {
  await pool.end();
});
```

---

### Q366: How do you implement message queues in Node.js?

**Answer:**

Message queues (RabbitMQ, Bull, SQS) enable async processing and decouple service communication.

```js
const Bull = require('bull');

const emailQueue = new Bull('email', {
  redis: { host: 'localhost', port: 6379 }
});

// Job producer
app.post('/api/register', async (req, res) => {
  const user = await createUser(req.body);

  await emailQueue.add({
    type: 'welcome',
    to: user.email,
    name: user.name
  }, {
    attempts: 3,
    backoff: { type: 'exponential', delay: 2000 },
    removeOnComplete: true
  });

  res.status(201).json(user);
});

// Job consumer
emailQueue.process(async (job) => {
  const { type, to, name } = job.data;

  switch (type) {
    case 'welcome':
      console.log('Sending welcome email to ' + to);
      await sendEmail(to, 'Welcome!', 'Hello ' + name + '!');
      break;
    case 'reset':
      console.log('Sending password reset to ' + to);
      break;
  }
});

// Event handlers
emailQueue.on('completed', (job, result) => {
  console.log('Job ' + job.id + ' completed');
});

emailQueue.on('failed', (job, err) => {
  console.error('Job ' + job.id + ' failed:', err.message);
});

emailQueue.on('stalled', (job) => {
  console.log('Job ' + job.id + ' stalled');
});

// Cleanup
setInterval(async () => {
  await emailQueue.clean(5000, 'completed');
  await emailQueue.clean(5000, 'failed');
}, 10000);
```

---

### Q367: How do you handle graceful shutdown in Node.js?

**Answer:**

Graceful shutdown stops accepting new requests, finishes in-flight requests, closes connections, and exits cleanly.

```js
const express = require('express');
const app = express();

let server;

async function gracefulShutdown(signal) {
  console.log(signal + ' received. Starting graceful shutdown...');

  // Stop accepting new requests
  server.close(() => {
    console.log('HTTP server closed');
  });

  // Force shutdown after timeout
  const forceShutdown = setTimeout(() => {
    console.error('Forced shutdown');
    process.exit(1);
  }, 30000);

  try {
    // Close database connections
    await pool.end();
    console.log('Database pool closed');

    // Close Redis
    await redisClient.quit();
    console.log('Redis disconnected');

    // Close message queue
    await emailQueue.close();
    console.log('Queue closed');

    clearTimeout(forceShutdown);
    console.log('Graceful shutdown complete');
    process.exit(0);
  } catch (err) {
    console.error('Error during shutdown:', err);
    process.exit(1);
  }
}

process.on('SIGTERM', () => gracefulShutdown('SIGTERM'));
process.on('SIGINT', () => gracefulShutdown('SIGINT'));

// Health endpoint for load balancer
app.get('/health', (req, res) => {
  res.json({ status: 'ok', shuttingDown: false });
});

server = app.listen(3000, () => {
  console.log('Server running on port 3000');
});
```

---

### Q368: What are event-driven architecture patterns in Node.js?

**Answer:**

Event-driven architecture uses events for communication between decoupled components via EventEmitter or message brokers.

```js
// Domain events
class DomainEvents {
  constructor() {
    this.handlers = new Map();
  }

  register(eventName, handler) {
    if (!this.handlers.has(eventName)) {
      this.handlers.set(eventName, []);
    }
    this.handlers.get(eventName).push(handler);
  }

  async dispatch(eventName, data) {
    const handlers = this.handlers.get(eventName) || [];
    const results = await Promise.allSettled(
      handlers.map(handler => handler(data))
    );
    results.forEach((result, i) => {
      if (result.status === 'rejected') {
        console.error('Handler ' + i + ' failed:', result.reason);
      }
    });
  }

  remove(eventName, handler) {
    const handlers = this.handlers.get(eventName);
    if (handlers) {
      const index = handlers.indexOf(handler);
      if (index > -1) handlers.splice(index, 1);
    }
  }
}

const domainEvents = new DomainEvents();

// Register handlers
domainEvents.register('UserRegistered', async (event) => {
  await emailService.sendWelcome(event.user.email);
});

domainEvents.register('UserRegistered', async (event) => {
  await analyticsService.track('user.registered', event.user);
});

// Usage
async function registerUser(data) {
  const user = await db.users.create(data);
  await domainEvents.dispatch('UserRegistered', { user });
  return user;
}
```

---

### Q369: How do you implement feature flags in Node.js?

**Answer:**

Feature flags toggle functionality on/off without deployment, enabling canary releases and A/B testing.

```js
class FeatureFlags {
  constructor() {
    this.flags = new Map();
    this.defaults = {};
  }

  async load() {
    // Load from database or config file
    this.flags.set('new-checkout', true);
    this.flags.set('dark-mode', false);
    this.flags.set('beta-features', process.env.NODE_ENV === 'development');
  }

  isEnabled(flag, user = null) {
    const value = this.flags.get(flag);
    if (value === undefined) return this.defaults[flag] || false;
    if (typeof value === 'function') return value(user);
    return value;
  }

  enable(flag) { this.flags.set(flag, true); }
  disable(flag) { this.flags.set(flag, false); }

  // Percentage rollout
  enableForPercent(flag, percent) {
    this.flags.set(flag, (user) => {
      const hash = this.hashCode(user.id) % 100;
      return hash < percent;
    });
  }

  hashCode(str) {
    let hash = 0;
    for (let i = 0; i < str.length; i++) {
      hash = ((hash << 5) - hash) + str.charCodeAt(i);
      hash |= 0;
    }
    return Math.abs(hash);
  }
}

const features = new FeatureFlags();
await features.load();

// Usage in routes
app.get('/checkout', (req, res) => {
  if (features.isEnabled('new-checkout', req.user)) {
    res.render('new-checkout');
  } else {
    res.render('old-checkout');
  }
});

app.get('/api/features', (req, res) => {
  res.json({
    newCheckout: features.isEnabled('new-checkout', req.user),
    darkMode: features.isEnabled('dark-mode', req.user)
  });
});
```

---

### Q370: How do you implement API versioning in Node.js?

**Answer:**

API versioning maintains backward compatibility using URL prefixes, headers, or query parameters.

```js
const express = require('express');
const app = express();

// URL-based versioning
const v1Router = express.Router();
const v2Router = express.Router();

// v1 API
v1Router.get('/users', (req, res) => {
  res.json([{ id: 1, name: 'Alice', email: 'alice@test.com' }]);
});

v1Router.get('/users/:id', (req, res) => {
  res.json({ id: req.params.id, name: 'Alice' });
});

// v2 API (new fields)
v2Router.get('/users', (req, res) => {
  res.json([{
    id: 1,
    name: 'Alice',
    email: 'alice@test.com',
    profile: { avatar: 'url', bio: 'Developer' },
    createdAt: '2024-01-01'
  }]);
});

v2Router.get('/users/:id', (req, res) => {
  res.json({
    id: req.params.id,
    name: 'Alice',
    profile: { avatar: 'url' }
  });
});

app.use('/api/v1', v1Router);
app.use('/api/v2', v2Router);

// Header-based versioning
app.use('/api', (req, res, next) => {
  const version = req.headers['accept-version'] || '1';
  req.apiVersion = version;
  next();
});

app.get('/api/users', (req, res) => {
  if (req.apiVersion === '2') {
    return v2Router.handle(req, res);
  }
  return v1Router.handle(req, res);
});

// Content negotiation
app.get('/api/users', (req, res) => {
  const accept = req.headers['accept'];
  if (accept === 'application/vnd.myapp.v2+json') {
    // return v2 response
  }
  // return v1 response
});
```

---

### Q371: How do you implement retry logic in Node.js?

**Answer:**

Retry logic handles transient failures with exponential backoff, jitter, and configurable retry counts.

```js
async function retry(fn, options = {}) {
  const {
    maxRetries = 3,
    baseDelay = 100,
    maxDelay = 10000,
    factor = 2,
    jitter = true
  } = options;

  let lastError;

  for (let attempt = 0; attempt <= maxRetries; attempt++) {
    try {
      return await fn(attempt);
    } catch (err) {
      lastError = err;

      if (attempt === maxRetries) {
        throw err;
      }

      // Calculate delay with exponential backoff
      let delay = Math.min(
        baseDelay * Math.pow(factor, attempt),
        maxDelay
      );

      // Add jitter
      if (jitter) {
        delay = delay * (0.5 + Math.random() * 0.5);
      }

      console.log('Attempt ' + (attempt + 1) + ' failed. Retrying in ' + Math.round(delay) + 'ms...');

      await new Promise(resolve => setTimeout(resolve, delay));
    }
  }
}

// Usage
async function fetchWithRetry(url) {
  return retry(async (attempt) => {
    console.log('Fetch attempt ' + (attempt + 1));
    const response = await fetch(url);
    if (!response.ok) throw new Error('HTTP ' + response.status);
    return response.json();
  }, {
    maxRetries: 5,
    baseDelay: 200,
    factor: 3,
    jitter: true
  });
}

// Retry with circuit breaker
class RetryWithCircuitBreaker {
  constructor(fn, options = {}) {
    this.fn = fn;
    this.maxRetries = options.maxRetries || 3;
    this.failures = 0;
    this.threshold = options.threshold || 5;
    this.state = 'CLOSED';
  }

  async call(...args) {
    if (this.state === 'OPEN') {
      throw new Error('Circuit breaker open');
    }

    for (let i = 0; i <= this.maxRetries; i++) {
      try {
        const result = await this.fn(...args);
        this.failures = 0;
        this.state = 'CLOSED';
        return result;
      } catch (err) {
        this.failures++;
        if (this.failures >= this.threshold) {
          this.state = 'OPEN';
          setTimeout(() => { this.state = 'HALF_OPEN'; }, 30000);
        }
        if (i === this.maxRetries) throw err;
      }
    }
  }
}
```

---

### Q372: What is the Saga pattern for distributed transactions?

**Answer:**

The Saga pattern manages distributed transactions across services using compensating actions on failure.

```js
class Saga {
  constructor() {
    this.steps = [];
    this.compensationStack = [];
  }

  step(name, execute, compensate) {
    this.steps.push({ name, execute, compensate });
    return this;
  }

  async execute(context = {}) {
    console.log('Starting saga...');

    for (const step of this.steps) {
      try {
        console.log('Executing step: ' + step.name);
        const result = await step.execute(context);
        context[step.name] = result;
        this.compensationStack.push(step);
      } catch (err) {
        console.error('Step ' + step.name + ' failed:', err.message);
        console.log('Starting compensation...');
        await this.compensate();
        throw new Error('Saga failed at step: ' + step.name);
      }
    }

    console.log('Saga completed successfully');
    return context;
  }

  async compensate() {
    while (this.compensationStack.length > 0) {
      const step = this.compensationStack.pop();
      try {
        console.log('Compensating step: ' + step.name);
        await step.compensate();
      } catch (err) {
        console.error('Compensation failed for ' + step.name + ':', err);
      }
    }
  }
}

// Order creation saga
const orderSaga = new Saga();

orderSaga
  .step(
    'createOrder',
    async (ctx) => {
      ctx.order = await db.createOrder(ctx.orderData);
      return ctx.order;
    },
    async (ctx) => {
      await db.deleteOrder(ctx.order.id);
    }
  )
  .step(
    'reserveInventory',
    async (ctx) => {
      ctx.inventory = await inventoryService.reserve(ctx.order.items);
      return ctx.inventory;
    },
    async (ctx) => {
      await inventoryService.release(ctx.inventory.reservationId);
    }
  )
  .step(
    'chargePayment',
    async (ctx) => {
      ctx.payment = await paymentService.charge(ctx.order.total, ctx.userId);
      return ctx.payment;
    },
    async (ctx) => {
      await paymentService.refund(ctx.payment.transactionId);
    }
  );

// Usage
try {
  const result = await orderSaga.execute({
    userId: 123,
    orderData: { items: ['item1', 'item2'], total: 100 }
  });
  console.log('Order created:', result.order.id);
} catch (err) {
  console.error('Order creation failed:', err.message);
}
```

---

### Q373: How do you implement request validation in Node.js?

**Answer:**

Request validation ensures incoming data meets expected format using Joi, Zod, or express-validator.

```js
const Joi = require('joi');

const schemas = {
  createUser: Joi.object({
    name: Joi.string().min(2).max(100).required(),
    email: Joi.string().email().required(),
    age: Joi.number().integer().min(18).max(150),
    role: Joi.string().valid('user', 'admin').default('user')
  }),

  updateUser: Joi.object({
    name: Joi.string().min(2).max(100),
    email: Joi.string().email(),
    age: Joi.number().integer().min(18).max(150)
  }).min(1),

  queryParams: Joi.object({
    page: Joi.number().integer().min(1).default(1),
    limit: Joi.number().integer().min(1).max(100).default(20),
    sort: Joi.string().valid('name', 'email', 'createdAt').default('createdAt'),
    order: Joi.string().valid('asc', 'desc').default('desc')
  })
};

function validate(schema, source = 'body') {
  return (req, res, next) => {
    const { error, value } = schema.validate(req[source], {
      abortEarly: false,
      stripUnknown: true
    });

    if (error) {
      const messages = error.details.map(d => ({
        field: d.path.join('.'),
        message: d.message
      }));
      return res.status(400).json({ errors: messages });
    }

    req[source] = value;
    next();
  };
}

// Usage
app.post('/api/users', validate(schemas.createUser), async (req, res) => {
  const user = await db.createUser(req.body);
  res.status(201).json(user);
});

app.put('/api/users/:id', validate(schemas.updateUser), async (req, res) => {
  const user = await db.updateUser(req.params.id, req.body);
  res.json(user);
});

app.get('/api/users', validate(schemas.queryParams, 'query'), async (req, res) => {
  const users = await db.findUsers(req.query);
  res.json(users);
});
```

---

### Q374: How do you implement pagination in REST APIs?

**Answer:**

Pagination breaks large result sets into pages using cursor-based or offset-based approaches.

```js
// Offset-based pagination
async function getUsers(page = 1, limit = 20) {
  const offset = (page - 1) * limit;
  const [users, total] = await Promise.all([
    db.query('SELECT * FROM users ORDER BY id DESC LIMIT $1 OFFSET $2', [limit, offset]),
    db.query('SELECT COUNT(*) FROM users')
  ]);

  return {
    data: users.rows,
    pagination: {
      page,
      limit,
      total: parseInt(total.rows[0].count),
      totalPages: Math.ceil(total.rows[0].count / limit),
      hasNext: page * limit < total.rows[0].count,
      hasPrev: page > 1
    }
  };
}

// Cursor-based pagination
async function getUsersCursor(cursor, limit = 20) {
  let query;
  let params;

  if (cursor) {
    query = 'SELECT * FROM users WHERE id < $1 ORDER BY id DESC LIMIT $2';
    params = [cursor, limit];
  } else {
    query = 'SELECT * FROM users ORDER BY id DESC LIMIT $1';
    params = [limit];
  }

  const result = await db.query(query, params);
  const users = result.rows;

  return {
    data: users,
    pagination: {
      cursor: users.length > 0 ? users[users.length - 1].id : null,
      hasMore: users.length === limit,
      limit
    }
  };
}

// Express pagination middleware
function paginate(req, res, next) {
  let page = parseInt(req.query.page) || 1;
  let limit = parseInt(req.query.limit) || 20;

  page = Math.max(1, page);
  limit = Math.min(100, Math.max(1, limit));

  req.pagination = { page, limit, offset: (page - 1) * limit };
  next();
}

app.get('/api/users', paginate, async (req, res) => {
  const result = await getUsers(req.pagination.page, req.pagination.limit);
  res.json(result);
});
```

---

### Q375: How do you implement logging correlation IDs?

**Answer:**

Correlation IDs trace requests across services and log entries for debugging distributed systems.

```js
const { AsyncLocalStorage } = require('async_hooks');
const { randomUUID } = require('crypto');

const asyncLocalStorage = new AsyncLocalStorage();

function correlationIdMiddleware(req, res, next) {
  const correlationId = req.headers['x-correlation-id'] || randomUUID();
  const store = { correlationId, startTime: Date.now() };
  asyncLocalStorage.run(store, () => {
    res.setHeader('x-correlation-id', correlationId);
    next();
  });
}

function getCorrelationId() {
  const store = asyncLocalStorage.getStore();
  return store?.correlationId;
}

class CorrelatedLogger {
  constructor() {
    this.levels = ['debug', 'info', 'warn', 'error'];
  }

  _log(level, message, meta = {}) {
    const correlationId = getCorrelationId();
    const entry = {
      level,
      message,
      correlationId,
      timestamp: new Date().toISOString(),
      service: process.env.SERVICE_NAME || 'unknown',
      ...meta
    };
    if (level === 'error') {
      console.error(JSON.stringify(entry));
    } else {
      console.log(JSON.stringify(entry));
    }
  }

  debug(msg, meta) { this._log('debug', msg, meta); }
  info(msg, meta) { this._log('info', msg, meta); }
  warn(msg, meta) { this._log('warn', msg, meta); }
  error(msg, meta) { this._log('error', msg, meta); }
}

const logger = new CorrelatedLogger();

// Usage
app.use(correlationIdMiddleware);

app.get('/api/users', async (req, res) => {
  logger.info('Fetching users', { query: req.query });
  try {
    const users = await db.getUsers();
    logger.info('Users fetched', { count: users.length });
    res.json(users);
  } catch (err) {
    logger.error('Failed to fetch users', { error: err.message });
    res.status(500).json({ error: 'Internal error' });
  }
});
```

---

### Q376: How do you implement soft deletes?

**Answer:**

Soft deletes mark records as deleted without removing them, using a `deleted_at` timestamp or `is_deleted` flag.

```js
// Schema
// ALTER TABLE users ADD COLUMN deleted_at TIMESTAMP DEFAULT NULL;
// CREATE INDEX idx_users_deleted_at ON users(deleted_at);

class SoftDeleteRepository {
  constructor(db, tableName) {
    this.db = db;
    this.tableName = tableName;
  }

  async findAll(includeDeleted = false) {
    let query;
    if (includeDeleted) {
      query = 'SELECT * FROM ' + this.tableName + ' ORDER BY id DESC';
    } else {
      query = 'SELECT * FROM ' + this.tableName + ' WHERE deleted_at IS NULL ORDER BY id DESC';
    }
    const { rows } = await this.db.query(query);
    return rows;
  }

  async findById(id, includeDeleted = false) {
    let query;
    if (includeDeleted) {
      query = 'SELECT * FROM ' + this.tableName + ' WHERE id = $1';
    } else {
      query = 'SELECT * FROM ' + this.tableName + ' WHERE id = $1 AND deleted_at IS NULL';
    }
    const { rows } = await this.db.query(query, [id]);
    return rows[0] || null;
  }

  async softDelete(id) {
    const { rows } = await this.db.query(
      'UPDATE ' + this.tableName + ' SET deleted_at = NOW() WHERE id = $1 AND deleted_at IS NULL RETURNING *',
      [id]
    );
    return rows[0] || null;
  }

  async restore(id) {
    const { rows } = await this.db.query(
      'UPDATE ' + this.tableName + ' SET deleted_at = NULL WHERE id = $1 RETURNING *',
      [id]
    );
    return rows[0] || null;
  }

  async hardDelete(id) {
    const { rowCount } = await this.db.query(
      'DELETE FROM ' + this.tableName + ' WHERE id = $1',
      [id]
    );
    return rowCount > 0;
  }
}

// Route handlers
app.delete('/api/users/:id', async (req, res) => {
  const user = await userRepo.softDelete(req.params.id);
  if (!user) return res.status(404).json({ error: 'User not found' });
  res.json({ message: 'User deleted' });
});

app.post('/api/users/:id/restore', async (req, res) => {
  const user = await userRepo.restore(req.params.id);
  if (!user) return res.status(404).json({ error: 'User not found' });
  res.json(user);
});
```

---

### Q377: How do you implement audit logging?

**Answer:**

Audit logging records who did what and when for compliance and debugging.

```js
class AuditLogger {
  constructor(db) {
    this.db = db;
  }

  async log(action, entityType, entityId, userId, changes = {}, metadata = {}) {
    const entry = {
      action,
      entity_type: entityType,
      entity_id: entityId,
      user_id: userId,
      changes: JSON.stringify(changes),
      metadata: JSON.stringify(metadata),
      ip_address: metadata.ip,
      user_agent: metadata.userAgent,
      timestamp: new Date().toISOString()
    };

    await this.db.query(
      'INSERT INTO audit_logs (action, entity_type, entity_id, user_id, changes, metadata, ip_address, user_agent) VALUES ($1, $2, $3, $4, $5, $6, $7, $8)',
      [entry.action, entry.entity_type, entry.entity_id, entry.user_id, entry.changes, entry.metadata, entry.ip_address, entry.user_agent]
    );
  }

  async getEntityHistory(entityType, entityId) {
    const { rows } = await this.db.query(
      'SELECT * FROM audit_logs WHERE entity_type = $1 AND entity_id = $2 ORDER BY timestamp DESC LIMIT 100',
      [entityType, entityId]
    );
    return rows.map(r => ({
      ...r,
      changes: JSON.parse(r.changes),
      metadata: JSON.parse(r.metadata)
    }));
  }
}

// Middleware for automatic audit logging
function auditMiddleware(entityType) {
  return async (req, res, next) => {
    const originalJson = res.json.bind(res);
    res.json = async function(body) {
      if (res.statusCode >= 200 && res.statusCode < 300) {
        const changes = {};
        if (req.method === 'POST') changes.created = body;
        if (req.method === 'PUT') changes.updated = req.body;
        if (req.method === 'DELETE') changes.deleted = { id: req.params.id };

        await auditLogger.log(
          req.method.toLowerCase(),
          entityType,
          body?.id || req.params.id,
          req.user?.id,
          changes,
          { ip: req.ip, userAgent: req.headers['user-agent'] }
        );
      }
      return originalJson(body);
    };
    next();
  };
}

app.post('/api/users', auditMiddleware('user'), async (req, res) => {
  const user = await db.createUser(req.body);
  res.status(201).json(user);
});
```

---

### Q378: How do you implement background jobs in Node.js?

**Answer:**

Background jobs handle time-consuming tasks asynchronously using job queues, worker threads, or child processes.

```js
const Bull = require('bull');

// Job queue
const jobQueue = new Bull('background-jobs', {
  redis: { host: 'localhost', port: 6379 },
  defaultJobOptions: {
    attempts: 3,
    backoff: { type: 'exponential', delay: 1000 },
    removeOnComplete: 100,
    removeOnFail: 50
  }
});

// Producer
class JobProducer {
  async sendEmail(payload) {
    return jobQueue.add('send-email', payload, {
      priority: 1,
      delay: 0
    });
  }

  async generateReport(payload) {
    return jobQueue.add('generate-report', payload, {
      priority: 3,
      delay: 5000 // delay 5 seconds
    });
  }

  async processImage(payload) {
    return jobQueue.add('process-image', payload, {
      attempts: 5,
      backoff: { type: 'fixed', delay: 5000 }
    });
  }
}

// Consumer
jobQueue.process('send-email', async (job) => {
  const { to, subject, body } = job.data;
  console.log('Sending email to ' + to + ': ' + subject);
  await transporter.sendMail({ to, subject, html: body });
});

jobQueue.process('generate-report', async (job) => {
  const { userId, reportType } = job.data;
  console.log('Generating ' + reportType + ' report for user ' + userId);
  const report = await generateReport(userId, reportType);
  await storeReport(userId, report);
});

jobQueue.process('process-image', async (job) => {
  const { imagePath, operations } = job.data;
  console.log('Processing image: ' + imagePath);
  await sharp(imagePath).resize(800, 600).toFile(imagePath + '_processed.jpg');
});

// Job events
jobQueue.on('completed', (job, result) => {
  console.log('Job ' + job.id + ' completed');
});

jobQueue.on('failed', (job, err) => {
  console.error('Job ' + job.id + ' failed: ' + err.message);
});

jobQueue.on('stalled', (job) => {
  console.warn('Job ' + job.id + ' stalled');
});

// Periodic/scheduled jobs
jobQueue.add('cleanup', {}, { repeat: { cron: '0 0 * * 0' } }); // weekly
jobQueue.add('send-digest', {}, { repeat: { every: 24 * 60 * 60 * 1000 } }); // daily

// Graceful shutdown
process.on('SIGTERM', async () => {
  await jobQueue.close();
});
```

---

### Q379: How do you implement Webhook handling?

**Answer:**

Webhooks send HTTP callbacks to registered URLs when events occur, with retry logic and signature verification.

```js
const crypto = require('crypto');
const express = require('express');
const app = express();

app.use(express.json());

// Webhook sender
class WebhookSender {
  constructor() {
    this.secret = process.env.WEBHOOK_SECRET || 'default-secret';
  }

  createSignature(payload) {
    const hmac = crypto.createHmac('sha256', this.secret);
    hmac.update(JSON.stringify(payload));
    return 'sha256=' + hmac.digest('hex');
  }

  async send(url, event, payload) {
    const body = { event, payload, timestamp: Date.now() };
    const signature = this.createSignature(body);

    try {
      const response = await fetch(url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-Webhook-Signature': signature,
          'X-Webhook-Event': event
        },
        body: JSON.stringify(body)
      });

      if (!response.ok) {
        throw new Error('Webhook failed with status ' + response.status);
      }

      return { success: true, status: response.status };
    } catch (err) {
      console.error('Webhook delivery failed:', err.message);
      throw err;
    }
  }

  async sendWithRetry(url, event, payload, maxRetries = 3) {
    for (let i = 0; i < maxRetries; i++) {
      try {
        return await this.send(url, event, payload);
      } catch (err) {
        if (i === maxRetries - 1) throw err;
        await new Promise(r => setTimeout(r, 1000 * Math.pow(2, i)));
      }
    }
  }
}

// Webhook receiver
function verifyWebhookSignature(req, res, next) {
  const signature = req.headers['x-webhook-signature'];
  const event = req.headers['x-webhook-event'];

  if (!signature || !event) {
    return res.status(400).json({ error: 'Missing headers' });
  }

  const hmac = crypto.createHmac('sha256', process.env.WEBHOOK_SECRET);
  hmac.update(JSON.stringify(req.body));
  const expected = 'sha256=' + hmac.digest('hex');

  if (!crypto.timingSafeEqual(Buffer.from(signature), Buffer.from(expected))) {
    return res.status(401).json({ error: 'Invalid signature' });
  }

  req.webhookEvent = event;
  next();
}

app.post('/webhooks', verifyWebhookSignature, async (req, res) => {
  console.log('Received webhook event:', req.webhookEvent);
  console.log('Payload:', req.body);

  // Acknowledge immediately
  res.status(200).json({ received: true });

  // Process asynchronously
  setImmediate(async () => {
    await processWebhook(req.webhookEvent, req.body);
  });
});
```

---

### Q380: How do you implement API rate limiting with Redis?

**Answer:**

Distributed rate limiting uses Redis to track request counts across multiple server instances.

```js
const redis = require('redis');
const client = redis.createClient();

async function checkRateLimit(key, maxRequests, windowSeconds) {
  const current = await client.incr(key);

  if (current === 1) {
    await client.expire(key, windowSeconds);
  }

  const ttl = await client.ttl(key);

  return {
    allowed: current <= maxRequests,
    current,
    limit: maxRequests,
    remaining: Math.max(0, maxRequests - current),
    resetAfter: ttl
  };
}

function rateLimiter(maxRequests, windowSeconds) {
  return async (req, res, next) => {
    const key = 'ratelimit:' + req.ip + ':' + req.path;
    const result = await checkRateLimit(key, maxRequests, windowSeconds);

    res.setHeader('X-RateLimit-Limit', result.limit);
    res.setHeader('X-RateLimit-Remaining', result.remaining);
    res.setHeader('X-RateLimit-Reset', result.resetAfter);

    if (!result.allowed) {
      return res.status(429).json({
        error: 'Too many requests',
        retryAfter: result.resetAfter
      });
    }

    next();
  };
}

// Sliding window with sorted sets
async function slidingWindowRateLimit(userId, maxRequests, windowMs) {
  const key = 'ratelimit:sliding:' + userId;
  const now = Date.now();
  const windowStart = now - windowMs;

  await client.zRemRangeByScore(key, 0, windowStart);
  const count = await client.zCard(key);

  if (count >= maxRequests) {
    return false;
  }

  await client.zAdd(key, { score: now, value: now.toString() });
  await client.expire(key, Math.ceil(windowMs / 1000));
  return true;
}

// Usage
app.use('/api', rateLimiter(100, 60));

app.post('/api/login', rateLimiter(5, 60), async (req, res) => {
  // 5 login attempts per minute
  await loginUser(req.body);
  res.json({ success: true });
});
```

---

## Phase 8: Tricky / Output Based Questions — Q381–Q400

---

### Q381: What is the output?

```js
console.log(1);
setTimeout(() => console.log(2), 0);
Promise.resolve().then(() => console.log(3));
console.log(4);
```

**Answer:**

```
1
4
3
2
```

Explanation: Synchronous code runs first (1, 4). Microtasks (Promise.then) run before macrotasks (setTimeout). So 3 logs before 2.

---

### Q382: What is the output?

```js
for (var i = 0; i < 3; i++) {
  setTimeout(() => console.log(i), 100);
}
```

**Answer:**

```
3
3
3
```

Explanation: `var` is function-scoped, not block-scoped. By the time the setTimeout callbacks execute, the loop has finished and `i` is 3. Using `let` instead of `var` would output 0, 1, 2.

---

### Q383: What is the output?

```js
console.log(typeof null);
console.log(typeof undefined);
console.log(typeof []);
console.log(typeof {});
console.log(typeof NaN);
```

**Answer:**

```
object
undefined
object
object
number
```

Explanation: `typeof null` returns `"object"` (a known JS bug). `NaN` is of type `"number"`. Arrays are objects.

---

### Q384: What is the output?

```js
console.log(0.1 + 0.2 === 0.3);
console.log(0.1 + 0.2);
```

**Answer:**

```
false
0.30000000000000004
```

Explanation: Floating-point precision causes 0.1 + 0.2 to be slightly more than 0.3. Use `Number.EPSILON` for comparison.

---

### Q385: What is the output?

```js
const x = { a: 1 };
const y = { a: 1 };
const z = x;
console.log(x === y);
console.log(x === z);
```

**Answer:**

```
false
true
```

Explanation: Objects are compared by reference. `x` and `y` are different objects with same properties, so not equal. `z` references the same object as `x`.

---

### Q386: What is the output?

```js
console.log(1 + '2' + '2');
console.log(1 + +'2' + '2');
console.log(1 + -'1' + '2');
console.log('A' - 'B' + '2');
console.log('A' - 'B' + 2);
```

**Answer:**

```
122
32
02
NaN2
NaN
```

Explanation: `+` with string causes concatenation. Unary `+` converts string to number. `'A' - 'B'` is `NaN` because subtraction forces numeric conversion.

---

### Q387: What is the output?

```js
console.log([] + []);
console.log([] + {});
console.log({} + []);
console.log({} + {});
```

**Answer:**

```
""
[object Object]
[object Object]
[object Object][object Object]
```

Explanation: The `+` operator converts both operands to primitives. Arrays become empty strings, objects become `[object Object]`.

---

### Q388: What is the output?

```js
function foo() {
  return
  {
    bar: 'baz'
  };
}
console.log(foo());
```

**Answer:**

```
undefined
```

Explanation: Automatic semicolon insertion (ASI) puts a semicolon after `return`, so the function returns `undefined`. The object literal is unreachable code.

---

### Q389: What is the output?

```js
console.log(1);
const promise = new Promise((resolve) => {
  console.log(2);
  resolve(3);
});
promise.then((val) => console.log(val));
console.log(4);
```

**Answer:**

```
1
2
4
3
```

Explanation: The Promise executor runs synchronously (logs 2), but `.then()` callback is a microtask (logs 3 after synchronous code).

---

### Q390: What is the output?

```js
async function test() {
  console.log('A');
  await Promise.resolve();
  console.log('B');
}
test();
console.log('C');
```

**Answer:**

```
A
C
B
```

Explanation: `await` yields control, so `C` logs before `B`. The rest after `await` is queued as a microtask.

---

### Q391: What is the output?

```js
const obj = {
  a: 1,
  b: function() { return this.a; },
  c: () => this.a
};
console.log(obj.b());
console.log(obj.c());
```

**Answer:**

```
1
undefined
```

Explanation: Regular function `b()` has `this` bound to `obj`. Arrow function `c()` captures `this` from enclosing scope (global/module), where `a` is undefined.

---

### Q392: What is the output?

```js
console.log([] == ![]);
console.log([] == 0);
console.log('' == 0);
console.log(null == undefined);
console.log(null === undefined);
```

**Answer:**

```
true
true
true
true
false
```

Explanation: Abstract equality (`==`) performs type coercion. `![]` is `false`, `[]` coerces to `0`, so `0 == false` is `true`. `'' == 0` is `true`. `null == undefined` is `true` but `null === undefined` is `false`.

---

### Q393: What is the output?

```js
let a = 3;
let b = new Number(3);
let c = 3;
console.log(a == b);
console.log(a === b);
console.log(b === c);
```

**Answer:**

```
true
false
false
```

Explanation: `==` coerces `b` to primitive (3). `===` compares type: `number` vs `object` (Number wrapper), so false.

---

### Q394: What is the output?

```js
console.log('hello' instanceof String);
const str = new String('hello');
console.log(str instanceof String);
console.log(str === 'hello');
console.log(str == 'hello');
```

**Answer:**

```
false
true
false
true
```

Explanation: Primitive strings are not instances of String. Only `new String()` creates an object. `===` compares type (object vs primitive), `==` coerces.

---

### Q395: What is the output?

```js
const arr = [1, 2, 3];
arr[10] = 99;
console.log(arr.length);
console.log(arr[5]);
console.log(arr);
```

**Answer:**

```
11
undefined
[1, 2, 3, empty x7, 99]
```

Explanation: Setting index 10 extends the array length to 11. Indices 3-9 are empty slots (not undefined, they don't exist).

---

### Q396: What is the output?

```js
const obj = { x: 1 };
Object.defineProperty(obj, 'y', {
  value: 2,
  writable: false,
  enumerable: false,
  configurable: false
});
console.log(obj.y);
obj.y = 3;
console.log(obj.y);
console.log(Object.keys(obj));
```

**Answer:**

```
2
2
['x']
```

Explanation: `writable: false` prevents assignment. `enumerable: false` hides from `Object.keys()`.

---

### Q397: What is the output?

```js
function test() {
  console.log(this);
}
const obj = { test };
test();
obj.test();
const bound = test.bind({ name: 'bound' });
bound();
```

**Answer:**

Depends on context (global in Node, window in browser), but:
- `test()`: global object (or undefined in strict mode)
- `obj.test()`: `obj`
- `bound()`: `{ name: 'bound' }`

---

### Q398: What is the output?

```js
try {
  throw new Error('Oops');
} catch (err) {
  console.log('Caught:', err.message);
} finally {
  console.log('Finally');
}
console.log('After');
```

**Answer:**

```
Caught: Oops
Finally
After
```

Explanation: `catch` handles the error, `finally` always runs, then execution continues normally.

---

### Q399: What is the output?

```js
const p1 = Promise.resolve(1);
const p2 = Promise.reject(2);
const p3 = Promise.resolve(3);

Promise.all([p1, p2, p3])
  .then(values => console.log('All:', values))
  .catch(err => console.log('Error:', err));

Promise.allSettled([p1, p2, p3])
  .then(results => console.log('Settled:', results));
```

**Answer:**

```
Error: 2
Settled: [
  { status: 'fulfilled', value: 1 },
  { status: 'rejected', reason: 2 },
  { status: 'fulfilled', value: 3 }
]
```

Explanation: `Promise.all` short-circuits on first rejection. `Promise.allSettled` waits for all to complete regardless of outcome.

---

### Q400: What is the output?

```js
const set = new Set([1, 1, 2, 2, 3, 3]);
console.log(set.size);

const map = new Map();
map.set(1, 'a');
map.set('1', 'b');
map.set(true, 'c');
console.log(map.size);
console.log(map.get(1));
console.log(map.get('1'));
console.log(map.has(true));
```

**Answer:**

```
3
3
a
b
true
```

Explanation: Sets store unique values (1, 2, 3). Maps use key equality (not type-coercing): `1` and `'1'` are different keys.

---

You've reached the end of the JavaScript (ES6+) 400+ Interview Q&A guide. Good luck with your interviews!
