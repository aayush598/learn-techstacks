## Differences Between JavaScript and TypeScript

### Definition

**JavaScript** is a **dynamically typed programming language** that runs directly in browsers and servers.

**TypeScript** is a **statically typed superset of JavaScript** that compiles into JavaScript before execution.

Key idea:

> TypeScript adds static typing and development features on top of JavaScript but ultimately compiles to JavaScript.

All valid JavaScript code is valid TypeScript code.

---

## Core Differences

### 1. Typing System

#### JavaScript (Dynamic Typing)

Types are determined at runtime.

Example:

```js
let age = 25;
age = "twenty five";
```

This is allowed and produces no error until runtime.

#### TypeScript (Static Typing)

Types are checked during development (compile time).

Example:

```ts
let age: number = 25;
age = "twenty five"; // Error
```

TypeScript prevents incorrect assignments before execution.

---

### 2. Error Detection

#### JavaScript

Errors are usually detected at runtime.

Example:

```js
function add(a, b) {
 return a + b;
}

add(5, "10");
```

Result:

```
"510"
```

JavaScript does not prevent this mistake.

---

#### TypeScript

Errors are detected during compilation.

Example:

```ts
function add(a: number, b: number) {
 return a + b;
}

add(5, "10"); // Error
```

TypeScript catches this before running.

---

### 3. Compilation

#### JavaScript

Runs directly in browsers or Node.js.

Flow:

```
JavaScript → Browser → Execution
```

No build step required.

---

#### TypeScript

Must be compiled into JavaScript.

Flow:

```
TypeScript → TypeScript Compiler → JavaScript → Execution
```

Example:

TypeScript:

```ts
let name: string = "John";
```

Compiled JavaScript:

```js
var name = "John";
```

---

### 4. Type Safety

#### JavaScript

No type safety by default.

Example:

```js
let user = {};
console.log(user.name);
```

This may cause runtime issues.

---

#### TypeScript

Provides type safety.

Example:

```ts
interface User {
 name: string;
}

let user: User = {
 name: "John"
};
```

TypeScript ensures correct structure.

---

### 5. Development Experience

#### JavaScript

Basic editor support.

* Limited autocomplete
* Harder refactoring
* Harder to maintain large projects

---

#### TypeScript

Better developer tooling.

* Autocomplete
* Type checking
* Refactoring support
* Navigation support

Example:

IDE can detect incorrect property usage.

---

### 6. Large Project Support

#### JavaScript

Harder to maintain large applications.

Problems:

* Hidden bugs
* Hard refactoring
* Unclear data structures

---

#### TypeScript

Designed for large applications.

Benefits:

* Clear structure
* Defined models
* Safer refactoring

Used in:

* Enterprise apps
* Large React projects

---

### 7. Interfaces and Types

#### JavaScript

No built-in type definitions.

Example:

```js
function printUser(user){
 console.log(user.name);
}
```

No guarantee user has `name`.

---

#### TypeScript

Supports interfaces and types.

Example:

```ts
interface User {
 name: string;
 age: number;
}

function printUser(user: User){
 console.log(user.name);
}
```

---

### 8. Advanced Features

TypeScript includes features not in JavaScript:

* Interfaces
* Enums
* Generics
* Utility Types
* Type Guards

Example:

```ts
function identity<T>(value: T): T {
 return value;
}
```

JavaScript has no generics.

---

## Comparison Table

| Feature         | JavaScript   | TypeScript        |
| --------------- | ------------ | ----------------- |
| Typing          | Dynamic      | Static            |
| Compilation     | Not required | Required          |
| Error detection | Runtime      | Compile time      |
| Tooling         | Basic        | Advanced          |
| Learning curve  | Easy         | Moderate          |
| Maintainability | Medium       | High              |
| Scalability     | Medium       | High              |
| Browser support | Direct       | Needs compilation |

---

## Advantages of JavaScript

* Simple to start
* Runs everywhere
* No build process required
* Flexible

Best for:

* Small projects
* Quick scripts
* Prototypes

---

## Advantages of TypeScript

* Type safety
* Fewer runtime errors
* Better IDE support
* Better scalability

Best for:

* Large projects
* React applications
* Team development

---

## Common Interview Questions Inside This Topic

Interviewers often ask:

### Is TypeScript faster than JavaScript?

Answer:

> No. TypeScript compiles into JavaScript, so runtime performance is the same.

---

### Is TypeScript a replacement for JavaScript?

Answer:

> No. TypeScript is a superset of JavaScript that compiles into JavaScript.

---

### Can browsers run TypeScript directly?

Answer:

> No. Browsers only understand JavaScript. TypeScript must be compiled first.

---

## Strong Interview Answer

> JavaScript is a dynamically typed language that runs directly in browsers, while TypeScript is a statically typed superset of JavaScript that compiles into JavaScript. TypeScript provides type safety, better tooling, and improved maintainability, especially for large applications.

---

Next question:

**Single-threaded nature of JavaScript**

This is extremely important for React interviews.
