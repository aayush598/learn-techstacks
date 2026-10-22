# Trace the Exception Path — a 6-step procedure

> Section 4 · Java · Exceptions & Error Handling · _Estimated reading time: 8 min_
> **Prerequisite:** [try/catch/finally and resource management](../01-concepts/02-try-catch-finally-and-resource-management.md)

## In one sentence

Every exception question reduces to **one line of executed code at a time**: find the throw site,
name the type, find the first matching `catch`, then run `finally`, then settle the return value.

## Why the pre-test tests this

- Output-prediction questions in the Java section are usually 8–12 lines of code. You cannot "read
  and hope" — you need a procedure.
- The procedure is also how you answer "does this compile / does this run", which is a *separate*
  reported archetype.
- At 90 seconds per question, a 6-step trace takes ~45 seconds and leaves 45 seconds of slack.

## Core concept

### The 6-step trace

**Step 1 — Build the execution table.** Write one row per line of code in the order it executes.
For output questions this table becomes your answer.

**Step 2 — List every throw site.** A throw site is:
- an explicit `throw new X(...)`,
- a call to a method that declares `throws X`,
- an operation that throws by itself: `/` by zero, array index out of bounds, null dereference,
  `ClassCastException` from a bad cast, `NumberFormatException` from `Integer.parseInt("x")`.

**Step 3 — Name the type of each throw site.** If the code shows `throw new ...`, the type is given.
If it is an implicit throw, you must know the JDK rule:

| Implicit throw | Exception type |
|---|---|
| `int a = 0; a / b;` where `b == 0` | `ArithmeticException` (`/ 0` only; `% 0` also) |
| `arr[5]` where `arr.length == 3` | `ArrayIndexOutOfBoundsException` |
| `obj.field` where `obj == null` | `NullPointerException` |
| `(String) someObject` where the object is an `Integer` | `ClassCastException` |
| `Integer.parseInt("abc")` | `NumberFormatException` |
| `int x = Integer.valueOf(null)` | `NullPointerException` (unboxing null) |

**Step 4 — Match the catch.** Walk the `catch` clauses top to bottom. The first clause whose
parameter type is the thrown type **or a supertype of it** wins. If no clause matches, the exception
propagates out of the method.

**Step 5 — Run `finally` (if present).** It runs after the catch (or after the pending return is
created). Check for a `return` inside it — that changes the outcome.

**Step 6 — Settle the return value.** Use this exact precedence:

```
finally has a return  →  that value is returned
otherwise            →  the pending value from try (normal path) or catch (caught path)
no pending value     →  the exception propagates
```

### The 4 question types and what they need

| Question type | What you must produce | Steps you need |
|---|---|---|
| "What does it print?" | An exact quoted output string | 1, 2, 3, 4, 5, 6 — all of them |
| "Does this compile?" | Yes / No + the compile error | 2, 3 only (plus catch ordering rules) |
| "Which exception is thrown?" | A type name | 2, 3 |
| "What is printed if the exception is not caught?" | Stack trace on stderr + non-zero exit | 2, 3, 4 (propagation) |

### "Compile or run" — the split

The fastest triage: **does the compiler need to know about an exception at all?**

```
Does the code contain a catch clause for a CHECKED exception type
that the try body cannot throw?
        │ yes
        ▼
COMPILE ERROR
        │ no
        ▼
Does any catch clause appear AFTER a catch of a supertype of itself?
        │ yes
        ▼
COMPILE ERROR  ("already caught")
        │ no
        ▼
Does the code compile?  →  now ask what it prints / what it throws
```

Compile errors that are **not** about exceptions still appear in this archetype (missing return,
unreachable statement, abstract instantiation). For the full catalogue see
[the compile-error catalogue](../../08-Output-Prediction-Patterns/05-reference/02-compile-error-catalogue.md)
in the [Output Prediction topic](../../08-Output-Prediction-Patterns/).

