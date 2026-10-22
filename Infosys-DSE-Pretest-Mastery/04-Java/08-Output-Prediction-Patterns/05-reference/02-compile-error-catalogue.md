# Compile-Error Catalogue — 30 Errors with the Exact javac Message

> Section 4 · Java · Output Prediction Patterns · _Estimated reading time: 12 min_
> **Prerequisite:** [Compile vs run taxonomy](../01-concepts/02-compile-vs-run-taxonomy.md)

## In one sentence

Thirty compile errors, each with the **actual javac wording** and a 5-line repro — this is the
catalogue you scan before you compute any output.

## Why the pre-test tests this

- "Does this code compile?" is a reported archetype. The options are usually:
  - "It compiles and prints X"
  - "It compiles and throws Y"
  - "It does not compile"
- Knowing the **exact wording** lets you recognise the error in 2 seconds, because you can see the
  phrase you were looking for.
- All messages below are from `javac` (Oracle JDK 8 / 17 wording is essentially the same).

## Core concept

### Group A — statements and control flow

| # | Repro | javac message |
|---|---|---|
| 1 | `int m(){ return 1; System.out.println("x"); }` | `unreachable statement` |
| 2 | `int m(){ }` | `missing return statement` |
| 3 | `void m(){ break; }` | `break outside switch or loop` |
| 4 | `void m(){ continue; }` | `continue outside of loop` |
| 5 | `class A { void m(){ return 1; } }` | `incompatible types: int cannot be converted to void` |
| 6 | `int x = 1 int y = 2;` | `';' expected` |
| 7 | `if (x = 1) { }` | compiles — **not** an error (assignment is a valid condition) |
| 8 | `int x; System.out.println(x);` | `variable x might not have been initialized` |

### Group B — types and conversions

| # | Repro | javac message |
|---|---|---|
| 9 | `int x = "hello";` | `incompatible types: String cannot be converted to int` |
| 10 | `int x = 10L;` | `possible lossy conversion from long to int` |
| 11 | `int x = 10.5;` | `possible lossy conversion from double to int` |
| 12 | `byte b = 300;` | `possible lossy conversion from int to byte` |
| 13 | `int x = someLong;` | `possible lossy conversion from long to int` |
| 14 | `byte b = someInt;` | `incompatible types: int cannot be converted to byte` |
| 15 | `char c = "a";` | `incompatible types: String cannot be converted to char` |
| 16 | `String s = new Object();` | `incompatible types: Object cannot be converted to String` |
| 17 | `byte b = 10; b = b + 5;` | `incompatible types: int cannot be converted to byte` |
| 18 | `int[] a = {1,2}; String s = a;` | `incompatible types: int[] cannot be converted to String` |

**Legal narrowing that surprises people:**

| Code | Why it is legal |
|---|---|
| `final int x = 10; byte b = x;` | `x` is a compile-time constant **in range** |
| `int x = 10L;` → `long y = x;` | Widening `int` → `long` is always fine |
| `double d = 10;` | Widening `int` → `double` is fine |
| `char c = 65;` | Compile-time constant in range |
| `b += 5;` where `b` is a `byte` | Compound assignment casts implicitly |

### Group C — members, classes and `this`/`super`

| # | Repro | javac message |
|---|---|---|
| 19 | `arr.length()` where `arr` is `int[]` | `cannot find symbol: method length()` |
| 20 | `obj.m();` in `static void main` with no object | `non-static method m() cannot be referenced from a static context` |
| 21 | `System.out.println(this);` in a `static` method | `non-static variable this cannot be referenced from a static context` |
| 22 | `super();` in a `static` method | `non-static variable super cannot be referenced from a static context` |
| 23 | `int x = 1; int x = 2;` | `variable x is already defined in method main` |
| 24 | `void m(){} void m(){}` | `method m() is already defined in class Main` |
| 25 | `new MyAbstract();` | `abstract class MyAbstract cannot be instantiated` |
| 26 | `new MyInterface();` | `interface MyInterface cannot be instantiated` |
| 27 | `class A extends B {} class B extends A {}` | `cyclic inheritance involving A` |
| 28 | `class C extends P { C(){ System.out.println("x"); super(); } }` | `constructor call must be first statement in constructor` |
| 29 | `class C extends P { C(){ this(); } }` where `P` has no no-arg constructor | `constructor P in class C cannot be applied to given types` |
| 30 | `final int x = 1; x = 2;` | `cannot assign a value to final variable x` |
| 31 | `void m(final int x){ x = 5; }` | `cannot assign a value to final parameter x` |
| 32 | `final int x;` in a class with no constructor | `variable x not initialized in the default constructor` |

### Group D — inheritance and overriding

| # | Repro | javac message |
|---|---|---|
| 33 | Parent `int m()`, child `String m()` | `m() in C cannot override m() in P; return type String is not compatible with int` |
| 34 | Parent `void m()`, child `static void m()` | `m() in C cannot override m() in P; overriding method is not static` |
| 35 | Parent `static void m()`, child `void m()` | `m() in C cannot override m() in P; overriding method is static` |
| 36 | Parent `final void m()`, child `void m()` | `m() in C cannot override m() in P; overriding method is final` |
| 37 | Concrete class missing an abstract method | `C is not abstract and does not override abstract method m() in I` |
| 38 | `static` and `instance` method with the same signature in one class | `method m() is already defined in class C` |

