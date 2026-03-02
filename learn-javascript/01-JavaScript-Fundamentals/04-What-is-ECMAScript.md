## What is ECMAScript?

### Definition

**ECMAScript** is the **official standard specification** that defines how the JavaScript language should work. It describes the **syntax, rules, types, and behavior** of JavaScript so that all JavaScript engines implement the language consistently.

In simple terms:

> ECMAScript is the specification (rules), and JavaScript is an implementation of those rules.

ECMAScript is standardized by **ECMA International** under the specification **ECMA-262**.

---

## Why ECMAScript Exists

Before ECMAScript, different browsers implemented JavaScript differently. This caused compatibility problems.

Example:

* Code working in one browser might fail in another browser.

ECMAScript was created to:

* Standardize JavaScript
* Ensure browser compatibility
* Define language features
* Maintain consistency

---

## Relationship Between ECMAScript and JavaScript

### ECMAScript

* A specification (document with rules)
* Defines how the language should behave

### JavaScript

* A programming language
* Implements ECMAScript specification

Other ECMAScript implementations include:

* JavaScript (most common)
* JScript (older Microsoft version)
* ActionScript (Adobe Flash)

Interview-ready explanation:

> ECMAScript is the standard specification that defines the JavaScript language, while JavaScript is the actual implementation used in browsers and servers.

---

## What ECMAScript Defines

ECMAScript defines:

### 1. Language Syntax

Example:

```js
let x = 10;
```

Rules for:

* Variables
* Functions
* Classes
* Loops
* Operators

---

### 2. Data Types

Defines:

* String
* Number
* Boolean
* Null
* Undefined
* Symbol
* BigInt
* Object

---

### 3. Built-in Objects

Examples:

* Array
* Object
* Date
* Math
* Promise

Example:

```js
const arr = [1,2,3];
arr.map(x => x*2);
```

---

### 4. Language Features

Examples:

* Arrow functions
* Classes
* Modules
* Async/await
* Destructuring

---

## ECMAScript Versions

ECMAScript evolves through yearly releases.

### ES5 (2009)

Important features:

* Strict mode
* JSON support
* Array methods

Example:

```js
"use strict";
```

---

### ES6 / ES2015 (Most Important Version)

Major update.

Introduced:

* `let` and `const`
* Arrow functions
* Classes
* Modules
* Promises
* Destructuring
* Spread operator

Example:

```js
const sum = (a,b) => a+b;
```

---

### ES2016+

Incremental improvements.

Examples:

#### ES2017

* async/await

```js
async function fetchData(){
 await fetch(url);
}
```

#### ES2020

* Optional chaining

```js
user?.name
```

#### ES2020

* Nullish coalescing

```js
value ?? "default"
```

---

## ECMAScript vs JavaScript Engine

ECMAScript defines rules, engines implement them.

Example engines:

* V8
* SpiderMonkey
* JavaScriptCore

Each engine reads the ECMAScript specification and implements it.

---

## Important Interview Clarifications

### ECMAScript is NOT JavaScript

Wrong:

> ECMAScript and JavaScript are the same.

Correct:

> ECMAScript is the specification, JavaScript is the implementation.

---

### ECMAScript Does NOT Include

ECMAScript does NOT define:

* DOM
* fetch
* setTimeout
* localStorage

These are provided by:

* Browsers
* Node.js

Example:

```js
document.getElementById()
```

This is **not ECMAScript**.

It is a **Browser API**.

---

## Strong Interview Answer

> ECMAScript is the official specification that defines how the JavaScript language works. It standardizes syntax, data types, and language features so that JavaScript behaves consistently across different engines and browsers.

---

Next question:

**Differences between JavaScript and TypeScript**

This is very commonly asked in React interviews.
