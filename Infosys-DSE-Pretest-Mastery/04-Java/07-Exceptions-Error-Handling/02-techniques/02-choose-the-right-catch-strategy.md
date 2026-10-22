# Choose the Right Catch Strategy — Matching, Ordering, and Multi-Catch

> Section 4 · Java · Exceptions & Error Handling · _Estimated reading time: 8 min_
> **Prerequisite:** [Throwable hierarchy, checked vs unchecked](../01-concepts/01-throwable-hierarchy-and-checked-vs-unchecked.md)

## In one sentence

`catch` clauses are tested **top to bottom** and the first one whose type matches wins — a
**subclass after its superclass is a compile error**, while a **superclass before its subclass is
perfectly legal**.

## Why the pre-test tests this

- "Which catch block will handle the exception?" is a standard one-marker with 4 options.
- "Does this compile?" is a reported archetype, and catch ordering is one of the few compile-error
  rules that are not obvious.
- Multi-catch and `catch (Exception e)` breadth are cheap points once you know the rules.

## Core concept

### The matching rule

Given a thrown exception of runtime type `T`, a `catch (C e)` clause matches if:

```
C is the same type as T, OR  C is a supertype of T
```

Matching is **not** based on the declared type of the variable being thrown — it is based on the
**actual object**.

| Thrown | `catch (Exception e)` | `catch (RuntimeException e)` | `catch (IOException e)` |
|---|---|---|---|
| `NullPointerException` | ✅ matches | ✅ matches | ❌ |
| `IOException` | ✅ matches | ❌ | ✅ matches |
| `Error` | ❌ | ❌ | ❌ |

### The ordering rule — and the compile error hiding in it

| Source order | Result |
|---|---|
| `catch (IOException e)` **then** `catch (Exception e)` | ✅ **Legal.** The specific one is tried first and wins. |
| `catch (Exception e)` **then** `catch (IOException e)` | ❌ **Compile error:** `exception IOException has already been caught` |

**Rule:** a `catch` clause that can never be reached because an earlier clause already covers it is a
compile error. "Already covers it" means *the earlier clause's type is a supertype of this one*.

The error message is exactly:

```
error: exception IOException has already been caught
```

### The three compile-error families in `catch`

| Family | Example | javac message |
|---|---|---|
| **Unreachable catch** | `catch (Exception e)` before `catch (IOException e)` | `exception IOException has already been caught` |
| **Never thrown** | `catch (IOException e)` around a body that cannot throw it | `exception IOException is never thrown in body of corresponding try statement` |
| **Checked exception not handled** | `throw new IOException()` with no `catch` and no `throws` | `unreported exception java.io.IOException; must be caught or declared to be thrown` |

The "never thrown" rule has one important exception:

> `catch (Exception e)` and `catch (Throwable e)` are **always legal**, whatever the body does,
> because the body can always throw *something* unchecked.

### Multi-catch (Java 7+)

```java
try {
    readConfig();
} catch (IOException | SQLException e) {
    System.out.println("problem: " + e.getMessage());
}
```

| Rule | Detail |
|---|---|
| Alternatives must be **unrelated** | `catch (IOException | FileNotFoundException e)` → compile error, `FileNotFoundException` is a subclass of `IOException` |
| Order does not matter | Unlike single `catch`, multi-catch has no "first match" semantics |
| The variable is **effectively final** | You cannot reassign `e` inside the block |
| Its static type is the **common supertype** | `e.getMessage()` works; `e.readObject()` does not compile without a cast |
| Java 8 adds **precise rethrow** | `catch (IOException | SQLException e)` with `throw e;` rethrows the *actual* type, so the method only needs `throws IOException, SQLException` |

### Choosing what to catch — a decision table

| Situation | Catch | Why |
|---|---|---|
| You can recover meaningfully | The narrowest type that covers it | Recovery logic belongs close to the failure |
| You must clean up | `finally` (or try-with-resources) | `finally` runs on every path |
| You must translate the exception | `catch (IOException e) { throw new MyException(e); }` | Keep the cause with `initCause` / the constructor |
| You are at the API boundary | `catch (Exception e)` and convert to a response | Last resort; log it |
| You cannot handle it at all | Do not catch it | Let it propagate — `throws` it up |