**Legal "hiding" that is *not* an error:**

| Code | Verdict |
|---|---|
| Parent `static void m()`, child `static void m()` | ✅ Legal — this is **hiding** |
| Parent `int x`, child `int x` | ✅ Legal — field **hiding** |
| Parent `void m()`, child `void m()` | ✅ Legal — **overriding** |

### Group E — exceptions

| # | Repro | javac message |
|---|---|---|
| 39 | `try { int x = 1; } catch (IOException e) { }` | `exception IOException is never thrown in body of corresponding try statement` |
| 40 | `catch (Exception e){} catch (IOException e){}` | `exception IOException has already been caught` |
| 41 | `throw new IOException();` with no `catch`/`throws` | `unreported exception java.io.IOException; must be caught or declared to be thrown` |
| 42 | `catch (IOException | FileNotFoundException e){}` | `alternatives in a multi-catch statement cannot be related by subclassing` |
| 43 | `catch (IOException | SQLException e){}` where the body throws neither | `exception IOException is never thrown in body of corresponding try statement` |

### Group F — generics, arrays and casts

| # | Repro | javac message |
|---|---|---|
| 44 | `List<int> l = new ArrayList<>();` | `type argument int is not within the bounds of the type-variable E` |
| 45 | `Object o = "s"; String s = (Integer) o;` | **compiles** — fails at runtime with `ClassCastException` |
| 46 | `int[] a = new int[-1];` | `illegal array size` (runtime for a non-constant) |
| 47 | `int x = (int) "abc";` | `incompatible types: String cannot be converted to int` |
| 48 | `String s = (String) 5;` | `incompatible types: int cannot be converted to String` |

### The 12 you are most likely to meet

| Rank | Error | Recognise it by |
|---|---|---|
| 1 | `unreachable statement` | code after a `return`/`throw`/`break` |
| 2 | `missing return statement` | a non-`void` method that can fall off the end |
| 3 | `incompatible types: X cannot be converted to Y` | assigning across unrelated types |
| 4 | `possible lossy conversion from X to Y` | narrowing a primitive |
| 5 | `cannot find symbol: method length()` | `arr.length()` |
| 6 | `non-static method ... cannot be referenced from a static context` | calling an instance method from `static main` |
| 7 | `abstract class X cannot be instantiated` | `new` on an abstract class |
| 8 | `interface X cannot be instantiated` | `new` on an interface |
| 9 | `exception X has already been caught` | catch order |
| 10 | `exception X is never thrown in body of corresponding try statement` | impossible checked catch |
| 11 | `unreported exception X; must be caught or declared to be thrown` | unchecked? no — checked exception unhandled |
| 12 | `variable x is already defined` | duplicate local |

## Worked example

**Q. Does this compile?**

```java
public class Main {
    static void m() {
        int x = 10;
        long y = x;
        byte z = y;
    }
}
```

**Solution**

| Statement | Legal? | Reason |
|---|---|---|
| `long y = x;` | ✅ | `int` → `long` is **widening**, always allowed |
| `byte z = y;` | ❌ | `long` → `byte` is **narrowing** and `y` is not a compile-time constant |

**Answer: It does not compile.**

```
error: incompatible types: long cannot be converted to byte
```

**Why the distractors fail**

| Option | Why it is wrong |
|---|---|
| "It compiles — `long` is bigger than `byte`" | Widening only goes one way: small → large |
| "It compiles and prints nothing" | A compile error means the program never runs |
| "It throws `ClassCastException`" | There is no cast here, and it never compiles |

## Quick rules

- Scan this catalogue **before** you compute any output.
- A compile error means **zero output** — no text, no stack trace.
- Widening is free; narrowing needs an explicit cast, except for in-range compile-time constants.
- `x += y` narrows implicitly; `x = x + y` does not.
- `static` methods **hide**, they do not override; mixing static and instance with the same signature
  **is** an error.

## Common traps

| Trap | Fix |
|---|---|
| "It compiles because the types are close" | Narrowing needs a cast |
| "It compiles because `catch (Exception)` is there" | Check the **order** of the catch clauses |
| "It prints nothing" for a compile error | Say "does not compile" |
| "Static methods are overridden" | They are hidden; a static/instance mismatch is an error |

## Checklist

- [ ] I can recognise the six most common javac messages on sight.
- [ ] I know the widening/narrowing rules cold.
- [ ] I know the difference between hiding and overriding.
- [ ] I know that a compile error produces no output.
- [ ] I know `arr.length` (field) vs `str.length()` (method).

## Related

- [Compile vs run taxonomy](../01-concepts/02-compile-vs-run-taxonomy.md)
- [Compile-error traps](../04-pitfalls/02-compile-error-traps.md)
- [The evaluation-order model](../01-concepts/01-the-evaluation-order-model.md)
- [Output rules one-pager](01-output-rules-one-pager.md)
- [Topic overview](../README.md)
