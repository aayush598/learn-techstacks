# Throwable Hierarchy, Checked vs Unchecked, and Custom Exceptions

> Section 4 · Java · Exceptions & Error Handling · _Estimated reading time: 9 min_
> **Prerequisite:** none

## In one sentence

Every exception in Java descends from `Throwable`, and **only `RuntimeException` and `Error` are
unchecked** — everything else the compiler forces you to handle.

## Why the pre-test tests this

- The pre-test asks "which of these is an unchecked exception?" and "which class is a superclass of
  all exceptions?" as one-liners. They are cheap marks if you own the tree.
- The same tree decides whether a `catch` clause compiles. That makes it a *scoring* topic, not a
  trivia topic.
- "Does this code compile?" questions are decided by one thing: is the checked exception handled?

## Core concept

### The hierarchy — memorise this shape

```
java.lang.Object
└── java.lang.Throwable                  ← only Throwable has getMessage(), getCause(), printStackTrace()
    ├── java.lang.Error                  ← UNCHECKED. Serious JVM problems. You do not catch these.
    │   ├── OutOfMemoryError
    │   ├── StackOverflowError
    │   └── VirtualMachineError
    └── java.lang.Exception              ← the "normal" exception branch
        ├── java.lang.RuntimeException   ← UNCHECKED. Programmer bugs.
        │   ├── NullPointerException
        │   ├── ArithmeticException      (÷ by zero)
        │   ├── ArrayIndexOutOfBoundsException
        │   ├── ClassCastException
        │   ├── NumberFormatException
        │   └── IllegalArgumentException  (parent of NumberFormatException)
        └── (everything else here is CHECKED)
            ├── java.io.IOException
            ├── java.sql.SQLException
            ├── java.lang.ClassNotFoundException
            ├── java.lang.CloneNotSupportedException
            └── java.lang.InterruptedException
```

**The rule in one line:** a throwable is **unchecked** if it is a `RuntimeException` or an `Error`;
everything else is **checked**.

### Checked vs unchecked — what actually changes

| | Checked | Unchecked |
|---|---|---|
| Examples | `IOException`, `SQLException`, `ClassNotFoundException` | `NullPointerException`, `ArithmeticException`, `ArrayIndexOutOfBoundsException` |
| Compiler behaviour | You **must** `catch` it or declare it with `throws` | Nothing required |
| Typical cause | Something outside your control (file, network, DB) | A bug in your logic |
| Best practice | Catch it at the boundary and handle/recover | Usually let it propagate and fix the bug |

### `throw` vs `throws` — the single most-tested distinction

| Keyword | Where it appears | What it does |
|---|---|---|
| `throw` | A **statement**, inside a method body | **Raises** one specific exception object now |
| `throws` | A **clause** on the method signature | **Declares** that this method may pass one (or several) exceptions to its caller |

```java
static void a() throws IOException {      // declares: callers must handle IOException
    throw new IOException("boom");        // raises: creates and throws it now
}

static void b() {                         // declares nothing → callers need not handle
    throw new RuntimeException("oops");    // unchecked → compiles with no catch
}
```

You can declare several: `throws IOException, SQLException`. You can also use a bare `throws Exception`,
which is legal but weak — it forces every caller to handle exceptions it will never see.

### Custom exceptions — the 3-line template

```java
class InsufficientBalanceException extends Exception {        // CHECKED
    InsufficientBalanceException(String message) {
        super(message);
    }
}
```

Change `extends Exception` to `extends RuntimeException` and it becomes **unchecked**.

| Base class | Resulting type | When to use |
|---|---|---|
| `extends Exception` | Checked | Business rule violated (insufficient balance, order not found) |
| `extends RuntimeException` | Unchecked | Programming error (invalid argument shape) |

A custom exception that adds no fields should still override the constructor and pass the message to
`super`. If you want a `code` field, add a getter — do not expose the field publicly.

### The compiler's decision, stated as a rule

For every `catch (X e)` clause, `javac` asks:

