# Compile-Error Traps — Snippets That Look Fine but Do Not Compile

> Section 4 · Java · Output Prediction Patterns · _Estimated reading time: 10 min_
> **Prerequisite:** [Compile vs run taxonomy](../01-concepts/02-compile-vs-run-taxonomy.md)

## In one sentence

These snippets **look** like valid Java to a fast reader — the trap is that the compiler rejects
them, so the correct answer is "does not compile" and **no output exists**.

## Why the pre-test tests this

- "Does this code compile?" is a reported archetype, and the answer is one of 4 options.
- The dangerous distractors are the ones with plausible printed output. If you never considered
  "compile error", you will pick one of them.
- Rule: **if any option says "does not compile", check the catalogue before you compute output.**

## Core concept

### The 10 compile-error traps

| # | Snippet | javac message | Trap |
|---|---|---|---|
| 1 | `return 1;` followed by `System.out.println("x");` | `unreachable statement` | Reads like two statements |
| 2 | `int m() { }` | `missing return statement` | Empty body "looks harmless" |
| 3 | `int x = "hello";` | `incompatible types: String cannot be converted to int` | |
| 4 | `int x = 10L;` | `possible lossy conversion from long to int` | "It's just a number" |
| 5 | `arr.length()` on an array | `cannot find symbol: method length()` | `length` is a **field** |
| 6 | `new MyAbstractClass();` | `abstract class MyAbstractClass cannot be instantiated` | |
| 7 | `new MyInterface();` | `interface MyInterface cannot be instantiated` | |
| 8 | `obj.instanceMethod()` from `static void main` without an object | `non-static method ... cannot be referenced from a static context` | |
| 9 | `System.out.println(this);` inside a `static` method | `non-static variable this cannot be referenced from a static context` | |
| 10 | `int x = 1; int x = 2;` | `variable x is already defined in method main` | |
| 11 | `break;` outside any loop or switch | `break outside switch or loop` | |
| 12 | `final int x = 1; x = 2;` | `cannot assign a value to final variable x` | |
| 13 | `super();` inside a `static` method | `non-static variable super cannot be referenced from a static context` | |
| 14 | `throw new IOException();` with no `catch`/`throws` | `unreported exception java.io.IOException; must be caught or declared to be thrown` | |
| 15 | A concrete class that does not implement an abstract method | `X is not abstract and does not override abstract method m() in I` | |
| 16 | `class A extends B` and `class B extends A` | `cyclic inheritance involving A` | |
| 17 | Override with an incompatible return type | `m() in B cannot override m() in A; ... return type int is not compatible with String` | |
| 18 | Override a `final` method | `m() in B cannot override m() in A; overriding method is final` | |
| 19 | Parent `static void m()`, child `void m()` | `m() in B cannot override m() in A; overriding method is static` | |
| 20 | Parent `void m()`, child `static void m()` | `m() in B cannot override m() in A; overriding method is not static` | |
| 21 | `catch (IOException e)` around a body that cannot throw it | `exception IOException is never thrown in body of corresponding try statement` | |
| 22 | `catch (Exception e)` then `catch (IOException e)` | `exception IOException has already been caught` | |
| 23 | `int y = 10; long x = y;` (reverse direction) | `possible lossy conversion` — but `long x = y;` is **legal** | |
| 24 | `this()` / `super()` not the first statement | `constructor call must be first statement in constructor` | |
| 25 | `int b = 10; byte c = b;` | `incompatible types: int cannot be converted to byte` | |
| 26 | `char c = 'a'; c = 'ab';` | `incompatible types: String cannot be converted to char` | |
| 27 | Use an uninitialised local | `variable x might not have been initialized` | |
| 28 | `final` field never assigned | `variable x not initialized in the default constructor` | |
| 29 | Two methods with the same signature | `method m() is already defined in class X` | |
| 30 | Missing semicolon | `';' expected` | |

### The "looks legal but is not" top 5

These are the ones that catch experienced candidates, because the *idea* is right and only the
**wording** is wrong:

| Snippet | Why it fails |
|---|---|
| `arr.length()` | `length` is a **field** on arrays, a **method** on `String` |
| `byte b = 10; b = b + 5;` | The compound form `b += 5` is legal; the plain form is not |
| `catch (Exception e) { } catch (IOException e) { }` | The second clause is unreachable |
| `class B extends A` where `A` has only `A(int)` constructors | `constructor A in class B cannot be applied to given types` |
| `int x = 10L;` | `long` → `int` is narrowing, not widening |

### The narrowing/widening table you will be tested on

| Statement | Legal? | Message if not |
|---|---|---|
| `long x = 10;` | ✅ | |
| `float f = 10;` | ✅ | |
| `double d = 10L;` | ✅ | |
| `int x = 10L;` | ❌ | `possible lossy conversion from long to int` |
| `int x = 10.5;` | ❌ | `possible lossy conversion from double to int` |
| `byte b = 10;` | ✅ | constant in range |
| `byte b = 300;` | ❌ | `possible lossy conversion from int to byte` |
| `char c = 65;` | ✅ | constant in range |
| `int x = someLong;` | ❌ | `possible lossy conversion from long to int` |
| `int x = (int) someLong;` | ✅ | explicit cast |
| `byte b = someByteInt;` | ❌ | `incompatible types: int cannot be converted to byte` |
| `byte b = (byte) someByteInt;` | ✅ | explicit cast |

### The "no output at all" reminder

For every compile error above, the program **never starts**. So:

- No output.
- No stack trace.
- No exit code — the JVM was never launched with that class.

If an option shows printed text for a non-compiling snippet, that option is wrong.

## Worked example

**Q. Which statement is TRUE?**

```java
public class Main {
    public static void main(String[] args) {
        int[] a = {1, 2, 3};
        System.out.println(a.length());
    }
}
```

A. It prints `3`.
B. It prints `3.0`.
C. It does not compile — `length` is a field, not a method.
D. It prints `[1, 2, 3]`.

**Solution** — `length` on an array is a **public final int field**, so it is accessed without
parentheses: `a.length`. Writing `a.length()` asks for a **method** named `length` on the array type
`int[]`, and arrays have no such method.

```
error: cannot find symbol: method length()
  location: variable a of type int[]
```

**Answer: C.**

**Why the distractors fail**

| Option | Why it is wrong |
|---|---|
| A | The code never compiles, so nothing is printed |
| B | Same — and `length` is an `int`, not a `double` |
| D | `System.out.println(a)` on an array prints the identity form like `[I@1b6d3586` (the digits vary per run), and `a.length()` still does not compile |

## Quick rules

- `length` is a **field** on arrays and a **method** on `String`.
- A compile error means **zero output**.
- Widening is free; narrowing needs an explicit cast, except for in-range compile-time constants.
- `x += y` narrows implicitly; `x = x + y` does not.
- A `catch` for a subtype placed after a `catch` for its supertype does not compile.
- A `catch` for a checked type the body cannot throw does not compile.
- `static` methods hide; they never override. `final` methods cannot be overridden at all.

## Common traps

| Trap | What you pick | Fix |
|---|---|---|
| Array bounds check | compile error | runtime |
| `arr.length()` | "prints 3" | field, not method |
| `catch (Exception)` then a subclass | compiles | "already been caught" |
| `int x = 10L;` | "widening" | narrowing |
| `byte b = b + 5;` | compiles | needs a cast |

## Checklist

- [ ] I check the compile-error catalogue before computing any output.
- [ ] I know the exact javac messages for the six most common errors.
- [ ] I know `length` is a field on arrays and a method on `String`.
- [ ] I can state the widening/narrowing table from memory.
- [ ] I know that a compile error produces no output whatsoever.

## Related

- [Compile vs run taxonomy](../01-concepts/02-compile-vs-run-taxonomy.md)
- [The evaluation-order model](../01-concepts/01-the-evaluation-order-model.md)
- [Compile-error catalogue](../05-reference/02-compile-error-catalogue.md)
- [Output traps](01-output-traps.md)
- [Topic overview](../README.md)