### The 45-second output table

Use this when the code has one `try`, at most two `catch` clauses, and one `finally`:

| Row | Column 1 | Column 2 | Column 3 | Column 4 |
|---|---|---|---|---|
| 1 | `try` runs | `catch` runs | `finally` runs | returned value |

Fill it left to right. Then read the answer off the row.

## Worked example

**Q. What is printed?**

```java
public class Main {
    static void g() {
        try {
            int[] a = new int[2];
            System.out.println(a[5]);
        } catch (ArithmeticException e) {
            System.out.println("arith");
        } catch (ArrayIndexOutOfBoundsException e) {
            System.out.println("aioobe");
        } finally {
            System.out.println("fin");
        }
    }
    public static void main(String[] args) {
        g();
        System.out.println("end");
    }
}
```

**Step 1 — Execution table**

| Step | Code | Output |
|---|---|---|
| 1 | `int[] a = new int[2];` | — |
| 2 | `System.out.println(a[5]);` | — (throws) |
| 3 | `catch (ArithmeticException e)` | not matched |
| 4 | `catch (ArrayIndexOutOfBoundsException e)` | matched → `aioobe` |
| 5 | `finally` | `fin` |
| 6 | back in `main` | `end` |

**Step 2 — Throw sites**: `a[5]` with `a.length == 2` → `ArrayIndexOutOfBoundsException`.

**Step 3 — Type**: `ArrayIndexOutOfBoundsException` (unchecked).

**Step 4 — Match**: `ArithmeticException` does not match (unrelated types). The second `catch` does.

**Step 5 — `finally`**: no `return` → prints `fin`, pending value unaffected.

**Step 6 — Return**: the method returns `void`; execution continues in `main`.

**Output (exact):**

```
aioobe
fin
end
```

**Why the distractors fail**

| Option | Why it is wrong |
|---|---|
| `arith` then `fin` then `end` | The exception is an index error, not an arithmetic error |
| `aioobe` then `end` | The `finally` block always runs |
| `fin` only | The catch clause matched and printed first |
| Compile error | `ArithmeticException` is unchecked, so catching it is always legal |

## Quick rules

- Trace **one line at a time**, never the whole method at once.
- `catch` matching is top-to-bottom, first match wins, supertypes match subclasses.
- `finally` runs last on every path except `System.exit()`.
- `finally` with a `return` beats every pending return value.
- An uncaught exception ends the program — nothing after the throw point in `main` runs.
- For "does it compile", checked-exception rules and catch ordering are 80% of the answer.

## Common traps

| Trap | Fix |
|---|---|
| Reading the whole `try` body before deciding | Read line by line |
| Assuming the first `catch` in the source is the one that matches | It matches only if the type is compatible; check all of them |
| Forgetting `finally` when the catch matched | `finally` runs in **both** cases |
| Treating `catch (Exception e)` as catching everything | It does not catch `Error` |
| Forgetting that an uncaught exception stops `main` | Nothing after the throw runs |

## Checklist

- [ ] I can name the exception type for all six implicit throw sites.
- [ ] I check catch clauses top-to-bottom instead of picking the "obviously right" one.
- [ ] I run `finally` on every path, including the catch path.
- [ ] I check whether `finally` contains a `return` before I settle the output.
- [ ] For compile questions, I check the checked-exception rule first.

## Related

- [Throwable hierarchy, checked vs unchecked](../01-concepts/01-throwable-hierarchy-and-checked-vs-unchecked.md)
- [try/catch/finally and resource management](../01-concepts/02-try-catch-finally-and-resource-management.md)
- [Choose the right catch strategy](02-choose-the-right-catch-strategy.md)
- [Solved exception set](../03-worked-examples/01-solved-exception-set.md)
- [Exception traps](../04-pitfalls/01-exception-traps.md)
- [Exception one-pager](../05-reference/01-exception-one-pager.md)
- [Topic overview](../README.md)
