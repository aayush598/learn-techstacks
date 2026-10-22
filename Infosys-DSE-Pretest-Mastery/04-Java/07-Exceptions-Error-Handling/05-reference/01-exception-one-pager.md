# Exceptions — One-Page Revision Sheet

> Section 4 · Java · Exceptions & Error Handling · _Estimated reading time: 5 min_
> **Prerequisite:** [Trace the exception path](../02-techniques/01-trace-the-exception-path.md)

## In one sentence

Print this page and the topic is two tables: **the hierarchy** (which decides compile vs runtime) and
**the execution table** (which decides the exact printed output).

## Why the pre-test tests this

- Exception questions are 4–6 of the 25 Java questions. This page is the whole revision surface.
- If you can redraw both tables from memory, you lose at most one mark here.

## Core concept

### Table 1 — the hierarchy (unchecked = shaded)

```
Throwable
├── Error                      ← UNCHECKED (OutOfMemoryError, StackOverflowError)
└── Exception
    ├── RuntimeException       ← UNCHECKED (NPE, ArithmeticException, AIOOBE, ClassCast, NFE)
    └── everything else        ← CHECKED (IOException, SQLException, ClassNotFoundException,
                                  CloneNotSupportedException, InterruptedException)
```

**Unchecked = `RuntimeException` + `Error`.** Nothing else.

### Table 2 — the execution table

| Path | `catch` | `finally` | Returned value |
|---|---|---|---|
| `try` completes | — | runs | value from `try` (unless `finally` returns) |
| `try` throws, catch matches | runs | runs | value from `catch` (unless `finally` returns) |
| `try` throws, no catch | skipped | runs | **propagates** |
| `System.exit()` inside `try` | — | **skipped** | JVM exits |

### Table 3 — compile errors in exception code

| javac message | Cause |
|---|---|
| `exception X has already been caught` | A `catch` for a **subtype** placed **after** a catch of its supertype |
| `exception X is never thrown in body of corresponding try statement` | A **checked** `catch` type the body cannot throw |
| `unreported exception X; must be caught or declared to be thrown` | A checked exception thrown with no `catch` and no `throws` |

### Table 4 — API cheat

| Call | Returns |
|---|---|
| `e.getMessage()` | The message text only |
| `e.getLocalizedMessage()` | Locale-specific message |
| `e.getCause()` | The wrapped exception, or `null` |
| `e.printStackTrace()` | Prints `Type: message` + frames **to stderr**; program continues |
| `e.toString()` | `Type: message` |
| `e.fillInStackTrace()` | Resets the stack trace of the throwable |

### 60-second time budget

| Phase | Seconds | Action |
|---|---|---|
| Find throw sites | 15 | Mark every `throw`, every risky operation |
| Name the type | 10 | Use the implicit-throw table |
| Match the catch | 10 | Top to bottom, first match |
| Run `finally` | 10 | Does it `return`? Does it throw? |
| Write the output | 10 | Quoted string, exact spaces |
| Match options | 5 | Mark and move |
| **Total** | **~60** | 30 s of slack inside the 90-second rule |

### The implicit-throw table (mini)

| Code | Throws |
|---|---|
| `x / 0`, `x % 0` | `ArithmeticException` |
| `arr[i]` with `i >= arr.length` | `ArrayIndexOutOfBoundsException` |
| `obj.f()` with `obj == null` | `NullPointerException` |
| `(String) anInteger` | `ClassCastException` |
| `Integer.parseInt("abc")` | `NumberFormatException` |
| `Integer.valueOf(null)` unboxed | `NullPointerException` |

## Worked example

**Q. What is printed?**

```java
public class Main {
    static void m() {
        try {
            throw new ArithmeticException("x");
        } catch (RuntimeException e) {
            System.out.println("A");
        } finally {
            System.out.println("B");
        }
    }
    public static void main(String[] args) {
        m();
        System.out.println("C");
    }
}
```

- Throw site: `new ArithmeticException("x")` → `ArithmeticException` (unchecked, extends
  `RuntimeException`).
- Catch: `catch (RuntimeException e)` matches (the thrown type is a subtype). Prints `A`.
- `finally`: no `return`, prints `B`.
- Back in `main`: prints `C`.

**Output (exact):**

```
A
B
C
```

## Quick rules

- Unchecked = `RuntimeException` + `Error`.
- First matching catch wins, top to bottom.
- Subclass-before-superclass = legal; superclass-before-subclass = compile error.
- `catch (Exception e)` / `catch (Throwable e)` always legal.
- `finally` runs on every path except `System.exit()`.
- `return` in `finally` wins over the pending value.
- An exception in `finally` replaces the original.
- `throw` raises, `throws` declares.
- `getMessage()` → message only; `getCause()` → the wrapped exception.

## Common traps

| Trap | Fix |
|---|---|
| `finally` runs after `System.exit()` | It does not |
| `try`'s pending return wins | `finally`'s return wins |
| Original exception survives an exception in `finally` | It is discarded |
| `catch (Exception)` catches `Error` | Use `Throwable` |
| Checked catch that can never happen compiles | Compile error |

## Checklist

- [ ] I can redraw the hierarchy in 30 seconds.
- [ ] I can recite the execution table.
- [ ] I know all three javac messages.
- [ ] I know the 60-second budget for one exception question.
- [ ] I can state the exact output of the worked example above (`A`, `B`, `C`).

## Related

- [Throwable hierarchy, checked vs unchecked](../01-concepts/01-throwable-hierarchy-and-checked-vs-unchecked.md)
- [try/catch/finally and resource management](../01-concepts/02-try-catch-finally-and-resource-management.md)
- [Trace the exception path](../02-techniques/01-trace-the-exception-path.md)
- [Choose the right catch strategy](../02-techniques/02-choose-the-right-catch-strategy.md)
- [Solved exception set](../03-worked-examples/01-solved-exception-set.md)
- [Exception traps](../04-pitfalls/01-exception-traps.md)
- [Topic overview](../README.md)
