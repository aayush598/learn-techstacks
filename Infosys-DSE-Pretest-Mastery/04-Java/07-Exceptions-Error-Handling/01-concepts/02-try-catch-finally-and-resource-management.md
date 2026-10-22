# try / catch / finally, Return Interaction, and Resource Management

> Section 4 · Java · Exceptions & Error Handling · _Estimated reading time: 10 min_
> **Prerequisite:** [Throwable hierarchy, checked vs unchecked](01-throwable-hierarchy-and-checked-vs-unchecked.md)

## In one sentence

`finally` runs on **every** path out of a `try` block — normal, caught, or propagating — and a
`return` inside `finally` **discards** whatever value `try` or `catch` was about to return.

## Why the pre-test tests this

- "What does this print?" is a reported archetype, and `try/catch/finally` is the most common place
  to hide one.
- The `finally`-overrides-`return` rule produces a different printed answer from what most candidates
  expect — it is a designed trap, and it appears every year.
- `finally` not running after `System.exit()` is the rarer version of the same trap.

## Core concept

### The execution table

| Situation | `try` body | `catch` | `finally` | Value returned | Output |
|---|---|---|---|---|---|
| 1 | completes | — | has `return X` | **X** (finally wins) | finally's own prints |
| 2 | completes | — | no `return` | value from `try` | finally's prints, then the value |
| 3 | throws, matching catch exists | runs | no `return` | value from `catch` (if any) | catch's prints + finally's prints |
| 4 | throws, matching catch exists | runs | has `return X` | **X** | catch's prints + finally's prints |
| 5 | throws, no matching catch | skipped | runs (if reached) | none — propagates | finally's prints, then the stack trace |
| 6 | `System.exit()` called | — | **skipped** | none | JVM exits immediately |

Two rules do all the work:

1. **`finally` runs last on every path except `System.exit()` (and JVM halt).**
2. **A `return` in `finally` replaces the pending return value.**

### The canonical trap, side by side

```java
static int a() {
    try { return 1; }                 // pending value = 1
    finally { return 2; }             // returns 2; the 1 is thrown away
}
static int b() {
    try { return 1; }                 // pending value = 1 (already computed & saved)
    finally { System.out.print("F"); } // no return → the 1 survives
}
```

`a()` returns **2**. `b()` prints `F` and returns **1**.

The distinction is subtle and worth stating precisely: in `b()` the value `1` is **captured before**
`finally` runs, so `finally` cannot change it unless it explicitly returns. In `a()` `finally`
performs its own return, which wins outright. `javac` accepts both, but `a()` is a code smell — the
compiler even warns about it in some IDEs.

### `finally` vs `System.exit()`

```java
public static void main(String[] args) {
    try {
        System.out.println("A");
        System.exit(0);
    } finally {
        System.out.println("B");     // NEVER printed
    }
}
```

Output is exactly:

```
A
```

`System.exit()` starts JVM shutdown. `finally` blocks of the running thread are **not** executed.
Shutdown hooks (`Runtime.getRuntime().addShutdownHook(...)`) *do* run — that is the only hook you get.

### An exception in `finally` swallows the original

```java
static void m() {
    try {
        throw new RuntimeException("Original");
    } finally {
        throw new IllegalStateException("From finally");
    }
}
```

The `RuntimeException("Original")` is **discarded**. The caller sees only
`java.lang.IllegalStateException: From finally`. The original stack trace is gone — there is no
"suppressed" list here, because that mechanism only exists inside try-with-resources.

### Try-with-resources (Java 7+)

```java
try (BufferedReader br = new BufferedReader(new FileReader("data.txt"));
     PrintWriter pw = new PrintWriter("out.txt")) {
    // ...
}
```

- Every resource is closed automatically, in **reverse order of declaration** (`pw` first, then `br`).
- `close()` runs whether the body completes normally or throws.
- If the body throws **and** `close()` also throws, the body's exception is the one that propagates
  and the `close()` exception is attached to it as a **suppressed** exception
  (`primary.getSuppressed()`).
- The declared type must implement `AutoCloseable`. Only one resource may be declared as
  `var x = ...` in Java 8 — Java 9 added the "effectively final resource variable" form.
- If the initialisation of the *second* resource throws, the *first* one is still closed.

