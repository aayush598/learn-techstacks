## Is JavaScript Compiled or Interpreted?

### Short Answer (Interview Version)

JavaScript is **both interpreted and compiled**. Traditionally it was interpreted, but modern JavaScript engines use **Just-In-Time (JIT) compilation** to improve performance.

A precise answer:

> JavaScript is an interpreted language that uses Just-In-Time (JIT) compilation in modern engines to optimize execution speed.

---

## Understanding Interpreted vs Compiled

### Compiled Languages

In compiled languages, code is translated into machine code **before execution**.

Example languages:

* C
* C++
* Go

Flow:

```
Source Code → Compiler → Machine Code → Run
```

Characteristics:

* Compilation step required
* Fast execution
* Errors detected before running

Example:

C code must be compiled before running.

---

### Interpreted Languages

In interpreted languages, code is executed **line by line at runtime**.

Example languages:

* JavaScript (traditionally)
* Python

Flow:

```
Source Code → Interpreter → Execution
```

Characteristics:

* No manual compilation step
* Runs immediately
* Errors occur at runtime

---

## How JavaScript Actually Works (Modern Engines)

Modern browsers use **JIT compilation (Just-In-Time)**.

Example engines:

* Chrome → V8
* Firefox → SpiderMonkey
* Safari → JavaScriptCore

### Execution Steps

#### Step 1 — Parsing

The engine reads the code and converts it into tokens.

Example:

```js
let x = 10;
```

Converted into syntax elements.

---

#### Step 2 — AST Creation

Code becomes an **Abstract Syntax Tree (AST)**.

Example structure:

```
VariableDeclaration
   Identifier: x
   Value: 10
```

---

#### Step 3 — Bytecode Generation

The engine converts AST into **bytecode**.

Bytecode is intermediate machine instructions.

---

#### Step 4 — Interpretation

The engine executes bytecode.

---

#### Step 5 — JIT Compilation

Frequently used code is optimized into **machine code**.

Example:

A loop running thousands of times becomes optimized machine code.

This improves performance dramatically.

---

## Why JavaScript Uses JIT Compilation

Reasons:

### 1. Speed

JIT makes JavaScript much faster than pure interpretation.

### 2. Optimization

Engines detect:

* Frequently executed functions
* Hot loops
* Stable types

Then optimize them.

---

## Important Interview Concept

### JavaScript is NOT Precompiled

Languages like C++:

```
Write → Compile → Run
```

JavaScript:

```
Write → Run Immediately
```

No manual compilation.

---

## Common Interview Trick Question

### Question

Is JavaScript compiled?

### Wrong Answer

> No, JavaScript is interpreted.

### Correct Answer

> JavaScript is interpreted but modern engines use JIT compilation.

---

## Real Interview Explanation (Best Answer)

> JavaScript is traditionally an interpreted language, but modern JavaScript engines use Just-In-Time compilation. The engine parses the code, converts it into bytecode, and frequently executed code is compiled into machine code for better performance.

---

## Follow-up Questions Usually Asked

Most interviewers immediately ask:

1. **How JavaScript runs in the browser**
2. **What is Event Loop**
3. **Single-threaded nature**

Next logical question:

**How JavaScript runs in the browser?**
