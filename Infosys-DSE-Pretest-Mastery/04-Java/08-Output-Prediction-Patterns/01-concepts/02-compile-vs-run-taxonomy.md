# Compile vs Run — a Three-Way Taxonomy

> Section 4 · Java · Output Prediction Patterns · _Estimated reading time: 10 min_
> **Prerequisite:** [The evaluation-order model](01-the-evaluation-order-model.md)

## In one sentence

Every code snippet in the pre-test ends in exactly one of three states — **compile error** (no
output at all), **runtime exception** (partial output, then a stack trace on stderr), or **normal
output** — and the first thing to decide is which one you are looking at.

## Why the pre-test tests this

- "Does this code compile?" and "What is the output?" are often the *same* question with different
  options.
- The most common wrong answer in this archetype is picking an option with **printed output** for
  code that does not compile. If the code does not compile, it prints **nothing at all**.
- Knowing the difference between the three states removes whole options instantly.

## Core concept

### The three states

| State | What the program does | What you see |
|---|---|---|
| **Compile error** | Never runs | **Nothing.** No output, no exception |
| **Runtime exception** | Runs until the throw, then dies | Whatever was printed **before** the throw, then a stack trace on **stderr**, non-zero exit code |
| **Normal output** | Runs to completion | Exactly the printed text |

The exam's options usually make this visible: if an option shows a stack trace, the answer is
"runtime error"; if an option shows printed lines only, the code must compile and complete.

### The 10-second decision

```
Does the code contain any construct from the compile-error catalogue?
   → YES: compile error. No output. Done.
   → NO: read the body for a throw site.
        → throw site reachable?  → runtime exception (partial output + stack trace)
        → no throw site?         → normal output
```

### The five compile-error families you must recognise instantly

| Family | Example | javac message (abridged) |
|---|---|---|
| **Missing / unreachable code** | `return;` then `System.out.println("x");` | `unreachable statement` |
| | a method that can fall off the end | `missing return statement` |
| **Type mismatch** | `int x = "hello";` | `incompatible types: String cannot be converted to int` |
| | `int x = 10L;` | `possible lossy conversion from long to int` |
| **Bad member access** | `arr.length()` on an array | `cannot find symbol: method length()` |
| | `obj.field` where `obj` is static-used | `non-static variable ... cannot be referenced from a static context` |
| **Abstract / interface misuse** | `new AbstractClass();` | `abstract class X cannot be instantiated` |
| | `new AnInterface();` | `interface X cannot be instantiated` |
| **Override violations** | covariant return broken, `final` method overridden, `static`/instance mismatch | `... cannot override ...` |
| **Checked exception not handled** | `throw new IOException();` with no `catch`/`throws` | `unreported exception java.io.IOException; must be caught or declared to be thrown` |

The full list with 5-line repros lives in
[the compile-error catalogue](../05-reference/02-compile-error-catalogue.md).

### The narrowing/widening rules (used constantly)

| Assignment | Legal? | Reason |
|---|---|---|
| `long x = 10;` | ✅ | Widening primitive conversion (`int` → `long`) is always allowed |
| `float f = 10;` | ✅ | Widening (`int` → `float`) |
| `double d = 10L;` | ✅ | Widening (`long` → `double`) |
| `int x = 10L;` | ❌ | Narrowing — "possible lossy conversion from long to int" |
| `int x = 10.5;` | ❌ | Narrowing from `double` |
| `byte b = 10;` | ✅ | A compile-time constant `int` in range fits into `byte` |
| `byte b = 300;` | ❌ | Constant out of `byte` range |
| `char c = 65;` | ✅ | Constant `int` in range fits into `char` |
| `Object o = "s";` | ✅ | Widening reference conversion |
| `String s = new Object();` | ❌ | Not a subtype |

**Constant narrowing is allowed; variable narrowing is not.** `final int x = 10; byte b = x;` works
because `x` is a compile-time constant in range. `int y = 10; byte b = y;` does not.