Without try-with-resources you write `finally { br.close(); }` — and if the body already threw, the
`close()` failure replaces the original exception. That is the bug try-with-resources was designed
to remove.

### Propagation

An exception that no `catch` in the current method handles **propagates to the caller**. The stack
is unwound one frame at a time. Each frame's `finally` blocks run on the way out.

```java
class A { void m() { throw new RuntimeException("boom"); } }
class B extends A { void m() { super.m(); } }   // no catch → propagates out of B.m() too
```

In `main`, an uncaught exception prints a stack trace to **stderr** and the JVM exits with a
**non-zero status code**. The program does **not** print "after" statements in `main` after the throw.

### Multi-catch (Java 7+)

```java
try {
    // ...
} catch (IOException | SQLException e) {
    // e is effectively final; its static type is the LUB of IOException and SQLException
}
```

- The alternatives must be **unrelated** (neither may be a subtype of the other).
- The order of the alternatives does **not** matter.
- You cannot catch a subclass and its superclass in the same multi-catch.

## Worked example

**Q. What is printed?**

```java
public class Main {
    static String f() {
        try {
            return "try";
        } catch (Exception e) {
            return "catch";
        } finally {
            return "finally";
        }
    }
    public static void main(String[] args) {
        System.out.println(f());
    }
}
```

**Solution**

1. `try` executes `return "try"` → a pending return value of `"try"` is created.
2. No exception was thrown, so `catch` is skipped.
3. `finally` runs, and it **performs its own `return`**.
4. A return inside `finally` overrides the pending value. The pending `"try"` is discarded.

**Output (exact):**

```
finally
```

**Why the distractors fail**

| Option | Why it is wrong |
|---|---|
| `try` | The pending return is discarded by the `finally` block's own return |
| `catch` | No exception is thrown, so `catch` never runs |
| `try finally` | `finally` has no print statement; it only returns |
| Compile error | `javac` accepts a `finally` with a `return` (it only warns) |

**Second variant, same skeleton:** if the `finally` block were `System.out.print("F");` with no
`return`, the output would be exactly `F` and then `try` — on two separate lines:

```
F
try
```

## Quick rules

- `finally` runs on the normal path, the caught path, and the propagating path. **Only
  `System.exit()` skips it.**
- A `return` in `finally` **wins**. A print in `finally` does not change a pending return value.
- An exception in `finally` **replaces** the original exception and the original is lost.
- Try-with-resources closes in **reverse declaration order** and preserves the primary exception.
- An uncaught exception → stack trace on stderr → non-zero exit code → nothing after the throw runs.
- `catch` blocks are tried **top to bottom**; the first match wins.
- Multi-catch alternatives must be unrelated types.

## Common traps

| Trap | The wrong answer you will pick | The right answer |
|---|---|---|
| `finally` only runs on the error path | "try" then "finally" | It runs **before** the method returns, always |
| `return` in `try` wins over `return` in `finally` | "try" | `finally` wins: the pending value is discarded |
| `System.exit()` still runs `finally` | "A" then "B" | Only "A" |
| Exception in `finally` keeps the original | "Original" | The `finally` exception replaces it |
| `catch (Exception e)` catches `Error` | "everything is caught" | `Error` is a **sibling** of `Exception` |
| Try-with-resources closes in declaration order | "br closed first" | Reverse order: last declared closes first |

## Checklist

- [ ] I can recite the execution table from memory.
- [ ] I know that `finally` is skipped **only** by `System.exit()`.
- [ ] I can state what happens to an exception thrown inside `finally`.
- [ ] I know the closing order of try-with-resources resources.
- [ ] I know that an uncaught exception kills the program with a non-zero exit code.

## Related

- [Throwable hierarchy, checked vs unchecked](01-throwable-hierarchy-and-checked-vs-unchecked.md)
- [Trace the exception path](../02-techniques/01-trace-the-exception-path.md)
- [Choose the right catch strategy](../02-techniques/02-choose-the-right-catch-strategy.md)
- [Solved exception set](../03-worked-examples/01-solved-exception-set.md)
- [Exception traps](../04-pitfalls/01-exception-traps.md)
- [Exception one-pager](../05-reference/01-exception-one-pager.md)
- [Topic overview](../README.md)
