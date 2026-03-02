## How JavaScript Runs in the Browser

This question tests understanding of the **JavaScript runtime environment**, including the **JavaScript engine, call stack, Web APIs, callback queues, and event loop**.

A structured explanation is expected in interviews.

---

## Overview

When JavaScript runs in a browser, multiple components work together:

1. **JavaScript Engine**
2. **Call Stack**
3. **Web APIs**
4. **Callback Queues**
5. **Event Loop**

Simplified flow:

```
JavaScript Code
     ↓
JavaScript Engine
     ↓
Call Stack
     ↓
Web APIs (async tasks)
     ↓
Callback Queue
     ↓
Event Loop
     ↓
Call Stack
```

---

## 1. JavaScript Engine

The browser contains a JavaScript engine responsible for executing JavaScript code.

Examples:

* Chrome → V8
* Firefox → SpiderMonkey
* Safari → JavaScriptCore

### Responsibilities

The engine:

1. Parses JavaScript code
2. Creates execution contexts
3. Executes code
4. Manages memory

---

## 2. Parsing Phase

When the browser loads JavaScript:

### Step 1 — Tokenization

The engine breaks code into tokens.

Example:

```js
let x = 10;
```

Tokens:

```
let | x | = | 10
```

---

### Step 2 — Abstract Syntax Tree (AST)

The tokens are converted into a structured tree.

Example structure:

```
VariableDeclaration
   Identifier: x
   Value: 10
```

---

## 3. Execution Context Creation

Before code runs, JavaScript creates an **Execution Context**.

Two phases occur:

### Phase 1 — Memory Creation Phase

Variables and functions are stored in memory.

Example:

```js
var x = 10;

function greet(){
 console.log("Hello");
}
```

Memory becomes:

```
x → undefined
greet → function code
```

---

### Phase 2 — Execution Phase

Code executes line by line.

Memory becomes:

```
x → 10
```

---

## 4. Call Stack

The **Call Stack** manages function execution.

It works on **LIFO (Last In First Out)**.

Example:

```js
function a(){
 b();
}

function b(){
 console.log("Hello");
}

a();
```

Stack behavior:

Step 1:

```
Global()
```

Step 2:

```
Global()
a()
```

Step 3:

```
Global()
a()
b()
```

Step 4:

```
Global()
a()
```

Step 5:

```
Global()
```

---

## 5. Web APIs

Web APIs are provided by the **browser**, not JavaScript itself.

Examples:

* DOM
* setTimeout
* fetch
* localStorage
* geolocation

Example:

```js
setTimeout(() => {
 console.log("Done");
}, 2000);
```

Process:

1. setTimeout goes to Web APIs
2. Timer starts
3. Call stack becomes free

---

## 6. Callback Queue (Task Queue)

When async operations finish, callbacks move into a queue.

Example:

```
Callback Queue:
[ setTimeout callback ]
```

The callback waits until the call stack is empty.

---

## 7. Microtask Queue

Higher priority queue.

Contains:

* Promise callbacks
* MutationObserver

Example:

```js
Promise.resolve().then(()=>{
 console.log("Promise");
});
```

Microtasks execute before normal tasks.

---

## 8. Event Loop

The **Event Loop** continuously checks:

1. Is Call Stack empty?
2. If yes → Move tasks from queues to stack.

Rule:

```
Microtask Queue → First
Callback Queue → Second
```

---

## Example Execution

```js
console.log("Start");

setTimeout(()=>{
 console.log("Timeout");
},0);

Promise.resolve().then(()=>{
 console.log("Promise");
});

console.log("End");
```

### Step-by-step

#### Step 1

```
Start
```

#### Step 2

setTimeout → Web API

#### Step 3

Promise → Microtask queue

#### Step 4

```
End
```

Stack empty.

#### Step 5

Microtask runs:

```
Promise
```

#### Step 6

Callback queue runs:

```
Timeout
```

### Final Output

```
Start
End
Promise
Timeout
```

---

## Important Interview Concept

### JavaScript Runtime Environment

JavaScript runtime in browser includes:

* JavaScript Engine
* Call Stack
* Web APIs
* Event Loop
* Queues

JavaScript language alone only includes:

* Variables
* Functions
* Objects

Browser provides:

* DOM
* fetch
* setTimeout

---

## Strong Interview Answer (Ideal)

> JavaScript runs in the browser using a JavaScript engine. The engine executes code using the call stack. Asynchronous operations like timers and API calls are handled by browser Web APIs. When those operations complete, callbacks are placed in queues, and the event loop moves them to the call stack when it becomes empty.

---

Next question:

**What is ECMAScript?**

This is usually asked immediately after this topic.
