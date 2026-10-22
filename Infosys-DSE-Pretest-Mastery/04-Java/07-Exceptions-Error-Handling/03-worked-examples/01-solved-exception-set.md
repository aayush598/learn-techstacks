# Exceptions — 10 Solved Questions

> Section 4 · Java · Exceptions & Error Handling · _Estimated reading time: 16 min_
> **Prerequisite:** [Trace the exception path](../02-techniques/01-trace-the-exception-path.md)

## In one sentence

Every answer below is produced by the same 6 steps — **find the throw site, name the type, find the
first matching catch, run `finally`, settle the return value, write the exact string**.

## Why the pre-test tests this

- The Java section has 25 questions; exception handling and "does it run?" questions together
  typically take 4–6 of them.
- Each question below has exactly one defensible answer. Where the exam's wording is ambiguous, the
  question is phrased so that only one option is guaranteed.
- Java 8 semantics assumed throughout.

## Core concept

The three rules that decide most of these questions:

| Rule | Effect |
|---|---|
| `finally` runs on every path except `System.exit()` | It always appears in the output |
| A `return` inside `finally` discards the pending value | `finally` wins |
| A `catch` clause after a clause for its supertype is a compile error | Order matters |

## Worked example

### Q1 — Answer: **the program prints `finally`**

```java
public class Main {
    static String f() {
        try { return "try"; }
        catch (Exception e) { return "catch"; }
        finally { return "finally"; }
    }
    public static void main(String[] args) {
        System.out.println(f());
    }
}
```

**Solution** — `try` creates a pending return value `"try"`. No exception → `catch` skipped.
`finally` executes its own `return`, which **discards** the pending value.

**Output (exact):**

```
finally
```

**Distractors** — `try`: the pending value is discarded. `catch`: no exception was thrown.
`try catch finally`: nothing prints `catch`.

---

### Q2 — Answer: **it does not compile**

```java
import java.io.IOException;
public class Main {
    public static void main(String[] args) {
        try {
            System.out.println("hi");
        } catch (Exception e) {
            System.out.println("generic");
        } catch (IOException e) {
            System.out.println("io");
        }
    }
}
```

**Solution** — `IOException` is a **subclass** of `Exception`. The `Exception` clause comes first and
already covers it, so the `IOException` clause is unreachable.

```
error: exception IOException has already been caught
```

**Distractors** — "It compiles and prints `hi`": the compile check runs first, so this never happens.
"Compile error, prints nothing": a compile error means the program never runs, which is the correct
idea, but you should name the reason.

---

### Q3 — Answer: **it prints `A` only**

```java
public class Main {
    public static void main(String[] args) {
        try {
            System.out.println("A");
            System.exit(0);
        } finally {
            System.out.println("B");
        }
    }
}
```

**Solution** — `System.exit(0)` starts JVM shutdown immediately. `finally` blocks of the running
thread are **not** executed.

**Output (exact):**

```
A
```

**Distractors** — `A` then `B`: `finally` does not run after `System.exit()`. `B` only: `A` is
printed before the exit call. "Runtime error": `System.exit(0)` is a normal, successful termination.

---

### Q4 — Answer: **`IllegalStateException`, and the original is lost**

```java
public class Main {
    public static void main(String[] args) {
        try {
            throw new RuntimeException("Original");
        } finally {
            throw new IllegalStateException("From finally");
        }
    }
}
```

**Solution** — the `finally` block throws. The exception in flight is **replaced** by the new one.
The `RuntimeException("Original")` is discarded, and because this is not a try-with-resources block
it is not even recorded as a suppressed exception.

**Output (exact)** — on **stderr**:

```
Exception in thread "main" java.lang.IllegalStateException: From finally
	at Main.main(Main.java:8)
```

(The stack-trace line numbers depend on the file layout; only the first line is fixed.)

**Distractors** — "Prints `Original`": the original never surfaces. "Prints both": only one exception
escapes a method. "Compile error": both are unchecked, so it compiles.

---

### Q5 — Answer: **it does not compile**

```java
import java.io.IOException;
public class Main {
    public static void main(String[] args) {
        try {
            int x = 10 / 2;
        } catch (IOException e) {
            System.out.println("io");
        }
    }
}
```

**Solution** — `IOException` is **checked**. The `try` body cannot throw it (integer division by a
non-zero literal cannot throw `IOException`). The rule that makes this a compile error is the
"never thrown" rule, and it applies only to **checked** types.

```
error: exception IOException is never thrown in body of corresponding try statement
```

**Distractors** — "It compiles and prints nothing": the compile check happens first. "It throws
`ArithmeticException`": `10 / 2` does not throw anything at all.

---

### Q6 — Answer: **`true`, and it prints `1`**

```java
public class Main {
    public static void main(String[] args) {
        int a = 0;
        boolean r = (a++ > 0) || (a++ > 0);
        System.out.println(r);
        System.out.println(a);
    }
}
```

**Solution** — `||` is **short-circuiting**, but short-circuiting only skips the right side when the
left side is *true*. Here the left side is `0 > 0` → `false` (and `a` becomes 1), so the right side
**does** run: `1 > 0` → `true` (and `a` becomes 2).