### Compound assignment escapes the narrowing rule

```java
byte b = 10;
b += 5;          // legal — implicit cast to byte is built into the compound assignment
b = b + 5;       // illegal — plain expression, needs an explicit cast
```

### "Runtime exception" — the six you will meet

| Trigger | Exception |
|---|---|
| `x / 0` or `x % 0` | `ArithmeticException` |
| `arr[i]` out of bounds | `ArrayIndexOutOfBoundsException` |
| Null dereference | `NullPointerException` |
| Bad reference cast | `ClassCastException` |
| `Integer.parseInt("abc")` | `NumberFormatException` |
| Modifying a collection while iterating it | `ConcurrentModificationException` |

### What the exam's options usually look like

| Option shape | What it tells you |
|---|---|
| A printed string with no exception text | The code compiles **and** completes normally — or it does not compile |
| A printed string **plus** `Exception in thread "main" ...` | The code compiles and throws at runtime, after the printed part |
| "Compilation error" / "does not compile" | A compile error — no output at all |
| An empty string `""` | Possible: a compile error, or code that prints nothing |

**Critical:** an empty-string option covers both "compile error" and "prints nothing". If the
question asks *which*, you must identify the compile error specifically.

## Worked example

**Q. Which statement is TRUE about the following code?**

```java
public class Main {
    public static void main(String[] args) {
        int[] a = new int[3];
        System.out.println(a[3]);
        System.out.println("done");
    }
}
```

A. It prints `done`.
B. It prints `3` and then `done`.
C. It throws `ArrayIndexOutOfBoundsException` at runtime; `done` is never printed.
D. It does not compile.

**Solution**

- **Compile check:** `int[] a = new int[3];` is fine. `a[3]` is a legal *expression*; the compiler
  does not know the value of `a[3]`. `a.length` is 3, but bounds checking is a runtime job.
  → **Compiles.**
- **Runtime check:** `a[3]` with `a.length == 3` → `ArrayIndexOutOfBoundsException`.
- The exception is thrown on the `println` line, so `done` is never reached.
- Uncaught → stack trace on stderr, non-zero exit code.

**Answer: C.**

**Why the distractors fail**

| Option | Why it is wrong |
|---|---|
| A | `done` is after the throwing line |
| B | `a[3]` throws; it does not print `3` |
| D | Array bounds are not a compile-time check in Java |

## Quick rules

- Compile error → **no output whatsoever**, not even a blank line.
- Runtime exception → printed output **up to** the throw, then a stack trace on stderr.
- Widening is free; narrowing needs a cast, **except** for compile-time constants in range.
- `x += y` narrows implicitly; `x = x + y` does not.
- Array bounds are checked at **runtime**, not compile time.
- `catch (Exception e)` is always legal; a checked catch the body cannot throw is not.

## Common traps

| Trap | What you pick | Why it is wrong |
|---|---|---|
| "Out of bounds" | compile error | Bounds are checked at runtime |
| "The code prints `done`" | the normal-path option | The throw happens first |
| "No output" for a compile error | empty-string option | Usually right, but say "compile error" if asked |
| `int x = 10L;` | "widening works" | `long` → `int` is narrowing |
| `byte b = 300;` | "constant, so it is fine" | The constant is out of `byte` range |

## Checklist

- [ ] I can name the three states and what each one produces.
- [ ] I check for a compile error **before** I look for output.
- [ ] I know the widening/narrowing table.
- [ ] I know that compound assignment narrows implicitly.
- [ ] I can list the six runtime exceptions you will meet.

## Related

- [The evaluation-order model](01-the-evaluation-order-model.md)
- [Compile-error catalogue](../05-reference/02-compile-error-catalogue.md)
- [Compile-error traps](../04-pitfalls/02-compile-error-traps.md)
- [10-second triage](../02-techniques/01-ten-second-triage.md)
- [Topic overview](../README.md)