> "Can an exception of type `X` be thrown in the body of this `try`?"

- If the body can throw `X` → fine.
- If the body can throw a **subtype** of `X` → fine.
- If `X` is `Exception` or `Throwable` → **always fine**, regardless of the body.
- If `X` is a **checked** exception and the body cannot throw it → **compile error**:
  `exception IOException is never thrown in body of corresponding try statement`.

That last row is the trap. `try { int x = 1 / 0; } catch (IOException e) { }` does **not** compile,
even though the body obviously throws something.

## Worked example

**Q. Which of the following statements is TRUE?**

```java
class MyEx extends RuntimeException { }
```

A. `MyEx` must be caught or declared with `throws`.
B. `MyEx` can be caught but does not have to be.
C. `MyEx` extends `Error`.
D. `MyEx` cannot be used in a `throw` statement.

**Solution**

| Step | Check | Result |
|---|---|---|
| 1 | `MyEx` extends `RuntimeException` | It is an **unchecked** exception |
| 2 | Unchecked exceptions need no declaration or catch | The compiler never forces you to handle it |
| 3 | `RuntimeException` is under `Exception`, not `Error` | C is false |

**Answer: B.**

**Why the distractors fail**

| Option | Why it is wrong |
|---|---|
| A | That obligation applies to **checked** exceptions only |
| C | `Error` and `RuntimeException` are siblings, not parent and child |
| D | `throw new MyEx()` is perfectly legal |

**Follow-up (same family, different answer):** if `MyEx` had extended `Exception` instead, the
answer to A would be the correct one.

## Quick rules

- **Unchecked = `RuntimeException` + `Error`.** Memorise those two names; you can rebuild the tree.
- `Throwable` is the root. `Exception` and `Error` are its two direct children.
- `throw` = raise. `throws` = declare.
- A checked exception that the `try` body cannot throw → **compile error**.
- `catch (Exception e)` and `catch (Throwable e)` are **always** legal.
- `catch (Error e)` is legal but almost always a bug in your design.
- A custom exception extending `Exception` is checked; extending `RuntimeException` is unchecked.
- `ArithmeticException` (÷0), `NullPointerException`, `ArrayIndexOutOfBoundsException`,
  `ClassCastException`, `NumberFormatException` are all unchecked — no `catch` required.

## Common traps

| Trap | What you will say | The truth |
|---|---|---|
| "All exceptions are unchecked" | Nothing needs catching | `IOException` is checked and the compiler enforces it |
| "Catching `Exception` catches `Error`" | One `catch` handles everything | `Error` is a sibling of `Exception` under `Throwable`; use `Throwable` for both |
| "`throws` means it throws" | The method definitely throws | `throws` only *declares* that it might |
| "Catching a checked exception you never see is fine" | Compiles | Compile error: "never thrown in body of corresponding try statement" |
| "`NumberFormatException` is checked" | Must declare it | It extends `IllegalArgumentException` → `RuntimeException` → unchecked |
| "Custom exceptions are always checked" | Must declare | Only if they extend `Exception` directly |

## Checklist

- [ ] I can draw the `Throwable` tree with `Error` and `Exception` as siblings.
- [ ] I can name the two unchecked branches without looking.
- [ ] I know that `catch (Exception e)` never fails to compile for the "never thrown" reason.
- [ ] I can write a custom checked exception with a constructor in 3 lines.
- [ ] I never mix up `throw` and `throws` in an exam answer.

## Related

- [try/catch/finally and resource management](../01-concepts/02-try-catch-finally-and-resource-management.md)
- [Trace the exception path](../02-techniques/01-trace-the-exception-path.md)
- [Choose the right catch strategy](../02-techniques/02-choose-the-right-catch-strategy.md)
- [Solved exception set](../03-worked-examples/01-solved-exception-set.md)
- [Exception traps](../04-pitfalls/01-exception-traps.md)
- [Exception one-pager](../05-reference/01-exception-one-pager.md)
- [Topic overview](../README.md)