**Output (exact):**

```
true
2
```

**Distractors** — `false` then `1`: the right operand is evaluated because the left was false.
`true` then `1`: `a++` in the second operand runs too, giving 2.

---

### Q7 — Answer: **it prints `init` then `use`**

```java
class Resource implements AutoCloseable {
    Resource() { System.out.println("init"); }
    void use()  { System.out.println("use"); }
    public void close() { System.out.println("close"); }
}
public class Main {
    public static void main(String[] args) {
        try (Resource r = new Resource()) {
            r.use();
        }
    }
}
```

**Solution** — try-with-resources: the resource is initialised (prints `init`), the body runs
(prints `use`), then `close()` is called automatically (prints `close`).

**Output (exact):**

```
init
use
close
```

**Distractors** — missing `close`: the whole point of try-with-resources is automatic closing.
`init` then `close` only: the body statement still runs.

---

### Q8 — Answer: **`java.lang.ClassCastException`**

```java
public class Main {
    public static void main(String[] args) {
        Object o = Integer.valueOf(42);
        String s = (String) o;
        System.out.println(s);
    }
}
```

**Solution** — the cast is checked at runtime. `Integer` and `String` are unrelated, so the cast
fails with `ClassCastException` (unchecked). The `println` never runs.

**Output (exact)** — on stderr:

```
Exception in thread "main" java.lang.ClassCastException: java.lang.Integer cannot be cast to java.lang.String
```

**Distractors** — "It prints `42`": `Integer.toString()` is not what a cast does.
"Compile error": casts between unrelated reference types are legal at compile time.

---

### Q9 — Answer: **it compiles; prints `try` after `F`**

```java
public class Main {
    static int f() {
        try {
            return 1;
        } finally {
            System.out.print("F");
        }
    }
    public static void main(String[] args) {
        System.out.println(f());
    }
}
```

**Solution** — `try` creates the pending value `1`. `finally` prints `F` but contains **no return**,
so the pending value survives. The method returns `1`.

**Output (exact):**

```
F1
```

(The `F` has no newline; `println(1)` supplies the newline at the end.)

**Distractors** — `1` then `F`: `finally` runs *before* the method returns. `F` then `2`: there is no
return in `finally` to override the value.

---

### Q10 — Answer: **the method declares `throws IOException`, which is the compile-time contract**

```java
import java.io.IOException;
public class Main {
    static void read() throws IOException {
        throw new IOException("file missing");
    }
    public static void main(String[] args) {
        try {
            read();
        } catch (IOException e) {
            System.out.println(e.getMessage());
        }
    }
}
```

**Solution** — `read()` **declares** `throws IOException` (a checked exception), so its caller must
handle it. `main` does, with a `catch`. The body throws `new IOException("file missing")`, and
`getMessage()` returns exactly that message.

**Output (exact):**

```
file missing
```

**Distractors** — "Compile error, `throws` means it throws": `throws` is a declaration, and `main`
handles the exception correctly. "Prints `java.io.IOException: file missing`": that is what
`printStackTrace()` or `toString()` would give; `getMessage()` gives only the message text.

## Quick rules

- `finally` beats a pending `return` only if `finally` **has** a `return`.
- `System.exit()` skips `finally`.
- An exception in `finally` replaces the original.
- Catch order: subclass before superclass, else compile error.
- Checked exception in a `catch` that the body cannot throw → compile error.
- `||` short-circuits only when the left side is `true`; `&&` only when the left side is `false`.
- `getMessage()` → the message only. `getCause()` → the wrapped exception (or `null`).

## Common traps

| Trap | Seen in | Fix |
|---|---|---|
| Believing `finally` always runs | Q3 | It does not run after `System.exit()` |
| Believing a pending return survives a `return` in `finally` | Q1 | The `finally` return wins |
| Believing the original exception survives an exception in `finally` | Q4 | It is discarded |
| Believing `catch (Exception e)` covers a checked exception the body cannot throw | Q5 | That is a compile error |

## Checklist

- [ ] I got Q1 right (finally's return wins) without hesitating.
- [ ] I got Q3 right (`System.exit` skips `finally`).
- [ ] I can name the two javac messages for catch-order and never-thrown.
- [ ] I can state the exact output of Q9 (`F1`).
- [ ] I finished all 10 in under 16 minutes (≈ 95 s each).

## Related

- [Throwable hierarchy, checked vs unchecked](../01-concepts/01-throwable-hierarchy-and-checked-vs-unchecked.md)
- [try/catch/finally and resource management](../01-concepts/02-try-catch-finally-and-resource-management.md)
- [Trace the exception path](../02-techniques/01-trace-the-exception-path.md)
- [Choose the right catch strategy](../02-techniques/02-choose-the-right-catch-strategy.md)
- [Exception traps](../04-pitfalls/01-exception-traps.md)
- [Exception one-pager](../05-reference/01-exception-one-pager.md)
- [Topic overview](../README.md)