### Custom exception with a cause

```java
class OrderFailedException extends Exception {
    OrderFailedException(String message, Throwable cause) {
        super(message, cause);          // Throwable(String, Throwable) — Java 6+
    }
}
```

```java
try {
    placeOrder();
} catch (SQLException e) {
    throw new OrderFailedException("could not place order", e);
}
```

Now `e.getCause()` returns the original `SQLException`. Without the cause chain, the root cause is
lost — and `getCause()` returning `null` is a common exam question.

## Worked example

**Q. Does the following compile?**

```java
public class Main {
    public static void main(String[] args) {
        try {
            int x = 10 / 0;
        } catch (ArithmeticException e) {
            System.out.println("arith");
        } catch (Exception e) {
            System.out.println("generic");
        }
    }
}
```

**Step 1 — Is any catch clause a subtype of an earlier one?** `ArithmeticException` is a subclass of
`Exception`, and it appears **first**. A subclass before its superclass is legal.

**Step 2 — Could the body throw a checked exception that is never caught?** The body can only throw
`ArithmeticException` (unchecked). `catch (Exception e)` is always legal regardless.

**Step 3 — Compile?** Yes.

**Step 4 — What would it print?** `10 / 0` throws `ArithmeticException: / by zero` → the first catch
matches → prints `arith`.

**Answer: It compiles, and prints `arith`.**

**Why the distractors fail**

| Option | Why it is wrong |
|---|---|
| "Does not compile — `Exception` catch is unreachable" | The **specific** type comes first; only the reverse order is an error |
| "Does not compile — `ArithmeticException` is never thrown" | It **is** thrown by `10 / 0`; and it is unchecked anyway |
| Prints `generic` | The first matching clause wins |
| Prints both `arith` and `generic` | Only one catch clause runs |

**The mirror-image trap:** swap the two `catch` clauses and the code **stops compiling**:

```
error: exception ArithmeticException has already been caught
```

## Quick rules

- First matching `catch` **top to bottom** wins.
- **Subclass first, superclass later = legal. Superclass first, subclass later = compile error.**
- `catch (Exception e)` and `catch (Throwable e)` are always legal.
- A checked exception in the `catch` that the body cannot throw → compile error.
- Multi-catch alternatives must be unrelated types.
- One `catch` clause runs per exception — never two.
- Keep the cause: `new MyException(msg, e)` so `getCause()` works.

## Common traps

| Trap | The wrong answer | The right answer |
|---|---|---|
| "Superclass must come first" | Compile error | Superclass-first is the error; subclass-first is fine |
| `catch (Exception e)` catches `Error` | "catches everything" | `Error` is a sibling; you need `Throwable` |
| Both matching catches run | Two lines of output | Only the first one runs |
| Multi-catch order matters | Reordering changes behaviour | It does not |
| `catch (IOException e)` around pure arithmetic | Compiles | Compile error — never thrown |

## Checklist

- [ ] I check catch order **before** I check the body.
- [ ] I know the exact javac wording: "already been caught" and "never thrown in body of
      corresponding try statement".
- [ ] I know multi-catch alternatives must be unrelated.
- [ ] I can say which one of two matching catches runs.
- [ ] I remember to pass the cause into a custom exception.

## Related

- [Throwable hierarchy, checked vs unchecked](../01-concepts/01-throwable-hierarchy-and-checked-vs-unchecked.md)
- [try/catch/finally and resource management](../01-concepts/02-try-catch-finally-and-resource-management.md)
- [Trace the exception path](01-trace-the-exception-path.md)
- [Solved exception set](../03-worked-examples/01-solved-exception-set.md)
- [Exception traps](../04-pitfalls/01-exception-traps.md)
- [Exception one-pager](../05-reference/01-exception-one-pager.md)
- [Topic overview](../README.md)
